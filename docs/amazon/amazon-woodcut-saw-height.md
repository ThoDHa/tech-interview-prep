# [Maximum Saw Height for At Least M Cut Length](https://www.fastprep.io/problems/amazon-woodcut-saw-height)

**Medium** | **NN minutes** | **Array, Binary Search**

You have vertical wooden poles with integer heights heights. Set a saw to a non-negative integer height h; every pole taller than h contributes height - h units of wood, and shorter poles contribute nothing.

Given requiredWood, return the largest saw height that collects at least that much wood.

## Examples

### Example 1

**Input:** `heights = [20,15,10,17]`, `requiredWood = 7`

**Output:** `15`

**Explanation:** At height 15 the cuts yield 5 + 0 + 0 + 2 = 7. Raising the saw would yield too little.

### Example 2

**Input:** `heights = [4,42,40,26,46]`, `requiredWood = 20`

**Output:** `36`

**Explanation:** Height 36 yields 6 + 4 + 10 = 20 units from the three taller poles.

### Example 3

**Input:** `heights = [5]`, `requiredWood = 5`

**Output:** `0`

**Explanation:** The only way to collect all five units is to place the saw at ground level.

## Constraints

- `1 <= heights.length <= 100000.`
- `1 <= heights[i] <= 10^9.`
- `1 <= requiredWood <= min(2 * 10^9, sum(heights)).`

## Solutions

### Scan Every Saw Height

#### Derivation

The collected wood is a function of the saw height alone: `wood(h) = sum(max(0, pole - h))`. It starts at `sum(heights)` for `h = 0`, falls strictly or weakly as `h` grows, and reaches zero above the tallest pole. The baseline scans every candidate height in that range and keeps the largest whose yield meets `requiredWood`:

1. For each `h` from `0` to `max(heights)`, sum the cut lengths.
2. Track the largest `h` with `wood(h) >= requiredWood`.

#### Walkthrough

Example 1, `heights = [20,15,10,17]`, `requiredWood = 7`: `wood(15) = 5 + 0 + 0 + 2 = 7` meets the requirement while `wood(16) = 4 + 0 + 0 + 1 = 5` falls short, so the answer is `15`. Example 3, `heights = [5]`, `requiredWood = 5`: only ground level collects all five units, giving `0`.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, heights: List[int], requiredWood: int) -> int:
        """Return the largest saw height collecting the required wood.

        Time:  O(max(heights) * n): every candidate height rescans the
            poles.
        Space: O(1).
        """
        best = 0
        for candidate in range(max(heights) + 1):
            wood = sum(pole - candidate for pole in heights if pole > candidate)
            if wood >= requiredWood:
                best = candidate
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(heights) * n)`

With heights up to `10^9`, the scan is astronomically long; it exists as the definition and the oracle.

##### Space Complexity: `O(1)`

One running sum at a time.

#### Key Insights

- `wood(h)` is nonincreasing in `h`: raising the saw never adds wood.
- The answer is the last height still meeting the requirement along that falling curve.

### Binary Search on the Saw Height

#### Derivation

The monotone fall invites binary search: find the largest `h` with `wood(h) >= requiredWood`. Each probe prices one linear scan. Because the predicate flips from true to false exactly once, the standard upper-bound search closes onto the boundary; note the predicate is "meets or exceeds", so the search keeps the largest satisfying height rather than the first failing one:

1. Search between `0` and `max(heights)`.
2. Probe the middle (biased upward, since the true branch sits lower): if the yield meets the requirement, the answer is at least `middle`; otherwise it is strictly smaller.
3. Return the closed boundary.

#### Walkthrough

Example 2, `heights = [4,42,40,26,46]`, `requiredWood = 20`: the window opens `[0, 46]`. Probe 23: `19 + 17 + 3 = 39 >= 20`, feasible, window `[23, 46]`. Probe 35: `7 + 5 + 11 = 23 >= 20`, window `[35, 46]`. Probe 41: `1 + 5 = 6 < 20`, window `[35, 40]`. Probe 38: `4 + 2 + 8 = 14 < 20`, window `[35, 37]`. Probe 37: `5 + 3 + 9 = 17 < 20`, window `[35, 36]`. Probe 36: `6 + 4 + 10 = 20 >= 20`, window `[36, 36]`: the answer is `36`, matching the expected output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, heights: List[int], requiredWood: int) -> int:
        """Return the largest saw height collecting the required wood.

        Time:  O(n * log(max(heights))): log-range probes, each a linear
            yield scan.
        Space: O(1).
        """

        def wood_at(candidate: int) -> int:
            return sum(pole - candidate for pole in heights if pole > candidate)

        low, high = 0, max(heights)
        while low < high:
            middle = (low + high + 1) // 2
            if wood_at(middle) >= requiredWood:
                low = middle
            else:
                high = middle - 1
        return low
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * log(max(heights)))`

About thirty probes at the stated ceiling, each linear.

##### Space Complexity: `O(1)`

Two bounds and a running sum.

#### Key Insights

- Monotonicity converts a height range of `10^9` into roughly thirty probes.
- The upward-biased middle avoids the classic infinite loop when the window shrinks to two adjacent heights.
- The result never exceeds `max(heights)`: above it no pole contributes, so the requirement (at least `1`) cannot hold.

## Comparison of Solutions

### Time Complexity

- **Scan Every Saw Height**: `O(max(heights) * n)` - unusable at the stated ceiling.
- **Binary Search on the Saw Height**: `O(n * log(max(heights)))`.

### Space Complexity

- **Scan Every Saw Height**: `O(1)`.
- **Binary Search on the Saw Height**: `O(1)`.

### Trade-offs

- The scan needs no correctness argument beyond the definition; the search needs the monotone-fall observation.
- Both probes price identically; the search simply probes logarithmically often.

### When to Use Each

- **Scan Every Saw Height**: cross-checking the search on small random inputs.
- **Binary Search on the Saw Height**: the stated constraints.

### Optimization Notes

- Sorting the poles once lets each probe binary-search the cut prefix and sum via prefix sums, making a probe `O(log n)` after `O(n log n)` setup; worthwhile when many queries share the poles.
- Heights fitting in 32 bits with required wood up to `2 * 10^9` means the yield sum needs a 64-bit accumulator in fixed-width languages; Python integers absorb it.
