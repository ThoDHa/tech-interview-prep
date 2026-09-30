# Interview Prep: Start Here

The rest of this site teaches the material: foundations, the problem bank (the Grind 75 and NeetCode 150 lists in one interleaved study order, plus Amazon OA), and the pattern guides behind them. This section is the plan around the material: how to budget your preparation time, which pace fits the time you have, how to pick and keep an interview language, and what the rounds beyond the coding problem (format, evaluation, behavioral, mocks) actually look like.

If you have never done algorithm interviews before, read this page once, then let the [study plan](study_plan.md) drive the rest.

## The preparation method

Eight steps, in the order you do them. Each maps onto something in this repo.

1. **Pick one language and commit to it.** Use the same language for every
   problem you solve. Switching mid-plan costs more than any language difference ever adds. See [Choosing a Language](language.md).
2. **Budget your time before you start.** Decide how many weeks and how many
   hours per week you can honestly give. The Grind 75 track takes roughly 32 hours at one clean pass per problem; nobody passes everything cleanly, so plan for two to three times that. See [Study Plan and Schedule](study_plan.md).
3. **Learn the prerequisites, then study and practice each topic together.**
   Read the [Foundations](../foundations/index.md) first (about an hour), then for each new topic: read the [pattern guide](../patterns/index.md), solve the problems that use it, and only then move on.
4. **Work the problems in study order.** For each one: read the problem page,
   open its linked pattern guide, attempt it yourself in the [`practice/`](https://github.com/ThoDHa/algo-oa-prep/tree/main/practice) workspace, then compare with the solution ladder, baseline first.
5. **Review what fades.** Rate every solve with the practice tracker
   (`progress.py rate`) and clear the `due` review queue weekly. Spaced repetition is what turns "I did that problem once" into a skill.
6. **Prepare the non-coding rounds.** A 90-second self-introduction, a handful
   of STAR stories, and real questions to ask your interviewer. See [Behavioral Interviews](behavioral.md).
7. **Rehearse under interview conditions.** Mock interviews, starting when you
   are about 60% through the plan. See [Mock Interviews](mock_interviews.md).
8. **Close the process out.** The last 24 hours, the offer conversation, and
   the follow-up: see [Interview Day and Follow-Up](interview_day.md) and
   [Salary Negotiation](salary_negotiation.md).

Steps 1 and 2 take an evening. Steps 3 through 5 are the plan's core; steps 6 and 7 run alongside the last stretch, and step 8 takes over when the loop ends.

## What the interview loop looks like

Formats vary by company and role. Ask your recruiter what the loop looks like before you prepare; it changes what matters. The common shapes:

| Format | How often | What it is like |
|--------|-----------|-----------------|
| Quiz | Occasional | A short live check of fundamentals or knowledge questions, sometimes part of a screen |
| Online assessment | Occasional | An automated, timed test (HackerRank-style) with one to three questions, usually after a resume screen |
| Take-home assignment | Rare (more common at startups) | Build a small project or feature over a day or two, reviewed asynchronously |
| Phone screen | Common | A 30 to 60 minute call with an engineer in a collaborative editor. Usually no execution, no debugger: talk while you write |
| Onsite loop | Almost always for full loops | Three to five rounds over a half day: one or two coding rounds, system design for mid and senior roles, and a behavioral round |

The coding rounds are what the problems and pattern guides train for. The [System Design section](../system_design/index.md) covers the design round, [Behavioral Interviews](behavioral.md) covers the people round, [Interview Day and Follow-Up](interview_day.md) covers the loop itself and its tail, and [Mock Interviews](mock_interviews.md) covers the skill of performing under either kind.

## How you are evaluated

Interviewers score coding rounds on roughly the same four dimensions everywhere:

- **Communication**: you narrate your thinking, confirm the problem, and state
  assumptions before coding.
- **Problem solving**: you move from examples to an approach deliberately, and
  you can say what its time and space cost are.
- **Technical competency**: the code you write is correct, readable, and
  reasonably efficient for the approach you chose.
- **Testing**: you trace your own code, probe corner cases, and fix what you
  find without being told.

The foundations section carries a full [coding interview rubric](../foundations/interview_rubrics.md) that unpacks each dimension into what strong and weak signals look like. Read it once before your first mock, and again before the real loop.

## Where to go next

- New to algorithms: start with the [Foundations](../foundations/index.md),
  then come back and follow the [study plan](study_plan.md).
- Already solving problems: skim the
  [study plan](study_plan.md) to place yourself in it, and put [mock interviews](mock_interviews.md) on the calendar for the 60% mark.
- Minutes before an online assessment or a live round: keep the
  [coding cheatsheet](coding_cheatsheet.md) open for the 30-second checklist, the pattern flash-cards, the warm-up set, and the corner-case shotgun.
- A loop on the calendar: run the [interview day](interview_day.md) checklist the night before, and have the [behavioral question bank](behavioral.md#the-common-questions-bank) ready.
- Holding an offer: [Salary Negotiation](salary_negotiation.md) is an evening's read that pays for the whole search.

---

*This page adapts the preparation method and interview-format overview from the Tech Interview Handbook's [Coding Interview Prep Guide](https://www.techinterviewhandbook.org/coding-interview-prep/) and [Software Engineering Interview Guide](https://www.techinterviewhandbook.org/software-engineering-interview-guide/). The mapping onto this repository's foundations, pattern guides, and practice workspace is original to this project.*
