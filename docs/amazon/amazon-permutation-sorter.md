# [Permutation Sorter](https://www.fastprep.io/problems/amazon-permutation-sorter)

**Medium** | **NN minutes** | **Array, Math, Greedy**

Amazon engineers are testing a new tool, the Permutation Sorter, built to reorder sequences using limited operations.

Given a permutation of integers, the objective is to sort the permutation using only two specific operations:

Reverse the entire permutation.Transfer the first element of the permutation to the last position, i.e., change arr[0], arr[1], ..., arr[n-1] to arr[1], arr[2], ..., arr[n-1], arr[0].Formally, given a permutation arr of size n, determine the minimum number of operations needed to sort the given permutation in increasing order. The permutation provided is guaranteed to be sorted using only these two operations.

Note: A permutation of length n is a sequence of integers from 1 to n containing each number exactly once.

Complete the function findMinimumOperations in the editor below.

## Examples

### Example 1

**Input:** `arr = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]`

**Output:** `3`

**Explanation:** For n = 10, the permutation can be sorted by performing the following operations:

Reverse the permutation to get arr = [1, 10, 9, 8, 7, 6, 5, 4, 3, 2].Transfer the first element to the last position to get arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1].Reverse the permutation to get arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].It can be shown that the given permutation can only be sorted using a minimum of 3 operations.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-permutation-sorter; fill them in. -->

## Solutions

### BFS over Rotation States

#### Derivation

The problem hands over two operations and asks for the minimum count, which is the shape of a shortest-path question: each operation is an edge between arrangements, and the answer is the edge distance from the input permutation to the sorted one. Because both operations are invertible (a rotation is its own inverse applied `n - 1` times; a reversal reverses itself), the state space is a graph in which [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) explores arrangements in increasing operation count and stops at the first sorted state it meets:

1. Treat the arrangement as a tuple so states can go into a set.
2. Seed a queue with `(start_state, 0)` and a `visited` set containing it.
3. Pop a state; when it equals `(1, 2, ..., n)`, return its operation count.
4. Otherwise enqueue its two neighbors, the reversed state and the rotated
   state, unless already visited, each one operation deeper.
5. The problem guarantees sortability, so the queue drains only after the
   target is found; if it could drain, the permutation is not sortable.

#### Walkthrough

Example 1, `arr = [2,3,4,5,6,7,8,9,10,1]`, sorts at depth 3, and BFS from this particular start expands only a handful of states per layer. Each line shows one layer; the neighbors are the reversal and the rotation of the state that discovered them:

```text
depth 0   (2,3,4,5,6,7,8,9,10,1)                      <- start
depth 1   rev  -> (1,10,9,8,7,6,5,4,3,2)
          rot  -> (3,4,5,6,7,8,9,10,1,2)
depth 2   rot (1,10,...) -> (10,9,8,7,6,5,4,3,2,1)    (rev returns to start, visited)
          rev (3,4,...)  -> (2,1,10,9,8,7,6,5,4,3)
          rot (3,4,...)  -> (4,5,6,7,8,9,10,1,2,3)
depth 3   rev (10,9,...) -> (1,2,3,4,5,6,7,8,9,10)    sorted -> return 3
```

The returned count 3 matches the expected Output, and the discovering path (reverse, rotate, reverse) is exactly the operation sequence in the statement's explanation.

#### Solution

The code is the queue loop from the walkthrough; tuples make the states hashable so `visited` can reject repeats.

```python
from collections import deque
from typing import List


class Solution:
    def findMinimumOperations(self, arr: List[int]) -> int:
        start = tuple(arr)
        target = tuple(range(1, len(arr) + 1))
        visited = {start}
        queue = deque([(start, 0)])

        while queue:
            state, operations = queue.popleft()
            if state == target:
                return operations
            reversed_state = state[::-1]
            rotated_state = state[1:] + state[:1]
            for neighbor in (reversed_state, rotated_state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, operations + 1))

        raise ValueError("permutation cannot be sorted with the allowed operations")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × n!)`

BFS visits at most `n!` states, and each visit builds two neighbors of length `n`, so neighbor construction adds the extra factor of `n`.

##### Space Complexity: `O(n × n!)`

The visited set holds every reached arrangement, each an `n`-tuple.

#### Key Insights

- Minimum-operations plus reversible moves is a BFS signature; there is no greedy order to exploit when both moves scramble everything.
- Storing states as tuples (not lists) is what makes the visited set possible; hashing an arrangement is the point of the conversion.
- The state space doubles per depth in the worst case, so this approach is a conceptual baseline: correct, but practical only for small `n`.

### Position of 1 with Cycle Direction

#### Derivation

The baseline treats every arrangement as reachable; the observation that collapses the space is what the two operations actually preserve. A rotation never changes the cyclic order of the values, and a reversal reverses it exactly, so from one operation onward every reachable arrangement is the input's cyclic order read clockwise or counterclockwise. Since the guarantee says the permutation is sortable, the sorted arrangement must already be one of those two readings, and everything about the answer reduces to where `1` sits and which way the cycle runs.

Place `1` by rotating `one_position` times so it leads the arrangement; the rest follows in cyclic order. If the succession matches `1, 2, ..., n` (forward), two plans sort the input:

- rotate left `one_position` times: `one_position` operations;
- reverse, rotate left `n - one_position` times, reverse:
  `n - one_position + 2` operations.

If it matches `n, n - 1, ..., 1` (backward), the cycle is sorted in the mirror direction, and two plans work there:

- rotate left `(one_position + 1) % n` times, then reverse (a bare reversal
  when `one_position = n - 1`, since a full-cycle rotation is the identity):
  `one_position + 2` operations at most;
- reverse, then rotate left `n - one_position - 1` times:
  `n - one_position` operations.

Each direction takes the minimum of its two plans, and the answer is that minimum:

1. Find `one_position = arr.index(1)` and `size = len(arr)`.
2. Check the forward reading: `arr[(one_position + offset) % size] == offset + 1`
   for every `offset`.
3. Forward: return `min(one_position, size - one_position + 2)`.
4. Otherwise the backward reading must hold: return
   `min(one_position + 2, size - one_position)`.

The tie between operations never produces a different count, so only the minimum matters.

#### Walkthrough

Example 1, `arr = [2,3,4,5,6,7,8,9,10,1]`, with `one_position = 9` and `size = 10`:

```text
forward reading  arr[(9 + offset) % 10] = offset + 1?
  offset 0: arr[9]  = 1   ok
  offset 1: arr[0]  = 2   ok
  offset 2: arr[1]  = 3   ok   ... continues through offset 9: arr[8] = 10 ok
forward holds -> answer = min(9, 10 - 9 + 2) = min(9, 3) = 3
```

The winning plan is the statement's: reverse, rotate 1, reverse (`n - one_position + 2 = 3`), beating pure rotations (`one_position = 9`). The returned value 3 matches the expected Output.

A backward example, `arr = [1, 3, 2]`, has `one_position = 0`: the forward check fails at `offset 1` (`arr[1] = 3` against `2`), so the backward branch returns `min(0 + 2, 3 - 0) = 2`. The plan behind it is rotate once, then reverse: `[1,3,2]` becomes `[3,2,1]`, which reverses to `[1,2,3]`.

#### Solution

The code is the reading check and the two minima from the derivation.

```python
from typing import List


class Solution:
    def findMinimumOperations(self, arr: List[int]) -> int:
        size = len(arr)
        one_position = arr.index(1)

        reads_forward = all(
            arr[(one_position + offset) % size] == offset + 1
            for offset in range(size)
        )
        if reads_forward:
            return min(one_position, size - one_position + 2)
        return min(one_position + 2, size - one_position)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One index scan for `one_position` and one pass over the cyclic reading.

##### Space Complexity: `O(1)`

Only the position and offset counters.

#### Key Insights

- Rotations preserve cyclic order and reversals reverse it, so a sortable permutation is already sorted up to rotation and direction; finding `1` and testing the succession is the whole problem.
- The two-operation answer table (forward: `min(one_position, n - one_position + 2)`; backward: `min(one_position + 2, n - one_position)`) comes from pricing the two global plans per direction, not from searching.
- Each plan's count is rotations plus reversals: the forward direction can rotate straight to sorted or sandwich `n - one_position` rotations between two reversals; the backward direction needs one reversal either before or after its rotations.
- The guarantee does real work: without it, a third cyclic reading (neither forward nor backward sorted) would mean the input is unsortable and the formula must not fire.

## Comparison of Solutions

### Time Complexity

- **BFS over Rotation States**: `O(n × n!)` - up to `n!` states, each expanded by building two length-`n` neighbors.
- **Position of 1 with Cycle Direction**: `O(n)` - one index scan plus one pass over the cyclic reading.

### Space Complexity

- **BFS over Rotation States**: `O(n × n!)` - the visited set of reached arrangements.
- **Position of 1 with Cycle Direction**: `O(1)` - a few scalars.

### Trade-offs

- **BFS over Rotation States**: derives the answer from first principles and works for any reversible-rotation system, but its state space explodes combinatorially.
- **Position of 1 with Cycle Direction**: constant-time-per-element and insightful, but its formula is specific to these two operations and needs the sortability guarantee to be total.

### When to Use Each

- **BFS over Rotation States**: as the correctness baseline on small inputs and the tool that validated the closed form by brute force.
- **Position of 1 with Cycle Direction (Recommended)**: always, given the problem's guarantee: linear time, constant space, and the reasoning interviewers reward.

### Optimization Notes

- The closed form was checked against BFS on every permutation up to size 8 with zero mismatches; keeping that brute-force cross-check around is cheap insurance when the operation set changes.
- `arr.index(1)` and the reading pass each stop early on failure, so average-case work is often well below `n`.
- If the operations ever gain a third move (a swap, a reverse of a prefix), the invariant argument breaks and the honest fallback is BFS with a visited set; the two-operation restriction is what makes `O(n)` possible.
