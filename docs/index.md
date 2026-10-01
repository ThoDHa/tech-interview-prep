# Tech Interview Prep Solutions

A study guide spanning three curated problem banks: the [Grind 75](https://www.techinterviewhandbook.org/grind75) and the [NeetCode 150](https://neetcode.io/practice/practice/neetcode150) LeetCode lists, merged into one unified [problem catalog](problems/index.md), and the [Amazon OA](problems/amazon_oa/index.md) bank. Problems on both LeetCode tracks appear once, credited to each. Each problem page covers the statement and examples, with constraints where available. The [pattern intuition guides](patterns/index.md) explain the mental models behind the recurring algorithm patterns, and the [`practice/`](https://github.com/ThoDHa/tech-interview-prep/tree/main/practice) workspace lets you implement and test each solution yourself.

!!! tip "New to algorithms or interviews?"

    Start with the [Foundations](foundations/index.md) section. It teaches the prerequisites the problem pages assume, Big-O notation, recursion, the core data structures, and a method for approaching any problem, all from zero. For the plan around the problems, time budgeting, and the non-coding rounds, see the [Interview Prep](interview_prep/index.md) section.

Browse every problem in the [Problems catalog](problems/index.md), or use the navigation sidebar.

## Pattern Intuition

The [pattern intuition guides](patterns/index.md) explain the *why* behind each recurring algorithm pattern: the mental model, when it applies, the invariant that makes it work, and the Grind75 problems that use it. Start there when a problem feels unfamiliar and you need to recognize which pattern fits.

## Practice Workspace

The [`practice/`](https://github.com/ThoDHa/tech-interview-prep/tree/main/practice) directory is a `pytest` workspace for solving the problems yourself. Each problem has a `solution.py` to implement plus two test sets that mirror LeetCode's Run (the examples) and Submit (a full corner-case gauntlet). See its [README](https://github.com/ThoDHa/tech-interview-prep/blob/main/practice/README.md) for setup and the practice loop.
