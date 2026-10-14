# [Maximize Adjacent Difference With One Reversal](https://www.fastprep.io/problems/amazon-maximize-adjacent-difference-with-one-reversal)

**Hard** | **NN minutes** | **Array, Greedy, Math**

Given an integer array values, define its score as the sum of abs(values[i] - values[i + 1]) over every adjacent pair.

You may reverse at most one contiguous subarray. Return the maximum score obtainable after the optional reversal.

## Examples

### Example 1

**Input:** `values = [2,3,1,5,4]`

**Output:** `10`

**Explanation:** The original score is 8. Reversing the subarray [3,1,5] produces [2,5,1,3,4], whose score is 10.

### Example 2

**Input:** `values = [1,2,3,4]`

**Output:** `5`

**Explanation:** Reversing [2,3] produces [1,3,2,4], with score 2 + 1 + 2 = 5.

## Constraints

- `1 <= values.length <= 10^5`
- `-10^9 <= values[i] <= 10^9`

## Solutions

### Reverse Every Subarray

#### Derivation

The score is a sum over adjacent pairs, and reversing `[left..right]` leaves every interior pair in place (reversed order, same absolute difference). Only the two boundary pairs can change. The baseline ignores that structure and simply tries everything: every `(left, right)` pair, rescoring the whole array each time:

1. Compute the original score.
2. For every subarray, build the reversal and rescore.
3. Return the maximum.

#### Walkthrough

Example 1, `values = [2,3,1,5,4]`, original score `1 + 2 + 4 + 1 = 8`. Reversing `[3,1,5]` produces `[2,5,1,3,4]` scoring `3 + 4 + 2 + 1 = 10`; no other reversal beats it, so the answer is `10`. Example 2, `values = [1,2,3,4]`, original score `3`; reversing `[2,3]` gives `[1,3,2,4]` scoring `2 + 1 + 2 = 5`, the expected output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        """Return the maximum adjacent-difference sum after one reversal.

        Time:  O(n^3): O(n^2) reversals, each rescored in O(n).
        Space: O(n) for the reversed copy.
        """

        def score(nums: List[int]) -> int:
            return sum(abs(left - right) for left, right in zip(nums, nums[1:]))

        best = score(values)
        for left in range(len(values)):
            for right in range(left + 1, len(values)):
                flipped = (
                    values[:left]
                    + values[left : right + 1][::-1]
                    + values[right + 1 :]
                )
                best = max(best, score(flipped))
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

Quadratic reversals with a linear rescore each; a toy rung at `n <= 10^5`.

##### Space Complexity: `O(n)`

One flipped copy at a time.

#### Key Insights

- Interior pairs are reversal-invariant: `|x - y| = |y - x|`, so only boundary pairs move the score.
- The full rescore is waste in hindsight, which the next rungs remove.

### Boundary Deltas Over Cut Pairs

#### Derivation

Name the cut positions: the cut at `k` is the adjacent pair `(values[k], values[k + 1])` with length `|values[k] - values[k + 1]|`. Reversing `[left..right]` with `left >= 1` and `right <= n - 2` replaces the pairs at cuts `i = left - 1` and `j = right` (with `i < j`) by `(values[i], values[j])` and `(values[i + 1], values[j + 1])`. The delta is therefore `|values[i] - values[j]| + |values[i + 1] - values[j + 1]| - length[i] - length[j]`, constant time per cut pair. Prefix reversals (`left = 0`) and suffix reversals (`right = n - 1`) change a single pair and get their own one-line candidates:

1. Precompute the cut lengths.
2. Sweep all interior cut pairs with the constant-time delta.
3. Add the best prefix and suffix single-pair candidates to the original score.

#### Walkthrough

Example 1: cut lengths are `1, 2, 4, 1` and the base score is `8`. The winning reversal `[3,1,5]` is `left = 1, right = 3`, so cuts `i = 0` and `j = 3`: delta `|2 - 5| + |3 - 4| - 1 - 1 = 3 + 1 - 2 = 2`, raising the score to `10`. Example 2: reversal `[2,3]` is `left = 1, right = 2`, cuts `i = 0` and `j = 2`: delta `|1 - 3| + |2 - 4| - 1 - 1 = 2 + 2 - 2 = 2`, raising `3` to `5`.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        """Return the maximum adjacent-difference sum after one reversal.

        Time:  O(n^2): every interior cut pair priced in constant time.
        Space: O(n) for the cut lengths.
        """
        size = len(values)
        lengths = [abs(values[k] - values[k + 1]) for k in range(size - 1)]
        base = sum(lengths)
        best = 0
        for cut in range(size - 1):
            if cut + 1 < size - 1:
                best = max(best, abs(values[0] - values[cut + 2]) - lengths[cut + 1])
            if cut - 1 >= 0:
                best = max(
                    best, abs(values[size - 1] - values[cut - 1]) - lengths[cut - 1]
                )
        for i in range(size - 1):
            for j in range(i + 1, size - 1):
                best = max(
                    best,
                    abs(values[i] - values[j])
                    + abs(values[i + 1] - values[j + 1])
                    - lengths[i]
                    - lengths[j],
                )
        return base + best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The interior cut-pair sweep dominates; `10^10` operations at the constraint ceiling still demands the final rung.

##### Space Complexity: `O(n)`

The cut-length list.

#### Key Insights

- Two cuts fully determine a reversal's effect: the delta formula is the whole problem compressed.
- Prefix and suffix reversals are single-cut degenerate cases with their own candidates.

### Sign-Combination Prefix Scan

#### Derivation

The interior delta is `cross(i, j) - length[i] - length[j]` with `cross = |a[i] - a[j]| + |a[i + 1] - a[j + 1]|` for cuts `i < j`. Absolute values decompose as `|x| = max(x, -x)`, so the cross term equals the maximum, over the four sign choices `(sigma, tau)` in `{±1}²`, of `sigma * (a[i] - a[j]) + tau * (a[i + 1] - a[j + 1])`. With the signs fixed, the expression separates by cut: define `prefix(cut) = sigma * a[cut] + tau * a[cut + 1] - length[cut]` and `suffix(cut) = sigma * a[cut] + tau * a[cut + 1] + length[cut]`, and the delta for that sign pair is `max over i < j of prefix(i) - suffix(j)`. A single left-to-right scan computes it by carrying the running maximum of `prefix`. Four sign pairs, four scans, linear total:

1. Compute the base score, the cut lengths, and the prefix/suffix single-cut candidates as before.
2. For each `(sigma, tau)`, sweep cuts left to right, carrying the running `prefix` maximum and combining it with each later cut's `suffix`.
3. Return the base plus the best delta found.

#### Walkthrough

Example 1, cuts `(2,3), (3,1), (1,5), (5,4)` with lengths `1, 2, 4, 1`, base `8`. The winning reversal needs cuts `i = 0, j = 3` where the cross `|2 - 5| + |3 - 4|` takes the negative sign on both terms, so `sigma = tau = -1`: `prefix(0) = -2 - 3 - 1 = -6`, `suffix(3) = -5 - 4 + 1 = -8`, delta `-6 - (-8) = 2`, and the score rises to `10`. No scan does better: along `sigma = tau = -1`, the suffix values are `suffix(1) = -3 - 1 + 2 = -2`, `suffix(2) = -1 - 5 + 4 = -2`, `suffix(3) = -8`, and the running prefix maxima before each are `-6`, then `max(-6, -3 - 1 - 2) = -6`, then `max(-6, -6) = -6` (`prefix(2) = -1 - 5 - 4 = -10`), giving candidates `-4`, `-4`, `2`; the other sign pairs top out at or below `0` on this input. Example 2, cuts `(1,2), (2,3), (3,4)` with lengths `1, 1, 1`, base `3`: at `sigma = tau = -1`, `prefix(0) = -1 - 2 - 1 = -4`, `suffix(2) = -3 - 4 + 1 = -6`, delta `2`, score `5`.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        """Return the maximum adjacent-difference sum after one reversal.

        Time:  O(n): four sign combinations, each one prefix-max scan.
        Space: O(n) for the cut lengths.
        """
        size = len(values)
        lengths = [abs(values[k] - values[k + 1]) for k in range(size - 1)]
        base = sum(lengths)
        best = 0
        for cut in range(size - 1):
            if cut + 1 < size - 1:
                best = max(best, abs(values[0] - values[cut + 2]) - lengths[cut + 1])
            if cut - 1 >= 0:
                best = max(
                    best, abs(values[size - 1] - values[cut - 1]) - lengths[cut - 1]
                )
        for sigma in (1, -1):
            for tau in (1, -1):
                running: int = None
                for cut in range(1, size - 1):
                    prefix = (
                        sigma * values[cut - 1] + tau * values[cut] - lengths[cut - 1]
                    )
                    running = prefix if running is None else max(running, prefix)
                    suffix = (
                        sigma * values[cut] + tau * values[cut + 1] + lengths[cut]
                    )
                    best = max(best, running - suffix)
        return base + best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two linear setup passes and four linear scans.

##### Space Complexity: `O(n)`

The cut-length list.

#### Key Insights

- `|x| = max(x, -x)` turns a two-sided absolute maximum into four separable maximums, one per sign pair.
- Separation is what buys the scan: with signs fixed, the earlier cut contributes a prefix value and the later cut a suffix value, and prefix maxima are running quantities.
- Each absolute value carries its own sign variable; folding both terms under one sign is the classic error this rung avoids.

## Comparison of Solutions

### Time Complexity

- **Reverse Every Subarray**: `O(n^3)` - the definition as code.
- **Boundary Deltas Over Cut Pairs**: `O(n^2)` - two cuts priced in constant time.
- **Sign-Combination Prefix Scan**: `O(n)` - four scans after one length pass.

### Space Complexity

- **Reverse Every Subarray**: `O(n)`.
- **Boundary Deltas Over Cut Pairs**: `O(n)`.
- **Sign-Combination Prefix Scan**: `O(n)`.

### Trade-offs

- Each rung keeps the previous as its oracle: the quadratic rung validates the linear one on random inputs, the cubic one validates the quadratic.
- The linear rung's correctness rests on the sign-separation argument rather than case enumeration.

### When to Use Each

- **Reverse Every Subarray**: teaching and tiny inputs.
- **Boundary Deltas Over Cut Pairs**: the natural interview middle rung; sufficient when `n` sits in the thousands.
- **Sign-Combination Prefix Scan**: `n = 10^5` and above.

### Optimization Notes

- The four scans can fold into one loop carrying four running maxima.
- Full-array reversal never changes the score (every pair maps to itself), so no rung considers it separately.
