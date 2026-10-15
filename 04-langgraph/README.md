# 04-langgraph — агент как ГРАФ (LangGraph)

> 🇬🇧 English version below ⬇️

Ещё один фреймворк для агентов. Метафора LangGraph — **граф / блок-схема**:
ты рисуешь логику агента из УЗЛОВ (шаги) и РЁБЕР (переходы), а между ними течёт
общее СОСТОЯНИЕ (State). Главная сила — **точный контроль над потоком**: циклы,
развилки, условия, возвраты назад.

## Где LangGraph сильнее других

```
больше контроля ◄─────────────────────────► больше готового
  LangGraph        OpenAI SDK       CrewAI
  (граф/схема)     (агенты+tools)   (команда ролей)
```

LangGraph удобен, когда поток НЕ линейный: «сделал → проверил → если плохо,
вернись и переделай». Это видно в `03_judge_graph.py` — там настоящий цикл.

## Файлы

| Файл | Что показывает |
|---|---|
| `01_graph_basics.py` | механика графа: State, узлы, рёбра, START/END |
| `03_judge_graph.py` | паттерн «Судья» как граф с ЦИКЛОМ (генерация → проверка → назад) |

## Установка и запуск

> 📁 `~/Downloads/foundations-practice` ниже — это ПРИМЕР пути. У тебя папка
> проекта может лежать в другом месте и называться иначе. Замени путь на свой:
> проще всего написать в терминале `cd ` (с пробелом) и перетащить туда папку
> проекта мышкой из Finder — путь подставится сам.

```bash
cd ~/Downloads/foundations-practice   # ← впиши СВОЙ путь к папке проекта
uv pip install langgraph ollama       # фреймворк + бесплатный движок
uv run 04-langgraph/01_graph_basics.py
```

По умолчанию примеры идут через **бесплатный локальный Ollama** (нужно
установленное приложение Ollama и модель: `ollama pull llama3.2`). Как
переключить на платный провайдер — написано в комментариях внутри файлов.

## Главная мысль

LangGraph — это «колонка фреймворков», как OpenAI SDK и CrewAI, только с упором
на **рисование потока графом**. Писать его руками не обязательно — важно знать,
что под сложные управляемые сценарии он удобен.

---
---

# 🇬🇧 English

# 04-langgraph — an agent as a GRAPH (LangGraph)

Another framework for agents. LangGraph's metaphor is a **graph / flowchart**:
you draw the agent's logic out of NODES (steps) and EDGES (transitions), and a
shared STATE flows between them. Its main strength — **precise control over the
flow**: loops, forks, conditions, going back.

## Where LangGraph is stronger than the others

```
more control ◄─────────────────────────► more ready-made
  LangGraph        OpenAI SDK       CrewAI
  (graph/diagram)  (agents+tools)   (team of roles)
```

LangGraph is handy when the flow is NOT linear: "did → checked → if bad, go back
and redo". You can see this in `03_judge_graph.py` — there's a real loop there.

## Files

| File | What it shows |
|---|---|
| `01_graph_basics.py` | graph mechanics: State, nodes, edges, START/END |
| `03_judge_graph.py` | the "Judge" pattern as a graph with a LOOP (generate → check → back) |

## Install and run

> 📁 `~/Downloads/foundations-practice` below is an EXAMPLE path. Your project
> folder might be somewhere else and named differently. Replace it with your
> own: easiest way — type `cd ` (with a trailing space) in the terminal, then
> drag the project folder from Finder right into the terminal window — the
> path fills in by itself.

```bash
cd ~/Downloads/foundations-practice   # ← put YOUR path to the project folder here
uv pip install langgraph ollama       # the framework + the free engine
uv run 04-langgraph/01_graph_basics.py
```

By default the examples go through the **free local Ollama** (you need the Ollama
app installed and a model: `ollama pull llama3.2`). How to switch to a paid
provider is described in the comments inside the files.

## The main idea

LangGraph is the same "framework column" as the OpenAI SDK and CrewAI, just with
an emphasis on **drawing the flow as a graph**. You don't have to write it by hand —
it's important to know it's handy for complex, controlled scenarios.
