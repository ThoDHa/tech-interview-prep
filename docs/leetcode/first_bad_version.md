# [First Bad Version](https://leetcode.com/problems/first-bad-version/)

**Easy** | **15 minutes** | **Binary Search**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/first_bad_version/solution.py`](../../practice/first_bad_version/solution.py)

You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.

Suppose you have n versions `[1, 2, ..., n]` and you want to find out the first bad one, which causes all the following ones to be bad.

You are given an API `bool isBadVersion(version)` which returns whether `version` is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.

## Examples

### Example 1

**Input:** `n = 5`, `bad = 4` **Output:** `4` **Explanation:** call isBadVersion(3) -> `false` call isBadVersion(5) -> `true` call isBadVersion(4) -> `true` Then `4` is the first bad version.

### Example 2

**Input:** `n = 1`, `bad = 1` **Output:** `1`

## Constraints

- `1 <= bad <= n <= 2^31 - 1`

## Deriving the Solution

Because every version after a bad one is also bad, the API's answers over versions `1..n` form a monotonic sequence: `False, False, ..., False, True, True, ..., True`. Finding the first bad version means locating the boundary where `False` flips to `True`, and each solution below is a different way of finding that boundary.

1. **Start literal.** Ask the API about version `1`, then `2`, and so on: the
   first `True` is the answer. Correct, but up to `n` API calls with `n` as large as `2³¹ - 1`: see [Linear Scan](#linear-scan).
2. **Spot the waste.** Each `False` answer rules out only the single version
   asked about, yet monotonicity makes one probe far more informative: a `False` at any version discards everything at or below it, and a `True` discards everything above it.
3. **Halve the range.** Probe the midpoint of the candidate range and keep the
   half that must still contain the boundary, converging in `O(log n)` API calls: see [Binary Search](#binary-search).
4. **Or lean on the library.** `bisect.bisect_left` runs the same left-boundary
   search over a virtual sequence keyed by `isBadVersion`: see [Bisect](#bisect).

## Solutions

A note on the harness: on LeetCode, `isBadVersion` is predefined by the judge. In this repo's practice setup, `practice/first_bad_version/solution.py` defines a module-level `bad` and an `isBadVersion` shim (`return v >= bad`) that the tests configure per case, so the same solution code runs unchanged.

### Linear Scan

#### Derivation

The most direct reading of the problem: [walk the versions in order](https://en.wikipedia.org/wiki/Linear_search) and return the first one the API reports as bad. Because every version after a bad version is also bad, the first `True` the scan encounters is the boundary we want.

1. Iterate `version` from `1` to `n`.
2. Call `isBadVersion(version)` on each.
3. Return the first `version` for which the API returns `True`.

The constraints guarantee at least one bad version exists, so the loop always returns before falling through; the trailing `return -1` only guards against an empty range.

#### Walkthrough

Let us watch the Linear Scan run on Example 1: `n = 5` with the first bad version at `4`, so `isBadVersion` returns `False` for versions `1, 2, 3` and `True` for `4, 5`.

The loop walks `version` from `1` upward, calling the API on each and returning the moment it sees `True`:

| Step | `version` | `isBadVersion(version)` | Action |
|------|-----------|-------------------------|--------|
| 1 | `1` | `False` | keep scanning |
| 2 | `2` | `False` | keep scanning |
| 3 | `3` | `False` | keep scanning |
| 4 | `4` | `True` | `return 4` |

At `version = 4` the API reports `True` for the first time, so the function returns `4` immediately and never reaches version `5`. The returned value `4` matches the example's expected Output. Notice the scan made `4` API calls to get here: the binary search below finds the same answer in far fewer.

#### Solution

The code is the walkthrough's loop: ask about each version in turn and return at the first `True`.

```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        for version in range(1, n + 1):
            if isBadVersion(version):
                return version
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

In the worst case the bad boundary sits at version `n`, so the scan makes `n` API calls. With `n` as large as `2³¹ - 1`, that is billions of calls, which is exactly what the problem asks us to avoid.

##### Space Complexity: `O(1)`

Only a single loop variable is tracked regardless of input size.

#### Key Insights

- This is the baseline that proves correctness: the first `True` is the answer.
- It maximizes API calls rather than minimizing them, so it fails the problem's
  optimization goal and exists mainly as a reference point.
- It would also time out on the upper end of the constraints.

### Binary Search

#### Derivation

The linear scan spends one API call to eliminate one version, which is exactly the cost the problem tells us to minimize. The structure that lets us do better is monotonicity: once versions go bad they stay bad, so the `isBadVersion` results form `False, False, ..., False, True, True, ..., True`. That is a sorted boolean array, and finding the first `True` is a textbook [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) for the left boundary: one probe at the midpoint discards half the candidate range, whichever answer comes back.

1. Maintain a closed search range `[lo, hi]` (both endpoints inclusive), starting at `lo = 1`, `hi = n`.
2. While `lo < hi`, compute `mid = lo + (hi - lo) // 2`.
3. If `mid` is bad, the answer is `mid` or earlier, so set `hi = mid` (keep
   `mid` in the candidate range).
4. If `mid` is good, the answer is strictly after `mid`, so set `lo = mid + 1`.
5. When `lo == hi` the range has collapsed onto the first bad version; return it.

The invariant is that the first bad version always lies in `[lo, hi]`. Each iteration shrinks the range while preserving that invariant, and because the bad version is guaranteed to exist, the range converges onto it rather than past it.

#### Walkthrough

Let us run the search on Example 1: `n = 5` with the first bad version at `4`, so `isBadVersion` returns `False` for versions `1, 2, 3` and `True` for `4, 5`. Each line shows the range `[lo, hi]` at the top of the loop, the midpoint probed, and how the range shrinks:

```text
lo=1  hi=5   mid = 1 + (5 - 1) // 2 = 3   isBadVersion(3) = False  -> lo = 4
lo=4  hi=5   mid = 4 + (5 - 4) // 2 = 4   isBadVersion(4) = True   -> hi = 4
lo=4  hi=4   loop ends (lo == hi)         -> return 4
```

The first probe at `3` comes back good, so the boundary lies strictly above it and `lo` jumps to `4`. The second probe at `4` comes back bad, so `4` itself stays inside the range as the new `hi`. The range has collapsed to a single version, and the function returns `4`, matching the expected Output. Two API calls sufficed where the linear scan spent four.

#### Solution

The code is the walkthrough's collapsing range: probe `mid` and keep the half that must still hold the boundary.

```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        lo, hi = 1, n
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if isBadVersion(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Each iteration halves the candidate range, so the loop runs at most `⌈log₂ n⌉` times and makes that many API calls. This is optimal: distinguishing the boundary requires at least logarithmically many queries.

##### Space Complexity: `O(1)`

Only the `lo`, `hi`, and `mid` integers are stored.

#### Key Insights

- Computing `mid = lo + (hi - lo) // 2` avoids the overflow that `(lo + hi) // 2`
  could cause when `n` approaches `2³¹ - 1` in fixed-width integer languages.
- Setting `hi = mid` (not `mid - 1`) is essential: `mid` itself may be the
  answer, so it must stay inside the range.
- The `lo < hi` loop condition with a collapsing range removes the need for a
  separate "found it" check; convergence is the answer.

### Bisect

#### Derivation

The hand-written search is a pattern the standard library already ships: [`bisect.bisect_left`](https://docs.python.org/3/library/bisect.html) performs the left-boundary binary search. Treating the versions as a virtual sorted sequence whose key is `isBadVersion`, the predicate maps to `False < True`, so the leftmost insertion point of `True` is the first bad version.

1. Use `range(n + 1)` as the implicit array of version numbers (index equals
   version).
2. Pass `key=isBadVersion` so `bisect` compares on the boolean each version maps
   to.
3. Restrict the search to versions `1..n` with `lo=1`.
4. Return the insertion point, which is the first version whose key is `True`.

The `range` is lazy, so no array is materialized; `bisect` evaluates the key only on the `O(log n)` midpoints it probes.

#### Walkthrough

Let us follow `bisect_left` itself on Example 1: `n = 5`, first bad version `4`. The virtual array is `range(6)` (indices `0..5`, index equals version), the target is `True`, and the search starts at `lo = 1` with `hi` defaulting to the sequence length `6`. Internally `bisect_left` runs the same halving loop as the hand-written version, testing `key(mid) < True` at each midpoint:

```text
lo=1  hi=6   mid = (1 + 6) // 2 = 3   isBadVersion(3) = False, False < True  -> lo = 4
lo=4  hi=6   mid = (4 + 6) // 2 = 5   isBadVersion(5) = True, not < True     -> hi = 5
lo=4  hi=5   mid = (4 + 5) // 2 = 4   isBadVersion(4) = True, not < True     -> hi = 4
lo=4  hi=4   loop ends -> insertion point 4
```

The insertion point `4` is the leftmost position whose key is `True`, so the call returns `4`, matching the expected Output. Note the upper bound: `hi` starts at `6` (the length of `range(n + 1)`) rather than `5`, so this run probes versions `3, 5, 4` where the hand-written search probed only `3, 4`; both stay within `O(log n)` calls.

#### Solution

The code hands the walkthrough's halving loop to the library: one `bisect_left` call over the lazy `range`.

```python
import bisect

# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        return bisect.bisect_left(range(n + 1), True, lo=1, key=isBadVersion)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

`bisect_left` runs a binary search and therefore calls the key on `O(log n)` versions, matching the hand-written approach.

##### Space Complexity: `O(1)`

`range` is a lazy sequence and `bisect` keeps only a constant amount of state.

#### Key Insights

- The `key` parameter on `bisect` functions (Python 3.10+) lets a binary search
  run over a predicate without building a parallel array.
- It expresses the same logic as the hand-written search in one line, but relies
  on the standard library to do the boundary work.
- `lo=1` keeps version `0` (which does not exist) out of the search space.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `O(n)` - one API call per version up to the boundary.
- **Binary Search**: `O(log n)` - halves the range each step.
- **Bisect**: `O(log n)` - the same binary search inside the standard library.

### Space Complexity

- **Linear Scan**: `O(1)` - a single loop counter.
- **Binary Search**: `O(1)` - three integer pointers.
- **Bisect**: `O(1)` - a lazy `range` and constant `bisect` state.

### Trade-offs

- Linear Scan is trivial to reason about but makes the maximum number of API
  calls, exactly what the problem forbids at scale.
- Binary Search adds the small mental overhead of boundary handling in exchange
  for the optimal call count and no library dependency.
- Bisect is the most concise but hides the boundary logic behind a stdlib call
  and requires Python 3.10+ for the `key` argument.

### When to Use Each

- **Linear Scan**: Only to confirm correctness or when `n` is tiny; never for
  the real constraints.
- **Binary Search**: The right call for interviews and production; it is optimal
  and dependency-free (Recommended).
- **Bisect**: When you want the shortest idiomatic code and a modern Python
  runtime is guaranteed.

### Optimization Notes

- Compute `mid` as `lo + (hi - lo) // 2` rather than `(lo + hi) // 2` to avoid
  integer overflow in fixed-width integer languages.
- Updating `hi = mid` (inclusive) instead of `hi = mid - 1` is what makes the
  search find the first bad version instead of overshooting it.
- All logarithmic approaches make the same number of API calls; choose between
  them on readability and runtime version, not performance.
