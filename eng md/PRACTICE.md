# 🎓 Practice: build your own AI consultant agent

> 📖 View it nicely: `Cmd+Shift+V` (Windows: `Ctrl+Shift+V`).

Your task — **with Claude's help** — build an AI consultant bot for **your own niche**
(a coffee shop, a salon, a store, a tutor — anything). You choose the topic yourself —
that way everyone ends up with their own project.

This isn't "rewrite the example", it's "come up with and build your own". You can
write the code via Claude — the main thing is that you understand **what** came out
and **from which bricks**.

---

## What your bot should be able to do (features)

| Feature | Which pattern it trains |
|---|---|
| Answers questions from your niche's "knowledge base" | basics (context) |
| Understands the question type and behaves differently (price / booking / general) | **Router** |
| Can do at least 1 real action (record a request / send a notification / calculate a price) | **Tool Calling** |
| Remembers the conversation | **Memory** |
| Checks its own answer before sending (for the top students) | **Judge** |
| A web chat you can talk to | **Gradio** |

> **A "knowledge base"** is just facts about your niche (menu, prices, services, rules)
> that you give the bot in the system prompt or in a text file. No complex database
> is needed.

---

## Three difficulty levels (pick yours)

- 🟢 **Basic:** the bot answers from the niche + **1 tool** + **Gradio**. Bare code.
- 🟡 **Intermediate:** everything from basic + **Router** + **Memory**.
- 🔴 **Advanced:** everything from intermediate + **Judge**, and build it on **two approaches**
  (bare code vs a framework) → compare what was simpler and why.

Start with basic — you can then extend it to intermediate and advanced.

---

## Where to start (how to ask Claude)

1. Decide on a niche and write out 5–10 facts about it (this will be the "knowledge base").
2. Decide which difficulty level you're taking.
3. Ask Claude to build the bot. You can take this **prompt template** and fill it in:

> "Build an AI consultant for **[my niche]**. It should:
> – answer questions from these facts: **[insert your facts]**;
> – distinguish the question type (**price / booking / general**) and behave differently;
> – be able to do one real action: **[for example, record a request and send me
>   a notification]**;
> – remember the conversation;
> – work as a web chat via Gradio.
> Build it on **[bare code / a framework]**. After building, briefly explain which
> patterns you applied and where."

4. Run it, check it, fix it with a prompt if something's off.

---

## What to submit at the end (the report)

Put together a short report (text + screenshot/video). In it:

1. **The niche and exact functionality** — 3–5 sentences + a list of features: what the bot can do.
2. **Which patterns are used and WHERE** — specifically, for example:
   - *Router* — I split questions into price / booking / general;
   - *Tool Calling* — the `record_request` tool;
   - *Memory* — I remember the client's name and history;
   - *Judge* — I check the answer's politeness before sending.
3. **Which approach/framework you built it on and why** — bare code / OpenAI SDK /
   CrewAI / LangGraph. Explain the choice (was bare code enough? why take a framework?).
4. **A demo** — a screenshot or a short video of the working chat.
5. **The prompt you used to ask Claude** — attach it (this is part of the skill — task framing).
6. **(Bonus)** deploy it to Railway/Render and give a link (see `DEPLOY.md`).

---

## Niche ideas (if you don't have one yet)

- ☕ **Café / coffee shop** — menu, opening hours, table reservation, owner notification.
- 💈 **Barbershop / salon** — services, prices, booking a time.
- 🛒 **Online store** — a product consultant, selection, collecting a request/lead.
- 📚 **Tutor / online school** — explains a topic and **checks the student's answers**
  (fits *Judge* perfectly).
- 🏋️ **Fitness trainer / nutritionist** — answers about programs, counts calories,
  books a consultation.
- ✈️ **Travel agency** — selecting a tour by parameters, price calculation, a request.
- 🐶 **Pet store / grooming** — products/services, booking, reminders.

---

## Readiness checklist

- [ ] The bot answers from my niche (not in "general terms").
- [ ] There's at least 1 real tool (an action).
- [ ] It works as a web chat (Gradio).
- [ ] *(intermediate+)* Distinguishes question types (Router).
- [ ] *(intermediate+)* Remembers the conversation (Memory).
- [ ] *(advanced)* Checks its own answer (Judge) and compared two approaches.
- [ ] The report on the 6 points above is ready.

Good luck! This is the first bot that is entirely **yours** — conceived and built by you.
