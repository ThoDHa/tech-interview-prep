# [Task Scheduler](https://www.fastprep.io/problems/amazon-task-scheduler)

**Medium** | **NN minutes** | **Greedy, Heap**


AMZ Interval Collection (A group of problems focused on operations involving intervals :) - 



Task Scheduler (Full-Time)

Merge Intervals (Intern, NG)

Find Overlapping Times (Intern)

Get Maximum Sum Find Overlapping Times (Full-Time)

Optimal Interval Difference

You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of at least n intervals between two tasks with the same label.



Return the minimum number of CPU intervals required to complete all tasks.

## Examples

### Example 1

**Input:** `tasks = ["A","A","A","B","B","B"]`, `n = 2`

**Output:** `8`

**Explanation:** A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.



After completing task A, you must wait two intervals before doing A again. The same applies to task B. In the 3rd interval, neither A nor B can be done, so you idle. By the 4th interval, you can do A again as 2 intervals have passed.

### Example 2

**Input:** `tasks = ["A","C","A","B","D","B"]`, `n = 1`

**Output:** `6`

**Explanation:** A possible sequence is: A -> B -> C -> D -> A -> B.



With a cooling interval of 1, you can repeat a task after just one other task.

### Example 3

**Input:** `tasks = ["A","A","A","B","B","B"]`, `n = 3`

**Output:** `10`

**Explanation:** A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B.



There are only two types of tasks, A and B, which need to be separated by 3 intervals. This leads to idling twice between repetitions of these tasks.

## Constraints

- `1 <= tasks.length <= 10^4`
- `tasks[i] is an uppercase English letter.`
- `0 <= n <= 100`

## Solutions

### Max-Heap Simulation

#### Derivation

The most direct reading of the problem builds the schedule itself, one decision at a time. The decision follows one greedy principle: at every moment, run a task with the most copies left, because the tasks that repeat most are the ones that force idle time later, so they should claim slots as early as possible. A [max-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) surfaces the largest remaining count on demand, and the cooldown becomes a structural rule: one cycle spans `n + 1` slots (one task slot plus the `n` cooldown slots that must pass before the same task may repeat), so a cycle pops up to `n + 1` distinct tasks, and survivors wait out the rest of the cycle before returning to the heap:

1. Tally frequencies into `counts`, then load the negated counts into `heap` and
   heapify (Python's `heapq` is a min-heap, so negation makes it a max-heap).
2. Repeat while `heap` is non-empty: pop up to `n + 1` counts, consuming one
   copy per pop and tallying `executed`. A count still above zero after its
   pop goes to `survivors`, not straight back into the heap, which prevents a
   task from running twice inside one cooldown window.
3. After the cycle completes, push every survivor back.
4. If `heap` still holds work, the cycle is padded to its full `n + 1` width
   and contributes `n + 1` to `time` (the unfilled slots are idle). Otherwise
   the final cycle ends after its last task and contributes only `executed`.
5. Return the accumulated `time`.

#### Walkthrough

Let us trace the heap cycles on Example 3: `tasks = ["A","A","A","B","B","B"]`, `n = 3`, so each cycle spans `n + 1 = 4` slots. Counting gives `counts = {"A": 3, "B": 3}`, so `heap` starts as `[-3, -3]`. Each line is one cycle: the counts popped (shown positive, before their decrement), the survivors pushed back afterwards, and the time it charges:

```text
cycle 1   pops 3,3  -> survivors [-2, -2]   heap = [-2, -2]   time += 4 -> 4
cycle 2   pops 2,2  -> survivors [-1, -1]   heap = [-1, -1]   time += 4 -> 8
cycle 3   pops 1,1  -> survivors []         heap = []         time += 2 -> 10
```

Cycle 1 pops both `3`s, runs `A` and `B`, and defers their two remaining copies until the cycle ends; only two of the four slots found work, so the other two are the idle units the padding charges. Cycle 2 repeats the pattern one copy down. Cycle 3 pops the last copies of both tasks, and because the heap and `survivors` are both empty afterwards, the final cycle is not padded: it contributes only its `executed = 2`. The total is `10`, matching the expected Output and the example's schedule `A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B`.

#### Solution

The code is the cycle trace written down: up to `n + 1` pops, survivors buffered until the cycle closes, then pad or finish.

```python
import heapq
from typing import List


class Solution:
    def solve(self, tasks: List[str], n: int) -> int:
        counts: dict[str, int] = {}
        for task in tasks:
            counts[task] = counts.get(task, 0) + 1

        heap = [-count for count in counts.values()]
        heapq.heapify(heap)

        time = 0
        while heap:
            survivors: list[int] = []
            executed = 0
            for _ in range(n + 1):
                if heap:
                    remaining = -heapq.heappop(heap) - 1
                    executed += 1
                    if remaining > 0:
                        survivors.append(-remaining)

            for survivor in survivors:
                heapq.heappush(heap, survivor)

            if heap:
                time += n + 1
            else:
                time += executed

        return time
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log 26)`

Where `N` is the number of tasks: every task copy is popped once across all cycles, and each heap operation costs `O(log 26)` because the heap never holds more than 26 distinct counts. That is linear in `N` up to a small constant.

##### Space Complexity: `O(1)`

The heap and `survivors` list each hold at most 26 entries, independent of `N`.

#### Key Insights

- The heap automates the greedy pick (most copies left first) without re-sorting, and the cycle width `n + 1` is where the cooldown actually lives.
- Deferring survivors until the cycle closes is the correctness load-bearing detail: pushing a task back mid-cycle would let it run twice within one cooldown window.
- Padding every non-final cycle to `n + 1` while letting the last cycle end early is how idle time is counted without ever placing an idle slot.
- The trace settles into the same skeleton every run: the peak task anchors `max_freq - 1` cooldown gaps, and every other task fills or overflows them. That regularity is exactly the observation the formula below turns into arithmetic.

### Greedy Math Formula

#### Derivation

The simulation is trustworthy but pays to build a schedule the question never asks for, and its own trace keeps settling into the same rigid shape. Read the pattern off the trace instead of walking the clock: the most frequent task pins down `max_freq - 1` gaps of width `n + 1` (each anchor plus the `n` slots the cooldown forces after it), and every other task either fills those gaps or, when the gaps overflow, stretches the schedule to exactly `len(tasks)` with no idling at all. The length can therefore be priced without building the schedule:

1. Tally each task's frequency into `counts`, a dictionary keyed by letter.
2. Read `max_freq`, the largest value in `counts`.
3. Count the tasks tied at that peak into `max_count` (each needs a slot in the
   closing block).
4. Compute `frame = (max_freq - 1) * (n + 1) + max_count`.
5. Return `max(len(tasks), frame)`.

#### Closed Form

Let \(f_{\max}\) be the highest task frequency and \(c\) the number of distinct tasks tied at it. The answer is the maximum of two independent lower bounds:

$$ \text{answer} = \max\Bigl(\ \underbrace{|\text{tasks}|}_{\text{no idling}},\ \ \underbrace{(f_{\max} - 1)(n + 1) + c}_{\text{cooldown frame}}\ \Bigr) $$

```text
frame  = (max_freq - 1) * (n + 1) + max_count
answer = max(len(tasks), frame)
```

The frame term prices the schedule the busiest task forces: `max_freq - 1` internal gaps of width `n + 1`, then a closing block holding every task tied at the peak. The other term applies when the task mix is diverse enough to fill every idle slot, at which point the schedule is just its own length. Both terms are always achievable, which is what makes taking their maximum exact rather than a mere bound. Notice \(n\) appears only in the frame term: once the mix is diverse, the cooldown stops binding.

#### Walkthrough

The formula runs no clock, so the trace is the arithmetic itself, taken from Example 1: `tasks = ["A","A","A","B","B","B"]`, `n = 2`:

```text
counts    = {"A": 3, "B": 3}
max_freq  = 3                          A's count (B ties it)
max_count = 2                          both A and B reach the peak
frame     = (3 - 1) * (2 + 1) + 2      two gaps of width 3, closing block of 2
          = 8
answer    = max(6, 8) = 8              frame wins: idling is forced
```

The frame is exactly the schedule from the example's explanation, `A -> B -> idle -> A -> B -> idle -> A -> B`: two `n + 1 = 3`-wide gaps anchored at `A`, each holding `B` plus one idle slot, then the closing block of the `max_count = 2` peak tasks. The result `8` matches the expected Output, and `frame - len(tasks) = 2` counts precisely the two idle units in that schedule.

Example 2 exercises the other regime: `tasks = ["A","C","A","B","D","B"]`, `n = 1`:

```text
counts    = {"A": 2, "B": 2, "C": 1, "D": 1}
max_freq  = 2
max_count = 2                          A and B tie at the peak
frame     = (2 - 1) * (1 + 1) + 2 = 4
answer    = max(6, 4) = 6              len(tasks) wins: no idling
```

With four distinct tasks available for a cooldown of only one, no slot ever has to go idle, so the six tasks run back to back and the function returns `6`, matching the expected Output.

#### Solution

The code is the closed form evaluated once: a counting pass, then the arithmetic.

```python
from typing import List


class Solution:
    def solve(self, tasks: List[str], n: int) -> int:
        counts: dict[str, int] = {}
        for task in tasks:
            counts[task] = counts.get(task, 0) + 1

        max_freq = max(counts.values())
        max_count = sum(1 for freq in counts.values() if freq == max_freq)

        frame = (max_freq - 1) * (n + 1) + max_count

        return max(len(tasks), frame)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N)`

Where `N` is the number of tasks: one pass tallies the frequencies, and the remaining work scans the at-most-26 distinct counts and does constant arithmetic.

##### Space Complexity: `O(1)`

The `counts` dictionary holds at most 26 entries (uppercase English letters), independent of `N`.

#### Key Insights

- The answer is governed by the peak frequency and how many tasks tie for it; the identities of the remaining letters never matter, only how many copies of them there are.
- `(max_freq - 1) * (n + 1)` measures the rigid cooldown skeleton; `max_count` widens the closing block for every task tied at the peak.
- `max(len(tasks), frame)` resolves the two regimes cleanly: frame wins when idling is forced, task count wins when the mix fills every slot.
- A formula without the walkthrough is easy to distrust: the trace above shows the frame reproducing the example's own schedule slot for slot.

## Comparison of Solutions

### Time Complexity

- **Max-Heap Simulation**: `O(N log 26)` - every task copy is popped once, each heap operation costing a logarithmic term over at most 26 entries.
- **Greedy Math Formula**: `O(N)` - one frequency pass, then constant arithmetic over at most 26 counts.

### Space Complexity

- **Max-Heap Simulation**: `O(1)` - a 26-entry heap plus a survivors list of the same bound.
- **Greedy Math Formula**: `O(1)` - a 26-entry dictionary.

### Trade-offs

- **Max-Heap Simulation** constructs the schedule cycle by cycle, so its correctness is visible in the trace, at the cost of heap bookkeeping and a larger constant.
- **Greedy Math Formula** prices the schedule without building it: a single expression, minimal constant factors, but the two-bounds argument (frame versus task count) must be believed or re-derived.

### When to Use Each

- **Max-Heap Simulation**: when the answer must be justified step by step, or when extending the problem (reconstructing an actual schedule, dynamic task arrivals).
- **Greedy Math Formula**: the submission of choice; it meets the constraint ceiling in one linear pass and is the shortest thing to type under OA time pressure.

### Optimization Notes

- The formula's frame already hides an optimization: the argument that any task surplus over the gap slots collapses the schedule to `len(tasks)` is what lets the code skip simulating the overflow entirely.
- In the heap version, storing bare counts rather than `(count, letter)` pairs suffices, because no decision depends on which letter carries a count.
- Both solutions exploit the 26-letter alphabet: every per-letter structure is constant size, so the only term that scales is the single counting pass over `tasks`.
