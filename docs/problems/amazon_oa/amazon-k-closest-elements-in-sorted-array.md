# [K Closest Elements in a Sorted Array](https://www.fastprep.io/problems/amazon-k-closest-elements-in-sorted-array)

**Medium** | **NN minutes** | **Array, Binary Search, Two Pointers**

Given an integer array arr sorted in nondecreasing order, an integer k, and a target x, return the k values closest to x in ascending order.

A value a is closer than a value b when |a - x| < |b - x|. When the distances are equal, the smaller value is considered closer.

## Examples

### Example 1

**Input:** `arr = [-10,-4,-1,3,8,12]`, `k = 4`, `x = 2`

**Output:** `[-4,-1,3,8]`

**Explanation:** Values -4 and 8 are equally distant from 2; the smaller value wins the boundary tie.

### Example 2

**Input:** `arr = [2,4,6,8]`, `k = 1`, `x = 5`

**Output:** `[4]`

**Explanation:** Values 4 and 6 are both one unit away, so the smaller value 4 is selected.

### Example 3

**Input:** `arr = [5,6,7]`, `k = 2`, `x = 100`

**Output:** `[6,7]`

**Explanation:** The target lies to the right of every array value, so the last two values are closest.

## Constraints

- `1 <= arr.length <= 100000.`
- `1 <= k <= arr.length.`
- `arr is sorted in nondecreasing order.`
- `-1000000000 <= arr[i], x <= 1000000000.`

## Solutions

### Sort by Distance

#### Derivation

The most literal reading of "closest" is to make the closeness rule itself the sort order. The comparison rule (closer means smaller `abs(value - x)`, and the smaller value wins an equal distance) is exactly a sort key of `(abs(value - x), value)`, so one sort rewrites the array into closeness order, the first `k` entries are the answer set, and the required ascending output is one more sort away:

1. Sort a copy of `arr` by the key `(abs(value - x), value)`.
2. Take the first `k` entries; they are the `k` closest by the problem's own
   tie rule.
3. Sort those `k` entries ascending and return them.

#### Walkthrough

Example 1, `arr = [-10,-4,-1,3,8,12]`, `k = 4`, `x = 2`. Distances to `x = 2` decide the closeness order:

```text
value    -10  -4  -1   3   8  12
|v - 2|   12   6   3   1   6  10
```

Sorting by `(distance, value)` gives `[3 (1), -1 (3), -4 (6), 8 (6), 12 (10), -10 (12)]`; the equal-distance pair `-4` and `8` keeps `-4` ahead because `value` breaks the tie. The first `k = 4` entries are `3, -1, -4, 8`, and sorting them ascending returns `[-4, -1, 3, 8]`, matching the expected Output. The boundary pick is where the tie rule earns its place: `-4` and `8` tie at distance `6`, and only one slot remains.

#### Solution

The code is the key sort, the slice, and the ascending re-sort:

```python
from typing import List


class Solution:
    def solve(self, arr: List[int], k: int, x: int) -> List[int]:
        """Return the k values closest to x in ascending order.

        Time:  O(n log n) for the key sort, plus O(k log k) for the ascending
            re-sort of the k winners.
        Space: O(n) for the reordered copy of arr.
        """
        by_closeness = sorted(arr, key=lambda value: (abs(value - x), value))
        return sorted(by_closeness[:k])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The key sort dominates; re-sorting the `k` winners adds `O(k log k)`.

##### Space Complexity: `O(n)`

The key sort builds a reordered copy of the array.

#### Key Insights

- The problem's two-clause comparison rule collapses into a single tuple key `(abs(value - x), value)`, which removes all hand-written tie handling.
- The output does not come out of the closeness sort in ascending order, so the final re-sort is not optional.
- Sorting destroys the index structure the array arrived with, which is the cost every later approach removes.

### Two-Pointers Window Shrink

#### Derivation

Sorting by distance ignores the property the input already has: `arr` is sorted, and the values nearest `x` form one contiguous window. The window `[left, right]` can start as the whole array and shrink `len(arr) - k` times, each step discarding the endpoint farther from `x`; when distances tie, dropping the right endpoint keeps the smaller value, which is the tie rule again. Because the window is always contiguous inside the sorted array, whatever survives is already ascending:

1. Start `left = 0` and `right = len(arr) - 1`.
2. While the window holds more than `k` values, compare
   `abs(arr[left] - x)` with `abs(arr[right] - x)`: move `left` right when the
   left distance is strictly larger, otherwise move `right` left.
3. Return `arr[left:right + 1]`, contiguous and already sorted ascending.

#### Walkthrough

Example 1, `arr = [-10,-4,-1,3,8,12]`, `k = 4`, `x = 2`. The window shrinks twice, from six values to four:

```text
window [-10..12]  |-10-2| = 12 vs |12-2| = 10  12 > 10 -> drop left,  left = 1
window [ -4..12]  |-4-2| = 6  vs |12-2| = 10  6 <= 10 -> drop right, right = 4
window [ -4..8 ]  holds 4 values -> stop
```

The surviving window `[-4, -1, 3, 8]` matches the expected Output. The second step is the tie-adjacent case in action: the left distance `6` is not strictly larger, so the right end `12` (distance `10`) is discarded and `-4` survives. Example 2 shrinks `[2, 4, 6, 8]` the same way: with `|2-5| = |8-5| = 3` the right end `8` drops first, then the left end `2` (`6` is farther from `5` than `4` is), then the right end `6` on the `4`-`6` tie, and finally the left end `2` again, leaving the window `[4]`; on each tie the smaller value survives, as the tie rule requires.

#### Solution

The code is the shrink loop and the window slice; no output sort is needed because the window never leaves the sorted array:

```python
from typing import List


class Solution:
    def solve(self, arr: List[int], k: int, x: int) -> List[int]:
        """Return the k values closest to x in ascending order.

        Time:  O(n - k) for the shrinking scans plus the final window copy.
        Space: O(1) auxiliary, or O(k) for the returned slice.
        """
        left, right = 0, len(arr) - 1
        while right - left + 1 > k:
            if abs(arr[left] - x) > abs(arr[right] - x):
                left += 1
            else:
                right -= 1
        return arr[left:right + 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n - k)`

Every shrink step discards exactly one endpoint, and exactly `n - k` steps run before the window holds `k` values.

##### Space Complexity: `O(1)`

Two indices; the returned slice is the output itself.

#### Key Insights

- The `k` closest values of a sorted array are always contiguous, so the answer is a window and never a scattered set.
- The tie rule falls out of the comparison: moving `right` left on a tie keeps the smaller value, exactly as the problem demands.
- The result is already ascending, so this approach is where the output sort of the brute force disappears.

### Binary Search on the Window Start

#### Derivation

Window shrink touches every discarded element once, which is `O(n)` even when `k` is tiny. The repair asks a binary-searchable question instead: what is the leftmost start `left` such that the window `arr[left .. left + k - 1]` is the answer? A start is too far left exactly when stepping one window to the right strictly improves it, and for sorted `arr` that comparison needs only the two boundary values `arr[left]` and `arr[left + k]`: each is farthest from `x` on its own side of the window's span, so if `abs(arr[left] - x) > abs(arr[left + k] - x)` the window must slide right. Searching the start over `[0, n - k]` costs `O(log(n - k))` comparisons:

1. Set `low = 0` and `high = len(arr) - k`, the last legal window start.
2. While `low < high`, probe `mid = (low + high) // 2`.
3. When `abs(arr[mid] - x) > abs(arr[mid + k] - x)`, the window starts too far
   left: set `low = mid + 1`. Otherwise set `high = mid`.
4. Return `arr[low:low + k]`.

#### Walkthrough

Example 1, `arr = [-10,-4,-1,3,8,12]`, `k = 4`, `x = 2`. Legal starts are `0`, `1`, `2`:

```text
probe mid = 1   |arr[1]−2| = 6   vs |arr[5]−2| = 10   6 <= 10 -> high = 1
probe mid = 0   |arr[0]−2| = 12  vs |arr[4]−2| = 6    12 > 6  -> low = 1
low == high = 1 -> window arr[1:5]
```

The returned window `[-4, -1, 3, 8]` matches the expected Output. The first probe is the tie-adjacent case again: `6 <= 10` refuses to move the start past index `1`, because the boundary value `-4` (the tie winner over `8`) would be lost. Example 3, `arr = [5,6,7]` with `x = 100`: the single probe `mid = 0` compares `95` with `93`, slides `low` to `1`, and the window `[6, 7]` matches.

#### Solution

The code is the binary search over window starts and the final slice:

```python
from typing import List


class Solution:
    def solve(self, arr: List[int], k: int, x: int) -> List[int]:
        """Return the k values closest to x in ascending order.

        Time:  O(log(n - k)) for the start search plus the final window copy.
        Space: O(1) auxiliary, or O(k) for the returned slice.
        """
        low, high = 0, len(arr) - k
        while low < high:
            mid = (low + high) // 2
            if abs(arr[mid] - x) > abs(arr[mid + k] - x):
                low = mid + 1
            else:
                high = mid
        return arr[low:low + k]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log(n - k))`

The search halves the start range until one start remains; each probe is two distance computations.

##### Space Complexity: `O(1)`

Two range bounds; the returned slice is the output itself.

#### Key Insights

- Comparing only the window edges works because the interior of a contiguous window cannot beat both edges: whatever the split of `x` across the window, `arr[mid]` and `arr[mid + k]` are the extreme candidates of their halves.
- On an edge tie the window stays put (`high = mid`), which keeps the smaller value at the left edge and matches the tie rule.
- The start range has exactly `n - k + 1` legal positions, so `high = len(arr) - k` is the last legal start, not an exclusive bound.

### One-Liner with a Key Sort

#### Derivation

After the sort-by-distance approach exists, its three steps collapse into one expression: sort with the tuple key, slice `k`, sort ascending. The algorithm is unchanged; only the intermediate names disappear:

1. Sort `arr` by `(abs(value - x), value)` and slice the first `k` entries.
2. Sort the slice ascending and return it.

#### Walkthrough

Example 2, `arr = [2,4,6,8]`, `k = 1`, `x = 5`: the key order is `4 (1), 6 (1), 2 (3), 8 (3)`, the slice of one entry is `[4]`, and the ascending re-sort returns `[4]`, matching the expected Output. The tie between `4` and `6` is resolved inside the key tuple, `value` ascending, before any slicing happens.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, arr: List[int], k: int, x: int) -> List[int]:
        """Return the k values closest to x in ascending order.

        Time:  O(n log n) for the key sort, plus O(k log k) for the re-sort.
        Space: O(n) for the reordered copy of arr.
        """
        return sorted(sorted(arr, key=lambda value: (abs(value - x), value))[:k])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Identical work to the sort-by-distance approach: one full key sort plus the winners' re-sort.

##### Space Complexity: `O(n)`

The inner sort builds a reordered copy of the array.

#### Key Insights

- The nested expression is the two-clause rule and the output order compressed into one line, readable only because each piece was derived separately above.
- It ranks last with the sort-by-distance approach: correct, but it pays `O(n log n)` and never uses the sortedness of the input.

## Comparison of Solutions

### Time Complexity

- **Sort by Distance**: `O(n log n)` - one full key sort dominates.
- **Two-Pointers Window Shrink**: `O(n - k)` - each discarded endpoint costs one comparison.
- **Binary Search on the Window Start**: `O(log(n - k))` - the start range halves per probe.
- **One-Liner with a Key Sort**: `O(n log n)` - same key sort and re-sort as the explicit version.

### Space Complexity

- **Sort by Distance**: `O(n)` - the key sort reorders a copy of the array.
- **Two-Pointers Window Shrink**: `O(1)` - two moving indices.
- **Binary Search on the Window Start**: `O(1)` - two range bounds.
- **One-Liner with a Key Sort**: `O(n)` - the inner sort's reordered copy.

### Trade-offs

- **Sort by Distance**: minimal reasoning to get a correct answer, but it discards the sorted-input property and pays a full sort for it.
- **Two-Pointers Window Shrink**: linear time, constant space, and already-ascending output, at the price of trusting the contiguity argument in an interview defense.
- **Binary Search on the Window Start**: logarithmic probes over a range instead of scans over data, with the subtlest correctness argument of the three (why two boundary distances suffice).
- **One-Liner with a Key Sort**: the same trade-offs as sort by distance, compressed past the point of easy explanation.

### When to Use Each

- **Two-Pointers Window Shrink (Recommended)**: the interview sweet spot: linear, constant space, and a contiguity story that is easy to state and defend.
- **Binary Search on the Window Start**: when the interviewer asks to beat linear, or in a follow-up where `n` is huge and `k` small.
- **Sort by Distance**: as the fast, correct baseline to state first while the window argument is being assembled.
- **One-Liner with a Key Sort**: for quick scripts and as a reference to cross-check the other approaches.

### Optimization Notes

- The two boundary distances `arr[mid]` and `arr[mid + k]` suffice only because the window is contiguous and `arr` sorted; comparing interior values would be wasted work and comparing fewer would be wrong.
- A common pitfall in the binary search is writing `high = len(arr) - 1`; the range being searched is window starts, whose last legal value is `len(arr) - k`.
- Another pitfall is breaking edge ties toward moving the start right (`low = mid` style); that can slide the window past the smaller of two equidistant boundary values and violates the tie rule.
- All approaches return the values themselves, not indices, and the ascending output of the window approaches is free because the window never leaves the sorted array.
