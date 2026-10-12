# [Minimum Cost to Convert Products to Variant A](https://www.fastprep.io/problems/amazon-minimum-cost-to-convert-products-to-variant-a)

**Medium** | **NN minutes** | **Array, Sliding Window, Greedy**

An inventory array product contains only 0 and 1, where 0 represents variant A and 1 represents variant B.

In one operation, choose a subarray of length k. The cost of that operation is the sum of the values inside the chosen subarray. Then choose one index inside that subarray whose value is 1 and change it to 0.

Return the minimum total cost needed to convert every product to variant A.

Function Description Complete the function minCostToConvertAllToVariantA in the editor below.

minCostToConvertAllToVariantA has the following parameters:

int[] product: the product variantsint k: the fixed operation window lengthReturns int: the minimum total cost.

## Examples

### Example 1

**Input:** `product = [1, 1, 1]`, `k = 2`

**Output:** `4`

**Explanation:** Use window [0, 1] twice, then window [1, 2] once. The costs are 2 + 1 + 1 = 4.

### Example 2

**Input:** `product = [1, 0, 1]`, `k = 2`

**Output:** `2`

**Explanation:** Choose the left window once to clear the first 1, and the right window once to clear the last 1.

## Constraints

- `product[i] is either 0 or 1`
- `1 <= k <= product.length`
- `Each operation must change exactly one 1 inside the chosen window to 0.`

## Solutions

### Simulate Every Operation Plan

#### Derivation

Each operation picks a length-k window and one of its 1s to clear; the cost is the window's current 1-count. The baseline explores the full decision tree: windows that contain at least one 1, times the choice of which 1 to clear, until no 1s remain:

1. Recurse over (window, cleared position) choices.
2. Each node pays the window's current count.
3. Return the cheapest path to the all-zero state.

#### Walkthrough

Example 1, `product = [1,1,1]`, `k = 2`: the plan window `[0,1]` (cost 2, clear position 0), then `[0,1]` (cost 1, clear position 1), then `[1,2]` (cost 1, clear position 2) totals 4. No cheaper path exists: the first operation necessarily pays at least 2 (every window covering a 1 holds two of them), and two more clearings remain. Example 2, `[1,0,1]`, `k = 2`: the left window clears the first 1 at cost 1, the right window clears the last at cost 1, total 2.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, product: List[int], k: int) -> int:
        """Return the minimum total cost to clear every 1.

        Time:  Exponential in the number of 1s: a branch per (window,
            cleared position) pair at every step.
        Space: O(number of 1s) recursion depth.
        """
        best = [float("inf")]

        def explore(state: List[int], total: int) -> None:
            if total >= best[0]:
                return
            if sum(state) == 0:
                best[0] = total
                return
            for start in range(len(state) - k + 1):
                window = state[start : start + k]
                window_cost = sum(window)
                if window_cost == 0:
                    continue
                for offset in range(k):
                    if window[offset] == 1:
                        nxt = list(state)
                        nxt[start + offset] = 0
                        explore(nxt, total + window_cost)

        explore(product, 0)
        return int(best[0])
```

#### Time and Space Complexity Analysis

##### Time Complexity: Exponential in the number of 1s

Every node branches over covering windows times clearable positions; only toy inventories run this rung.

##### Space Complexity: `O(number of 1s)`

The recursion depth plus one state copy per level.

#### Key Insights

- A window's cost counts the 1s still inside it, so clearing inside a busy window early is expensive and re-using it gets cheaper.
- The definitional search doubles as the oracle for the memoized rung.

### Memoize on the Remaining Ones

#### Derivation

The array's zeros never matter; the state is exactly the set of uncleared positions. Writing the state as a bitmask over the 1-positions, the recursion becomes: pick any window covering at least one remaining 1, pay the count of remaining 1s inside it, clear one of them, recurse. Memoizing on the mask collapses repeated states (different clearing orders reaching the same set). One structural fact guides the choices: within a fixed window, clearing its `j` remaining ones one per operation costs `j + (j-1) + ... + 1 = j(j+1)/2` when nothing outside interferes, so the optimizer is really choosing window-shaped groups and their clearing order:

1. Index the 1-positions.
2. `solve(mask)` = minimum over covering windows and covered positions of `count_in_window + solve(mask minus that position)`.
3. Memoize per mask.

#### Walkthrough

The statement examples: `[1,1,1]`, `k = 2` yields 4 as above. A subtler case shows the grouping: `product = [1,0,0,1,1,0]`, `k = 5` (two windows, `[0..4]` and `[1..5]`). The ones sit at 0, 3, 4. Clearing all three inside `[0..4]` costs `3 + 2 + 1 = 6`; the optimum clears 3 and 4 first inside `[1..5]` (which excludes the 1 at 0) for `2 + 1 = 3`, then clears the lone 0 inside `[0..4]` for 1, totaling 4. The memo finds this by exploring the `[1..5]` branch first at the states where it is cheapest.

#### Solution

```python
from functools import lru_cache
from typing import List


class Solution:
    def solve(self, product: List[int], k: int) -> int:
        """Return the minimum total cost to clear every 1.

        Time:  O(2^j * (n * k)) with j the number of 1s: each mask
            explores every window and covered position.
        Space: O(2^j) masks memoized.
        """
        n = len(product)
        ones = [position for position, value in enumerate(product) if value == 1]
        if not ones:
            return 0
        bit_of = {position: bit for bit, position in enumerate(ones)}
        full_mask = (1 << len(ones)) - 1

        @lru_cache(maxsize=None)
        def explore(mask: int) -> int:
            if mask == 0:
                return 0
            remaining = [ones[bit] for bit in range(len(ones)) if mask >> bit & 1]
            remaining_set = set(remaining)
            best = float("inf")
            for start in range(n - k + 1):
                window = range(start, start + k)
                covered = [position for position in remaining if position in window]
                if not covered:
                    continue
                for position in covered:
                    candidate = len(covered) + explore(mask & ~(1 << bit_of[position]))
                    if candidate < best:
                        best = candidate
            return best

        return explore(full_mask)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^j * n * k)` with `j` the count of 1s

Each of the `2^j` masks scans windows and their covered positions.

##### Space Complexity: `O(2^j)`

One memo entry per mask.

#### Key Insights

- Only the set of remaining 1s distinguishes states; the zeros are scenery.
- A window isolating `j` ones costs `j(j+1)/2` to drain, which is why the optimizer prefers windows that exclude distant ones before clearing them.
- Clearing order inside one window is forced (any order pays the same staircase sum), so the real choice is which window group to drain first.

## Comparison of Solutions

### Time Complexity

- **Simulate Every Operation Plan**: exponential without memoization; fine up to a handful of 1s.
- **Memoize on the Remaining Ones**: `O(2^j * n * k)`; polynomial in the array, exponential only in the 1-count.

### Space Complexity

- **Simulate Every Operation Plan**: `O(j)` depth.
- **Memoize on the Remaining Ones**: `O(2^j)`.

### Trade-offs

- The brute force states the operation semantics outright.
- The memoized rung scales to dozens of 1s and exposes the staircase-cost structure.

### When to Use Each

- **Simulate Every Operation Plan**: the oracle in tests.
- **Memoize on the Remaining Ones**: any input where the 1-count is moderate.

### Optimization Notes

- Symmetric masks (mirror-image positions under some window) could share answers, but the window geometry rarely admits the symmetry in practice.
- When every window of the array has the same 1-count shape (all 1s contiguous at one end), the staircase sum alone answers the question without search.
