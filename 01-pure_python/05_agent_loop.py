# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
05 — Паттерн Agent Loop (Цикл агента)
=====================================
Дай LLM инструменты и крути его в цикле — он САМ составит план и САМ выполнит.
Определение агента: «LLM гоняет инструменты в цикле, пока не достигнет цели».
Здесь инструменты — вести todo-список и отмечать сделанное. План мы НЕ диктуем.

МОДЕЛЬ — переключатель PROVIDER ниже: по умолчанию локальный qwen2.5 (🆓 бесплатно,
offline), либо облачный gemini. Слабая llama3.2 в цикле путается — бери qwen2.5.

💡 Где пригодится: исследовательский ассистент, агент-программист.

Запуск:  uv run 01-pure_python/05_agent_loop.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
05 — The Agent Loop pattern
=====================================
Give the LLM tools and spin it in a loop — it makes a plan ITSELF and executes it.
Definition of an agent: "an LLM runs tools in a loop until it reaches the goal".
Here the tools keep a todo list and mark things done. We do NOT dictate the plan.

MODEL — the PROVIDER switch below: local qwen2.5 by default (🆓 free, offline),
or the cloud gemini. The weak llama3.2 gets lost in the loop — use qwen2.5.

💡 Where useful: a research assistant, a coding agent.

Run:  uv run 01-pure_python/05_agent_loop.py
"""
# endregion

import os
import sys
import json
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


# ⬇️ ЯЗЫК примера: "ru" (русский) | "en" (English) — на нём будут цель и ответ агента
# ⬇️ Example LANGUAGE: "ru" (Russian) | "en" (English) — the goal and the agent's answer language
LANG = "ru"

# RU: инструкция агенту + языковое правило (иначе слабая модель мешает языки)
# EN: the agent's instruction + a language rule (otherwise a weak model mixes languages)
SYSTEM = {
    "ru": ("Ты — агент. Сначала составь план через create_todos, затем выполняй шаги по очереди, "
           "отмечая каждый через mark_complete, и описывай результат шага в тексте. "
           "Когда все шаги выполнены — дай итоговый ответ. Отвечай СТРОГО на русском языке."),
    "en": ("You are an agent. First make a plan via create_todos, then do the steps one by one, "
           "marking each with mark_complete, and describe the result of each step in text. "
           "When all steps are done — give the final answer. Reply STRICTLY in English."),
}[LANG]

# RU: цель на двух языках — выбирается по LANG выше
# EN: the goal in two languages — picked by LANG above
GOAL = {
    "ru": ("Придумай простой контент-план на неделю для Telegram-канала про кофе: "
           "5 идей постов с короткими описаниями."),
    "en": ("Come up with a simple one-week content plan for a Telegram channel about coffee: "
           "5 post ideas with short descriptions."),
}[LANG]


# ── RU: состояние агента — список задач ──
# ── EN: agent state — the task list ──
todos: list[str] = []
done: list[bool] = []


def create_todos(descriptions: list[str]) -> str:
    """
    RU: создать план — список шагов.
    EN: create a plan — a list of steps.
    """
    for d in descriptions:
        todos.append(d)
        done.append(False)
    return render_todos()


def mark_complete(index: int) -> str:
    """
    RU: отметить шаг (нумерация с 1) выполненным.
    EN: mark a step (numbered from 1) as done.
    """
    if 1 <= index <= len(todos):
        done[index - 1] = True
        return render_todos()
    return "Нет шага с таким номером."


def render_todos() -> str:
    if not todos:
        return "Список пуст."
    lines = []
    for i, t in enumerate(todos):
        mark = "✅" if done[i] else "⬜"
        lines.append(f"{i + 1}. {mark} {t}")
    return "\n".join(lines)


# ── RU: описание инструментов для модели (формат OpenAI/Gemini) ──
# ── EN: tool descriptions for the model (OpenAI/Gemini format) ──
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_todos",
            "description": "Создать список шагов (план) из списка описаний.",
            "parameters": {
                "type": "object",
                "properties": {
                    "descriptions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Шаги плана",
                    },
                },
                "required": ["descriptions"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mark_complete",
            "description": "Отметить шаг (номер с 1) выполненным.",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "Номер шага, начиная с 1"},
                },
                "required": ["index"],
            },
        },
    },
]


def run_tool(name: str, arguments: dict) -> str:
    if name == "create_todos":
        return create_todos(**arguments)
    elif name == "mark_complete":
        return mark_complete(**arguments)
    return f"Неизвестный инструмент: {name}"


# ── RU: тот же цикл, что в 04_tools.py ──
# ── EN: the same loop as in 04_tools.py ──

def run_agent(goal: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": goal},
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message

        # RU: печатаем «мысли вслух» агента на этом шаге
        # EN: print the agent's "thinking out loud" on this step
        if msg.content and msg.content.strip():
            print("🤖", msg.content.strip())

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

        for tc in msg.tool_calls:
            arguments = json.loads(tc.function.arguments)
            print(f"   [инструмент] {tc.function.name}({json.dumps(arguments, ensure_ascii=False)})")
            result = run_tool(tc.function.name, arguments)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})


if __name__ == "__main__":
    print("Цель / Goal:", GOAL, "\n")
    final = run_agent(GOAL)
    print("\n=== Итоговый план задач / Final task list ===")
    print(render_todos())
    print("\n=== Финальный ответ агента / Agent's final answer ===")
    print(final)

    # RU: мы не диктовали шаги — агент сам спланировал и выполнил. Это агентность.
    # EN: we didn't dictate the steps — the agent planned and executed itself. That's agency.
