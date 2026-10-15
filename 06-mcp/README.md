# 06 — MCP: свой сервер инструментов

> 📖 Красиво смотреть: `Cmd+Shift+V` (Windows: `Ctrl+Shift+V`).
> Что такое MCP вообще — простыми словами в `../rus md/MCP.md`.
> 🇬🇧 English version below ⬇️

Здесь — **минимальный MCP-сервер** (`server.py`) с двумя инструментами:
🌤️ погода города и ➕ сложение чисел. Цель — потрогать руками, как один сервер
инструментов подключается к ИИ-клиенту.

## 1. Установить пакет

```bash
uv pip install mcp
```

## 2. Проверить, что сервер стартует

```bash
uv run 06-mcp/server.py
```

Сервер запустится и будет **молча ждать** подключения клиента (он общается не с
тобой в терминале, а с программой-клиентом). Это нормально. Останови — `Ctrl+C`.

> 🔍 **Хочешь увидеть инструменты «вживую» в браузере?** Есть официальный
> отладчик — **MCP Inspector**. Он покажет список твоих инструментов и даст
> вызвать их вручную, мышкой:
> ```bash
> npx @modelcontextprotocol/inspector uv run 06-mcp/server.py
> ```
> Это **необязательный** шаг — нужен только для удобной отладки.

### Что за «Node.js» и нужно ли его ставить?

Команда `npx` выше — из мира **Node.js**. Node.js — это «движок», который умеет
запускать программы на JavaScript (примерно как `uv`/Python запускает наши `.py`).
Inspector написан на JavaScript, поэтому для него нужен Node.

- **Для самого проекта Node.js НЕ нужен** — весь наш код на Python (`uv run`).
- Node нужен **только** если захочешь запустить MCP Inspector (удобный отладчик).

Если решишь поставить:

- 🔗 Скачать: **https://nodejs.org/** (бери версию **LTS** — стабильную).
  - **macOS:** скачай установщик с сайта, или через терминал: `brew install node`
  - **Windows:** скачай установщик с сайта и пройди «Далее → Далее».
- После установки **закрой и открой терминал заново**, проверь: `node --version`
  и `npx --version` — должны показать версии.
- `npx` ставится вместе с Node автоматически — он скачивает и запускает Inspector
  на лету, отдельно ничего качать не надо.

## 3. Подключить к Claude Desktop

Чтобы инструменты появились прямо в приложении **Claude Desktop**, добавь сервер
в его конфиг.

Файл конфига:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Впиши туда (укажи **полный путь** к папке проекта вместо примера — у тебя он
будет другим, например `/Users/твоеимя/Desktop/AI Agents Workbook RUS/06-mcp/server.py`):

```json
{
  "mcpServers": {
    "foundations-tools": {
      "command": "uv",
      "args": ["run", "/полный/путь/к/foundations-practice/06-mcp/server.py"]
    }
  }
}
```

> 💡 Как узнать свой полный путь: открой терминал в папке проекта и введи
> `pwd` — он покажет полный путь; допиши к нему `/06-mcp/server.py`.

Затем **полностью перезапусти Claude Desktop**. После этого в чате можно попросить:
«какая погода в Москве?» — и Claude сам вызовет твой инструмент `get_weather`.

> 💡 Тот же сервер так же подключается к другим MCP-клиентам (Claude Code, IDE) —
> в этом и смысл MCP: написал инструмент один раз, пользуешься везде.

## 4. Добавить свой инструмент

Просто допиши функцию с декоратором `@mcp.tool()` в `server.py`. Описание в
`"""кавычках"""` — это инструкция для ИИ, по ней он поймёт, когда звать инструмент.

```python
@mcp.tool()
def get_time() -> str:
    """Вернуть текущее время."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M")
```

---
---

# 🇬🇧 English

# 06 — MCP: your own tool server

> 📖 View it nicely: `Cmd+Shift+V` (Windows: `Ctrl+Shift+V`).
> What MCP is in general — in simple words in `../eng md/MCP.md`.

Here is a **minimal MCP server** (`server.py`) with two tools:
🌤️ a city's weather and ➕ adding numbers. The goal is to get hands-on with how one
tool server connects to an AI client.

## 1. Install the package

```bash
uv pip install mcp
```

## 2. Check that the server starts

```bash
uv run 06-mcp/server.py
```

The server will start and **silently wait** for a client to connect (it talks not
to you in the terminal, but to a client program). That's normal. Stop it — `Ctrl+C`.

> 🔍 **Want to see the tools "live" in the browser?** There's an official debugger —
> **MCP Inspector**. It shows the list of your tools and lets you call them by hand,
> with the mouse:
> ```bash
> npx @modelcontextprotocol/inspector uv run 06-mcp/server.py
> ```
> This is an **optional** step — needed only for convenient debugging.

### What is "Node.js" and do you need to install it?

The `npx` command above is from the **Node.js** world. Node.js is an "engine" that
can run programs written in JavaScript (roughly like `uv`/Python runs our `.py`).
The Inspector is written in JavaScript, so it needs Node.

- **For the project itself Node.js is NOT needed** — all our code is Python (`uv run`).
- Node is needed **only** if you want to run MCP Inspector (a handy debugger).

If you decide to install it:

- 🔗 Download: **https://nodejs.org/** (take the **LTS** version — the stable one).
  - **macOS:** download the installer from the site, or via the terminal: `brew install node`
  - **Windows:** download the installer from the site and go through "Next → Next".
- After installing **close and reopen the terminal**, check: `node --version`
  and `npx --version` — they should show versions.
- `npx` is installed together with Node automatically — it downloads and runs the
  Inspector on the fly, nothing extra to download separately.

## 3. Connect to Claude Desktop

To make the tools appear right inside the **Claude Desktop** app, add the server
to its config.

The config file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Put this there (use the **full path** to the project folder instead of the
example — yours will be different, e.g.
`/Users/yourname/Desktop/AI Agents Workbook ENG/06-mcp/server.py`):

```json
{
  "mcpServers": {
    "foundations-tools": {
      "command": "uv",
      "args": ["run", "/full/path/to/foundations-practice/06-mcp/server.py"]
    }
  }
}
```

> 💡 How to find your full path: open a terminal in the project folder and
> type `pwd` — it prints the full path; append `/06-mcp/server.py` to it.

Then **fully restart Claude Desktop**. After that, in the chat you can ask:
"what's the weather in Moscow?" — and Claude will call your `get_weather` tool itself.

> 💡 The same server connects the same way to other MCP clients (Claude Code, IDE) —
> that's the whole point of MCP: write a tool once, use it everywhere.

## 4. Add your own tool

Just add a function with the `@mcp.tool()` decorator in `server.py`. The description
in `"""quotes"""` is the instruction for the AI — from it, it understands when to call the tool.

```python
@mcp.tool()
def get_time() -> str:
    """Return the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M")
```
