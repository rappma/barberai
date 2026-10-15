# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
03 — Паттерн LLM-as-a-Judge (Судья)
===================================
Один ИИ генерирует ответ, второй (судья) оценивает. Забраковал — генератор
переделывает с учётом замечания, и так по кругу, пока не примут.

💡 Где пригодится: проверка ответа бота ПЕРЕД отправкой клиенту, модерация,
   контроль тона бренда — везде, где цена ошибки высока.

Запуск:  uv run 01-pure_python/03_judge.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
03 — The LLM-as-a-Judge pattern
===================================
One AI generates an answer, a second (the judge) evaluates it. If rejected, the
generator redoes it with the feedback, and so on in a loop until it's accepted.

💡 Where useful: checking a bot's answer BEFORE sending it to a customer,
   moderation, brand-tone control — anywhere the cost of a mistake is high.

Run:  uv run 01-pure_python/03_judge.py
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


def generate(question: str, feedback: str | None = None) -> str:
    """
    RU: генератор: отвечает на вопрос, учитывая фидбек судьи (если был).
    EN: generator: answers the question, taking the judge's feedback into account (if any).
    """
    system = "Ты — консультант. Отвечай полезно и конкретно."
    if feedback:
        system += f"\n\nТвой прошлый ответ отклонили. Причина: {feedback}\nИсправь это."
    return ask(question, system=system)


def evaluate(question: str, answer: str) -> tuple[bool, str]:
    """
    RU: судья: возвращает (принято?, замечание). Первая строка вердикта — ДА/НЕТ.
    EN: judge: returns (accepted?, feedback). The first line of the verdict is YES/NO.
    """
    system = (
        "Ты — строгий контролёр качества. Ответ приемлем, ТОЛЬКО если он прямо "
        "отвечает на вопрос и содержит конкретный практический шаг."
    )
    prompt = (
        f"Вопрос: {question}\n\n"
        f"Ответ агента: {answer}\n\n"
        "Оцени ответ. ПЕРВОЙ строкой напиши строго ДА или НЕТ. "
        "Со второй строки — коротко почему."
    )
    verdict = ask(prompt, system=system)

    # RU: смотрим первую строку вердикта
    # EN: look at the first line of the verdict
    first_line = verdict.strip().splitlines()[0].upper()
    is_ok = first_line.startswith("ДА") or first_line.startswith("YES")
    return is_ok, verdict.strip()


if __name__ == "__main__":
    question = "С чего начать вести личный бюджет?"
    feedback = None

    # RU: максимум 3 попытки
    # EN: at most 3 attempts
    for attempt in range(1, 4):
        print(f"\n--- Попытка {attempt} ---")

        answer = generate(question, feedback)
        print("Ответ генератора:\n", answer)

        is_ok, feedback = evaluate(question, answer)
        if is_ok:
            print("\n✅ Судья ПРИНЯЛ ответ.")
            break
        else:
            print("\n❌ Судья ОТКЛОНИЛ. Замечание:\n", feedback)
    else:
        print("\n⚠️ Попытки кончились — отдаём последний вариант как есть.")

    # RU: генератор + судья + переделка = простейший самопроверяющийся агент
    # EN: generator + judge + redo = the simplest self-checking agent
