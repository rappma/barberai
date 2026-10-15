# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
01 — Простой вызов на CrewAI (сравни с ../01-pure_python/00_chain.py)
=====================================================================
Характер CrewAI: даже для одного вопроса описываешь «сотрудника» (роль, цель,
бэкграунд) и «задачу». Для одиночного вызова это избыточно — CrewAI создан
для КОМАНД (см. 09_crew.py). Модель — облачный Google Gemini (нужен GOOGLE_API_KEY).

Запуск:  uv run 03-crewai/01_basic.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
01 — A simple call on CrewAI (compare with ../01-pure_python/00_chain.py)
=====================================================================
CrewAI's character: even for one question you describe an "employee" (role,
goal, backstory) and a "task". For a single call it's overkill — CrewAI is
built for TEAMS (see 09_crew.py). The model is the cloud Google Gemini (needs GOOGLE_API_KEY).

Run:  uv run 03-crewai/01_basic.py
"""
# endregion

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# RU: модель. Облачный Gemini. Бесплатно локально: MODEL = "ollama/llama3.2"
# EN: the model. Cloud Gemini. Free locally: MODEL = "ollama/llama3.2"
MODEL = "gemini/gemini-2.5-flash"

# RU: предохранитель №1 — установлен ли фреймворк
# EN: guard #1 — is the framework installed
try:
    from crewai import Agent, Task, Crew, LLM
except ImportError:
    print("\n⚠️  Нет фреймворка. Установи (с поддержкой Gemini):  uv pip install \"crewai[google-genai]\"\n")
    sys.exit(1)

# RU: предохранитель №2 — для Gemini нужен ключ Google (для ollama — нет)
# EN: guard #2 — Gemini needs the Google key (ollama does not)
if not MODEL.startswith("ollama") and (not os.getenv("GOOGLE_API_KEY") or "..." in os.getenv("GOOGLE_API_KEY", "")):
    print("\n⚠️  Нет ключа GOOGLE_API_KEY (впиши в .env). Бесплатный ключ: https://aistudio.google.com/apikey")
    print("    Или сделай бесплатно локально: поставь MODEL = \"ollama/llama3.2\" вверху файла.\n")
    sys.exit(1)


if __name__ == "__main__":
    # RU: LLM — «мозг» команды; ключ Google берём из .env
    # EN: LLM — the team's "brain"; the Google key is taken from .env
    llm = LLM(model=MODEL, api_key=os.getenv("GOOGLE_API_KEY"))

    # RU: Agent = «сотрудник»: роль + цель + бэкграунд
    # EN: Agent = an "employee": role + goal + backstory
    expert = Agent(
        role="Эксперт-объяснитель",
        goal="Объяснять сложные темы простыми словами",
        backstory="Ты годами учишь новичков и умеешь объяснять на пальцах.",
        llm=llm,
        verbose=False,
    )

    # RU: Task = что сделать + какой ожидается результат
    # EN: Task = what to do + what result is expected
    task = Task(
        description="Объясни простыми словами, что такое API. Три предложения.",
        expected_output="Три коротких понятных предложения.",
        agent=expert,
    )

    # RU: Crew = команда: сотрудники + задачи, запуск через kickoff()
    # EN: Crew = the team: employees + tasks, run via kickoff()
    crew = Crew(agents=[expert], tasks=[task], verbose=False)
    result = crew.kickoff()

    print(result)
