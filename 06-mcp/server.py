# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
server.py — МИНИМАЛЬНЫЙ MCP-СЕРВЕР (твой набор инструментов для ИИ)
===================================================================
Запускаешь один раз — и любой MCP-клиент (Claude Desktop, Claude Code, IDE)
видит эти инструменты. Тут два: 🌤️ get_weather и ➕ add_numbers.

Запуск (проверить, что стартует):  uv run 06-mcp/server.py
Подключение к Claude Desktop — см. README.md в этой папке.
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
server.py — A MINIMAL MCP SERVER (your set of tools for the AI)
===================================================================
Run it once — and any MCP client (Claude Desktop, Claude Code, IDE) sees these
tools. There are two: 🌤️ get_weather and ➕ add_numbers.

Run (to check it starts):  uv run 06-mcp/server.py
Connecting to Claude Desktop — see README.md in this folder.
"""
# endregion

import sys
import urllib.parse
import urllib.request

# RU: предохранитель — нужен пакет mcp
# EN: guard — the mcp package is needed
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("\n⚠️  Нет библиотеки mcp. Установи её:  uv pip install mcp\n")
    sys.exit(1)


# RU: сервер с именем (его увидит клиент в списке)
# EN: the server with a name (the client will see it in the list)
mcp = FastMCP("foundations-tools")


# RU: @mcp.tool() превращает функцию в инструмент MCP; докстринг — описание для ИИ
# EN: @mcp.tool() turns a function into an MCP tool; the docstring is the AI's description

@mcp.tool()
def get_weather(city: str) -> str:
    """Узнать текущую погоду в указанном городе. На вход — название города."""
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=3&lang=ru"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.read().decode("utf-8").strip()
    except Exception as error:
        return f"Не удалось узнать погоду: {error}"


@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Сложить два числа и вернуть сумму."""
    return a + b


if __name__ == "__main__":
    # RU: поднимает сервер и ждёт подключения клиента (общение через stdio)
    # EN: brings up the server and waits for a client (communication over stdio)
    mcp.run()
