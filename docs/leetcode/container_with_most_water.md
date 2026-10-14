# [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

**Medium** | **15 minutes** | **Array**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Algorithm:** [Two-pointer technique](https://usaco.guide/silver/two-pointers)

**Practice:** [`practice/container_with_most_water/solution.py`](../../practice/container_with_most_water/solution.py)

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i`th line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

**Note:** You may not slant the container.

## Examples

### Example 1

![Container Example](./assets/container_with_most_water_example1.jpg)

**Input:** `height = [1,8,6,2,5,4,8,3,7]`

**Output:** `49`

**Explanation:** The above vertical lines are represented by array `[1,8,6,2,5,4,8,3,7]`. In this case, the max area of water (blue section) the container can contain is 49.

### Example 2

**Input:** `height = [1,1]`

**Output:** `1`

## Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

## Deriving the Solution

Every candidate container is a pair of lines `i < j`, worth `(j - i) * min(height[i], height[j])`: the width times the shorter wall. The question every solution answers is how many of those pairs actually need to be measured.

1. **Start literal.** Measure every pair and keep the best. Correct, but there
   are `n * (n - 1) / 2` pairs, so it costs `O(n^2)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Consider the widest pair. Its area is capped by its
   shorter wall, and any other pair that keeps that shorter wall is narrower with the same cap or a lower one. Every such pair loses to the one just measured, so it never needs to be checked.
3. **Discard in bulk.** Start at the two ends and repeatedly move the pointer
   at the shorter wall inward: each move discards all pairs involving that wall at once, leaving only `n - 1` measurements: see [Two Pointers](#two-pointers).
4. **Skip whole runs.** The same argument condemns any line no taller than the
   current limiting wall, so the pointer can jump past consecutive runs of them instead of stepping one at a time. Same `O(n)` bound, fewer area computations: see [Two Pointers with Skip Optimization](#two-pointers-with-skip-optimization).

## Solutions

### Brute Force

#### Derivation

The most direct way to solve this is to consider every possible pair of lines as the two walls of the container. For each pair `(i, j)`, the amount of water it holds is limited by the shorter of the two lines, multiplied by the horizontal distance between them. Nothing more than the objective itself is needed: evaluate it everywhere and keep the best value seen.

1. Iterate over every starting line `i`.
2. For each `i`, iterate over every later line `j`.
3. Compute `width = j - i` and `current_height = min(height[i], height[j])`,
   and multiply them to get the pair's area.
4. Track the maximum area seen across all pairs in `max_area` and return it.

This examines all `n * (n - 1) / 2` pairs, guaranteeing the optimum is found, but the quadratic work makes it impractical for large inputs.

#### Formula

A container is chosen by picking two lines \(i < j\). Its water is bounded by the shorter wall, so the objective is:

$$ \text{area}(i, j) = (j - i) \cdot \min\bigl(\text{height}[i],\ \text{height}[j]\bigr) $$

$$ \text{answer} = \max_{0 \le i < j < n} \text{area}(i, j) $$

```text
area(i, j) = (j - i) * min(height[i], height[j])
answer     = max area(i, j) over all 0 <= i < j < n
```

The brute force evaluates this maximum literally, over every pair. The number of pairs is

$$ \binom{n}{2} = \frac{n(n-1)}{2} $$

```text
number of pairs = C(n, 2) = n * (n - 1) / 2
```

which is the source of the \(O(n^2)\) bound. The two-pointer solution below discards pairs in bulk instead: moving the taller wall inward can only shrink both factors at once, so no pair it skips can beat the one just measured.

#### Walkthrough

Example 1 has 9 lines, which means 36 pairs to check: too many to follow by hand. To watch the nested loops actually run, trace the smaller input `height = [1,8,6,2]` instead. The outer loop fixes a left wall `i`, the inner loop sweeps every later right wall `j`, and `max_area` only grows when a pair beats every pair seen so far.

Each row computes `width = j - i`, `current_height = min(height[i], height[j])`, and `area = width * current_height`:

| `i` | `j` | `width` (`j - i`) | `min(height[i], height[j])` | `area` | `max_area` after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | `min(1, 8)` = 1 | 1 | 1 |
| 0 | 2 | 2 | `min(1, 6)` = 1 | 2 | 2 |
| 0 | 3 | 3 | `min(1, 2)` = 1 | 3 | 3 |
| 1 | 2 | 1 | `min(8, 6)` = 6 | 6 | 6 |
| 1 | 3 | 2 | `min(8, 2)` = 2 | 4 | 6 |
| 2 | 3 | 1 | `min(6, 2)` = 2 | 2 | 6 |

The loops have now exhausted all 6 pairs, so the function returns `max_area = 6`, the best container for `[1,8,6,2]`. Notice the limiting wall is always the shorter line: the pair `(1, 3)` has the tall line `8` on the left, yet its area is capped by the short `2` on the right.

The full Example 1 runs the exact same nested sweep over all 36 pairs of `[1,8,6,2,5,4,8,3,7]`. The winning pair is `(i = 1, j = 8)`, with `width = 7` and `min(height[1], height[8]) = min(8, 7) = 7`, giving `area = 7 * 7 = 49`. So the function returns `49`, matching the expected Output.

#### Solution

The code is the nested sweep from the walkthrough: every pair measured once.

```python
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        n = len(height)
        max_area = 0

        # Try every pair of lines as the container walls
        for i in range(n):
            for j in range(i + 1, n):
                # Water level is capped by the shorter wall
                width = j - i
                current_height = min(height[i], height[j])
                max_area = max(max_area, width * current_height)

        return max_area
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The nested loops evaluate every pair of lines, which grows quadratically with the number of lines.

##### Space Complexity: `O(1)`

Only a few scalar variables are used regardless of input size.

#### Key Insights

- Provides a correct baseline by exhaustively checking every container
- The limiting wall is always the shorter line, so the height term is a `min`
- The quadratic pair count is what the two-pointer approach later eliminates

### Two Pointers

#### Derivation

The brute force measures every pair even though most pairs cannot possibly win. The [two-pointer technique](https://usaco.guide/silver/two-pointers) turns that observation into a discard rule. Look at the widest pair, the two end lines: its area is `width * min(height[left], height[right])`, capped by the shorter wall. Now ask what any other pair keeping that shorter wall could do. It would be strictly narrower, and its height would still be capped at the same shorter wall or lower, so it can never beat the pair just measured. That means every remaining pair involving the shorter wall is dead, and the pointer standing on it can move inward, writing off all those pairs in one step.

Repeating the argument at each new pair discards the pair space in bulk: moving the shorter wall's pointer is always safe, because the pairs it skips are provably no better than one already recorded. Only `n - 1` pairs are ever measured.

1. Start with `left = 0` and `right = len(height) - 1`, the widest container,
   and `max_area = 0`.
2. Measure the current pair: `width = right - left`,
   `current_height = min(height[left], height[right])`, and `current_area = width * current_height`; fold it into `max_area`.
3. Move the pointer at the shorter wall inward: `left += 1` when
   `height[left] < height[right]`, otherwise `right -= 1`.
4. Repeat until the pointers meet, then return `max_area`.

#### Walkthrough

Let us run the scan by hand on Example 1: `height = [1,8,6,2,5,4,8,3,7]`. Each line shows the pair measured and which pointer moves; `h[i]` abbreviates `height[i]`:

```text
left=0 (h=1)  right=8 (h=7)   width=8  min=1  area=8    max_area=8    h[0]<h[8] -> left+=1
left=1 (h=8)  right=8 (h=7)   width=7  min=7  area=49   max_area=49   h[1]>=h[8] -> right-=1
left=1 (h=8)  right=7 (h=3)   width=6  min=3  area=18   max_area=49   right-=1
left=1 (h=8)  right=6 (h=8)   width=5  min=8  area=40   max_area=49   equal heights -> right-=1
left=1 (h=8)  right=5 (h=4)   width=4  min=4  area=16   max_area=49   right-=1
left=1 (h=8)  right=4 (h=5)   width=3  min=5  area=15   max_area=49   right-=1
left=1 (h=8)  right=3 (h=2)   width=2  min=2  area=4    max_area=49   right-=1
left=1 (h=8)  right=2 (h=6)   width=1  min=6  area=6    max_area=49   right-=1 -> pointers meet
```

The first move retires the short wall of height `1`, and the very next pair (`left = 1`, `right = 8`) is the winner: `7 * min(8, 7) = 49`. Every later pair is narrower and never beats it, so the loop ends with `max_area = 49`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's loop: measure the pair, fold it into `max_area`, move the shorter wall inward.

```python
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        max_area = 0

        while left < right:
            # Calculate current area
            width = right - left
            current_height = min(height[left], height[right])
            current_area = width * current_height

            # Update maximum area if current is larger
            max_area = max(max_area, current_area)

            # Move the pointer with smaller height inward
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_area
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We make a single pass through the array using two pointers that move toward each other. Each element is visited at most once, making this a linear time algorithm.

##### Space Complexity: `O(1)`

The algorithm uses only a constant amount of extra space for variables (`left`, `right`, `max_area`, `current_area`, etc.), regardless of the input size.

#### Key Insights

- **Two-pointer optimization**: Starting from the widest possible container and systematically narrowing based on height constraints ensures we don't miss the optimal solution
- **Greedy choice correctness**: Moving the shorter line is always the right choice because keeping it would only yield worse results as we decrease width
- **No need to check all pairs**: The naive O(n²) approach of checking every pair is unnecessary due to the pruning property of the two-pointer technique
- **Geometric intuition**: We're finding the rectangle with maximum area under the constraint that one side must touch the x-axis and the other two sides are limited by the given heights

### Two Pointers with Skip Optimization

#### Derivation

The plain [two-pointer scan](https://usaco.guide/silver/two-pointers) still advances one line at a time, even through lines its own discard argument has already condemned. After measuring a pair, the limiting wall is the shorter of the two, `current_height`. Any line on that side whose height is less than or equal to `current_height` cannot improve the answer: moving to it shrinks the width while the height stays capped at the same value or lower. So instead of a single step, the pointer may jump past the entire consecutive run of such lines in one inner loop.

1. Measure the pair at `left` and `right`: fold
   `current_height * (right - left)` into `max_area`, exactly as before.
2. Identify the shorter side; its height is the limiting `current_height`.
3. Advance that side's pointer past every consecutive line with height at most
   `current_height`, guarding each step with `left < right`.
4. Repeat until the pointers meet, then return `max_area`.

The result is identical to the plain two-pointer scan; the inner skip loops simply collapse runs of useless positions into one move.

#### Walkthrough

Let us rerun Example 1, `height = [1,8,6,2,5,4,8,3,7]`, and watch the skip loops eat whole runs. Each measurement line is followed by the skip it triggers; `h[i]` abbreviates `height[i]`:

```text
left=0 (h=1)  right=8 (h=7)   cap=1  area=8*1=8    max_area=8
  skip left:  h[0]=1 <= 1 -> left=1; h[1]=8 > 1 stops the skip
left=1 (h=8)  right=8 (h=7)   cap=7  area=7*7=49   max_area=49
  skip right: h[8]=7 <= 7 -> right=7; h[7]=3 <= 7 -> right=6; h[6]=8 > 7 stops
left=1 (h=8)  right=6 (h=8)   cap=8  area=5*8=40   max_area=49
  skip right: h[6]=8, h[5]=4, h[4]=5, h[3]=2, h[2]=6 all <= 8 -> right=1
left=1, right=1 -> pointers meet, loop ends
```

The second skip discards indices `8` and `7` in one move, and the third discards the whole remaining run because no line left of index `6` exceeds the cap of `8`. Only 3 areas are computed instead of the plain scan's 8, and the function returns `max_area = 49`, matching the expected Output for Example 1.

#### Solution

The code adds the two inner skip loops to the plain scan; nothing else changes.

```python
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        max_area = 0

        while left < right:
            # Limiting wall and current area
            current_height = min(height[left], height[right])
            max_area = max(max_area, current_height * (right - left))

            # Advance past every line no taller than the limiting wall:
            # those positions can only shrink width without raising the cap
            if height[left] < height[right]:
                while left < right and height[left] <= current_height:
                    left += 1
            else:
                while left < right and height[right] <= current_height:
                    right -= 1

        return max_area
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each pointer only ever moves inward, and the inner skip loops advance the same pointers. Across the whole run every index is visited at most once, so the total work remains linear.

##### Space Complexity: `O(1)`

Only the two pointers and a couple of scalar variables are stored, independent of input size.

#### Key Insights

- **Pruning runs of short lines**: A line no taller than the current limiting wall
  can never beat the area already recorded, so it is safe to skip past it
- **Same asymptotic bound, smaller constant**: The skip loops do not change the
  `O(n)` complexity but can reduce the number of area computations on inputs with long plateaus or many short lines
- **Correctness preserved**: Because skipped lines are provably non-improving, the
  optimized scan returns exactly the same maximum as the plain two-pointer version

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - Evaluates every pair of lines
- **Two Pointers**: `O(n)` - Single pass with two converging pointers
- **Two Pointers with Skip Optimization**: `O(n)` - Same single pass, with skip loops that only ever advance the pointers inward

### Space Complexity

- **Brute Force**: `O(1)` - Only scalar tracking variables
- **Two Pointers**: `O(1)` - Only scalar tracking variables
- **Two Pointers with Skip Optimization**: `O(1)` - Only the two pointers and scalar variables

### Trade-offs

- Brute force is trivial to reason about and obviously correct, but its quadratic time makes it unusable for the upper constraint of 10^5 lines
- Two pointers is dramatically faster, at the cost of needing the greedy-movement insight to see why it never misses the optimal container
- The skip-optimized variant adds a small amount of code in exchange for fewer area computations on inputs with long runs of short lines, while keeping the same `O(n)` bound

### When to Use Each

- **Brute Force**: For building intuition or verifying the optimized solution on small inputs
- **Two Pointers**: For any real use, especially under the given constraints where quadratic time would time out
- **Two Pointers with Skip Optimization**: When a slightly lower constant factor matters on inputs with many non-improving lines, and the extra inner loops are acceptable

### Optimization Notes

- The leap from brute force to two pointers comes from the observation that moving the taller wall can never improve the area, so only the shorter wall's pointer should advance
- The skip optimization extends that observation: any line no taller than the current limiting wall is non-improving, so consecutive such lines can be skipped in one move rather than one step at a time
- All three approaches use `O(1)` space, so the entire gain is in time, not memory
