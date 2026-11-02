# [Longest Equal-Value Run](https://www.fastprep.io/problems/amazon-longest-equal-value-run)

**Easy** | **NN minutes** | **Array**

Given an integer array nums, return the length of its longest contiguous run of equal values.

## Examples

### Example 1

**Input:** `nums = [4,4,2,2,2,4]`

**Output:** `3`

**Explanation:** The maximal runs are [4,4], [2,2,2], and [4], with lengths 2, 3, and 1. The answer is 3.

## Constraints

- `For this exercise, assume 0 <= nums.length <= 100000.`
- `Every element of nums is an integer.`
- `An empty array is a valid input and returns 0.`

## Deriving the Solution

The array decomposes into maximal runs of equal values, separated exactly where a value differs from its predecessor, and the answer is the length of the longest run. Everything below is a strategy for measuring those runs without doing redundant work:

1. **Start literal.** From every position, extend a run as far right as the equal values reach, and keep the longest measurement. Correct, but each run is measured once per position it contains: see [Brute Force Run Rescan](#brute-force-run-rescan).
2. **Measure each run once.** A single walk can extend the running measurement while values repeat and restart it when they differ, so every element is touched exactly once: see [Single-Pass Run Counter](#single-pass-run-counter).
3. **Hand the grouping to the standard library.** Grouping consecutive equal values is `itertools.groupby`'s job; the run lengths fall out of the groups: see [Run-Length Groups with itertools.groupby](#run-length-groups-with-itertoolsgroupby).

## Solutions

### Brute Force Run Rescan

#### Derivation

The statement's most literal reading: a run is a maximal stretch of equal values, so try to start a run at every position, extend it rightward while the values stay equal, and remember the longest extension. The extension loop is the statement's definition of a run, applied once per candidate start:

1. Return 0 immediately for an empty array (the statement grants it with
   an expected answer of 0); otherwise set `longest_run = 1`, since any
   non-empty array has a run of length 1.
2. For each `start`, advance `run_end` from `start` while
   `nums[run_end + 1] == nums[run_end]`.
3. Update `longest_run` with the stretch length `run_end - start + 1`.
4. Return `longest_run` after every start has been tried.

#### Walkthrough

Example 1, `nums = [4, 4, 2, 2, 2, 4]`. Each start's extension is one row; the maximal runs are visible as the repeated measurements:

```text
start 0 (4)   extends over index 1        length 2
start 1 (4)   extends to index 1          length 1
start 2 (2)   extends over index 3, 4     length 3
start 3 (2)   extends over index 4        length 2
start 4 (2)   stops immediately           length 1
start 5 (4)   stops immediately           length 1
```

The largest measurement is 3, matching the expected Output. The rescan is visible in the rows: the run [2, 2, 2] is measured three times, once per position inside it.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        if not nums:
            return 0
        longest_run = 1
        for start in range(len(nums)):
            run_end = start
            while run_end + 1 < len(nums) and nums[run_end + 1] == nums[run_end]:
                run_end += 1
            longest_run = max(longest_run, run_end - start + 1)
        return longest_run
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

A run of length `L` is re-extended from each of its `L` positions, so an array of one giant run costs `n + (n-1) + ... = O(n^2)` comparisons.

##### Space Complexity: `O(1)`

Only the `start`, `run_end`, and `longest_run` locals live across iterations.

#### Key Insights

- The extension loop is the definition of a run, which makes this version almost impossible to get wrong and a good baseline to state first.
- The redundancy is measurable: every element inside a run of length `L` is compared `L` times before the scan moves on.
- The answer is at least 1 for any non-empty array, which the `longest_run = 1` seed encodes; the granted empty array is answered by the early return, keeping the loop free of special cases.

### Single-Pass Run Counter

#### Derivation

The Brute Force re-measures a run once per element inside it, but a single walk can carry the measurement forward: `current_run` counts the run ending at the previous element, so an element equal to its predecessor extends that same run, and any different value proves the previous run ended and restarts the count. The maximum is updated the moment a run grows, so nothing is measured twice:

1. Return 0 immediately for an empty array (the statement grants it with
   an expected answer of 0); otherwise seed `current_run = 1` and
   `longest_run = 1` for the first element.
2. For each `index` from 1 onward: when `nums[index] == nums[index - 1]`,
   increment `current_run` and raise `longest_run` to match if larger.
3. Otherwise reset `current_run` to 1; the run ending at `index` starts over.
4. Return `longest_run` after the walk.

#### Walkthrough

Example 1, `nums = [4, 4, 2, 2, 2, 4]`, one row per element with `(current_run, longest_run)` after it:

```text
index 0 (4)   seed                          current_run = 1, longest_run = 1
index 1 (4)   equal    -> extend            current_run = 2, longest_run = 2
index 2 (2)   differs  -> restart           current_run = 1, longest_run = 2
index 3 (2)   equal    -> extend            current_run = 2, longest_run = 2
index 4 (2)   equal    -> extend            current_run = 3, longest_run = 3
index 5 (4)   differs  -> restart           current_run = 1, longest_run = 3
```

The final `longest_run = 3` matches the expected Output: the [2, 2, 2] run was measured exactly once, as it grew.

#### Solution

The code is the walkthrough's extend-or-restart branch, applied once per element.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        if not nums:
            return 0
        longest_run = 1
        current_run = 1
        for index in range(1, len(nums)):
            if nums[index] == nums[index - 1]:
                current_run += 1
                longest_run = max(longest_run, current_run)
            else:
                current_run = 1
        return longest_run
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One predecessor comparison per element, with a constant-time branch and at most one `max` call per element.

##### Space Complexity: `O(1)`

Two counters, regardless of the array's size or run structure.

#### Key Insights

- Extending versus restarting is decided by exactly one comparison, `nums[index] == nums[index - 1]`; run boundaries never need to be found explicitly.
- Raising `longest_run` inside the extend branch (rather than after the loop) means the maximum is always current and no second pass is needed.
- The restart branch needs no `max`: a freshly started run of length 1 can only beat `longest_run` when the array is a single element, which the seed already covers.

### Run-Length Groups with itertools.groupby

#### Derivation

The Single-Pass counter maintains run lengths by hand, but grouping consecutive equal values is precisely what [`itertools.groupby`](https://docs.python.org/3/library/itertools.html#itertools.groupby) does: it yields one group per maximal run, in order. Measuring each group's length and taking the maximum expresses the whole solution as one aggregation, with the run-splitting bookkeeping handed to the standard library:

1. Group `nums` with `groupby`; each `(value, group)` pair is one maximal run.
2. Measure each group with `len(list(group))`.
3. Return the `max` group length, with `default=0` answering the
   granted empty input.

#### Walkthrough

Example 1, `nums = [4, 4, 2, 2, 2, 4]`, one row per group:

```text
group 1   value 4, positions 0-1     length 2
group 2   value 2, positions 2-4     length 3
group 3   value 4, position 5        length 1
```

The maximum group length is 3, matching the expected Output. Note the two 4-groups stay separate: `groupby` groups consecutive equals only, so the non-adjacent repeat of 4 does not merge.

#### Solution

```python
from itertools import groupby
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        return max((len(list(group)) for _, group in groupby(nums)), default=0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`groupby` yields each element once, and measuring a group is one pass over it.

##### Space Complexity: `O(L)`

Each materialized group holds at most the longest run's length `L` at one time; the running maximum is constant.

#### Key Insights

- `groupby` splits consecutive equal values, not equal values in general, which is exactly the run semantics the problem asks for.
- The one-liner is the Single-Pass counter with its bookkeeping renamed: correctness rests on the same grouping, so it is worth writing the counter first to know what `groupby` is doing.
- A group must be consumed (here with `list`) before the iterator advances; relying on lazy groups inside `max` is a classic way to measure zeros.

## Comparison of Solutions

### Time Complexity

- **Brute Force Run Rescan**: `O(n^2)` - every run is re-extended from each position inside it.
- **Single-Pass Run Counter**: `O(n)` - one comparison per element, no run measured twice.
- **Run-Length Groups with itertools.groupby**: `O(n)` - the library yields each element once.

### Space Complexity

- **Brute Force Run Rescan**: `O(1)` - loop locals only.
- **Single-Pass Run Counter**: `O(1)` - two counters.
- **Run-Length Groups with itertools.groupby**: `O(L)` - one materialized group at a time.

### Trade-offs

- **Brute Force Run Rescan**: transcribes the definition directly and survives any run structure, but pays quadratically on run-heavy inputs.
- **Single-Pass Run Counter**: linear time, constant space, and every line of it is the problem's own logic.
- **Run-Length Groups with itertools.groupby**: the shortest expression, delegating the grouping; it hides the extend-or-restart decision inside a library call.

### When to Use Each

- **Brute Force Run Rescan**: as the baseline to state and test against, or when the input is tiny and throwaway.
- **Single-Pass Run Counter (Recommended)**: the answer to give in an interview: linear, constant space, and easy to prove with the extend-or-restart argument.
- **Run-Length Groups with itertools.groupby**: in Python, once the counter is established, as the tidy idiomatic form.

### Optimization Notes

- **Single-Pass Run Counter** is the recommended choice: it touches each element exactly once and carries no per-run overhead.
- The whole problem is a special case of run-length encoding: if follow-ups ask *which* value runs longest or *where*, the same walk records the run's value and start index alongside its length.
- The statement grants the empty array with an expected answer of 0, so every approach answers it explicitly: an early return in the two loop forms, `default=0` on the `max` over `groupby`.
