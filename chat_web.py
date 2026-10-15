# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
chat_web.py — живой чат в браузере через Gradio
===============================================
Превращает бота в настоящее окно чата (как ChatGPT). По умолчанию — бесплатный
локальный Ollama. Подробности — в GRADIO.md.

Запуск:  uv run chat_web.py  → открой адрес из терминала (http://127.0.0.1:7860)
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
chat_web.py — a live chat in the browser via Gradio
===============================================
Turns a bot into a real chat window (like ChatGPT). By default — the free local
Ollama. Details — in GRADIO.md.

Run:  uv run chat_web.py  → open the address from the terminal (http://127.0.0.1:7860)
"""
# endregion

import sys

# RU: предохранители — нужны gradio и ollama
# EN: guards — gradio and ollama are needed
try:
    import gradio as gr
except ImportError:
    print("\n⚠️  Нет Gradio. Установи:  uv pip install gradio\n")
    sys.exit(1)
try:
    import ollama
except ImportError:
    print("\n⚠️  Нет ollama. Установи:  uv pip install ollama\n")
    sys.exit(1)


MODEL = "llama3.2"  # RU: бесплатно, локально / EN: free, local


def to_plain_text(content) -> str:
    """
    RU: Gradio 6 отдаёт content не строкой, а списком блоков вида
        [{"type": "text", "text": "..."}] (чтобы поддерживать картинки/файлы).
        Ollama же ждёт обычную строку — эта функция достаёт текст из блоков.
    EN: Gradio 6 gives content not as a string but as a list of blocks like
        [{"type": "text", "text": "..."}] (to support images/files). Ollama
        expects a plain string — this function pulls the text out of the blocks.
    """
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if block.get("type") == "text")
    return content


def chat(message, history):
    """
    RU: Gradio вызывает эту функцию на каждое сообщение пользователя.
    EN: Gradio calls this function on every user message.
    """
    # RU: история + новое сообщение → бот помнит контекст разговора
    # EN: history + new message → the bot remembers the conversation context
    # RU: просим зеркалить язык вопроса ЯВНО (мягкой фразы слабой модели не хватает)
    # EN: we ask to mirror the question's language FIRMLY (a soft line isn't enough for a weak model)
    system_prompt = (
        "Ты — дружелюбный помощник. ВАЖНОЕ ПРАВИЛО: всегда отвечай СТРОГО на языке "
        "последнего сообщения пользователя (английский вопрос — английский ответ, "
        "русский — русский). Никогда не переключайся на другой язык сам."
    )
    messages = [{"role": "system", "content": system_prompt}]
    # RU: приводим историю к простым строкам (см. to_plain_text выше)
    # EN: normalize the history to plain strings (see to_plain_text above)
    messages += [{"role": m["role"], "content": to_plain_text(m["content"])} for m in history]
    messages += [{"role": "user", "content": message}]

    try:
        response = ollama.chat(model=MODEL, messages=messages)
    except Exception as error:
        return f"⚠️ Ollama не отвечает. Запущено ли приложение и есть ли модель {MODEL}?\n{error}"
    return response.message.content


if __name__ == "__main__":
    # RU: ChatInterface рисует окно чата; launch() открывает его в браузере
    # EN: ChatInterface draws the chat window; launch() opens it in the browser
    # RU: временная публичная ссылка для друга — launch(share=True)
    # EN: a temporary public link for a friend — launch(share=True)
    # RU: type="messages" тут не нужен — в Gradio 6+ это единственный формат по умолчанию
    # EN: no type="messages" needed here — in Gradio 6+ it's the only, default format
    gr.ChatInterface(chat, title="Мой первый AI-чат  /  My first AI chat").launch()
