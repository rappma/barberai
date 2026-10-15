# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
10 — Память в CrewAI одним флагом (memory=True)
==============================================
Показывает фичу памяти CrewAI. Включается ОДНОЙ строкой: memory=True.
Дальше CrewAI сам хранит, что узнал, и подсовывает это агентам при следующих
запусках. Тебе НЕ нужно вручную писать историю в файл (сравни с
../01-pure_python/10_memory.py, где мы делали это руками).

⚠️ ВАЖНО, чем это отличается от нашего 10_memory.py:
  • CrewAI НЕ создаёт читаемый memory.json. Он хранит память в своей базе
    (SQLite + векторное хранилище) — в этом файле мы направили её в видимую
    папку ./crewai_memory, чтобы ты увидел, что там появляются служебные файлы.
  • Память CrewAI — это не дословная история чата, а «выводы» из прошлых
    запусков (кого как зовут, предпочтения). Работает нечётко, но между запусками.
  • memory=True требует «эмбеддинг-модель». Тут всё локально и бесплатно (Ollama),
    чтобы можно было запускать СКОЛЬКО УГОДНО раз — на памяти это и видно.
  • ⚠️ Чтобы бот ЧИСТО вспомнил факт, нужна модель поумнее: llama3.2 путается с
    инструментом поиска по памяти. Для наглядного «вспомнил имя» поставь
    CHAT_MODEL = "ollama/qwen2.5" (ollama pull qwen2.5) или Gemini/Claude/GPT.

ПОДГОТОВКА (один раз):
  uv pip install crewai
  ollama pull llama3.2          (модель-«мозг»)
  ollama pull nomic-embed-text  (модель для эмбеддингов памяти)

Как проверить: запусти файл, потом поменяй MESSAGE ниже на «как меня зовут?»
и запусти ещё раз — CrewAI должен вспомнить имя из первого запуска.

Запуск:  uv run 03-crewai/10_memory.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
10 — Memory in CrewAI with one flag (memory=True)
==============================================
Shows CrewAI's memory feature. It's turned on with ONE line: memory=True.
After that CrewAI stores what it learned itself and feeds it to the agents on
later runs. You do NOT write history to a file by hand (compare with
../01-pure_python/10_memory.py, where we did it manually).

⚠️ IMPORTANT, how it differs from our 10_memory.py:
  • CrewAI does NOT create a readable memory.json. It stores memory in its own
    database (SQLite + a vector store) — here we pointed it at a visible folder
    ./crewai_memory so you can see the service files appear there.
  • CrewAI memory isn't a verbatim chat history, but "insights" from past runs
    (names, preferences). It's fuzzy, but it persists across runs.
  • memory=True needs an "embedding model". Here everything is local and free
    (Ollama), so you can run it AS MANY TIMES as you like — that's how you see memory.
  • ⚠️ For the bot to CLEANLY recall a fact you need a smarter model: llama3.2
    fumbles the memory-search tool. For a clear "it remembered the name" set
    CHAT_MODEL = "ollama/qwen2.5" (ollama pull qwen2.5) or Gemini/Claude/GPT.

SETUP (once):
  uv pip install crewai
  ollama pull llama3.2          (the "brain" model)
  ollama pull nomic-embed-text  (the model for memory embeddings)

How to test: run the file, then change MESSAGE below to "what's my name?" and
run again — CrewAI should recall the name from the first run.

Run:  uv run 03-crewai/10_memory.py
"""
# endregion

import os
import sys

# RU: КУДА CrewAI сложит память. Задаём ДО импорта crewai, иначе не применится.
#     Обычно память прячется в системной папке — тут кладём в видимую ./crewai_memory.
# EN: WHERE CrewAI stores memory. Set this BEFORE importing crewai, or it won't apply.
#     Normally memory hides in a system folder — here we put it in a visible ./crewai_memory.
os.environ["CREWAI_STORAGE_DIR"] = os.path.join(os.path.dirname(__file__), "crewai_memory")

# RU: что «говорит» пользователь. Меняй эту строку между запусками:
#     1-й запуск — представься; 2-й запуск — спроси «как меня зовут?».
# EN: what the user "says". Change this line between runs:
#     1st run — introduce yourself; 2nd run — ask "what's my name?".
MESSAGE = "Привет! Меня зовут Дима, я люблю латте."

# RU: всё локально через Ollama (без лимитов) / EN: all local via Ollama (no limits)
CHAT_MODEL = "ollama/llama3.2"
EMBED_MODEL = "nomic-embed-text"

try:
    from crewai import Agent, Task, Crew, Process, LLM
except ImportError:
    print("\n⚠️  Нет фреймворка. Установи:  uv pip install crewai\n")
    sys.exit(1)


if __name__ == "__main__":
    llm = LLM(model=CHAT_MODEL)

    # RU: один агент-ассистент. EN: a single assistant agent.
    assistant = Agent(
        role="Личный ассистент",
        goal="Общаться с пользователем и помнить, что о нём известно",
        backstory="Ты дружелюбный ассистент с хорошей памятью.",
        llm=llm,
        verbose=True,
    )

    task = Task(
        description=(
            f"Ответь на сообщение пользователя, используя всё, что ты помнишь о нём "
            f"из прошлых разговоров.\n\nСообщение пользователя: {MESSAGE}"
        ),
        expected_output="Короткий дружелюбный ответ на языке пользователя.",
        agent=assistant,
    )

    # RU: ВОТ ОНА — память включается одним флагом memory=True.
    #     embedder — какой моделью считать «эмбеддинги» для памяти (тут локальный Ollama).
    # EN: HERE IT IS — memory is turned on with the single flag memory=True.
    #     embedder — which model computes the memory "embeddings" (here local Ollama).
    crew = Crew(
        agents=[assistant],
        tasks=[task],
        process=Process.sequential,
        memory=True,   # ← RU: включили долгую память / EN: long-term memory turned on
        embedder={
            "provider": "ollama",
            "config": {"model_name": EMBED_MODEL},
        },
        verbose=True,
    )

    result = crew.kickoff()
    print("\n=== Ответ ассистента / Assistant's reply ===\n", result)
    print("\n💾 RU: память CrewAI лежит в папке ./crewai_memory (это НЕ json, а база).")
    print("💾 EN: CrewAI's memory is in the ./crewai_memory folder (NOT json, it's a database).")
    print("👉 RU: поменяй MESSAGE на «как меня зовут?» и запусти снова — вспомнит ли?")
    print("👉 EN: change MESSAGE to \"what's my name?\" and run again — will it recall?")
