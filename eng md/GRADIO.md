# Gradio — turn a bot into a real chat in the browser

Until now you ran bots in the terminal with the question written in advance. **Gradio**
lets you, in ~10 lines, turn a function into a **real chat window in the browser** —
you type live, like in ChatGPT.

## What Gradio is

It's a Python library that makes a **web interface** out of your function: a chat,
a form, buttons. No knowledge of HTML/CSS — Gradio draws the interface itself.

```
terminal with a script   →   Gradio   →   a live chat in the browser
(text written in)                          (you type yourself, in real time)
```

## Install

> 📁 `~/Downloads/foundations-practice` below is an EXAMPLE path. Your project
> folder might be somewhere else and named differently. Replace it with your
> own: easiest way — type `cd ` (with a trailing space) in the terminal, then
> drag the project folder from Finder right into the terminal window — the
> path fills in by itself.

```bash
cd ~/Downloads/foundations-practice   # ← put YOUR path to the project folder here
uv pip install gradio
```

## Minimal code (the whole essence of Gradio)

```python
import gradio as gr

# The chat function: receives the user's message and the history, returns an answer.
def chat(message, history):
    return "You wrote: " + message      # the AI call goes here

# ChatInterface turns the function into a chat window. launch() — opens it.
gr.ChatInterface(chat).launch()
```

> ⚠️ If you have an old Gradio version (before 6.0), you might need
> `gr.ChatInterface(chat, type="messages")` — older versions also had a
> `type="tuples"` format, and you had to pick one explicitly. In Gradio 6+
> (the current version when you `uv pip install gradio`), the messages format
> is the only one and is used by default — you don't need to write `type=...`,
> and doing so now throws `TypeError: unexpected keyword argument 'type'`.

Three things Gradio does:

1. draws the chat page;
2. calls the `chat(...)` function on each of your messages;
3. shows what it returned.

## How to run and what happens

```bash
uv run chat_web.py
```

In the terminal a line like this will appear:

```
Running on local URL:  http://127.0.0.1:7860
```

Open this address in the browser (often Gradio opens it itself) — there's the chat window.
You type a message → the bot answers live. To stop — `Ctrl+C` in the terminal.

## The ready-made example in the project

The file **`chat_web.py`** — a working chat connected to an AI (by default the free
local Ollama). Run it and have a chat:

```bash
uv run chat_web.py
```

## Share a link (temporarily)

Add `share=True` — Gradio will give a **public link** for ~72 hours, which you can
send to a friend (it works while your script is running):

```python
gr.ChatInterface(chat).launch(share=True)
```

## Where to host it permanently

A local Gradio lives while your computer is on. To run 24/7 — upload it to a
server (see `HOSTING.md`). For Gradio the simplest free hosting is
**Hugging Face Spaces** (you create a Space, upload the files, and it brings up the
chat at a public link itself).

## Cheat sheet

| I want                          | What to do                                                      |
| ------------------------------- | --------------------------------------------------------------- |
| A chat in the browser locally   | `gr.ChatInterface(chat).launch()` → open localhost:7860         |
| A temporary link for a friend   | `.launch(share=True)`                                           |
| A permanent public bot          | publish on Hugging Face Spaces (or a VPS, see HOSTING.md)       |
| Not just a chat, but a form/buttons | `gr.Interface(...)` / `gr.Blocks(...)` (other kinds of interface) |
