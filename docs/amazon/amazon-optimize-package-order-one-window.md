# [Optimize Package Order by Sorting One Window](https://www.fastprep.io/problems/amazon-optimize-package-order-one-window)

**Medium** | **NN minutes** | **Array, Sorting, Simulation**

Given an integer array of package priorities and a window size k, choose exactly one contiguous window of length k and sort only that window in ascending order.

Return the lexicographically smallest complete array obtainable by that operation.

## Examples

### Example 1

**Input:** `packages = [3,2,1,4]`, `k = 3`

**Output:** `[1,2,3,4]`

**Explanation:** Sorting the first three values produces the smallest possible first element.

### Example 2

**Input:** `packages = [1,4,3,2]`, `k = 2`

**Output:** `[1,3,4,2]`

**Explanation:** The window [4,3] is the first choice that improves the array lexicographically.

## Constraints

- `1 <= packages.length <= 200`
- `1 <= k <= packages.length`
- `Package priorities fit in signed 32-bit integers.`

## Solutions

### Enumerate Every Window

#### Derivation

The operation is fully described by one choice: the window's start. There are `len(packages) - k + 1` candidate starts, and each produces one concrete array: the untouched prefix, the window's values sorted ascending, and the untouched suffix. The lexicographically smallest complete array is the minimum over all candidates under element-by-element comparison:

1. For every start from `0` to `len(packages) - k`, build the candidate array.
2. Keep the lexicographically smallest candidate seen.

#### Walkthrough

Example 1, `packages = [3,2,1,4]`, `k = 3`, has two candidate starts. Start 0 sorts `[3,2,1]` into `[1,2,3]`, giving `[1,2,3,4]`. Start 1 sorts `[2,1,4]` into `[1,2,4]`, giving `[3,1,2,4]`. The first position already decides it: `1 < 3`, so `[1,2,3,4]` wins, matching the expected output. Example 2, `packages = [1,4,3,2]`, `k = 2`, has three starts; start 0 sorts `[1,4]` with no change, start 1 sorts `[4,3]` into `[3,4]` giving `[1,3,4,2]`, and start 2 sorts `[3,2]` into `[2,3]` giving `[1,4,2,3]`; comparing position 1 (`3` versus `4`) elects `[1,3,4,2]`, the expected output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, packages: List[int], k: int) -> List[int]:
        """Return the smallest array after sorting exactly one window of length k.

        Time:  O((n - k + 1) * (n + k log k)): each candidate costs a sort
            plus a full-array comparison.
        Space: O(n): one candidate array at a time.
        """
        best: List[int] = list(packages)
        for window_start in range(len(packages) - k + 1):
            candidate = (
                packages[:window_start]
                + sorted(packages[window_start : window_start + k])
                + packages[window_start + k :]
            )
            if candidate < best:
                best = candidate
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n - k + 1) * (n + k log k))`

Every one of the `n - k + 1` starts pays a `k log k` sort and an `O(n)` build-and-compare.

##### Space Complexity: `O(n)`

One candidate list at a time plus the running best.

#### Key Insights

- The choice space is one-dimensional: a start index, so exhaustive enumeration is the definitional baseline.
- Element-by-element comparison decides at the first differing position, so most candidate comparisons stop early in practice, but the worst case stays linear per candidate.

### First-Divergence Window

#### Derivation

A window starting at `s` can only change positions inside `[s, s + k - 1]`, and any value it can bring to position `p` comes from `[p, s + k - 1]`, a subset of `[p, p + k - 1]`. Scan from the left and let `i` be the first position where `packages[i]` exceeds the minimum in `packages[i + 1 : i + k]`: a strictly smaller value sits within one window's reach to the right. If no such `i` exists, no window changes the array and it is already the answer. For any start `s < i`, sorting cannot decrease any position before `i`: a decrease at some `p < i` would mean a smaller value reached `p` from `[p, s + k - 1]`, which is inside `[p, p + k - 1]`, contradicting `i` being the first such position; and an increase at an early position is immediately worse. At position `i` itself, the window starting exactly at `i` delivers `min(packages[i : i + k])`, the smallest value any covering window can place there, because every other covering window draws from a subset of that range. The window starting at `i` therefore dominates:

1. Compute, for each position, the minimum over the next `k - 1` positions (a monotonic deque keeps this linear).
2. Find the first `i` whose value exceeds that right-minimum; if none, return the array unchanged.
3. Sort `packages[i : i + k]` in place and return.

#### Walkthrough

Example 1, `[3,2,1,4]`, `k = 3`: at `i = 0`, the value `3` exceeds the minimum of `[2,1]`, which is `1`, so the window starts at 0 and sorting `[3,2,1]` gives `[1,2,3,4]`. Example 2, `[1,4,3,2]`, `k = 2`: position 0 has `1` against a right-minimum of `4`, no improvement; position 1 has `4` against `3`, improvement, so the window `[4,3]` sorts into `[3,4]`, giving `[1,3,4,2]`.

#### Solution

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, packages: List[int], k: int) -> List[int]:
        """Return the smallest array after sorting exactly one window of length k.

        Time:  O(n + k log k): one deque scan to locate the divergence, one
            sort of the winning window.
        Space: O(k): the deque and the sorted slice.
        """
        packages = list(packages)
        total = len(packages)
        reach = k - 1
        right_minima = [total] * total
        candidates: deque = deque()
        for scan in range(total - 1, 0, -1):
            while candidates and packages[candidates[-1]] >= packages[scan]:
                candidates.pop()
            candidates.append(scan)
            if candidates[0] > scan - 1 + reach:
                candidates.popleft()
            right_minima[scan - 1] = candidates[0]
        for position in range(total):
            index = right_minima[position]
            if index < total and packages[position] > packages[index]:
                packages[position : position + k] = sorted(
                    packages[position : position + k]
                )
                break
        return packages
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + k log k)`

Each index enters and leaves the deque at most once; the final sort covers only the winning window.

##### Space Complexity: `O(n)`

The right-minima table holds one index per position; the deque inside it holds at most `k` indices.

#### Key Insights

- The first position any window can decrease dictates the winner; every earlier window can only match or worsen positions before it.
- A monotonic deque turns "minimum within the next `k - 1` positions" into one linear pass; pruning uses the bound of the position each minimum serves.
- The subset argument (a window starting left of `p` draws `p`'s value from a subset of `[p, p + k - 1]`) is the whole correctness story.

## Comparison of Solutions

### Time Complexity

- **Enumerate Every Window**: `O((n - k + 1) * (n + k log k))` - every start pays a sort and a comparison.
- **First-Divergence Window**: `O(n + k log k)` - one scan plus one sort.

### Space Complexity

- **Enumerate Every Window**: `O(n)` - candidate arrays.
- **First-Divergence Window**: `O(n)` - the right-minima table, with only `O(k)` live deque state.

### Trade-offs

- The baseline is short and obviously correct against the definition; the greedy rung needs the reach argument to justify skipping starts.
- The greedy copies once and sorts in place; the baseline rebuilds every candidate.

### When to Use Each

- **Enumerate Every Window**: at `n <= 200` the constraints allow it everywhere; it doubles as the cross-check oracle for the greedy in tests.
- **First-Divergence Window**: when `n` grows far past the constraint's scale or the operation runs inside a larger loop.

### Optimization Notes

- Both rungs are deterministic; equal candidates resolve to the earliest window, which is also what the scan produces.
- The deque can be dropped for a sparse-table or block-minimum if `k` is tiny and `n` enormous, but the asymptotics above already hold.
