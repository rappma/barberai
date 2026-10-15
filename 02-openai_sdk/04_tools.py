# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
04 — Tool Calling на OpenAI Agents SDK (сравни с ../01-pure_python/04_tools.py)
===============================================================================
В голой версии было ~120 строк (JSON-схемы + диспетчер + цикл). Здесь декоратор
@function_tool прячет всё это: схему аргументов фреймворк строит сам из типов.

Запуск:  uv run 02-openai_sdk/04_tools.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
04 — Tool Calling on the OpenAI Agents SDK (compare with ../01-pure_python/04_tools.py)
===============================================================================
The bare version was ~120 lines (JSON schemas + dispatcher + loop). Here the
@function_tool decorator hides all of it: the framework builds the arg schema from types.

Run:  uv run 02-openai_sdk/04_tools.py
"""
# endregion

# ℹ️ RU: ЭТА ПАПКА — про ФРЕЙМВОРК OpenAI Agents SDK. ЭТОТ файл по умолчанию идёт на модели
#        OpenAI (gpt-*) — нужен ключ OPENAI_API_KEY. НО сам фреймворк умеет ЛЮБУЮ
#        OpenAI-совместимую модель, включая БЕСПЛАТНЫЙ локальный Ollama — как подключить,
#        показано в 10_memory.py (переключатель PROVIDER). Тут OpenAI выбран потому, что
#        вызов инструментов (tool calling) надёжнее на сильной модели, чем на локальной.
# ℹ️ EN: THIS FOLDER is about the OpenAI Agents SDK FRAMEWORK. THIS file runs on an OpenAI model
#        (gpt-*) by default — needs OPENAI_API_KEY. BUT the framework can use ANY
#        OpenAI-compatible model, including FREE local Ollama — see 10_memory.py (the PROVIDER
#        switch). OpenAI is chosen here because tool calling is more reliable on a strong model
#        than on a small local one.

import os
import sys
import math
from dotenv import load_dotenv

load_dotenv()

try:
    from agents import Agent, Runner, function_tool
except ImportError:
    print("\n⚠️  Нет фреймворка. Установи:  uv pip install openai-agents\n")
    sys.exit(1)

if not os.getenv("OPENAI_API_KEY") or "..." in os.getenv("OPENAI_API_KEY", ""):
    print("\n⚠️  Нет ключа OPENAI_API_KEY (впиши в .env).\n")
    sys.exit(1)


# RU: @function_tool превращает обычную функцию в инструмент агента
# EN: @function_tool turns an ordinary function into an agent tool

@function_tool
def calculate_tiles(roof_area: float, tile_size: float, reserve_percent: float = 10) -> str:
    """Рассчитать количество плитки на крышу заданной площади (с запасом)."""
    total = math.ceil((roof_area / tile_size) * (1 + reserve_percent / 100))
    return f"Нужно {total} плиток."


@function_tool
def save_note(text: str) -> str:
    """Сохранить короткую текстовую заметку."""
    print(f"   📝 [save_note] сохранено: {text}")
    return "Заметка сохранена."


if __name__ == "__main__":
    # RU: перечисляем инструменты — цикл вызова фреймворк ведёт сам
    # EN: just list the tools — the framework runs the call loop itself
    agent = Agent(
        name="Агент-помощник",
        instructions="Помогай пользователю, используя доступные инструменты.",
        tools=[calculate_tiles, save_note],
        model="gpt-4o-mini",
    )

    task = "Посчитай плитку на крышу 50 м², если плитка 0.25 м². Потом сохрани итог в заметку."
    print("Задача:", task, "\n")

    result = Runner.run_sync(agent, task)
    print("\nОтвет агента:\n", result.final_output)
