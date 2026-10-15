# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
09 — Orchestrator на OpenAI Agents SDK (сравни с ../01-pure_python/09_orchestrator.py)
======================================================================================
Приём фреймворка: agent.as_tool() — превратить агента в ИНСТРУМЕНТ другого агента.
Дирижёр «вызывает специалистов» как функции и собирает результат.

Запуск:  uv run 02-openai_sdk/09_orchestrator.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
09 — Orchestrator on the OpenAI Agents SDK (compare with ../01-pure_python/09_orchestrator.py)
======================================================================================
Framework trick: agent.as_tool() — turn an agent into a TOOL of another agent.
The conductor "calls the specialists" like functions and assembles the result.

Run:  uv run 02-openai_sdk/09_orchestrator.py
"""
# endregion

# ℹ️ RU: ЭТА ПАПКА — про ФРЕЙМВОРК OpenAI Agents SDK. ЭТОТ файл по умолчанию идёт на модели
#        OpenAI (gpt-*) — нужен ключ OPENAI_API_KEY. НО сам фреймворк умеет ЛЮБУЮ
#        OpenAI-совместимую модель, включая БЕСПЛАТНЫЙ локальный Ollama — как подключить,
#        показано в 10_memory.py (переключатель PROVIDER). Тут OpenAI выбран потому, что
#        «агенты как инструменты» надёжнее на сильной модели, чем на локальной.
# ℹ️ EN: THIS FOLDER is about the OpenAI Agents SDK FRAMEWORK. THIS file runs on an OpenAI model
#        (gpt-*) by default — needs OPENAI_API_KEY. BUT the framework can use ANY
#        OpenAI-compatible model, including FREE local Ollama — see 10_memory.py (the PROVIDER
#        switch). OpenAI is chosen here because "agents as tools" are more reliable on a strong
#        model than on a small local one.

import os
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    from agents import Agent, Runner
except ImportError:
    print("\n⚠️  Нет фреймворка. Установи:  uv pip install openai-agents\n")
    sys.exit(1)

if not os.getenv("OPENAI_API_KEY") or "..." in os.getenv("OPENAI_API_KEY", ""):
    print("\n⚠️  Нет ключа OPENAI_API_KEY (впиши в .env).\n")
    sys.exit(1)


# RU: специалисты
# EN: specialists
copywriter = Agent(name="Копирайтер",   instructions="Пишешь короткие цепляющие заголовки.", model="gpt-4o-mini")
brander    = Agent(name="Бренд-райтер", instructions="Пишешь тёплый абзац «о нас».",         model="gpt-4o-mini")

# RU: дирижёр — специалисты подключены как инструменты через .as_tool()
# EN: conductor — specialists are attached as tools via .as_tool()
manager = Agent(
    name="Дирижёр",
    instructions=(
        "Собери цельный текст лендинга. Сначала получи заголовок и абзац «о нас» "
        "через инструменты, затем объедини их в красивый итоговый текст."
    ),
    tools=[
        copywriter.as_tool(tool_name="написать_заголовок", tool_description="Пишет заголовок для бренда"),
        brander.as_tool(tool_name="написать_о_нас",       tool_description="Пишет абзац о бренде"),
    ],
    model="gpt-4o-mini",
)


if __name__ == "__main__":
    task = "Собери лендинг для бренда: кофейня «Зерно» — кофе в зёрнах для дома."
    print("Задача:", task, "\n")

    result = Runner.run_sync(manager, task)
    print("Итоговый лендинг:\n", result.final_output)
