# [Task Scheduler](https://leetcode.com/problems/task-scheduler/)

**Medium** | **30 minutes** | **Array, Hash Table, Greedy, Sorting, Heap**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md), [Greedy](../patterns/greedy_core/intuition.md)

**Algorithm:** [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) · [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure))

**Practice:** [`practice/task_scheduler/solution.py`](../../practice/task_scheduler/solution.py)

Given a characters array `tasks`, representing the tasks a CPU needs to do, where each letter represents a different task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.

However, there is a non-negative integer `n` that represents the cooldown period between two same tasks (the same letter in the array), that is, there must be at least `n` units of time between any two same tasks.

Return the least number of units of time that the CPU will take to finish all the given tasks.

## Examples

### Example 1

**Input:** `tasks = ["A","A","A","B","B","B"]`, `n = 2`

**Output:** `8`

**Explanation:** A -> B -> idle -> A -> B -> idle -> A -> B There is at least 2 units of time between any two same tasks.

### Example 2

**Input:** `tasks = ["A","A","A","B","B","B"]`, `n = 0`

**Output:** `6`

**Explanation:** On this case any permutation of size 6 would work since n = 0. `["A","A","A","B","B","B"]` `["A","B","A","B","A","B"]` `["B","B","B","A","A","A"]` ... And so on.

### Example 3

**Input:** `tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"]`, `n = 2`

**Output:** `16`

**Explanation:** One possible solution is A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A

## Constraints

- `1 <= task.length <= 10^4`
- `tasks[i]` is an uppercase English letter.
- `0 <= n <= 100`

## Deriving the Solution

The cooldown binds only through repetition: `n` other units must separate two copies of the same letter, so the task that repeats most often is the one that threatens idle time. Every solution below therefore runs the most frequent remaining task as early as possible; they differ in how much of the schedule they actually build in order to measure its length.

1. **Start literal.** Walk the timeline one unit at a time, and at each unit run the
   eligible task (off cooldown, copies left) with the most copies remaining. Correct by construction, but every unit, idle ones included, rescans up to 26 counts, costing `O(N * (n + 1) * 26)`: see [Brute Force Simulation](#brute-force-simulation).
2. **Read the pattern off the trace.** The simulation always settles into the same
   shape: the most frequent task pins down `max_freq - 1` gaps of width `n + 1`, and every other task either fills those gaps or overflows them. That skeleton can be priced directly as `max(len(tasks), (max_freq - 1) * (n + 1) + max_count)`, with no loop over time at all: see [Greedy Math Formula](#greedy-math-formula).
3. **Simulate in rounds instead.** The formula's leap is easy to distrust, and the
   brute force's flaw was only its per-unit crawl. Keeping the simulation but processing a whole `n + 1`-wide round per iteration removes the idle-unit scans: sort the counts, run the top `n + 1` tasks, pad short rounds with idle time: see [Greedy Round Simulation](#greedy-round-simulation).
4. **Automate the greedy pick.** Re-sorting all 26 counts each round only to take
   the largest few is exactly the work a max-heap avoids, surfacing the largest count in `O(log 26)` per pop: see [Max-Heap Simulation](#max-heap-simulation).
5. **Hand the tally to the library.** Every approach above opens by building the
   same frequency dictionary by hand, which is bookkeeping rather than algorithm. `Counter(tasks)` does it in one call, leaving the greedy idle-frame arithmetic fully explicit while deleting three lines from the shortest solution: see [Greedy Math Formula with Counter](#greedy-math-formula-with-counter).

## Solutions

### Brute Force Simulation

#### Derivation

The question to ask first is the literal one: what does the schedule actually look like, unit by unit? At each time unit the CPU either runs some eligible task or sits idle, so the only decision is which task to run when several are eligible. Running the task with the most copies left is the [greedy choice](https://en.wikipedia.org/wiki/Greedy_algorithm) that keeps later idle gaps fillable: the tasks that repeat most are the ones that force idling, so they should claim slots as early as possible. The cooldown itself needs no cleverness, only memory: recording when each task last ran decides eligibility directly.

1. Count each task's frequency into a plain dictionary and collect the counts into a
   `remaining` list. Keep a parallel `last_used` list recording the time unit at which each task last ran (`-inf` until it first runs).
2. Step the clock from `time = 0` upward. A task is eligible at the current unit when
   it still has copies left and enough time has passed since it last ran (`time - last_used[i] > n`).
3. Among the eligible tasks, pick the one with the largest `remaining` count.
4. If a task was chosen, decrement it, stamp `last_used`, and mark one more task
   `done`. If none was eligible, the unit is idle. Either way, advance the clock.
5. Stop once every task copy has been placed and return the elapsed `time`.

The cooldown bookkeeping is done entirely by hand through `last_used`, with no sort, heap, or formula. It is the slowest approach but the easiest to believe correct, because it mirrors the literal definition of the schedule.

#### Walkthrough

Let us watch the brute force simulation run on Example 1: `tasks = ["A","A","A","B","B","B"]`, `n = 2`. After counting, `counts = {"A": 3, "B": 3}`, so index `0` tracks `A` and index `1` tracks `B`. Both start at `remaining = [3, 3]` with `last_used = [-inf, -inf]`.

At each `time` unit, we scan for the eligible task (off cooldown, `time - last_used[i] > n`, copies left) with the largest `remaining` count. The tie-break is strict (`remaining[i] > remaining[best]`), so when counts are equal the lower index wins, which is why `A` is preferred over `B` on the first tie. The table shows the state after each unit is processed:

| `time` | chosen | `remaining` | `last_used` | `done` |
|--------|--------|-------------|-------------|--------|
| 0 | `A` | `[2, 3]` | `[0, -inf]` | 1 |
| 1 | `B` | `[2, 2]` | `[0, 1]` | 2 |
| 2 | idle | `[2, 2]` | `[0, 1]` | 2 |
| 3 | `A` | `[1, 2]` | `[3, 1]` | 3 |
| 4 | `B` | `[1, 1]` | `[3, 4]` | 4 |
| 5 | idle | `[1, 1]` | `[3, 4]` | 4 |
| 6 | `A` | `[0, 1]` | `[6, 4]` | 5 |
| 7 | `B` | `[0, 0]` | `[6, 7]` | 6 |

Reading the choices in order: at `time = 0`, both are tied at 3 so `A` runs. At `time = 1`, `A` is now on cooldown (`1 - 0 = 1`, not `> 2`), so `B` runs. At `time = 2`, neither is eligible yet (`A` ran at 0, `B` ran at 1, both within the 2-unit cooldown), so the CPU idles and `time` simply ticks. By `time = 3`, `A` is off cooldown again (`3 - 0 = 3 > 2`) and runs, and the pattern repeats: `A -> B -> idle -> A -> B -> idle -> A -> B`.

Once `done` reaches `total = 6` at `time = 7`, the loop exits and `time` has already advanced to `8`. The returned value is `8`, matching the expected Output.

#### Solution

The code is the walkthrough's loop written down: one clock tick per iteration, with the eligibility scan and the greedy pick inside.

```python
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # Tally each task's frequency; only the counts matter here, never
        # which letter carries them.
        counts = {}
        for t in tasks:
            counts[t] = counts.get(t, 0) + 1

        remaining = list(counts.values())
        # Track the last time unit at which each task ran; -inf means never.
        last_used = [float("-inf")] * len(remaining)
        done = 0
        total = len(tasks)
        time = 0

        # Walk the timeline one unit at a time until every task is placed.
        while done < total:
            # Among tasks that are off cooldown and still have copies, pick the
            # one with the most remaining: that greedy choice avoids future idle.
            best = -1
            for i in range(len(remaining)):
                if remaining[i] > 0 and time - last_used[i] > n:
                    if best == -1 or remaining[i] > remaining[best]:
                        best = i

            if best != -1:
                remaining[best] -= 1
                last_used[best] = time
                done += 1
            # If no task is eligible, this unit is idle; either way the clock ticks.
            time += 1

        return time
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N * (n + 1) * 26)`

Let `N` be the number of tasks. The clock advances one unit per iteration, and the schedule length is not `O(N)`: idle units count too, and the optimal schedule can be as long as `(max_freq - 1) * (n + 1) + max_count`, which is `O(N * (n + 1))` when one task dominates. Each unit scans the at-most-26 distinct task counts to find the best eligible one, giving `O(N * (n + 1) * 26)` overall. With `n <= 100` this is still manageable for the constraints, but it is far from linear in `N` alone.

##### Space Complexity: `O(1)`

The `counts` dictionary together with the `remaining` and `last_used` lists hold at most 26 entries (uppercase letters), independent of `N`.

#### Key Insights

- Simulating unit by unit follows the problem statement literally, which makes the
  result easy to trust without any cleverness.
- Tracking `last_used` per task enforces the cooldown directly: a task simply cannot
  be chosen until `n` units have passed since its last run.
- The greedy "run the highest remaining count" tie-break is what prevents the
  simulation from idling unnecessarily.
- It is wasteful: every idle unit is still scanned, so the round-based simulation
  below collapses the timeline into `n + 1`-wide rounds to skip that per-unit work.

### Greedy Math Formula

#### Derivation

The brute force answers the question by walking every unit of the schedule, idle units included, even though its own trace keeps producing the same rigid shape. Ask instead what forces idle time at all: only the most frequent task. Suppose its frequency is `max_freq`, and lay its occurrences out as anchors separated by cooldown gaps of width `n`:

```text
A . . . A . . . A
```

There are `max_freq - 1` gaps, each spanning `n + 1` slots (the task plus the `n` slots after it), which accounts for `(max_freq - 1) * (n + 1)` units. The final anchor block needs room for every task that also hits the peak frequency, so add `max_count`, the number of tasks tied for the maximum. Every other task either slots into a gap, or, when the gaps overflow, pushes the schedule out to exactly `len(tasks)` with no idling at all. The schedule length can therefore be priced without building the schedule:

1. Count each task's frequency into a plain dictionary.
2. Find `max_freq` and `max_count` (how many tasks reach it).
3. Compute the frame `(max_freq - 1) * (n + 1) + max_count`.
4. Return `max(len(tasks), frame)`.

When the frame exceeds `len(tasks)`, the difference is exactly the number of forced idle units; otherwise every slot is busy.

#### Closed Form

Let \(f_{\max}\) be the highest task frequency and \(c\) the number of distinct tasks tied at it. The answer is a maximum of two independent lower bounds:

$$ \text{answer} = \max\Bigl(\ \underbrace{|\text{tasks}|}_{\text{no idling}},\ \ \underbrace{(f_{\max} - 1)(n + 1) + c}_{\text{cooldown frame}}\ \Bigr) $$

```text
frame  = (max_freq - 1) * (n + 1) + max_count
answer = max(len(tasks), frame)
```

Both terms are lower bounds, and the larger one is always achievable, which is what makes taking their maximum exact rather than merely a bound. The frame term counts the schedule forced by the busiest task: its \(f_{\max}\) copies create \(f_{\max} - 1\) gaps, each occupying \(n + 1\) slots, plus a final block wide enough for the \(c\) tasks tied at the peak. The other term applies when there are enough distinct tasks to fill every idle slot, at which point no idling happens and the schedule is just its own length.

Note that \(n\) does not appear in the second term at all: once the task mix is diverse enough, the cooldown stops binding entirely.

#### Walkthrough

The formula runs no clock, so the trace is the arithmetic itself. First Example 1: `tasks = ["A","A","A","B","B","B"]`, `n = 2`. Counting gives `counts = {"A": 3, "B": 3}`:

```text
max_freq  = 3                          A's count (B ties it)
max_count = 2                          both A and B hit the peak
frame     = (3 - 1) * (2 + 1) + 2      two gaps of width 3, final block of 2
          = 8
answer    = max(6, 8) = 8              frame wins: idling is forced
```

The frame is the schedule `A -> B -> idle -> A -> B -> idle -> A -> B`: two full `n + 1 = 3`-wide gaps anchored at `A`, each holding `B` plus one idle slot, then the closing block of the `max_count = 2` peak tasks. The result `8` matches Example 1's Output, and `frame - len(tasks) = 2` counts exactly the two idle units.

Example 2 exercises the other regime: the same tasks with `n = 0`:

```text
max_freq  = 3
max_count = 2
frame     = (3 - 1) * (0 + 1) + 2 = 4
answer    = max(6, 4) = 6              len(tasks) wins: no idling
```

With no cooldown the frame collapses below the task count, so the answer is simply the `6` tasks back to back, matching Example 2's Output.

#### Solution

The code is the closed form evaluated once: a counting pass, then the arithmetic.

```python
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # Tally frequencies: the formula reads only the peak count and how
        # many tasks tie for it.
        counts = {}
        for t in tasks:
            counts[t] = counts.get(t, 0) + 1

        max_freq = max(counts.values())
        # How many distinct tasks share that peak frequency.
        max_count = sum(1 for freq in counts.values() if freq == max_freq)

        # Frame built around the most frequent task: (max_freq - 1) full gaps of
        # width (n + 1), then the final block holding every peak task.
        frame = (max_freq - 1) * (n + 1) + max_count

        # If there are enough distinct tasks to fill every idle slot, no idling is
        # needed and the answer is simply the number of tasks.
        return max(len(tasks), frame)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N)`

Where `N` is the number of tasks. Counting frequencies is `O(N)`, and the remaining work scans at most 26 distinct task counts, which is constant.

##### Space Complexity: `O(1)`

The frequency dictionary holds at most 26 entries (uppercase letters), independent of `N`.

#### Key Insights

- The answer is governed entirely by the peak frequency and how many tasks tie for
  it; the exact identities of other tasks do not matter.
- `(max_freq - 1) * (n + 1)` measures the rigid skeleton imposed by cooldown; adding
  `max_count` accounts for the trailing block of all peak tasks.
- Taking `max(len(tasks), frame)` cleanly resolves the two cases: idle-bound (frame
  wins) versus task-bound (no idling needed).
- The formula collapses the round-by-round simulation into a single arithmetic
  expression with no loop over time at all, but it requires the peak-frequency insight that the simulations below make explicit by tracing the schedule directly.

### Greedy Round Simulation

#### Derivation

The formula is fast but rests on a leap; the brute force is trustworthy but crawls through every idle unit one scan at a time. This approach repairs the brute force's per-unit waste while keeping the simulation: the schedule naturally divides into frames of `n + 1` slots, the minimum gap before the most frequent task may repeat, so process a whole frame per iteration instead of a single unit. Within each frame, [greedily](https://en.wikipedia.org/wiki/Greedy_algorithm) run the tasks with the most copies left, because those are the ones most likely to force idle time later.

1. Count each task's frequency into a plain dictionary, then collect the counts
   into a `remaining` list.
2. Repeat until every count is zero. At the start of each round, sort `remaining`
   in descending order so the most-needed tasks come first.
3. Execute up to `n + 1` of them: decrement each chosen task's count and tally
   `executed`, the number that actually ran this round.
4. If any tasks still remain after the round, the round must be padded to the full
   `n + 1` width (the unfilled slots are idle), so add `n + 1` to `time`. If nothing remains, the final round needs no trailing idle, so add only `executed`.
5. Return the accumulated `time`.

The idle time is never placed explicitly; it falls out of padding non-final rounds to full width.

#### Walkthrough

Let us run the rounds on Example 1: `tasks = ["A","A","A","B","B","B"]`, `n = 2`, so each round spans `n + 1 = 3` slots. After counting, `remaining = [3, 3]` (index `0` for `A`, index `1` for `B`). Each line shows one round: the descending sort, the slots executed, and the time added:

```text
round 1   sort [3, 3]   run 2 -> remaining [2, 2]   work left:  time += 3 -> 3
round 2   sort [2, 2]   run 2 -> remaining [1, 1]   work left:  time += 3 -> 6
round 3   sort [1, 1]   run 2 -> remaining [0, 0]   all done:   time += 2 -> 8
```

Only two distinct tasks exist, so each round fills two of its three slots; the third slot is the idle unit, charged implicitly when the round is padded to `n + 1 = 3`. The final round is not padded: both counts hit zero, so it contributes only its `executed = 2` units. The accumulated `time` is `8`, matching Example 1's Output and the schedule `A -> B -> idle -> A -> B -> idle -> A -> B`.

#### Solution

The code is one round per loop iteration: sort, run up to `n + 1` tasks, then pad or close.

```python
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # Tally frequencies; the counts alone drive each round's greedy pick.
        counts = {}
        for t in tasks:
            counts[t] = counts.get(t, 0) + 1

        remaining = list(counts.values())
        time = 0

        # Simulate the schedule one cooldown frame at a time.
        while any(c > 0 for c in remaining):
            # Greedily run the highest-frequency tasks first this round.
            remaining.sort(reverse=True)

            executed = 0
            # A round can run at most n + 1 distinct tasks before the most
            # frequent task is eligible to repeat.
            for i in range(n + 1):
                if i < len(remaining) and remaining[i] > 0:
                    remaining[i] -= 1
                    executed += 1

            # If tasks still remain, the unused slots in this round are idle;
            # otherwise the final round simply ends with no trailing idle time.
            if any(c > 0 for c in remaining):
                time += n + 1
            else:
                time += executed

        return time
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N * 26 log 26)`

Let `N` be the number of tasks. The simulation runs roughly `O(total_time)` rounds, bounded by the schedule length which is `O(N)`. Each round sorts the `remaining` list of at most 26 counts, costing `O(26 log 26)`, a constant. Multiplying gives `O(N * 26 log 26)`, which is effectively linear in `N` with a constant factor.

##### Space Complexity: `O(1)`

The `counts` dictionary and `remaining` list hold at most 26 entries (uppercase letters), independent of `N`.

#### Key Insights

- Running the highest-remaining-count tasks first each round is the greedy choice
  that minimizes forced idling.
- Each cooldown frame is naturally `n + 1` wide, which is why a round executes up to
  `n + 1` distinct tasks.
- The idle time is never placed explicitly; it emerges from padding non-final rounds
  to full width while letting the last round end early.
- The 26-letter alphabet caps `remaining` at 26 entries, so the per-round sort is a
  constant cost no matter how long `tasks` grows.

### Max-Heap Simulation

#### Derivation

The round simulation re-sorts the entire `remaining` list every round only to read off its largest few entries. Surfacing the largest count on demand is exactly what a [max-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) does in `O(log 26)` per pop, so the per-round sort can go. The rounds themselves stay: each cooldown cycle is `n + 1` slots wide, the minimum gap before the most frequent task may repeat, so each cycle pops up to `n + 1` tasks, decrements them, and defers any survivors to the next cycle.

1. Count frequencies into a plain dictionary, then build a max-heap by negating
   the counts (Python's `heapq` is a min-heap).
2. For each cooldown cycle, attempt to pop up to `n + 1` tasks. For every pop,
   consume one copy and tally `executed`; if copies remain, stash the task in a temporary `survivors` list rather than pushing it back mid-cycle (which could let a task run twice inside one cooldown window).
3. Push every survivor back onto the heap after the cycle completes.
4. If the heap still holds work, the cycle must be padded to its full `n + 1`
   width (the unfilled slots are idle), so add `n + 1` to `time`. If nothing remains, the final cycle ends after its last task, so add only `executed`.

Deferring survivors until the cycle completes is what enforces the cooldown: a task cannot reappear until `n + 1` slots have passed.

#### Walkthrough

Let us trace the heap on Example 3: `tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"]`, `n = 2`, so each cycle spans `n + 1 = 3` slots. Counting gives `A: 6` and one copy each of `B` through `G`; negated, `heap` starts as one `-6` and six `-1` entries. The heap stores only counts, so any of the tied `-1` entries may be popped first; the schedule length is the same either way. Each line shows one cycle: the counts popped (positive, before their decrement), the survivors pushed back, and the time added:

```text
cycle 1   pops 6,1,1   survivors [-5]   heap [-5,-1,-1,-1,-1]   time += 3 -> 3
cycle 2   pops 5,1,1   survivors [-4]   heap [-4,-1,-1]         time += 3 -> 6
cycle 3   pops 4,1,1   survivors [-3]   heap [-3]               time += 3 -> 9
cycle 4   pops 3       survivors [-2]   heap [-2]               time += 3 -> 12
cycle 5   pops 2       survivors [-1]   heap [-1]               time += 3 -> 15
cycle 6   pops 1       survivors []     heap []                 time += 1 -> 16
```

The first three cycles run `A` plus two of the singleton tasks each, consuming `B` through `G`. From cycle 4 on, only `A` survives: each cycle pops it once, finds the heap empty for its remaining two slots (`executed = 1`), and is still padded to the full width of `3`, charging two idle units. The final cycle is not padded: after its pop both the heap and `survivors` are empty, so it contributes only `executed = 1`. The total is `16`, matching Example 3's Output and its schedule `A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A`.

#### Solution

The code is the cycle trace written down: up to `n + 1` pops, survivors buffered and re-pushed, then pad or close.

```python
import heapq
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # Tally frequencies; only these counts are ever loaded into the heap.
        counts = {}
        for t in tasks:
            counts[t] = counts.get(t, 0) + 1

        # Negate counts to turn Python's min-heap into a max-heap.
        heap = [-c for c in counts.values()]
        heapq.heapify(heap)

        time = 0
        while heap:
            survivors = []
            executed = 0
            # One cooldown cycle is n + 1 slots wide; run up to n + 1 tasks.
            for _ in range(n + 1):
                if heap:
                    # Pop the most frequent remaining task and consume one copy.
                    count = -heapq.heappop(heap) - 1
                    executed += 1
                    if count > 0:
                        survivors.append(-count)

            # Return the still-pending tasks to the heap for the next cycle.
            for s in survivors:
                heapq.heappush(heap, s)

            # If work remains, pad this cycle to full width (the unused slots
            # are idle); otherwise the final cycle ends after the last task.
            if heap:
                time += n + 1
            else:
                time += executed

        return time
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log 26)`

Let `N` be the number of tasks. Every task copy is popped and possibly pushed once across all cycles, and each heap operation costs `O(log 26)` since the heap holds at most 26 distinct tasks. The total is `O(N log 26)`, effectively linear in `N` with a small constant.

##### Space Complexity: `O(1)`

The heap and `survivors` list each hold at most 26 entries (uppercase letters), independent of `N`.

#### Key Insights

- The heap automates the greedy "run the most frequent task first" rule, replacing
  the per-round sort of the array-based simulation.
- Survivors must be buffered and pushed back only after the full `n + 1` cycle,
  otherwise a task could be scheduled twice within a single cooldown window.
- Breaking out when both the heap and survivors are empty avoids counting trailing
  idle slots in the final, partial cycle.

### Greedy Math Formula with Counter

#### Derivation

Every solution above opens with the same three lines: an empty dictionary, a loop over `tasks`, and a `counts.get(t, 0) + 1` bump. That tally is bookkeeping, not algorithm, and [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) does exactly it in one call. Applying it to the [Greedy Math Formula](#greedy-math-formula) leaves the greedy reasoning completely untouched: the peak frequency still pins down `max_freq - 1` gaps of width `n + 1`, the tied peak tasks still occupy the closing block, and `max(len(tasks), frame)` still resolves the idle-bound and task-bound cases. Only the counting loop moves off the page.

1. Build `counts = Counter(tasks)`, which walks `tasks` once and returns a
   frequency map keyed by task letter.
2. Read `max_freq = max(counts.values())`, the frequency of the busiest task.
3. Count how many tasks tie at that peak to get `max_count`.
4. Compute the idle frame `(max_freq - 1) * (n + 1) + max_count` exactly as
   before, keeping the arithmetic explicit rather than hiding it behind a helper.
5. Return `max(len(tasks), frame)`.

The keys never matter to the arithmetic, only the multiset of counts, so `Counter` is a drop-in for the dictionary with no change in behavior. A `Counter` also spares the reader from checking that the `get(t, 0)` default is right, a small correctness question that simply stops existing.

#### Walkthrough

Take Example 3, the case where one task dominates a field of singletons: `tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"]`, `n = 2`. The single `Counter` call replaces the whole tally loop:

```text
counts    = Counter({A: 6, B: 1, C: 1, D: 1, E: 1, F: 1, G: 1})
max_freq  = 6                          A repeats six times; nothing ties it
max_count = 1                          only A reaches the peak
frame     = (6 - 1) * (2 + 1) + 1      five gaps of width 3, closing block of 1
          = 16
answer    = max(12, 16) = 16           frame wins: idling is forced
```

The frame is the schedule `A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A`: five `n + 1 = 3`-wide gaps anchored at `A`, then the closing block holding the single peak task. The six singletons fill only six of the ten non-anchor slots, so `frame - len(tasks) = 4` counts exactly the four idle units in that schedule. The result `16` matches Example 3's expected Output of `16`.

#### Solution

The same closed form as before, with the tally delegated to the standard library.

```python
from collections import Counter
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        counts = Counter(tasks)

        max_freq = max(counts.values())
        # How many distinct tasks share that peak frequency.
        max_count = sum(1 for freq in counts.values() if freq == max_freq)

        # Frame built around the most frequent task: (max_freq - 1) full gaps of
        # width (n + 1), then the final block holding every peak task.
        frame = (max_freq - 1) * (n + 1) + max_count

        # If there are enough distinct tasks to fill every idle slot, no idling is
        # needed and the answer is simply the number of tasks.
        return max(len(tasks), frame)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N)`

Where `N` is the number of tasks. `Counter(tasks)` makes one pass over the input, and the two reads of `counts.values()` plus the arithmetic touch at most 26 distinct counts, which is constant. Identical to the hand-rolled formula, with a smaller constant on the counting pass because `Counter` tallies in C rather than through a Python-level loop.

##### Space Complexity: `O(1)`

The `Counter` holds at most 26 keys (uppercase letters), independent of `N`. A hash table costs more per entry than a plain dictionary would, which does not move the bound.

#### Key Insights

- The greedy reasoning is untouched: `Counter` replaces only the tally, while the
  `(max_freq - 1) * (n + 1) + max_count` frame stays spelled out on the page, which is the whole point of the substitution.
- Frequency counting is the single most repeated idiom in this problem, appearing
  identically in all four hand-rolled solutions, so it is the obvious candidate to hand to the library.
- `Counter` is a `dict` subclass, so `counts.values()` and `max(...)` behave
  exactly as they did over the plain dictionary, and no other line needs adapting.
- The zero-key hazard that bites `Counter` in sliding-window problems cannot
  arise here, because nothing is ever decremented: the counts are built once and only read.

## Comparison of Solutions

### Time Complexity

- **Brute Force Simulation**: `O(N * (n + 1) * 26)` because it advances the clock
  through every unit of the schedule, idle units included, and the schedule can be `O(N * (n + 1))` units long, scanning up to 26 counts at each one.
- **Greedy Math Formula**: `O(N)` because it only counts frequencies once and then
  does constant arithmetic over at most 26 counts.
- **Greedy Round Simulation**: `O(N * 26 log 26)` because it runs roughly `O(N)`
  rounds, each sorting up to 26 counts.
- **Max-Heap Simulation**: `O(N log 26)` because every task copy is popped and
  pushed once, each heap operation costing `O(log 26)`.
- **Greedy Math Formula with Counter**: `O(N)`, the same single counting pass and
  constant arithmetic as the hand-rolled formula, with `Counter` tallying in C rather than through a Python-level loop.

### Space Complexity

- **Brute Force Simulation**: `O(1)`, using a 26-entry dictionary plus the
  `remaining` and `last_used` lists.
- **Greedy Math Formula**: `O(1)`, using a 26-entry dictionary.
- **Greedy Round Simulation**: `O(1)`, using a 26-entry dictionary and list.
- **Max-Heap Simulation**: `O(1)`, using a 26-entry heap and survivors list.
- **Greedy Math Formula with Counter**: `O(1)`, using a 26-key `Counter`, which
  carries more per-entry overhead than a plain dictionary without changing the bound.

All five use constant auxiliary space; the difference is in time and conceptual complexity.

### Trade-offs

- The brute force simulation builds the schedule one time unit at a time, mirroring
  the problem statement literally. That makes it the easiest to trust, but it scans every idle unit, so it does the most redundant work.
- The formula is a single expression with no loop over time, making it dramatically
  faster. It requires the insight that the peak frequency alone determines the idle skeleton, a leap that is harder to derive from scratch.
- The greedy round simulation collapses the timeline into `n + 1`-wide rounds,
  skipping the per-unit idle scan. It pays for this with a per-round sort and still traces the schedule round by round.
- The max-heap simulation replaces the per-round sort with a heap, automating the
  greedy choice in `O(log 26)` per operation. It is the natural data-structure refinement of the round simulation while still tracing the schedule cycle by cycle.
- The `Counter` formula keeps the closed form's runtime and its explicit idle-frame
  arithmetic while shedding the four-line tally, so the only thing on the page is the reasoning a reader has to check. The cost is an import and a hash table where a plain dictionary would do, neither of which changes the complexity.

### When to Use Each

- **Brute Force Simulation**: When you want the most literal, easiest-to-verify
  model of the schedule, or as a baseline to check the faster approaches against.
- **Greedy Math Formula**: Preferred for production and for the constraint ceiling,
  where the closed form runs in a single linear pass with no simulation overhead.
- **Greedy Round Simulation**: Useful when you want to verify behavior, visualize the
  actual schedule, or when the greedy formula's derivation is not yet obvious.
- **Max-Heap Simulation**: When you want the simulation's transparency but prefer a
  heap to express the greedy choice, a common interview-favored formulation.
- **Greedy Math Formula with Counter**: The Pythonic default. Reach for it whenever
  `collections` is available and readability is the deciding factor, since it is the shortest form that still shows the idle-frame arithmetic in full. Fall back to the hand-rolled dictionary only where an import is genuinely unavailable, such as a restricted judge or a port to a language without an equivalent helper.

### Optimization Notes

- The brute force simulation establishes the greedy principle (always run the most
  frequent eligible task first) by hand, tracking each task's cooldown through a `last_used` timestamp.
- The formula is the key algorithmic optimization: recognizing that the most
  frequent task dictates the layout removes the need to simulate every time unit, collapsing an `O(N * (n + 1) * 26)` walk into constant arithmetic over 26 counts.
- The greedy round simulation skips the per-unit idle scan by processing a full
  `n + 1`-wide round at a time, surfacing the greedy choice with a per-round sort.
- The max-heap simulation is the structural optimization of the round simulation: a
  heap surfaces the most frequent task in `O(log 26)` instead of re-sorting each round.
- Every solution spends one `O(N)` pass tallying frequencies and then works only
  over the at-most-26 distinct counts, so the tally is the sole term in any of them that actually scales with `N`.
- Greedy Math Formula with Counter changes no arithmetic at all: `Counter(tasks)`
  simply performs the tally in C rather than in a Python-level loop, which trims the constant on that one linear pass.
