# [Maximize K-Element AND with an Increment Budget](https://www.fastprep.io/problems/amazon-maximize-k-element-and-with-increment-budget)

**Hard** | **NN minutes** | **Array, Bit Manipulation, Greedy, Sorting**

You are given an array nums, an integer k, and a nonnegative increment budget budget. You may increase array elements by nonnegative integer amounts whose total is at most budget.

After applying the increments, choose exactly k distinct array positions. Return the maximum possible bitwise AND of the chosen values.

You do not need to return the chosen positions or the increment allocation.

## Examples

### Example 1

**Input:** `nums = [5,4,1,7,2]`, `k = 3`, `budget = 3`

**Output:** `6`

**Explanation:** Increase 4 to 6 and 5 to 6. Choosing 6, 6, 7 gives 6 & 6 & 7 = 6.

### Example 2

**Input:** `nums = [1,2,3]`, `k = 2`, `budget = 0`

**Output:** `2`

**Explanation:** Without increments, choose 2 and 3; their bitwise AND is 2.

### Example 3

**Input:** `nums = [0,0]`, `k = 2`, `budget = 2`

**Output:** `1`

**Explanation:** Increase both values to 1. Their bitwise AND is 1.

## Constraints

- `1 <= nums.length <= 200000.`
- `1 <= k <= nums.length.`
- `0 <= nums[i] <= 1000000000.`
- `0 <= budget <= 1000000000.`
- `All arithmetic fits in a signed 64-bit integer.`

## Solutions

### Exhaustive Allocation

#### Derivation

The definitional baseline enumerates the whole choice space: which `k` positions, and how the budget splits among them. Increments are "at most" the budget, so every total from `0` to `budget` is tried, splitting each total across the chosen positions in every way:

1. For each size-`k` subset of positions, and each total in `0..budget`, enumerate every split of the total.
2. Apply the split, AND the chosen values, and keep the maximum seen.

The enumeration is factorial in the budget and combinatorial in `n`, so it only runs on the page's toy examples; its value is being the oracle that licenses the greedy rung below.

#### Walkthrough

Example 2, `nums = [1,2,3]`, `k = 2`, `budget = 0`: only the empty allocation exists; the pairs AND to `1 & 2 = 0`, `1 & 3 = 1`, `2 & 3 = 2`, so the best is `2`. Example 3, `nums = [0,0]`, `k = 2`, `budget = 2`: the split `(1, 1)` raises both values to `1`, whose AND is `1`; no split reaches a higher AND because both values must carry the same bits and the budget tops out at `2`. Example 1's search space (`10` subsets times `20` splits) confirms `6` the same way.

#### Solution

```python
from itertools import combinations
from typing import List, Tuple


class Solution:
    def solve(self, nums: List[int], k: int, budget: int) -> int:
        """Return the best AND of k values using at most the budget.

        Time:  O(C(n, k) * budget^k * k): a toy-scale oracle, unusable at
            the stated constraints.
        Space: O(k) per trial.
        """

        def allocations(total: int, slots: int) -> List[Tuple[int, ...]]:
            if slots == 1:
                return [(total,)]
            spread: List[Tuple[int, ...]] = []
            for give in range(total + 1):
                for rest in allocations(total - give, slots - 1):
                    spread.append((give,) + rest)
            return spread

        best = 0
        for positions in combinations(range(len(nums)), k):
            for total in range(budget + 1):
                for alloc in allocations(total, len(positions)):
                    trial = list(nums)
                    for position, add in zip(positions, alloc):
                        trial[position] += add
                    combined = trial[positions[0]]
                    for position in positions[1:]:
                        combined &= trial[position]
                    best = max(best, combined)
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C(n, k) * budget^k * k)`

Splits of a total across `k` slots grow polynomially in the budget and factorially in `k`; the rung exists for validation, not scale.

##### Space Complexity: `O(k)`

One split tuple and one trial list at a time.

#### Key Insights

- "At most budget" means enumerating every total from zero; forcing exact spending would miss cheaper achievable targets.
- The oracle's output on the examples pins the target the fast rung must reproduce.

### Bit-Greedy Over the Mask

#### Derivation

Two observations collapse the search. First, the answer is a mask: the AND of the chosen values has exactly the bits those values all share, so asking "which masks are achievable within budget" is the whole question. Second, the cheapest way to raise one value `value` so the result is at least `value` and contains every bit of a candidate mask is a single high-to-low scan: copy `value`'s bits while they satisfy the mask, and at the first mask bit `value` lacks, set it and copy the mask's remaining bits (taking the mask's low bits keeps the raised number as small as possible while still containing the mask). Bits are then tried from the highest down, each tested against the mask already accepted: keep the bit exactly when the `k` cheapest raise costs sum within the budget. High-to-low order makes the greedy safe: an accepted bit outweighs every combination of lower bits, so no later acceptance can compensate for an earlier rejection, and every rejection is final.

1. For each bit from high to low, form the candidate mask (accepted mask plus the bit).
2. Price each element's cheapest raise onto the candidate mask.
3. Keep the bit when the `k` cheapest prices sum to at most `budget`.

#### Walkthrough

Example 1, `nums = [5,4,1,7,2]`, `k = 3`, `budget = 3`. Bit 2 (`100`): raising onto `100` costs `5 -> 5` (0), `4 -> 4` (0), `1 -> 4` (3), `7 -> 7` (0), `2 -> 4` (2); the three cheapest are `0 + 0 + 0 = 0 <= 3`, kept. Bit 1 (`110`): costs are `7 -> 7` (0), `5 -> 6` (1), `4 -> 6` (2), `2 -> 6` (4), `1 -> 6` (5); the three cheapest sum to `0 + 1 + 2 = 3 <= 3`, kept, using the whole budget on `5` and `4` while `7` rides free. Bit 0 (`111`): costs are `7 -> 7` (0), `5 -> 7` (2), `4 -> 7` (3), `2 -> 7` (5), `1 -> 7` (6); the three cheapest sum to `5 > 3`, rejected. The final mask is `110 = 6`, matching the expected output. Example 2 confirms rejection under a zero budget (only bits already common to some pair survive, and `2 & 3 = 2` is the largest), and Example 3 confirms acceptance of bit 0 alone (`0 -> 1` twice costs exactly `2`).

#### Solution

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], k: int, budget: int) -> int:
        """Return the largest AND of k values reachable within the budget.

        Time:  O(32 * n log n): each bit trial prices and sorts every
            element's raise cost.
        Space: O(n) for the per-trial cost list.
        """

        def raise_cost(value: int, mask: int) -> int:
            raised = 0
            diverged = False
            for bit in range(31, -1, -1):
                if diverged:
                    raised |= mask & (1 << bit)
                elif mask & (1 << bit) and not value & (1 << bit):
                    raised |= 1 << bit
                    diverged = True
                else:
                    raised |= value & (1 << bit)
            return raised - value

        mask = 0
        for bit in range(31, -1, -1):
            candidate = mask | (1 << bit)
            costs = sorted(raise_cost(value, candidate) for value in nums)
            if sum(costs[:k]) <= budget:
                mask = candidate
        return mask
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(32 * n log n)`

Thirty-two bit trials, each sorting `n` small-integer costs; at `n <= 200000` this is a few million comparisons.

##### Space Complexity: `O(n)`

One cost list per trial.

#### Key Insights

- The cheapest raise onto a mask is one high-to-low scan: copy until the first missing mask bit, then follow the mask; a value already containing the mask costs nothing.
- Testing each bit against the accumulated mask, high to low, is what makes rejections final: a kept bit outweighs all lower bits combined.
- The same `k` cheapest costs decide every bit, so a partial-selection pass (`heapq.nsmallest`) would replace the full sort without changing the asymptotics.

## Comparison of Solutions

### Time Complexity

- **Exhaustive Allocation**: `O(C(n, k) * budget^k * k)` - toy scale only.
- **Bit-Greedy Over the Mask**: `O(32 * n log n)` - the production rung at the stated constraints.

### Space Complexity

- **Exhaustive Allocation**: `O(k)`.
- **Bit-Greedy Over the Mask**: `O(n)`.

### Trade-offs

- The oracle is definitionally correct but explodes with the budget; the greedy needs the raise-cost scan and the high-to-low argument to be trusted.
- The greedy prices all `n` elements per bit although only the `k` cheapest matter; a selection pass trims the constant.

### When to Use Each

- **Exhaustive Allocation**: as the practice-gauntlet oracle on small random inputs, cross-checking the greedy.
- **Bit-Greedy Over the Mask**: always, at the constraints' scale.

### Optimization Notes

- `sum(costs[:k])` only needs the `k` smallest costs; `heapq.nsmallest(k, ...)` avoids sorting all `n`.
- The raise-cost scan can stop at the candidate mask's highest set bit, trimming the loop for sparse masks.
