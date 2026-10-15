# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
12 — RAG-lite: бот отвечает по своей БАЗЕ ЗНАНИЙ
================================================
RAG = подсунуть модели ТВОИ факты (цены, меню, правила), чтобы она отвечала
по ним, а не выдумывала. Здесь простой вариант: вся база кладётся в системный
промпт (для больших баз добавляют шаг «поиск» по кускам).

💡 Где пригодится: бот поддержки, консультант магазина/кафе — ответы по своим данным.

Запуск:  uv run 01-pure_python/12_rag_knowledge.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
12 — RAG-lite: the bot answers from its own KNOWLEDGE BASE
================================================
RAG = feed the model YOUR facts (prices, menu, rules) so it answers from them
instead of making things up. Here the simple variant: the whole base goes into
the system prompt (for large bases you add a "search" step over chunks).

💡 Where useful: a support bot, a shop/café consultant — answers from your data.

Run:  uv run 01-pure_python/12_rag_knowledge.py
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


# RU: файл с фактами лежит рядом со скриптом
# EN: the facts file sits next to the script
KNOWLEDGE_FILE = os.path.join(os.path.dirname(__file__), "knowledge.txt")


def load_knowledge() -> str:
    """
    RU: прочитать базу знаний из файла.
    EN: read the knowledge base from the file.
    """
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return f.read()


def answer(question: str, knowledge: str) -> str:
    """
    RU: ответить ТОЛЬКО по фактам из базы (главный приём RAG).
    EN: answer ONLY from the facts in the base (the main RAG trick).
    """
    system = (
        "Ты — консультант. Отвечай ТОЛЬКО на основе фактов ниже. "
        "Если ответа в фактах нет — честно скажи, что не знаешь, и не выдумывай.\n\n"
        "ФАКТЫ:\n" + knowledge
    )
    return ask(question, system=system)


if __name__ == "__main__":
    kb = load_knowledge()

    questions = [
        "Сколько стоит капучино?",          # RU: есть в фактах / EN: in the facts
        "Вы работаете в воскресенье?",      # RU: есть в фактах / EN: in the facts
        "А у вас есть детская площадка?",   # RU: НЕТ в фактах — бот должен честно сказать / EN: NOT in the facts
    ]

    for q in questions:
        print("❓", q)
        print("🤖", answer(q, kb), "\n")
