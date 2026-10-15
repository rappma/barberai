# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
06 — Паттерн Router (Маршрутизатор)
===================================
ИИ смотрит на вопрос и решает, какому «специалисту» его отдать.
    Вопрос → [ИИ-диспетчер определяет тему] → нужный специалист отвечает

💡 Где пригодится: умная поддержка (оплата → финансист, доставка → логист),
   сортировка писем по отделам.

Запуск:  uv run 01-pure_python/06_router.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
06 — The Router pattern
===================================
The AI looks at the question and decides which "specialist" to hand it to.
    Question → [AI dispatcher figures out the topic] → the right specialist answers

💡 Where useful: smart support (payment → finance, delivery → logistics),
   sorting emails by department.

Run:  uv run 01-pure_python/06_router.py
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


# RU: специалисты — тема → инструкция (system), кем быть ИИ
# EN: specialists — topic → instruction (system), who the AI should be
SPECIALISTS = {
    "код":      "Ты — опытный программист. Отвечай технически и по делу.",
    "финансы":  "Ты — финансовый консультант. Объясняй просто, без жаргона.",
    "здоровье": "Ты — врач-консультант. Будь аккуратен, советуй обратиться к специалисту.",
    "другое":   "Ты — эрудированный помощник. Отвечай кратко и понятно.",
}


def route(question: str) -> str:
    """
    RU: ШАГ 1 — спросить ИИ, к какой теме относится вопрос (маршрутизация).
    EN: STEP 1 — ask the AI which topic the question belongs to (the routing).
    """
    category = ask(
        "К какой ОДНОЙ категории относится вопрос? "
        "Выбери одно слово из списка: код, финансы, здоровье, другое. "
        f"Верни ТОЛЬКО это слово.\n\nВопрос: {question}"
    ).strip().lower()

    # RU: подстраховка — ищем известную категорию внутри ответа
    # EN: fallback — look for a known category inside the answer
    for key in SPECIALISTS:
        if key in category:
            return key
    return "другое"


if __name__ == "__main__":
    questions = [
        "Как развернуть сайт на сервере?",
        "Стоит ли откладывать 10% дохода?",
        "Что делать при лёгкой простуде?",
    ]

    for q in questions:
        category = route(q)                            # RU: куда направить / EN: where to route
        print(f"\nВопрос: {q}\nТема: [{category}]")
        answer = ask(q, system=SPECIALISTS[category])  # RU: отвечает специалист / EN: the specialist answers
        print("Ответ специалиста:\n", answer)

    # RU: ИИ сам распределил вопросы по ролям — это Router
    # EN: the AI distributed the questions to roles itself — that's a Router
