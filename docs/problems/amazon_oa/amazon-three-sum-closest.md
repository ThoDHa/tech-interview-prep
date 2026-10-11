# [Three Sum Closest](https://www.fastprep.io/problems/amazon-three-sum-closest)

**Medium** | **NN minutes** | **Array, Sorting, Two Pointers**

Given an integer array nums and an integer target, choose three distinct indices and return the sum of their values that is closest to target.

If two obtainable sums are equally close, return the smaller sum.

## Examples

### Example 1

**Input:** `nums = [-1,2,1,-4]`, `target = 1`

**Output:** `2`

**Explanation:** The closest sum is -1 + 2 + 1 = 2.

### Example 2

**Input:** `nums = [0,0,0]`, `target = 1`

**Output:** `0`

**Explanation:** The only possible sum is 0.

### Example 3

**Input:** `nums = [-2,0,2,4]`, `target = 1`

**Output:** `0`

**Explanation:** Sums 0 and 2 are both one away, so the smaller sum 0 is returned.

## Constraints

- `3 <= nums.length <= 1000.`
- `-10^4 <= nums[i], target <= 10^4.`
- `The answer fits in a signed 32-bit integer.`

## Solutions

### Brute Force

#### Derivation

The most literal reading of the problem tries every legal choice: pick three distinct indices, add their values, and keep the sum that beats the best one seen so far. There are `n choose 3` index triples, which the given constraints allow us to enumerate outright. The tie rule (two sums equally close: return the smaller) folds directly into the update condition, so a candidate replaces the best sum only when it is strictly closer to `target`, or exactly as close and smaller:

1. Initialize `closest_sum` to the sum of the first three elements.
2. Loop `first` over `0 .. len(nums) - 3`, `second` over `first + 1 .. len(nums) - 2`, and `third` over `second + 1 .. len(nums) - 1`, so every index triple is visited exactly once with `first < second < third`.
3. Compute `current_sum = nums[first] + nums[second] + nums[third]`.
4. Replace `closest_sum` when `current_sum` is strictly closer to `target`, or equally close and smaller.
5. Return `closest_sum` after the loops.

#### Walkthrough

Let us enumerate Example 1 by hand: `nums = [-1,2,1,-4]`, `target = 1`. Four values admit `4 choose 3 = 4` triples. The scan opens with `closest_sum = nums[0] + nums[1] + nums[2] = -1 + 2 + 1 = 2`, and each row below weighs one triple against it:

```text
(first, second, third)   current_sum        distance |sum - 1|   closest_sum
(0, 1, 2)                -1 + 2 + 1 =  2        1    tie, 2 < 2 is false: keep 2
(0, 1, 3)                -1 + 2 - 4 = -3        4    farther: keep 2
(0, 2, 3)                -1 + 1 - 4 = -4        5    farther: keep 2
(1, 2, 3)                 2 + 1 - 4 = -1        2    farther: keep 2
```

The very first triple already held the best answer and the remaining three only confirm it: the function returns `2`, matching the expected Output. Example 2, `nums = [0,0,0]`, has the single triple `(0, 1, 2)` summing to `0`, and the same loop returns it.

#### Solution

The code is the enumeration from the walkthrough, with the tie-aware condition guarding every update:

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], target: int) -> int:
        closest_sum = nums[0] + nums[1] + nums[2]

        for first in range(len(nums) - 2):
            for second in range(first + 1, len(nums) - 1):
                for third in range(second + 1, len(nums)):
                    current_sum = nums[first] + nums[second] + nums[third]
                    if abs(current_sum - target) < abs(closest_sum - target) or (
                        abs(current_sum - target) == abs(closest_sum - target)
                        and current_sum < closest_sum
                    ):
                        closest_sum = current_sum

        return closest_sum
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

The three nested loops visit every index triple once, `n choose 3 = O(n^3)` combinations, and each is weighed in constant time.

##### Space Complexity: `O(1)`

Only `closest_sum` and the three loop indices are stored.

#### Key Insights

- The tie rule is owned entirely by the update condition: a replacement on an equal distance requires the new sum to be strictly smaller, so the smaller of two equally close sums survives regardless of visit order.
- Initializing `closest_sum` to the first triple lets one comparison guard every candidate, including the one used for initialization.
- Correct but cubic: at the constraint ceiling `n = 1000` this is roughly `1.7 × 10^8` triples, which is slow in practice; the next approach removes an entire factor of `n`.

### Two Pointers

#### Derivation

The brute force re-derives every sum from scratch, blind to order. Sorting first buys structure: once the array is ascending, the best pair to complete a fixed anchor `nums[anchor]` can be found by closing two pointers on the remainder instead of trying every pair. Start `left` just after the anchor and `right` at the end. When `current_sum` falls below `target`, no pair with this `left` and a smaller `right` can do better, so `left` moves right; when it exceeds `target`, no pair with this `right` and a larger `left` can, so `right` moves left. Each pointer step discards a whole family of pairs in one comparison, and the anchor loop repeats the sweep for every anchor. The tie-aware update condition carries over unchanged:

1. Sort `nums` in place.
2. Initialize `closest_sum = nums[0] + nums[1] + nums[2]`.
3. For each `anchor` from `0` to `len(nums) - 3`, set `left = anchor + 1` and `right = len(nums) - 1`.
4. While `left < right`: compute `current_sum = nums[anchor] + nums[left] + nums[right]`, apply the tie-aware update, then move `left` right when `current_sum < target`, move `right` left when `current_sum > target`, and return `target` immediately when `current_sum == target` (no sum can beat distance zero).
5. Return `closest_sum` after the anchor loop.

#### Walkthrough

Sorting Example 1 gives `nums = [-4, -1, 1, 2]` with `target = 1`, and the code initializes `closest_sum = -4 + (-1) + 1 = -4` (distance 5). Each line is one pointer state and the decision it forces:

```text
anchor 0 (-4)  left=1 (-1)  right=3 (2)   current_sum = -3   distance 4 < 5: closest_sum = -3
               -3 < 1: grow the sum, left = 2
               left=2 (1)   right=3 (2)   current_sum = -1   distance 2 < 4: closest_sum = -1
               -1 < 1: left = 3, window empty
anchor 1 (-1)  left=2 (1)   right=3 (2)   current_sum =  2   distance 1 < 2: closest_sum = 2
               2 > 1: shrink the sum, right = 2, window empty
anchor 2       left = right = 3: window starts empty, no pair search
```

The best sum improves three times, `-4` to `-3` to `-1` to `2`, and the function returns `2`, matching the expected Output.

Example 3 exercises the tie rule: sorted, `nums = [-2, 0, 2, 4]` with `target = 1`, and `closest_sum` starts at `-2 + 0 + 2 = 0` (distance 1):

```text
anchor 0 (-2)  left=1 (0)   right=3 (4)   current_sum =  2   distance 1 ties, 2 < 0 is false: keep 0
               2 > 1: right = 2
               left=1 (0)   right=2 (2)   current_sum =  0   distance 1 ties, 0 < 0 is false: keep 0
               0 < 1: left = 2, window empty
anchor 1 (0)   left=2 (2)   right=3 (4)   current_sum =  6   farther: keep 0
               6 > 1: right = 2, window empty
```

Both obtainable sums `0` and `2` sit at distance 1, and the update condition keeps the smaller one: the function returns `0`, matching Example 3's Output.

#### Solution

The code is the sweep from the walkthrough: anchors outside, two pointers inside, one tie-aware update per probe.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], target: int) -> int:
        nums.sort()
        closest_sum = nums[0] + nums[1] + nums[2]

        for anchor in range(len(nums) - 2):
            left, right = anchor + 1, len(nums) - 1
            while left < right:
                current_sum = nums[anchor] + nums[left] + nums[right]
                if abs(current_sum - target) < abs(closest_sum - target) or (
                    abs(current_sum - target) == abs(closest_sum - target)
                    and current_sum < closest_sum
                ):
                    closest_sum = current_sum

                if current_sum < target:
                    left += 1
                elif current_sum > target:
                    right -= 1
                else:
                    return target

        return closest_sum
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Sorting costs `O(n log n)`, and the anchor loop runs one `O(n)` two-pointer sweep per round, so the sweeps dominate at `O(n^2)`.

##### Space Complexity: `O(1)`

The sort runs in place and the search keeps only `anchor`, `left`, `right`, and the two running sums.

#### Key Insights

- Sorting turns the best-pair search for a fixed anchor into a two-pointer sweep: every comparison retires one pointer, so a linear number of comparisons covers all pairs of that anchor.
- The early return on `current_sum == target` is the strongest pruning available: distance zero cannot be beaten, so the entire remaining search is skipped.
- The tie rule survives unchanged because the update condition, not the traversal order, owns it.
- `nums.sort()` reorders the caller's list; the problem asks for a sum, not an index into the original order, so the mutation is safe for this contract.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^3)` - three nested loops over all index triples.
- **Two Pointers**: `O(n^2)` - a linear two-pointer sweep per anchor after an `O(n log n)` sort.

### Space Complexity

- **Brute Force**: `O(1)` - a running sum and three loop indices.
- **Two Pointers**: `O(1)` - an in-place sort plus a constant number of pointers.

### Trade-offs

- **Brute Force** needs no precondition and no reasoning beyond the update condition, but the cubic triple count is prohibitive once `n` approaches its constraint ceiling of `1000`.
- **Two Pointers** removes a factor of `n` by exploiting order, at the cost of sorting first, trusting the pointer-discard argument, and reordering the input.

### When to Use Each

- **Brute Force**: as a correctness oracle on small inputs, or when the array cannot be reordered.
- **Two Pointers**: the default in an interview or OA setting; it scales comfortably across the full constraint range.

### Optimization Notes

- The early exit on an exact hit (`current_sum == target`) is the practical difference on many inputs: any triple summing exactly to `target` ends the search on the spot.
- The update condition evaluates each `abs(...)` twice; caching the two distances in locals trims the constant without touching the logic.
- The same ladder generalizes across the k-sum family: sort, anchor the outer loop, then sweep or recurse on the remainder; the closest-sum variant swaps the equality test for a distance comparison.
