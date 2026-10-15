# MCP in simple words (Model Context Protocol)

> 📖 View it nicely: `Cmd+Shift+V` (Windows: `Ctrl+Shift+V`).

## Easiest to grasp through an example

Remember the tools from `01-pure_python/11_real_tools.py` (weather, speech,
notifications)? There the tool was "baked into" one bot. **MCP is a way to move
such tools outside**, so anyone can use them, not just one script.
Under the hood — the same "the agent has hands" idea, only the hands are now shared.

## What it is

**MCP is a "USB port" for AI tools.** Before, every tool (weather, a database,
a calendar) had to be baked into a SPECIFIC bot. With MCP you write a "tool server"
**once** — and **any** client understands it: Claude Desktop, Claude Code, your
IDE, other apps.

```
Before:  every bot     →  its own tool code    (all over again)
With MCP: one MCP server  ←  any clients connect (Claude Desktop, IDE, ...)
```

Analogy: USB. One port — and a mouse, a flash drive, a printer all fit the computer.
MCP is the same kind of shared "port", only for AI tools.

## MCP and an ordinary API — what's the difference

A logical question: "but services already have APIs — why also MCP?"

**An API** is a "door" into a specific service (the weather has its own, the CRM
its own, the bank its own). Each door has its own lock, its own rules, its own
manual. For an AI to use ten services, a programmer has to manually write code for
each of the ten APIs separately.

**MCP** is a **single standard on top of these doors**. You wrap a service in an
MCP server once — and after that any AI client uses it **the same way**, without
knowing the details of each API.

| | Ordinary API | MCP |
|---|---|---|
| Standard of access | each service has its own | **one common** for all |
| Who writes the integration | a programmer — for each API by hand | connect the server — and done |
| Who calls it | your code → API | **the AI agent itself** → MCP server |
| A new service appears | write new integration code | just connect its MCP server |

Visually, how the scheme changes:

```
BEFORE (API only):
   your code ──your integration code──> weather API
   your code ──your integration code──> CRM API
   your code ──your integration code──> bank API
   (for each service — separate code, and a programmer writes it)

NOW (via MCP):
                       ┌─> weather MCP server ──> weather API
   AI agent ──one──────>├─> CRM MCP server     ──> CRM API
            way         └─> bank MCP server    ──> bank API
   (the agent talks to all of them THE SAME WAY; the API stays under the hood)
```

> ⚠️ Important: **MCP doesn't replace the API, it sits ON TOP of it.** Inside, an
> MCP server usually calls an ordinary API itself (our `get_weather` under the hood
> goes to the weather site). MCP just makes all tools look and be called **the same
> way** for the AI — the way a USB port hides the differences between a mouse, a
> flash drive, and a printer.

## Why this matters to you

- Write a tool once — use it everywhere there's MCP.
- No need to bake tools into every bot.
- Lots of **ready-made** MCP servers already exist (files, GitHub, databases,
  search, etc.) — you connect them and use them, you don't write them yourself.

## The two sides of MCP

| Side | What it is | Example |
|---|---|---|
| **MCP server** | a program that PROVIDES tools | our `06-mcp/server.py` (weather + calculator) |
| **MCP client** | a program that USES the tools | Claude Desktop, Claude Code, IDE |

The `06-mcp/` folder has a **minimal server** — to get hands-on with how it works.
Running and connecting it — in `06-mcp/README.md`.

## Where to get ready-made MCP servers

There are open catalogs of MCP servers (file system, GitHub, Slack, Postgres, and
much more). They usually connect in a couple of lines of config — no code needed.

## Are there other protocols? (A2A, etc.)

Yes, new ones are appearing. MCP's most notable "neighbor" is **A2A (Agent-to-Agent)**,
a protocol from Google. Don't confuse them — they're about DIFFERENT things:

| Protocol | Who talks to whom | In simple words |
|---|---|---|
| **MCP** (Anthropic) | agent ↔ **tools/data** | "give the AI hands": weather, files, a database |
| **A2A** (Google) | agent ↔ **another agent** | "let agents negotiate with each other" |

That is, MCP connects tools to the AI, while A2A lets several agents (possibly from
different teams and on different frameworks) work together.

> 🧭 This is a young area, the protocols are still settling. No need to memorize
> them — it's enough to know that **MCP = agent and tools**, **A2A = agent and
> agent**. In practice, MCP is what you'll encounter most often right now.
