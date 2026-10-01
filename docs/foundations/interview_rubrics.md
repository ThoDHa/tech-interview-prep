# How You Are Scored

Every coding interview ends the same way: the interviewer fills out a scorecard, and your performance is reduced to a few rows of ratings. Knowing those rows turns vague advice ("communicate well") into a checklist you can train deliberately. This page is the four dimensions interviewers actually score, the signals they look for at each level, the bands those signals map to, and the part of this guide that trains each one.

## The four dimensions

### Communication

Can you turn a half-specified problem into a shared plan, out loud?

**Basic signals:** asks clarifying questions before coding; explains the approach and its tradeoffs; keeps narrating while coding; stays organized and succinct.

**Advanced signals:** adjusts fluently when the interviewer steers; summarizes decisions so the interviewer can follow the final code without narration.

**Trained by:** [The Coding Interview, Phase by Phase](interview_practices.md), which is organized around exactly these behaviors, and [step 1 of the method](how_to_approach.md#1-understand-the-problem-exactly), restating the problem before touching it.

### Problem solving

Can you get from a blank page to a good approach, without being dragged?

**Basic signals:** understands the problem quickly via good questions; works systematically instead of guessing; reaches an optimized solution; states the correct complexity; needs no major hints.

**Advanced signals:** produces multiple solutions and compares them; analyzes tradeoffs and lands on a conclusion; extends the solution when the interviewer adds a follow-up.

**Trained by:** [How to Approach a Problem](how_to_approach.md), whose seven steps *are* the systematic approach; the [pattern recognition table](how_to_approach.md#pattern-recognition-signals), which is how the optimized approach gets found; and [Optimizing a Working Solution](optimizing.md), which names the complexity floor and the moves past the first working idea.

### Technical competency

Can you turn the agreed approach into code that actually runs?

**Basic signals:** working code with few bugs; clean, readable implementation; sensible abstractions; neat style.

**Advanced signals:** compares implementation approaches (not just algorithm approaches); strong command of the language's constructs.

**Trained by:** [step 7 of the method](how_to_approach.md#7-code-it-then-test-the-edges), and above all the [`practice/`](https://github.com/ThoDHa/tech-interview-prep/blob/main/practice/README.md) workspace: writing and running real code for every problem is what turns "looks right" into "is right". The pattern guides' solution write-ups model the clean version you are aiming at.

### Testing

Can you find your own bugs before they find you?

**Basic signals:** tests typical cases; tests corner cases; catches and fixes own bugs.

**Advanced signals:** verifies systematically, stepping through the code like a debugger instead of eyeballing it.

**Trained by:** [step 7 of the method](how_to_approach.md#7-code-it-then-test-the-edges) for the corner-case list, the phase-by-phase guide's [verify and test phase](interview_practices.md#5-verify-and-test) for doing it out loud, and the practice harness's `full` marker, which is a ready-made corner-case gauntlet for every problem.

## The bands

Interviewers score each dimension (often on a 1-4 scale) and the hiring loop compresses the result into one of four bands:

| Band | What it means |
|------|---------------|
| Strong hire | Signals across the board; the interviewer would argue for you in the debrief |
| Hire | Positive on the whole; would support an offer |
| No hire | Too many missing signals to risk an offer |
| Strong no hire | Actively negative signals; the interviewer would argue against you |

Some companies insert an indecision or "lean" band between hire and no hire; phone screens in particular often pass on a leaning-hire rather than a confident one.

## How the scores are used

- A **phone screen** exists to filter: a leaning-hire advances you to the
  full loop, anything lower ends the process there.
- In a **full loop**, every round is collected before the decision, so one
  rough round rarely sinks you alone; the debrief weighs the whole set.
- **Mixed results** go to a hiring-committee discussion, where the whole set
  of rounds is weighed rather than any single one.
- **Unclear signals** can trigger a follow-up round rather than an instant
  rejection.
- Interviewers can often see feedback from your **previous rounds**, so a
  re-interview is scored partly on growth. Visible improvement between attempts is itself a signal.

## Why the rubric is good news

Every row is trainable. Nothing above requires talent: asking two clarifying questions, narrating while you code, testing before you say done, restating complexity. The [study path](index.md) and the six phases of [the phase-by-phase guide](interview_practices.md) exercise each dimension deliberately; treat every practice problem as a rep for all four rows.

---

*The four evaluation dimensions, their basic signals, the advanced signal lists for problem solving and technical competency, the hire bands, and the scoring process follow the Tech Interview Handbook's [Coding Interview Rubrics](https://www.techinterviewhandbook.org/coding-interview-rubrics/); the advanced signals for communication and testing are this project's inference from the same source, and the mapping to this guide's material is its own.*
