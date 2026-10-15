# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
10 — Паттерн Memory (Память между запусками)
============================================
Живой диалог в терминале с настоящей памятью. Весь разговор сохраняется в файл
memory.json ПОСЛЕ КАЖДОГО сообщения. Закрой файл, запусти снова — бот продолжит
разговор с того же места, помня всё, что ты писал раньше.

Так работает «долгая память»: модель сама ничего не помнит — мы храним историю
в файле и подгружаем её обратно при следующем запуске.

💡 Где пригодится: ассистент, помнящий тебя между сессиями; бот с историей клиента.

Запуск:  uv run 01-pure_python/10_memory.py   (для выхода — набери "выход" или "exit")
         Чтобы «забыть всё» и начать заново — удали файл memory.json.
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
10 — The Memory pattern (memory between runs)
============================================
A live terminal chat with real memory. The whole conversation is saved to
memory.json AFTER EVERY message. Close the file, run it again — the bot picks up
the conversation right where it left off, remembering everything you wrote before.

That's how "long-term memory" works: the model itself remembers nothing — we
store the history in a file and load it back on the next run.

💡 Where useful: an assistant that remembers you between sessions; a client-history bot.

Run:  uv run 01-pure_python/10_memory.py   (to quit, type "выход" or "exit")
      To "forget everything" and start over — delete the memory.json file.
"""
# endregion

import os
import sys
import json
import ollama                       # RU: библиотека локальной модели (Ollama) // EN: local-model library (Ollama)
from openai import OpenAI           # RU: универсальная «трубка»; ею же зовём Gemini // EN: universal client; it also calls Gemini
from dotenv import load_dotenv

# RU: читаем .env и кладём ключи в окружение, чтобы os.getenv их увидел
# EN: read .env and load the keys into the environment so os.getenv sees them
load_dotenv()

# ⬇️ РУБИЛЬНИК: "ollama" (локально, бесплатно) | "gemini" (облако Google)
# ⬇️ SWITCH: "ollama" (local, free) | "gemini" (Google cloud)
PROVIDER = "gemini"

MEMORY_FILE = "memory.json"  # RU: сюда сохраняем весь разговор / EN: we save the whole conversation here


def ask(messages: list[dict]) -> str:
    """
    RU: отправить модели ВЕСЬ список сообщений (а не один вопрос) — так бот видит
        весь ход разговора и «помнит» контекст в рамках сессии.
    EN: send the model the WHOLE list of messages (not just one question) — so the
        bot sees the full conversation and "remembers" the context within the session.
    """
    # ── RU: Вариант 1 — локальная Ollama / EN: Option 1 — local Ollama ──
    if PROVIDER == "ollama":
        response = ollama.chat(model="llama3.2", messages=messages)
        return response.message.content

    # RU: предохранитель — если PROVIDER не "ollama" и не "gemini", это, скорее
    #     всего, опечатка (например "olama") — сообщаем прямо, а не молча
    #     соскальзываем в Gemini.
    # EN: guard — if PROVIDER is neither "ollama" nor "gemini", it's most
    #     likely a typo (e.g. "olama") — tell the user directly instead of
    #     silently falling through to Gemini.
    if PROVIDER != "gemini":
        print(f"\n⚠️  Неизвестный PROVIDER='{PROVIDER}' — похоже на опечатку. "
              f"Допустимые значения: \"ollama\" или \"gemini\".")
        print(f"⚠️  Unknown PROVIDER='{PROVIDER}' — looks like a typo. "
              f"Allowed values: \"ollama\" or \"gemini\".\n")
        sys.exit(1)

    # ── RU: Вариант 2 — облачный Gemini / EN: Option 2 — cloud Gemini ──
    key = os.getenv("GOOGLE_API_KEY")
    if not key or "..." in key:
        print("\n⚠️  Нет ключа GOOGLE_API_KEY в .env. / No GOOGLE_API_KEY in .env.")
        print("    Ключ / key: https://aistudio.google.com/apikey\n")
        sys.exit(1)
    client = OpenAI(
        api_key=key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    response = client.chat.completions.create(model="gemini-3.8-flash", messages=messages)
    return response.choices[0].message.content


def load_conversation() -> list[dict]:
    """
    RU: прочитать сохранённый разговор из файла (нет файла — память пустая).
    EN: read the saved conversation from the file (no file — memory is empty).
    """
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_conversation(history: list[dict]) -> None:
    """
    RU: сохранить весь разговор обратно в файл (перезаписываем целиком).
    EN: save the whole conversation back to the file (rewrite it entirely).
    """
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # RU: 1) подгружаем прошлый разговор (долгая память между запусками)
    # EN: 1) load the previous conversation (long-term memory between runs)
    history = load_conversation()   # RU: только user/assistant / EN: user/assistant only
    if history:
        print(f"🧠 Помню прошлый разговор / Remember the past chat: {len(history)} сообщ. / msgs")
    else:
        print("🧠 Память пуста — это первый разговор. / Memory is empty — this is the first chat.")
    print("💬 Пиши сообщения боту / Type messages to the bot. Чтобы выйти / To quit — «выход» / «exit».\n")

    # RU: 2) системная инструкция (в файл её НЕ сохраняем — только реплики).
    #        Просим модель зеркалить язык последнего сообщения пользователя.
    # EN: 2) the system instruction (NOT saved to the file — only the turns are).
    #        We ask the model to mirror the language of the user's last message.
    system = (
        "Ты — личный ассистент с памятью. Помни всё, что пользователь говорил в этом "
        "разговоре, и используй это в ответах. "
        "ВАЖНОЕ ПРАВИЛО: всегда отвечай СТРОГО на том языке, на котором написано "
        "последнее сообщение пользователя. Английский вопрос — английский ответ. "
        "Русский вопрос — русский ответ. Никогда не переключайся на другой язык сам."
    )

    # RU: 3) живой цикл диалога. conversation = система + вся история + новые реплики.
    # EN: 3) the live dialogue loop. conversation = system + full history + new turns.
    while True:
        user_message = input("Вы / You: ").strip()
        if user_message.lower() in ("выход", "exit", "quit"):
            break
        if not user_message:
            continue

        history.append({"role": "user", "content": user_message})
        # RU: собираем полный список для модели: system + вся история
        # EN: build the full list for the model: system + the whole history
        conversation = [{"role": "system", "content": system}] + history
        answer = ask(conversation)
        history.append({"role": "assistant", "content": answer})
        print("Ассистент / Assistant:", answer, "\n")

        # RU: 4) сохраняем ПОСЛЕ КАЖДОГО сообщения — файл появляется сразу и
        #        переживёт даже закрытие терминала (не нужно ждать выхода).
        # EN: 4) save AFTER EVERY message — the file appears right away and
        #        survives even closing the terminal (no need to wait for exit).
        save_conversation(history)

    print(f"\n💾 Разговор сохранён в {MEMORY_FILE} / Conversation saved to {MEMORY_FILE}.")
    print("👉 Запусти файл ещё раз / Run the file again — бот продолжит с этого места / "
          "the bot will continue from here.")
