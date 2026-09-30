# Study Plan and Schedule

Working through a problem bank without a plan stalls around problem 30, when the novelty wears off and the problems stop being easy. This page turns the bank into a budget: how many hours the preparation really takes, which style fits the time you have, and a week-by-week schedule that places the foundations and the Grind 75 track's canonical 75 into the eight weeks the repository promises. The NeetCode-only problems slot into the same weeks beside their closest Grind 75 topic; the [Amazon OA](../problems/amazon_oa/index.md) bank is its own track, paced by its own section.

## How much time this takes

The honest arithmetic:

- The Grind 75 track's problems carry a target time each (the Time column in the
  [problem list](../index.md)). Summed, they come to about 32 hours of first-pass solving.
- Nobody solves everything on the first pass. Between struggles, re-reading
  pattern guides, and spaced reviews, a realistic budget is two to three times the first-pass figure: roughly 65 to 100 hours total.
- Add the [Foundations](../foundations/index.md) (about an hour), behavioral
  preparation (about three hours, see [Behavioral Interviews](behavioral.md)), and two to four [mock interviews](mock_interviews.md).

As rough anchors: about 30 hours of focused work is the bare minimum to get through the core track meaningfully; about 100 hours leaves you well prepared. Eight weeks at 8 to 12 hours per week lands inside that band, which is why the schedule below is built on eight weeks.

**Estimate conservatively.** Plan for your worst realistic week, not your best one. A plan you keep beats an ambitious one you abandon in week three; if the schedule below feels tight, stretch it to ten or twelve weeks rather than cramming. Burnout late in the plan costs more than a slower start.

## How the budget moves with seniority

The totals above assume the coding track dominates, which is true at every level but to different degrees. What the loop actually tests shifts with seniority, and the budget should shift with it:

| Level | Realistic total | Where the hours go | Schedule adjustment |
|-------|-----------------|--------------------|---------------------|
| Junior / new grad | 60 to 80 hours | Nearly all coding: the full Grind 75 track, the [Foundations](../foundations/index.md) read twice, light [behavioral](behavioral.md) prep (about three hours) | Run the 8-week table as printed; behavioral stories come from internships, course projects, and side projects |
| Mid-level | 80 to 100 hours | The full coding track plus [System Design](../system_design/index.md) from week 5, at roughly a 4:1 coding-to-design split | Keep 8 weeks only if you can give 10 or more hours weekly; otherwise stretch to 10 rather than cut the design track |
| Senior and above | 100 to 120 hours | Coding drops to about half the hours; system design (including the [case studies](../system_design/case_studies/index.md)) and leadership-heavy behavioral stories take the other half | Stretch to 10 or 12 weeks; add one design case study per week from week 4 and rehearse influence stories, not just teamwork ones |

The pattern behind the table: the more senior the role, the more the loop scores judgment over recall. Junior loops stay inside data structures and algorithms; senior loops spend real time on design tradeoffs and on behavioral rounds that probe influence, mentoring, and cross-team leadership rather than teamwork basics. The 8-week schedule below stays the backbone at every level; seniority changes the mix around it, not the shape.

*The seniority adjustments follow the Tech Interview Handbook's guidance on [engineering levels](https://www.techinterviewhandbook.org/engineering-levels/) and [behavioral interviews for senior candidates](https://www.techinterviewhandbook.org/behavioral-interview-senior-candidates/); the hour totals and the mix split are derived from this repository's Time column and track structure.*

## Three ways to work through the bank

| Style | Shape | Choose it when |
|-------|-------|----------------|
| Breadth-first | Work the catalog in order, touching every topic as it appears | You have a month or more and no glaringly weak topic. This is the default the schedule below uses |
| Depth-first | Stay on one topic until it is exhausted, then move to the next | You have very little time, or an interview next week on a specific topic |
| Depth-then-breadth | Shore up your weakest topics first, then sweep the whole bank | You have more than a month and you already know where you are weak |

Breadth-first and depth-then-breadth are usually better than pure depth-first: topics you touched early come back before you forget them, which is the same instinct the practice tracker's spaced-repetition queue automates. In the unified study order, breadth-first works naturally because the ordering already revisits every topic several times.

## The 8-week schedule

The schedule paces the Grind 75 track in its canonical order, which moves from easier to harder problems with related problem types grouped together, so the weeks derive straight from that order: problems 1 through 30 in the first three weeks (ten each, while problems are short), then nine per week as they lengthen, ending with the nine hard problems in week 8. In the [problem list](../index.md) the NeetCode-only problems sit beside that backbone, slotted next to their closest Grind 75 topic; do each in the week its neighbors land in. The weekly schedule interleaves the [pattern groups](../patterns/index.md) in the same problem order; to follow the pattern curriculum instead, read each group straight through.

First-pass time is the sum of the Time column: one clean attempt each. It is a lower bound, not the plan.

| Week | Problems | First-pass time | Focus |
|------|----------|-----------------|-------|
| 1 | Foundations (about 1 hour), then 1-10 | 2h 55m | Read the four [Foundations](../foundations/index.md) first. Hash maps, two pointers, stacks, linked lists, binary search, first trees |
| 2 | 11-20 | 3h 05m | More trees and linked lists, queue from stacks, first dynamic programming ([Climbing Stairs](../problems/climbing_stairs.md)) |
| 3 | 21-30 | 4h 05m | First mediums: tree recursion, intervals, heaps, sliding window |
| 4 | 31-39 | 3h 55m | BFS and graphs, expression stacks, tries, DP ([Coin Change](../problems/coin_change.md)), design problems |
| 5 | 40-48 | 4h 25m | Graph traversal, binary search variants, backtracking begins, intervals. [Start mock interviews](mock_interviews.md) here |
| 6 | 49-57 | 3h 50m | The DP cluster, simulation, more backtracking, string DP |
| 7 | 58-66 | 4h 30m | Tree construction, backtracking on grids, heaps and greedy, design ([LRU Cache](../problems/lru_cache.md)) |
| 8 | 67-75 | 5h 30m | The hard tier: hard window and DP problems, serialization, monotonic stacks, streaming median, k-way merge |

Operating notes:

- **Week 1 starts with the foundations**, before problem 1. They are about an
  hour total and every later page assumes them.
- **Rate every solve from day one.** After each problem, record how it felt
  (`progress.py rate`). From week 2 on, clear the `due` review queue once a week before starting new problems; by weeks 5 through 8 that queue is where much of the real learning happens.
- **Read the pattern guide before each unfamiliar topic**, not after failing.
  The guide makes attempt one count.
- **Falling behind? Shift the plan, do not compress it.** Moving everything a
  week costs nothing. Squeezing week 8 into three days throws away the hard problems, which are the ones that differentiate.

!!! tip "Mocks start around week 5"

    That is roughly the 60% mark of the plan: enough patterns internalized that a mock is useful, enough plan left to fix what the mock exposes. See [Mock Interviews](mock_interviews.md).

## After week 8

- Two bonus problems, [Binary Tree Maximum Path Sum](../problems/binary_tree_maximum_path_sum.md)
  and [Maximum Frequency Stack](../problems/maximum_frequency_stack.md), sit beyond the canonical 75 if you want extra practice on trees and designs.
- Interviewing for mid-level and senior roles? Work through the
  [System Design section](../system_design/index.md) in parallel from about week 5, not after it.
- Keep the `due` queue running until the offer is signed. The review habit is
  worth more than any single problem.

## Make it yours

The schedule is a shape, not a contract. To adapt it: put real dates on a calendar first, then decide how many hours per week each block gets. Ten hours a week fits the table as printed; five hours a week means doubling the durations and stretching to about sixteen weeks, which is fine. If your interview is sooner than week 8 ends, cut breadth (for example, week 6's extra DP practice) before you cut the hard tier or the mocks.

---

*This page adapts the time-budgeting figures, preparation-style taxonomy, and conservative-estimation advice from the Tech Interview Handbook's [Coding Interview Study Plan](https://www.techinterviewhandbook.org/coding-interview-study-plan/). The 8-week schedule itself, the weekly splits, and the time sums are derived from this repository's problem order and Time column, and the spaced-repetition integration is original to this project.*
