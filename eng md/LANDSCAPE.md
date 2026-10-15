# Market map: frameworks, models, and no-code

> 📖 View it nicely: `Cmd+Shift+V` (Windows: `Ctrl+Shift+V`).

This file is an overview "map of the terrain". You don't need to learn everything;
it's far more important to **know what exists** and what for, so you can pick the
right tool for the task. The main idea of the whole project: under the hood they
all do the same thing (call the model, give it tools, spin it in a loop) — **only
the syntax changes**.

---

## 1. Frameworks for agents

A framework is a "ready-made kitchen": the agent loop, tool calling, memory, and
handoffs between agents are already written for you. You write less, but you play
by the framework's rules.

### Already covered in this project

| Framework | The idea in one sentence | Folder |
|---|---|---|
| **OpenAI Agents SDK** | a minimalist agent: `Agent` + `Runner` + tools | `02-openai_sdk/` |
| **CrewAI** | a "team of roles": agents with professions split tasks | `03-crewai/` |
| **LangGraph** | an agent as a **graph**: nodes and edges, strong in memory and complex logic | `04-langgraph/` |

### What else is on the market (know that it exists)

| Framework | What for | Worth digging into |
|---|---|---|
| **LangChain** | the "grandfather" of all, a huge ecosystem; LangGraph is part of it | if you need a ready-made integration with almost anything |
| **LlamaIndex** | tailored for **data and RAG** (search over your documents) | when the main thing is answering from a large knowledge base |
| **Pydantic AI** | new, **type-safe**, strict data structures | if you like strict, predictable code |
| **Microsoft AutoGen** | multi-agent "dialogues": agents negotiate with each other | complex scenarios with several AIs |
| **Semantic Kernel** | a Microsoft framework, friendly with .NET / the enterprise world | enterprise development |
| **Google ADK** (Agent Development Kit) | agents in the Google / Vertex AI ecosystem | if you're in Google Cloud |
| **Smolagents** (Hugging Face) | minimalism: an agent in a few lines | a quick prototype |
| **DSPy** | not about agents, but about **auto-tuning prompts** | when you want to "train" prompts instead of writing them by hand |

> 🧭 **Takeaway:** there are dozens of frameworks, but they all share one principle.
> Once you've mastered 2–3 (like in this project), you learn a new one in an evening —
> the wrapper changes, not the essence.

---

## 2. Models (neural networks — the agent's "brain")

The model is the AI that thinks. The agent code is one thing, and the "brain" can be
swapped. In bare code that's done with one line, `PROVIDER = ...`, right at the
top of every file (quick pick: `ollama` / `gemini`); the full list of 7
providers lives in `01-pure_python/llm.py`.

### Local (free, on your computer, via Ollama)

| Model | Note |
|---|---|
| **llama3.2** (Meta) | light and fast, but a bit weak, can mix up languages |
| **qwen2.5** (Alibaba) | **understands many languages noticeably better** — use it for non-English tasks |

Pros: free and private (nothing goes to the cloud). Cons: weaker than the cloud ones,
loads your computer.

### Cloud, international (via API, usually paid)

| Model | Who | Note |
|---|---|---|
| **Claude** | Anthropic | strong at reasoning and working with tools |
| **GPT** | OpenAI | the most famous, a big ecosystem |
| **Gemini** | Google | 🆓 at the time this course was recorded there's **free** access via the API, but the limit is small — only ~20 requests a day per model, see `FAQ.md` |
| **DeepSeek** | DeepSeek | very **cheap** with good quality, OpenAI-compatible |
| **Mistral** | Mistral (Europe) | has a free tier, open models |
| **Grok** | xAI | for general awareness |
| **Perplexity** | Perplexity | answers **with internet search** |

### 🇷🇺 Russian (paid in rubles, no foreign card)

| Model | Who | How to connect |
|---|---|---|
| **YandexGPT** | Yandex | **already works** in `llm.py`: `PROVIDER = "yandex"` + the key and `YANDEX_FOLDER_ID` in `.env` |
| **GigaChat** | Sber | connects via its own scheme — see below |

**Why this matters:** you don't need a foreign card and a foreign account — a common pain.

#### How to connect GigaChat (Sber)

GigaChat isn't "OpenAI-compatible" directly: login is via an **OAuth token**, it has
its own package. In brief:

1. Get access and an `Authorization key` in the GigaChat (Sber) dashboard.
2. Install the package: `uv pip install gigachat`
3. Minimal call:

```python
from gigachat import GigaChat

# verify_ssl_certs=False — a common gotcha: Sber uses its own certificates.
with GigaChat(credentials="YOUR_AUTHORIZATION_KEY", verify_ssl_certs=False) as giga:
    response = giga.chat("Hi! Say one friendly sentence.")
    print(response.choices[0].message.content)
```

> This is a separate path from `llm.py` (there — only OpenAI-compatible providers).
> If GigaChat becomes your main one — you can set up your own `ask()` function by analogy.

---

## 3. No-code / low-code (build an agent with the mouse, without code)

Sometimes no code is needed at all — the logic is assembled from blocks in a visual editor.

| Tool | Known for |
|---|---|
| **n8n** | powerful automation, thousands of integrations, can self-host |
| **Make** (formerly Integromat) | visual "if this → then that" scenarios |
| **Flowise** | a visual builder for LLM apps (based on LangChain) |
| **Langflow** | similar to Flowise, drag-and-drop graphs |
| **Dify** | a platform for AI apps and chatbots with a UI |

**The three-level analogy (as in the README):**

```
bare code (01-pure_python)  ↔  plain CSS    — everything by hand, maximum control
framework (02/03/04)         ↔  Tailwind      — also code, but shorter
no-code (n8n / Flowise)      ↔  Tilda/Webflow — with the mouse, no code
```

---

## How to choose (short cheat sheet)

- **Learning / need maximum control** → bare code + a local model (free).
- **Need a smarter model for free** → Gemini (free tier) or the local qwen2.5.
- **Cost per volume matters** → DeepSeek.
- **Can't use a foreign card** → YandexGPT / GigaChat (rubles).
- **Complex logic / memory / many agents** → a framework (LangGraph, CrewAI).
- **Want no code** → n8n / Flowise.

> Don't chase "the trendiest". Take the simplest thing that solves your task.
