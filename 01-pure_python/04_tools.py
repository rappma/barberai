# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
04 — Паттерн Tool Calling (Инструменты)
=======================================
LLM сам решает, какую функцию вызвать и с какими аргументами, а выполняем её МЫ
(Python). Результат возвращаем в LLM — он формулирует финальный ответ.

МОДЕЛЬ — переключатель PROVIDER ниже: по умолчанию локальный qwen2.5 (🆓 бесплатно,
offline), либо облачный gemini. Для tool calling нужна умная модель — qwen2.5 годится,
а слабая llama3.2 путается в вызовах.

💡 Где пригодится: бот записывает в CRM, шлёт уведомления, считает, бронирует.

Запуск:  uv run 01-pure_python/04_tools.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
04 — The Tool Calling pattern
=======================================
The LLM decides which function to call and with which arguments, but WE (Python)
run it. We return the result to the LLM — it formulates the final answer.

MODEL — the PROVIDER switch below: local qwen2.5 by default (🆓 free, offline),
or the cloud gemini. Tool calling needs a capable model — qwen2.5 is fine, while
the weak llama3.2 fumbles the calls.

💡 Where useful: a bot writes to a CRM, sends notifications, calculates, books.
ollama pull qwen2.5

Run:  uv run 01-pure_python/04_tools.py
"""
# endregion

import os
import sys
import math
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ⬇️ РУБИЛЬНИК: "ollama" (локально, бесплатно) | "gemini" (облако Google)
# ⬇️ SWITCH: "ollama" (local, free) | "gemini" (Google cloud)
PROVIDER = "ollama"

OLLAMA_MODEL = "qwen2.5"           # RU: локальная модель (ollama pull qwen2.5) / EN: local model
GEMINI_MODEL = "gemini-2.5-flash"  # RU: облачная модель / EN: cloud model

# RU: секрет — Ollama говорит «на языке OpenAI» по адресу localhost, поэтому и локально,
#     и в облаке используем ОДНУ библиотеку openai и ОДИН и тот же цикл ниже. Меняется
#     только адрес (base_url), ключ и имя модели.
# EN: the trick — Ollama speaks "OpenAI's language" at localhost, so both locally and
#     in the cloud we use ONE openai library and the SAME loop below. Only the address
#     (base_url), key and model name change.
if PROVIDER == "ollama":
    MODEL = OLLAMA_MODEL
    client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
elif PROVIDER == "gemini":
    key = os.getenv("GOOGLE_API_KEY")
    if not key or "..." in key:
        print("\n⚠️  Нет ключа GOOGLE_API_KEY в .env. / No GOOGLE_API_KEY in .env.")
        print("    Бесплатный ключ / free key: https://aistudio.google.com/apikey\n")
        sys.exit(1)
    MODEL = GEMINI_MODEL
    client = OpenAI(api_key=key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
else:
    # RU: защита от опечатки в слове (например "olama") — иначе молча пошло бы не туда
    # EN: guard against a typo in the word (e.g. "olama") — otherwise it'd silently misroute
    print(f"\n⚠️  Неизвестный PROVIDER={PROVIDER!r}. Допустимо: 'ollama' или 'gemini'.")
    print(f"    Unknown PROVIDER={PROVIDER!r}. Allowed: 'ollama' or 'gemini'.\n")
    sys.exit(1)


# ⬇️ ЯЗЫК примера: "ru" (русский) | "en" (English) — на нём будут задача и ответ
# ⬇️ Example LANGUAGE: "ru" (Russian) | "en" (English) — the task and the answer language
LANG = "ru"

# RU: языковое правило — без него слабая модель мешает языки (см. вывод в терминале)
# EN: language rule — without it a weak model mixes languages (see the terminal output)
SYSTEM = {
    "ru": "Ты — помощник с инструментами. Отвечай СТРОГО на русском языке; не вставляй английские слова.",
    "en": "You are a tool-using assistant. Reply STRICTLY in English; do not insert Russian words.",
}[LANG]

# RU: задача на двух языках — выбирается по LANG выше
# EN: the task in two languages — picked by LANG above
TASK = {
    "ru": ("Посчитай, сколько плитки нужно на крышу 50 м², если одна плитка 0.25 м². "
           "Потом сохрани итог в заметку."),
    "en": ("Calculate how many tiles are needed for a 50 m² roof if one tile is 0.25 m². "
           "Then save the result to a note."),
}[LANG]


# ── RU: 1. Реальные функции (выполняет Python) ──
# ── EN: 1. Real functions (run by Python) ──

def calculate_tiles(roof_area: float, tile_size: float, reserve_percent: float = 10) -> str:
    """
    RU: сколько плиток нужно на крышу, с запасом.
    EN: how many tiles are needed for the roof, with a reserve.
    """
    base = roof_area / tile_size
    total = math.ceil(base * (1 + reserve_percent / 100))
    return f"Нужно {total} плиток (площадь {roof_area} м², плитка {tile_size} м², запас {reserve_percent}%)."


def save_note(text: str) -> str:
    """
    RU: «сохраняем» заметку (для демо просто печатаем).
    EN: "save" a note (for the demo we just print it).
    """
    print(f"   [save_note] 📝 сохранено: {text}")
    return "Заметка сохранена."


# ── RU: 2. Описание инструментов для модели (формат OpenAI/Gemini) ──
# ── EN: 2. Tool descriptions for the model (OpenAI/Gemini format) ──
# RU: модель видит имя, назначение и схему аргументов — по ним решает, что вызвать
# EN: the model sees the name, purpose and argument schema — it decides what to call

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_tiles",
            "description": "Рассчитать количество плитки на крышу заданной площади.",
            "parameters": {
                "type": "object",
                "properties": {
                    "roof_area": {"type": "number", "description": "Площадь крыши в м²"},
                    "tile_size": {"type": "number", "description": "Площадь одной плитки в м²"},
                    "reserve_percent": {"type": "number", "description": "Запас в процентах (по умолчанию 10)"},
                },
                "required": ["roof_area", "tile_size"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Сохранить короткую текстовую заметку.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Текст заметки"},
                },
                "required": ["text"],
            },
        },
    },
]


# ── RU: 3. Диспетчер: имя инструмента → Python-функция ──
# ── EN: 3. Dispatcher: tool name → Python function ──

def run_tool(name: str, arguments: dict) -> str:
    if name == "calculate_tiles":
        return calculate_tiles(**arguments)
    elif name == "save_note":
        return save_note(**arguments)
    else:
        return f"Неизвестный инструмент: {name}"


# ── RU: 4. Цикл вызова ──
# ── EN: 4. The call loop ──

def chat_with_tools(user_message: str) -> str:
    # RU: системный промпт задаёт язык ответа / EN: the system prompt sets the answer language
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_message},
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,   # RU: передаём список инструментов / EN: pass the list of tools
        )
        msg = response.choices[0].message

        # RU: модель не просит инструмент — она готова ответить, выходим
        # EN: the model doesn't request a tool — it's ready to answer, we exit
        if not msg.tool_calls:
            return msg.content

        # RU: сохраняем ход модели (с запросами инструментов) в историю
        # EN: save the model's turn (with tool requests) into the history
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ],
        })

        # RU: выполняем запрошенные инструменты и возвращаем результаты
        # EN: run the requested tools and return the results
        for tc in msg.tool_calls:
            arguments = json.loads(tc.function.arguments)
            print(f"   [LLM вызвал] {tc.function.name}({json.dumps(arguments, ensure_ascii=False)})")
            result = run_tool(tc.function.name, arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,   # RU: тот же id, что прислал LLM / EN: same id the LLM sent
                "content": result,
            })
        # RU: ...и цикл идёт снова: теперь LLM видит результаты и продолжает
        # EN: ...and the loop runs again: now the LLM sees the results and continues


if __name__ == "__main__":
    print("Задача / Task:", TASK, "\n")
    final = chat_with_tools(TASK)
    print("\nФинальный ответ агента / Agent's final answer:\n", final)
