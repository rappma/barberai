# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
09 — Команда на CrewAI / Orchestrator (сравни с ../01-pure_python/09_orchestrator.py)
=====================================================================================
Стихия CrewAI: команда из трёх ролей делает лендинг. Задачи идут по очереди,
результат предыдущей передаётся дальше (контекст). Модель — облачный Gemini.

Запуск:  uv run 03-crewai/09_crew.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
09 — A team on CrewAI / Orchestrator (compare with ../01-pure_python/09_orchestrator.py)
=====================================================================================
CrewAI's element: a team of three roles makes a landing page. Tasks run one
after another, the previous one's result is passed on (context). Model — cloud Gemini.

Run:  uv run 03-crewai/09_crew.py
"""
# endregion

import os
import sys
from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini/gemini-2.5-flash"   # RU: бесплатно локально "ollama/llama3.2" / EN: free locally "ollama/llama3.2"

try:
    from crewai import Agent, Task, Crew, Process, LLM
except ImportError:
    print("\n⚠️  Нет фреймворка. Установи (с поддержкой Gemini):  uv pip install \"crewai[google-genai]\"\n")
    sys.exit(1)

if not MODEL.startswith("ollama") and (not os.getenv("GOOGLE_API_KEY") or "..." in os.getenv("GOOGLE_API_KEY", "")):
    print("\n⚠️  Нет ключа GOOGLE_API_KEY (впиши в .env). Или MODEL = \"ollama/llama3.2\" для бесплатно.\n")
    sys.exit(1)


if __name__ == "__main__":
    # RU: ключ Google берём из .env
    # EN: the Google key is taken from .env
    llm = LLM(model=MODEL, api_key=os.getenv("GOOGLE_API_KEY"))
    brand = "кофейня «Зерно» — кофе в зёрнах для дома"

    # RU: сотрудники (3 роли)
    # EN: employees (3 roles)
    copywriter = Agent(
        role="Копирайтер",
        goal="Придумывать короткие цепляющие заголовки",
        backstory="Ты пишешь продающие заголовки для брендов.",
        llm=llm, verbose=True,
    )
    brander = Agent(
        role="Бренд-райтер",
        goal="Писать тёплый текст о бренде",
        backstory="Ты передаёшь дух бренда душевными словами.",
        llm=llm, verbose=True,
    )
    editor = Agent(
        role="Редактор",
        goal="Собирать части в цельный лендинг",
        backstory="Ты делаешь из кусков гладкий итоговый текст.",
        llm=llm, verbose=True,
    )

    # RU: задачи (по одной на сотрудника)
    # EN: tasks (one per employee)
    t1 = Task(description=f"Придумай заголовок лендинга для бренда: {brand}.",
              expected_output="Один цепляющий заголовок.", agent=copywriter)
    t2 = Task(description=f"Напиши короткий абзац «о нас» для бренда: {brand}.",
              expected_output="Один тёплый абзац.", agent=brander)
    t3 = Task(description="Собери цельный лендинг из заголовка и абзаца о нас.",
              expected_output="Готовый текст лендинга.", agent=editor)

    # RU: команда: process=sequential — задачи по очереди, контекст передаётся дальше
    # EN: the team: process=sequential — tasks in order, context is passed on
    crew = Crew(
        agents=[copywriter, brander, editor],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    print("\n=== Готовый лендинг ===\n", result)
