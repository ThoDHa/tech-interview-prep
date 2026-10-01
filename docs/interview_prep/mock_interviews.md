# Mock Interviews

Solving a problem and being interviewed while solving it are different skills. A mock is a rehearsal of the second one, and it is the highest-leverage thing you can do in the last stretch of your preparation: it exposes the gaps that solo practice cannot show, while there is still time to close them.

## Why mocks matter

Your first real interview should not be the first time someone watches you code. Mocks reliably surface failure modes that never appear in solo practice:

- Going silent while you think, leaving the interviewer with no signal to
  score.
- Fixating on one approach because it was the first one you said out loud.
- Forgetting to test, or coding for ten minutes without confirming the
  problem.
- Time-blindness: spending twenty minutes on what felt like five.

Every one of these is cheap to fix once you have seen yourself do it, and nearly invisible from the inside.

## When to start

About 60% of the way through the plan: week 5 in the [8-week schedule](study_plan.md). Earlier than that and you have not seen enough patterns for a mock to say anything useful; later and you cannot act on what it reveals. From week 5, aim for one mock every one to two weeks until the real loop.

## The platform landscape

| Option | What it is | Cost |
|--------|------------|------|
| Peer-mock platforms | You interview a stranger for half the session, they interview you for the other half; matching is automatic | Free |
| Professional platforms | Anonymous mock interviews with real engineers, commonly with a recording you can watch afterward (for example [interviewing.io](https://interviewing.io)) | Paid per session |
| A friend or colleague | Someone who plays the interviewer seriously, ideally another person who is also preparing | Free |

Peer mocks give you volume and also make you a better interviewer, and interviewing others sharpens the judgment you use in your own rounds. Professional mocks give you the most realistic signal, since the other side interviews for a living. A serious friend sits in between. Any of them beats none.

## Run a mock with a peer, using this repo

This repository is built for this. The `main` branch is spoiler-free by design, which makes problem selection easy:

1. **The interviewer picks a problem the candidate has not seen** from the
   [problem list](../index.md), roughly at the candidate's current level: problems from week 4 to 5 of the schedule are a good mid-plan target.
2. **The interviewer prepares from the published site** (or the `solutions`
   branch), so they know the expected approaches and can judge the ladder rather than just the final answer.
3. **Budget it like a real round:** five minutes of introductions, 30 to 40
   minutes on the problem (use the problem's Time column as the target), five to ten minutes for the candidate's questions.
4. **The candidate works in the [`practice/`](https://github.com/ThoDHa/tech-interview-prep/tree/main/practice)
   workspace** and narrates throughout. `-m simple` after the first working pass is the "Run" button; `-m full` before declaring done is "Submit".
5. **Debrief for ten minutes** while it is fresh (below).

## Run one alone

A solo mock cannot grade your communication the way a partner can, but it still trains narration and the clock:

1. Pick an unsolved problem, set a timer for its Time column, and have it
   visible where you can see it burning down.
2. Narrate out loud for the whole session, even with nobody there. If it
   feels absurd, that is the point: the real interview will not feel absurd.
3. Record yourself (audio is enough) and listen for silences longer than a
   few seconds.
4. Use `-m simple` as Run and `-m full` as Submit, and no peeking at the
   pattern guide until you have declared an approach out loud.
5. Afterwards, read the solution ladder and note what a partner would have
   flagged.

## How to debrief

Within a day of any mock, answer four questions in writing:

1. **Where did the time go?** Understanding the problem, choosing an
   approach, coding, debugging: which one ate the budget?
2. **Did you narrate?** Could the interviewer have followed your thinking?
3. **Did you test your own code?** Corner cases traced by hand before claiming
   done?
4. **Did you reach working code?** If not, at which step did it go wrong?

Then pick exactly one thing to fix in the next mock. Fixing one failure mode per mock works; trying to fix all four at once changes nothing. If the mock used a repo problem, re-rate it honestly in the practice tracker (`progress.py rate`); a struggled rating puts it back in the `due` queue, which is where you want it.

---

*This page adapts the mock-interview timing advice (start near 60% of the plan) and platform guidance from the Tech Interview Handbook's [Coding Interview Prep Guide](https://www.techinterviewhandbook.org/coding-interview-prep/) and [Coding Interview Study Plan](https://www.techinterviewhandbook.org/coding-interview-study-plan/). The peer and solo workflows built on this repository's practice workspace, and the debrief protocol, are original to this project.*
