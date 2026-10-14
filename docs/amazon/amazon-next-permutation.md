# [Next Permutation](https://www.fastprep.io/problems/amazon-next-permutation)

**Medium** | **NN minutes** | **Array, Two Pointers**

Return the lexicographically next permutation of nums. If the current ordering is the greatest possible, return the smallest ordering. Duplicate values are allowed.

## Examples

### Example 1

**Input:** `nums = [1,2,3]`

**Output:** `[1,3,2]`

**Explanation:** Swapping the final two values gives the next greater ordering.

### Example 2

**Input:** `nums = [-1,0,-1]`

**Output:** `[0,-1,-1]`

**Explanation:** Covers wraparound, duplicates, pivot placement, tiny arrays, equality, and signed values.

### Example 3

**Input:** `nums = [2,3,1,3,3]`

**Output:** `[2,3,3,1,3]`

**Explanation:** Covers wraparound, duplicates, pivot placement, tiny arrays, equality, and signed values.

## Constraints

- `1 <= nums.length <= 10000`
- `Values fit in a signed 32-bit integer.`

## Solutions

### Permutation Enumeration

#### Derivation

The most literal reading of the request: a permutation is one ordering of `nums`, and "the next permutation" is whichever ordering follows the current one in lexicographic order. So produce every ordering, sort them, find the current one in that sorted list, and hand back its right neighbor, wrapping to the first ordering when the current one is the greatest possible:

1. Build `orderings`, a set of tuples, starting from the empty tuple. For each
   `value` in `nums`, form a new set by inserting `value` at every position of
   every partial ordering. Keeping the results in a set collapses the
   duplicates that repeated values would otherwise produce.
2. Sort the set into `sorted_orderings`, which for tuples is lexicographic order.
3. Scan `sorted_orderings` for `target = tuple(nums)`; return the ordering at
   the next position, wrapping with `% len(sorted_orderings)`.

#### Walkthrough

Example 1 asks for the next ordering of `nums = [1,2,3]`. The insertion loop grows the set one value at a time, inserting the new value at every position of every partial ordering:

```text
start          orderings = {()}
insert 1       { (1,) }
insert 2       { (2,1), (1,2) }
insert 3       { (3,2,1), (2,3,1), (2,1,3),
                 (3,1,2), (1,3,2), (1,2,3) }
```

Sorting the six orderings and locating `target = (1,2,3)`:

```text
sorted_orderings = [ (1,2,3), (1,3,2), (2,1,3),
                     (2,3,1), (3,1,2), (3,2,1) ]
target (1,2,3) at position 0 -> return position 1 = (1,3,2)
```

The function returns `[1,3,2]`, matching the expected Output for Example 1. Had the current ordering been the last one, `(3,2,1)`, the wraparound `(position + 1) % len` would land back on `(1,2,3)`.

#### Solution

The code is the walkthrough written down: insertion-built set, one sort, one scan.

```python
from typing import List, Set, Tuple


class Solution:
    def solve(self, nums: List[int]) -> List[int]:
        orderings: Set[Tuple[int, ...]] = {()}
        for value in nums:
            orderings = {
                ordering[:position] + (value,) + ordering[position:]
                for ordering in orderings
                for position in range(len(ordering) + 1)
            }

        sorted_orderings = sorted(orderings)
        target = tuple(nums)
        for position, ordering in enumerate(sorted_orderings):
            if ordering == target:
                next_position = (position + 1) % len(sorted_orderings)
                return list(sorted_orderings[next_position])

        return nums
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n^2 log n)`

Building the `n!` orderings costs `O(n! × n^2)` (each of the `n!` final orderings is extended `n` times by an `O(n)` tuple copy), and sorting them dominates: `log(n!) = O(n log n)` comparisons, each touching tuples of length `O(n)`.

##### Space Complexity: `O(n! × n)`

The set and the sorted list hold `n!` orderings of length `n` each.

#### Key Insights

- The brute force needs a set (or an explicit deduplication), not a list: with repeated values, identical orderings are generated many times, and stepping from the first copy of `nums` to its duplicate would return the input unchanged.
- Tuple comparison in Python is lexicographic, so one `sorted` call produces exactly the ordering the problem ranks by.
- The approach is correct for any `n` but astronomically out of scale with the constraint `nums.length <= 10000`, where `n!` orderings cannot even be counted, let alone stored.

### Suffix Scan with Sort

#### Derivation

The enumeration never looks at `nums` until the final scan, and that is the waste: the current arrangement already pins down most of the answer. Compare any ordering with its successor and a prefix survives untouched; the change begins at one specific position. Scanning from the right, the suffix is non-increasing for a while (each element `>=` the one after it), and the first place that descent breaks, the first index with `nums[pivot_idx] < nums[pivot_idx + 1]`, is exactly where the next permutation must act. Call that index `pivot_idx`.

What must happen at the pivot? The values right of `pivot_idx` cannot produce a larger ordering on their own (they are at their maximum arrangement, non-increasing), so `nums[pivot_idx]` itself must grow, and it must grow as little as possible: swap it with the smallest suffix value that is strictly greater. The tail is then some arrangement of leftover values, and the smallest arrangement of any multiset is its ascending sort:

1. Scan `pivot_idx` from `count - 2` down to `0` while `nums[pivot_idx] >= nums[pivot_idx + 1]`. If `pivot_idx` drops below `0`, the whole array is non-increasing: it is the greatest ordering, so reverse `nums` entirely and return the smallest.
2. Scan `successor_idx` from `count - 1` down while `nums[successor_idx] <= nums[pivot_idx]`, then swap `nums[pivot_idx]` with `nums[successor_idx]`.
3. Sort the slice `nums[pivot_idx + 1:]` ascending, in place, and return `nums`.

#### Walkthrough

Example 3 runs the scan on `nums = [2,3,1,3,3]`, whose expected Output `[2,3,3,1,3]` the three steps must reproduce:

```text
nums = [2, 3, 1, 3, 3]

pivot scan from the right:
  pair (nums[3], nums[4]) = (3, 3)    3 >= 3, keep scanning
  pair (nums[2], nums[3]) = (1, 3)    1 <  3, pivot_idx = 2

suffix nums[3:] = [3, 3]
smallest suffix value strictly greater than 1 is 3
its rightmost occurrence is index 4 = successor_idx
swap indices 2 and 4                 -> [2, 3, 3, 3, 1]

sort suffix indices 3..4             -> [1, 3]
result = [2, 3, 3, 1, 3]
```

The result matches the expected Output for Example 3. Example 2, `nums = [-1,0,-1]`, follows the same steps with `pivot_idx = 0` and reaches `[0,-1,-1]`; the branch the three cases never hit is the wraparound one, where no ascent exists at all: for the tailored input `nums = [3,2,1]` the pivot scan falls off the left end and the whole array reverses to `[1,2,3]`.

#### Solution

The code is the walkthrough's three steps: pivot scan, successor swap, suffix sort.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> List[int]:
        count = len(nums)

        pivot_idx = count - 2
        while pivot_idx >= 0 and nums[pivot_idx] >= nums[pivot_idx + 1]:
            pivot_idx -= 1

        if pivot_idx >= 0:
            successor_idx = count - 1
            while nums[successor_idx] <= nums[pivot_idx]:
                successor_idx -= 1
            nums[pivot_idx], nums[successor_idx] = (
                nums[successor_idx], nums[pivot_idx])
            nums[pivot_idx + 1:] = sorted(nums[pivot_idx + 1:])

        return nums
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The pivot and successor scans are linear, and sorting the suffix of up to `n - 1` values costs `O(n log n)`, which dominates.

##### Space Complexity: `O(n)`

The slice copy `nums[pivot_idx + 1:]` plus Timsort's working buffer are both linear in the suffix length.

#### Key Insights

- Locating the pivot from the right is what keeps the prefix intact: everything left of `pivot_idx` is already the smallest it can ever be for any successor sharing that prefix.
- The successor scan finds the smallest suffix value that is strictly greater than the pivot, because the non-increasing suffix puts that minimum at the scan's first hit from the right.
- Strict inequality (`<=` in the scan guards) is what makes duplicates work: swapping equal values would leave the ordering unchanged.

### Suffix Scan with Reverse

#### Derivation

The sort in the previous approach is the only superlinear step, and it re-derives order that the swap already preserved. The claim worth writing down: if the pivot is swapped with the *rightmost* suffix value strictly greater than it, the suffix stays non-increasing. That makes the sort pure waste, because reversing a non-increasing sequence produces the same ascending arrangement, and a reversal is two pointers and one linear pass:

1. Find `pivot_idx` exactly as before; if none exists, fall through to the
   reversal with `pivot_idx = -1`, which reverses the whole array.
2. Find `successor_idx` with the same right-to-left scan: the first suffix
   value strictly greater than `nums[pivot_idx]`, which is simultaneously the
   smallest such value and its rightmost occurrence, because the suffix is
   non-increasing. Swap the two.
3. Reverse `nums[pivot_idx + 1:]` in place with two pointers and return `nums`.

#### Invariant

The suffix to the right of `pivot_idx` is non-increasing, before and after the swap:

```text
invariant: nums[pivot_idx + 1] >= nums[pivot_idx + 2] >= ... >= nums[count - 1]

holds:     when the pivot scan stops, because pivot_idx is the last ascent
           (every adjacent pair to its right satisfied nums[k] >= nums[k + 1])

preserved: by the swap at successor_idx. The scan from the right stopped at
           the first value > nums[pivot_idx], so every element to the right of
           successor_idx is <= nums[pivot_idx] (small enough to sit after the
           swapped-in pivot value), and every element to its left is
           >= nums[successor_idx] > nums[pivot_idx] (large enough to sit before it)

at exit:   reversing a non-increasing sequence yields a non-decreasing one,
           which is the smallest arrangement of those values
```

The invariant is what licenses the reversal: no comparison happens in step 3, because the ordering was already earned by the scan and the swap.

#### Walkthrough

Example 2 exercises the successor scan and a reversal that happens to be a no-op, on `nums = [-1,0,-1]`:

```text
nums = [-1, 0, -1]

pivot scan from the right:
  pair (nums[1], nums[2]) = (0, -1)    0 >= -1, keep scanning
  pair (nums[0], nums[1]) = (-1, 0)    -1 < 0, pivot_idx = 0

successor scan from the right:
  nums[2] = -1:  -1 <= -1, keep scanning
  nums[1] = 0:   0 > -1, successor_idx = 1

swap indices 0 and 1                  -> [0, -1, -1]
suffix indices 1..2 = [-1, -1], still non-increasing
reverse indices 1..2                  -> [-1, -1] (unchanged)

result = [0, -1, -1]
```

The result matches the expected Output for Example 2. Example 3 shows the reversal doing real work: after the same pivot and swap steps as the sort walkthrough, the suffix is `[3, 1]` and the reversal turns it into `[1, 3]`, producing `[2,3,3,1,3]`.

#### Solution

The code is the two scans and the two-pointer reversal; the wraparound branch needs no special case, because `pivot_idx = -1` makes the reversal span the whole array.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> List[int]:
        count = len(nums)

        pivot_idx = count - 2
        while pivot_idx >= 0 and nums[pivot_idx] >= nums[pivot_idx + 1]:
            pivot_idx -= 1

        if pivot_idx >= 0:
            successor_idx = count - 1
            while nums[successor_idx] <= nums[pivot_idx]:
                successor_idx -= 1
            nums[pivot_idx], nums[successor_idx] = (
                nums[successor_idx], nums[pivot_idx])

        left, right = pivot_idx + 1, count - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

        return nums
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three linear passes at most: the pivot scan, the successor scan, and the two-pointer reversal.

##### Space Complexity: `O(1)`

Everything happens through in-place swaps; no slices, no auxiliary structures.

#### Key Insights

- The pivot scan and the successor scan are the same scan run twice: both walk right to left comparing adjacent values, which is why the whole algorithm stays cache-friendly and branch-simple.
- Choosing the rightmost strictly-greater successor is not a convenience, it is the correctness proof: that choice is what keeps the suffix non-increasing so the reversal can replace the sort.
- The wraparound case (greatest ordering wraps to the smallest) costs no extra code: the same reversal that tidies a suffix reverses the entire array when no pivot exists.

## Comparison of Solutions

### Time Complexity

- **Permutation Enumeration**: `O(n! × n^2 log n)` - builds and lexicographically sorts every ordering of `nums`.
- **Suffix Scan with Sort**: `O(n log n)` - three linear scans plus one sort of the suffix.
- **Suffix Scan with Reverse**: `O(n)` - three linear scans with no sorting at all.

### Space Complexity

- **Permutation Enumeration**: `O(n! × n)` - stores every distinct ordering as a tuple.
- **Suffix Scan with Sort**: `O(n)` - the suffix slice copy plus Timsort's working buffer.
- **Suffix Scan with Reverse**: `O(1)` - in-place swaps only.

### Trade-offs

- **Permutation Enumeration**: impossible to get wrong once the ordering is defined, but the `n!` blowup makes it unusable past a dozen elements and it never inspects the input's own structure.
- **Suffix Scan with Sort**: the safest correct form to write under time pressure, since the sort absorbs any mistake about where the swapped value lands, at the price of one superlinear step and linear scratch space.
- **Suffix Scan with Reverse**: optimal in both bounds, but its correctness leans on the non-increasing-suffix invariant, which must be stated (or at least remembered) rather than seen.

### When to Use Each

- **Permutation Enumeration**: when `n` is tiny (four or fewer) and the ordering notion might change, since the enumeration adapts to any total order by swapping the comparator.
- **Suffix Scan with Sort (Recommended)**: the pragmatic interview answer if the invariant feels shaky: it shares the pivot logic of the optimal solution and is easier to argue correct.
- **Suffix Scan with Reverse**: the answer to give when asked for `O(1)` space or the follow-up "can you avoid the sort?", and the standard expectation once the problem name is known.

### Optimization Notes

- The successor scan's `<=` guard is load-bearing: replacing it with `<` swaps a duplicate value for the pivot and can leave the ordering unchanged, a silent wrong answer on inputs like `[2,3,1,3,3]`.
- The reversal branch doubles as the wraparound handler, so the whole algorithm is one straight-line path with no separate "is it the last permutation" test.
- This is the same three-step routine (pivot, swap, reverse) that powers `itertools.permutations` order guarantees and C++ `std::next_permutation`; knowing it by name is worth the invariant memorization.
