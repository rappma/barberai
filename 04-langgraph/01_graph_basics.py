# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
01 — Механика графа на LangGraph (узлы, рёбра, состояние)
=========================================================
Простейший граф из двух шагов:
    START → [написать] → [улучшить] → END
Идея LangGraph: собираешь СХЕМУ из узлов (шагов) и рёбер (переходов), между
ними течёт общее состояние (State).

Запуск:  uv run 04-langgraph/01_graph_basics.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
01 — Graph mechanics in LangGraph (nodes, edges, state)
=========================================================
The simplest two-step graph:
    START → [write] → [improve] → END
LangGraph's idea: you assemble a DIAGRAM from nodes (steps) and edges
(transitions), with a shared state (State) flowing between them.

Run:  uv run 04-langgraph/01_graph_basics.py
"""
# endregion

import sys
from typing import TypedDict

# RU: предохранители — нужны langgraph и ollama
# EN: guards — langgraph and ollama are needed
try:
    from langgraph.graph import StateGraph, START, END
except ImportError:
    print("\n⚠️  Нет LangGraph. Установи:  uv pip install langgraph\n")
    sys.exit(1)
try:
    import ollama
except ImportError:
    print("\n⚠️  Нет ollama. Установи:  uv pip install ollama\n")
    sys.exit(1)


MODEL = "llama3.2"  # RU: бесплатно, локально / EN: free, local


def ask(prompt: str) -> str:
    """
    RU: спросить локальную модель и вернуть текст.
    EN: ask the local model and return the text.
    """
    try:
        r = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    except Exception as e:
        print(f"\n⚠️  Ollama не отвечает (запущено приложение? есть модель {MODEL}?)\n   {e}\n")
        sys.exit(1)
    return r.message.content


# RU: 1. Состояние — «общая память», которую видят и меняют все узлы
# EN: 1. State — the "shared memory" all nodes see and change
class State(TypedDict):
    text: str


# RU: 2. Узлы — функции-шаги: получают состояние, возвращают изменения (словарь)
# EN: 2. Nodes — step functions: receive the state, return changes (a dict)

def write_node(state: State) -> dict:
    """
    RU: шаг 1 — написать короткий пост (тема лежит в state).
    EN: step 1 — write a short post (the topic is in state).
    """
    result = ask(f"Напиши очень короткий пост на тему: {state['text']}")
    return {"text": result}


def improve_node(state: State) -> dict:
    """
    RU: шаг 2 — улучшить результат предыдущего узла.
    EN: step 2 — improve the result of the previous node.
    """
    result = ask(f"Сделай этот текст живее, в одно предложение:\n\n{state['text']}")
    return {"text": result}


# RU: 3. Сборка графа: узлы + рёбра
# EN: 3. Building the graph: nodes + edges
builder = StateGraph(State)
builder.add_node("написать", write_node)
builder.add_node("улучшить", improve_node)

builder.add_edge(START, "написать")
builder.add_edge("написать", "улучшить")
builder.add_edge("улучшить", END)

graph = builder.compile()


if __name__ == "__main__":
    # RU: invoke запускает граф с начальным состоянием
    # EN: invoke runs the graph with the initial state
    result = graph.invoke({"text": "польза утренней пробежки"})
    print("Результат:\n", result["text"])
