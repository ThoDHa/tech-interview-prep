# [Maximum Profit in Job Scheduling](https://www.fastprep.io/problems/amazon-maximum-profit-job-scheduling)

**Hard** | **NN minutes** | **Array, Sorting, Binary Search, Dynamic Programming, Intervals**

You are given equal-length arrays startTime, endTime, and profit. Job i runs on the half-open interval from its start time to its end time and earns its profit.

Select non-overlapping jobs to maximize total profit. A job that starts exactly when another ends does not overlap.

## Examples

### Example 1

**Input:** `startTime = [1,2,3,3]`, `endTime = [3,4,5,6]`, `profit = [50,10,40,70]`

**Output:** `120`

**Explanation:** Choose jobs [1,3) and [3,6) for profit 120.

### Example 2

**Input:** `startTime = [1,2,3,4,6]`, `endTime = [3,5,10,6,9]`, `profit = [20,20,100,70,60]`

**Output:** `150`

**Explanation:** Jobs [1,3), [4,6), and [6,9) earn 150.

### Example 3

**Input:** `startTime = [1,1,1]`, `endTime = [2,3,4]`, `profit = [5,6,4]`

**Output:** `6`

**Explanation:** All jobs overlap, so choose the highest-profit one.

## Constraints

- `1 ≤ startTime.length = endTime.length = profit.length ≤ 50000.`
- `0 ≤ startTime[i] < endTime[i] ≤ 10^9.`
- `1 ≤ profit[i] ≤ 10000.`

## Solutions

The four solutions below are the same weighted interval scheduling problem in increasing order of refinement: enumerate every legal subset, then order the decisions so dynamic programming applies, then speed up the predecessor lookup from a scan to a search. The final two differ only in who owns the binary search.

### Brute Force

#### Derivation

The most literal reading enumerates every subset of jobs that can legally run together and keeps the most profitable one. Walk the jobs in their given order and branch at each one: skip it, or take it and reject it when it overlaps a job already committed on this path. Because the input is unsorted, the last-taken job is not necessarily the latest in time, so a candidate must be compared against the whole `chosen` set, not just its most recent member. Treating each job as the half-open interval `[start, end)` makes the shared-boundary rule automatic: `[candidate_start, candidate_end)` is disjoint from `[chosen_start, chosen_end)` when `candidate_end <= chosen_start` or `chosen_end <= candidate_start`:

1. `search(job_idx, chosen)` returns `0` once `job_idx` passes the last job:
   every job has been decided.
2. The skip branch is `search(job_idx + 1, chosen)` unchanged.
3. The take branch is allowed only when no interval in `chosen` overlaps
   `(start, end)`; it returns `profit` plus `search(job_idx + 1, chosen +
   [(start, end)])`.
4. Return the larger of the two branches; start at `search(0, [])`.

#### Walkthrough

Example 1, with jobs labeled `j0 = [1,3) p=50`, `j1 = [2,4) p=10`, `j2 = [3,5) p=40`, `j3 = [3,6) p=70`. The winning path takes `j0` then `j3`; the trace shows that path with the sibling branches it beat:

```text
search(0, [])                     -> max(skip 70, take j0 120) = 120
├─ skip: search(1, [])            -> 70   (best without j0 is j3 alone)
└─ take j0 [1,3) profit 50: 50 + search(1, [(1,3)])
   search(1, [(1,3)])             -> 70
   ├─ skip: search(2, [(1,3)])    -> 70
   │  ├─ skip: search(3, [(1,3)]) -> 70
   │  │  ├─ skip: search(4, ...)  -> 0   (all jobs decided)
   │  │  └─ take j3 [3,6): shares boundary 3, allowed -> 70
   │  └─ take j2 [3,5): shares boundary 3, allowed -> 40
   │     (with [3,5) chosen, j3 [3,6) overlaps and is rejected below)
   └─ take j1 [2,4): overlaps chosen [1,3), rejected
   take j0 total = 50 + 70 = 120
```

The take-`j2` branch is the instructive one: choosing `[3,5)` still respects the boundary rule against `[1,3)`, but it then blocks `j3 = [3,6)`, so that path tops out at `90` instead of `120`. The root keeps `120`, matching the expected Output for Example 1 (jobs `j0` and `j3`, profit `50 + 70`).

#### Solution

The code is the walkthrough's take-or-skip recursion with the all-intervals overlap test.

```python
from typing import List, Tuple


class Solution:
    def solve(
        self, start_times: List[int], end_times: List[int], profits: List[int]
    ) -> int:
        """Return the maximum total profit from non-overlapping jobs.

        Time:  O(2^n * n): every job branches into take or skip, and each
            take compares the candidate against the whole chosen set.
        Space: O(n): recursion depth plus the chosen list along one path.
        """
        job_count = len(start_times)

        def search(job_idx: int, chosen: List[Tuple[int, int]]) -> int:
            if job_idx == job_count:
                return 0

            best_without = search(job_idx + 1, chosen)

            start, end, profit = (
                start_times[job_idx],
                end_times[job_idx],
                profits[job_idx],
            )
            if all(
                end <= chosen_start or chosen_end <= start
                for chosen_start, chosen_end in chosen
            ):
                best_with = profit + search(job_idx + 1, chosen + [(start, end)])
                return max(best_without, best_with)
            return best_without

        return search(0, [])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

Each job independently contributes a take-or-skip branch, so up to `2^n` selections are explored (when no jobs overlap, every subset is legal), and each take branch scans up to `n` chosen intervals for compatibility.

##### Space Complexity: `O(n)`

The recursion is at most `n` frames deep and the `chosen` list along any path holds at most `n` intervals.

#### Key Insights

- The overlap test `end <= chosen_start or chosen_end <= start` is the whole constraint; a shared boundary passes because the intervals are half-open, exactly the problem's rule.
- Checking the candidate against every chosen interval, not just the latest one, is forced by the unsorted input: jobs may be taken in a different order than they run in time.
- Correct but exponential, so this is a baseline and a testing oracle, not a submission for the stated constraint of 50,000 jobs.

### Quadratic DP

#### Derivation

The brute force explodes because the unsorted input gives the decisions no order: every path must remember every interval it committed to, so no two paths share work. Sorting the jobs by end time repairs this. Once sorted, every job that could legally precede job `i` (one ending at or before job `i` starts) sits earlier in the list, so its answer is already final, and the whole history of a path collapses into one number: the best profit from the first `i` jobs.

Let `best[position]` be the maximum profit using only the first `position` jobs in end-time order. The current job (start `start`, profit `gain`) contributes either nothing or everything since its predecessor:

- **Skip it:** the answer is `best[position - 1]`.
- **Take it:** add `gain` to the best profit from jobs finishing by `start`.

This version locates that latest non-conflicting job with a plain backward scan over the sorted end times; the next two solutions replace the scan with a search:

1. Zip `(end_times, start_times, profits)` and sort by end time.
2. Extract the sorted end times into `ends` for scanning.
3. For job `position`, walk `predecessor` left until
   `ends[predecessor - 1] <= start`.
4. Set `best[position] = max(best[position - 1], best[predecessor] + gain)`.
5. Return `best[job_count]`.

#### Recurrence

Sort the jobs so that \(\text{end}_1 \le \text{end}_2 \le \dots \le \text{end}_n\), and let \(p(i)\) be the latest job that finishes no later than job `i` starts:

$$ p(i) = \max\bigl\{\, j < i \ :\ \text{end}_j \le \text{start}_i \,\bigr\}, \qquad p(i) = 0 \ \text{ if no such job exists} $$

```text
p(i) = max { j < i : ends[j - 1] <= start of job i }   (jobs 1-indexed)
p(i) = 0   if no such j exists
```

Let `best[position]` be the maximum profit from the first `position` sorted jobs. Each job is skipped or taken:

$$ \text{best}[i] = \begin{cases} 0, & i = 0 \\[4pt] \max\bigl(\underbrace{\text{best}[i-1]}_{\text{skip}},\ \underbrace{\text{best}[p(i)] + \text{profit}_i}_{\text{take}}\bigr), & i \ge 1 \end{cases} $$

```text
best[0] = 0
best[position] = max(best[position - 1], best[predecessor] + profit)   for position >= 1
                   skip                    take
```

Taking job `i` jumps the state back to \(p(i)\), discarding every job in between: those overlap job `i` and cannot combine with it. Sorting by end time is what makes \(p(i)\) well defined and monotone; by start time would leave legal predecessors scattered on both sides. The last two solutions below differ from this one only in how they evaluate \(p(i)\).

#### Walkthrough

Fill `best` by hand on Example 1: `startTime = [1,2,3,3]`, `endTime = [3,4,5,6]`, `profit = [50,10,40,70]`. Sorting the `(end, start, gain)` triples changes nothing here, since the input already arrives in end order:

```text
setup   jobs = [(3,1,50), (4,2,10), (5,3,40), (6,3,70)]
        ends = [3, 4, 5, 6]        best = [0, 0, 0, 0, 0]

i=1  (end=3, start=1, gain=50)   predecessor = 0 (empty window, scan guard fails)
     best[1] = max(best[0]=0, best[0]+50=50) = 50
i=2  (end=4, start=2, gain=10)   scan: ends[1]=4 > 2 -> predecessor=1;
                                 ends[0]=3 > 2 -> predecessor=0
     best[2] = max(50, best[0]+10=10) = 50
i=3  (end=5, start=3, gain=40)   scan: ends[1]=4 > 3 -> predecessor=1;
                                 ends[0]=3 <= 3 stop
     best[3] = max(50, best[1]+40=90) = 90
i=4  (end=6, start=3, gain=70)   scan: ends[2]=5 > 3 -> 2; ends[1]=4 > 3 -> 1;
                                 ends[0]=3 <= 3 stop
     best[4] = max(90, best[1]+70=120) = 120
```

The scan's stopping test is strict (`> start`), so an end time equal to the start passes: at `i=3` and `i=4` the first job, ending at `3`, counts as a legal predecessor of jobs starting at `3`, which is the shared-boundary rule. The winning take at `i=4` pairs the fourth job with `best[1] = 50`: profit `50 + 70 = 120`, matching the expected Output. (Example 3, where all jobs overlap, drives every scan back to `predecessor = 0` and returns `best[3] = 6`, the best single job.)

#### Solution

The code is the walkthrough's loop: sort, scan left for `predecessor`, then the skip/take maximum.

```python
from typing import List


class Solution:
    def solve(
        self, start_times: List[int], end_times: List[int], profits: List[int]
    ) -> int:
        """Return the maximum total profit from non-overlapping jobs.

        Time:  O(n^2): sorting is O(n log n) and each of the n DP steps may
            scan back across up to n earlier jobs.
        Space: O(n): the sorted jobs, the end-time array, and the DP array.
        """
        jobs = sorted(zip(end_times, start_times, profits))
        ends = [job_end for job_end, _, _ in jobs]

        job_count = len(jobs)
        best = [0] * (job_count + 1)

        for position in range(1, job_count + 1):
            _, start, profit = jobs[position - 1]

            predecessor = position - 1
            while predecessor > 0 and ends[predecessor - 1] > start:
                predecessor -= 1

            best[position] = max(best[position - 1], best[predecessor] + profit)

        return best[job_count]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Sorting costs `O(n log n)`; the DP loop runs `n` times and each backward scan may walk across up to `n` earlier jobs, which dominates the bound.

##### Space Complexity: `O(n)`

The sorted `jobs` list, the `ends` array, and the `best` array each hold one entry per job.

#### Key Insights

- Sorting by end time is the linchpin: it guarantees every legal predecessor of a job lies to its left, so a single index summarizes everything decided so far.
- `best` is non-decreasing, so `best[predecessor]` already folds in every compatible earlier job, not just job `predecessor` itself.
- The quadratic cost sits entirely in the predecessor scan, which is exactly the piece the next solution replaces.

### DP with Manual Binary Search

#### Derivation

The DP is unchanged from the Quadratic DP: sort by end time, then for each job take the better of skipping it or pairing it with the best compatible prefix. The flaw is the lookup: the backward scan walks a sorted array one step at a time, paying `O(n)` for an answer the ordering could give in `O(log n)`. Because `ends` is sorted ascending, a hand-written [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) for the first index whose end time exceeds `start` returns exactly the count of jobs ending at or before `start`, which is the predecessor's `best` slot. The search window is capped at `[0, position - 1)` so the current job never searches past its own position:

1. Sort, extract `ends`, and allocate `best`, exactly as before.
2. For each job `position`, search with `low, high = 0, position - 1`:
   probe `middle = low + (high - low) // 2`, move `low = middle + 1` when
   `ends[middle] <= start`, otherwise `high = middle`.
3. When `low == high`, `low` is the count of compatible jobs and thus the
   predecessor's `best` index.
4. Set `best[position] = max(best[position - 1], best[low] + profit)` and
   return `best[job_count]`.

#### Walkthrough

Re-run Example 1 with the probes spelled out: `jobs = [(3,1,50), (4,2,10), (5,3,40), (6,3,70)]`, `ends = [3, 4, 5, 6]`. Each probe tests `ends[middle] <= start` and discards half the window:

```text
i=1  start=1   low=0, high=0   window empty, loop skipped        -> predecessor=0
     best[1] = max(0, best[0]+50=50) = 50
i=2  start=2   low=0, high=1
     probe middle=0: ends[0]=3 <= 2? no  -> high=0              -> predecessor=0
     best[2] = max(50, 10) = 50
i=3  start=3   low=0, high=2
     probe middle=1: ends[1]=4 <= 3? no  -> high=1
     probe middle=0: ends[0]=3 <= 3? yes -> low=1               -> predecessor=1
     best[3] = max(50, best[1]+40=90) = 90
i=4  start=3   low=0, high=3
     probe middle=1: ends[1]=4 <= 3? no  -> high=1
     probe middle=0: ends[0]=3 <= 3? yes -> low=1               -> predecessor=1
     best[4] = max(90, best[1]+70=120) = 120
```

The searches land on the same predecessors the backward scans found, but the probe at `i=4` discards `ends[1]` and `ends[2]` in a single comparison instead of stepping over each. The `ends[0] = 3 <= start = 3` probe moving `low` past index `0` is the shared-boundary rule at work: the job ending at `3` counts as a legal predecessor of one starting at `3`. The function returns `best[4] = 120`, matching the expected Output.

#### Solution

The code is the Quadratic DP with the backward scan replaced by the walkthrough's probe loop.

```python
from typing import List


class Solution:
    def solve(
        self, start_times: List[int], end_times: List[int], profits: List[int]
    ) -> int:
        """Return the maximum total profit from non-overlapping jobs.

        Time:  O(n log n): sorting is O(n log n) and each of the n DP steps
            performs one O(log n) binary search.
        Space: O(n): the sorted jobs, the end-time array, and the DP array.
        """
        jobs = sorted(zip(end_times, start_times, profits))
        ends = [job_end for job_end, _, _ in jobs]

        job_count = len(jobs)
        best = [0] * (job_count + 1)

        for position in range(1, job_count + 1):
            _, start, profit = jobs[position - 1]

            low, high = 0, position - 1
            while low < high:
                middle = low + (high - low) // 2
                if ends[middle] <= start:
                    low = middle + 1
                else:
                    high = middle
            predecessor = low

            best[position] = max(best[position - 1], best[predecessor] + profit)

        return best[job_count]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting costs `O(n log n)`; the DP loop runs `n` times and each iteration performs one `O(log n)` search, contributing another `O(n log n)`.

##### Space Complexity: `O(n)`

The sorted `jobs` list, the `ends` array, and the `best` array each hold one entry per job.

#### Key Insights

- Searching for the first end time strictly greater than `start` yields the count of compatible jobs, which doubles as the predecessor's `best` index: no separate pointer bookkeeping exists.
- Computing `middle` as `low + (high - low) // 2` is the overflow-safe midpoint form, worth keeping as a habit even though Python integers do not overflow.
- The half-open window `[0, position - 1)` is what stops the current job from pairing with itself or with a same-end-time job that sorts later.

### DP with bisect

#### Derivation

The DP is identical to the two versions above; the only change is who owns the search. The hand-written probe loop implements exactly one operation, the insertion point of `start` in the sorted `ends` array just past every entry `<= start`, and [`bisect.bisect_right`](https://docs.python.org/3/library/bisect.html) is the standard library's implementation of that operation. Passing `0` and `position - 1` as the bounds confines the lookup to the already-decided window `[0, position - 1)` without slicing, so the call returns the same predecessor index the manual loop converged on:

1. Sort, extract `ends`, and allocate `best`, exactly as before.
2. For each job `position`, set
   `predecessor = bisect.bisect_right(ends, start, 0, position - 1)`: the
   count of windowed jobs ending at or before `start`.
3. Set `best[position] = max(best[position - 1], best[predecessor] + profit)`
   and return `best[job_count]`.

#### Walkthrough

Re-run Example 1 once more: `ends = [3, 4, 5, 6]`. Internally `bisect_right` runs the mirror image of the manual search's probes, testing `start < ends[middle]` at the same midpoints:

```text
i=1  bisect_right(ends, 1, 0, 0)   window empty                       -> 0
     best[1] = max(0, best[0]+50=50) = 50
i=2  bisect_right(ends, 2, 0, 1)   probe middle=0: 2 < 3 -> high=0    -> 0
     best[2] = max(50, 10) = 50
i=3  bisect_right(ends, 3, 0, 2)   probe middle=1: 3 < 4 -> high=1
                                   probe middle=0: 3 < 3? no -> low=1 -> 1
     best[3] = max(50, best[1]+40=90) = 90
i=4  bisect_right(ends, 3, 0, 3)   probe middle=1: 3 < 4 -> high=1
                                   probe middle=0: 3 < 3? no -> low=1 -> 1
     best[4] = max(90, best[1]+70=120) = 120
```

Each call returns the same index the hand-written loop converged on, because `start < ends[middle]` failing is exactly `ends[middle] <= start` succeeding; the boundary equality at `3` again moves the insertion point past index `0`. With the search delegated, only the recurrence remains in view, and the function returns `best[4] = 120`, matching the expected Output.

#### Solution

The code is the previous solution with the probe loop delegated to `bisect_right`.

```python
import bisect
from typing import List


class Solution:
    def solve(
        self, start_times: List[int], end_times: List[int], profits: List[int]
    ) -> int:
        """Return the maximum total profit from non-overlapping jobs.

        Time:  O(n log n): sorting is O(n log n) and each of the n DP steps
            performs one O(log n) bisect_right call.
        Space: O(n): the sorted jobs, the end-time array, and the DP array.
        """
        jobs = sorted(zip(end_times, start_times, profits))
        ends = [job_end for job_end, _, _ in jobs]

        job_count = len(jobs)
        best = [0] * (job_count + 1)

        for position in range(1, job_count + 1):
            _, start, profit = jobs[position - 1]

            predecessor = bisect.bisect_right(ends, start, 0, position - 1)

            best[position] = max(best[position - 1], best[predecessor] + profit)

        return best[job_count]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting costs `O(n log n)`; the DP loop runs `n` times and each iteration performs one `O(log n)` `bisect_right` call.

##### Space Complexity: `O(n)`

The sorted `jobs` list, the `ends` array, and the `best` array each hold one entry per job.

#### Key Insights

- `bisect_right` returns the count of compatible jobs directly, so no manual bound tracking or off-by-one reasoning survives in the code.
- The `lo`/`hi` bounds `(0, position - 1)` confine the search without slicing, so no temporary copies are created.
- This is the idiomatic Python form and the right submission for the stated constraint of 50,000 jobs; the library handles the search that the earlier approaches spell out by hand.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^n × n)` - every job branches into take or skip, and each take scans the chosen set for overlap.
- **Quadratic DP**: `O(n^2)` - the per-job backward scan dominates after the initial sort.
- **DP with Manual Binary Search**: `O(n log n)` - each predecessor lookup drops to logarithmic, matching the sort cost.
- **DP with bisect**: `O(n log n)` - identical to the manual search, with the lookup delegated to `bisect_right`.

### Space Complexity

- **Brute Force**: `O(n)` - recursion stack plus the chosen intervals along one path.
- **Quadratic DP**: `O(n)` - sorted jobs, end times, and the DP array.
- **DP with Manual Binary Search**: `O(n)` - identical auxiliary storage.
- **DP with bisect**: `O(n)` - identical auxiliary storage.

### Trade-offs

- **Brute Force**: the direct transcription of the selection rule and a useful oracle, but exponential time restricts it to a handful of jobs.
- **Quadratic DP**: the easiest DP to read and verify, with no index arithmetic to get wrong, but the linear scan is wasteful on a sorted array.
- **DP with Manual Binary Search**: scales to the full constraint range, at the price of window and boundary reasoning that is easy to get subtly wrong.
- **DP with bisect**: same speed as the manual search while hiding the boundary details in the standard library, leaving only the recurrence to read.

### When to Use Each

- **Brute Force**: as the correctness oracle for checking the faster versions on small inputs, and as the spoken first step in an interview.
- **Quadratic DP**: for small inputs or when teaching the recurrence; the scan makes the predecessor concept visible.
- **DP with Manual Binary Search**: when the search must be understood explicitly or ported to a language without a standard binary-search helper.
- **DP with bisect (Recommended)**: the interview default and the right submission for `n` up to `5 × 10^4`: shortest correct form, standard library owned.

### Optimization Notes

- The three DP solutions share one setup and one recurrence; only the predecessor lookup changes, which makes them easy to diff against each other while debugging.
- The half-open interval convention does the boundary work: `bisect_right` (equivalently, the strict `ends[middle] <= start` test) admits a job ending exactly at the next job's start, as Example 1's boundary at time `3` shows.
- Because `best` is non-decreasing, no separate prefix-maximum array is needed; `best[predecessor]` already reflects the best of all compatible earlier jobs.
- `sorted(zip(end_times, start_times, profits))` sorts ties by start time and then profit, which never affects correctness here: equal end times are mutually overlapping, so at most one of them can be taken and the recurrence's skip branch covers the rest.
