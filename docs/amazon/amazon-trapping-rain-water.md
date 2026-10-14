# [Trapping Rain Water](https://www.fastprep.io/problems/amazon-trapping-rain-water)

**Hard** | **NN minutes** | **Array, Two Pointers, Stack**

You are given an integer array height of length n. n vertical bars stand on the x-axis. The i-th bar has width 1 and height height[i].

Compute how many units of water the bars can trap after rain.

Water sits above a bar only when both a strictly taller left boundary and a strictly taller right boundary exist. The water depth at index i is max(0, min(leftMax[i], rightMax[i]) - height[i]), where leftMax[i] is the tallest bar at an index < i and rightMax[i] is the tallest bar at an index > i.

## Examples

### Example 1

**Input:** `height = [0,1,0,2,1,0,1,3,2,1,2,1]`

**Output:** `6`

**Explanation:** The bars trap 1 + 1 + 2 + 1 + 1 = 6 units of water.

### Example 2

**Input:** `height = [4,2,0,3,2,5]`

**Output:** `9`

**Explanation:** The valley between the height-4 and height-5 bars traps 2 + 4 + 1 + 2 = 9 units.

## Constraints

- `1 <= height.length <= 2 * 10^4.`
- `0 <= height[i] <= 10^5.`

## Solutions

### Brute Force

#### Derivation

The question to ask first is local: how much water sits directly above bar `i`? The statement prices it exactly: the water level is the shorter of the two surrounding walls, the tallest bar strictly left of `i` and the tallest bar strictly right of `i`, and the bar itself displaces `height[i]` of that column. The literal way to find the two walls is to scan for them:

1. For every index `i`, scan left over `height[0 .. i - 1]` to find `left_max`.
2. Scan right over `height[i + 1 .. n - 1]` to find `right_max`.
3. Add `max(0, min(left_max, right_max) - height[i])` to the running `trapped`
   total.

The `max(0, ...)` clamp is load-bearing here: a bar taller than one of its walls (or taller than both) would otherwise contribute a negative depth. A bar at the array edge has one wall missing entirely, and the clamp absorbs that too, because a missing wall leaves the scan at the sentinel `0`.

#### Walkthrough

Let us run the Brute Force on Example 1: `height = [0,1,0,2,1,0,1,3,2,1,2,1]`. For every bar `i` we scan left for `left_max` (tallest strictly before `i`), scan right for `right_max` (tallest strictly after `i`), and add the clamped depth to `trapped`:

| `i` | `height[i]` | `left_max` | `right_max` | `min(left_max, right_max) - height[i]` | `trapped` |
|-----|-------------|------------|-------------|----------------------------------------|-----------|
| 0 | 0 | none | 3 | no left wall: clamped to 0 | 0 |
| 1 | 1 | 0 | 3 | `0 - 1 = -1` -> 0 | 0 |
| 2 | 0 | 1 | 3 | `1 - 0 = 1` | 1 |
| 3 | 2 | 1 | 3 | `1 - 2 = -1` -> 0 | 1 |
| 4 | 1 | 2 | 3 | `2 - 1 = 1` | 2 |
| 5 | 0 | 2 | 3 | `2 - 0 = 2` | 4 |
| 6 | 1 | 2 | 3 | `2 - 1 = 1` | 5 |
| 7 | 3 | 2 | 2 | `2 - 3 = -1` -> 0 | 5 |
| 8 | 2 | 3 | 2 | `2 - 2 = 0` | 5 |
| 9 | 1 | 3 | 2 | `2 - 1 = 1` | 6 |
| 10 | 2 | 3 | 1 | `1 - 2 = -1` -> 0 | 6 |
| 11 | 1 | 3 | none | no right wall: clamped to 0 | 6 |

The clamp fires on five rows, which shows why the statement carries `max(0, ...)`: bar `1` is taller than its weak left wall (`left_max = 0`), bar `7` is taller than both walls, and bars `10` and `11` face a right side that falls away. The five positive rows (`2`, `4`, `5`, `6`, `9`) sum to `1 + 1 + 2 + 1 + 1 = 6`, matching Example 1's Output and its Explanation line.

#### Solution

The code is the walkthrough's table computed row by row: two scans and one clamped subtraction per bar.

```python
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        trapped = 0

        for i in range(n):
            left_max = 0
            for j in range(i):
                left_max = max(left_max, height[j])

            right_max = 0
            for j in range(i + 1, n):
                right_max = max(right_max, height[j])

            trapped += max(0, min(left_max, right_max) - height[i])

        return trapped
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` bars we rescan both flanks to recompute the two maxima, so the work is quadratic.

##### Space Complexity: `O(1)`

Only a few scalar accumulators are tracked; no auxiliary array is allocated.

#### Key Insights

- Transcribes the statement's formula directly: depth above bar `i` is
  `max(0, min(leftMax[i], rightMax[i]) - height[i])`.
- The sentinel `0` for a missing wall and the `max(0, ...)` clamp together handle the array edges without special-casing.
- Wasteful: every bar rebuilds maxima that its neighbor could inherit, which is the redundancy the next approach removes.

### Prefix and Suffix Maximums

#### Derivation

The brute force rescans the same flanks over and over: `left_max` at `i` differs from `left_max` at `i - 1` by at most one comparison, yet every bar rebuilds it from scratch. That one-step dependence is the signature of [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming): two linear sweeps cache every wall height the depth formula needs, and a third pass sums the water. Because the statement's maxima are strict (`index < i` and `index > i`), the recurrences fold in the *neighbor* bar, not the bar itself:

1. Build `left_max` in a forward sweep: `left_max[0] = 0` (no left wall), then
   `left_max[i] = max(left_max[i - 1], height[i - 1])`.
2. Build `right_max` in a backward sweep: `right_max[n - 1] = 0` (no right wall), then
   `right_max[i] = max(right_max[i + 1], height[i + 1])`.
3. For each bar, add `max(0, min(left_max[i], right_max[i]) - height[i])` to `trapped`.

The clamp stays, unlike in the inclusive-maxima formulation where it is redundant: a strict maximum can undercut its own bar.

#### Formula

Let `n = len(height)`. The statement's wall heights and depth, with the sweeps that fill them:

$$ L[i] = \max_{0 \le k < i} \text{height}[k], \qquad R[i] = \max_{i < k \le n - 1} \text{height}[k], \qquad \text{water}[i] = \max\bigl(0,\ \min(L[i], R[i]) - \text{height}[i]\bigr) $$

```text
left_max[i]  = max(height[0 .. i - 1])          sentinel 0 at i = 0 (no left wall)
right_max[i] = max(height[i + 1 .. n - 1])      sentinel 0 at i = n - 1 (no right wall)
water[i]     = max(0, min(left_max[i], right_max[i]) - height[i])
trapped      = sum of water[i] over i = 0 .. n - 1
```

The strict maxima satisfy one-step recurrences, which is what makes the precomputation linear:

$$ L[0] = 0, \qquad L[i] = \max\bigl(L[i-1],\ \text{height}[i-1]\bigr) \quad (1 \le i < n) $$

```text
left_max[0]  = 0
left_max[i]  = max(left_max[i - 1], height[i - 1])     for 1 <= i < n
right_max[n - 1] = 0
right_max[i] = max(right_max[i + 1], height[i + 1])    for 0 <= i < n - 1
```

The `\max(0, \cdot)` is not redundant here: unlike an inclusive maximum, `min(L[i], R[i])` may sit below `height[i]` when the bar overtops one of its walls, and the clamp turns that negative into the correct depth of `0`.

#### Walkthrough

Let us fill the arrays on Example 2: `height = [4,2,0,3,2,5]`. The forward sweep carries the running maximum of everything strictly left, the backward sweep everything strictly right:

```text
height       [4, 2, 0, 3, 2, 5]
left_max     [0, 4, 4, 4, 4, 4]     forward: tallest bar strictly left of i
right_max    [5, 5, 5, 5, 5, 0]     backward: tallest bar strictly right of i
```

The tallest bar `5` sits at the right edge, so `right_max` is `5` everywhere except the last slot, and every interior column's water level is set by `left_max`. The summation pass applies the formula bar by bar:

```text
i=0   max(0, min(0, 5) - 4) = 0    trapped = 0    (no left wall)
i=1   min(4, 5) - 2 = 2            trapped = 2
i=2   min(4, 5) - 0 = 4            trapped = 6
i=3   min(4, 5) - 3 = 1            trapped = 7
i=4   min(4, 5) - 2 = 2            trapped = 9
i=5   max(0, min(4, 0) - 5) = 0    trapped = 9    (no right wall)
```

The dip between the wall of height `4` at `i = 0` and the wall of height `5` at `i = 5` fills up to level `4`, giving `2 + 4 + 1 + 2 = 9` units. The final `trapped = 9` matches Example 2's Output and its Explanation line.

#### Solution

The code is the three passes from the walkthrough: forward sweep, backward sweep, then the summation.

```python
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        left_max = [0] * n
        right_max = [0] * n

        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i - 1])

        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i + 1])

        trapped = 0
        for i in range(n):
            trapped += max(0, min(left_max[i], right_max[i]) - height[i])

        return trapped
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three linear passes over the array.

##### Space Complexity: `O(n)`

Two arrays of size `n` store the prefix and suffix maxima.

#### Key Insights

- The strict maxima change the recurrences, not the formula: each sweep folds in the neighboring bar instead of the current one, and the sentinels sit at the edges where no wall exists.
- The `max(0, ...)` clamp must stay because a strict maximum can undercut its own bar; dropping it would corrupt exactly the overtopped bars.
- The `O(n)` space is the price for clarity; the two-pointer method removes it.

### Monotonic Stack

#### Derivation

Both approaches so far account for water column by column, which forces each column to know its two walls. Flip the accounting: fill the water in horizontal layers, and settle each layer the moment its right wall arrives. The [stack](https://usaco.guide/gold/stacks) holds indices of bars whose heights are decreasing from bottom to top, so the top is always the most recent unresolved dip. When a bar taller than the stack top arrives, it acts as a right wall: the popped top becomes the `floor` of a basin, and the new stack top (if any) is the `left` wall:

1. Walk left to right, treating the stack as a record of unresolved dips.
2. While the current bar `h` is taller than the bar at the top of the stack, pop
   the top as `floor`.
3. If the stack is now empty there is no left wall, so that water escapes;
   otherwise the settled layer holds `(i - left - 1) * (min(height[left], h) - height[floor])` units: the width between the walls times the depth of the shorter wall above the floor.
4. Push the current index `i` and continue.

A single bar may settle several layers as it pops successively taller floors, and each index is pushed and popped at most once.

#### Walkthrough

Let us run the stack on Example 2: `height = [4,2,0,3,2,5]`. Each line is one event: a push, or a pop that settles a layer of `width * bounded` water:

```text
i=0 h=4   push 0                                      stack [0]      heights [4]
i=1 h=2   push 1                                      stack [0,1]    heights [4,2]
i=2 h=0   push 2                                      stack [0,1,2]  heights [4,2,0]
i=3 h=3   pop floor=2  left=1  1 * (min(2,3)-0) = 2   trapped 2
          pop floor=1  left=0  2 * (min(4,3)-2) = 2   trapped 4
          push 3                                      stack [0,3]    heights [4,3]
i=4 h=2   push 4                                      stack [0,3,4]  heights [4,3,2]
i=5 h=5   pop floor=4  left=3  1 * (min(3,5)-2) = 1   trapped 5
          pop floor=3  left=0  4 * (min(4,5)-3) = 4   trapped 9
          pop floor=0  stack empty -> break           water escapes left
          push 5                                      stack [5]      heights [5]
```

The bar of height `3` at `i = 3` settles two layers on arrival: first the thin layer above the floor of height `0` up to its left wall of height `2`, then the wider layer above the floor of height `2`, capped at `min(4, 3) = 3`. The final bar of height `5` settles the remaining layers the same way, and when it pops the bar of height `4` with nothing left beneath it, the empty-stack check discards that water: with no left wall it would spill off the edge. The total is `trapped = 9`, matching Example 2's Output.

#### Solution

The code is the event log above: the `while` loop performs the pops that settle layers, and every index is pushed exactly once.

```python
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        stack = []
        trapped = 0

        for i, h in enumerate(height):
            while stack and height[stack[-1]] < h:
                floor = stack.pop()

                if not stack:
                    break

                left = stack[-1]
                width = i - left - 1
                bounded = min(height[left], h) - height[floor]
                trapped += width * bounded

            stack.append(i)

        return trapped
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each index is pushed onto the stack once and popped at most once, so the total work across the whole scan is linear.

##### Space Complexity: `O(n)`

In the worst case (a strictly decreasing elevation map) every index sits on the stack at once before any pops occur.

#### Key Insights

- The decreasing-height invariant guarantees that when a taller bar arrives, the popped bar is genuinely a local floor with a known left wall.
- Water is accumulated layer by layer between walls rather than column by column, which is what makes the per-basin amounts available as a byproduct.
- The empty-stack check after a pop is essential: it discards water that would spill off the left edge when no left wall exists.

### Two Pointers

#### Derivation

The prefix and suffix arrays store every wall height, yet the depth formula only ever consumes `min(left_max[i], right_max[i])`: the larger side is computed and then ignored. The [two-pointer method](https://usaco.guide/silver/two-pointers) exploits that slack. Walk inward from both ends carrying just two running maxima. If `left_max <= right_max`, the water level at the left pointer is already decided: some bar on the right reaches `right_max >= left_max`, so no bar between the pointers can lower the level at the left position. The symmetric claim holds on the right, so whichever side carries the smaller running max can be settled and stepped inward immediately.

The running maxima here are inclusive of the bar they name, so the settled amount is `left_max - height[left]` without a clamp. That is the statement's formula in different clothes: when a bar overtops one of its walls, the statement clamps the depth to `0`, and the inclusive form produces that same `0` because its minimum is then the bar itself:

1. Place `left` and `right` at the two ends and seed `left_max` / `right_max` with
   the endpoint heights.
2. While `left < right`, compare the running maxima. If `left_max <= right_max`,
   advance `left`, fold the new bar into `left_max`, and add `left_max - height[left]`; otherwise mirror the step on the right side.
3. Stop when the pointers meet: every column has been settled from one side or the
   other.

#### Walkthrough

Let us walk the pointers on Example 1: `height = [0,1,0,2,1,0,1,3,2,1,2,1]`. Start with `left = 0`, `right = 11`, `left_max = 0`, `right_max = 1`. Each line shows the `left_max <= right_max` comparison, the pointer that moves, and the water settled at its new position:

```text
0 <= 1   left  -> 1    left_max 1    + 1-1 = 0   trapped 0
1 <= 1   left  -> 2    left_max 1    + 1-0 = 1   trapped 1
1 <= 1   left  -> 3    left_max 2    + 2-2 = 0   trapped 1
2 >  1   right -> 10   right_max 2   + 2-2 = 0   trapped 1
2 <= 2   left  -> 4    left_max 2    + 2-1 = 1   trapped 2
2 <= 2   left  -> 5    left_max 2    + 2-0 = 2   trapped 4
2 <= 2   left  -> 6    left_max 2    + 2-1 = 1   trapped 5
2 <= 2   left  -> 7    left_max 3    + 3-3 = 0   trapped 5
3 >  2   right -> 9    right_max 2   + 2-1 = 1   trapped 6
3 >  2   right -> 8    right_max 2   + 2-2 = 0   trapped 6
3 >  2   right -> 7    right_max 3   + 3-3 = 0   trapped 6
```

The left pointer settles the deep dip at indices `2` through `6` using only `left_max = 2`, which is safe because `right_max = 2` guarantees a wall at least that tall further right. Once `left_max` reaches `3` at the tallest bar, the right side becomes the smaller one and settles indices `10` down to `8`. The pointers meet at `i = 7`, the tallest bar, which is its own wall and contributes `0` from either side. The loop exits with `trapped = 6`, matching Example 1's Output.

#### Solution

The code is the two-branch step from the walkthrough, repeated until the pointers meet.

```python
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        trapped = 0

        while left < right:
            if left_max <= right_max:
                left += 1
                left_max = max(left_max, height[left])
                trapped += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                trapped += right_max - height[right]

        return trapped
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each pointer moves inward at most `n` times total, so we touch every bar once.

##### Space Complexity: `O(1)`

Only a fixed number of scalars are tracked regardless of input size.

#### Key Insights

- The water above a bar rises to the minimum of the two surrounding wall heights; the two-pointer trick obtains that minimum implicitly, one side at a time.
- Always moving the smaller-max side is what makes the local decision provably safe: the larger running max proves a wall at least that tall exists across the gap.
- The inclusive running maxima fold the statement's `max(0, ...)` clamp in for free: a bar that overtops its own side settles exactly `0`.
- No auxiliary arrays are needed, beating the prefix and suffix approach on space.

### Prefix and Suffix Maximums with accumulate

#### Derivation

The two sweeps in [Prefix and Suffix Maximums](#prefix-and-suffix-maximums) are both instances of one shape: seed an accumulator with `0`, then fold each next element into it with `max`. That fold is precisely [`itertools.accumulate`](https://docs.python.org/3/library/itertools.html#itertools.accumulate) with `initial=0`. Substituting it changes nothing about the algorithm: `left_max` and `right_max` hold the same values they held before, and the water is still summed bar by bar with the explicit clamped `min(left_max[i], right_max[i]) - height[i]`. What disappears is the index arithmetic, the two seeded sentinel slots, and the descending `range(n - 2, -1, -1)` that is easy to get wrong by one:

1. Build `left_max = list(accumulate(height, max, initial=0))[:-1]`. With the
   `initial=0` seed, entry `i` is the maximum of `height[0 .. i - 1]`, the strict prefix maximum; the trailing `[:-1]` drops the one-past-the-end entry so the list lines up with the bars.
2. Build the strict suffix maxima symmetrically: accumulate over `reversed(height)` with the same seed, drop the last entry, then reverse with `[::-1]`. Running maxima always flow left to right, so a suffix maximum is a prefix maximum of the reversed array, read back in the original order.
3. Sum `max(0, min(left_max[i], right_max[i]) - height[i])` over every index, unchanged from the hand-rolled version.

The reversal is the one place this form asks something of the reader that the explicit loop did not. It buys a genuine simplification anyway: the backward loop it replaced carried both a descending range and a seeded final slot, two separate chances for an off-by-one.

#### Walkthrough

Let us build the arrays on Example 1: `height = [0,1,0,2,1,0,1,3,2,1,2,1]`. The forward `accumulate` gives the strict prefix maxima directly. For the strict suffix maxima, the middle row below shows what `accumulate(reversed(height), max, initial=0)` produces before trimming, and the last row shows it after trimming and `[::-1]`:

```text
height                          [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
left_max   accumulate, trim     [0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
            accumulate(reversed) [0, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3]
right_max  trim, reversed back  [3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 1, 0]
```

Check one entry each way: `left_max[4] = 2` is the tallest of `height[0..3]`, and `right_max[4] = 3` is the tallest of `height[5..11]`. The untrimmed row carries 13 entries, the strict prefix maxima of 12 bars plus the `0` seed; the trim removes the final full-array maximum. The summation pass applies the formula bar by bar:

```text
i=0    max(0, min(0, 3) - 0) = 0    trapped = 0    (no left wall)
i=1    max(0, min(0, 3) - 1) = 0    trapped = 0
i=2    min(1, 3) - 0 = 1            trapped = 1
i=3    max(0, min(1, 3) - 2) = 0    trapped = 1
i=4    min(2, 3) - 1 = 1            trapped = 2
i=5    min(2, 3) - 0 = 2            trapped = 4
i=6    min(2, 3) - 1 = 1            trapped = 5
i=7    max(0, min(2, 2) - 3) = 0    trapped = 5
i=8    max(0, min(3, 2) - 2) = 0    trapped = 5
i=9    min(3, 2) - 1 = 1            trapped = 6
i=10   max(0, min(3, 1) - 2) = 0    trapped = 6
i=11   max(0, min(3, 0) - 1) = 0    trapped = 6    (no right wall)
```

The clamp fires wherever the bar overtops a wall, the same five rows the Brute Force walkthrough flagged. The final `trapped = 6` matches Example 1's Output.

#### Solution

The same three passes, with the two strict-maximum sweeps delegated to the standard library.

```python
from itertools import accumulate
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        left_max = list(accumulate(height, max, initial=0))[:-1]
        right_max = list(accumulate(reversed(height), max, initial=0))[:-1][::-1]

        trapped = 0
        for i in range(len(height)):
            trapped += max(0, min(left_max[i], right_max[i]) - height[i])

        return trapped
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Still three linear passes: one `accumulate` forward, one `accumulate` backward plus its trim and `[::-1]` copy, and one summation. The reversal and the slice each cost `O(n)` and fold into the same linear bound, and `accumulate` runs its `max` fold in C rather than through a Python-level loop.

##### Space Complexity: `O(n)`

Two arrays of size `n` hold the strict prefix and suffix maxima, exactly as the hand-rolled version allocates. The backward pass briefly holds one extra `n`-sized list, the untrimmed accumulation, before the trim and `[::-1]` produce the final `right_max`, which leaves the bound at `O(n)`.

#### Key Insights

- A strict running maximum is a fold seeded below the data: `left_max[i] = max(left_max[i - 1], height[i - 1])` is what `accumulate(height, max, initial=0)` computes, with the `initial=0` seed standing in for the missing wall at the edge.
- The trapping formula stays fully explicit, including the `max(0, ...)` clamp the strict maxima require. `accumulate` absorbs only how the wall heights are obtained, which is exactly the part that was identical in both directions and therefore the part worth factoring out.
- Suffix maxima have no direct `accumulate` form, so the backward sweep costs a `reversed` going in and a trim plus `[::-1]` coming out. That asymmetry is the honest price of this version and the one line a reader must pause on.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - every bar rescans both flanks for its two walls.
- **Prefix and Suffix Maximums**: `O(n)` - three linear passes.
- **Monotonic Stack**: `O(n)` - each index is pushed and popped at most once.
- **Two Pointers**: `O(n)` - single inward sweep.
- **Prefix and Suffix Maximums with accumulate**: `O(n)` - the same three linear
  passes, with the two folds and the reversal running in C.

### Space Complexity

- **Brute Force**: `O(1)` - only scalar accumulators.
- **Prefix and Suffix Maximums**: `O(n)` - two precomputed arrays.
- **Monotonic Stack**: `O(n)` - the stack can hold every index for a decreasing map.
- **Two Pointers**: `O(1)` - a handful of scalars.
- **Prefix and Suffix Maximums with accumulate**: `O(n)` - the same two arrays,
  plus one transient `n`-sized list before the backward result is trimmed and reversed.

### Trade-offs

- The Brute Force approach is the easiest to derive and uses no extra space, but its quadratic rescans make it too slow for the upper constraint of `2 * 10^4` bars.
- The Prefix and Suffix Maximums approach trades `O(n)` space for a transparent, formula-driven implementation that caches the brute force's repeated maxima into two linear sweeps.
- The Monotonic Stack approach also uses `O(n)` space but fills water in horizontal layers, which is the natural fit when a per-basin breakdown is wanted.
- The Two Pointers approach achieves optimal constant space but relies on the subtler invariant that the smaller running max bounds its side's water level.
- The accumulate variant keeps the prefix and suffix approach's transparency and its `O(n)` space while removing the two most error-prone lines of it, the seeded sentinel slots and the descending range. It charges for that a `reversed` and a trim-and-reverse on the backward sweep, which is one idiom a reader has to recognize.

### When to Use Each

- **Brute Force**: As a first correctness check or to derive the depth formula before optimizing; not viable at full input size.
- **Prefix and Suffix Maximums**: When clarity matters most, or as a stepping stone to establish correctness before optimizing.
- **Monotonic Stack**: When a layer-by-layer or per-basin view of the trapped water is useful, or to practice the broader monotonic-stack pattern.
- **Two Pointers**: When memory is constrained or the interviewer asks for the optimal space solution.
- **Prefix and Suffix Maximums with accumulate**: The Pythonic default whenever the `O(n)` space is acceptable and readability is the deciding factor, since it states both sweeps as the folds they are and leaves only the depth formula to read. Prefer the explicit loops when the reversal idiom would obscure things for the audience, such as teaching the recurrences themselves or porting to a language with no equivalent helper.

### Optimization Notes

- The Brute Force recomputes the same wall heights for every bar; the Prefix and Suffix Maximums approach caches them, dropping the time from `O(n^2)` to `O(n)`.
- The four linear approaches differ only in space and in how the water is accounted for: per column, per layer, or implicitly.
- The statement's strict maxima keep the `max(0, ...)` clamp load-bearing in every column-based approach; only the inclusive running maxima of Two Pointers fold it away.
- The Two Pointers and accumulate variants need no empty-input guard beyond a length check, and the accumulate variant needs none at all: `accumulate` with `initial=0` yields a single-entry list for empty input, which the trim empties, so the summation loop never runs and `trapped` stays `0`.
