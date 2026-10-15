# 02-openai_sdk — те же паттерны, но на ФРЕЙМВОРКЕ (OpenAI Agents SDK)

> 🇬🇧 English version below ⬇️

Здесь те же боты, что в папке выше (голый код), но написанные на **OpenAI
Agents SDK** — фреймворке. Цель — наглядно сравнить «голый код ↔ фреймворк».

> ⚠️ Эта папка работает на моделях **OpenAI** (gpt-*), а НЕ на Gemini. Нужен
> **отдельный платный ключ `OPENAI_API_KEY`** (оплачивается отдельно от Google).
> Это осознанно — цель папки показать именно фреймворк OpenAI.

## Аналогия (для понимания)

```
голый код (../)        ↔  чистый CSS      — всё руками, максимум контроля
Agents SDK (эта папка) ↔  Tailwind        — тоже код, но короче, готовые блоки
n8n / Flowise          ↔  Tilda/Webflow   — графика, без кода вообще
```

Под капотом все делают одно и то же. Меняется только, сколько пишешь сам.

## Что сравнить

| Паттерн | Голый код | На фреймворке | Что спрятал фреймворк |
|---|---|---|---|
| Простой вызов | `../01-pure_python/00_chain.py` | `01_basic.py` | сборку сообщений и текста |
| Tool Calling | `../01-pure_python/04_tools.py` (~120 строк) | `04_tools.py` (~25 строк) | JSON-схемы, цикл, «большой IF» |
| Router | `../01-pure_python/06_router.py` | `06_router.py` | классификацию (через handoffs) |
| Orchestrator | `../01-pure_python/09_orchestrator.py` | `09_orchestrator.py` | вызов «агентов как инструментов» |

## Установка и запуск

> 📁 `~/Downloads/foundations-practice` ниже — это ПРИМЕР пути. У тебя папка
> проекта может лежать в другом месте и называться иначе. Замени путь на свой:
> проще всего написать в терминале `cd ` (с пробелом) и перетащить туда папку
> проекта мышкой из Finder — путь подставится сам.

```bash
cd ~/Downloads/foundations-practice   # ← впиши СВОЙ путь к папке проекта
uv pip install openai-agents          # сам фреймворк
cp .env.example .env                  # впиши OPENAI_API_KEY
uv run 02-openai_sdk/01_basic.py
```

> Нужен платный ключ OpenAI (`OPENAI_API_KEY`). В каждом файле стоит
> предохранитель: без ключа/без библиотеки выпадет понятное сообщение.

## Зачем это

Фреймворк **не «круче», а экономит шаблонный код** на больших проектах:
готовый цикл агента, авто-схемы инструментов, передача между агентами, трейсы.
Цена — зависимость от фреймворка и больше «магии под капотом». Практику-нонкодеру
писать это не нужно — нужно понимать, *когда попросить Claude собрать на нём.*

---
---

# 🇬🇧 English

# 02-openai_sdk — the same patterns, but on a FRAMEWORK (OpenAI Agents SDK)

Here are the same bots as in the folder above (bare code), but written on the
**OpenAI Agents SDK** — a framework. The goal is to clearly compare "bare code ↔ framework".

> ⚠️ This folder runs on **OpenAI** models (gpt-*), NOT on Gemini. It needs a
> **separate paid `OPENAI_API_KEY`** (billed separately from Google). This is
> intentional — the folder's goal is to show the OpenAI framework specifically.

## Analogy (to make it click)

```
bare code (../)          ↔  plain CSS       — everything by hand, maximum control
Agents SDK (this folder) ↔  Tailwind         — still code, but shorter, ready-made blocks
n8n / Flowise            ↔  Tilda/Webflow    — graphical, no code at all
```

Under the hood they all do the same thing. Only how much you write yourself changes.

## What to compare

| Pattern | Bare code | On the framework | What the framework hid |
|---|---|---|---|
| Simple call | `../01-pure_python/00_chain.py` | `01_basic.py` | assembling messages and text |
| Tool Calling | `../01-pure_python/04_tools.py` (~120 lines) | `04_tools.py` (~25 lines) | JSON schemas, the loop, the "big IF" |
| Router | `../01-pure_python/06_router.py` | `06_router.py` | the classification (via handoffs) |
| Orchestrator | `../01-pure_python/09_orchestrator.py` | `09_orchestrator.py` | calling "agents as tools" |

## Install and run

> 📁 `~/Downloads/foundations-practice` below is an EXAMPLE path. Your project
> folder might be somewhere else and named differently. Replace it with your
> own: easiest way — type `cd ` (with a trailing space) in the terminal, then
> drag the project folder from Finder right into the terminal window — the
> path fills in by itself.

```bash
cd ~/Downloads/foundations-practice   # ← put YOUR path to the project folder here
uv pip install openai-agents          # the framework itself
cp .env.example .env                  # put in OPENAI_API_KEY
uv run 02-openai_sdk/01_basic.py
```

> You need a paid OpenAI key (`OPENAI_API_KEY`). Each file has a safety guard:
> without a key/library it prints a clear message.

## Why this matters

A framework is **not "cooler", it saves boilerplate** on large projects: a
ready-made agent loop, auto tool schemas, handoffs between agents, traces.
The price — dependence on the framework and more "magic under the hood". A
no-code practitioner doesn't need to write this — they need to understand
*when to ask Claude to build it on the framework.*
