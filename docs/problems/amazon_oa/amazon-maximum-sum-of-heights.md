# [Maximum Sum of Heights](https://www.fastprep.io/problems/amazon-maximum-sum-of-heights)

**Hard** | **NN minutes** | **Array, Stack, Dynamic Programming**

Given positive maximum heights maxHeights, choose a positive height for every index so that height[i] <= maxHeights[i]. The resulting array must be mountain-shaped: for some peak index, heights do not decrease before the peak and do not increase after it.

Return the maximum possible sum of the chosen heights.

Interview follow-upThe interviewer asked follow-up questions about the approach, complexity, and possible alternatives.

## Examples

### Example 1

**Input:** `maxHeights = [5,3,4,1,1]`

**Output:** `13`

**Explanation:** Choosing [5,3,3,1,1] forms a mountain with sum 13.

### Example 2

**Input:** `maxHeights = [6,5,3,9,2,7]`

**Output:** `22`

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-maximum-sum-of-heights; fill them in. -->

## Solutions

### Recompute Per Peak

#### Derivation

The most literal reading of the statement: some peak index defines the mountain, and once the peak is fixed the whole mountain is forced. Climbing non-decreasing into the peak caps every left cell at the smallest allowance between it and the peak, so the pointwise-largest feasible choice is `heights[position] = min(maxHeights[position..peak])` on the left and `heights[position] = min(maxHeights[peak..position])` on the right. Trying every peak and keeping the best total answers the question:

1. For each `peak` in `range(length)`:
2. Set `running = maxHeights[peak]` and `total = running`; walk `position`
   from `peak - 1` down to `0`, keeping `running = min(running,
   maxHeights[position])` and adding it to `total`.
3. Reset `running = maxHeights[peak]`; walk `position` from `peak + 1` up to
   `length - 1`, keeping `running = min(running, maxHeights[position])` and
   adding it to `total`.
4. Keep the largest total in `best_sum` and return it.

#### Walkthrough

Example 1, `maxHeights = [5,3,4,1,1]`. The peak `2` (value `4`) builds outward with the running cap:

```text
peak 2, running starts at 4
left walk:  position 1: running = min(4, 3) = 3, total = 4 + 3 = 7
            position 0: running = min(3, 5) = 3, total = 7 + 3 = 10
right walk: position 3: running = min(4, 1) = 1, total = 10 + 1 = 11
            position 4: running = min(1, 1) = 1, total = 11 + 1 = 12
```

That builds `[3,3,4,1,1]` and sums to `12`, not the winner. The winning peak is `0` (value `5`):

```text
peak 0, running starts at 5
left walk:  nothing to the left, total = 5
right walk: position 1: running = min(5, 3) = 3, total = 5 + 3 = 8
            position 2: running = min(3, 4) = 3, total = 8 + 3 = 11
            position 3: running = min(3, 1) = 1, total = 11 + 1 = 12
            position 4: running = min(1, 1) = 1, total = 12 + 1 = 13
```

The mountain `[5,3,3,1,1]` sums to `13`, matching the expected Output, and no other peak beats it (peak `1` reaches only `11`, with `[3,3,3,1,1]`).

#### Solution

```python
from typing import List


class Solution:
    def maximumSumOfHeights(self, maxHeights: List[int]) -> int:
        length = len(maxHeights)
        best_sum = 0
        for peak in range(length):
            total = maxHeights[peak]
            running = maxHeights[peak]
            for position in range(peak - 1, -1, -1):
                running = min(running, maxHeights[position])
                total += running
            running = maxHeights[peak]
            for position in range(peak + 1, length):
                running = min(running, maxHeights[position])
                total += running
            best_sum = max(best_sum, total)
        return best_sum
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` candidate peaks triggers two walks that together cross the whole array.

##### Space Complexity: `O(1)`

Only the running cap, the accumulating total, and the loop positions live outside the input.

#### Key Insights

- Once the peak is fixed, the pointwise-maximal mountain is forced: every height is the minimum of the allowances between it and the peak, so no optimization inside a peak remains.
- The peak does not have to be a local maximum of `maxHeights` for the construction to work; capping makes the built array mountain-shaped regardless.
- Adjacent peaks share almost all their work: moving the peak one step re-derives nearly the same two walks, and that redundancy is what the faster solution removes.

### Monotonic Stack Sweeps

#### Derivation

The two walks per peak are the flaw: the left walk from `peak` repeats almost exactly the left walk from `peak + 1`. Name what each walk accumulates. Let `prefix_sums[i]` be the sum over all `p <= i` of `min(maxHeights[p..i])`: this is exactly the total the left walk builds when the peak is `i`, peak included, because the height assigned to `p` is the minimum allowance between `p` and the peak. The question becomes: can every `prefix_sums[i]` be built in one sweep? The answer lives in the nearest previous index with a smaller-or-equal height. Call it `previous`. Splitting the sum at `previous`:

- For `p` in `(previous, i]`, every element between `previous + 1` and `i` is
  strictly greater than `maxHeights[i]` (those indices were popped from the
  stack for exactly that reason), so `min(maxHeights[p..i]) = maxHeights[i]`.
- For `p <= previous`, the minimum over `[p..i]` equals the minimum over
  `[p..previous]`, because `maxHeights[previous] <= maxHeights[i]` caps the
  left side at or below the new bar.

So `prefix_sums[i] = prefix_sums[previous] + maxHeights[i] * (i - previous)`: one finished sum inherited plus one rectangle of the new bar's height. A [monotonic stack](https://en.wikipedia.org/wiki/Monotonic_stack) of indices with non-decreasing heights finds `previous` by popping strictly greater heights, and each index enters and leaves the stack once. `suffix_sums[i]`, the mirror sum over `p >= i`, falls out of a right-to-left sweep with the same pop rule, using the nearest following index with a smaller-or-equal height. Because both sums count the peak cell, the best mountain with peak `i` is `prefix_sums[i] + suffix_sums[i] - maxHeights[i]`:

1. Sweep left to right with a stack, popping while the top's height is
   strictly greater than the new one; fill `prefix_sums[i]` by the recurrence
   above, with `previous = -1` on an empty stack.
2. Sweep right to left the same way; fill `suffix_sums[i]`, with
   `successor = length` on an empty stack.
3. Return the maximum of
   `prefix_sums[peak] + suffix_sums[peak] - maxHeights[peak]` over all peaks.

#### Formula

With `previous` the nearest index left of `i` whose height is at most `maxHeights[i]` (or `-1`), and `successor` its mirror on the right (or `length`):

$$ \text{prefix\_sums}[i] = \text{prefix\_sums}[\text{previous}] + \text{maxHeights}[i] \times (i - \text{previous}) $$
$$ \text{suffix\_sums}[i] = \text{suffix\_sums}[\text{successor}] + \text{maxHeights}[i] \times (\text{successor} - i) $$

```text
prefix_sums[i]  = prefix_sums[previous]  + maxHeights[i] * (i - previous)
suffix_sums[i]  = suffix_sums[successor] + maxHeights[i] * (successor - i)
base case       = maxHeights[i] times the distance to the array edge
answer          = max over i of prefix_sums[i] + suffix_sums[i] - maxHeights[i]
```

The rectangle term credits `maxHeights[i]` to every position the new bar dominates up to the nearest bar that caps it; the inherited term reuses the finished sum of that capping bar. The subtraction removes the peak, which both sums count.

#### Walkthrough

Example 1, `maxHeights = [5,3,4,1,1]`, left sweep, stack holding indices with non-decreasing heights:

```text
i=0  h=5   stack empty -> previous -1   prefix_sums[0] = 5*1 = 5      stack [0]
i=1  h=3   pop 0 (5 > 3) -> previous -1 prefix_sums[1] = 3*2 = 6      stack [1]
i=2  h=4   top 1 (h=3): no pop -> previous 1
                                        prefix_sums[2] = 6 + 4*1 = 10 stack [1, 2]
i=3  h=1   pop 2 (4 > 1), pop 1 (3 > 1) -> previous -1
                                        prefix_sums[3] = 1*4 = 4      stack [3]
i=4  h=1   top 3 (h=1): no pop -> previous 3
                                        prefix_sums[4] = 4 + 1*1 = 5  stack [3, 4]
```

Reading `prefix_sums[2] = 10` back as subarray minimums: `min(5,3,4) + min(3,4) + 4 = 3 + 3 + 4 = 10`, exactly the left walk for peak `2`. The right sweep mirrors it:

```text
i=4  h=1   stack empty -> successor 5   suffix_sums[4] = 1*1 = 1      stack [4]
i=3  h=1   top 4 (h=1): no pop -> successor 4
                                        suffix_sums[3] = 1 + 1*1 = 2  stack [3, 4]
i=2  h=4   tops 4, 3 (h=1, 1): no pop -> successor 3
                                        suffix_sums[2] = 2 + 4*1 = 6  stack [2, 3, 4]
i=1  h=3   pop 2 (4 > 3); top 3 (h=1): no pop -> successor 3
                                        suffix_sums[1] = 2 + 3*2 = 8  stack [1, 3, 4]
i=0  h=5   tops 1, 3, 4 (h=3, 1, 1): no pop -> successor 1
                                        suffix_sums[0] = 8 + 5*1 = 13 stack [0, 1, 3, 4]
```

`suffix_sums[2] = 6` reads back as `4 + min(4,1) + min(4,1,1) = 6`, the right walk for peak `2`. Combining, subtracting the peak once:

```text
peak 0   5 + 13 - 5 = 13
peak 1   6 + 8 - 3 = 11
peak 2   10 + 6 - 4 = 12
peak 3   4 + 2 - 1 = 5
peak 4   5 + 1 - 1 = 5
```

The best is `13` at peak `0`, matching the expected Output and the brute force's winner.

#### Solution

The code is the two sweeps from the walkthrough plus one combination scan; the pop condition is strict (`>`) in both directions, so equal heights stay on the stack and the boundary indices they offer remain valid caps.

```python
from typing import List


class Solution:
    def maximumSumOfHeights(self, maxHeights: List[int]) -> int:
        length = len(maxHeights)

        prefix_sums = [0] * length
        stack = []
        for position in range(length):
            while stack and maxHeights[stack[-1]] > maxHeights[position]:
                stack.pop()
            if stack:
                previous = stack[-1]
                prefix_sums[position] = (prefix_sums[previous]
                                         + maxHeights[position] * (position - previous))
            else:
                prefix_sums[position] = maxHeights[position] * (position + 1)
            stack.append(position)

        suffix_sums = [0] * length
        stack = []
        for position in range(length - 1, -1, -1):
            while stack and maxHeights[stack[-1]] > maxHeights[position]:
                stack.pop()
            if stack:
                successor = stack[-1]
                suffix_sums[position] = (suffix_sums[successor]
                                         + maxHeights[position] * (successor - position))
            else:
                suffix_sums[position] = maxHeights[position] * (length - position)
            stack.append(position)

        return max(prefix_sums[peak] + suffix_sums[peak] - maxHeights[peak]
                   for peak in range(length))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each index is pushed and popped at most once per sweep, and the combination scan is linear.

##### Space Complexity: `O(n)`

The two sum arrays plus the stack.

#### Key Insights

- The left walk for every peak is a subarray-minimum sum in disguise; the classic monotonic stack decomposition computes all of them in one sweep.
- The boundary index is a cap, not a floor: the nearest smaller-or-equal bar limits how far the new bar's height can be credited, and everything beyond it is inherited already finished.
- Strict (`>`) popping in both sweeps keeps equal-height bars on the stack, so the boundary they return is the nearest surviving cap; a non-strict pop is equally correct but changes which twin bar serves as the boundary.
- Both sums count the peak cell, so the combination subtracts `maxHeights[peak]` once; forgetting the subtraction inflates every candidate.

## Comparison of Solutions

### Time Complexity

- **Recompute Per Peak**: `O(n^2)` - two full walks for each of `n` candidate peaks.
- **Monotonic Stack Sweeps**: `O(n)` - constant amortized stack work per index in each sweep.

### Space Complexity

- **Recompute Per Peak**: `O(1)` - a running cap and total per walk.
- **Monotonic Stack Sweeps**: `O(n)` - the two sum arrays plus the stack.

### Trade-offs

- **Recompute Per Peak**: nearly no code and no invariants, but it re-derives overlapping walks for every peak, which collapses at the top of the constraint range.
- **Monotonic Stack Sweeps**: linear time and one pass per direction, at the cost of the boundary recurrence and its base cases, which are easy to get subtly wrong.

### When to Use Each

- **Recompute Per Peak**: as the first working answer in an interview, as a correctness oracle for the fast version on small inputs, or when `n` is small enough that the quadratic cost is irrelevant.
- **Monotonic Stack Sweeps (Recommended)**: whenever `n` can be large: it is the asymptotically optimal construction and the one the follow-up questions aim at.

### Optimization Notes

- The pop condition must be strict in both sweeps for the boundary to be a valid cap; using `>=` on one side still yields correct sums but points the boundary at a farther bar, changing the rectangle split but not the total.
- The base-case arms (`previous = -1`, `successor = length`) encode "nothing caps me", so the bar's height extends to the array edge; folding them into sentinel-free branches avoids allocating padded arrays.
- No peak can be skipped without being priced: a peak's total is not monotonic in its position, so the combination scan must run over the whole array before the maximum is known.
