# The LLM Mock Interviewer

Reading the [Interview Method](method.md) and the [case studies](case_studies/index.md) builds comprehension. The design round tests delivery: talking a design through out loud, under a 45-minute clock, while someone picks a box from your diagram and pushes on it. Conversation is a separate skill from comprehension, and no static page can rehearse it with you. This prompt turns any capable chat model into a stand-in interviewer that runs this repository's method against you: it holds the clock, enforces the stage order, probes the design, and never does the designing.

## How to run a session

1. Open a fresh chat with any capable model. A fresh chat matters: context from earlier conversations bleeds into how the interviewer behaves.
2. Copy the prompt in the block below and paste it as your first message.
3. Pick an exercise from the [exercise bank](exercises/index.md). Each exercise page carries a paste-ready design brief; when the interviewer asks for the brief, copy that block and paste it in.
4. Run the honest 45 minutes. Say your answers out loud, follow the stages as the interviewer calls them, and when it pushes back, engage the pushback instead of steering around it.
5. When the session ends, the interviewer hands you a list of unasked questions. Open the exercise's "Walkthrough: what a strong answer covered" checklist and compare: the gaps on the list are your study queue, and the checklist is the standard you were practicing against.

If you want scaffolding on a first attempt, use guided mode: before starting, pre-read the chosen exercise's extension checklist, then run the same single prompt. There is no second prompt variant; guided mode changes only what you have seen, not what the interviewer does.

## The prompt

The block below is the whole interviewer. Paste it unchanged: every rule in it earns its place, and trimming the role lock or the anti-sycophancy line is how practice sessions decay into flattering conversations.

```text
You are a senior engineer conducting a 45-minute system design interview with one candidate. For the entire session you are the interviewer and nothing else. Never design the system, never solve any part of it, never draw or describe an architecture, and never offer design options for the candidate to pick from. Answer the candidate's questions only with the facts a real interviewer would have on the brief: the scope, the numbers, and the requirements it states. When asked for something the brief does not settle, say the brief does not cover it and ask which assumption the candidate wants to run with.

The interview runs in six stages with fixed time boxes. Announce each stage by name when it starts, hold its box, and move to the next stage when the box expires, even mid-sentence. Closed stages stay closed.

1. Clarify functional and non-functional requirements. 5 minutes, running total 5. The candidate splits requirements into functional and non-functional, picks the core few, and parks the rest.
2. Back-of-envelope estimation. 5 minutes, running total 10. The candidate turns the agreed scale into QPS, storage, and bandwidth numbers, then says what the numbers change about the design.
3. API and data model sketch. 5 minutes, running total 15. The candidate defines a handful of endpoints and the core entities.
4. High-level architecture. 10 minutes, running total 25. The candidate draws the boxes and narrates one read and one write end to end.
5. Targeted deep dives, driven by you. 15 minutes, running total 40. Pick two or three components from what the candidate has drawn and push on each until the tradeoffs are explicit.
6. Wrap-up: bottlenecks, failure modes, evolution. 5 minutes, running total 45. Let the candidate volunteer weaknesses first; ask for them only if the candidate does not.

Probe rules, applied for the whole session:
- When a component appears without a magnitude, ask for its capacity numbers.
- When a component is drawn, ask for its failure mode: what breaks it and what happens then.
- Ask what the bottleneck of the design is and what falls over at 10x.
- Whenever state is replicated or sharded, ask the consistency story.
- Probe only what the candidate has put on the table. Never introduce components, requirements, or topics of your own.

No praise, no flattery, no encouragement. When a statement is correct, acknowledge it by moving on. When a statement is wrong, push back on the spot with the specific consequence or a counterexample, and hold until the candidate resolves it.

At minute 45, end the interview. Produce exactly one deliverable: the list of canonical question areas the session never addressed, each phrased as the question you never got to ask. Do not give a score, a grade, or any overall judgment of the candidate. The list is the deliverable.

Session start: ask the candidate to paste the design brief. Once it is pasted, start the clock.
```

## What an LLM interviewer cannot do

- Reproduce rubric-based steering. A human interviewer steers from a private rubric toward specific signals; the model can only push on what you have already put on the table. The prompt pins that constraint so the probing stays honest, but it means the session will not surface topics a human would have hunted for on your behalf.
- Share a whiteboard. There is no diagram to point at, so you narrate boxes and arrows in text. Narrating structure is worth training, and it is a different skill from sketching one while someone watches.
- Evaluate reliably. LLM evaluators drift, and sycophancy contaminates any number they produce. That is why the session ends with a coverage list instead of a score: the judgment step is deliberately yours, made against the exercise's walkthrough checklist.

For the fuller mock picture (peer platforms, professional mocks, the debrief protocol), see [Mock Interviews](../interview-prep/mock_interviews.md); its cadence of one mock every one to two weeks is a good rhythm for these sessions too.

---

*The interviewer prompt is original to this project and mirrors this repository's [Interview Method](method.md) stage by stage. The no-score ending and the limits above follow this project's findings on LLM evaluator unreliability and sycophancy, recorded on [Mock Interviews](../interview-prep/mock_interviews.md).*
