# region 🇷🇺 Русский — о движке  (нажми стрелку ▸ слева, чтобы свернуть)
"""
llm.py — УНИВЕРСАЛЬНЫЙ ДВИЖОК (любой ИИ-провайдер в одном месте)
================================================================
Одна функция ask(вопрос) для всех файлов-паттернов. Какая нейросеть отвечает —
решает переключатель PROVIDER ниже.

КАК ВЫБРАТЬ ПРОВАЙДЕРА: поменяй ОДНУ строку (PROVIDER = "...").
  "ollama"   — 🆓 бесплатно, локально, без ключа
  "claude"   — 💰 Anthropic Claude     (ключ ANTHROPIC_API_KEY)
  "openai"   — 💰 ChatGPT / GPT         (ключ OPENAI_API_KEY)
  "gemini"   — 🆓* Google Gemini        (ключ GOOGLE_API_KEY)
  "deepseek" — 💰 DeepSeek (очень дёшево, ключ DEEPSEEK_API_KEY)
  "mistral"  — 💰 Mistral (есть free-лимит, ключ MISTRAL_API_KEY)
  "yandex"   — 💰🇷🇺 YandexGPT  (ключ YANDEX_API_KEY + YANDEX_FOLDER_ID)
Ключи кладутся в файл .env (образец — .env.example).

🆓* Gemini: на момент записи курса у Google есть бесплатный лимит по API.
    Ключ: https://aistudio.google.com/apikey
"""
# endregion

# region 🇬🇧 English — about the engine  (click the ▸ arrow to collapse)
"""
llm.py — THE UNIVERSAL ENGINE (any AI provider in one place)
================================================================
One ask(question) function for all the pattern files. Which network answers is
decided by the PROVIDER switch below.

HOW TO CHOOSE A PROVIDER: change ONE line (PROVIDER = "...").
  "ollama"   — 🆓 free, local, no key
  "claude"   — 💰 Anthropic Claude     (key ANTHROPIC_API_KEY)
  "openai"   — 💰 ChatGPT / GPT         (key OPENAI_API_KEY)
  "gemini"   — 🆓* Google Gemini        (key GOOGLE_API_KEY)
  "deepseek" — 💰 DeepSeek (very cheap, key DEEPSEEK_API_KEY)
  "mistral"  — 💰 Mistral (has a free tier, key MISTRAL_API_KEY)
  "yandex"   — 💰🇷🇺 YandexGPT  (key YANDEX_API_KEY + YANDEX_FOLDER_ID)
Keys go into the .env file (template — .env.example).

🆓* Gemini: at recording time Google offers a free API tier.
    Key: https://aistudio.google.com/apikey
"""
# endregion

import os
import sys
from dotenv import load_dotenv

# RU: подгружаем ключи из .env
# EN: load the keys from .env
load_dotenv()


# RU: ГЛАВНЫЙ ПЕРЕКЛЮЧАТЕЛЬ — меняй здесь
# EN: THE MAIN SWITCH — change it here
PROVIDER = "gemini"   # ollama | claude | openai | gemini | deepseek | mistral | yandex


# RU: какая модель у какого провайдера. Можно менять.
# EN: which model for which provider. You can change these.
MODELS = {
    "ollama":   "llama3.2",              # RU: или "qwen2.5" (лучше для русского) / EN: or "qwen2.5"
    "claude":   "claude-opus-4-8",       # RU: или "claude-haiku-4-5" (дешевле) / EN: or "claude-haiku-4-5" (cheaper)
    "openai":   "gpt-4o-mini",
    "gemini":   "gemini-2.5-flash",
    "deepseek": "deepseek-chat",
    "mistral":  "mistral-small-latest",
    "yandex":   "yandexgpt",             # RU: gpt://<folder>/ добавится сам ниже / EN: gpt://<folder>/ is added below
}


def _stop(message: str) -> None:
    """
    RU: остановить программу с понятным сообщением (а не крашем).
    EN: stop the program with a clear message (not a crash).
    """
    print("\n⚠️  " + message + "\n")
    sys.exit(1)


def ask(prompt: str, system: str = "Ты — помощник. Отвечай по делу и кратко.") -> str:
    """
    RU: задать вопрос текущему провайдеру и вернуть текст ответа.
    EN: ask the current provider and return the answer text.
    """
    model = MODELS.get(PROVIDER)
    if model is None:
        _stop(f"Неизвестный PROVIDER='{PROVIDER}'. Доступны: "
              "ollama, claude, openai, gemini, deepseek, mistral, yandex.")

    # ── RU: бесплатно — локальная Ollama / EN: free — local Ollama ──
    if PROVIDER == "ollama":
        try:
            import ollama
        except ImportError:
            _stop("Нет библиотеки ollama. Установи:  uv pip install ollama")
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as error:
            _stop(
                "Ollama не отвечает. Проверь:\n"
                "   • запущено ли приложение Ollama (значок ламы в меню);\n"
                f"   • скачана ли модель:  ollama pull {model}\n"
                f"   Детали: {error}"
            )
        return response.message.content

    # ── RU: Anthropic Claude / EN: Anthropic Claude ──
    if PROVIDER == "claude":
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key or "..." in key:
            _stop("Нет ключа ANTHROPIC_API_KEY (впиши его в .env). Или поставь PROVIDER='ollama' (бесплатно).")
        try:
            import anthropic
        except ImportError:
            _stop("Нет библиотеки anthropic. Установи:  uv pip install anthropic")
        client = anthropic.Anthropic()
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        # RU: ответ приходит списком блоков — склеиваем текстовые
        # EN: the answer comes as a list of blocks — glue the text ones
        return "".join(b.text for b in response.content if b.type == "text")

    # ── RU: все OpenAI-совместимые: GPT, Gemini, DeepSeek, Mistral, YandexGPT ──
    # ── EN: all OpenAI-compatible: GPT, Gemini, DeepSeek, Mistral, YandexGPT ──
    # RU: отличаются только именем ключа в .env и адресом сервера (None = сервер OpenAI)
    # EN: they differ only in the key name in .env and the server address (None = OpenAI server)
    openai_compatible = {
        "openai":   ("OPENAI_API_KEY",   None),
        "gemini":   ("GOOGLE_API_KEY",   "https://generativelanguage.googleapis.com/v1beta/openai/"),
        "deepseek": ("DEEPSEEK_API_KEY", "https://api.deepseek.com"),
        "mistral":  ("MISTRAL_API_KEY",  "https://api.mistral.ai/v1"),
        "yandex":   ("YANDEX_API_KEY",   "https://llm.api.cloud.yandex.net/v1"),
    }
    if PROVIDER in openai_compatible:
        try:
            from openai import OpenAI
        except ImportError:
            _stop("Нет библиотеки openai. Установи:  uv pip install openai")

        env_name, base_url = openai_compatible[PROVIDER]
        key = os.getenv(env_name)
        if not key or "..." in key:
            _stop(f"Нет ключа {env_name} (впиши его в .env). Или поставь PROVIDER='ollama' (бесплатно).")

        # RU: YandexGPT — в имени модели нужен твой folder_id из Yandex Cloud
        # EN: YandexGPT — the model name needs your folder_id from Yandex Cloud
        if PROVIDER == "yandex":
            folder = os.getenv("YANDEX_FOLDER_ID")
            if not folder or "..." in folder:
                _stop("Нет YANDEX_FOLDER_ID (впиши его в .env). Это ID каталога в Yandex Cloud.")
            model = f"gpt://{folder}/{model}"

        client = OpenAI(api_key=key, base_url=base_url) if base_url else OpenAI(api_key=key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    _stop(f"Неизвестный PROVIDER='{PROVIDER}'.")


# RU: самопроверка: uv run llm.py — спросит у текущего провайдера
# EN: self-test: uv run llm.py — asks the current provider
if __name__ == "__main__":
    print(f"Провайдер / Provider: {PROVIDER}  |  модель / model: {MODELS.get(PROVIDER)}")
    print(ask("Скажи одно дружелюбное предложение, что ты на связи."))
