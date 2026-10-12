# [Minimum Operations to Sort a Permutation](https://www.fastprep.io/problems/amazon-minimum-operations-to-sort-permutation)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given a permutation arr of size n, containing each integer from 1 to n exactly once.

In one operation, you may do either of the following:

Move the first element of the array to the end, shifting every other element one position to the left.Reverse the entire array.It is guaranteed that the array can be sorted into increasing order using these operations. Return the minimum number of operations needed to sort arr.

## Examples

### Example 1

**Input:** `arr = [3,1,2]`

**Output:** `1`

**Explanation:** Move the first element 3 to the end to get [1,2,3].

### Example 2

**Input:** `arr = [1,5,4,3,2]`

**Output:** `2`

**Explanation:** Move 1 to the end to get [5,4,3,2,1], then reverse the array to get [1,2,3,4,5].

### Example 3

**Input:** `arr = [1,2,3,4]`

**Output:** `0`

**Explanation:** The array is already sorted.

## Constraints

- `1 <= arr.length <= 10^5`
- `1 <= arr[i] <= arr.length`
- `arr is a permutation of integers from 1 to arr.length.`
- `It is guaranteed that arr can be sorted using the given operations.`

## Solutions

### BFS over Operation States

#### Derivation

The most literal reading turns the problem into a search: the two operations are moves on an array, so start from the given `arr`, apply every operation, and stop at the first state that is sorted. [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) explores the states level by level, and the level of the sorted state is exactly the minimum operation count, because every operation has unit cost:

1. Put `arr` in a queue with depth `0`; record it in `visited` so identical
   states are not expanded twice.
2. Pop a state. For each of the two moves, build the next state: the rotation
   `state[1:] + state[:1]` and the reversal `reversed(state)`.
3. Return the depth as soon as a next state is sorted.
4. Otherwise append the unseen next state with `depth + 1`.

#### Walkthrough

Example 1, `arr = [3, 1, 2]`, needs only one level of expansion. Each line is one state the queue produces:

```text
depth 0   [3, 1, 2]        (start)
depth 1   rotate -> [1, 2, 3]   sorted, stop
depth 1   reverse -> [2, 1, 3]  (never reached: the rotation won)
```

The rotation of the start state is already `[1, 2, 3]`, so BFS returns the depth of that state, `1`, matching the expected Output.

#### Solution

The code is the walkthrough's level-by-level expansion with a `visited` set:

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, arr: List[int]) -> int:
        start = tuple(arr)
        target = tuple(sorted(arr))
        if start == target:
            return 0

        visited = {start}
        queue = deque([(start, 0)])
        while queue:
            state, depth = queue.popleft()
            for next_state in (state[1:] + state[:1],
                               tuple(reversed(state))):
                if next_state == target:
                    return depth + 1
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, depth + 1))
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2 × n!)`

The search may touch every permutation, `n!` states, and producing each state costs `O(n)` for the tuple surgery. Fine for toy inputs, hopeless at the constraint `n <= 10^5`.

##### Space Complexity: `O(n^2 × n!)`

The visited set holds every discovered state, and each state is an `O(n)` tuple.

#### Key Insights

- Unit-cost moves plus a search for the shortest move sequence is the signature of BFS on an implicit graph.
- The guarantee promise does the search a huge favor: only states reachable from `arr` are ever expanded, never all `n!` permutations.
- The visited set is what keeps the queue finite; without it the two moves would cycle forever between a state and its reversal.

### Rotation Classification

#### Derivation

The search never asks what it is searching for. The guarantee pins the sorted end state, and both moves are symmetries of a circle, so every reachable state is a rotation of the ascending order `1..n` or a rotation of its reverse `n..1`. The start state is one of those rotations too, which means its whole future is decided by a single reading: where does the cycle start? No search is needed, only classification.

Reading the head unlocks both shapes. When `arr` is the ascending cycle starting at value `first` (reading `first, first + 1, ..., n, 1, ..., first - 1`), the block of `first - 1` small values sits behind the `n`, and sorting moves that block to the back. When `arr` is the reverse cycle starting at `first` (reading `first, first - 1, ..., 1, n, ..., first + 1`), the descending block and the ascending block each offer a one-reversal finish. Counting rotations on each shape gives closed-form answers:

1. Read `first = arr[0]` and check in one pass whether every
   `arr[position] == (position + first - 1) % length + 1` (ascending cycle).
2. Ascending and `first == 1`: already sorted, return `0`.
3. Ascending otherwise: the `length - first + 1` rotation-lefts sort directly;
   or `first - 1` rotation-lefts followed by a reversal sort through the
   reverse cycle. Return `min(length - first + 1, first + 1)`.
4. Reverse cycle: either `first` rotation-lefts then a reversal, or a reversal
   then `length - first` rotation-lefts. Return `min(first, length - first) + 1`.

#### Walkthrough

Example 2, `arr = [1, 5, 4, 3, 2]`: `first = 1`, and the head check fails (`arr[1]` would need to be `2`), so the array is a reverse cycle. The two candidate counts are `min(1, 5 - 1) + 1 = 2`. The winning route is the one the example explanation describes: rotate the lone `1` to the back, then reverse:

```text
start        [1, 5, 4, 3, 2]
rotate-left  [5, 4, 3, 2, 1]
reverse      [1, 2, 3, 4, 5]    2 operations
```

The classification returns `2`, the expected Output. (Example 1, `arr = [3, 1, 2]`, reads as an ascending cycle with `first = 3`: `min(3 - 3 + 1, 3 + 1) = 1`.)

#### Solution

The code is the head check and the two closed forms from the derivation:

```python
from typing import List


class Solution:
    def solve(self, arr: List[int]) -> int:
        length = len(arr)
        first = arr[0]
        ascending_rotation = all(
            arr[position] == (position + first - 1) % length + 1
            for position in range(length))

        if ascending_rotation:
            if first == 1:
                return 0
            return min(length - first + 1, first + 1)

        return min(first, length - first) + 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass verifies the ascending cycle; every other step is arithmetic on `first` and `length`.

##### Space Complexity: `O(1)`

Only `first`, `length`, and the pass flag are stored.

#### Key Insights

- The guarantee is not a convenience, it is the whole algorithm: sortability restricts the input to rotations of two fixed arrays, so classification replaces search.
- The array head is the cycle's starting value, and the starting value determines the operation count on both shapes; no scan past the verification pass is needed.
- Two reversals can beat one: the ascending route `min(length - first + 1, first + 1)` counts the reversal-plus-rotation path that walks the cycle backwards, which a single-reversal analysis misses.
- The descending formula `min(first, length - first) + 1` says it all: reach one of the two reversal distances from either end of the cycle, then pay exactly one reversal.

## Comparison of Solutions

### Time Complexity

- **BFS over Operation States**: `O(n^2 × n!)` - up to every permutation expanded, `O(n)` tuple surgery per move.
- **Rotation Classification**: `O(n)` - one verification pass plus constant-time arithmetic on the head value.

### Space Complexity

- **BFS over Operation States**: `O(n^2 × n!)` - the visited set stores every discovered `O(n)` state.
- **Rotation Classification**: `O(1)` - two integers and a boolean.

### Trade-offs

- **BFS over Operation States**: needs no insight at all and doubles as a brute-force oracle, but it cannot even read an input at the constraint sizes.
- **Rotation Classification**: linear time and constant space, but correctness rests on a group-level argument (rotations and reversals preserve cycle membership) that must be stated, not seen.

### When to Use Each

- **BFS over Operation States**: validating the closed form on small inputs, or when the move set is richer than the standard pair and no structure is visible.
- **Rotation Classification (Recommended)**: the interview answer: the guarantee plus the head value gives the minimum count immediately.

### Optimization Notes

- Verify the ascending cycle with the modular test `(position + first - 1) % length + 1` rather than building a sorted copy; that single change keeps the whole solution in constant space.
- The guarantee removes every error branch: the descending formula never needs its own membership check, because a sortable array that is not an ascending cycle is a reverse cycle by assumption.
- A common pitfall is counting the reversal before the rotations it saves: on the ascending shape the reversal-first route costs `first + 1`, not `first - 1 + 1`, because the reversal walks the cycle backwards one step.
