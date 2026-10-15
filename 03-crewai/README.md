# 03-crewai — те же паттерны, но «командой сотрудников» (CrewAI)

> 🇬🇧 English version below ⬇️

Третий уровень сравнения. CrewAI — фреймворк с метафорой **«экипаж/команда»**:
ты описываешь СОТРУДНИКОВ (роль, цель, бэкграунд) и ЗАДАЧИ для них, а CrewAI
запускает «команду». Заточен под мульти-агентов (наш паттерн Orchestrator).

## Три уровня в одном проекте

```
01-pure_python/  ↔  чистый CSS     — всё руками
02-openai_sdk/   ↔  Tailwind       — агенты + инструменты, гибко
03-crewai/       ↔  готовый шаблон — «команда ролей» + задачи (этот фолдер)
```

## Что сравнить

| | Голый код | OpenAI SDK | CrewAI (тут) |
|---|---|---|---|
| Простой вызов | `../01-pure_python/00_chain.py` | `../02-openai_sdk/01_basic.py` | `01_basic.py` |
| Команда/Orchestrator | `../01-pure_python/09_orchestrator.py` | `../02-openai_sdk/09_orchestrator.py` | `09_crew.py` |

Главное отличие CrewAI: вместо «вызовов» и «инструментов» ты мыслишь
**ролями и задачами** — почти как ставишь работу живой команде.

## Установка и запуск

> 📁 `~/Downloads/foundations-practice` ниже — это ПРИМЕР пути. У тебя папка
> проекта может лежать в другом месте и называться иначе. Замени путь на свой:
> проще всего написать в терминале `cd ` (с пробелом) и перетащить туда папку
> проекта мышкой из Finder — путь подставится сам.

```bash
cd ~/Downloads/foundations-practice   # ← впиши СВОЙ путь к папке проекта
uv pip install "crewai[google-genai]" # фреймворк + поддержка Gemini (ставится не быстро)
cp .env.example .env                  # впиши GOOGLE_API_KEY
uv run 03-crewai/01_basic.py
```

> Модель — облачный **Google Gemini** (нужен `GOOGLE_API_KEY` в `.env`).

### Бесплатно на Ollama (без ключа)
В каждом файле вверху есть строка `MODEL = "gemini/gemini-2.5-flash"`. Поменяй на
`MODEL = "ollama/llama3.2"` — и CrewAI пойдёт через бесплатный локальный Ollama
(ключ не нужен; качество слабее).

## Зачем это нужно

CrewAI — это та же категория «фреймворков», что и OpenAI SDK,
просто с другой метафорой («команда ролей»). Практику его писать не надо —
надо знать, что под мульти-агентные задачи он удобен, и попросить Claude.

---
---

# 🇬🇧 English

# 03-crewai — the same patterns, but as a "team of employees" (CrewAI)

The third level of comparison. CrewAI is a framework with a **"crew/team"** metaphor:
you describe EMPLOYEES (role, goal, backstory) and TASKS for them, and CrewAI runs
the "team". It's tailored for multi-agents (our Orchestrator pattern).

## Three levels in one project

```
01-pure_python/  ↔  plain CSS       — everything by hand
02-openai_sdk/   ↔  Tailwind        — agents + tools, flexible
03-crewai/       ↔  ready template  — a "team of roles" + tasks (this folder)
```

## What to compare

| | Bare code | OpenAI SDK | CrewAI (here) |
|---|---|---|---|
| Simple call | `../01-pure_python/00_chain.py` | `../02-openai_sdk/01_basic.py` | `01_basic.py` |
| Team/Orchestrator | `../01-pure_python/09_orchestrator.py` | `../02-openai_sdk/09_orchestrator.py` | `09_crew.py` |

CrewAI's main difference: instead of "calls" and "tools" you think in
**roles and tasks** — almost like assigning work to a real team.

## Install and run

> 📁 `~/Downloads/foundations-practice` below is an EXAMPLE path. Your project
> folder might be somewhere else and named differently. Replace it with your
> own: easiest way — type `cd ` (with a trailing space) in the terminal, then
> drag the project folder from Finder right into the terminal window — the
> path fills in by itself.

```bash
cd ~/Downloads/foundations-practice   # ← put YOUR path to the project folder here
uv pip install "crewai[google-genai]" # the framework + Gemini support (installs slowly)
cp .env.example .env                  # put in GOOGLE_API_KEY
uv run 03-crewai/01_basic.py
```

> The model is the cloud **Google Gemini** (needs `GOOGLE_API_KEY` in `.env`).

### Free on Ollama (no key)
At the top of each file there's a line `MODEL = "gemini/gemini-2.5-flash"`. Change it to
`MODEL = "ollama/llama3.2"` — and CrewAI will go through the free local Ollama
(no key needed; lower quality).

## Why this matters

CrewAI is the same "framework" category as the OpenAI SDK, just with a different
metaphor (a "team of roles"). A practitioner doesn't need to write it — they need
to know it's handy for multi-agent tasks, and to ask Claude.
