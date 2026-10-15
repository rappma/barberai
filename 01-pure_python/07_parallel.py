# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
07 — Паттерн Parallelization (Параллельность)
=============================================
Задачу режут на куски и обрабатывают ОДНОВРЕМЕННО, потом сводят результаты.
    [отзыв1] [отзыв2] [отзыв3] → все сразу → общий вывод

💡 Где пригодится: 500 отзывов за минуту, 100 резюме разом, сравнение товаров.

Запуск:  uv run 01-pure_python/07_parallel.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
07 — The Parallelization pattern
=============================================
The task is split into pieces and processed SIMULTANEOUSLY, then results merged.
    [review1] [review2] [review3] → all at once → overall conclusion

💡 Where useful: 500 reviews a minute, 100 resumes at once, product comparison.

Run:  uv run 01-pure_python/07_parallel.py
"""
# endregion

import os
import sys
# RU: ThreadPoolExecutor запускает задачи одновременно
# EN: ThreadPoolExecutor runs tasks simultaneously
from concurrent.futures import ThreadPoolExecutor
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


reviews = [
    "Кофе отличный, но очередь огромная.",
    "Невкусно и дорого, больше не приду.",
    "Уютно, милый персонал, вернусь ещё!",
]


def summarize(review: str) -> str:
    """
    RU: обработать ОДИН отзыв: позитив/негатив + суть одной фразой.
    EN: process ONE review: positive/negative + the gist in one phrase.
    """
    return ask(f"Одной короткой фразой: это позитив или негатив, и в чём суть? Отзыв: {review}")


if __name__ == "__main__":
    print("=== Обрабатываем все отзывы ОДНОВРЕМЕННО ===")

    # RU: ex.map применяет функцию к каждому элементу списка ПАРАЛЛЕЛЬНО
    # EN: ex.map applies the function to each list item IN PARALLEL
    with ThreadPoolExecutor() as ex:
        results = list(ex.map(summarize, reviews))

    for review, summary in zip(reviews, results):
        print(f"\n• {review}\n  → {summary}")

    # RU: сводим короткие выводы в один общий итог
    # EN: merge the short conclusions into one overall summary
    print("\n=== Общий вывод ===")
    overall = ask("Сведи эти оценки в один короткий вывод о заведении:\n" + "\n".join(results))
    print(overall)
