# Foundations — AI-agent patterns

A learning project: the core patterns for building AI agents, shown at **three
levels** — from bare code to a framework. Every file is densely commented
"for absolute beginners" and equipped with safety guards against errors.

## Project structure

```
foundations-practice/
├── 01-pure_python/     ← LEVEL 1: bare code (everything by hand, maximum control)
│   ├── llm.py       ← engine: any provider (Ollama/Claude/GPT/Gemini)
│   └── 00..13.py    ← patterns (basic, chain, judge, router, tools, ...)
│
├── 02-openai_sdk/      ← LEVEL 2: the same patterns on a FRAMEWORK (OpenAI Agents SDK)
│   └── 01,04,06,09  ← shorter, ready-made blocks
│
├── 03-crewai/          ← LEVEL 2 (another framework): a "team of roles" (CrewAI)
│   └── 01,09        ← Agent + Task + Crew
│
├── 04-langgraph/       ← LEVEL 2 (another framework): "an agent as a graph" (LangGraph)
│   └── 01,03        ← nodes + edges + state, the "judge" loop
│
├── 05-example_bot/     ← 🎯 the REFERENCE consultant bot (all patterns together)
│   └── bot.py + knowledge.txt
│
├── 06-mcp/             ← MCP: your own tool server for the AI (a minimal example)
│   └── server.py + README.md
│
├── chat_web.py      ← a live chat in the browser (Gradio), runs right away
├── requirements.txt
├── .env.example     ← template for keys (copy to .env)
├── RESOURCES.md     ← 🚀 START HERE: what to install so everything works
├── LANDSCAPE.md     ← 🗺️ market map: which frameworks, models, no-code exist
├── PRACTICE.md      ← 🎓 assignment: build your own AI consultant
├── HOSTING.md       ← where bots "live": how to run them 24/7 on the internet
├── GRADIO.md        ← how to make a real chat in the browser (not the terminal)
├── DEPLOY.md        ← memory + deploying bots (Railway/Render) for each framework
├── MCP.md           ← what MCP is (a "USB port" for AI tools)
├── FAQ.md           ← what to do if it doesn't work
└── GLOSSARY.md      ← a dictionary of terms in simple words
```

> 🚀 **New to the project?** First open [`RESOURCES.md`](RESOURCES.md) — it walks
> through, step by step, what to install (for macOS and Windows). To read `.md`
> files nicely — `Cmd+Shift+V` (Windows: `Ctrl+Shift+V`).

## The three-level analogy (in web terms)

```
01-pure_python/  ↔  plain CSS      — everything by hand
02-openai_sdk/   ↔  Tailwind        — also code, but shorter, ready-made blocks
n8n/Flowise   ↔  Tilda/Webflow   — graphical, no code (that's already not in the code)
```

Under the hood they all do the same thing. Only how much you write yourself changes.

## Install (once)

> 📁 `~/Downloads/foundations-practice` below is an EXAMPLE path. Your project
> folder might be somewhere else (Desktop, Downloads, anywhere) and named
> differently. Replace it with your own: easiest way — type `cd ` (with a
> trailing space) in the terminal, then drag the project folder from Finder
> right into the terminal window — the path fills in by itself.

```bash
cd ~/Downloads/foundations-practice   # ← put YOUR path to the project folder here
uv venv
uv pip install -r requirements.txt        # bare-code libraries
uv pip install openai-agents              # the framework (for the 02-openai_sdk folder)
```

## How to run

**Bare code** (free on Ollama — by default):
```bash
cd ~/Downloads/foundations-practice   # ← same path as above — yours, not this example
uv run 01-pure_python/00_chain.py
uv run 01-pure_python/06_router.py
# ...and so on
```

**Framework** (needs an OpenAI key in .env):
```bash
uv run 02-openai_sdk/01_basic.py
```

## Providers (bare code)

**Every** file in the `01-pure_python/` folder has its own switch right at the top:
```python
PROVIDER = "gemini"   # "ollama" (🆓 local, free) | "gemini" (Google cloud)
```
It's deliberately done this way, not in one shared file — open any specific
file, and you immediately see and change the model right there, nothing to look up elsewhere.

The Gemini key goes in `.env` (template in `.env.example`, variable
`GOOGLE_API_KEY`, free tier: https://aistudio.google.com/apikey). Set
`PROVIDER = "ollama"` — everything works **for free, locally**, no key needed at all.

> 🗺️ There's also a separate file, `01-pure_python/llm.py` — a universal engine
> supporting all 7 providers at once (Claude, OpenAI, DeepSeek, Mistral,
> YandexGPT, and others). The pattern files don't use it directly (they each
> have their own simple switch), but it's handy as a reference and as a
> ready-made "single entry point" approach if you build your own larger
> project. A full overview of models and frameworks — in [`LANDSCAPE.md`](LANDSCAPE.md).

> 🆓 At the time this course was recorded, Google offers **free access to
> Gemini via the API** (a free tier; terms may change over time) — that's why
> every file defaults to `PROVIDER = "gemini"`.

## Pattern map (in 01-pure_python/)

| File | Pattern | Group |
|---|---|---|
| `00_chain.py` | a simple call + Chain (plus switching models) | basics |
| `06_router.py` | Router | simple |
| `07_parallel.py` | Parallelization | simple |
| `03_judge.py` | Judge | smart |
| `05_agent_loop.py` | ReAct — the "think-act" loop | smart |
| `08_plan_execute.py` | Plan-and-Execute | smart |
| `09_orchestrator.py` | Orchestrator | smart |
| `10_memory.py` | Memory (a live terminal dialogue) | smart |
| `04_tools.py` / `11_real_tools.py` | Tool Calling | tools |
| `12_rag_knowledge.py` | RAG — answers from a knowledge base | data |
| `13_structured_output.py` | Structured Output — strict JSON | data |

Every file has a "💡 WHERE THIS IS USEFUL IN REAL LIFE" block — real applications.

## Safety guards

If you run without the needed key/library — instead of a scary error you get a
clear message about what to do. The free files (Ollama) work right away.
