# [Sort an Array with Rotate and Flip](https://www.fastprep.io/problems/amazon-sort-array-with-rotate-and-flip)

**Medium** | **NN minutes** | **Array, Math, Simulation**

You are given an array values containing distinct integers. You may apply either of these operations:

Rotate: Move the first element to the end of the array.Flip: Reverse the entire array.Return the minimum number of operations needed to place values in strictly increasing order. You may use the operations in any sequence. If increasing order cannot be reached, return -1.

## Examples

### Example 1

**Input:** `values = [3,4,1,2]`

**Output:** `2`

**Explanation:** Rotate twice: [3,4,1,2] becomes [1,2,3,4]. No single operation produces increasing order.

### Example 2

**Input:** `values = [3,2,1,4]`

**Output:** `2`

**Explanation:** Flip to obtain [4,1,2,3], then rotate once to obtain [1,2,3,4].

### Example 3

**Input:** `values = [1,3,2,4]`

**Output:** `-1`

**Explanation:** Rotations preserve the circular order, and a flip only reverses that order. Neither orientation can match [1,2,3,4], so sorting is impossible.

## Constraints

- `1 <= values.length <= 200000`
- `Every element is a 32-bit signed integer.`
- `All elements are distinct.`

## Solutions

### BFS over Operation Sequences

#### Derivation

The most literal reading of the problem: each operation transforms the current array into exactly one new array, so the search for the minimum operation count is a shortest-path question over arrays. Treat every reachable array as a node and the two operations as edges of weight one, then run [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) from the input until the strictly increasing order appears or the reachable set runs out:

1. Compute `target`, the sorted order of `values`, and seed the queue with the
   input as a tuple.
2. Pop states level by level, counting `operations` per level.
3. A popped state equal to `target` returns the current `operations` count.
4. Otherwise enqueue its two neighbors, `rotated` (`state[1:] + state[:1]`) and
   `flipped` (`tuple(reversed(state))`), skipping states already visited.
5. An exhausted queue proves the sorted order is unreachable: return `-1`.

#### Walkthrough

Example 1, `values = [3,4,1,2]`, with `target = (1,2,3,4)`. Each line is one BFS level; the queue holds tuples:

```text
level 0   queue = [(3, 4, 1, 2)]                              operations = 0
          not the target; neighbors (4,1,2,3) and (2,1,4,3) enqueued
level 1   queue = [(4, 1, 2, 3), (2, 1, 4, 3)]                operations = 1
          (4,1,2,3): rotate (1,2,3,4) new, flip (3,2,1,4) new
          (2,1,4,3): rotate (1,4,3,2) new, flip (3,4,1,2) visited
level 2   queue = [(1, 2, 3, 4), (3, 2, 1, 4), (1, 4, 3, 2)]  operations = 2
          (1,2,3,4) == target -> return 2
```

The sorted order first appears two operations deep, reached by one rotate from `(4, 1, 2, 3)`, which itself is one rotate from the start. That two-rotate path matches the expected Output of `2`.

#### Solution

The code is the level-by-level scan from the walkthrough: one queue, one visited set, one counter.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        target = tuple(sorted(values))
        start = tuple(values)
        queue = deque([start])
        visited = {start}
        operations = 0
        while queue:
            for _ in range(len(queue)):
                state = queue.popleft()
                if state == target:
                    return operations
                rotated = state[1:] + state[:1]
                flipped = tuple(reversed(state))
                for neighbor_state in (rotated, flipped):
                    if neighbor_state not in visited:
                        visited.add(neighbor_state)
                        queue.append(neighbor_state)
            operations += 1
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Rotations and flips generate at most `2n` distinct reachable arrays; each is enqueued once and hashing or comparing an `n`-length tuple costs `O(n)`.

##### Space Complexity: `O(n^2)`

The `visited` set stores up to `2n` tuples of length `n`.

#### Key Insights

- The reachable set is small: rotations and flips generate at most `2n` distinct arrays, so the BFS itself cannot blow up beyond that frontier.
- Level-order traversal returns the minimum count for free, because every operation is an edge of weight one.
- The `-1` case needs no special detection: an exhausted queue is the proof that neither orientation of the circular order matches the sorted order.
- Each state still costs `O(n)` to hash and compare, and the visited set holds `n`-length tuples, which is why this cannot run at `n = 200000`.

### Target Scan with Cost Formulas

#### Derivation

BFS pays `O(n)` per state to discover arrays it could have predicted. Every operation sequence collapses to one of two shapes: two flips cancel, and flip-rotate-flip composes to a single rotation, so a sequence with an even number of flips nets to a pure rotation `rot^offset(values)`, and a sequence with an odd number of flips nets to a reflected rotation `reverse(rot^offset(values))`. Instead of searching, enumerate the at most `2n` candidate end states directly and price the cheapest sequence that produces each. For a rotation by `offset` places the two production paths are `offset` straight rotations, or flip, rotate the complement `(n - offset) mod n` times, flip again; for the reflected rotation they are rotate `offset` then flip (`offset + 1` operations), or flip first then rotate the complement:

1. Build `target = sorted(values)` and `reversed_target = target[::-1]`.
2. For each `offset` in `range(length)`, form `rotated = values[offset:] + values[:offset]`.
3. A `rotated` equal to `target` offers cost `rotation_cost(offset)`; one equal
   to `reversed_target` offers `reflection_cost(offset)`.
4. Keep the smallest offer in `best_cost`; return it, or `-1` when no offset
   matched either orientation.

#### Formula

The price of reaching each candidate from `values`, where `n` is the array length and `offset` ranges over `0` to `n - 1`:

$$ \text{cost}(offset) = \begin{cases} \min(offset,\ ((n - offset) \bmod n) + 2), & \text{target is the forward rotation} \\[4pt] 1 + \min(offset,\ (n - offset) \bmod n), & \text{target is the reflected rotation} \end{cases} $$

```text
rotation_cost(offset)   = min(offset, (n - offset) % n + 2)   forward match
reflection_cost(offset) = 1 + min(offset, (n - offset) % n)   backward match
```

The first line prices the two even-flip paths: straight rotations, or the flip-rotate-flip detour that rotates the complement for two flips plus its rotations. The second line prices the two odd-flip paths: rotate then flip, or flip then rotate. The answer is the minimum over the offsets whose candidate matches.

#### Walkthrough

Example 2, `values = [3,2,1,4]`, with `target = [1,2,3,4]` and `reversed_target = [4,3,2,1]`:

```text
offset 0   rotated [3,2,1,4]   no match
offset 1   rotated [2,1,4,3]   no match
offset 2   rotated [1,4,3,2]   no match
offset 3   rotated [4,3,2,1]   == reversed_target
           reflection_cost(3) = 1 + min(3, (4 - 3) % 4 = 1) = 2
best_cost = 2
```

The sole match is the offset whose rotation reverses into the sorted order. Of its two production paths, flip first then one rotate (cost `1 + 1`) beats rotate three times then flip (cost `4`), so the scan returns `2`, matching the expected Output.

#### Solution

The code is the offset loop from the walkthrough, with the two pricing formulas as nested helpers.

```python
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        length = len(values)
        target = sorted(values)
        reversed_target = target[::-1]
        best_cost = None

        def rotation_cost(offset: int) -> int:
            return min(offset, (length - offset) % length + 2)

        def reflection_cost(offset: int) -> int:
            return 1 + min(offset, (length - offset) % length)

        for offset in range(length):
            rotated = values[offset:] + values[:offset]
            if rotated == target:
                forward_cost = rotation_cost(offset)
                if best_cost is None or forward_cost < best_cost:
                    best_cost = forward_cost
            if rotated == reversed_target:
                backward_cost = reflection_cost(offset)
                if best_cost is None or backward_cost < best_cost:
                    best_cost = backward_cost

        return best_cost if best_cost is not None else -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` offsets builds and compares an `n`-length slice pair.

##### Space Complexity: `O(n)`

The target lists plus one rotated slice at a time; no visited set survives the loop.

#### Key Insights

- Operation sequences collapse by flip parity: an even number of flips is a pure rotation, an odd number is a reflected rotation, so only `2n` end states exist and none of them needs a search to name.
- The flip-rotate-flip detour makes a large rotation cheap: rotating `199999` places of a `200000`-length array costs `3` operations, not `199999`.
- Reflection pricing is symmetric for the same reason: flip first or flip last, whichever direction needs fewer rotations.
- The remaining waste is comparison cost: every offset pays `O(n)` to build and test a slice, which the next solution removes by predicting the only offset that can match.

### Minimum-Anchored Orientation Check

#### Derivation

The target scan compares `n`-length arrays at every offset, but a sorted target admits only one candidate offset per orientation. The forward rotation must start at the smallest value: rotations preserve the circular order, and the sorted order of distinct values begins at its minimum, so `minimum_offset = values.index(min(values))` is the only offset worth a forward check. The reflected target must start at the largest value for the mirror reason, so `maximum_offset` is the only offset worth the backward check. One linear comparison per orientation then decides reachability, and the cost formulas from [Target Scan with Cost Formulas](#target-scan-with-cost-formulas) price each match:

1. Build `target = sorted(values)`; locate `minimum_offset` and `maximum_offset`.
2. Forward check: `values[(minimum_offset + position) % length] == target[position]`
   for every `position`; on success price `min(minimum_offset, (length - minimum_offset) % length + 2)`.
3. Backward check: `values[(maximum_offset + position) % length] == target[length - 1 - position]`
   for every `position`; on success price `1 + min(maximum_offset, (length - maximum_offset) % length)`.
4. Return the smaller price, or `-1` when neither orientation matched.

#### Walkthrough

Example 1, `values = [3,4,1,2]`, with `target = [1,2,3,4]`. The minimum `1` sits at `minimum_offset = 2` and the maximum `4` at `maximum_offset = 1`:

```text
forward from offset 2:   values[2]=1 vs target[0]=1  ok
                         values[3]=2 vs target[1]=2  ok
                         values[0]=3 vs target[2]=3  ok
                         values[1]=4 vs target[3]=4  ok  -> forward match
rotation price = min(2, (4 - 2) % 4 + 2 = 4) = 2

backward from offset 1:  values[1]=4 vs target[3]=4  ok
                         values[2]=1 vs target[2]=3  fail -> no backward match
best_cost = 2
```

The forward orientation survives its single anchored check and prices at `2` straight rotations, because the two-flip detour would cost `4`; the backward orientation dies on its second comparison. That returns `2`, matching the expected Output. Example 2 lives on its backward anchor instead (also priced `2`), and Example 3 fails both anchors, returning `-1`.

#### Solution

The code is the two anchored comparisons from the walkthrough, each priced by its formula inline.

```python
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        length = len(values)
        target = sorted(values)
        minimum_offset = values.index(min(values))
        maximum_offset = values.index(max(values))
        best_cost = None

        if all(values[(minimum_offset + position) % length] == target[position]
               for position in range(length)):
            best_cost = min(minimum_offset, (length - minimum_offset) % length + 2)

        if all(values[(maximum_offset + position) % length] == target[length - 1 - position]
               for position in range(length)):
            backward_cost = 1 + min(maximum_offset, (length - maximum_offset) % length)
            if best_cost is None or backward_cost < best_cost:
                best_cost = backward_cost

        return best_cost if best_cost is not None else -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; locating the extremes and running the two anchored comparisons are linear scans.

##### Space Complexity: `O(n)`

The sorted `target` list; every other value is a scalar.

#### Key Insights

- Distinctness makes the anchor unique: the sorted order begins at the minimum and its reverse at the maximum, so one comparison per orientation replaces the scan over all offsets.
- An already-sorted input resolves instantly: `minimum_offset = 0` prices at `min(0, 2) = 0`.
- The flip-parity collapse is what bounds the candidate set to two; without it, "which sequences of operations are worth pricing" has no short answer.
- The sort exists only for the comparison; a version that checks strict monotonicity around the anchor instead compares against `sorted` and drops to `O(n)` time.

## Comparison of Solutions

### Time Complexity

- **BFS over Operation Sequences**: `O(n^2)` - up to `2n` reachable states, each hashed and compared at `O(n)` cost.
- **Target Scan with Cost Formulas**: `O(n^2)` - one `O(n)` slice build and comparison per offset.
- **Minimum-Anchored Orientation Check**: `O(n log n)` - sorting dominates, with linear anchored checks around it.

### Space Complexity

- **BFS over Operation Sequences**: `O(n^2)` - the visited set holds up to `2n` tuples of length `n`.
- **Target Scan with Cost Formulas**: `O(n)` - the target lists and one rotated slice at a time.
- **Minimum-Anchored Orientation Check**: `O(n)` - the sorted target list.

### Trade-offs

- **BFS over Operation Sequences**: needs no insight about the operation group and doubles as a correctness oracle, but quadratic time and memory put `n = 200000` out of reach.
- **Target Scan with Cost Formulas**: removes the memory blow-up and makes the flip-parity structure explicit, but still pays `O(n)` to test every offset.
- **Minimum-Anchored Orientation Check**: optimal and the shortest code, but its correctness rests on the parity collapse and the uniqueness of the extreme-element anchors, exactly the parts an interviewer will probe.

### When to Use Each

- **Minimum-Anchored Orientation Check (Recommended)**: the interview answer: optimal, short, and the anchored checks read directly from the statement's distinctness guarantee.
- **Target Scan with Cost Formulas**: when explaining the cost model matters more than the last factor of `n`, or as the stepping stone that makes the anchors believable.
- **BFS over Operation Sequences**: for tiny inputs, as a cross-check oracle when testing the closed-form prices, or to explore reachability before committing to the formulas.

### Optimization Notes

- The `(length - offset) % length + 2` arm of the rotation price is load-bearing: dropping it overprices large rotations and misses the true minimum whenever the sorted order sits more than halfway around the circle.
- `values.index(min(values))` makes two linear passes; a single `enumerate` loop can record both extremes at once if the constant factor matters.
- The `-1` return must survive the neither-anchor-matched case; both comparisons failing is exactly the Example 3 situation, where neither orientation of the circular order matches the sorted order.
