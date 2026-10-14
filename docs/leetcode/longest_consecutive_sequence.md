# [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)

**Medium** | **25 minutes** | **Array, Hash Table, Union Find**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/longest_consecutive_sequence/solution.py`](../../practice/longest_consecutive_sequence/solution.py)

Given an array of integers `nums`, return *the length* of the longest consecutive sequence of elements that can be formed.

A *consecutive sequence* is a sequence of elements in which each element is exactly `1` greater than the previous element. The elements do *not* have to be consecutive in the original array.

You must write an algorithm that runs in `O(n)` time.

## Examples

### Example 1

**Input:** `nums = [2,20,4,10,3,4,5]`

**Output:** `4`

**Explanation:** The longest consecutive sequence is `[2, 3, 4, 5]`.

### Example 2

**Input:** `nums = [0,3,2,5,4,6,1,1]`

**Output:** `7`

## Constraints

- `0 <= nums.length <= 100,000`
- `-10^9 <= nums[i] <= 10^9`

## Deriving the Solution

The input is an unordered bag, but the question is about *runs* of consecutive values, a property of the sorted universe the values inhabit. Every solution below must in effect discover where each value's run begins and ends; they differ in how much of the sorting work they actually perform.

1. **Start literal.** Sort the values and sweep, counting the current run and resetting at each gap. Correct and simple, but sorting is `O(n log n)` and the problem demands `O(n)`: see [Sort and Sweep](#sort-and-sweep).
2. **Spot the waste.** Sorting spends `log n` on ordering values whose relative order mostly does not matter: only the *neighbor existence* questions (`is x + 1 present?`) define runs, and existence is exactly what a hash set answers in `O(1)`.
3. **Ask set questions instead.** Put all values in a set. Walking every value's run forward is still `O(n²)` in the worst case, because the same run is re-walked once per member: see [Set Walk from Every Number](#set-walk-from-every-number).
4. **Walk each run once.** The repair is a single guard: walk forward only from values with no predecessor in the set, the run starts. Every value is then visited at most twice overall, and the algorithm meets the `O(n)` bound: see [Sequence Start Detection](#sequence-start-detection).

## Solutions

### Sort and Sweep

#### Derivation

Runs are easiest to see in sorted order, where every run is a contiguous block and a run boundary is exactly a place where the next value is not the previous value plus one. So sort, then sweep once, carrying the length of the run currently under the cursor:

1. Handle the empty input by returning `0`.
2. Sort a copy of `nums`.
3. Walk the sorted values, tracking `current_length` for the run in progress.
4. When `value == previous + 1`, extend `current_length`; when `value == previous`, it is a duplicate, skip it; otherwise a gap intervenes and `current_length` resets to `1`.
5. Track the maximum seen in `longest` and return it.

#### Walkthrough

Trace the sweep on Example 1: `nums = [2,20,4,10,3,4,5]`, which sorts to `[2,3,4,4,5,10,20]`:

```text
value 2   current_length = 1   longest = 1
value 3   3 == 2 + 1 -> extend   current_length = 2   longest = 2
value 4   4 == 3 + 1 -> extend   current_length = 3   longest = 3
value 4   duplicate of previous -> skip
value 5   5 == 4 + 1 -> extend   current_length = 4   longest = 4
value 10  gap after 5            current_length = 1
value 20  gap after 10           current_length = 1
```

The longest run measured is `4`, matching Example 1's expected Output. Example 2 sorts to `[0,1,2,3,4,5,6,6]`; the sweep runs unbroken from `0` to `6` (skipping the duplicate `6`) and reports `7`, matching its expected Output.

#### Solution

The code is the sorted sweep with its three cases: extend, duplicate, gap.

```python
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        longest = 1
        current_length = 1
        values = sorted(nums)
        for index in range(1, len(values)):
            value = values[index]
            previous = values[index - 1]
            if value == previous + 1:
                current_length += 1
            elif value != previous:
                current_length = 1
            longest = max(longest, current_length)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; the sweep that follows is a single linear pass.

##### Space Complexity: `O(n)`

`sorted` materializes a new list of `n` values.

#### Key Insights

- Sorting turns the fuzzy notion of "consecutive elements somewhere in the array" into contiguous blocks with local adjacency checks.
- The duplicate case must be skipped *without* resetting the counter, a classic sorting-sweep subtlety that Example 2's repeated `1` exercises.
- Fails the problem's `O(n)` requirement, but remains the honest baseline every set-based design is measured against.

### Set Walk from Every Number

#### Derivation

The `O(n)` demand rules out sorting, but the only questions runs really ask are membership questions: is `value + 1` present? And the [hash set](https://en.wikipedia.org/wiki/Hash_table) answers those in `O(1)` average time. The first set-based design is the unguarded one: put every value in a set, and for each number walk forward while the next value exists, counting as you go:

1. Build `numbers`, a set of all values (duplicates collapse for free).
2. For each `num` in the set, start `length` at `1`.
3. While `num + length` is in the set, increment `length`.
4. Track the maximum in `longest` and return it.

The flaw is invisible until the cost model is applied: every member of a run of length `L` walks the same run, doing `O(L)` work each, so a single run of length `n` costs `O(n²)`.

#### Walkthrough

Trace the per-number walks on a tailored small input (Example 1's full trace would repeat the same run four times): `nums = [1, 2, 3]`:

```text
set = {1, 2, 3}

num = 1   walk: 2 in set -> 3 in set -> 4 absent   length = 3
num = 2   walk: 3 in set -> 4 absent               length = 2
num = 3   walk: 4 absent                           length = 1
```

The maximum is `3`, the correct answer, but the walk re-counted the same run once per member: `3 + 2 + 1` steps for a run of length `3`. On one long run of length `n` this shape costs `n(n+1)/2` steps, which is `O(n²)` and misses the requirement.

#### Solution

The code is the unguarded walk: correct on every input, quadratic on the adversarial one.

```python
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numbers = set(nums)
        longest = 0
        for num in numbers:
            length = 1
            while num + length in numbers:
                length += 1
            longest = max(longest, length)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Building the set is `O(n)`, but a run of length `L` is re-walked by each of its `L` members, so one long run costs `O(n²)` in the worst case.

##### Space Complexity: `O(n)`

The set holds every distinct value.

#### Key Insights

- Membership queries replace ordering entirely, which is the right primitive for run detection.
- The design is *almost* linear: on randomly scattered inputs it behaves well, which is exactly what makes the quadratic worst case dangerous.
- The set already solved duplicates and the empty-input case for free; the remaining problem is purely the repeated work.

### Sequence Start Detection

#### Derivation

The quadratic blow-up has one cause: a run of length `L` is walked from all `L` of its starting points instead of one. But the set itself knows where the true start is: a value `num` begins a run exactly when `num - 1` is *absent* from the set, because nothing extends the run to its left. Guarding the walk on that condition means each run is walked once, from its head, and the work per run is `O(L)` for a run of length `L`. Since runs partition the distinct values, the total walk work is `O(n)`:

1. Build `numbers`, a set of all values.
2. For each `num` in the set, skip it when `num - 1` is in the set (not a run start).
3. Otherwise walk forward with `length = 1`, advancing while `num + length` is in the set.
4. Track the maximum in `longest` and return it.

#### Walkthrough

Trace the guarded sweep on Example 1: `nums = [2,20,4,10,3,4,5]`, whose set is `{2, 3, 4, 5, 10, 20}`:

```text
num = 2    1 absent  -> run start
           walk: 3, 4, 5 present; 6 absent   length = 4   longest = 4
num = 3    2 present -> skip
num = 4    3 present -> skip
num = 5    4 present -> skip
num = 10   9 absent  -> run start
           walk: 11 absent                    length = 1
num = 20   19 absent -> run start
           walk: 21 absent                    length = 1
```

Only three values are ever walked, each from the head of its run, and the walk work totals `4 + 1 + 1` steps rather than one walk per value. The maximum `4` matches Example 1's expected Output. Example 2's set `{0,1,2,3,4,5,6}` has the single run start `0`, one walk of length `7`, and returns `7`, matching its expected Output. The guard also survives the adversarial case that sank the previous design: on `[1, 2, ..., n]` only `1` is a start, so one `O(n)` walk replaces `n` of them.

#### Solution

The code is the guarded walk: one membership test before each walk, one forward walk per run.

```python
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numbers = set(nums)
        longest = 0
        for num in numbers:
            if num - 1 in numbers:
                continue
            length = 1
            while num + length in numbers:
                length += 1
            longest = max(longest, length)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the set is `O(n)`. The guard ensures every value is visited at most twice overall: once by the outer loop and once by the inner walk of its run, so the walk phase is linear despite the nested-loop shape.

##### Space Complexity: `O(n)`

The set holds every distinct value.

#### Key Insights

- The single guard `num - 1 not in numbers` converts a quadratic walk into a linear one by making each run's cost `O(L)` instead of `O(L²)`.
- Hash sets buy `O(1)` membership without ordering, which is exactly the primitive this problem needs and sorting over-supplies.
- The nested loop is not automatically quadratic: analyze *total* work across all inner iterations, not per-outer-iteration work.

## Comparison of Solutions

### Time Complexity

- **Sort and Sweep**: `O(n log n)` - sorting dominates the linear sweep.
- **Set Walk from Every Number**: `O(n²)` worst case - each member of a run re-walks it.
- **Sequence Start Detection**: `O(n)` - each value is walked at most once from its run's head.

### Space Complexity

- **Sort and Sweep**: `O(n)` - a sorted copy of the values.
- **Set Walk from Every Number**: `O(n)` - the set of distinct values.
- **Sequence Start Detection**: `O(n)` - the set of distinct values.

### Trade-offs

- **Sort and Sweep** needs no hashing and its correctness is immediate, but it misses the stated complexity requirement by a log factor.
- **Set Walk from Every Number** adopts the right primitive (membership) but pays repeatedly for the same run.
- **Sequence Start Detection** adds one guard to the walk and meets the `O(n)` bound; the only price is trusting the amortized argument that runs partition the values.

### When to Use Each

- **Sort and Sweep**: when hashing is unavailable or input is already (nearly) sorted.
- **Set Walk from Every Number**: as a stepping stone; its flaw motivates the final design and is the interview's key teaching moment.
- **Sequence Start Detection**: the answer to the problem as stated (recommended here).

### Optimization Notes

- The `while num + length in numbers` loop never rebuilds what it looks up: keeping the set outside the loop and growing `length` is what keeps each run's walk at `O(L)`.
- Iterating the set rather than the input list means duplicates are visited once, not once per copy; Example 2's repeated `1` never matters.
- Values spanning the full `±10^9` range change nothing: the set is keyed by value, not by a value-sized array, which is why this beats a counting-array design here.
