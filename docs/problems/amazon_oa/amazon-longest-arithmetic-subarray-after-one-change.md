# [Longest Arithmetic Subarray After One Change](https://www.fastprep.io/problems/amazon-longest-arithmetic-subarray-after-one-change)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given an integer array deviation.

You may change at most one element of the array to any integer value. After making at most one change, find the maximum possible length of a contiguous subarray that forms an arithmetic progression.

The changed element stays at its original index and may be used to connect the unchanged elements before it and after it into one longer arithmetic subarray.

A contiguous subarray forms an arithmetic progression if the difference between every pair of consecutive elements in that subarray is the same.

## Examples

### Example 1

**Input:** `deviation = [8, 5, 2, 1, 100]`

**Output:** `4`

**Explanation:** Change 1 to -1. The contiguous subarray [8,5,2,-1] has common difference -3, so its length is 4.

### Example 2

**Input:** `deviation = [1, 2, 3, 4, 100, 6, 7, 8, 9, 10]`

**Output:** `10`

**Explanation:** Change 100 to 5. The entire array becomes an arithmetic progression with common difference 1.

## Constraints

- `Constraints:`
- `1 <= deviation.length <= 105`
- `-109 <= deviation[i] <= 109`
- `You may change at most one element, and the changed value may be any integer.`

## Solutions

### Brute Force over Windows

#### Derivation

The problem states a property of subarrays with a repair budget, so the literal solution tests every subarray for the property directly: for each window, decide whether at most one element change turns it into an arithmetic progression. The per-window test reads the gaps once and counts where adjacent gaps disagree: a clean window has no disagreement, a window with exactly one disagreement between `gaps[break_position]` and `gaps[break_position + 1]` is repairable only by changing the element those two gaps share (which replaces both by the bridge value `(deviation[change + 1] - deviation[change - 1]) / 2`), and a window with disagreements spread further apart is beyond repair:

1. Loop `left` and `right` over every window with at least two elements.
2. Collect `gaps`, the differences of consecutive elements in the window.
3. `window_works` tries every element of the window as the changed one:
   removing the one or two gaps the change replaces must leave a uniform
   `kept` list, and when two gaps go, the bridge
   `(deviation[change + 1] - deviation[change - 1]) / 2` must be an integer
   equal to that kept gap. A change at the window edge replaces one gap
   freely, so only the kept uniformity matters there.
4. Track the largest window that works.

#### Walkthrough

Example 1, `deviation = [8, 5, 2, 1, 100]`. Two windows decide the answer; each line shows the window's gaps and the verdict:

```text
window [0..4]   gaps [-3, -3, -1, 99]
                best repair: change element 3 (value 1), it replaces
                the two gaps -1 and 99, kept gaps [-3, -3]
                bridge = (100 - 2) / 2 = 49, but 49 != -3 -> infeasible
window [0..3]   gaps [-3, -3, -1]
                change element 3, the window's last element:
                one gap replaced freely -> [-3, -3, -3] -> works, length 4
```

The length-4 window wins, and the expected Output is `4`.

#### Solution

The code is the double window loop with the gap verdict as a helper:

```python
from typing import List


class Solution:
    def solve(self, deviation: List[int]) -> int:
        length = len(deviation)
        best = min(length, 2)

        def window_works(left: int, right: int) -> bool:
            gaps = [deviation[end + 1] - deviation[end]
                    for end in range(left, right)]
            gap_count = len(gaps)
            for change in range(left, right + 1):
                affected = ({change - 1 - left, change - left}
                            & set(range(gap_count)))
                kept = [gap for gap_position, gap in enumerate(gaps)
                        if gap_position not in affected]
                if len(set(kept)) > 1:
                    continue
                if len(affected) == 2:
                    endpoint_sum = (deviation[change + 1]
                                    - deviation[change - 1])
                    if endpoint_sum % 2 != 0:
                        continue
                    if kept and endpoint_sum // 2 != kept[0]:
                        continue
                return True
            return False

        for left in range(length):
            for right in range(left + 1, length):
                if window_works(left, right):
                    best = max(best, right - left + 1)
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L^3)`

`O(L^2)` windows, each inspected in `O(L)` to build and scan the gaps.

##### Space Complexity: `O(L)`

The `gaps` list for one window at a time.

#### Key Insights

- The gap sequence encodes everything: a window is an arithmetic progression exactly when its gaps are uniform, and one change edits at most two adjacent gaps.
- The edge change is the easy case: replacing a single boundary gap is free, so any window whose only defect sits at a boundary works.
- The interior bridge is where brute force earns its keep: the replaced pair must sum to twice the kept gap, which the double loop tests exhaustively and the optimal solution tests analytically.

### Forward and Backward Runs Around the Change

#### Derivation

The brute force re-reads every window although neighboring windows share almost all their gaps. The structural fact underneath is that one change splits any answer into three pieces: the unchanged run before the changed element, the unchanged run after it, and the changed element itself. Each run is a longest arithmetic progression pinned to an endpoint, and endpoint-pinned runs are computable for every position in one sweep each: `forward_run[position]` grows while the last two gaps keep agreeing, and `backward_run[position]` grows the same way right to left.

The change sweep then combines the pieces per candidate `change`. The dropped run pieces give `forward_run[change - 1] + 1` and `backward_run[change + 1] + 1`. The bridge combination needs the changed value to serve both sides at once: the endpoints force `bridge = (deviation[change + 1] - deviation[change - 1]) / 2`, each side accepts the bridge only when its own internal difference agrees (a longer run pins its difference; a single-element run imposes nothing), and the two forced values must be equal, which the endpoint parity test decides first:

1. Build `forward_run` left to right: continue the run while the last two
   gaps agree, otherwise restart at length `2`.
2. Build `backward_run` right to left by the mirrored rule.
3. For each `change`, take the one-sided candidates
   `forward_run[change - 1] + 1` and `backward_run[change + 1] + 1`.
4. When `change` is interior and the endpoint difference
   `deviation[change + 1] - deviation[change - 1]` is even, compute
   `bridge`, truncate each side to a single element when its pinned
   difference disagrees with the bridge, and take
   `left_usable + right_usable + 1`.
5. Return the largest candidate seen.

#### Recurrence

Let `forward_run[position]` be the length of the longest arithmetic suffix ending exactly at `position`, and `backward_run[position]` the mirrored prefix starting at `position`:

$$ forward\_run[p] = \begin{cases}
1, & p = 0 \\[4pt]
2, & p = 1 \\[4pt]
forward\_run[p - 1] + 1, & p \ge 2 \text{ and } deviation[p] - deviation[p-1] = deviation[p-1] - deviation[p-2] \\[4pt]
2, & \text{otherwise}
\end{cases} $$

```text
forward_run[0] = 1
forward_run[1] = 2
forward_run[p] = forward_run[p - 1] + 1
                if deviation[p] - deviation[p - 1]
                   == deviation[p - 1] - deviation[p - 2], for p >= 2
forward_run[p] = 2                            otherwise

backward_run[L - 1] = 1
backward_run[L - 2] = 2
backward_run[p] = backward_run[p + 1] + 1
                if deviation[p + 1] - deviation[p]
                   == deviation[p + 2] - deviation[p + 1], for p <= L - 3
backward_run[p] = 2                           otherwise
```

The base cases say a run needs two elements to have a difference; the steps say a run extends exactly while its newest gap repeats the previous one. The answer is read from the change sweep, not from either table alone.

#### Walkthrough

Example 1, `deviation = [8, 5, 2, 1, 100]`. The gap sequence is `[-3, -3, -1, 99]`, which builds the run tables:

```text
position        0    1    2    3    4
deviation       8    5    2    1  100
forward_run     1    2    3    2    2
backward_run    3    2    2    2    1
```

The change sweep over each candidate `change`, with the bridge value when the endpoints allow one:

```text
change 0   right piece backward_run[1] + 1 = 3                 best 3
change 1   left piece forward_run[0] + 1 = 2
           right piece backward_run[2] + 1 = 3
           endpoints 8 and 2: bridge (2 - 8) / 2 = -3
           left run 1 (nothing pinned); right run 2 pins 99
           99 != -3 -> right truncates to 1: 1 + 1 + 1 = 3     best 3
change 2   left piece forward_run[1] + 1 = 3
           right piece backward_run[3] + 1 = 3
           endpoints 5 and 1: bridge (1 - 5) / 2 = -2
           left pins -3, right pins 99: both truncate
           to 1: 1 + 1 + 1 = 3                                 best 3
change 3   left piece forward_run[2] + 1 = 4                   best 4
           endpoints 2 and 100: bridge 98 / 2 = 49
           left pins -3, right run 1: 1 + 1 + 1 = 3, below 4
change 4   left piece forward_run[3] + 1 = 3                   best 4
```

The sweep peaks at `change 3` with the one-sided candidate `4`: changing the `1` extends the `[8, 5, 2]` suffix by one repaired element, matching the expected Output. (Example 2 peaks at `change 4`, the `100`: `forward_run[3] = 4`, `backward_run[5] = 5`, bridge `(6 - 4) / 2 = 1` agrees with both pinned differences of `1`, so `4 + 5 + 1 = 10`.)

#### Solution

The code is the two run tables and the change sweep with the bridge test:

```python
from typing import List


class Solution:
    def solve(self, deviation: List[int]) -> int:
        length = len(deviation)
        if length <= 2:
            return length

        forward_run = [1] * length
        for position in range(1, length):
            if (position >= 2
                    and deviation[position] - deviation[position - 1]
                    == deviation[position - 1] - deviation[position - 2]):
                forward_run[position] = forward_run[position - 1] + 1
            else:
                forward_run[position] = 2

        backward_run = [1] * length
        for position in range(length - 2, -1, -1):
            if (position + 2 < length
                    and deviation[position + 1] - deviation[position]
                    == deviation[position + 2] - deviation[position + 1]):
                backward_run[position] = backward_run[position + 1] + 1
            else:
                backward_run[position] = 2

        best = 2
        for change in range(length):
            if change >= 1:
                best = max(best, forward_run[change - 1] + 1)
            if change + 1 < length:
                best = max(best, backward_run[change + 1] + 1)
            if change == 0 or change == length - 1:
                continue
            endpoint_sum = deviation[change + 1] - deviation[change - 1]
            if endpoint_sum % 2 != 0:
                continue
            bridge = endpoint_sum // 2
            left_run = forward_run[change - 1]
            left_diff = (deviation[change - 1] - deviation[change - 2]
                         if change >= 2 else None)
            left_usable = (left_run if left_run < 2 or left_diff == bridge
                           else 1)
            right_run = backward_run[change + 1]
            right_diff = (deviation[change + 2] - deviation[change + 1]
                          if change + 2 < length else None)
            right_usable = (right_run if right_run < 2 or right_diff == bridge
                            else 1)
            best = max(best, left_usable + right_usable + 1)
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L)`

Two sweeps build the run tables and one sweep tries every change point; each step is constant work.

##### Space Complexity: `O(L)`

The two run tables; they can be replaced by rolling values if only the sweep's neighbors are kept.

#### Key Insights

- One change partitions the answer at the changed index, so "longest repairable window" decomposes into endpoint-pinned runs plus one bridge test per index.
- The bridge is forced twice over: the endpoints fix its value as `(right_endpoint - left_endpoint) / 2`, and the parity of the endpoint difference decides up front whether such a value exists.
- A run longer than one element carries a pinned internal difference and must agree with the bridge; a single-element run carries nothing and always merges. Skipping that truncation rule overcounts windows where the run heads in the wrong direction.
- `min(length, 2)` is the honest floor: any one or two element window is an arithmetic progression regardless of values, with or without a change.

## Comparison of Solutions

### Time Complexity

- **Brute Force over Windows**: `O(L^3)` - every window re-derives its gaps from scratch.
- **Forward and Backward Runs Around the Change**: `O(L)` - two run sweeps and one change sweep.

### Space Complexity

- **Brute Force over Windows**: `O(L)` - the gap list of the current window.
- **Forward and Backward Runs Around the Change**: `O(L)` - the two run tables.

### Trade-offs

- **Brute Force over Windows**: a direct transcription of the problem statement, and small enough to test by hand, but cubic time collapses quickly as the array grows.
- **Forward and Backward Runs Around the Change**: linear in both time and space, at the cost of the bridge algebra whose details (parity, pinned differences, truncation) each hide an off-by-one.

### When to Use Each

- **Brute Force over Windows**: validating the linear solution on small arrays, or when the change semantics are still being pinned down.
- **Forward and Backward Runs Around the Change (Recommended)**: the interview answer: the decomposition is natural to explain and the implementation is two sweeps and one loop.

### Optimization Notes

- The parity test `endpoint_sum % 2 != 0` must precede the bridge division: with integer values an odd endpoint difference admits no changed element at all.
- The truncation rule (a disagreeing run falls back to one element) is the difference between a correct solution and an overcounting one; the brute force never faces it because it tests whole windows.
- Example 2's whole-array answer `10` is the bridge case in its cleanest form: both runs pin difference `1`, the endpoints `4` and `6` average to the same value, and the changed element welds the halves seamlessly.
