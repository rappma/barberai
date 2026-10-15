# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
10 — Память в OpenAI Agents SDK (SQLiteSession)
==============================================
Живой диалог в терминале с памятью. Память включается ОДНОЙ строкой — созданием
сессии SQLiteSession(...). Дальше SDK САМ сохраняет каждую реплику в файл-базу и
подгружает историю при следующих запусках. Тебе не нужно вручную вести список
сообщений (сравни с ../01-pure_python/10_memory.py, где мы делали это руками).

🔑 ВАЖНО про модель: OpenAI Agents SDK — это ФРЕЙМВОРК от OpenAI, но модель к нему
   можно подключить ЛЮБУЮ OpenAI-совместимую. Поэтому тут есть переключатель:
     "ollama" — бесплатно, локально, без ключа (по умолчанию)
     "openai" — модели OpenAI (gpt-*), нужен платный ключ OPENAI_API_KEY
   То есть OpenAI-ключ НЕ обязателен — можно учиться на фреймворке бесплатно.

⚠️ Чем это проще CrewAI (../03-crewai/10_memory.py):
  • НЕ нужна отдельная эмбеддинг-модель.
  • Хранит ДОСЛОВНУЮ историю чата в обычном файле SQLite (не вектора).
  • Файл `openai_memory.db` можно открыть просмотрщиком SQLite и увидеть сообщения.

Запуск:  uv run 02-openai_sdk/10_memory.py   (для выхода — "выход" или "exit")
         Чтобы «забыть всё» — удали файл openai_memory.db.
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
10 — Memory in the OpenAI Agents SDK (SQLiteSession)
==============================================
A live terminal chat with memory. Memory is turned on with ONE line — creating a
SQLiteSession(...). After that the SDK ITSELF saves every turn to a file database
and loads the history on later runs. You don't keep a message list by hand
(compare with ../01-pure_python/10_memory.py, where we did it manually).

🔑 IMPORTANT about the model: the OpenAI Agents SDK is a FRAMEWORK by OpenAI, but
   you can plug in ANY OpenAI-compatible model. So there's a switch here:
     "ollama" — free, local, no key (default)
     "openai" — OpenAI models (gpt-*), needs a paid OPENAI_API_KEY
   So an OpenAI key is NOT required — you can learn the framework for free.

⚠️ How it's simpler than CrewAI (../03-crewai/10_memory.py):
  • No separate embedding model needed.
  • Stores the VERBATIM chat history in a plain SQLite file (not vectors).
  • The `openai_memory.db` file can be opened with a SQLite viewer to see the messages.

Run:  uv run 02-openai_sdk/10_memory.py   (to quit — "выход" or "exit")
      To "forget everything" — delete the openai_memory.db file.
"""
# endregion

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ⬇️ РУБИЛЬНИК: "ollama" (локально, бесплатно) | "openai" (нужен ключ)
# ⬇️ SWITCH: "ollama" (local, free) | "openai" (needs a key)
PROVIDER = "ollama"

# RU: предохранитель — установлен ли фреймворк
# EN: guard — is the framework installed
try:
    from agents import (
        Agent, Runner, SQLiteSession,
        AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled,
    )
except ImportError:
    print("\n⚠️  Нет фреймворка. Установи:  uv pip install openai-agents\n")
    sys.exit(1)


def build_model():
    """
    RU: собрать модель под выбранного провайдера.
    EN: build the model for the chosen provider.
    """
    # ── RU: Вариант 1 — локальная Ollama (OpenAI-совместимый адрес) ──
    # ── EN: Option 1 — local Ollama (OpenAI-compatible endpoint) ──
    if PROVIDER == "ollama":
        # RU: трейсинг шлётся в OpenAI — при Ollama его выключаем, иначе ругань про ключ
        # EN: tracing goes to OpenAI — with Ollama we disable it, else it complains about a key
        set_tracing_disabled(disabled=True)
        client = AsyncOpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
        return OpenAIChatCompletionsModel(model="llama3.2", openai_client=client)

    # ── RU: Вариант 2 — модели OpenAI (нужен ключ) ──
    # ── EN: Option 2 — OpenAI models (needs a key) ──
    if not os.getenv("OPENAI_API_KEY") or "..." in os.getenv("OPENAI_API_KEY", ""):
        print("\n⚠️  PROVIDER='openai', но нет ключа OPENAI_API_KEY (впиши в .env).")
        print("    Или поставь PROVIDER = \"ollama\" — бесплатно, без ключа.\n")
        sys.exit(1)
    return "gpt-4o-mini"


# RU: файл-база рядом со скриптом (виден в папке 02-openai_sdk)
# EN: the file database next to the script (visible in the 02-openai_sdk folder)
DB_FILE = os.path.join(os.path.dirname(__file__), "openai_memory.db")


if __name__ == "__main__":
    agent = Agent(
        name="Ассистент",
        instructions=(
            "Ты — дружелюбный ассистент с памятью. Помни, что пользователь говорил "
            "раньше. Всегда отвечай на языке последнего сообщения пользователя."
        ),
        model=build_model(),
    )

    # RU: ВОТ ОНА — память включается созданием сессии.
    #     "user_dima" — id разговора (кому принадлежит память).
    #     DB_FILE — файл SQLite, в котором SDK сам хранит историю (переживёт перезапуск).
    # EN: HERE IT IS — memory is turned on by creating a session.
    #     "user_dima" — the conversation id (whose memory it is).
    #     DB_FILE — the SQLite file where the SDK stores history itself (survives restart).
    session = SQLiteSession("user_dima", DB_FILE)

    print(f"💬 Пиши сообщения боту / Type messages to the bot (модель / model: {PROVIDER}).")
    print("   Чтобы выйти / To quit — «выход» / «exit». Память в openai_memory.db.\n")

    while True:
        user_message = input("Вы / You: ").strip()
        if user_message.lower() in ("выход", "exit", "quit"):
            break
        if not user_message:
            continue

        # RU: передаём session — SDK сам подгрузит историю и сам сохранит новую реплику
        # EN: pass session — the SDK loads the history itself and saves the new turn itself
        result = Runner.run_sync(agent, user_message, session=session)
        print("Ассистент / Assistant:", result.final_output, "\n")

    print(f"\n💾 История сохранена в {os.path.basename(DB_FILE)} (обычный SQLite, не вектора).")
    print(f"💾 History saved to {os.path.basename(DB_FILE)} (a plain SQLite file, not vectors).")
    print("👉 Запусти файл ещё раз / Run the file again — бот вспомнит разговор / the bot will recall the conversation.")
