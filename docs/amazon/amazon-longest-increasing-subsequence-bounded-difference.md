# [Longest Increasing Subsequence With Bounded Adjacent Difference](https://www.fastprep.io/problems/amazon-longest-increasing-subsequence-bounded-difference)

**Hard** | **NN minutes** | **Array, Dynamic Programming, Segment Tree**

Given a non-empty integer array arr and a non-negative integer k, return the maximum length of a subsequence that satisfies all of the following:

The selected values are strictly increasing.The difference between every pair of consecutive selected values is at most k.The selected values preserve their relative order in arr.A subsequence may delete any number of elements without changing the order of the remaining elements.

## Examples

### Example 1

**Input:** `arr = [7,1,4,5,8,8,10,6,7,7,7,8]`, `k = 4`

**Output:** `6`

**Explanation:** One longest valid subsequence is [1,4,5,6,7,8]. It preserves input order, every adjacent difference is at most 4, and its length is 6.

### Example 2

**Input:** `arr = [3,1,2,6,10,11,4,5]`, `k = 3`

**Output:** `4`

**Explanation:** The subsequence [1,2,4,5] is strictly increasing, preserves input order, and has adjacent differences 1, 2, and 1.

### Example 3

**Input:** `arr = [5,4,3,2,1]`, `k = 2`

**Output:** `1`

**Explanation:** No two values form a strictly increasing pair in subsequence order, so every valid longest subsequence contains one value.

## Constraints

- `1 <= arr.length <= 2 * 10^5`
- `-10^9 <= arr[i] <= 10^9`
- `0 <= k <= 2 * 10^9`

## Solutions

### Bottom-Up DP

#### Derivation

The classic [longest increasing subsequence](../leetcode/longest_increasing_subsequence.md) question transfers with one extra clause. Anchor on the last element: any valid chain has a last value, and the chain ending at index `i` must extend some shorter valid chain whose last value `arr[j]` sits strictly below `arr[i]` and within reach of the difference bound. Both demands fold into one window: `arr[j] >= arr[i] - k` and `arr[j] <= arr[i] - 1`. Since every chain ending at `i` only builds on chains ending earlier, the answers fill left to right with a plain double loop:

1. Let `dp[i]` be the length of the longest valid chain ending at index `i`;
   seed every entry at `1`, the element alone.
2. Sweep `i` left to right; for each `i`, sweep `j` from `0` through `i - 1`
   and extend wherever `arr[i] - k <= arr[j] <= arr[i] - 1`.
3. Return `max(dp)`, the best chain over all ending points.

#### Recurrence

Let `dp[i]` be the length of the longest valid chain ending at index `i`:

$$ dp[i] = 1 + \max\limits_{j < i,\ \ arr[i] - k \,\le\, arr[j] \,\le\, arr[i] - 1} dp[j] $$

```text
dp[i] = 1 + max(dp[j] : j < i and arr[i] - k <= arr[j] <= arr[i] - 1)
        (max over an empty set reads 0, so dp[i] never drops below 1)
answer = max(dp)
```

The window's two edges carry the problem's two rules at once: the upper edge `arr[j] <= arr[i] - 1` is strictness, the lower edge `arr[j] >= arr[i] - k` is the bounded difference. The answer is read from the largest entry, because a longest chain can end at any index.

#### Walkthrough

Example 2: `arr = [3,1,2,6,10,11,4,5]`, `k = 3`. Each row lists the earlier values inside the window `[arr[i] - 3, arr[i] - 1]` and the best chain they offer:

```text
start   dp = [1, 1, 1, 1, 1, 1, 1, 1]    every dp[i] = 1: the element alone
i=0 (3)   window [0, 2]   no earlier element          dp[0] = 1
i=1 (1)   window [-2, 0]  3 outside the window        dp[1] = 1
i=2 (2)   window [-1, 1]  1 qualifies: dp[1] + 1 = 2  dp[2] = 2
i=3 (6)   window [3, 5]   3 qualifies: dp[0] + 1 = 2  dp[3] = 2
i=4 (10)  window [7, 9]   3,1,2,6 all outside         dp[4] = 1
i=5 (11)  window [8, 10]  10 qualifies: dp[4] + 1 = 2 dp[5] = 2
i=6 (4)   window [1, 3]   3 -> 1; 1 -> 1; 2 -> 2+1=3  dp[6] = 3
i=7 (5)   window [2, 4]   2 -> 2+1=3; 4 -> 3+1=4      dp[7] = 4
answer = max(dp) = 4
```

The winner is the chain ending at the final `5`: `dp[7] = 4` extends the chain `1, 2, 4` recorded at `dp[6] = 3`, and indeed `[1, 2, 4, 5]` is a longest valid subsequence, matching the expected Output for Example 2. (The same fill returns `6` for Example 1.)

#### Solution

The code is the table fill from the walkthrough: seed every entry at `1`, then run the double loop over the window condition.

```python
from typing import List


class Solution:
    def solve(self, arr: List[int], k: int) -> int:
        length = len(arr)
        dp = [1] * length
        for i in range(length):
            for j in range(i):
                if arr[i] - k <= arr[j] <= arr[i] - 1:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

The nested sweeps pair every index with every earlier index once, `n × (n - 1) / 2` window checks with constant work each.

##### Space Complexity: `O(n)`

The `dp` table stores one entry per index.

#### Key Insights

- The whole problem is the classic LIS recurrence plus one window edge: `arr[j] < arr[i]` becomes the pair of edges `arr[i] - k <= arr[j] <= arr[i] - 1`.
- The window condition is checkable in constant time per pair, so the double loop needs no preprocessing; that simplicity is the baseline's whole appeal.
- Correct on every input the constraints allow, but at `n = 200000` the quadratic pair count is roughly `2 × 10^10` checks, far past interview-feasible time; the inner question needs a faster answer.

### Segment Tree with Coordinate Compression

#### Derivation

The table's inner loop re-answers one question for every `i`: among chains ending on a value inside the window `[arr[i] - k, arr[i] - 1]`, which is longest? Pre-answer it per value instead of per pair. Keep one slot per possible value holding the best chain length that ends on that value so far; then each element needs a range max over its window plus one slot write. A [segment tree](https://en.wikipedia.org/wiki/Segment_tree) answers both in `O(log n)` on the value axis, and coordinate compression keeps the tree small: only the `n` array values themselves can ever hold a chain, so each value maps to its rank in the sorted distinct values, and the window endpoints are located with two insertion-point searches (`bisect_left` for the window's lower edge, `bisect_right` past its upper edge):

1. Build `values = sorted(set(arr))` and a max segment tree `chain_tree` of
   `len(values)` slots, every slot starting at `0` (no chain yet).
2. For each `value` in `arr`: map the window to ranks with
   `low_rank = bisect_left(values, value - k)` and
   `high_rank = bisect_right(values, value - 1) - 1`.
3. `chain_length = chain_tree.range_max(low_rank, high_rank) + 1`: the best
   chain reachable from `value`, plus `value` itself. An empty window reads `0`
   and yields the element-alone chain of length `1`.
4. Write `chain_length` into the tree at `bisect_left(values, value)` and track
   the best `chain_length` in `longest`.
5. Return `longest`.

The processing order makes correctness automatic: when `value` queries the tree, the tree holds exactly the chains ending at strictly earlier indices, so "value window" and "earlier position" are enforced by the same mechanism.

#### Walkthrough

Example 2 again: `arr = [3,1,2,6,10,11,4,5]`, `k = 3`. Compression sorts the distinct values into `[1, 2, 3, 4, 5, 6, 10, 11]`, so a value's rank is its position there. Each line is one loop step: the value, its rank window, what the tree holds there, and the write:

```text
value 3   window [0, 2]    ranks 0, 1, 2 empty                    max 0 -> chain 1   write rank 2 <- 1
value 1   window [-2, 0]   rank 0 empty                           max 0 -> chain 1   write rank 0 <- 1
value 2   window [-1, 1]   rank 0 (value 1) holds 1               max 1 -> chain 2   write rank 1 <- 2
value 6   window [3, 5]    rank 2 (value 3) holds 1               max 1 -> chain 2   write rank 5 <- 2
value 10  window [7, 9]    no array value lies in 7..9            max 0 -> chain 1   write rank 6 <- 1
value 11  window [8, 10]   rank 6 (value 10) holds 1              max 1 -> chain 2   write rank 7 <- 2
value 4   window [1, 3]    ranks 0,1,2 hold 1,2,1                 max 2 -> chain 3   write rank 3 <- 3
value 5   window [2, 4]    ranks 2,3 hold 1,3                     max 3 -> chain 4   write rank 4 <- 4
answer = 4
```

The last step is the payoff: `5` reaches into the window holding `2` (chain 2) and `4` (chain 3), takes the max `3`, and lands on chain length `4`. Every intermediate number matches the `dp` table of the bottom-up walkthrough; the tree simply keeps the per-value bests findable in logarithmic time. The same run on Example 1 returns `6`.

#### Solution

The code is the walkthrough's loop over a `MaxSegmentTree` that keeps one maximum per value rank.

```python
import bisect
from typing import List


class MaxSegmentTree:
    def __init__(self, size: int) -> None:
        self.size = size
        self.tree = [0] * (4 * size)

    def update(self, rank: int, chain_length: int) -> None:
        self._update(1, 0, self.size - 1, rank, chain_length)

    def _update(self, node: int, node_low: int, node_high: int, rank: int,
                chain_length: int) -> None:
        if node_low == node_high:
            self.tree[node] = max(self.tree[node], chain_length)
            return
        middle = (node_low + node_high) // 2
        if rank <= middle:
            self._update(2 * node, node_low, middle, rank, chain_length)
        else:
            self._update(2 * node + 1, middle + 1, node_high, rank, chain_length)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def range_max(self, low: int, high: int) -> int:
        if low > high:
            return 0
        return self._query(1, 0, self.size - 1, low, high)

    def _query(self, node: int, node_low: int, node_high: int, low: int,
               high: int) -> int:
        if low <= node_low and node_high <= high:
            return self.tree[node]
        middle = (node_low + node_high) // 2
        best = 0
        if low <= middle:
            best = max(best, self._query(2 * node, node_low, middle, low, high))
        if middle < high:
            best = max(best, self._query(2 * node + 1, middle + 1, node_high,
                                         low, high))
        return best


class Solution:
    def solve(self, arr: List[int], k: int) -> int:
        values = sorted(set(arr))
        chain_tree = MaxSegmentTree(len(values))
        longest = 0

        for value in arr:
            low_rank = bisect.bisect_left(values, value - k)
            high_rank = bisect.bisect_right(values, value - 1) - 1
            chain_length = chain_tree.range_max(low_rank, high_rank) + 1
            longest = max(longest, chain_length)
            chain_tree.update(bisect.bisect_left(values, value), chain_length)

        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each of the `n` elements performs two insertion-point searches and one segment tree query plus update, all `O(log n)` on at most `n` ranks.

##### Space Complexity: `O(n)`

The sorted distinct values and the segment tree's array both scale with the number of distinct values, at most `n`.

#### Key Insights

- Coordinate compression bounds the tree by what can matter: only array values ever hold a chain, so `n` ranks suffice even though values span `2 × 10^9`.
- The two `bisect` calls translate the value window `[value - k, value - 1]` into rank space in one step; `bisect_right` past the upper edge is what makes the window's strictness exact.
- The `range_max` guard `low > high` absorbs empty windows (`k = 0`, or every candidate value missing from the array) and returns the chain-of-one baseline `0 + 1`.
- One pass suffices because the tree only contains chains from earlier indices: the position rule and the value rule collapse into the update-then-query discipline.

## Comparison of Solutions

### Time Complexity

- **Bottom-Up DP**: `O(n²)` - every index pairs with every earlier index for one window check.
- **Segment Tree with Coordinate Compression**: `O(n log n)` - per element, logarithmic rank lookups, range max, and update.

### Space Complexity

- **Bottom-Up DP**: `O(n)` - one `dp` entry per index.
- **Segment Tree with Coordinate Compression**: `O(n)` - the sorted distinct values plus the segment tree array.

### Trade-offs

- **Bottom-Up DP**: the recurrence written as code, trivially correct and ten lines long, but the quadratic pair count is unusable at the `2 × 10^5` constraint scale.
- **Segment Tree with Coordinate Compression**: meets the constraints comfortably, but carries a data structure, two rank mappings, and an empty-window guard that each need defending.

### When to Use Each

- **Bottom-Up DP**: while reasoning out the problem, as the reference oracle for small inputs, and whenever the array is known to stay short (a few thousand elements).
- **Segment Tree with Coordinate Compression (Recommended)**: whenever the stated constraints apply: it is the only one of the two that finishes `n = 200000` in time.

### Optimization Notes

- The window translation is the page's correctness crux: `bisect_left(values, value - k)` through `bisect_right(values, value - 1) - 1` is exact even when neither endpoint is an array value; off-by-one there fails silently on duplicates.
- The segment tree stores only maxima and needs no lazy propagation, because each element contributes exactly one point update.
- Rebuilding the tree is unnecessary across calls if the array is reused; the tree's `0` initialization doubles as the "no chain ends here yet" state.
- The same shape (compress values, keep a per-value aggregate, query a value window) solves the whole family of bounded-difference chain problems, including the non-strict variant where the window widens to `[value - k, value]`.
