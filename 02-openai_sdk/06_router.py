# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
06 — Router на OpenAI Agents SDK через HANDOFFS (сравни с ../01-pure_python/06_router.py)
=========================================================================================
В голой версии классификацию писали сами. Здесь встроенный механизм handoffs:
агент-диспетчер сам решает, какому специалисту передать вопрос.

Запуск:  uv run 02-openai_sdk/06_router.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
06 — Router on the OpenAI Agents SDK via HANDOFFS (compare with ../01-pure_python/06_router.py)
=========================================================================================
In the bare version we wrote the classification ourselves. Here the built-in
handoffs mechanism: a dispatcher agent decides which specialist to hand it to.

Run:  uv run 02-openai_sdk/06_router.py
"""
# endregion

# ℹ️ RU: ЭТА ПАПКА — про ФРЕЙМВОРК OpenAI Agents SDK. ЭТОТ файл по умолчанию идёт на модели
#        OpenAI (gpt-*) — нужен ключ OPENAI_API_KEY. НО сам фреймворк умеет ЛЮБУЮ
#        OpenAI-совместимую модель, включая БЕСПЛАТНЫЙ локальный Ollama — как подключить,
#        показано в 10_memory.py (переключатель PROVIDER). Тут OpenAI выбран потому, что
#        handoffs/маршрутизация надёжнее на сильной модели, чем на локальной.
# ℹ️ EN: THIS FOLDER is about the OpenAI Agents SDK FRAMEWORK. THIS file runs on an OpenAI model
#        (gpt-*) by default — needs OPENAI_API_KEY. BUT the framework can use ANY
#        OpenAI-compatible model, including FREE local Ollama — see 10_memory.py (the PROVIDER
#        switch). OpenAI is chosen here because handoffs/routing are more reliable on a strong
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


# RU: специалисты — обычные агенты со своими ролями
# EN: specialists — ordinary agents with their own roles
finance = Agent(name="Финансист", instructions="Отвечай на вопросы про деньги, оплату, цены.", model="gpt-4o-mini")
logist  = Agent(name="Логист",    instructions="Отвечай на вопросы про доставку и сроки.",    model="gpt-4o-mini")
general = Agent(name="Поддержка",  instructions="Отвечай на общие вопросы кратко и понятно.",  model="gpt-4o-mini")

# RU: диспетчер: handoffs = кому он может передать вопрос
# EN: the dispatcher: handoffs = who it can hand the question to
triage = Agent(
    name="Диспетчер",
    instructions="Определи тему вопроса и передай его нужному специалисту.",
    handoffs=[finance, logist, general],
    model="gpt-4o-mini",
)


if __name__ == "__main__":
    questions = [
        "Сколько стоит подписка и как оплатить?",
        "Когда приедет мой заказ?",
        "Какой у вас график работы?",
    ]
    for q in questions:
        print(f"\nВопрос: {q}")
        result = Runner.run_sync(triage, q)
        print("Ответ:", result.final_output)
