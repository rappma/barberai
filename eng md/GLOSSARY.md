# Glossary — terms in simple words

> 📖 View it nicely: `Cmd+Shift+V` (Windows: `Ctrl+Shift+V`).

A short cheat sheet for the words that come up in the project.

| Term | In simple words |
|---|---|
| **LLM** | a large language model — the "brain" of the AI that understands and writes text (ChatGPT, Claude, Gemini, llama). |
| **Model** | a specific "brain" (for example `llama3.2`, `gpt-4o-mini`). Can be local (on your computer) or cloud (on the provider's servers). |
| **Token** | a piece of a word (~3–4 letters). Models "think" in tokens; length and cost are also counted in them. |
| **Context (context window)** | how much text the model remembers at once (up to ~1M tokens on modern models, ~700 pages). When a conversation outgrows the window, the old part is summarized or dropped. |
| **Prompt** | what you write to the model (a request/question). |
| **System prompt** | the secret "who to be" instruction for the model (role, rules). The user doesn't see it. |
| **Provider** | the company that provides the model: Anthropic (Claude), OpenAI (GPT), Google (Gemini), or the local Ollama. |
| **API** | the "rules of communication" with the model over the internet (address + request format). |
| **API call** | one request to the model by those rules (a single call). |
| **SDK** | a convenient library that makes the API call for you from code (`anthropic`, `openai`, `ollama`). |
| **Key (API key)** | your "password" to a paid provider. Stored in the `.env` file, never written into the code. |
| **Agent** | a program that doesn't just answer but acts: thinks, calls tools, repeats — in a loop, until it solves the task. |
| **Tool (Tool Calling)** | a function the model can call to DO something real (calculate, record, send). |
| **Pattern** | a typical "assembly scheme" of an agent (Chain, Router, Judge, Memory, etc.). A brick that bots are built from. |
| **Framework** | a ready-made "wrapper" for agents (CrewAI, LangGraph, OpenAI Agents SDK) — you write less code, but there's more "magic". |
| **RAG** | "generation that peeks at your own data": you give the model your facts (a knowledge base) so it answers from them instead of making things up. |
| **Structured output** | when the model returns a strict format (JSON with fields) rather than free text — convenient to pass on. |
| **Memory** | storing context so the bot doesn't forget the conversation (or remembers between runs — in a file/database). |
| **Gradio** | a library that turns your function into a chat/interface in the browser. |
| **Hosting / deploy** | placing the bot on a server so it runs 24/7, not only while your computer is on. |
| **Embeddings** | a way to turn text into numbers to search "by meaning" (used in real RAG for large bases). |

> Didn't understand a word that isn't here? Ask Claude: "explain in simple words what … is".
