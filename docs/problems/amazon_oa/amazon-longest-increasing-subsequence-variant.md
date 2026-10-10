# [Longest Increasing Subsequence](https://www.fastprep.io/problems/amazon-longest-increasing-subsequence-variant)

**Medium** | **NN minutes** | **Array, Binary Search, Dynamic Programming**

Given an integer array nums, return the length of its longest strictly increasing subsequence.

## Examples

### Example 1

**Input:** `nums = [10,9,2,5,3,7,101,18]`

**Output:** `4`

**Explanation:** One longest strictly increasing subsequence is [2, 3, 7, 101], which has length 4.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-longest-increasing-subsequence-variant; fill them in. -->

## Solutions

### Brute Force

#### Derivation

The most literal reading enumerates subsequences directly: walk the array left to right holding the last value taken, and at each element make the two possible moves. Skipping keeps the previous value and moves on; taking is allowed only when the current value is strictly greater than the last taken one, and it then becomes the value every later element must beat. The recursion returns the longest chain obtainable from the remaining elements:

1. Define `best(position, previous)` as the longest strictly increasing
   subsequence length usable from index `position` onward, with every taken
   value strictly greater than `previous`.
2. Base case: `position == len(nums)` means no elements remain, so
   return `0`.
3. Skip branch: `best(position + 1, previous)`.
4. Take branch: allowed only when `nums[position] > previous`, worth
   `1 + best(position + 1, nums[position])`.
5. Return `max(skip, take)`; the answer is `best(0, -inf)`.

Nothing is shared between routes, so each element's two branches fork again on every path that reaches it: the recursion generates all `2^n` subsequences of positions.

#### Walkthrough

The recursion tree on Example 1 (`nums = [10,9,2,5,3,7,101,18]`) has `2^8` leaves, far too wide to draw, so trace a tailored input instead: `nums = [1, 3, 2]`, which exercises a blocked take (the `2` cannot follow a route already holding `3`) and two restarts. Each line is a call returning; children print above their parent:

```text
      best(3, -inf) -> 0    base case: no elements left
      best(3, 2) -> 0    base case: no elements left
    best(2, -inf) -> 1    skip = 0, take = 1 + best(3, 2) = 1, keep take
      best(3, 3) -> 0    base case: no elements left
    best(2, 3) -> 0    skip = 0, take blocked: 2 <= 3, keep skip
  best(1, -inf) -> 1    skip = 1, take = 1 + best(2, 3) = 1, keep skip
      best(3, 1) -> 0    base case: no elements left
      best(3, 2) -> 0    base case: no elements left
    best(2, 1) -> 1    skip = 0, take = 1 + best(3, 2) = 1, keep take
      best(3, 3) -> 0    base case: no elements left
    best(2, 3) -> 0    skip = 0, take blocked: 2 <= 3, keep skip
  best(1, 1) -> 1    skip = 1, take = 1 + best(2, 3) = 1, keep skip
best(0, -inf) -> 2    skip = 1, take = 1 + best(1, 1) = 2, keep take
-> 2
```

The root takes `1`, which lets the suffix choose between `3` and `2`, each worth one more element: `best(0, -inf)` returns `2`, and indeed the longest strictly increasing subsequences of `[1, 3, 2]` (`[1, 3]` and `[1, 2]`) both have length `2`. Note how `best(2, 3)` runs twice and the base calls carry `previous` values `-inf, 2, 3, 1, 2, 3` yet all return `0`: repeated questions answered identically on separate routes, which is exactly the waste the next approach caches away.

#### Solution

The code is the walkthrough's two branches around the exhausted-index base case.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        def best(position: int, previous: float) -> int:
            if position == len(nums):
                return 0
            skip = best(position + 1, previous)
            take = 0
            if nums[position] > previous:
                take = 1 + best(position + 1, nums[position])
            return max(skip, take)

        return best(0, float("-inf"))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each call forks into a skip branch and, whenever the take is legal, a take branch, so the tree roughly doubles per element: up to `2^n` leaves, one per subsequence. Nothing is remembered between routes, so every branch pays in full.

##### Space Complexity: `O(n)`

No table is kept; the recursion stack reaches depth `n` along the all-take chain.

#### Key Insights

- The `previous` value alone summarizes the past: a future element extends
  the chain exactly when it beats the last taken value, so no other history
  matters.
- The strict comparison `nums[position] > previous` encodes "strictly
  increasing"; equal values block the take.
- Correct on every input but exponential: the same suffix question is
  re-derived once per route, which is what the DP version keys on.

### Bottom-Up DP

#### Derivation

The brute force's flaw is re-deriving the same suffix answer on different routes. Re-anchor the question to the element: the longest chain that *ends* at index `i` depends only on `i` and the answers before it, because such a chain must extend some chain ending at a smaller earlier value. Since every call only needs earlier indices, the answers fill naturally from the array's start, which [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) tabulates with a plain left-to-right loop and no recursion:

1. Let `dp[i]` be the length of the longest strictly increasing subsequence
   ending at index `i`; seed every entry at `1`, the element alone.
2. Sweep `i` left to right; for each `i`, sweep `j` from `0` through `i - 1`
   and extend wherever `nums[j] < nums[i]`.
3. Return `max(dp)`, the best chain over all ending points.

#### Recurrence

Let `dp[i]` be the length of the longest strictly increasing subsequence ending at index `i`:

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

Let us fill the table on Example 1: `nums = [10,9,2,5,3,7,101,18]`. Only the inner-loop comparisons that change or set `dp[i]` are listed; `dp` is shown after the sweep:

```text
start   dp = [1, 1, 1, 1, 1, 1, 1, 1]    every dp[i] = 1: the element alone
i=1 (9)    no earlier element below 9                        dp[1] = 1
i=2 (2)    no earlier element below 2                        dp[2] = 1
i=3 (5)    2 < 5: dp[2] + 1 = 2                              dp[3] = 2
i=4 (3)    2 < 3: dp[2] + 1 = 2                              dp[4] = 2
i=5 (7)    2 < 7: 2; 5 < 7: dp[3] + 1 = 3; 3 < 7: dp[4] + 1 = 3   dp[5] = 3
i=6 (101)  every earlier value is below 101: dp[5] + 1 = 4   dp[6] = 4
i=7 (18)   every value except 101 is below 18: dp[5] + 1 = 4  dp[7] = 4
answer = max(dp) = 4
```

The equal-value and greater-value comparisons (`10 < 9`, `9 < 5`, `101 < 18`) fail silently and are skipped. Row `7` extends `dp[5] = 3` (the chain `2, 3, 7`) with `18`, and row `6` extends the same chain with `101`, so the longest chains are `[2, 3, 7, 101]` and `[2, 3, 7, 18]`, and `max(dp) = 4`, matching the expected Output for Example 1.

#### Solution

The code is the table fill from the walkthrough: seed every entry at `1`, then run the double loop.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        length = len(nums)
        dp = [1] * length
        for i in range(1, length):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

The nested sweeps pair every index with every earlier index exactly once, a total of `n × (n - 1) / 2` comparisons with constant work each.

##### Space Complexity: `O(n)`

The `dp` table stores one entry per index.

#### Key Insights

- Seeding at `1` folds the recurrence's base case into the table, so no
  empty-array or single-element guard survives.
- The final `max` over all entries is not a detail: a longest chain can end
  anywhere, and the last element's entry can be small.
- The inner scan exists only to answer one question, "what is the best chain
  whose tail is below `nums[i]`?"; the next approach keeps that question
  pre-answered.

### Patience Sorting with Binary Search

#### Derivation

The table's inner loop re-finds the same thing for every `i`: the longest chain among those whose tail is below `nums[i]`. Keep one summary per chain length instead: for each length `k`, only the smallest value any increasing subsequence of length `k` seen so far ends on, in a list `tails` where `tails[k - 1]` is that value for length `k`. Two facts make the list tiny and searchable: it is strictly increasing (a longer chain needs a larger tail), and a new element `number` can only matter in two ways. It either extends the longest chain (it exceeds every tail, so it is appended) or it becomes a better, smaller tail for the shortest chain it can join. Both amount to one operation: find the leftmost tail that is `>= number` and overwrite it, or append when no such tail exists. A [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) over the sorted `tails` finds that slot in `O(log n)`:

1. Start `tails` empty.
2. For each `number`, binary-search `tails` for the leftmost index with
   `tails[index] >= number`.
3. If no such index exists (`index == len(tails)`), append `number`: a chain
   one longer than any before now exists, ending at `number`.
4. Otherwise write `number` into `tails[index]`: a chain of length
   `index + 1` now ends on the smaller value `number`.
5. After the loop, `len(tails)` is the length of the longest strictly
   increasing subsequence.

#### Invariant

`tails[k - 1]` is always the smallest possible tail of a strictly increasing subsequence of length `k` among the elements processed so far, and `tails` is strictly increasing:

```text
tails[k - 1] = smallest tail among all increasing subsequences
               of length k seen so far
tails        = strictly increasing
```

Each branch preserves it. Appending happens only when `number` exceeds every tail, so it forms a chain one longer than any before, and minimality holds because `number` is the only new tail. Overwriting `tails[low]` with `number` happens when `tails[low - 1] < number <= tails[low]`: the chain of length `low + 1` that ended at `tails[low]` now ends at the smaller `number`, sortedness survives because `number` still exceeds `tails[low - 1]`, and no shorter chain's tail is touched. At loop exit the invariant covers all elements, and the longest chain's length is exactly `len(tails)`: a chain of that length exists (its tail sits in the list), and the strictly increasing `tails` cannot hold more entries than the longest chain allows.

#### Walkthrough

Let us trace Example 1: `nums = [10,9,2,5,3,7,101,18]`. Each element's slot comes from the binary search for the leftmost tail at or above it:

```text
number = 10   tails = []                       append              tails = [10]
number = 9    leftmost tail >= 9 is tails[0]   overwrite with 9    tails = [9]
number = 2    leftmost tail >= 2 is tails[0]   overwrite with 2    tails = [2]
number = 5    exceeds every tail               append              tails = [2, 5]
number = 3    leftmost tail >= 3 is tails[1]   overwrite with 3    tails = [2, 3]
number = 7    exceeds every tail               append              tails = [2, 3, 7]
number = 101  exceeds every tail               append              tails = [2, 3, 7, 101]
number = 18   leftmost tail >= 18 is tails[3]  overwrite with 18   tails = [2, 3, 7, 18]
answer = len(tails) = 4
```

The final overwrite is the invariant at work: `18` cannot extend a length-4 chain, because extending means beating the tail `101` and `18` does not, so it becomes the smaller tail for length 4 and `tails` stops growing. `len(tails) = 4` matches the expected Output for Example 1, and `tails` itself (`[2, 3, 7, 18]`) is not required to be a real subsequence of positions, only its length is meaningful.

#### Solution

The code is the walkthrough's per-element step: binary-search for the leftmost tail at or above `number`, then append or overwrite.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        tails: List[int] = []
        for number in nums:
            low, high = 0, len(tails)
            while low < high:
                middle = (low + high) // 2
                if tails[middle] < number:
                    low = middle + 1
                else:
                    high = middle
            if low == len(tails):
                tails.append(number)
            else:
                tails[low] = number
        return len(tails)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each of the `n` elements runs one binary search over `tails`, which never exceeds `n` entries: `O(log n)` per element.

##### Space Complexity: `O(n)`

The `tails` list holds at most one entry per chain length, `n` at most.

#### Key Insights

- `tails` is not itself an increasing subsequence of `nums`; the overwrites
  rewrite history no real chain follows, and the invariant is what licenses
  that.
- The leftmost `>= number` slot is the strictness rule in disguise: an equal
  tail is overwritten rather than appended past, so equal values never
  lengthen a chain.
- This is the patience card game rule: place each card on the leftmost pile
  whose top is at least it, and the pile count is the answer.

### Patience Sorting with bisect

#### Derivation

The hand-written search walks the standard binary search skeleton to find the leftmost index with `tails[index] >= number`. That is precisely what [`bisect.bisect_left`](https://docs.python.org/3/library/bisect.html) computes: the leftmost insertion point for `number` in a sorted list. Swapping it in deletes the loop and leaves the per-element decision, append or overwrite, exactly as before:

1. Keep `tails` and the per-element decision verbatim.
2. Replace the `low`/`high` loop with
   `index = bisect.bisect_left(tails, number)`.
3. Append when `index == len(tails)`, otherwise overwrite `tails[index]`.

#### Walkthrough

The library search lands on the same slots the hand-written one traced, Example 1 again: `nums = [10,9,2,5,3,7,101,18]`:

```text
number = 10   bisect_left([], 10) = 0            append              tails = [10]
number = 9    bisect_left([10], 9) = 0           overwrite tails[0]  tails = [9]
number = 2    bisect_left([9], 2) = 0            overwrite tails[0]  tails = [2]
number = 5    bisect_left([2], 5) = 1            append              tails = [2, 5]
number = 3    bisect_left([2, 5], 3) = 1         overwrite tails[1]  tails = [2, 3]
number = 7    bisect_left([2, 3], 7) = 2         append              tails = [2, 3, 7]
number = 101  bisect_left([2, 3, 7], 101) = 3    append              tails = [2, 3, 7, 101]
number = 18   bisect_left([2, 3, 7, 101], 18) = 3  overwrite tails[3]  tails = [2, 3, 7, 18]
answer = len(tails) = 4
```

Every index matches the hand-rolled search's slot, the final `18` again overwrites the `101` tail, and `len(tails) = 4` matches the expected Output for Example 1.

#### Solution

The patience algorithm with the library's binary search standing in for the loop.

```python
import bisect
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        tails: List[int] = []
        for number in nums:
            index = bisect.bisect_left(tails, number)
            if index == len(tails):
                tails.append(number)
            else:
                tails[index] = number
        return len(tails)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

One `bisect_left` per element over a list of at most `n` entries; the library search runs the same comparison count as the hand-written loop.

##### Space Complexity: `O(n)`

The `tails` list holds at most one entry per chain length.

#### Key Insights

- `bisect_left(tails, number)` returns the leftmost slot with
  `tails[index] >= number`, exactly the strictness-preserving slot;
  `bisect_right` would place `number` after equal tails and wrongly
  lengthen chains on duplicates such as `[7, 7, 7, 7]`.
- The algorithm is unchanged from the hand-rolled version; only the search's
  bookkeeping moved into the library.
- Recovering an actual subsequence, not just its length, needs extra
  predecessor bookkeeping on top of either patience variant.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^n)` - the recursion enumerates subsequences, one leaf each.
- **Bottom-Up DP**: `O(n²)` - the double sweep pairs every index with every earlier index.
- **Patience Sorting with Binary Search**: `O(n log n)` - one binary search per element.
- **Patience Sorting with bisect**: `O(n log n)` - the library's `bisect_left` per element.

### Space Complexity

- **Brute Force**: `O(n)` - recursion stack only.
- **Bottom-Up DP**: `O(n)` - the `dp` table.
- **Patience Sorting with Binary Search**: `O(n)` - the `tails` list.
- **Patience Sorting with bisect**: `O(n)` - the `tails` list.

### Trade-offs

- The Brute Force is the direct transcription of "take or skip" and needs no auxiliary structure, but it is the only approach here that misses any reasonable constraint budget.
- The Bottom-Up DP computes every chain-ending answer, which variants and follow-up queries can reuse; the patience pair computes only the length.
- The patience pair gives up the table and wins a `log n` factor; the hand-written search shows the bisected invariant, the `bisect` call is shorter and identical in asymptotics.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for checking the faster versions on tiny inputs.
- **Bottom-Up DP** (recommended): when per-index answers are wanted or the interviewer extends the problem, and as the cleanest statement of the recurrence; switch to the patience pair when only the length is needed and `n` runs large.
- **Patience Sorting with Binary Search**: the fastest from-scratch answer, with the tails invariant stated and searched by hand.
- **Patience Sorting with bisect**: the Pythonic tidy-up of the same algorithm when `bisect` is available.

### Optimization Notes

- The inner scan of the `O(n²)` DP and the binary search of the patience variants answer the same question; the tails invariant is what turns a scan over `i` candidates into a search over `log n` chain lengths.
- `bisect_left`, not `bisect_right`: on duplicates the left search overwrites the equal tail (no length change), the right search would insert past it and inflate the answer for inputs like `[7, 7, 7, 7]`.
- The `tails` list is sorted as a consequence of the invariant, not by an explicit sort; each write lands at a binary-searched slot, so sortedness is preserved by construction.
- For the longest *non-decreasing* subsequence variant, the comparison becomes `tails[middle] > number` in the hand-written search, which is `bisect_right` on the same list.
