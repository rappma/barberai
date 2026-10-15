# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
09 — Паттерн Orchestrator (Дирижёр и специалисты)
=================================================
Дирижёр раздаёт РАЗНЫЕ части задачи РАЗНЫМ специалистам и собирает результат.
Отличие от Plan-and-Execute: там одна роль идёт по шагам, тут разные роли.
    Задача → [специалист A] [B] [C] → дирижёр собирает

💡 Где пригодится: лендинг силами «отдела» — заголовок, текст, призыв.

Запуск:  uv run 01-pure_python/09_orchestrator.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
09 — The Orchestrator pattern (conductor and specialists)
=================================================
The conductor hands DIFFERENT parts of the task to DIFFERENT specialists and
assembles the result. Unlike Plan-and-Execute (one role, step by step) — here
different roles work on different pieces.
    Task → [specialist A] [B] [C] → the conductor assembles

💡 Where useful: a landing page by a "department" — headline, body, CTA.

Run:  uv run 01-pure_python/09_orchestrator.py
"""
# endregion

import os
import sys
import ollama                       # RU: библиотека локальной модели (Ollama) // EN: local-model library (Ollama)
from openai import OpenAI           # RU: универсальная «трубка»; ею же зовём Gemini // EN: universal client; it also calls Gemini
from dotenv import load_dotenv

# RU: читаем .env и кладём ключи в окружение // EN: read .env and load the keys into the environment
load_dotenv()

# ⬇️ РУБИЛЬНИК: "ollama" (локально, бесплатно) | "gemini" (облако Google)
# ⬇️ SWITCH: "ollama" (local, free) | "gemini" (Google cloud)
PROVIDER = "gemini"


def ask(prompt: str, system: str = "Ты — помощник. Отвечай по делу и кратко.") -> str:
    """
    RU: задать вопрос выбранной модели и вернуть текст ответа.
    EN: ask the chosen model and return the answer text.
    """
    # ── RU: Вариант 1 — локальная Ollama / EN: Option 1 — local Ollama ──
    if PROVIDER == "ollama":
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )
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
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    brand = "кофейня «Зерно» — кофе в зёрнах для дома"

    print("=== Специалисты работают над своими частями ===")

    # RU: специалист 1 — заголовок
    # EN: specialist 1 — the headline
    headline = ask(
        f"Придумай один цепляющий заголовок для лендинга бренда: {brand}",
        system="Ты — маркетолог-копирайтер.",
    )
    print("\nЗаголовок:\n", headline)

    # RU: специалист 2 — блок «о нас»
    # EN: specialist 2 — the "about us" block
    about = ask(
        f"Напиши короткий абзац «о нас» для бренда: {brand}",
        system="Ты — бренд-райтер, пишешь тёплым голосом.",
    )
    print("\nО нас:\n", about)

    # RU: специалист 3 — призыв к действию (кнопка)
    # EN: specialist 3 — the call to action (button)
    cta = ask(
        f"Придумай короткий призыв к действию (текст кнопки) для бренда: {brand}",
        system="Ты — специалист по конверсии.",
    )
    print("\nПризыв:\n", cta)

    # RU: дирижёр собирает части в цельный лендинг
    # EN: the conductor assembles the parts into a whole landing page
    print("\n=== Дирижёр собирает всё вместе ===")
    page = ask(
        "Собери цельный текст лендинга из этих частей, чтобы звучало гладко:\n\n"
        f"Заголовок: {headline}\n\nО нас: {about}\n\nКнопка: {cta}",
        system="Ты — редактор, делаешь из кусков цельный текст.",
    )
    print(page)
