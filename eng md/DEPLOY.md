# Deploy and memory: how to put a bot online without it forgetting the conversation

> 📖 View it nicely: `Cmd+Shift+V` (Windows: `Ctrl+Shift+V`).

This file answers two beginner questions:
1. How do you make a bot **remember** a conversation?
2. How do you put a bot on the internet so it runs **24/7**, not just on your own computer?

---

## Part 0. First — what "memory" actually means for a bot

An AI model **doesn't remember anything by itself**. Every call you make to it is
a blank page: it has no idea what you talked about a minute ago.

A bot's "memory" is an illusion. What actually happens is:
**before every new question, you resend the model the ENTIRE conversation history**,
and it looks like it "remembers" — but really it just read everything from the start.

```
Question 1:                         [Question 1]                                → model answers
Question 2: [Question 1][Answer 1] [Question 2]                                → model answers
Question 3: [Question 1][Answer 1] [Question 2][Answer 2] [Question 3]        → model answers
```

Two practical consequences follow from this:
- The longer the conversation, the more text gets sent every single time — so it's
  **more expensive and slower**.
- You need somewhere to **store** the conversation history, so there's something to
  resend. That's what the rest of this file is about.

There are two kinds of storage like this:

- **Short-term memory** — keep the history while the conversation stays open (one
  session). Close the tab — it's forgotten.
- **Long-term memory** — save the history **to a file/database**, so the bot
  remembers you even after a restart, and separately per user.

---

## Part 0.5. "Is the WHOLE thing really resent every time?" — optimizations

A fair question: if you resend the entire history before every message, isn't that
a mountain of tokens? Let's break it down — there are important nuances.

**First, about size.** Modern models have a **huge context window — up to
1,000,000 tokens** (Gemini, Claude, Qwen3 Max, DeepSeek, etc.; the light local
llama3.2 is around 128k). A million tokens is roughly 700+ pages of text. So the
problem is usually **not that "the history won't fit"** — it almost always fits.

The real problem: even when it fits, pushing a giant context **every single time**
is:
- 💸 **expensive** — you pay for every input token, and you pay for the long history
  AGAIN on each message;
- 🐢 **slow** — the model re-reads everything from scratch;
- 🎯 **worse quality** — on a very long context the model starts to "lose the
  middle" (it notices important things buried mid-history less well).

So the history isn't dragged along "as is" — it's optimized. The main techniques:

| Technique | What it does |
|---|---|
| **Prompt caching** | The provider remembers the unchanged **beginning** of the request and doesn't recompute it. The history is still "sent," but you pay **~10× less** and get a faster reply. Turns on almost automatically (Anthropic / OpenAI / Google). |
| **Sliding window** | Keep only the **last N** messages, just drop the old ones. The simplest approach. |
| **Summarization / compaction** | Replace the old part with a short recap: 20 messages → 2 lines "client Dima, wants a haircut on Friday". |
| **RAG over history** (semantic search) | Store the whole history in a database, and give the model **only the relevant** chunks for the current question (via embeddings) instead of everything. This is how CrewAI works with `memory=True`. |

**The key idea — these are TWO different things (Part 0 blurs them):**
- **what to store** — the whole history, in a file/database, to survive a restart;
- **what of it you actually send/process each time** — this is where caching,
  windowing, summarization and RAG live.

The naive version from Part 0 ("send everything") is when the second problem isn't
solved yet. As conversations grow, you add summarization or RAG, and prompt caching
makes even a big unchanged "tail" of history cost pennies.

> 🧭 At the start (learning bots, short dialogues) you can **ignore all this** —
> "send everything" works great and costs pennies. Optimizations matter once the
> history gets long or you have many users.

---

## Part 1. How to turn this on — for each kind of code

### Bare code (`01-pure_python`)
You assemble the list of messages yourself and send it whole every time (this is
"short-term memory"). In `chat_web.py` this is already done — look at the
`history` variable.

For **long-term** memory (surviving a restart) — save the history to a file or a
database. There's a ready example in `01-pure_python/10_memory.py`.

### OpenAI Agents SDK — `Sessions`
The framework can save the history itself, if you give it a "session" backed by a file/database:
```python
from agents import Agent, Runner, SQLiteSession

# "user_123" is the conversation/user ID. conversations.db is a file on disk.
session = SQLiteSession("user_123", "conversations.db")
result = Runner.run_sync(agent, "Hi!", session=session)
# The next call with session=session and the same ID — the bot remembers the
# previous conversation, even if you restarted the program.
```

### CrewAI — turned on with one flag
```python
crew = Crew(agents=[...], tasks=[...], memory=True)
```
Under the hood CrewAI stores memory locally (as "embeddings" — don't worry about
the details, just know it's a way to store the meaning of text). By default this
needs an `OPENAI_API_KEY` — CrewAI uses OpenAI embeddings for this, even if your
actual chat model is something else.

### LangGraph — the most flexible option (`checkpointer`)
```python
from langgraph.checkpoint.memory import MemorySaver   # stores in RAM (lost on restart)
# from langgraph.checkpoint.sqlite import SqliteSaver  # stores in a file (survives a restart)

graph = builder.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "user_123"}}   # the id of a specific conversation
graph.invoke({...}, config)   # LangGraph fills in the history for this thread_id itself
```

> ⚠️ **Important point.** Sooner or later a conversation will get long enough to
> exceed the model's limit (the "context window" — the maximum amount of text at
> once). When that happens, the old part of the history isn't kept word for word —
> it's **compressed into a short summary**. This is called compaction. Frameworks
> have ready-made settings for this.

---

## Where to host (important)

Our bot is a **Gradio** app — a continuously running server. So it needs a
**regular host** (Render / Railway / Hugging Face Spaces), NOT serverless.

> ⚠️ **Vercel is not a fit for our bot** — it's serverless (the code "wakes up"
> for one request and goes back to sleep), it's for JS websites, and Gradio
> doesn't live on it. (Vercel + Supabase is a great combo, but for a Next.js
> frontend, not a Python-Gradio bot.) For all hosts and pricing — see `HOSTING.md`.

Next — deploying **in two steps**: first just put the bot online (Step 1), then
connect a **Supabase** database so it remembers bookings (Step 2). Below I show
**Render**; Railway is almost the same, and **Hugging Face Spaces** is the simplest
free option for Gradio.

---

## Step 1. Put the bot online (talk within a session)

Goal of this step: the bot works at a public link and remembers the conversation
**while the chat is open** (one session). Client bookings are still in a file and
can be lost on a server restart — we fix that in Step 2.

### What exactly you deploy (a nuance)

Files in `01-pure_python` (`03_judge.py`, `06_router.py` …) are scripts: they run,
print to the terminal, and exit. They **can't be deployed** — there's nobody to
talk to them.

You deploy a file that **keeps listening for messages**:
- `chat_web.py` — a simple Gradio chat;
- `05-example_bot/bot.py` — our barbershop bot (we'll use this one).

### Preparing the bot for a server (3 things — already done in the project)

1. **Cloud model.** There's no Ollama on a server, so `bot.py` has
   `PROVIDER = "gemini"`. Needs the `GOOGLE_API_KEY` key.
2. **`gradio` in `requirements.txt`.** The host installs only what's listed there —
   without this line the bot won't build.
3. **The host's port.** The bot already reads it itself:
   ```python
   .launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
   ```

### Deploying on Render — step by step

1. **Push the project to GitHub** (see `RESOURCES.md`, or ask Claude to help with `git`).
2. **render.com → New → Web Service** → connect your repository.
3. Set the commands:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python 05-example_bot/bot.py`
4. **Environment** → add `GOOGLE_API_KEY = your_key` (like in `.env` on your computer).
5. **Create Web Service** → Render builds the project and gives you a **public link**.
6. Open the link — chat with the bot in the browser. 🎉

> ⚠️ On the free tier Render's service **"falls asleep"** after ~15 minutes idle;
> the first request after a pause answers in ~30–60 seconds — that's normal.

> **Railway:** *New Project → Deploy from GitHub → Start Command → keys in Variables*.
> **Hugging Face Spaces:** create a Space, upload the files, and it brings up the
> chat itself — the simplest free path for Gradio. See `HOSTING.md`.

Done: the bot is live and answering. But client bookings are still in a file on the
server, which gets wiped on a restart/redeploy. To stop losing bookings → Step 2.

---

## Step 2. Connect Supabase (so the bot remembers bookings FOREVER)

**Supabase is a cloud Postgres database** with a handy admin UI. It lives
**separately** from the bot: you can redeploy, restart, or move the bot to another
host — and the bookings stay in the database.

Our `bot.py` is **already ready** for this. The `record_lead` function looks at the
`DATABASE_URL` variable itself:
- if `DATABASE_URL` is set → it writes to the database (Supabase);
- if not → it writes to the `leads.json` file (like locally).

**No code changes needed** — just give the bot the database address.

### Step by step

1. Create a project on **supabase.com** (free).
2. **Settings → Database → Connection string → URI.** Copy a string like:
   ```
   postgresql://postgres:[PASSWORD]@db.xxxx.supabase.co:5432/postgres
   ```
   (`[PASSWORD]` is the one you set when creating the project.)
3. Give this string to the bot as `DATABASE_URL`:
   - **on Render** — Environment → add `DATABASE_URL = postgresql://...`;
   - **locally** (optional) — put `DATABASE_URL=postgresql://...` into `.env`.
     Then even from your laptop the bot writes bookings to the cloud database.
4. Restart the bot. On the first booking it **creates the `leads` table itself**
   (`CREATE TABLE IF NOT EXISTS`) — nothing to set up by hand.

### See the bookings with your own eyes

Supabase → **Table Editor** → the **`leads`** table. A client books in the chat → a
row appears in the table. A clear demonstration of the bot's "real memory".

### Diagram (who lives where)

```
🤖 Bot (Gradio)    →  Render / Railway / HF Spaces
        │  DATABASE_URL
        ▼
🗄️ Database (bookings) →  Supabase (Postgres, separate)
```

### Gotchas (common)

- **SSL.** Supabase requires a secure connection. Usually the URI string works as
  is; if `psycopg2` complains — append `?sslmode=require`.
- **Direct vs pooler.** Supabase gives two strings: **Direct** (port `5432`) and
  **Connection Pooler** (port `6543`). Either works for our bot; if you expect many
  concurrent users — use the pooler (`6543`).
- **Sleeping.** On the free tier a Supabase project sleeps after ~7 days idle — you
  can wake it from the dashboard.

> 💡 Why Supabase is handier than a host's "built-in" database: it's separate — it
> isn't deleted along with the service and moves easily between hosts.

---

## What to add for your specific framework

The difference at deploy time is minimal — install the right package and wire in memory.

### Bare code / Gradio
- Nothing special: `requirements.txt` (it already has `gradio`). The simplest option.

### OpenAI Agents SDK
- In `requirements.txt`: `openai-agents`; the `OPENAI_API_KEY` key.
- Memory: `SQLiteSession(...)` (see Part 1). You write the "listening" part (Gradio/site) yourself.

### CrewAI
- In `requirements.txt`: `crewai`. Model key (`GOOGLE_API_KEY`) plus a separate
  `OPENAI_API_KEY` if memory is on (`memory=True` — embeddings via OpenAI).
- Memory: `Crew(..., memory=True)`.

### LangGraph
- In `requirements.txt`: `langgraph`. Memory: `checkpointer=SqliteSaver(...)` + `thread_id` (see Part 1).
- There's also a "native" **LangGraph Platform** (deploy + memory + monitoring out of the box).

---

## The short route "I just want to test it right now"

1. Push the project to GitHub.
2. On Render, deploy `05-example_bot/bot.py` (Start Command: `python 05-example_bot/bot.py`).
3. Put `GOOGLE_API_KEY` into Environment → open the Render link → chat with the bot. **(Step 1)**
4. When you want bookings to stop getting lost — create a Supabase project and add
   `DATABASE_URL` to Environment. **(Step 2)**
