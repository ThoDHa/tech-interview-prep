# [Missing Number](https://leetcode.com/problems/missing-number/)

**Easy** | **15 minutes** | **Array, Hash Table, Math, Binary Search, Bit Manipulation, Sorting**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Arithmetic series](https://en.wikipedia.org/wiki/Arithmetic_progression) · [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Exclusive or](https://en.wikipedia.org/wiki/Exclusive_or) · [Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/missing_number/solution.py`](../../practice/missing_number/solution.py)

Given an array `nums` containing `n` integers in the range `[0, n]` without any duplicates, return the single number in the range that is missing from `nums`.

**Follow-up**: Could you implement a solution using only `O(1)` extra space complexity and `O(n)` runtime complexity?

## Examples

### Example 1

**Input:** `nums = [1,2,3]`

**Output:** `0`

**Explanation:** Since there are 3 numbers, the range is [0,3]. The missing number is 0 since it does not appear in nums.

### Example 2

**Input:** `nums = [0,2]`

**Output:** `1`

## Constraints

- `1 <= nums.length <= 1000`

## Deriving the Solution

The array is the full range `0..n` with exactly one value removed, so the problem is not "find" but "diff": whatever the full range has and the array lacks is the answer. Every solution below computes that difference, by membership, by total, by pairing, or by position.

1. **Start literal.** Collect the array's values in a set, then test every
   candidate `0..n` for membership; the one candidate no value matches is the
   answer. Correct and obvious, but the set costs `O(n)` space: see
   [Hash Set](#hash-set).
2. **Diff totals instead of memberships.** The full range sums to the
   [arithmetic series](https://en.wikipedia.org/wiki/Arithmetic_progression)
   `n * (n + 1) // 2`; subtracting the array's sum cancels every present
   value and leaves the missing one. One pass, one accumulator, `O(1)` space:
   see [Gauss Sum Formula](#gauss-sum-formula).
3. **Diff pairs instead of totals.** The same cancellation works value by
   value: exclusive or is its own inverse, so folding every index and every
   array value into one accumulator cancels each present pair and leaves the
   missing one. No overflow anywhere, `O(1)` space: see
   [XOR Fold](#xor-fold).
4. **Let position reveal it.** Sorting puts each present value on its own
   index: the first place `i != nums[i]` names the missing value, and if no
   place mismatches, the missing value is `n` itself. The sort costs
   `O(n log n)`: see [Sort and Scan](#sort-and-scan).

## Solutions

### Hash Set

#### Derivation

The most direct reading turns the range into a checklist: mark which values the array actually holds, then walk the range and report the one value no mark covers. The steps:

1. Build `num_set` holding every value in `nums`.
2. For each `candidate` from `0` through `n`, return it as soon as
   `candidate` is not in `num_set`.
3. The guarantee that exactly one value is missing means the loop always
   returns inside the range; the trailing return satisfies the signature.

#### Walkthrough

Let us run the checklist on Example 1: `nums = [1,2,3]`, expected Output `0`. Building the set, then probing candidates in order:

```text
build     num_set = {1, 2, 3}
probe 0   0 in {1, 2, 3}?  no   -> return 0
```

The first probe already fails to find its candidate: `0` is the only value of `0..3` the array lacks, so the function returns `0`, matching the expected Output for Example 1. Example 2 exercises a deeper probe: `nums = [0,2]` builds `{0, 2}`, the probe `0` is found, and the probe `1` is the first miss, returning `1`, again matching the expected Output.

#### Solution

The code is the walkthrough's build-then-probe.

```python
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        num_set = set(nums)
        for candidate in range(len(nums) + 1):
            if candidate not in num_set:
                return candidate
        return len(nums)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the set is one pass over `n` values, and the probe loop tests at most `n + 1` candidates with `O(1)` average lookups.

##### Space Complexity: `O(n)`

The set holds `n` values, which the follow-up's `O(1)`-space demand rules out.

#### Key Insights

- Reads directly off the problem: it is a membership question, so use a membership structure.
- The early return probes only up to the missing value; but the set is built in full before any probe.
- The baseline the arithmetic and XOR solutions exist to beat on space.

### Gauss Sum Formula

#### Derivation

The set pays `O(n)` space to learn something arithmetic already knows: the values `0..n` sum to the [arithmetic series](https://en.wikipedia.org/wiki/Arithmetic_progression) `n * (n + 1) // 2`. Subtract the array's actual sum from that expected total and every present value cancels its counterpart, leaving exactly the missing value. One accumulator, no structure, and the follow-up's two demands are met at once. The steps:

1. Let `n = len(nums)` and compute the expected total
   `n * (n + 1) // 2`.
2. Subtract `sum(nums)` from the expected total.
3. Return the difference.

#### Walkthrough

Let us diff the totals on Example 1: `nums = [1,2,3]`, expected Output `0`:

```text
n = 3
expected = 3 * 4 // 2 = 6
actual   = 1 + 2 + 3   = 6
missing  = 6 - 6       = 0
```

Every value the array holds contributes to both totals and cancels; the missing `0` contributes to neither, and the difference is `0`, matching the expected Output for Example 1. Example 2 shows a nonzero gap: `nums = [0,2]` gives `expected = 2 * 3 // 2 = 3`, `actual = 2`, and the difference `1` is the value the array lacks, matching the expected Output.

#### Solution

The code is the two totals and their difference.

```python
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        return n * (n + 1) // 2 - sum(nums)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass to sum the array; the formula is constant work on `n`.

##### Space Complexity: `O(1)`

One accumulator, meeting the follow-up's space demand.

#### Key Insights

- The range's total is a checksum: any single absence survives the subtraction as the exact difference.
- In fixed-width languages the running total can overflow where the XOR Fold cannot; in Python, arbitrary-precision integers make this a non-issue.
- `sum(nums)` streams, so this works on iterators and needs no random access, unlike the sorting approach.

### XOR Fold

#### Derivation

The Gauss total cancels values by addition. Exclusive or cancels them by identity: `x ^ x == 0` and `0 ^ v == v`, so folding the whole range together with the whole array leaves only values that appear an odd number of times, which is exactly the missing one. Fold every index `0..n - 1`, the value `n` itself, and every array value into one accumulator, and each present value pairs with a range value to cancel; the missing value has no partner and survives. The steps:

1. Initialize the accumulator `acc` to `n` (the one range value no index
   visit will supply).
2. For each index `i`, fold in both `i` and `nums[i]`: `acc ^= i ^ nums[i]`.
3. Return `acc` after the pass.

#### Walkthrough

Let us fold Example 2 by hand: `nums = [0,2]`, expected Output `1`. The accumulator starts at `n = 2`, then each index folds its index and value in:

```text
start    acc = 2                        (2 = n, the unvisited range value)
i = 0    acc = 2 ^ 0 ^ 0 = 2            (0 ^ 0 cancels)
i = 1    acc = 2 ^ 1 ^ 2 = 1            (2 ^ 2 cancels, 1 survives)
```

The value `2` appears both as the seed and as `nums[1]`, so it cancels itself; the index `1` pairs with nothing in the array, because `1` is the missing value, and it is what the accumulator holds. The function returns `1`, matching the expected Output for Example 2. Example 1 behaves identically: the seed `3` cancels against `nums[2] = 3`, the indices `1` and `2` cancel against the array's `1` and `2`, and the survivor is `0`.

#### Solution

The code is the walkthrough's fold: one seed, one line per element.

```python
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        acc = len(nums)
        for i, num in enumerate(nums):
            acc ^= i ^ num
        return acc
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass, two exclusive-ors per element.

##### Space Complexity: `O(1)`

One integer accumulator, meeting the follow-up.

#### Key Insights

- The same cancellation argument as Single Number's XOR Accumulator, generalized: fold the range and the array together and pairs annihilate.
- Never overflows, unlike the sum difference in fixed-width languages: the accumulator stays bounded by the width of the values folded.
- The seed `n` is what keeps the fold honest: the range has `n + 1` values but the array has `n` entries, so one range value must enter without an index partner.

### Sort and Scan

#### Derivation

Give the values positions and the missing one identifies itself: after sorting, a complete prefix of the range sits at its own index, so `nums[i] == i` holds until the gap and `nums[i] > i` after it. The first index where `nums[i] != i` is exactly the missing value. If no index mismatches, every position `0..n - 1` holds its own value and the missing one is `n`. The steps:

1. Sort `nums` in place.
2. Scan `i` from `0` to `n - 1`; return `i` at the first `nums[i] != i`.
3. When the scan finishes clean, return `n`.

#### Walkthrough

Let us sort and scan Example 2: `nums = [0,2]`, expected Output `1`:

```text
sorted      [0, 2]
i = 0       nums[0] = 0 == 0   match, keep scanning
i = 1       nums[1] = 2 != 1   mismatch -> return 1
```

The mismatch at `i = 1` says the value `1` never arrived: everything before it forms the complete prefix `0`, and everything from `2` upward has been pushed one slot right by the gap. The function returns `1`, matching the expected Output for Example 2. The mismatch also covers Example 1's missing-at-bottom shape: `[1,2,3]` sorts to itself, index `0` already holds `1 != 0`, and the very first probe returns `0`, matching the expected Output for Example 1. The clean-scan exit is reserved for the missing-at-top case: on `[0,1,2]` every index matches, the loop finishes, and the function returns `n = 3`.

#### Solution

The code is the walkthrough's sort, scan, and clean-exit.

```python
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        nums.sort()
        for i, num in enumerate(nums):
            if num != i:
                return i
        return len(nums)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Dominated by the sort; the scan afterward is a single linear pass.

##### Space Complexity: `O(1)` or `O(n)`

An in-place sort uses `O(1)` auxiliary space; Python's `list.sort` allocates `O(n)` temporaries in the worst case.

#### Key Insights

- Position does the bookkeeping: the array's own indices become the checklist the Hash Set built explicitly.
- The mismatch is one-sided (`num != i` never means `num < i`): the gap shifts every later value up by exactly one, never down.
- Slower than the two `O(1)`-space linear solutions and mutates the input, which is why it ranks behind them despite the elegant exit.

## Comparison of Solutions

The practice harness's `practice/missing_number/reference.py` implements the **Gauss Sum Formula** solution.

### Time Complexity

- **Hash Set**: `O(n)` - one pass to build, one probe loop with constant lookups.
- **Gauss Sum Formula**: `O(n)` - one pass to sum.
- **XOR Fold**: `O(n)` - one pass, two exclusive-ors per element.
- **Sort and Scan**: `O(n log n)` - sort dominates; the scan is linear.

### Space Complexity

- **Hash Set**: `O(n)` - the membership set.
- **Gauss Sum Formula**: `O(1)` - one accumulator.
- **XOR Fold**: `O(1)` - one accumulator.
- **Sort and Scan**: `O(1)` or `O(n)` - in-place sort; Python's `list.sort` may allocate linearly.

### Trade-offs

- The Hash Set is the most literal translation and the easiest to extend (several missing values, arbitrary ranges), but it is the only one that misses the follow-up's space bar.
- The Gauss Sum Formula and the XOR Fold both meet `O(n)` time and `O(1)` space; they differ in failure mode, overflow in fixed-width languages versus none, and in transparency, arithmetic versus bit identity.
- The Sort and Scan needs no formula at all but pays `O(n log n)`, mutates the input, and leans on the language's sort stability for nothing in particular.

### When to Use Each

- **Hash Set**: when several values may be missing or the range is sparse, where set semantics generalize directly.
- **Gauss Sum Formula** (recommended): the default answer; it meets the follow-up in one readable line.
- **XOR Fold**: when the values' width makes the running sum dangerous in fixed-width languages, or when the Single Number idiom should carry over.
- **Sort and Scan**: when the input must end sorted anyway or a formula feels unjustified without derivation.

### Optimization Notes

- Both `O(1)`-space solutions stream: neither needs random access or the whole array at once, so both work on sequences that cannot be held in memory.
- The Gauss difference and the XOR fold compute the same cancellation from opposite directions; their intermediate values differ wildly (the sum grows to `n^2 / 2`, the fold stays word-width) while their results agree.
- If the range were `1..n` with values in `1..n + 1`, only the seed changes (`n + 1` instead of `n`); the formula version's expected total becomes `(n + 1)(n + 2) // 2`.
- Binary search on the sorted array (`nums[mid] == mid` decides the half) reaches the answer in `O(log n)` comparisons after an `O(n log n)` sort, which only pays when many queries hit one sorted copy.
