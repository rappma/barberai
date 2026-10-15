# region 🇷🇺 Русский — о файле  (нажми стрелку ▸ слева, чтобы свернуть)
"""
03 — Паттерн «Судья» КАК ГРАФ с циклом (стихия LangGraph)
=========================================================
Поток НЕ линейный: судья забраковал → граф возвращается назад и переделывает.
    START → [генерация] → [проверка] → ХОРОШО → END
                              └─ ПЛОХО → назад в [генерацию]

Запуск:  uv run 04-langgraph/03_judge_graph.py
"""
# endregion

# region 🇬🇧 English — about this file  (click the ▸ arrow to collapse)
"""
03 — The "Judge" pattern AS A GRAPH with a loop (LangGraph's element)
=========================================================
The flow is NOT linear: the judge rejects → the graph goes back and redoes it.
    START → [generate] → [check] → GOOD → END
                            └─ BAD → back to [generate]

Run:  uv run 04-langgraph/03_judge_graph.py
"""
# endregion

import sys
from typing import TypedDict

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

MODEL = "llama3.2"  # RU: бесплатно локально / EN: free, local


def ask(prompt: str, system: str = "Ты — помощник.") -> str:
    try:
        r = ollama.chat(model=MODEL, messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ])
    except Exception as e:
        print(f"\n⚠️  Ollama не отвечает (запущено приложение? есть модель {MODEL}?)\n   {e}\n")
        sys.exit(1)
    return r.message.content


# RU: состояние — всё, что нужно помнить между узлами
# EN: state — everything to remember between nodes
class State(TypedDict):
    question: str    # RU: вопрос пользователя / EN: the user's question
    answer: str      # RU: текущий ответ / EN: the current answer
    feedback: str    # RU: замечание судьи / EN: the judge's feedback
    attempts: int    # RU: сколько попыток сделали / EN: how many attempts made
    accepted: bool   # RU: принял ли судья / EN: did the judge accept


def generate_node(state: State) -> dict:
    """
    RU: узел 1 — генерация ответа (учитывает прошлый фидбек).
    EN: node 1 — generate the answer (takes past feedback into account).
    """
    system = "Ты — консультант. Отвечай конкретно, с практическим шагом."
    if state.get("feedback"):
        system += f"\n\nПрошлый ответ отклонили. Причина: {state['feedback']}\nИсправь это."
    answer = ask(state["question"], system)
    print(f"\n[попытка {state['attempts'] + 1}] ответ: {answer}")
    return {"answer": answer, "attempts": state["attempts"] + 1}


def evaluate_node(state: State) -> dict:
    """
    RU: узел 2 — проверка судьёй (первая строка вердикта — ДА/НЕТ).
    EN: node 2 — check by the judge (first line of the verdict is YES/NO).
    """
    system = "Ты — строгий контролёр. Ответ приемлем, только если он по делу и с конкретным шагом."
    verdict = ask(
        f"Вопрос: {state['question']}\nОтвет: {state['answer']}\n\n"
        "Первой строкой напиши строго ДА или НЕТ. Со второй строки — почему.",
        system,
    )
    first_line = verdict.strip().splitlines()[0].upper()
    accepted = first_line.startswith("ДА") or first_line.startswith("YES")
    print(f"   судья: {'✅ принял' if accepted else '❌ отклонил'}")
    return {"accepted": accepted, "feedback": verdict.strip()}


def decide(state: State) -> str:
    """
    RU: развилка — принято или 3 попытки → конец; иначе на переделку.
    EN: fork — accepted or 3 attempts → end; otherwise redo.
    """
    if state["accepted"]:
        return "готово"
    if state["attempts"] >= 3:
        return "готово"
    return "ещё"


# RU: сборка графа
# EN: building the graph
builder = StateGraph(State)
builder.add_node("генерация", generate_node)
builder.add_node("проверка", evaluate_node)

builder.add_edge(START, "генерация")
builder.add_edge("генерация", "проверка")

# RU: условное ребро — «ещё» → назад в генерацию (ЦИКЛ), «готово» → END
# EN: conditional edge — "again" → back to generate (LOOP), "done" → END
builder.add_conditional_edges("проверка", decide, {
    "ещё": "генерация",
    "готово": END,
})

graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke({
        "question": "С чего начать вести личный бюджет?",
        "answer": "",
        "feedback": "",
        "attempts": 0,
        "accepted": False,
    })
    print("\n=== ИТОГ ===\n", result["answer"])
