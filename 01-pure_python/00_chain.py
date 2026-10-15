# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
00 — Chain (цепочка) + переключение моделей (локальная ↔ Google)
================================================================
Два в одном:
  1) РУБИЛЬНИК модели: меняешь PROVIDER — отвечает Ollama (локально, бесплатно)
     или Google Gemini (облако, нужен GOOGLE_API_KEY в .env). Функция ask() одна.
  2) CHAIN (цепочка): выход одного вызова = вход следующего.
     Тема → [написать пост] → [сократить] → [перевести]

Запуск (из корня проекта):  uv run 01-pure_python/00_chain.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
00 — Chain + model switching (local ↔ Google)
================================================================
Two in one:
  1) MODEL SWITCH: change PROVIDER — either Ollama (local, free) or Google
     Gemini (cloud, needs GOOGLE_API_KEY in .env) answers. One ask() function.
  2) CHAIN: the output of one call = the input of the next.
     Topic → [write a post] → [shorten] → [translate]

Run (from the project root):  uv run 01-pure_python/00_chain.py
"""
# endregion

import os
import sys
# RU: библиотека локальной модели (Ollama)
# EN: local-model library (Ollama)
import ollama
# RU: универсальная «трубка»; ею же зовём Gemini
# EN: universal client; it also calls Gemini
from openai import OpenAI
from dotenv import load_dotenv

# RU: читаем .env и кладём ключи в окружение, чтобы os.getenv их увидел
# EN: read .env and load the keys into the environment so os.getenv sees them
load_dotenv()

# RU: РУБИЛЬНИК: "ollama" (локально, бесплатно) | "gemini" (облако Google)
# EN: SWITCH: "ollama" (local, free) | "gemini" (Google cloud)
PROVIDER = "gemini"


def ask(prompt: str, system: str = "Ты — помощник. Отвечай кратко.") -> str:
    """
    RU: задать вопрос выбранной модели и вернуть текст ответа.
    EN: ask the chosen model and return the answer text.
    """

    # ── RU: Вариант 1 — локальная Ollama ──
    # ── EN: Option 1 — local Ollama ──
    if PROVIDER == "ollama":
        # RU: шлём два сообщения: system (роль) и user (наш вопрос)
        # EN: send two messages: system (role) and user (our question)
        response = ollama.chat(
            model="llama3.2",   # RU: или "qwen2.5" (лучше для русского) / EN: or "qwen2.5"
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )
        # RU: у Ollama текст лежит в response.message.content
        # EN: Ollama puts the text in response.message.content
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

    # ── RU: Вариант 2 — облачный Gemini ──
    # ── EN: Option 2 — cloud Gemini ──
    # RU: предохранитель — без ключа понятная подсказка, а не краш
    # EN: guard — a clear hint instead of a crash when there's no key
    key = os.getenv("GOOGLE_API_KEY")
    if not key or "..." in key:
        print("\n⚠️  Нет ключа GOOGLE_API_KEY в .env. / No GOOGLE_API_KEY in .env.")
        print("    Ключ / key: https://aistudio.google.com/apikey\n")
        sys.exit(1)

    # RU: та же «трубка», но с адресом Google (base_url) → звонок уходит в Gemini
    # EN: same client, but with Google's base_url → the call goes to Gemini
    client = OpenAI(
        api_key=key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    response = client.chat.completions.create(
        model="gemini-3.8-flash",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    # RU: у OpenAI-совместимых текст глубже: choices[0].message.content
    # EN: for OpenAI-compatible, the text is deeper: choices[0].message.content
    return response.choices[0].message.content


if __name__ == "__main__":
    print(f"Сейчас работает / Now running: {PROVIDER}\n")

    topic = "польза утренней пробежки"

    # RU: ШАГ 1 — написать пост
    # EN: STEP 1 — write a post
    post = ask(
        f"Напиши короткий пост для соцсетей на тему: {topic}",
        system="Ты — копирайтер. Пиши живо.",
    )
    print("=== Шаг 1: пост ===\n", post, "\n")

    # RU: ШАГ 2 — вход = результат шага 1
    # EN: STEP 2 — input = result of step 1
    short = ask(
        f"Сократи этот текст до одного цепляющего предложения:\n\n{post}",
        system="Ты — редактор.",
    )
    print("=== Шаг 2: сократили ===\n", short, "\n")

    # RU: ШАГ 3 — вход = результат шага 2
    # EN: STEP 3 — input = result of step 2
    english = ask(
        f"Переведи на английский, сохранив тон:\n\n{short}",
        system="Ты — переводчик.",
    )
    print("=== Шаг 3: перевод ===\n", english)

    # RU: три вызова в конвейере — это Chain; сменишь PROVIDER — та же цепочка на другой модели
    # EN: three calls in a pipeline = Chain; change PROVIDER — the same chain on another model
