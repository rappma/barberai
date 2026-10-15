# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
01 — Простой вызов на OpenAI Agents SDK (сравни с ../01-pure_python/00_chain.py)
================================================================================
То же «вопрос → ответ», но на фреймворке: без client, messages и ручной сборки
текста — Runner делает всё сам.

Запуск:  uv run 02-openai_sdk/01_basic.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
01 — A simple call on the OpenAI Agents SDK (compare with ../01-pure_python/00_chain.py)
================================================================================
The same "question → answer", but on a framework: no client, messages or manual
text assembly — the Runner does it all.

Run:  uv run 02-openai_sdk/01_basic.py
"""
# endregion

# ℹ️ RU: ЭТА ПАПКА — про ФРЕЙМВОРК OpenAI Agents SDK. ЭТОТ файл по умолчанию идёт на модели
#        OpenAI (gpt-*) — нужен ключ OPENAI_API_KEY. НО сам фреймворк умеет ЛЮБУЮ
#        OpenAI-совместимую модель, включая БЕСПЛАТНЫЙ локальный Ollama — как подключить,
#        показано в 10_memory.py (переключатель PROVIDER). То есть ключ OpenAI НЕ обязателен.
# ℹ️ EN: THIS FOLDER is about the OpenAI Agents SDK FRAMEWORK. THIS file runs on an OpenAI model
#        (gpt-*) by default — needs OPENAI_API_KEY. BUT the framework can use ANY
#        OpenAI-compatible model, including FREE local Ollama — see 10_memory.py (the PROVIDER
#        switch) for how. So an OpenAI key is NOT required.

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# RU: предохранитель №1 — установлен ли фреймворк
# EN: guard #1 — is the framework installed
try:
    from agents import Agent, Runner
except ImportError:
    print("\n⚠️  Нет фреймворка. Установи:  uv pip install openai-agents\n")
    sys.exit(1)

# RU: предохранитель №2 — есть ли ключ OpenAI
# EN: guard #2 — is there an OpenAI key
if not os.getenv("OPENAI_API_KEY") or "..." in os.getenv("OPENAI_API_KEY", ""):
    print("\n⚠️  Нет ключа OPENAI_API_KEY (впиши в .env). Ключ: https://platform.openai.com/api-keys\n")
    sys.exit(1)


if __name__ == "__main__":
    # RU: Agent = имя + инструкция + модель
    # EN: Agent = name + instruction + model
    agent = Agent(
        name="Помощник",
        instructions="Ты — дружелюбный эксперт. Отвечай коротко и по делу.",
        model="gpt-4o-mini",
    )

    # RU: Runner запускает агента и ведёт весь процесс сам
    # EN: the Runner launches the agent and runs the whole process itself
    result = Runner.run_sync(agent, "Объясни простыми словами, что такое API. Три предложения.")

    print(result.final_output)
