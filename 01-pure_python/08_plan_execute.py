# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
08 — Паттерн Plan-and-Execute (Планирование и исполнение)
=========================================================
Сначала ИИ составляет ВЕСЬ план, потом выполняет его по шагам. В отличие от
Chain, где шаги задаём мы, здесь план придумывает сам ИИ.
    Цель → [ИИ строит план] → [шаг 1] [шаг 2] ... → итог

💡 Где пригодится: «запусти рекламную кампанию» — ИИ сам планирует и делает шаги.

Запуск:  uv run 01-pure_python/08_plan_execute.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
08 — The Plan-and-Execute pattern
=========================================================
First the AI builds the WHOLE plan, then executes it step by step. Unlike Chain,
where we set the steps, here the AI comes up with the plan itself.
    Goal → [AI builds a plan] → [step 1] [step 2] ... → result

💡 Where useful: "launch an ad campaign" — the AI plans and does the steps itself.

Run:  uv run 01-pure_python/08_plan_execute.py
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
    goal = "Подготовить запуск Telegram-канала про домашний кофе"

    # RU: ШАГ 1 — ИИ составляет план; каждый шаг с новой строки, с "- "
    # EN: STEP 1 — the AI builds the plan; each step on its own line, with "- "
    print("=== План ===")
    plan_text = ask(
        f"Составь короткий план (3–4 шага) для цели: {goal}. "
        "Каждый шаг — с новой строки, начинай строку с '- '. Без лишних слов."
    )
    print(plan_text)

    # RU: достаём строки-шаги (начинаются с "-")
    # EN: extract the step lines (they start with "-")
    steps = [line.strip(" -") for line in plan_text.splitlines() if line.strip().startswith("-")]

    # RU: ШАГ 2 — выполняем каждый шаг по очереди
    # EN: STEP 2 — execute each step one by one
    results = []
    for i, step in enumerate(steps, start=1):
        print(f"\n=== Выполняю шаг {i}: {step} ===")
        result = ask(
            f"Цель: {goal}\nВыполни конкретно этот шаг и дай готовый результат:\n{step}"
        )
        print(result)
        results.append(f"Шаг {i} ({step}):\n{result}")

    # RU: ШАГ 3 — общий итог
    # EN: STEP 3 — the overall result
    print("\n=== ИТОГ ===")
    final = ask("Собери из результатов шагов короткое финальное резюме:\n\n" + "\n\n".join(results))
    print(final)
