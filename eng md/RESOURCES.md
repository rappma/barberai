# Resources and installation (what to install so everything works)

Here's everything you need to install **once** to get the project running.
The frameworks (openai-agents, crewai, langgraph) do **not** need to be installed
yet — we'll install them later, separately.

> 📖 **To make this and other `.md` files open nicely** (with headings and tables,
> not raw text), press in the editor:
> **macOS:** `Cmd + Shift + V`  ·  **Windows:** `Ctrl + Shift + V`

---

## 1. VS Code — the code editor

The program in which you open and read the project files. Free.

🔗 Download: **https://code.visualstudio.com/download**
(on the page pick your system — macOS or Windows — and install it like a normal app).

**What it gives you:** convenient code viewing, opening `.md` in a preview (`Cmd+Shift+V`),
running the built-in terminal (menu *Terminal → New Terminal*).

---

## 2. uv — the package and Python manager

`uv` is a modern tool that installs libraries and manages Python itself.
It replaces the old `pip`. Through it you run files (`uv run ...`).

🔗 About it: **https://github.com/astral-sh/uv**

**macOS / Linux** (paste into the terminal and press Enter):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows** (open PowerShell and paste):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**What the command does:** downloads and installs `uv`. After installing **close
and reopen the terminal**, then check: `uv --version` — a version should appear.

---

## 3. Ollama — the free local AI (no keys, no payment)

An app that runs neural networks **right on your computer**. Needed so the free
examples work without any keys.

🔗 Download: **https://ollama.com/download**

**macOS:** download the app from the link and drag it into "Applications", then run
it once (a llama icon will appear in the menu bar).
Alternative via the terminal:
```bash
brew install ollama
```

**Windows:** download the installer from the link and install it (Ollama starts in the background on its own).
Alternative via the terminal:
```powershell
winget install Ollama.Ollama
```

**What it does:** installs the "engine". By itself it's empty — next you need to
download a "brain" (a model).

### Download models (the commands are the same on macOS and Windows)

```bash
ollama pull llama3.2
```
**What it does:** downloads the **llama3.2** model (~2 GB) — light, fast, for general
tasks. Downloaded once, then works offline.

```bash
ollama pull qwen2.5
```
**What it does:** downloads the **qwen2.5** model — it **understands many languages
noticeably better** than llama3.2. If good non-English answers matter — use it.

> Which model to use is set in the code by the line `MODEL = "..."`
> (for example `"llama3.2"` or `"qwen2.5"`).

### 🆓 Free, but cloud: Google Gemini

Don't want to install Ollama (or need a smarter model)? **At the time this course
was recorded, Google offers FREE access to Gemini via the API.** It's a cloud model —
smarter than the local one, and free at that (a free tier; terms may change over time).

1. Get a free key: **https://aistudio.google.com/apikey**
2. Put it into the `.env` file (the line `GOOGLE_API_KEY=...`).
3. In the code set the Gemini provider: the line `PROVIDER = "gemini"` at the
   top of any file in `01-pure_python/` — it's already set there by default.

That way you can learn on a good cloud model **for free**.

> 🗺️ Which models and frameworks exist at all (including the cheap DeepSeek and
> the 🇷🇺 Russian YandexGPT / GigaChat — paid in rubles, no foreign card) —
> see the overview file `LANDSCAPE.md`.

---

## 4. The project's libraries (without the frameworks)

The base libraries needed by the bare code and the chat. **The frameworks are NOT included here.**
Run from the project folder (where `requirements.txt` is).

**macOS and Windows** (the same):
```bash
uv venv
uv pip install -r requirements.txt
uv pip install gradio
```

**What the commands do:**
- `uv venv` — creates a "box" for the project's libraries (the `.venv` folder).
- `uv pip install -r requirements.txt` — installs the base libraries
  (ollama, anthropic, openai, python-dotenv).
- `uv pip install gradio` — installs Gradio (for the browser chat, `chat_web.py`).

---

## 5. Git — to download (clone) the project

Git is needed to download the project from a repository with one command.

🔗 Windows installer: **https://git-scm.com/download/win**

**macOS:** usually already installed. If not — it installs like this:
```bash
xcode-select --install
```
or via `brew install git`.

**Windows:** install from the link above (the usual "Next → Next").

**Check:** `git --version` — a version should appear.

Download the project (once there's a repository link):
```bash
git clone REPOSITORY_LINK
```

---

## 6. The project repository

🔗 The link will appear later: **(to be added)**

Here we'll put the address of the repository with this project, so you can download
everything with one `git clone` command.

---

## ✅ Checking that everything works

From the project folder, run the free example:
```bash
uv run 01-pure_python/00_chain.py
```
If an AI answer appeared in the terminal — the installation was successful. 🎉

> If something doesn't run — every file has a "safety guard": it will tell you in
> clear text exactly what isn't installed or configured.
