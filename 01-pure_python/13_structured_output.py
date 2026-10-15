# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
13 — Structured Output: строгий JSON вместо свободного текста
=============================================================
Чтобы надёжно работать дальше (записать в базу, передать другому шагу), нужен
предсказуемый формат. Просим модель вернуть строго JSON и парсим; пришёл
не-JSON — просим ещё раз. Работает на любой модели.

💡 Где пригодится: извлечь {имя, телефон, услуга} из сообщения → сразу в CRM.

Запуск:  uv run 01-pure_python/13_structured_output.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
13 — Structured Output: strict JSON instead of free text
=============================================================
To work reliably afterwards (save to a DB, pass to another step) you need a
predictable format. We ask the model for strict JSON and parse it; if non-JSON
comes back — we ask again. Works on any model.

💡 Where useful: extract {name, phone, service} from a message → straight to a CRM.

Run:  uv run 01-pure_python/13_structured_output.py
"""
# endregion

import os
import sys
import json
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


def extract(text: str) -> dict | None:
    """
    RU: извлечь данные клиента в виде словаря (через JSON от модели).
    EN: extract the client's data as a dictionary (via JSON from the model).
    """
    prompt = (
        "Извлеки данные клиента из сообщения и верни СТРОГО JSON с полями "
        "name, phone, service. Если поля нет — поставь null. "
        "Верни ТОЛЬКО JSON, без пояснений и без ```.\n\n"
        f"Сообщение: {text}"
    )

    # RU: максимум 2 попытки — модель иногда добавляет лишний текст
    # EN: at most 2 attempts — the model sometimes adds extra text
    for _ in range(2):
        raw = ask(prompt)
        data = _try_parse_json(raw)
        if data is not None:
            return data
        prompt += "\nТы вернул не валидный JSON. Верни ТОЛЬКО корректный JSON."
    return None


def _try_parse_json(raw: str) -> dict | None:
    """
    RU: достать JSON из ответа: кусок от первой { до последней }.
    EN: pull JSON out of the answer: the chunk from the first { to the last }.
    """
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(raw[start:end + 1])
    except json.JSONDecodeError:
        return None


if __name__ == "__main__":
    message = "Здравствуйте! Меня зовут Иван, хочу записаться на стрижку, мой номер 8 900 123-45-67."
    print("Сообщение:", message, "\n")

    data = extract(message)
    print("Извлечено (словарь):", data)

    # RU: поля достаются по именам — удобно использовать дальше
    # EN: fields are accessed by name — convenient to use further
    if data:
        print("  Имя:    ", data.get("name"))
        print("  Услуга: ", data.get("service"))
        print("  Телефон:", data.get("phone"))
