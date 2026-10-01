# The Coding Interview, Phase by Phase

Knowing how to solve problems (the method in [How to Approach a Problem](how_to_approach.md)) is half of a coding interview. The other half is running the round itself: what you do in the minutes before any code exists, while you write it, and after you think you are done. Interviewers score those minutes deliberately; [How You Are Scored](interview_rubrics.md) shows the rubric they hold. This page is the behavior each row of that rubric asks for, as the six phases every coding round falls into.

## The time budget

For a standard 45-minute round, budget roughly:

| Phase | Time | Running total |
|-------|------|---------------|
| 1. Introduce yourself | 2 min | 2 |
| 2. Clarify the question | 5 min | 7 |
| 3. Discuss the approach and its tradeoffs | 8 min | 15 |
| 4. Code while narrating | 20 min | 35 |
| 5. Verify and test | 7 min | 42 |
| 6. Wrap up | 3 min | 45 |

The budget is a guide, not a law. Its real job is to stop the two classic failures: coding in minute five against a half-understood problem, and reaching minute forty with fifteen lines written and no test run.

## Before the round

- Prepare a self-introduction of about 90 seconds, two minutes at the most,
  and two or three questions to ask at the end; [Behavioral Interviews](../interview_prep/behavioral.md) has the full preparation method for both.
- For a virtual round: quiet room, charged laptop, tested audio, and paper or
  a whiteboard app within reach for drawing.
- For a phone screen: earphones, so both your hands are free to type.

## The six phases

### 1. Introduce yourself

About 90 seconds of background: who you are, what you have built, why you are here.

**Do:** keep it under two minutes, sound like a person who wants to be there, and connect one line of your experience to the role.

**Don't:** eat into the coding time. A ten-minute life story is a worse signal than a mediocre palindrome answer.

### 2. Clarify the question

This is [step 1 and step 2 of the method](how_to_approach.md#1-understand-the-problem-exactly), run as a conversation instead of solo reading.

**Do:**

- Paraphrase the problem back in your own words before anything else.
- Ask at least two or three real questions: How is the input stored? Is it
  sorted? May I modify it? What values appear (negatives, duplicates, empties, how large)?
- Work the provided example, or a smaller one, by hand before proposing
  anything.

**Don't:** start coding on the heels of the prompt, and don't stay silent while thinking. Saying "so for this example I would..." is clarification too.

### 3. Discuss the approach and its tradeoffs

Roughly five to ten minutes of two-way discussion before any code. This is where [steps 3 through 6 of the method](how_to_approach.md#3-write-the-brute-force-first) happen out loud.

**Do:**

- Name more than one approach at a high level, with the tradeoff for each:
  "nested loops are `O(n²)` time and `O(1)` space; a hash map buys `O(n)` time for `O(n)` memory".
- State the time and space complexity of whichever you recommend, and
  [the floor it cannot beat](optimizing.md#find-the-floor-the-best-theoretical-complexity).
- Wait for the interviewer's green light before writing code.

**Don't:** code before the green light, ignore information the interviewer hands you ("the input fits in memory" is a hint, not small talk), or hide uncertainty. "My first instinct is X, though there may be something smarter" scores better than silent doubt.

### 4. Code while narrating

**Do:**

- Keep talking. A running commentary of intent ("here I'm walking the list,
  keeping the running sum") is the behavior the communication score is built from.
- Write real, runnable code, not pseudocode, with descriptive names.
- Build small helpers on a skeleton (the same decomposition as
  [step 3 of the method](how_to_approach.md#3-write-the-brute-force-first)), and ask permission for shortcuts: "assuming a `Counter` is fine to use?"
- Say your corner-cutting out loud: "skipping input validation here; with
  more time I'd check for it."

**Don't:** over-comment, use one-letter names, paste code you have not read, or go quiet for minutes. If the interviewer interjects, it is usually a hint, and hints are gifts.

### 5. Verify and test

The round is not over when the code compiles. This is [step 7 of the method](how_to_approach.md#7-code-it-then-test-the-edges), performed visibly.

**Do:**

- Re-read your own code with fresh eyes before declaring anything; off-by-one
  mistakes live exactly there.
- Walk through one example line by line, tracking the variables like a
  debugger, out loud.
- Propose the corner cases yourself: empty input, a single element, duplicates,
  the largest allowed value, negatives.
- Restate the final time and space complexity, and name what you would
  improve with more time.

**Don't:** announce "done" the moment the last line is written, and don't argue when the interviewer spots a bug. "Good catch" plus a fast fix is the behavior being graded. The `full` marker in the [practice workspace](https://github.com/ThoDHa/tech-interview-prep/blob/main/practice/README.md) runs exactly this kind of corner-case gauntlet on every problem in this guide.

### 6. Wrap up

Three minutes to leave the impression you want.

**Do:** ask the questions you prepared, tailored to the company, and thank the interviewer.

**Don't:** trail off with "I guess that's it", or reopen your solution yet again during the goodbyes. If something is unfinished, say what you would do with another ten minutes: that is a stronger close than a rushed fix.

## After the round

- Write down the questions you were asked while they are fresh; they are the
  best study material you will ever have for the next loop.
- Send a short thank-you note. It is polite, and it keeps the conversation
  alive if the loop is still deciding.

---

*The six phases, the do/don't guidance, and the before/after notes are adapted from the Tech Interview Handbook's [Coding Interview Cheatsheet](https://www.techinterviewhandbook.org/coding-interview-cheatsheet/); the time budget and the cross-links into this project's method are original.*
