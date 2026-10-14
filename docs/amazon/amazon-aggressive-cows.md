# [Aggressive Cows](https://www.fastprep.io/problems/amazon-aggressive-cows)

**Medium** | **NN minutes** | **Array, Sorting, Binary Search, Greedy**

Given distinct integer stall positions stalls and an integer cows, place exactly cows cows in different stalls.

Return the largest possible value of the minimum distance between every pair of placed cows.

## Examples

### Example 1

**Input:** `stalls = [1,2,4,8,9]`, `cows = 3`

**Output:** `3`

**Explanation:** Placing cows at 1, 4, and 8 gives a minimum distance of 3, which cannot be improved.

### Example 2

**Input:** `stalls = [10,1,2,7,5]`, `cows = 3`

**Output:** `4`

**Explanation:** After sorting, positions 1, 5, and 10 achieve minimum distance 4.

### Example 3

**Input:** `stalls = [0,5]`, `cows = 2`

**Output:** `5`

**Explanation:** Both stalls must be used, so their distance is the answer.

## Constraints

- `2 <= stalls.length <= 10^5.`
- `2 <= cows <= stalls.length.`
- `0 <= stalls[i] <= 10^9.`
- `All stall positions are distinct.`

## Solutions

### Exhaustive Placement Search

#### Derivation

The most literal reading of the objective: a placement is any choice of `cows` distinct stalls, and the best placement is the one whose smallest pairwise distance is largest. Enumerate every placement, measure it, and keep the winner. Sorting the stalls first lets every placement be built in increasing position order, which reduces measuring to one pass: the smallest pairwise distance of a sorted placement is the smallest gap between adjacent chosen stalls, because every non-adjacent pair spans at least one adjacent gap:

1. Sort `stalls` into `sorted_stalls`.
2. `place(start_index, cows_left)` extends `chosen` with each stall from
   `start_index` onward, recursing with `index + 1` and `cows_left - 1`.
3. When `cows_left` reaches 0, the placement is complete: compute `smallest_gap`
   as the minimum of `chosen[position + 1] - chosen[position]` over its adjacent
   pairs, and raise `best_distance` to it when larger.
4. Return `best_distance` after the top-level call `place(0, cows)` finishes.

#### Walkthrough

Example 1 sorts to `sorted_stalls = [1, 2, 4, 8, 9]`, and `cows = 3` gives C(5, 3) = 10 placements. The recursion emits them in lexicographic order; the table shows each placement's adjacent gaps:

```text
chosen       gaps    smallest_gap   best_distance
(1, 2, 4)    1, 2    1              1
(1, 2, 8)    1, 6    1              1
(1, 2, 9)    1, 7    1              1
(1, 4, 8)    3, 4    3              3
(1, 4, 9)    3, 5    3              3
(1, 8, 9)    7, 1    1              3
(2, 4, 8)    2, 4    2              3
(2, 4, 9)    2, 5    2              3
(2, 8, 9)    6, 1    1              3
(4, 8, 9)    4, 1    1              3
```

The maximum `smallest_gap` over the ten placements is 3, achieved by `(1, 4, 8)` and `(1, 4, 9)`, matching the expected Output of Example 1.

#### Solution

The code is the walkthrough's enumeration: a backtracking walk over sorted positions that measures each complete placement once.

```python
from typing import List


class Solution:
    def solve(self, stalls: List[int], cows: int) -> int:
        """Return the largest achievable minimum distance between placed cows.

        Time:  O(C(n, cows) * cows): every placement of cows stalls is built
            once and measured with one pass over its adjacent gaps.
        Space: O(cows) for the recursion stack and the chosen list.
        """
        sorted_stalls = sorted(stalls)
        stall_count = len(sorted_stalls)
        chosen: List[int] = []
        best_distance = 0

        def place(start_index: int, cows_left: int) -> None:
            nonlocal best_distance
            if cows_left == 0:
                smallest_gap = min(
                    chosen[position + 1] - chosen[position]
                    for position in range(cows - 1)
                )
                best_distance = max(best_distance, smallest_gap)
                return
            for index in range(start_index, stall_count):
                chosen.append(sorted_stalls[index])
                place(index + 1, cows_left - 1)
                chosen.pop()

        place(0, cows)
        return best_distance
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C(n, cows) × cows)`

Every placement of `cows` stalls among `n` is built exactly once, and measuring one placement is a linear pass over its `cows - 1` adjacent gaps.

##### Space Complexity: `O(cows)`

The recursion descends one frame per placed cow, and `chosen` holds the current placement.

#### Key Insights

- Sorting first means a placement's minimum pairwise distance is its minimum adjacent gap, so measuring is one linear pass instead of all pairs.
- The search space is the binomial coefficient C(n, cows); at the constraint maximum of `10^5` stalls this count is astronomical, which is exactly the waste the next approach removes.
- The `cows_left == 0` check fires only on complete placements, so partial prefixes are never measured.

### Binary Search on the Answer

#### Derivation

The enumeration re-decides overlapping choices millions of times and never uses the structure the objective has. The structure is a monotone feasibility question. Define `can_place(distance)`: can `cows` cows be positioned so every pair is at least `distance` apart? A greedy scan answers it in one pass: put the first cow at the leftmost stall, then walk right and place each next cow at the first stall at least `distance` beyond the last placement. Placing each cow as early as possible is safe by an exchange argument: moving a placed cow earlier never shrinks the room left for the cows that follow. Feasibility is monotone in the other variable too: if distance `d` is achievable, every smaller distance is achievable by the same placement. So the achievable distances form a prefix of the range `1 .. sorted_stalls[-1] - sorted_stalls[0]`, and binary search over that range finds its boundary, the largest feasible distance:

1. Sort into `sorted_stalls`; the search space starts at `low_distance = 1`
   (the smallest gap between distinct integers) and ends at
   `high_distance = sorted_stalls[-1] - sorted_stalls[0]` (cows at the extremes).
2. `can_place(distance)` scans once: `placed_cows` starts at 1 with
   `last_position = sorted_stalls[0]`, and each stall at least `distance` past
   `last_position` hosts the next cow.
3. While `low_distance <= high_distance`: probe
   `candidate = (low_distance + high_distance) // 2`; a feasible probe records
   `best_distance = candidate` and raises `low_distance`, an infeasible one
   lowers `high_distance`.
4. Return `best_distance`.

#### Walkthrough

Example 1: `sorted_stalls = [1, 2, 4, 8, 9]`, `cows = 3`, search space `1 .. 8`. Each line is one probe and the greedy walk it performs:

```text
candidate 4   place at 1; next stall >= 5 is 8; next stall >= 12: none
              2 cows placed < 3    -> infeasible, high_distance = 3
candidate 2   place at 1; next stall >= 3 is 4; next stall >= 6 is 8
              3 cows placed        -> feasible, best_distance = 2, low_distance = 3
candidate 3   place at 1; next stall >= 4 is 4; next stall >= 7 is 8
              3 cows placed        -> feasible, best_distance = 3, low_distance = 4
low_distance (4) > high_distance (3) -> return best_distance = 3
```

The final probe confirms 3 is achievable (cows at 1, 4, 8) and the first probe proved 4 is not, so the boundary sits exactly at 3, matching the expected Output. Example 2 behaves the same after its sort to `[1, 2, 5, 7, 10]`: the probe `candidate = 4` places cows at 1, 5, 10 and succeeds, while `candidate = 5` strands the third cow (1, 7, then nothing below 12), so the answer is 4.

#### Solution

The code is the probes from the walkthrough: one greedy feasibility scan wrapped in a binary search over the distance range.

```python
from typing import List


class Solution:
    def solve(self, stalls: List[int], cows: int) -> int:
        """Return the largest achievable minimum distance between placed cows.

        Time:  O(n log n) to sort plus O(n log D) for the search, where D is
            the span between the outermost stalls.
        Space: O(n) for the sorted copy of the stall positions.
        """
        sorted_stalls = sorted(stalls)
        stall_count = len(sorted_stalls)

        def can_place(distance: int) -> bool:
            placed_cows = 1
            last_position = sorted_stalls[0]
            for position_index in range(1, stall_count):
                if sorted_stalls[position_index] - last_position >= distance:
                    last_position = sorted_stalls[position_index]
                    placed_cows += 1
            return placed_cows >= cows

        low_distance, high_distance = 1, sorted_stalls[-1] - sorted_stalls[0]
        best_distance = 0

        while low_distance <= high_distance:
            candidate = (low_distance + high_distance) // 2
            if can_place(candidate):
                best_distance = candidate
                low_distance = candidate + 1
            else:
                high_distance = candidate - 1

        return best_distance
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n + n log D)`

Sorting costs `O(n log n)`; the binary search probes `O(log D)` distances, where `D = max(stalls) - min(stalls)`, and each probe scans the `n` stalls once.

##### Space Complexity: `O(n)`

The sorted copy of the stall positions; the greedy scan and the search itself use constant extra space.

#### Key Insights

- Feasibility is monotone in `distance`: one achievable distance makes every smaller one achievable, which is what lets binary search replace the enumeration.
- The greedy check is the heart of the approach: placing every cow at the earliest legal stall is safe because an earlier placement never reduces the options of the cows that follow.
- The answer range needs no knowledge of the actual gaps: any distance outside `1 .. max(stalls) - min(stalls)` is trivially infeasible, so the extremes alone bound the search.
- Sorting is what makes the greedy walk correct: with positions ascending, taking the first stall at least `distance` beyond the last placement never skips a choice a later cow needed.

## Comparison of Solutions

### Time Complexity

- **Exhaustive Placement Search**: `O(C(n, cows) × cows)` - every placement is built once and measured with one adjacent-gap pass.
- **Binary Search on the Answer**: `O(n log n + n log D)` - one sort, then `O(log D)` probes of one linear greedy scan each.

### Space Complexity

- **Exhaustive Placement Search**: `O(cows)` - the recursion stack plus the current placement.
- **Binary Search on the Answer**: `O(n)` - the sorted copy of the stall positions.

### Trade-offs

- **Exhaustive Placement Search**: needs no insight beyond the definition and doubles as a correctness oracle, but the placement count is exponential and useless past a dozen stalls.
- **Binary Search on the Answer**: near-linear after the sort and scales to the constraint maximum, but it relies on the greedy feasibility argument, which must be recognized and trusted.

### When to Use Each

- **Exhaustive Placement Search**: tiny inputs, or as the reference implementation when testing the fast version.
- **Binary Search on the Answer (Recommended)**: any real input; it is the standard pattern for maximize-the-minimum objectives over a sorted array.

### Optimization Notes

- `can_place` can return as soon as `placed_cows` reaches `cows`, shortening the probes that succeed early; the asymptotics do not change.
- The same ladder solves the sibling objectives "minimize the maximum" (allocate minimum pages, capacity to ship packages within D days): flip the feasibility direction and search for the lower boundary.
- Integer stall positions keep the search exact; with real-valued positions the loop would switch to a fixed iteration count, since exact floating-point convergence is not guaranteed.
