# [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)

**Medium** | **25 minutes** | **Array, Binary Search, Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Longest increasing subsequence](https://en.wikipedia.org/wiki/Longest_increasing_subsequence) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm)

**Practice:** [`practice/longest_increasing_subsequence/solution.py`](../../practice/longest_increasing_subsequence/solution.py)

Given an integer array `nums`, return the *length* of the longest strictly *increasing* subsequence.

A **subsequence** is a sequence that can be derived from the given sequence by deleting some or no elements  without changing the relative order of the remaining characters.

* For example, `"cat"` is a subsequence of `"crabt"`.

## Examples

### Example 1

**Input:** `nums = [9,1,4,2,3,3,7]`

**Output:** `4`

**Explanation:** The longest increasing subsequence is [1,2,3,7], which has a length of 4.

### Example 2

**Input:** `nums = [0,3,1,3,2,3]`

**Output:** `4`

## Constraints

- `1 <= nums.length <= 1000`
- `-1000 <= nums[i] <= 1000`

## Deriving the Solution

Deleting elements never disturbs the order of those that remain, so an increasing subsequence is a set of positions `i1 < i2 < ... < ik` with `nums[i1] < nums[i2] < ... < nums[ik]`, and the question is how long such a set can be. Every solution below decides the same thing per element: what is the best increasing chain that uses this element, or that lives inside the elements before it.

1. **Start literal.** Walk the array once and, at each element, branch: skip it,
   or take it and forbid every later value at or below it. Every subsequence is
   generated, so the answer falls out, at `O(2^n)` branches: see
   [Brute Force](#brute-force).
2. **Spot the waste.** Different routes reach the same element carrying the same
   "last taken value", so the same suffix question is answered again and again.
   Re-anchor the question to the element instead of the route: the longest chain
   *ending* at index `i` depends only on `i` and the answers before it. Cache
   that per index, `O(n^2)`: see [Top-Down Memoization](#top-down-memoization).
3. **Flip the direction.** The cached answers fill from the array's start
   anyway, since the shortest prefixes are decided first: tabulate the same
   relation with a plain left-to-right loop: see
   [Bottom-Up DP](#bottom-up-dp).
4. **Search instead of scan.** The table's inner loop scans every earlier `j`
   just to find the best chain whose tail is below `nums[i]`. Keep one summary
   per chain length instead: the smallest tail a chain of that length can end
   on. Those tails are sorted, so each element finds its slot by binary search
   and the whole run drops to `O(n log n)`: see
   [Patience Sorting with Binary Search](#patience-sorting-with-binary-search).
5. **Hand the search to the library.** The hand-written binary search is
   `bisect_left`: see
   [Patience Sorting with bisect](#patience-sorting-with-bisect).

## Solutions

### Brute Force

#### Derivation

The most literal reading enumerates subsequences directly: walk left to right holding the value last taken, and at each element make the two possible moves. Skipping keeps the previous value and moves on; taking is allowed only when the current value beats the last taken one, and it then becomes the value every later element must beat. The recursion returns the longest chain obtainable from the remaining elements:

1. Define `best(i, previous)` as the longest increasing subsequence length usable
   from index `i` onward, with every taken value strictly greater than `previous`.
2. Base case: `i == len(nums)` means no elements remain, so return `0`.
3. Skip branch: `best(i + 1, previous)`.
4. Take branch: allowed only when `nums[i] > previous`, worth
   `1 + best(i + 1, nums[i])`.
5. Return `max(skip, take)`; the answer is `best(0, -inf)`.

Nothing is shared between routes, so each element's two branches fork again on every path that reaches it: the recursion generates all `2^n` subsequences of positions.

#### Walkthrough

The recursion tree on either example is far too wide to draw, so trace a tailored input instead: `nums = [1, 3, 2]`, which exercises a blocked take (`3` can never follow `3`) and two restarts. Each line is a call returning; children print above their parent:

```text
      best(3, -inf) -> 0    base case: no elements left
      best(3, 2) -> 0    base case: no elements left
    best(2, -inf) -> 1    skip = 0, take = 1 + best(3, 2) = 1, keep take
      best(3, 3) -> 0    base case: no elements left
    best(2, 3) -> 0    skip = 0, take = blocked: nums[i] <= previous, keep skip
  best(1, -inf) -> 1    skip = 1, take = 1 + best(2, 3) = 1, keep skip
      best(3, 1) -> 0    base case: no elements left
      best(3, 2) -> 0    base case: no elements left
    best(2, 1) -> 1    skip = 0, take = 1 + best(3, 2) = 1, keep take
      best(3, 3) -> 0    base case: no elements left
    best(2, 3) -> 0    skip = 0, take = blocked: nums[i] <= previous, keep skip
  best(1, 1) -> 1    skip = 1, take = 1 + best(2, 3) = 1, keep skip
best(0, -inf) -> 2    skip = 1, take = 1 + best(1, 1) = 2, keep take
-> 2
```

The root takes `1`, which lets the suffix decide between `3` and `2`, each worth one more element: `best(0, -inf)` returns `2`, and indeed the longest increasing subsequences of `[1, 3, 2]`, `[1, 3]` and `[1, 2]` all have length `2`. Note how `best(2, 3)` runs twice, and the six base calls carry `previous` values `-inf, 2, 3, 1, 2, 3` (`best(3, -inf)` runs once) yet all return `0`: repeated questions answered identically on separate routes, which is exactly the waste the next solution caches away.

#### Solution

The code is the walkthrough's two branches around the exhausted-index base case.

```python
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        def best(i: int, previous: float) -> int:
            if i == len(nums):
                return 0
            skip = best(i + 1, previous)
            take = 0
            if nums[i] > previous:
                take = 1 + best(i + 1, nums[i])
            return max(skip, take)

        return best(0, float("-inf"))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each call forks into a skip branch and, whenever the take is legal, a take branch, so the tree roughly doubles per element: up to `2^n` leaves, one per subsequence. Nothing is remembered between routes, so every branch pays in full.

##### Space Complexity: `O(n)`

No table is kept; the recursion stack reaches depth `n` along the all-take chain.

#### Key Insights

- The `previous` value alone summarizes the past: any future element beats the chain
  exactly when it beats the last taken value, so no other history matters.
- The strict comparison `nums[i] > previous` encodes the "strictly increasing" rule;
  equal values block the take.
- Correct on every input but exponential: the same `(i, previous)` state is
  re-derived once per route, which is what the memoized version keys on.

### Top-Down Memoization

#### Derivation

The Brute Force's state is the pair `(i, previous)`, and identical pairs recur across routes. Re-anchor the question to remove the redundancy: instead of asking about a suffix with a constraint inherited from the route, ask about a prefix with the chain pinned to its last element. Define `lis(i)` as the length of the longest increasing subsequence that *ends* at index `i`. That answer depends only on `i` and the earlier answers, because the chain ending at `i` must extend some chain ending at a smaller value before it:

1. Keep a `memo` dictionary keyed by the index.
2. Compute `lis(i)` as `1` plus the best `lis(j)` over `j < i` with
   `nums[j] < nums[i]`, or plain `1` when no such `j` exists.
3. Store `memo[i]` before returning, so every later request is a lookup.
4. No single `lis(i)` is guaranteed to be the overall answer: a longest chain can
   end anywhere, so return the maximum of `lis(i)` over all `i`.

Each index computes its body once and every other mention is a dictionary hit, which turns the exponential fan-out into one `O(i)` scan per index.

#### Walkthrough

Trace Example 1: `nums = [9, 1, 4, 2, 3, 3, 7]`. The answer loop calls `lis(0)` through `lis(6)` in order, and each call scans `j` ascending; compute lines print after their children, and marked lines are memo hits:

```text
lis(0) -> 1    no earlier smaller element, memo[0] = 1
lis(1) -> 1    no earlier smaller element, memo[1] = 1
  lis(1) -> 1    ** memo hit **
lis(2) -> 2    1 + lis(1), memo[2] = 2
  lis(1) -> 1    ** memo hit **
lis(3) -> 2    1 + lis(1), memo[3] = 2
  lis(1) -> 1    ** memo hit **
  lis(3) -> 2    ** memo hit **
lis(4) -> 3    1 + lis(3), memo[4] = 3
  lis(1) -> 1    ** memo hit **
  lis(3) -> 2    ** memo hit **
lis(5) -> 3    1 + lis(3), memo[5] = 3
  lis(1) -> 1    ** memo hit **
  lis(2) -> 2    ** memo hit **
  lis(3) -> 2    ** memo hit **
  lis(4) -> 3    ** memo hit **
  lis(5) -> 3    ** memo hit **
lis(6) -> 4    1 + lis(4), memo[6] = 4
answer = max over i = 4
```

Every request for an already-decided index is answered from `memo`, so each of the seven bodies runs exactly once: `lis(6)` reaches `4` via `1 + lis(4)` (`3 + 7`), with `1 + lis(5)` tying at the same length and the leftward scan keeping the first winner, and the answer loop reports `max(1, 1, 2, 2, 3, 3, 4) = 4`, matching the expected Output for Example 1.

#### Solution

The code is the cached ending-at-`i` scan: one pass per index over its smaller predecessors.

```python
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        memo = {}

        def lis(i: int) -> int:
            if i in memo:
                return memo[i]
            length = 1
            for j in range(i):
                if nums[j] < nums[i]:
                    length = max(length, lis(j) + 1)
            memo[i] = length
            return length

        return max(lis(i) for i in range(n))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` indices runs its body once and scans the `i` indices before it, giving `1 + 2 + ... + (n - 1)` comparisons; every other call is a constant-time dictionary hit.

##### Space Complexity: `O(n)`

The memo holds one entry per index, and the recursion stack reaches depth `n` along the strictly increasing chain `0, 1, ..., n - 1`.

#### Key Insights

- Pinning the chain to its last element is what makes the state a single index:
  the value comparison `nums[j] < nums[i]` replaces the recursive `previous`
  bookkeeping entirely.
- The final `max` over all indices is not an optimization detail: `lis(n - 1)`
  can be small (a tiny last element) while the longest chain ends in the middle.
- The recurrence is the same one the Brute Force explored; only the sharing of
  results changed, which is why the correctness argument carries over untouched.

### Bottom-Up DP

#### Derivation

The memoized recursion fills its cache from the array's start anyway: `lis(0)` is decided first, then `lis(1)`, and so on, because every call only needs earlier indices. [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) with tabulation produces that same table in that same order with a plain loop and no recursion at all:

1. Let `dp[i]` be the length of the longest increasing subsequence ending at
   index `i`, matching `lis(i)` exactly; seed every entry at `1`, the element
   alone.
2. Sweep `i` left to right; for each `i`, sweep `j` from `0` to `i - 1` and
   apply the recurrence wherever `nums[j] < nums[i]`.
3. Return `max(dp)`, the best chain over all ending points.

#### Recurrence

Let `dp[i]` be the length of the longest increasing subsequence ending at index `i`:

$$ dp[i] = \begin{cases}
1, & \text{no } j < i \text{ with } nums[j] < nums[i] \\[4pt]
1 + \max\limits_{j < i,\ nums[j] < nums[i]} dp[j], & \text{otherwise}
\end{cases} $$

```text
dp[i] = 1                                                   when no earlier element is smaller
dp[i] = 1 + max(dp[j] : j < i and nums[j] < nums[i])        otherwise
answer = max(dp)
```

The base case is the element alone: a chain of length `1` always exists. The answer is read from the largest entry, because a longest chain can end at any index.

#### Walkthrough

Let us fill the table on Example 2: `nums = [0, 3, 1, 3, 2, 3]`. Every comparison of the inner loop is one row; `dp` is shown after each `i` finishes:

```text
start   dp = [1, 1, 1, 1, 1, 1]    every dp[i] = 1: the element alone
i = 1  j = 0   nums[0] = 0 < 3   dp[0] + 1 = 2   dp[1] = max(1, 2) = 2
i = 1 done   dp = [1, 2, 1, 1, 1, 1]
i = 2  j = 0   nums[0] = 0 < 1   dp[0] + 1 = 2   dp[2] = max(1, 2) = 2
i = 2  j = 1   nums[1] = 3 < 1 is false: skip
i = 2 done   dp = [1, 2, 2, 1, 1, 1]
i = 3  j = 0   nums[0] = 0 < 3   dp[0] + 1 = 2   dp[3] = max(1, 2) = 2
i = 3  j = 1   nums[1] = 3 < 3 is false: skip
i = 3  j = 2   nums[2] = 1 < 3   dp[2] + 1 = 3   dp[3] = max(2, 3) = 3
i = 3 done   dp = [1, 2, 2, 3, 1, 1]
i = 4  j = 0   nums[0] = 0 < 2   dp[0] + 1 = 2   dp[4] = max(1, 2) = 2
i = 4  j = 1   nums[1] = 3 < 2 is false: skip
i = 4  j = 2   nums[2] = 1 < 2   dp[2] + 1 = 3   dp[4] = max(2, 3) = 3
i = 4  j = 3   nums[3] = 3 < 2 is false: skip
i = 4 done   dp = [1, 2, 2, 3, 3, 1]
i = 5  j = 0   nums[0] = 0 < 3   dp[0] + 1 = 2   dp[5] = max(1, 2) = 2
i = 5  j = 1   nums[1] = 3 < 3 is false: skip
i = 5  j = 2   nums[2] = 1 < 3   dp[2] + 1 = 3   dp[5] = max(2, 3) = 3
i = 5  j = 3   nums[3] = 3 < 3 is false: skip
i = 5  j = 4   nums[4] = 2 < 3   dp[4] + 1 = 4   dp[5] = max(3, 4) = 4
i = 5 done   dp = [1, 2, 2, 3, 3, 4]
answer = max(dp) = 4
```

The equal-value rows (`3 < 3` is false) are the strictness rule at work: a chain cannot extend through an equal element. The last row extends `dp[4] = 3` (`0, 1, 2`) with the final `3`, so `max(dp) = 4`, matching the expected Output for Example 2.

#### Solution

The code is the table fill from the walkthrough: seed every entry at `1`, then run the double loop.

```python
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        # dp[i] = longest increasing subsequence ending at index i
        dp = [1] * n
        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The nested sweeps pair every index with every earlier index exactly once, a total of `n * (n - 1) / 2` comparisons with constant work each.

##### Space Complexity: `O(n)`

The `dp` table stores one entry per index.

#### Key Insights

- Seeding at `1` folds the recurrence's base case into the table, so no empty
  or single-element guard survives.
- The inner scan exists only to answer one question: "what is the best chain
  whose tail is below `nums[i]`?" The next solution keeps that question
  pre-answered.
- The full table costs `O(n)` space but makes every prefix's answer available,
  which variants that ask "best chain ending at `i`" get for free.

### Patience Sorting with Binary Search

#### Derivation

The table's inner loop re-finds the same thing for every `i`: the longest chain among those whose tail is below `nums[i]`. Summaries can answer that without scanning. Keep, for each chain length `k`, only the smallest value any increasing subsequence of length `k` seen so far ends on, in a list `tails` where `tails[k - 1]` is that value for length `k`. Two facts make the list tiny and searchable: it is sorted in increasing order (a longer chain needs a larger tail), and a new element `num` can only matter in two ways. It either extends the longest chain (it exceeds every tail, so it is appended), or it becomes a better, smaller tail for the shortest chain it can join. Both amount to one operation: find the leftmost tail that is `>= num` and overwrite it, or append when no such tail exists. A [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) over the sorted `tails` finds that slot in `O(log n)`:

1. Start `tails` empty.
2. For each `num`, binary-search `tails` for the leftmost index with
   `tails[index] >= num`.
3. If no such index exists (`index == len(tails)`), append `num`: a chain one
   longer than any before now exists, ending at `num`.
4. Otherwise write `num` into `tails[index]`: a chain of length
   `index + 1` now ends on the smaller value `num`.
5. After the loop, `len(tails)` is the length of the longest increasing
   subsequence.

#### Invariant

`tails[k - 1]` is always the smallest possible tail of a strictly increasing subsequence of length `k` among the elements processed so far, and `tails` is strictly increasing:

$$ \text{tails}[k-1] = \min \{\, x : \text{some increasing subsequence of length } k \text{ so far ends at } x \,\} $$

```text
tails[k - 1] = smallest tail among all increasing subsequences
               of length k seen so far
tails        = strictly increasing
```

Each branch preserves it. Appending happens only when `num` is greater than every tail, so it forms a chain one longer than any before, and minimality holds because `num` is the only new tail. Overwriting `tails[index]` with `num` happens when `tails[index - 1] < num <= tails[index]`: the chain of length `index + 1` that ended at `tails[index]` now ends at the smaller `num`, sortedness survives because `num` still exceeds `tails[index - 1]`, and no shorter chain's tail is touched. At loop exit the invariant covers all elements, and the longest chain's length is exactly `len(tails)`: a chain of that length exists (its tail sits in the list), and the strictly increasing `tails` cannot hold more entries than the longest chain allows.

#### Walkthrough

Trace Example 1: `nums = [9, 1, 4, 2, 3, 3, 7]`. Each element runs the binary search over the current `tails`; the search's `lo`/`hi` evolution is shown per iteration:

```text
num =  9
      lo=0 hi=0 loop ends -> return 0
    index == len(tails): append   tails = [9]
num =  1
      lo=0 hi=1 mid=0 tails[0]=9 >= 1 -> hi = mid = 0
      lo=0 hi=0 loop ends -> return 0
    replace tails[0] with 1   tails = [1]
num =  4
      lo=0 hi=1 mid=0 tails[0]=1 < 4  -> lo = mid + 1 = 1
      lo=1 hi=1 loop ends -> return 1
    index == len(tails): append   tails = [1, 4]
num =  2
      lo=0 hi=2 mid=1 tails[1]=4 >= 2 -> hi = mid = 1
      lo=0 hi=1 mid=0 tails[0]=1 < 2  -> lo = mid + 1 = 1
      lo=1 hi=1 loop ends -> return 1
    replace tails[1] with 2   tails = [1, 2]
num =  3
      lo=0 hi=2 mid=1 tails[1]=2 < 3  -> lo = mid + 1 = 2
      lo=2 hi=2 loop ends -> return 2
    index == len(tails): append   tails = [1, 2, 3]
num =  3
      lo=0 hi=3 mid=1 tails[1]=2 < 3  -> lo = mid + 1 = 2
      lo=2 hi=3 mid=2 tails[2]=3 >= 3 -> hi = mid = 2
      lo=2 hi=2 loop ends -> return 2
    replace tails[2] with 3   tails = [1, 2, 3]
num =  7
      lo=0 hi=3 mid=1 tails[1]=2 < 7  -> lo = mid + 1 = 2
      lo=2 hi=3 mid=2 tails[2]=3 < 7  -> lo = mid + 1 = 3
      lo=3 hi=3 loop ends -> return 3
    index == len(tails): append   tails = [1, 2, 3, 7]
answer = len(tails) = 4
```

The second `3` is the strictness case: it lands on `tails[2] = 3` and overwrites it with itself, a no-op, because `3` cannot extend the length-3 chain, only join it. The final `7` exceeds every tail and appends, so `len(tails) = 4`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's per-element step: binary search for the leftmost tail at or above `num`, then append or overwrite.

```python
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails: List[int] = []
        for num in nums:
            lo, hi = 0, len(tails)
            while lo < hi:
                mid = (lo + hi) // 2
                if tails[mid] < num:
                    lo = mid + 1
                else:
                    hi = mid
            if lo == len(tails):
                tails.append(num)
            else:
                tails[lo] = num
        return len(tails)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each of the `n` elements runs one binary search over `tails`, which never exceeds `n` entries: `O(log n)` per element.

##### Space Complexity: `O(n)`

The `tails` list holds at most one entry per chain length, `n` at most.

#### Key Insights

- `tails` is not itself an increasing subsequence of `nums`; only its length is
  meaningful. The overwrite steps rewrite history that no real chain follows,
  and the invariant is what licenses that.
- The leftmost `>= num` slot is the strictness rule in disguise: an equal tail
  is overwritten rather than appended, so equal values never lengthen a chain.
- This is the patience-card-game rule: place each card on the leftmost pile
  whose top is at least it, and the pile count is the answer.

### Patience Sorting with bisect

#### Derivation

The hand-written search walks the standard [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) skeleton to find the leftmost index with `tails[index] >= num`. That is precisely what [`bisect.bisect_left`](https://docs.python.org/3/library/bisect.html) computes: the leftmost insertion point for `num` in a sorted list. Swapping it in deletes the loop and leaves the per-element decision, append or overwrite, exactly as before:

1. Keep `tails` and the per-element step verbatim.
2. Replace the `lo`/`hi` loop with
   `index = bisect.bisect_left(tails, num)`.
3. Append when `index == len(tails)`, otherwise overwrite `tails[index]`.

#### Walkthrough

The bisect search lands on the same slots the hand-written one traced, Example 1 again: `nums = [9, 1, 4, 2, 3, 3, 7]`:

```text
num =  9   bisect_left(tails, 9) = 0   append   tails = [9]
num =  1   bisect_left(tails, 1) = 0   replace tails[0]   tails = [1]
num =  4   bisect_left(tails, 4) = 1   append   tails = [1, 4]
num =  2   bisect_left(tails, 2) = 1   replace tails[1]   tails = [1, 2]
num =  3   bisect_left(tails, 3) = 2   append   tails = [1, 2, 3]
num =  3   bisect_left(tails, 3) = 2   replace tails[2]   tails = [1, 2, 3]
num =  7   bisect_left(tails, 7) = 3   append   tails = [1, 2, 3, 7]
answer = len(tails) = 4
```

Every index matches the hand-rolled search's return, the duplicate `3` again overwrites itself, and `len(tails) = 4` matches the expected Output for Example 1.

#### Solution

The patience algorithm with the library's binary search standing in for the loop.

```python
import bisect
from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails: List[int] = []
        for num in nums:
            index = bisect.bisect_left(tails, num)
            if index == len(tails):
                tails.append(num)
            else:
                tails[index] = num
        return len(tails)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

One `bisect_left` per element over a list of at most `n` entries; the library search runs the same comparison count as the hand-written loop.

##### Space Complexity: `O(n)`

The `tails` list holds at most one entry per chain length.

#### Key Insights

- `bisect_left(tails, num)` returns the leftmost slot with `tails[index] >= num`,
  which is exactly the strictness-preserving slot; `bisect_right` would place
  `num` after equal tails and wrongly lengthen chains on duplicates.
- The algorithm is unchanged from the hand-rolled version; only the search's
  bookkeeping moved into the library.
- Recovering an actual subsequence (not just its length) needs extra
  predecessor bookkeeping on top of either patience variant.

## Comparison of Solutions

The practice harness's `practice/longest_increasing_subsequence/reference.py` implements the **Patience Sorting with Binary Search** solution.

### Time Complexity

- **Brute Force**: `O(2^n)` - the recursion enumerates subsequences, one leaf each.
- **Top-Down Memoization**: `O(n^2)` - one body per index, scanning its smaller predecessors.
- **Bottom-Up DP**: `O(n^2)` - the same work as a double sweep, no recursion.
- **Patience Sorting with Binary Search**: `O(n log n)` - one binary search per element.
- **Patience Sorting with bisect**: `O(n log n)` - the library's `bisect_left` per element.

### Space Complexity

- **Brute Force**: `O(n)` - recursion stack only.
- **Top-Down Memoization**: `O(n)` - memo entries plus the stack.
- **Bottom-Up DP**: `O(n)` - the `dp` table.
- **Patience Sorting with Binary Search**: `O(n)` - the `tails` list.
- **Patience Sorting with bisect**: `O(n)` - the `tails` list.

### Trade-offs

- The Brute Force is the direct transcription of "pick or skip" and needs no
  auxiliary structure, but it is the only approach here that misses the
  constraint budget for long inputs.
- Both `O(n^2)` DP versions compute every chain-ending answer, which variants
  and follow-up queries can reuse; the patience pair computes only the length.
- The patience pair gives up the table and wins a `log n` factor; the
  hand-written search shows the bisected invariant, the `bisect` call is shorter
  and identical in asymptotics.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for
  checking the faster versions on tiny inputs.
- **Top-Down Memoization**: when the ending-at-`i` recurrence is easiest to
  trust in its recursive form and inputs stay modest.
- **Bottom-Up DP**: when per-index answers are wanted, or as the cleanest
  statement of the recurrence before optimizing.
- **Patience Sorting with Binary Search** (recommended): the default; `O(n log n)`
  with the tails invariant stated and searched by hand, no library dependency.
- **Patience Sorting with bisect**: the Pythonic tidy-up of the same algorithm
  when `bisect` is available.

### Optimization Notes

- The inner scan of the `O(n^2)` DP and the binary search of the patience
  variants answer the same question; the invariant is what turns a scan over
  `i` candidates into a search over `log n` chain lengths.
- `bisect_left`, not `bisect_right`: on duplicates the left search overwrites the
  equal tail (no length change), the right search would insert past it and
  inflate the answer for inputs like `[2, 2]`.
- The `tails` list is sorted as a consequence of the invariant, not by an
  explicit sort; each write lands at a binary-searched slot, so sortedness is
  preserved by construction.
- For the longest *non-decreasing* subsequence variant, the comparison becomes
  `tails[index] > num` (append past equals), which is `bisect_right` on the same
  list.
