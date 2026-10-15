# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
11 — Настоящие инструменты (агент ДЕЛАЕТ видимые вещи)
======================================================
Инструменты, результат которых видно и слышно:
  🌤️ get_weather — реальная погода;  🔊 say_aloud — Mac говорит вслух;
  🔔 show_notification — всплывает уведомление.
«Мозг» (что вызвать) — переключатель PROVIDER ниже: по умолчанию локальный qwen2.5
(🆓 бесплатно, offline), либо облачный gemini. Для tool calling бери qwen2.5, не llama3.2.

⚠️ `say` и уведомление — только macOS; погода — везде.
💡 Где пригодится: бот пишет в CRM, шлёт уведомления, бронирует, отправляет письма.

Запуск:  uv run 01-pure_python/11_real_tools.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
11 — Real tools (the agent DOES visible things)
======================================================
Tools whose result you can see and hear:
  🌤️ get_weather — real weather;  🔊 say_aloud — the Mac speaks aloud;
  🔔 show_notification — a notification pops up.
The "brain" (what to call) — the PROVIDER switch below: local qwen2.5 by default
(🆓 free, offline), or the cloud gemini. For tool calling use qwen2.5, not llama3.2.

⚠️ `say` and the notification are macOS only; the weather works everywhere.
💡 Where useful: a bot writes to a CRM, sends notifications, books, sends emails.

Run:  uv run 01-pure_python/11_real_tools.py
"""
# endregion

import os
import sys
import json
# RU: subprocess запускает команды компьютера (say, osascript)
# EN: subprocess runs computer commands (say, osascript)
import subprocess
import urllib.parse
import urllib.request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ⬇️ РУБИЛЬНИК: "ollama" (локально, бесплатно) | "gemini" (облако Google)
# ⬇️ SWITCH: "ollama" (local, free) | "gemini" (Google cloud)
PROVIDER = "ollama"

OLLAMA_MODEL = "qwen2.5"           # RU: локальная модель (ollama pull qwen2.5) / EN: local model
GEMINI_MODEL = "gemini-2.5-flash"  # RU: облачная модель / EN: cloud model

# RU: Ollama говорит «на языке OpenAI» по адресу localhost → та же библиотека и тот же
#     цикл, что для Gemini. Меняются только адрес, ключ и имя модели.
# EN: Ollama speaks "OpenAI's language" at localhost → the same library and the same
#     loop as for Gemini. Only the address, key and model name change.
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
    print(f"\n⚠️  Неизвестный PROVIDER={PROVIDER!r}. Допустимо: 'ollama' или 'gemini'.")
    print(f"    Unknown PROVIDER={PROVIDER!r}. Allowed: 'ollama' or 'gemini'.\n")
    sys.exit(1)


# ⬇️ ЯЗЫК примера: "ru" (русский) | "en" (English) — задача, ответ и язык погоды
# ⬇️ Example LANGUAGE: "ru" (Russian) | "en" (English) — task, answer and weather language
LANG = "ru"

# RU: языковое правило — без него слабая модель мешает языки
# EN: language rule — without it a weak model mixes languages
SYSTEM = {
    "ru": "Ты — агент с инструментами. Отвечай СТРОГО на русском языке; не вставляй английские слова.",
    "en": "You are a tool-using agent. Reply STRICTLY in English; do not insert Russian words.",
}[LANG]

# RU: задача на двух языках — выбирается по LANG выше
# EN: the task in two languages — picked by LANG above
TASK = {
    "ru": ("Узнай погоду в Москве. Затем скажи её вслух и покажи "
           "уведомление с заголовком «Погода» и текстом погоды."),
    "en": ('Find out the weather in Moscow. Then say it aloud and show a '
           'notification titled "Weather" with the weather text.'),
}[LANG]


# ── RU: 1. Настоящие функции-инструменты ──
# ── EN: 1. Real tool functions ──

def get_weather(city: str) -> str:
    """
    RU: реальная погода через бесплатный wttr.in (без ключа).
    EN: real weather via the free wttr.in (no key).
    """
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=3&lang={LANG}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.read().decode("utf-8").strip()
    except Exception as error:
        return f"Не удалось узнать погоду: {error}"


def say_aloud(text: str) -> str:
    """
    RU: Mac произносит текст вслух (команда macOS `say`).
    EN: the Mac speaks the text aloud (the macOS `say` command).
    """
    try:
        subprocess.run(["say", text], check=True)
        return "Сказано вслух."
    except Exception as error:
        return f"Не получилось озвучить: {error}"


def show_notification(title: str, message: str) -> str:
    """
    RU: всплывающее уведомление macOS (osascript).
    EN: a macOS pop-up notification (osascript).
    """
    safe_title = title.replace('"', "'")
    safe_message = message.replace('"', "'")
    script = f'display notification "{safe_message}" with title "{safe_title}"'
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        return "Уведомление показано."
    except Exception as error:
        return f"Не получилось показать уведомление: {error}"


# ── RU: 2. Описание инструментов для модели (формат OpenAI/Gemini) ──
# ── EN: 2. Tool descriptions for the model (OpenAI/Gemini format) ──

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Узнать текущую погоду в указанном городе.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "Название города"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "say_aloud",
            "description": "Произнести текст вслух через динамики компьютера.",
            "parameters": {
                "type": "object",
                "properties": {"text": {"type": "string", "description": "Что сказать вслух"}},
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "show_notification",
            "description": "Показать всплывающее уведомление на экране.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Заголовок уведомления"},
                    "message": {"type": "string", "description": "Текст уведомления"},
                },
                "required": ["title", "message"],
            },
        },
    },
]


# ── RU: 3. Диспетчер: имя → функция ──
# ── EN: 3. Dispatcher: name → function ──

def run_tool(name: str, arguments: dict) -> str:
    if name == "get_weather":
        return get_weather(**arguments)
    elif name == "say_aloud":
        return say_aloud(**arguments)
    elif name == "show_notification":
        return show_notification(**arguments)
    return f"Неизвестный инструмент: {name}"


# ── RU: 4. Цикл агента (тот же, что в файле 04) ──
# ── EN: 4. The agent loop (the same as in file 04) ──

def run_agent(user_message: str) -> str:
    # RU: системный промпт задаёт язык ответа / EN: the system prompt sets the answer language
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_message},
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message

        # RU: инструмент не нужен — модель готова ответить
        # EN: no tool needed — the model is ready to answer
        if not msg.tool_calls:
            return msg.content

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ],
        })

        # RU: выполняем инструменты — тут происходят настоящие действия
        # EN: run the tools — this is where the real actions happen
        for tc in msg.tool_calls:
            arguments = json.loads(tc.function.arguments)
            print(f"   🛠️  агент вызвал: {tc.function.name}({json.dumps(arguments, ensure_ascii=False)})")
            result = run_tool(tc.function.name, arguments)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})


if __name__ == "__main__":
    print("Задача / Task:", TASK, "\n")
    final = run_agent(TASK)
    print("\nФинальный ответ агента / Agent's final answer:\n", final)
