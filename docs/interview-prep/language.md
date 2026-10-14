# Choosing a Language

Pick your interview language once, before problem 1, and commit to it for the whole plan. The difference between good interview languages is small; the cost of switching halfway through the plan is large. This page gives the selection criteria, the standard tier list, and why this repository speaks Python.

## The three criteria

1. **Interview suitability.** High-level languages with rich standard
   libraries win: they translate the solution in your head into working code faster, and any interviewer can read them.
2. **Your familiarity.** In an interview the bottleneck is the thinking, not
   the writing. A language you already think in beats a marginally better one you have to fight with.
3. **Domain exceptions.** Some roles bring their own language: JavaScript for
   front end, Swift for iOS, and similar. When the role demands it, the role wins over the tier list.

## The tier list

| Tier | Languages | Why |
|------|-----------|-----|
| Recommended | Python, C++, Java, JavaScript | High-level with expressive standard libraries; you write solutions at the speed you think them |
| Acceptable | Go, Ruby, PHP, C#, Swift, Kotlin | Workable; slightly more friction in some interview settings, and some interviewers see them less often |
| Avoid | Haskell, Erlang, Perl, C, Matlab | Not because they are bad languages, but because interviews are the wrong place for them: interviewers may not read them, or they make the easy parts hard |

"Acceptable" means you will not lose an interview over the choice. It does not mean there is no cost: expect to hand-roll small helpers a recommended language ships with.

## Familiarity beats optimality

Do not learn a new language under deadline pressure. That is the single most common prep mistake after skipping mocks.

Valid reasons to switch languages for interviews:

- Your daily language sits in the avoid tier (C, for example).
- Your target role demands its own language (front end, iOS).
- You have months, not weeks, and the new language is one you will keep using.

Poor reasons to switch:

- "Company X uses it." You are interviewing, not working there yet.
- "It looks faster to write." Only if you already write it fast.
- "My solution feels clumsy in my current language." The clumsiness is almost
  never the language.

Two corner cases worth knowing:

- Some companies restrict the choice. Google, for example, only allows a
  fixed set of languages. Check before you commit.
- If your language lacks a standard structure, do not build one mid-interview.
  Say you are assuming it, and state its complexities: "I'll assume a queue with O(1) push and pop." That is normal and accepted.

## Why this repository speaks Python

Python is the default here for the same reasons it tops the recommended tier:

- It reads like pseudocode, so the write-ups concentrate on the idea rather
  than the ceremony.
- Its standard library carries the interview toolkit: `collections`,
  `heapq`, `bisect`, `itertools`.
- Its APIs are consistent, which matters when you are recalling them under
  pressure.

Every foundations page, problem page, and pattern guide uses it, and the practice workspace is a Python `pytest` harness. If you choose a different language, the ideas transfer unchanged: the pattern guides and solution ladders are about the algorithm, not the syntax. You lose the runnable harness, so compensate with LeetCode or a local scratch setup, and keep everything else in the plan the same.

---

*This page adapts the selection criteria, tier list, and familiarity argument from the Tech Interview Handbook's [Programming Languages for Coding Interviews](https://www.techinterviewhandbook.org/programming-languages-for-coding-interviews/). The rationale for this repository's Python standard is original to this project.*
