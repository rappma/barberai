# Where do these bots ultimately "live"? (hosting)

You run the files with `uv run ...` — and the bot works while your computer is on
and the terminal is open. This file explains how to make the bot run on its own,
24/7, on the internet.

## The main thing: TWO different things get hosted

Any bot in this project (whether bare code or on a framework) is an ordinary
Python program. It has two "residents", and they can be in different places:

```
1) YOUR agent CODE   → runs somewhere on a server (computer / VPS / cloud)
2) THE MODEL (the AI's brain) → either locally (Ollama), or on the
                       provider's servers via API (OpenAI / Claude / Google)
```

For example: the code lives on a cheap server, but "thinks" via the cloud Claude.
Or both the code and the model (Ollama) are on one server of your own. Any combination.

---

## The hosting ladder for your CODE

| Where                                    | What it is                                     | When it fits                                      |
| ---------------------------------------- | ---------------------------------------------- | ------------------------------------------------- |
| 🖥️ **Local**                             | your computer (`uv run`)                       | development and tests; works while the computer is on |
| ☁️ **Your server / VPS**                 | Railway, Render, Fly.io, Hetzner, DigitalOcean | production 24/7: you upload the code — it runs always |
| ⚡ **Serverless**                        | Vercel, AWS Lambda, Google Cloud Run, Modal    | "on-demand" launch; you pay for usage             |
| 🤖 **Managed agent platforms**           | hosting from the framework's creators (see below) | deploy + memory + monitoring "out of the box"     |

The lower down the table — the less you think about the server, but the more you
pay / depend on the platform.

---

## Free or paid? (important — check the current pricing)

Hosting prices change, but at the time of writing the picture is this:

| Where | Free? |
|---|---|
| 🖥️ **Local** (`uv run`) | ✅ completely free (while your computer is on) |
| 🤗 **Hugging Face Spaces** | ✅ **has a free tier — the best option for a Gradio bot** |
| ☁️ **Railway** | ⚠️ a **$5** trial credit (expires in 30 days), then **$5/mo** (Hobby) |
| ☁️ **Render** | ⚠️ has a free tier, but the service **"falls asleep"** when idle |
| ⚡ **Vercel** | ✅ has a free tier, but it's serverless (for websites, not bots with memory) |

**Want to publish a Gradio bot for free, permanently → Hugging Face Spaces.**
Railway is good when you want "cheap and grown-up" (with a database in a couple
of clicks), but it's **no longer free** for continuous operation.

---

## Each framework has its "native" hosting platform

| Framework              | Its own platform                                                                                     |
| ---------------------- | -------------------------------------------------------------------------------------------------- |
| **LangGraph**          | LangGraph Platform (LangChain) — deploy graphs + memory + monitoring (LangSmith)                   |
| **CrewAI**             | CrewAI AMP / Enterprise — deploy "crews"                                                            |
| **Google ADK**         | Vertex AI Agent Engine — managed hosting in Google Cloud                                            |
| **OpenAI Agents SDK**  | there's no hosting platform for the code — you run it yourself (VPS / serverless). OpenAI hosts only the models |
| **Claude (Anthropic)** | Claude on the web / Managed Agents — cloud agent sessions                                           |

Using the "native" platform isn't required — any framework's code can be uploaded
to an ordinary VPS.

---

## And if there's no code (no-code)?

The tools **n8n / Flowise / Make** — there the bot is assembled with the mouse, no
code, and the hosting is built in: either the service's own cloud, or self-host on
your own server.

---

## In simple words

> A bot is a program. To make it run around the clock (not just while your computer
> is on), you **upload it to a server**: your own (a VPS like Railway) or a managed
> one (LangGraph Platform, Vertex Agent Engine, etc.). The model is then either
> local (Ollama on the same server) or in the cloud (via the provider's API).

---

## How to choose (short cheat sheet)

- **Just try it out / learn** → local (`uv run`).
- **🆓 Publish a Gradio bot for free** → Hugging Face Spaces.
- **A small bot 24/7, cheaply (but paid)** → Railway ($5/mo after the trial credit) or Render.
- **Rare / event-driven launch** → serverless (Vercel, Cloud Run).
- **A complex agent + you need memory and monitoring** → the framework's managed platform.
- **No code at all** → n8n / Flowise (their own cloud).
