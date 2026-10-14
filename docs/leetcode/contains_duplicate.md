# [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)

**Easy** | **10 minutes** | **Array, Hash Table, Sorting**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm)

**Practice:** [`practice/contains_duplicate/solution.py`](../../practice/contains_duplicate/solution.py)

Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.

## Examples

### Example 1

**Input:** `nums = [1,2,3,1]`

**Output:** `true`

**Explanation:** The value `1` appears twice in the array.

### Example 2

**Input:** `nums = [1,2,3,4]`

**Output:** `false`

**Explanation:** All elements in the array are distinct.

### Example 3

**Input:** `nums = [1,1,1,3,3,4,3,2,4,2]`

**Output:** `true`

**Explanation:** The array contains multiple duplicate values.

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

## Deriving the Solution

A duplicate exists exactly when some value is seen a second time, so every solution is a strategy for answering "have I seen this value before?": by re-scanning, by remembering, or by rearranging.

1. **Start literal.** Compare every element against every other element and
   report the first match. Correct with no extra memory, but there are `n * (n - 1) / 2` pairs, so it costs `O(n^2)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Each new element is re-compared against the same prefix
   the previous elements already scanned; the answer to "was this value seen?" is re-derived from scratch every time instead of being remembered.
3. **Remember instead.** Keep the values seen so far in a hash set, where
   membership is an `O(1)` average lookup. One pass answers the question in `O(n)` time at the cost of `O(n)` space: see [Hash Set](#hash-set).
4. **Rearrange instead.** Sorting places equal values next to each other, so a
   single adjacent-pair scan finds any duplicate. That trades the hash memory for an `O(n log n)` sort: see [Sorting](#sorting).
5. **Delegate to the library.** The same hash idea can be handed entirely to
   built-ins: construct a `set` and compare sizes, or tally frequencies with `Counter` and look for a count above one. These rank last because the library does the core work: see [Set Length Comparison](#set-length-comparison) and [Counter](#counter).

## Solutions

### Brute Force

#### Derivation

The most direct idea is to compare every pair of elements and report the first match:

1. For each index `i`, compare `nums[i]` against every later element `nums[j]` with `j > i`.
2. If any pair is equal, a duplicate exists, so return `True` immediately.
3. If no pair matches after checking all combinations, every element is distinct, so return `False`.

Pairing `i` with only the indices after it avoids comparing an element to itself and avoids checking the same pair twice. This requires no extra data structures: just two nested loops.

#### Walkthrough

Trace the Brute Force solution on Example 1: `nums = [1,2,3,1]`. The outer loop fixes `i`, and the inner loop walks every later index `j` looking for a match. Each row shows one comparison of `nums[i]` against `nums[j]`:

| Step | `i` | `nums[i]` | `j` | `nums[j]` | `nums[i] == nums[j]`? | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `0` | `1` | `1` | `2` | no | keep scanning |
| 2 | `0` | `1` | `2` | `3` | no | keep scanning |
| 3 | `0` | `1` | `3` | `1` | yes | return `True` |

At step 3 the element at index `0` (value `1`) matches the element at index `3` (value `1`), so the code hits `return True` immediately and never examines `i = 1` or `i = 2`. The returned value is `True`, which matches the expected Output for Example 1.

#### Solution

The code is the walkthrough's pair scan written down: two nested loops and an equality test.

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] == nums[j]:
                    return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every pair of indices is examined in the worst case, and there are roughly `n^2 / 2` such pairs, giving quadratic time.

##### Space Complexity: `O(1)`

Only a couple of loop counters are used; no storage grows with the input.

#### Key Insights

- The most self-evident approach: check every pair directly with no auxiliary structure.
- Constant extra space, but the quadratic time makes it too slow for the upper constraint of `10^5` elements.
- Starting `j` at `i + 1` avoids redundant and self comparisons.

### Hash Set

#### Derivation

The brute force forgets everything between iterations: element `i` re-scans the same prefix that elements before it already scanned. The repair is to remember. If the values seen so far live in a [hash set](https://en.wikipedia.org/wiki/Hash_table), the question "was this value seen before?" becomes a single membership test, constant time on average, and one pass over the array settles the whole problem:

1. Initialize an empty set `seen`.
2. Iterate through `nums`. For each `num`, check whether it is already in `seen`.
3. If it is, a duplicate exists, so return `True` immediately.
4. Otherwise add `num` to `seen` and continue.
5. If the loop finishes without a hit, every element was distinct, so return `False`.

Membership tests and insertions on a hash set are constant time on average, which keeps the whole scan linear. The early return means the work stops the moment the first duplicate appears.

#### Walkthrough

Trace the scan on Example 1: `nums = [1,2,3,1]`. Each line shows one element and the state of `seen` after handling it:

```text
num = 1   not in seen -> add it     seen = {1}
num = 2   not in seen -> add it     seen = {1, 2}
num = 3   not in seen -> add it     seen = {1, 2, 3}
num = 1   in seen -> return True
```

The second `1` is caught by a single membership test against `seen`, with no re-scan of the earlier elements. The function returns `True`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's loop: test membership, then insert.

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each element is processed once, and each set lookup and insertion is `O(1)` on average, giving `O(n)` total.

##### Space Complexity: `O(n)`

In the worst case (all distinct values), the set grows to hold every element.

#### Key Insights

- A hash set turns the "have I seen this before" question into an `O(1)` average operation.
- The early return avoids scanning the rest of the array once a duplicate is found.
- The logic is library-free: a plain `set` and a loop are all that is required.

### Sorting

#### Derivation

The Hash Set spends `O(n)` extra memory to remember what it has seen. When that memory is the constraint, rearrange the array instead: [sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) brings equal values next to each other, so any duplicate, however far apart its occurrences started, ends up as an adjacent pair. One scan comparing neighbors then decides the question:

1. Sort a copy of `nums` into ascending order.
2. Walk from the second element to the last, comparing each element with its predecessor.
3. If any adjacent pair is equal, return `True`.
4. If no adjacent pair matches, return `False`.

This trades the extra hash-set memory for the cost of sorting. It is useful when auxiliary space is constrained and the input may be sorted in place.

#### Walkthrough

Trace the technique on Example 1: `nums = [1,2,3,1]`. Sorting is the core of this approach, and its effect is what matters: the two `1`s, originally at indices `0` and `3`, become neighbors:

```text
sorted nums = [1, 1, 2, 3]          the 1s from indices 0 and 3 are now adjacent
i = 1   nums[1] = 1 == nums[0] = 1  -> return True
```

The very first neighbor comparison finds the duplicate pair that the sort created, so the function returns `True`, matching the expected Output for Example 1. On a duplicate-free input such as Example 2 the scan would compare every adjacent pair, find no match, and return `False`.

#### Solution

The code is the sort followed by the walkthrough's neighbor scan.

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        nums = sorted(nums)
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The sort dominates at `O(n log n)`; the adjacent-pair scan adds only `O(n)`.

##### Space Complexity: `O(n)` or `O(1)`

Sorting a copy uses `O(n)` space; sorting the input in place keeps the extra space at `O(1)` aside from the sort's own overhead.

#### Key Insights

- Sorting collapses the duplicate search to a comparison of neighbors.
- No hash structure is needed, which can matter under tight memory budgets.
- It is slower than the hash approach because of the `O(n log n)` sort.

### Set Length Comparison

#### Derivation

The Hash Set solution builds its set one element at a time so it can stop at the first repeat. If early exit is given up, the language can do the whole build in one expression: a [`set`](https://en.wikipedia.org/wiki/Hash_table) constructor discards duplicate values by definition, so the sizes alone answer the question:

1. Build a set from `nums`, which keeps only distinct values.
2. If the set is smaller than the original list, at least one value was dropped as a duplicate, so return `True`.
3. Otherwise the sizes match and every element was unique, so return `False`.

The built-in `set` does the core deduplication work here, which is why this concise form is ranked after the hand-written approaches.

#### Walkthrough

Follow what `set(nums)` does internally on Example 1: `nums = [1,2,3,1]`. The constructor inserts each element in turn, and an insert of a value already present changes nothing:

```text
insert 1   new value, kept        set = {1}
insert 2   new value, kept        set = {1, 2}
insert 3   new value, kept        set = {1, 2, 3}
insert 1   already present        set stays {1, 2, 3}
len(set) = 3  <  len(nums) = 4    -> return True
```

The duplicate `1` is exactly the element the set silently dropped, so the size comparison `3 < 4` detects it. The function returns `True`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough compressed into one expression: build the set, compare the lengths.

```python
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(set(nums)) < len(nums)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the set visits every element once.

##### Space Complexity: `O(n)`

The set stores all distinct values, up to `n` of them.

#### Key Insights

- Reduces the problem to a single length comparison.
- Reads cleanly but always processes the entire array, with no early exit.
- Relies on the language's `set` to perform the deduplication.

### Counter

#### Derivation

The set-based forms only record whether a value has appeared. Counting how many times each value appears answers a strictly stronger question, and [`collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) builds that tally in one call. A duplicate then shows up as any count above one:

1. Build a `Counter` over `nums` to map each value to its frequency.
2. Scan the frequency values and return `True` as soon as one exceeds `1`.
3. If no count is greater than `1`, return `False`.

This leans most heavily on the standard library, so it sits last among the approaches.

#### Walkthrough

Follow the tally on Example 1: `nums = [1,2,3,1]`. The `Counter` walks the array once, incrementing a per-value count; the second `1` raises its count to `2`:

```text
tally 1    counts = {1: 1}
tally 2    counts = {1: 1, 2: 1}
tally 3    counts = {1: 1, 2: 1, 3: 1}
tally 1    counts = {1: 2, 2: 1, 3: 1}
scan values: 2 > 1 -> any(...) short-circuits -> return True
```

The values are scanned in insertion order, so the first count examined is `2` for the value `1`, and `any` stops there. The function returns `True`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's tally-then-scan in a single expression.

```python
from collections import Counter
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return any(count > 1 for count in Counter(nums).values())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Counting visits every element once, and scanning the distinct counts is at most `O(n)`.

##### Space Complexity: `O(n)`

The counter holds an entry for each distinct value.

#### Key Insights

- Produces full frequency information, which is more than this yes/no question needs.
- `any` short-circuits on the first count above one.
- Most library-driven of the options, so it ranks after the from-scratch solutions.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - compares every pair of elements.
- **Hash Set**: `O(n)` - single pass with constant-time average lookups.
- **Sorting**: `O(n log n)` - bounded by the sort step.
- **Set Length Comparison**: `O(n)` - one pass to build the set.
- **Counter**: `O(n)` - one pass to tally frequencies.

### Space Complexity

- **Brute Force**: `O(1)` - only loop counters, no auxiliary structure.
- **Hash Set**: `O(n)` - stores seen values, up to `n` of them.
- **Sorting**: `O(n)` or `O(1)` - depends on copying versus sorting in place.
- **Set Length Comparison**: `O(n)` - stores all distinct values.
- **Counter**: `O(n)` - stores a count per distinct value.

### Trade-offs

- The Brute Force approach needs no extra memory but its quadratic time is too slow at scale.
- The Hash Set approach is optimal in time and can exit early, at the cost of auxiliary memory.
- The Sorting approach avoids a hash structure but pays the `O(n log n)` sorting cost.
- The Set Length Comparison is the most concise but always scans the whole array.
- The Counter approach computes more information than needed but reads clearly.

### When to Use Each

- **Brute Force**: Only for tiny inputs or as a starting point before optimizing.
- **Hash Set**: The default choice when fastest detection with early exit matters.
- **Sorting**: When memory is tight and an in-place sort is acceptable.
- **Set Length Comparison**: When brevity and readability outweigh early termination.
- **Counter**: When frequencies are already needed elsewhere in the code.

### Optimization Notes

- The Brute Force approach uses no extra space but does redundant pairwise work; the Hash Set trades `O(n)` memory to cut the time to linear.
- The Hash Set approach terminates the moment the first duplicate is found, which is ideal when duplicates are common and appear early.
- The Sorting approach can drop to `O(1)` extra space by sorting the input in place when mutation is allowed.
- The Set Length Comparison and Counter forms favor clarity but process every element regardless of when a duplicate occurs.
