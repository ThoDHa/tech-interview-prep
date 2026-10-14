# [Container With Most Water](https://www.fastprep.io/problems/amazon-container-with-most-water)

**Medium** | **NN minutes** | **Array, Two Pointers, Greedy**

You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the i-th line are (i, 0) and (i, height[i]).

Find two lines that, together with the x-axis, form a container so that the container holds the most water.

Return the maximum amount of water a container can store.

You may not slant the container.

## Examples

### Example 1

**Input:** `height = [1,8,6,2,5,4,8,3,7]`

**Output:** `49`

**Explanation:** The lines at indices 1 and 8 have heights 8 and 7. The width is 7, so the area is min(8, 7) * 7 = 49.

### Example 2

**Input:** `height = [1,1]`

**Output:** `1`

**Explanation:** The only pair forms a container of width 1 and height 1.

## Constraints

- `2 <= height.length <= 10^5.`
- `0 <= height[i] <= 10^4.`

## Solutions

### Brute Force

#### Derivation

The most literal reading executes the problem's own sentence: a container is a pair of lines, its water level is the shorter of the two heights, and its width is the distance between them. Trying every pair and keeping the best area answers the question directly:

1. Loop `left` over every line index from `0` to `line_count - 1`.
2. Loop `right` over every later index, so each unordered pair is visited once.
3. Compute `width = right - left` and
   `water_level = min(height[left], height[right])`, and fold
   `width * water_level` into `max_area`.
4. Return `max_area` after the double loop.

#### Walkthrough

Example 1's nine lines produce thirty-six pairs, so this walkthrough uses a tailored shorter input, the first five lines of Example 1: `height = [1, 8, 6, 2, 5]`. Each row is one pair with its area, and the running best is `max_area`:

```text
pair (0,1)   width 1, water_level min(1,8) = 1 -> area 1    max_area = 1
pair (0,2)   width 2, min(1,6) = 1                -> area 2  max_area = 2
pair (0,3)   width 3, min(1,2) = 1                -> area 3  max_area = 3
pair (0,4)   width 4, min(1,5) = 1                -> area 4  max_area = 4
pair (1,2)   width 1, min(8,6) = 6                -> area 6  max_area = 6
pair (1,3)   width 2, min(8,2) = 2                -> area 4  max_area = 6
pair (1,4)   width 3, min(8,5) = 5                -> area 15 max_area = 15
pair (2,3)   width 1, min(6,2) = 2                -> area 2  max_area = 15
pair (2,4)   width 2, min(6,5) = 5                -> area 10 max_area = 15
pair (3,4)   width 1, min(2,5) = 2                -> area 2  max_area = 15
```

The best pair here is lines `1` and `4`: height `8` paired with height `5` over width `3` gives `15`. On the full Example 1 the same double loop reaches `49` at the pair of indices `1` and `8`, matching the expected Output.

#### Solution

The code is the walkthrough's double loop with the area fold:

```python
from typing import List


class Solution:
    def solve(self, height: List[int]) -> int:
        """Return the maximum water area over all pairs of lines.

        Time:  O(n^2): every one of the n * (n - 1) / 2 pairs is
            evaluated once with constant work.
        Space: O(1): only the running maximum and loop indices.
        """
        line_count = len(height)
        max_area = 0
        for left in range(line_count):
            for right in range(left + 1, line_count):
                width = right - left
                water_level = min(height[left], height[right])
                max_area = max(max_area, width * water_level)
        return max_area
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The double loop visits each of the `n × (n − 1) / 2` pairs once and spends constant work per pair.

##### Space Complexity: `O(1)`

Only the running maximum and the two loop indices are stored.

#### Key Insights

- The area formula decomposes into two independent factors, `width` and `water_level`, and the shorter line always sets the water level; the taller line's excess holds nothing.
- The brute force is the correctness baseline: every later approach must agree with it on every input, which makes it the reference for random cross-checking.
- The quadratic cost is pure redundancy: most pairs are re-measuring capacity that other, wider pairs already dominate, and spotting that waste is what the next approach does.

### Two Pointers

#### Derivation

The brute force re-examines every pair, but whole families of pairs can be discarded at once. Start the search at the widest possible container, `left = 0` and `right = n - 1`, and make one claim: when `height[left] < height[right]`, the line at `left` can be retired, because every container keeping `left` and narrowing the other end is strictly worse than the container already measured. For any `right_prime < right`:

```text
area(left, right_prime) = (right_prime - left) * min(height[left], height[right_prime])
                        <= (right_prime - left) * height[left]
                        <  (right - left) * height[left]
                        =  area(left, right)
```

The first line caps the water level at the shorter line `height[left]`, and the third line shrinks because `right_prime - left < right - left`. Symmetrically, when `height[right] <= height[left]`, the line at `right` can be retired. Every step therefore discards one line with a proof that no unvisited pair involving it wins, so `n - 1` steps sweep all `n^2` pairs down to a linear walk:

1. Set `left = 0`, `right = len(height) - 1`, `max_area = 0`.
2. While `left < right`: set `width = right - left`.
3. If `height[left] < height[right]`, the limiting height is `height[left]` and
   `left` is retired: fold `width * height[left]` into `max_area` and advance
   `left += 1`.
4. Otherwise the limiting height is `height[right]`: fold
   `width * height[right]` into `max_area` and retreat `right -= 1`.
5. Return `max_area` when the pointers meet.

#### Walkthrough

Example 1, `height = [1,8,6,2,5,4,8,3,7]`. Each line is one loop pass with the pointer positions, the measured container, and the pointer that the retirement rule moves:

```text
left=0, right=8   width 8, min(1,7) = 1 -> area 8    max_area = 8     left 0 retired
left=1, right=8   width 7, min(8,7) = 7 -> area 49   max_area = 49    right 8 retired
left=1, right=7   width 6, min(8,3) = 3 -> area 18   max_area = 49    right 7 retired
left=1, right=6   width 5, min(8,8) = 8 -> area 40   max_area = 49    right 6 retired
left=1, right=5   width 4, min(8,4) = 4 -> area 16   max_area = 49    right 5 retired
left=1, right=4   width 3, min(8,5) = 5 -> area 15   max_area = 49    right 4 retired
left=1, right=3   width 2, min(8,2) = 2 -> area 4    max_area = 49    right 3 retired
left=1, right=2   width 1, min(8,6) = 6 -> area 6    max_area = 49    right 2 retired
                  pointers meet -> return max_area
```

The best measurement happens on the very second pass: lines `1` and `8` with heights `8` and `7` over width `7` give `49`, the expected Output. The remaining six passes only prove that nothing hidden inside the shrinking window beats it.

#### Solution

The code is the walkthrough's retirement loop: measure, fold into `max_area`, move the limiting pointer.

```python
from typing import List


class Solution:
    def solve(self, height: List[int]) -> int:
        """Return the maximum water area over all pairs of lines.

        Time:  O(n): each pass retires one line, so the loop runs
            n - 1 times with constant work.
        Space: O(1): two pointers and the running maximum.
        """
        left, right = 0, len(height) - 1
        max_area = 0
        while left < right:
            width = right - left
            if height[left] < height[right]:
                water_level = height[left]
                left += 1
            else:
                water_level = height[right]
                right -= 1
            max_area = max(max_area, width * water_level)
        return max_area
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every pass retires exactly one line and the pointers stop when they meet, so the loop runs `n - 1` times with constant work per pass.

##### Space Complexity: `O(1)`

Two pointer positions and the running maximum are the only state.

#### Key Insights

- The correctness argument never enumerates the discarded pairs: it proves each retired line's best remaining container is already on record, which is what turns `n^2` candidates into `n` steps.
- Greedy shrinking is safe only because the width always decreases; any move must be justified by a dominance argument, not by hope that the new pair is better.
- Ties (`height[left] == height[right]`) can retire either side; the proof needs only one side's inequality, and the equal case satisfies both.
- The water level of a container is `min` of the two heights, so the taller line's surplus above the shorter one is dead capacity that no pair can use.

### Sorted by Height Sweep

#### Derivation

The two-pointer pass is optimal, but its retirement proof is subtle enough that a wrong move silently loses the answer. This approach replaces the pointer dance with a monotone fact that is easier to trust: process the lines from tallest to shortest. When the sweep reaches a line, every line taller than it has already been visited, so the visited lines' leftmost and rightmost positions are known; call them `leftmost_taller` and `rightmost_taller`. For the current line at position `line` with height `height[line]`, and for any taller partner at `partner >= line` in processing order, the best container the pair forms is bounded:

```text
area(line, partner) = height[line] * (partner - line)
                    <= height[line] * (rightmost_taller - line)
```

because `partner` sits between `leftmost_taller` and `rightmost_taller`, so `partner - line` never exceeds `rightmost_taller - line`, and the sweep folds exactly that bound into `max_area`. Shorter partners cannot raise the water level above `height[line]`, so no unvisited pair beats the recorded fold, and the sweep can stop reasoning about them:

1. Build `order_by_height`, the line indices sorted by height, tallest first.
2. Initialize `leftmost_taller` and `rightmost_taller` to `None` and
   `max_area = 0`.
3. For each `line` in `order_by_height`: when a taller line was already seen,
   fold `height[line] * (line - leftmost_taller)` and
   `height[line] * (rightmost_taller - line)` into `max_area`.
4. Update `leftmost_taller` to the smaller of itself and `line`, and
   `rightmost_taller` to the larger of itself and `line`.
5. Return `max_area` after the sweep.

#### Walkthrough

Example 1, `height = [1,8,6,2,5,4,8,3,7]`. The sweep order by descending height is lines `1, 6` (both height `8`), `8` (height `7`), `2` (height `6`), `4` (height `5`), `5` (height `4`), `7` (height `3`), `3` (height `2`), `0` (height `1`). Each row is one sweep step with the two candidate folds:

```text
line 1 (h8)   no taller line seen yet -> no fold
              leftmost_taller = 1, rightmost_taller = 1
line 6 (h8)   8*(6-1) = 40, 8*(6-1) = 40             max_area = 40
              leftmost_taller = 1, rightmost_taller = 6
line 8 (h7)   7*(8-1) = 49, 7*(8-6) = 14             max_area = 49
              leftmost_taller = 1, rightmost_taller = 8
line 2 (h6)   6*(2-1) = 6,  6*(8-2) = 36             max_area = 49
line 4 (h5)   5*(4-1) = 15, 5*(8-4) = 20             max_area = 49
line 5 (h4)   4*(5-1) = 16, 4*(8-5) = 12             max_area = 49
line 7 (h3)   3*(7-1) = 18, 3*(8-7) = 3              max_area = 49
line 3 (h2)   2*(3-1) = 4,  2*(8-3) = 10             max_area = 49
line 0 (h1)   1*(0-1) = -1, 1*(8-0) = 8              max_area = 49
```

The winning fold is at line `8`: paired against `leftmost_taller = 1` it gives `7 × 7 = 49`, the expected Output. Every later line is shorter, so its water level caps below `7` and none of its folds beats `49`.

#### Solution

The code is the sweep from the walkthrough: sort, fold both spans per line, widen the taller-window bounds.

```python
from typing import List, Optional


class Solution:
    def solve(self, height: List[int]) -> int:
        """Return the maximum water area over all pairs of lines.

        Time:  O(n log n) for the descending sort plus O(n) sweep steps
            of constant work.
        Space: O(n) for the sorted order of line indices.
        """
        line_count = len(height)
        order_by_height = sorted(
            range(line_count), key=lambda line: height[line], reverse=True
        )
        leftmost_taller: Optional[int] = None
        rightmost_taller: Optional[int] = None
        max_area = 0
        for line in order_by_height:
            if leftmost_taller is not None:
                max_area = max(max_area, height[line] * (line - leftmost_taller))
                max_area = max(max_area, height[line] * (rightmost_taller - line))
            leftmost_taller = line if leftmost_taller is None else min(leftmost_taller, line)
            rightmost_taller = line if rightmost_taller is None else max(rightmost_taller, line)
        return max_area
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The descending sort dominates; the sweep that follows visits each line once with constant work.

##### Space Complexity: `O(n)`

The sorted order of line indices is the only structure that scales with the input.

#### Key Insights

- Sorting by height makes "all taller lines seen" a processing invariant, which converts the partner search into two running extremes instead of a pointer strategy.
- Only the two extreme positions of the taller set can matter: any in-between partner produces a narrower container with the same water level, so two variables replace the whole set.
- The two folds evaluate `line - leftmost_taller` even when it is negative, as the walkthrough's last row shows; a negative width can never win, so no guard is needed beyond taking the running max.
- The approach is dominated by Two Pointers in both time and space on this problem; its value is the reusable pattern "process by descending key so the rest of the set is already summarized".

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - every one of the `n × (n − 1) / 2` pairs is measured.
- **Two Pointers**: `O(n)` - each of the `n - 1` passes retires one line with constant work.
- **Sorted by Height Sweep**: `O(n log n)` - a descending sort plus one linear sweep.

### Space Complexity

- **Brute Force**: `O(1)` - a running maximum and loop indices.
- **Two Pointers**: `O(1)` - two pointers and a running maximum.
- **Sorted by Height Sweep**: `O(n)` - the sorted order of line indices.

### Trade-offs

- **Brute Force**: direct transcription of the problem statement and trivially correct, but quadratic work is hopeless at `n = 10^5`.
- **Two Pointers**: optimal time and constant space, but its correctness rests on the retirement inequality, which must be stated precisely to be believed.
- **Sorted by Height Sweep**: replaces the retirement argument with a monotone processing order that is easy to reason about, at the cost of a sort and linear extra space.

### When to Use Each

- **Brute Force**: for tiny inputs, or as the reference implementation when cross-checking an optimized version against random tests.
- **Two Pointers (Recommended)**: the interview answer: one pass, constant space, and a two-line proof per step.
- **Sorted by Height Sweep**: when the two-pointer invariant feels too slippery to defend out loud, or when the same sweep-by-descending-key pattern solves a richer variant.

### Optimization Notes

- The two-pointer move rule needs only the shorter side to retire: moving the taller side instead can discard the optimal pair, the classic wrong variant of this problem.
- Ties in the two-pointer comparison can retire either side without loss, since the retirement inequality holds for both sides of an equal pair.
- In the sorted sweep, comparing a line against both extremes is what survives ties in height: equal-height lines see each other as partners, which the walkthrough's first fold (lines `1` and `6`, both height `8`) exercises.
- All three approaches work with `height[i] = 0`, which yields an area of `0` for the affected pairs; the initial `max_area = 0` already encodes the empty-container floor.
