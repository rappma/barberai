# FAQ — what to do if it doesn't work

> 📖 View it nicely: `Cmd+Shift+V` (Windows: `Ctrl+Shift+V`).

Common beginner errors and quick fixes. First **read the last line of the error**
in the terminal — that's usually where the reason is.

---

### `zsh: command not found: ollama` (or `uv`, `git`)
The program isn't installed **or** the terminal doesn't "see" it yet.
- Install it (see `RESOURCES.md`).
- Then **close and reopen the terminal** — commands are picked up in a new window.

---

### `Ollama isn't responding` / `connection refused` / `Could not connect to ollama`
The Ollama engine isn't running or there's no model.
- Make sure the **Ollama app is running** (on a Mac — the llama icon in the menu bar).
- Download a model: `ollama pull llama3.2` (or `qwen2.5`).
- Check: `ollama list` — the model should be in the list.

---

### `ModuleNotFoundError: No module named 'X'`
The library `X` isn't installed.
- Install it: `uv pip install X`
- Or install everything at once: `uv pip install -r requirements.txt`
- Frameworks install separately: `uv pip install openai-agents` / `crewai` / `langgraph`.

---

### `Could not resolve authentication` / "No key"
No key for the chosen provider (Claude / OpenAI / Gemini / DeepSeek / Mistral / YandexGPT).
- Put the key into the **`.env`** file (template — `.env.example`).
- For YandexGPT you also need `YANDEX_FOLDER_ID` (the Yandex Cloud catalog ID).
- Or switch to the free path: in the code `PROVIDER = "ollama"`.
- Which models exist at all (incl. 🇷🇺 Russian ones) — see `LANDSCAPE.md`.

---

### `RateLimitError: 429` / "Quota exceeded" / `RESOURCE_EXHAUSTED` (Gemini)
Google Gemini's **free** tier (`gemini-2.5-flash`) has a very small limit —
just **20 requests PER DAY** per model. It's shared across the whole day, not
per file run: if you've already tested a few examples in a row, the limit can
run out by your 2nd–3rd question.
- This isn't a code bug — it's a limit of Google's free tier.
- **For active development and testing**, switch to the free local model:
  `PROVIDER = "ollama"` (no limits, works offline).
- **The limit is daily** — it resets on its own the next day.
- Save Gemini for a final demo/showcase rather than for trial-and-error
  experimenting — that way your 20 requests last much longer.

---

### `.env` isn't picked up (the key "isn't seen")
- The file must be named exactly **`.env`** (not `.env.txt`).
- It must be in the **project root** (next to `requirements.txt`).
- After editing `.env`, run again.

---

### `address already in use` / port `7860` is busy (Gradio)
A previous chat is already running.
- Close the previous terminal (`Ctrl+C`) and run again.
- Or specify a different port: `.launch(server_port=7861)`.

---

### The bot mixes up languages / answers poorly
It's a **small free model** (llama3.2) — it's a bit weak.
- Take a better model for your language: `ollama pull qwen2.5`, in the code `MODEL = "qwen2.5"`.
- Or use a cloud model (Claude / GPT / free Gemini) — noticeably smarter.

---

### It runs slowly
A local model is computed on your computer — that's normal, especially on a weak one.
- Take a lighter model or a cloud one (it's faster).

---

### A `.pyc` file or a `__pycache__` folder — what is that?
It's Python's service cache. **Don't touch or read** it. Open only `.py` files.

---

> If nothing helped — copy the **last line of the error** and ask Claude:
> "I got this error when running — what should I do?". It will help.
