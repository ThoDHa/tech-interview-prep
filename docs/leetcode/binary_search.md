# [Binary Search](https://leetcode.com/problems/binary-search/)

**Easy** | **15 minutes** | **Binary Search**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/binary_search/solution.py`](../../practice/binary_search/solution.py)

Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return -1.

You must write an algorithm with `O(log n)` runtime complexity.

## Examples

### Example 1

**Input:** `nums = [-1,0,3,5,9,12]`, `target = 9`

**Output:** `4`

**Explanation:** `9` exists in `nums` and its index is `4`.

### Example 2

**Input:** `nums = [-1,0,3,5,9,12]`, `target = 2`

**Output:** `-1`

**Explanation:** `2` does not exist in `nums` so return `-1`.

## Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 < nums[i], target < 10^4`
- All the integers in `nums` are unique.
- `nums` is sorted in ascending order.

## Deriving the Solution

The array is sorted, and sortedness turns one comparison into a verdict about many elements: if `nums[mid] < target`, then everything at or left of `mid` is also too small. Every solution past the first is built on discarding half the candidates per comparison.

1. **Start literal.** Ignore the sorted order and check every element in turn.
   Correct on any array, but `O(n)`, which violates the problem's required `O(log n)` bound: see [Linear Scan](#linear-scan).
2. **Use what the problem hands you.** One comparison against the middle
   element rules out an entire half, so keep an interval of surviving candidates and halve it each round: `O(log n)` with two index variables, the halving written as a loop: see [Iterative Binary Search](#iterative-binary-search), or as a recursion where each call owns one subinterval: see [Recursive Binary Search](#recursive-binary-search).
3. **Let the library do the halving.** Python's `bisect` module performs the
   same binary search internally; one insertion-point call plus a presence check finishes the job, which is why it ranks after the from-scratch forms: see [Library Bisect](#library-bisect).

## Solutions

### Linear Scan

#### Derivation

Before exploiting the sorted order, the most direct idea is a [linear search](https://en.wikipedia.org/wiki/Linear_search): look at every element in turn and report the first index that matches `target`. This works on any array, sorted or not, and needs no insight beyond a single pass:

1. Iterate over the indices `0` to `len(nums) - 1`.
2. If `nums[i]` equals `target`, return `i` immediately.
3. If the loop finishes without a match, `target` is absent, so return `-1`.

Because the array is scanned left to right, the first index returned is the only index for any value (the constraints guarantee unique elements).

#### Walkthrough

Trace the scan on Example 1: `nums = [-1, 0, 3, 5, 9, 12]`, `target = 9`. The loop compares each element against `target` in index order:

```text
i=0   nums[0]=-1   -1 != 9, keep going
i=1   nums[1]=0     0 != 9, keep going
i=2   nums[2]=3     3 != 9, keep going
i=3   nums[3]=5     5 != 9, keep going
i=4   nums[4]=9     9 == 9 -> return 4
```

The match at `i = 4` returns immediately, giving `4`, the expected Output of Example 1. Note that the scan walked right past the sorted structure: the comparisons at `i = 0..3` each eliminated only a single element, and an absent target (Example 2) would force all six comparisons before returning `-1`.

#### Solution

The code is the walkthrough's loop verbatim: compare, return on match, `-1` after the loop.

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i in range(len(nums)):
            if nums[i] == target:
                return i
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- In the worst case the target is at the last position or absent, so all `n` elements are examined.
- This does not meet the problem's required `O(log n)` bound; it is the baseline to improve upon.

##### Space Complexity: `O(1)`

- Only the loop index is stored, so memory usage is constant.

#### Key Insights

- This is the most self-derivable approach: it ignores the sorted order entirely and simply checks each element.
- It is correct for every input but wastes the structure the problem hands us, motivating the logarithmic binary search below.
- The `O(n)` runtime violates the problem's stated requirement, so it serves only as a baseline rather than an accepted answer.

### Iterative Binary Search

#### Derivation

The Linear Scan buys each discarded candidate with one comparison, never using the fact that `nums` is sorted. Sortedness is exactly what [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) exploits: a single comparison against the middle element reveals which half of the remaining range can still contain the target, so half the candidates vanish per comparison instead of one. Maintaining an inclusive search interval `[left, right]` and repeatedly halving it is the most direct way to express this:

1. Initialize `left` to `0` and `right` to `len(nums) - 1`, bounding the full array.
2. While the interval is non-empty (`left <= right`):
   - Compute the middle index as `left + (right - left) // 2`.
   - If `nums[mid]` equals `target`, return `mid`.
   - If `nums[mid]` is less than `target`, the answer must lie to the right, so set `left = mid + 1`.
   - Otherwise the answer lies to the left, so set `right = mid - 1`.
3. When the loop exits, the interval is empty and the target was never found, so return `-1`.

Each iteration discards half of the candidates, so the interval shrinks to a single element in logarithmic time.

#### Invariant and Bound

The loop keeps one property true at all times:

$$ \text{if } \textit{target} \in \textit{nums}, \text{ then its index lies in } [\,\textit{left},\ \textit{right}\,] $$

```text
if target in nums, then its index lies in [left, right]
```

Every branch preserves it. Sortedness means `nums[mid] < target` rules out everything at or left of `mid`, so `left = mid + 1` discards only indices that provably cannot hold the answer, and symmetrically on the other side. When `left > right` the interval is empty, so the invariant says the target was never present, which is what justifies returning `-1` rather than searching further.

The interval halves each pass, so after \(k\) iterations at most \(n/2^{k}\) candidates remain. The loop ends once that drops below one:

$$ \frac{n}{2^{k}} < 1 \qquad\Longleftrightarrow\qquad k > \log_2 n $$

```text
n / 2^k < 1   if and only if   k > log2(n)
        (k = iterations completed, n = number of candidates)
```

giving \(O(\log n)\): roughly 20 steps for a million elements, and 30 for a billion.

Computing the midpoint as `left + (right - left) // 2` rather than `(left + right) // 2` is deliberate. The two are equal in exact arithmetic:

$$ \textit{left} + \frac{\textit{right} - \textit{left}}{2} = \frac{\textit{left} + \textit{right}}{2} $$

```text
left + (right - left) / 2 == (left + right) / 2     (in exact arithmetic)
```

but in a fixed-width integer type the second form can overflow when `left` and `right` are both large, while the first never exceeds `right`. Python's integers are arbitrary-precision so it cannot overflow here, but the habit carries to languages where it can.

#### Walkthrough

Using Example 1: `nums = [-1, 0, 3, 5, 9, 12]` and `target = 9`. The search keeps an inclusive interval `[left, right]`, looks at the middle element each round, and throws away the half that cannot contain `9`.

The interval starts at `left = 0`, `right = 5`. Each row shows the state at the top of one loop iteration, after `mid` is computed:

| Iteration | `left` | `right` | `mid` | `nums[mid]` | Comparison to `target = 9` | Action |
|-----------|--------|---------|-------|-------------|-----------------------------|--------|
| 1 | `0` | `5` | `2` | `3` | `3 < 9` | answer is to the right: `left = mid + 1 = 3` |
| 2 | `3` | `5` | `4` | `9` | `9 == 9` | match found: `return mid = 4` |

Step by step:

1. Iteration 1: `mid = 0 + (5 - 0) // 2 = 2`, so `nums[2] = 3`. Since `3 < 9`, everything from index `0` to `2` is too small, so `left` jumps to `3`. The interval shrinks to `[3, 5]`.
2. Iteration 2: `mid = 3 + (5 - 3) // 2 = 4`, so `nums[4] = 9`. This equals `target`, so the function returns `4` immediately.

The returned value is `4`, which matches the expected Output of Example 1. Notice it took only two comparisons instead of the five a linear scan would have needed to reach index `4`: that is the halving that makes binary search `O(log n)`.

#### Solution

The code is the walkthrough's interval bookkeeping: `left` and `right` bound the candidates, `mid` decides which half survives.

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

- Every iteration halves the size of the search interval.
- For an array of length `n`, at most `log₂(n)` iterations are needed before the interval is empty.
- This satisfies the problem's required logarithmic runtime.

##### Space Complexity: `O(1)`

- Only the two index variables `left` and `right` are stored.
- No recursion or auxiliary data structure is used, so memory usage is constant.

#### Key Insights

- The inclusive interval `[left, right]` with the `left <= right` loop condition handles the single-element interval correctly, which is where off-by-one bugs usually appear.
- Computing `mid` as `left + (right - left) // 2` avoids the integer overflow that `(left + right) // 2` can cause in fixed-width integer languages.
- The constant space makes this the standard production form of binary search.

### Recursive Binary Search

#### Derivation

This is the same halving strategy expressed through [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)), where each call owns one subinterval and delegates the smaller subinterval to the next call:

1. The public `search` method seeds the recursion with the full range `[0, len(nums) - 1]`.
2. The helper `_binary_search` handles one interval at a time:
   - Base case: if `left > right`, the interval is empty and the target is absent, so return `-1`.
   - Compute `mid` and compare `nums[mid]` with `target`.
   - If they are equal, return `mid`.
   - If `nums[mid] < target`, recurse on the right half `[mid + 1, right]`.
   - Otherwise recurse on the left half `[left, mid - 1]`.

Because each call passes a strictly smaller interval, the recursion is guaranteed to terminate.

#### Walkthrough

Example 1 finds its target before the interval ever empties, so it never touches the base case. Example 2, `nums = [-1, 0, 3, 5, 9, 12]` with `target = 2` (absent), is the official example that drives the recursion all the way down to `left > right`. The trace indents one level per call:

```text
_binary_search(left=0, right=5)         mid=2, nums[2]=3   3 > 2 -> left half
  _binary_search(left=0, right=1)       mid=0, nums[0]=-1  -1 < 2 -> right half
    _binary_search(left=1, right=1)     mid=1, nums[1]=0    0 < 2 -> right half
      _binary_search(left=2, right=1)   left > right -> return -1
```

Each call shrinks the interval: `[0, 5]` to `[0, 1]` to `[1, 1]` to the empty `[2, 1]`. The base case returns `-1`, and because every caller returns its recursive call's value unchanged, that `-1` passes straight back up the chain. The function returns `-1`, matching the expected Output of Example 2.

#### Solution

The code is the walkthrough's call chain: one interval per call, base case first.

```python
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        return self._binary_search(nums, target, 0, len(nums) - 1)

    def _binary_search(
        self, nums: List[int], target: int, left: int, right: int
    ) -> int:
        if left > right:
            return -1

        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return self._binary_search(nums, target, mid + 1, right)
        else:
            return self._binary_search(nums, target, left, mid - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

- Each recursive call halves the interval, so the recursion depth is at most `log₂(n)`.
- A constant amount of work is done per call, giving logarithmic total time.

##### Space Complexity: `O(log n)`

- The recursion call stack grows to a depth of `log₂(n)`.
- This is the only extra memory used, but it is not constant like the iterative form.

#### Key Insights

- The recursion mirrors the divide-and-conquer structure of binary search directly, which some readers find clearer than the loop.
- The base case `left > right` is the recursive analogue of the iterative loop terminating, and getting it right is essential to avoid infinite recursion.
- The call stack means this form is not strictly constant space; very large inputs theoretically risk deep recursion, though `log₂(10^4)` is tiny in practice.

### Library Bisect

#### Derivation

Python's [`bisect`](https://docs.python.org/3/library/bisect.html) module performs binary search over a sorted sequence, so the work reduces to a single library call plus a membership check:

1. `bisect.bisect_left(nums, target)` returns the leftmost index where `target` could be inserted to keep `nums` sorted.
2. If that index is within bounds and `nums[index]` equals `target`, the target is present, so return `index`.
3. Otherwise `target` is not in the array, so return `-1`.

The bounds and equality check are required because `bisect_left` returns an insertion point even when the target is absent.

#### Walkthrough

The library call is the whole technique here, so the trace follows what `bisect_left` does internally and then the presence check that converts its insertion point into an answer. Use Example 2: `nums = [-1, 0, 3, 5, 9, 12]`, `target = 2` (absent), which exercises both the insertion-point semantics and the `-1` conversion.

Internally `bisect_left` halves a half-open interval `[lo, hi)`, moving `lo` past elements smaller than `target` and pulling `hi` down onto everything else:

```text
lo=0, hi=6   mid=3, nums[3]=5    5 < 2 is false -> hi=3
lo=0, hi=3   mid=1, nums[1]=0    0 < 2 is true  -> lo=2
lo=2, hi=3   mid=2, nums[2]=3    3 < 2 is false -> hi=2
lo=2, hi=2   lo == hi -> return 2
```

So `index = 2`: inserting `2` between `0` and `3` would keep the array sorted. Now the presence check: `index < len(nums)` holds (`2 < 6`), but `nums[index] = 3` does not equal `target = 2`, so the target is absent and the method returns `-1`, matching the expected Output of Example 2. On Example 1 the same call returns `4` with `nums[4] = 9` equal to the target, so `4` is returned directly.

#### Solution

The code is one `bisect_left` call followed by the walkthrough's presence check.

```python
import bisect
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        index = bisect.bisect_left(nums, target)
        if index < len(nums) and nums[index] == target:
            return index
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

- `bisect_left` runs a binary search internally, taking logarithmic time.
- The follow-up bounds and equality check is constant time.

##### Space Complexity: `O(1)`

- `bisect_left` operates in place over the existing list and allocates no auxiliary structure.

#### Key Insights

- This is the idiomatic Python way to binary-search a sorted list and is the least error-prone to write under time pressure.
- The insertion-point semantics of `bisect_left` mean an explicit presence check is mandatory; returning the raw index would wrongly report absent targets as found.
- It relies on the standard library to do the core search, so it is included after the from-scratch approaches that demonstrate the underlying algorithm.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `O(n)` - checks every element in the worst case.
- **Iterative Binary Search**: `O(log n)` - halves the interval each iteration.
- **Recursive Binary Search**: `O(log n)` - halves the interval each call.
- **Library Bisect**: `O(log n)` - `bisect_left` performs an internal binary search.

### Space Complexity

- **Linear Scan**: `O(1)` - only the loop index.
- **Iterative Binary Search**: `O(1)` - only two index variables.
- **Recursive Binary Search**: `O(log n)` - the recursion call stack.
- **Library Bisect**: `O(1)` - no auxiliary allocation.

### Trade-offs

- **Linear Scan** is the simplest to write and works on unsorted data, but it ignores the sorted structure and fails the required `O(log n)` bound.
- **Iterative Binary Search** gives constant space and full control over the index arithmetic at the cost of slightly more verbose pointer bookkeeping.
- **Recursive Binary Search** reads as a clean divide-and-conquer expression but pays a logarithmic stack cost and adds call overhead.
- **Library Bisect** is the shortest and least bug-prone to write, but it hides the algorithm and requires an explicit presence check to convert an insertion point into a found index.

### When to Use Each

- **Linear Scan**: Only as a baseline or when the array is not sorted; it does not satisfy this problem's logarithmic requirement.
- **Iterative Binary Search**: The default choice for production code and interviews where constant space is valued.
- **Recursive Binary Search**: When the divide-and-conquer structure should be emphasized for readability or teaching.
- **Library Bisect** (Recommended for quick, correct code): When working in Python and a sorted list is already available, and clarity outweighs demonstrating the algorithm.

### Optimization Notes

- The linear scan is the discoverable baseline; the three logarithmic solutions all exploit the sorted order to discard half the candidates per step.
- The hand-written binary searches compute `mid` as `left + (right - left) // 2` to avoid the integer overflow that `(left + right) // 2` can cause in fixed-width integer languages.
- The iterative form is generally preferred over the recursive form in production because it avoids the call-stack growth and associated overhead.
- A common variant runs the loop half-open over `[left, right)` with `while left < right`, shrinking with `right = mid` and `left = mid + 1`. That shape computes the *lower bound* (the first index with `nums[i] >= target`), which is exactly what `bisect_left` implements, and it generalizes cleanly to first-occurrence and last-occurrence searches where the closed-interval loop needs extra care.
