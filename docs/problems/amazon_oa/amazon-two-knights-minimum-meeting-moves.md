# [Minimum Moves for Two Knights to Meet](https://www.fastprep.io/problems/amazon-two-knights-minimum-meeting-moves)

**Medium** | **NN minutes** | **Math, Breadth First Search**

Two knights start at coordinates first = [x1, y1] and second = [x2, y2] on an infinite chessboard. They take turns, with the first knight moving first. On a turn, the chosen knight must make one standard knight move: two squares along one axis and one square along the other.

Return the minimum total number of moves until the two knights occupy the same coordinate. If they already share a coordinate, return 0.

## Examples

### Example 1

**Input:** `first = [0,0]`, `second = [1,2]`

**Output:** `1`

**Explanation:** The first knight can reach the second knight in one move.

### Example 2

**Input:** `first = [0,0]`, `second = [1,0]`

**Output:** `3`

**Explanation:** The adjacent displacement is the exceptional three-move case.

### Example 3

**Input:** `first = [7,-4]`, `second = [7,-4]`

**Output:** `0`

**Explanation:** The knights already meet.

## Constraints

- `first.length == second.length == 2`
- `-10^9 <= first[i], second[i] <= 10^9`

## Solutions

### Relative-Gap BFS

#### Derivation

The literal reading of the problem is a simulation: apply one knight move per turn, alternating movers, and stop when the two knights first share a square. Tracking both positions is unnecessary. Because both knights move over the same infinite board, only the gap between them matters: define the gap as `(second[0] - first[0], second[1] - first[1])`. A move by the first knight shifts its own position and changes the gap by the negative of the move vector; a move by the second knight changes the gap by the move vector itself. The knights meet exactly when the gap reaches `(0, 0)`, so the simulation becomes a shortest-path search over gap vectors, and [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) over turns finds the first turn that produces the zero gap:

1. Reduce the input to the seed gap `(start_gap_x, start_gap_y) = (second[0] - first[0], second[1] - first[1])` and return `0` immediately when it is already `(0, 0)`.
2. Define the search window: the two starts' bounding box grown by `margin = 4` on every side, giving the bounds `min_x`, `max_x`, `min_y`, `max_y`.
3. Seed `seen` and `queue` with the start gap at `turns = 0`, then loop: pop `(gap_x, gap_y, turns)`. The mover is the first knight on even `turns` and the second knight on odd `turns`, encoded as `mover_shift = -1` on even turns and `+1` on odd turns.
4. For each of the eight `(move_x, move_y)` knight moves, form the candidate gap `(next_x, next_y)`. A candidate equal to `(0, 0)` ends the search with `turns + 1`; otherwise enqueue it when it lies inside the window and the gap `(next_x, next_y)` is unseen.
5. `seen` keys on the gap alone, and that key is safe because a gap fixes its
   own depth parity: every knight move vector has an odd coordinate sum, so
   each move flips the parity of `gap_x + gap_y`, meaning the same gap can
   never be reached at depths of different parity. The first BFS visit to a
   gap is therefore at the minimal depth for its mover schedule, which is all
   optimality requires.

One safety question remains: why is the window big enough? A shortest meeting plan keeps every knight on the squares of a single shortest knight path, and such a path never needs to leave the starts' bounding box by more than 2 (the same room a single-knight BFS is given by the standard offset trick). The gap of two squares inside that grown box stays inside the box grown by 4, so `margin = 4` contains a shortest plan, which is all BFS needs to answer optimally.

#### Walkthrough

Example 2 is the case worth watching: `first = [0,0]`, `second = [1,0]`, seed gap `(1, 0)`. The window spans `[-4, 5] × [-4, 4]`. Turn 1 expands the eight moves of the first knight; turn 2 expands the eight moves of the second knight from each; the branch below is the one that first generates the zero gap, at turn 3:

```text
seed      gap = (1, 0)   parity even: knight 1 moves first
turn 1    knight 1 plays (1, 2):  gap = (1, 0) - (1, 2) = (0, -2)
turn 2    knight 2 plays (2, 1):  gap = (0, -2) + (2, 1) = (2, -1)
turn 3    knight 1 plays (2, -1): gap = (2, -1) - (2, -1) = (0, 0)
          zero gap detected on generation, return turns + 1 = 3
```

In square terms that branch is: the first knight moves `(0,0) → (1,2)`, the second knight moves `(1,0) → (3,1)`, and the first knight moves `(1,2) → (3,1)`, joining the second knight on its square. No two-turn plan exists because the knight-neighborhoods of `(0,0)` and `(1,0)` do not intersect, so `3` is the returned minimum, matching the expected Output. (Example 1 returns `1` on the first expansion, and Example 3 returns `0` at the seed.)

#### Solution

The code is the gap loop from the walkthrough: alternate the mover by turn parity, test the zero gap on generation, prune by the window and the gap-keyed `seen` set.

```python
from collections import deque
from typing import List


class Solution:
    def solve(self, first: List[int], second: List[int]) -> int:
        start_gap_x = second[0] - first[0]
        start_gap_y = second[1] - first[1]
        if start_gap_x == 0 and start_gap_y == 0:
            return 0

        margin = 4
        min_x = min(first[0], second[0]) - margin
        max_x = max(first[0], second[0]) + margin
        min_y = min(first[1], second[1]) - margin
        max_y = max(first[1], second[1]) + margin

        knight_moves = [(1, 2), (2, 1), (2, -1), (1, -2),
                        (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

        seen = {(start_gap_x, start_gap_y)}
        queue = deque([(start_gap_x, start_gap_y, 0)])
        while queue:
            gap_x, gap_y, turns = queue.popleft()
            mover_shift = -1 if turns % 2 == 0 else 1
            for move_x, move_y in knight_moves:
                next_x = gap_x + mover_shift * move_x
                next_y = gap_y + mover_shift * move_y
                if next_x == 0 and next_y == 0:
                    return turns + 1
                if (min_x <= next_x <= max_x and min_y <= next_y <= max_y
                        and (next_x, next_y) not in seen):
                    seen.add((next_x, next_y))
                    queue.append((next_x, next_y, turns + 1))
        return -1  # unreachable: the knights always meet on an infinite board
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((|Δx| + c) × (|Δy| + c))`

Where `Δx`, `Δy` are the coordinate differences between the knights and `c` is the constant window growth (twice `margin`, here `8`): the gap states form a grid of that size, each expanded once with eight transitions.

##### Space Complexity: `O((|Δx| + c) × (|Δy| + c))`

The `seen` set holds one entry per discovered gap state, plus the queue.

#### Key Insights

- Tracking the gap vector instead of both positions halves the state and turns "two moving pieces" into an ordinary shortest-path search that ends at the origin.
- Every knight move has an odd coordinate sum, so each move flips the parity of `gap_x + gap_y`: a gap determines its own depth parity, and `seen` can key on the gap alone with no state lost.
- Meeting is detected when a successor equals `(0, 0)`, which also covers the first knight landing directly on the second knight's current square.
- The approach is correct but dies at the stated constraints: coordinates up to `10^9` would need around `10^18` gap states, which motivates the closed-form solution below.

### Closed-Form Knight Distance

#### Derivation

The simulation can be replaced by arithmetic once two facts about the knight metric pin the answer. Write `d(P, Q)` for the single-knight knight distance between squares `P` and `Q`, and `d1 = d(first, second)` for the starts.

**Lower bound: no plan beats `d1` total moves.** The knight distance is a shortest-path metric, so it obeys the triangle inequality. When the first knight moves `P → P'`, the new separation satisfies `d(P, Q) ≤ d(P, P') + d(P', Q) = 1 + d(P', Q)`, hence `d(P', Q) ≥ d(P, Q) - 1`, and symmetrically `d(P', Q) ≤ 1 + d(P, Q)`. One move, by either knight, changes the separation by at most `1` in either direction. The separation starts at `d1` and must reach `0`, so the total number of moves is at least `d1`.

**Upper bound: `d1` moves suffice.** Fix one shortest knight path `v_0, v_1, …, v_{d1}` from `first` to `second`. Send the first knight along it forward (`v_0 → v_1 → …`) and the second knight along it backward (`v_{d1} → v_{d1-1} → …`). The first knight needs `⌈d1 / 2⌉` moves and the second needs `⌊d1 / 2⌋`, and those counts interleave exactly with the alternating turns. When `d1` is even, both reach the midpoint `v_{d1/2}` and the second knight lands on turn `d1`; when `d1` is odd, the second knight arrives at `v_{(d1+1)/2}` on turn `d1 - 1` and waits one turn for the first knight, which lands there on turn `d1`. The two knights can never coincide earlier on this schedule, since that would splice a shorter path out of the shortest one, and the lower bound forbids earlier anyway.

Total moves equal `d1` exactly, and the problem reduces to computing one knight distance in constant time. Three observations bound that distance for a displacement whose axis-aligned magnitudes are `large = max(|Δx|, |Δy|)` and `small = min(|Δx|, |Δy|)`:

1. Every knight move advances at most `2` along any single axis, so at least `⌈large / 2⌉ = (large + 1) // 2` moves are needed.
2. Every move reduces the Manhattan distance to the target by at most `3`, so at least `⌈(large + small) / 3⌉ = (large + small + 2) // 3` moves are needed.
3. Every move changes `x + y` by an odd amount (`±3` or `±1`), so the move count and `large + small` agree modulo `2`; an estimate of the wrong parity is bumped by `1`.

Two exceptional displacements evade these bounds and are special-cased: `(1, 0)` genuinely needs `3` moves (a knight cannot land on an adjacent square in one move, and two moves cannot do it either), and `(2, 2)` needs `4` (the two lower bounds only force `2`). Exhaustive comparison against bounded-board BFS confirms these are the only exceptions.

#### Closed Form

With `large = max(|Δx|, |Δy|)`, `small = min(|Δx|, |Δy|)`, the meeting total is the single-knight distance

$$ d(\Delta x, \Delta y) = \begin{cases}
3, & (\text{large}, \text{small}) = (1, 0) \\[4pt]
4, & (\text{large}, \text{small}) = (2, 2) \\[4pt]
\max\!\left(\left\lceil \tfrac{\text{large}}{2} \right\rceil, \left\lceil \tfrac{\text{large} + \text{small}}{3} \right\rceil\right) + p, & \text{otherwise}
\end{cases} $$

where `p` is `1` when the maximized estimate disagrees with `(large + small) % 2` and `0` otherwise.

```text
large = max(|dx|, |dy|), small = min(|dx|, |dy|)
d = 3    if (large, small) == (1, 0)
d = 4    if (large, small) == (2, 2)
otherwise:
  estimate = max((large + 1) // 2, (large + small + 2) // 3)
  d = estimate     if estimate % 2 == (large + small) % 2
  d = estimate + 1 otherwise
```

Read back: the first bound counts axis coverage, the second counts total travel budget, the parity bump keeps the count reachable given each move flips the parity of `x + y`, and the two special cases patch the small displacements where the bounds undershoot. The integer forms `(large + 1) // 2` and `(large + small + 2) // 3` are exactly the ceilings used in the code.

#### Walkthrough

The three official examples, run through the closed form:

```text
Example 1: first = [0,0], second = [1,2]
  large = 2, small = 1
  estimate = max((2 + 1) // 2, (2 + 1 + 2) // 3) = max(1, 1) = 1
  parity: 1 % 2 == 1 and (2 + 1) % 2 == 1 -> agree, p = 0
  d = 1                                     matches Output 1

Example 2: first = [0,0], second = [1,0]
  (large, small) = (1, 0) -> the adjacent exception
  d = 3                                     matches Output 3

Example 3: first = [7,-4], second = [7,-4]
  large = 0, small = 0
  estimate = max(0 // 2, (0 + 2) // 3) = max(0, 0) = 0
  parity: 0 % 2 == 0 and 0 % 2 == 0 -> agree, p = 0
  d = 0                                     matches Output 0
```

Example 1 is also the one case where the path-walk construction is visible in a single move: the first knight walks the one-edge shortest path `(0,0) → (1,2)` on turn 1 and the meeting is already complete.

#### Solution

The code is the closed form from the walkthrough: order the magnitudes, patch the two exceptions, then apply the bounds and the parity bump.

```python
from typing import List


class Solution:
    def solve(self, first: List[int], second: List[int]) -> int:
        span_x = abs(first[0] - second[0])
        span_y = abs(first[1] - second[1])
        large, small = max(span_x, span_y), min(span_x, span_y)

        if large == 1 and small == 0:
            return 3
        if large == 2 and small == 2:
            return 4

        moves = max((large + 1) // 2, (large + small + 2) // 3)
        if moves % 2 != (large + small) % 2:
            moves += 1
        return moves
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

A fixed number of comparisons and integer operations, independent of the coordinate magnitudes.

##### Space Complexity: `O(1)`

A handful of integer locals.

#### Key Insights

- The crux is a metric argument, not a search: because the knight distance is a shortest-path metric, one move changes the inter-knight separation by at most `1`, which makes `d(first, second)` an immediate lower bound on the total.
- The matching construction is to march both knights along one shortest path toward each other; the alternating-turn constraint absorbs `⌈d1 / 2⌉` and `⌊d1 / 2⌋` automatically, with no case analysis needed beyond even versus odd `d1`.
- The closed form rests on three independent lower bounds (axis coverage `⌈large / 2⌉`, travel budget `⌈(large + small) / 3⌉`, parity) plus exactly two exceptions, `(1, 0)` and `(2, 2)`.
- Meeting arithmetic differs from solo travel only in interpretation: the same `d1` that a lone knight would spend is split between two knights by the path walk.

## Comparison of Solutions

### Time Complexity

- **Relative-Gap BFS**: `O((|Δx| + c) × (|Δy| + c))` - one BFS state per gap cell in the window grown by the constant `c`, each expanded with eight transitions.
- **Closed-Form Knight Distance**: `O(1)` - constant-time integer arithmetic on the displacement magnitudes.

### Space Complexity

- **Relative-Gap BFS**: `O((|Δx| + c) × (|Δy| + c))` - the `seen` set of visited gaps plus the queue.
- **Closed-Form Knight Distance**: `O(1)` - a few integer locals.

### Trade-offs

- **Relative-Gap BFS**: models the alternating turns directly and generalizes to variants where the closed form breaks (blocked squares, non-standard boards), but its state space scales with the coordinate spread and is unusable at `10^9`.
- **Closed-Form Knight Distance**: constant time and space at any coordinate magnitude, but it is specific to the free infinite board and leans on the two-exception patch, which must be trusted or re-verified if the move set changes.

### When to Use Each

- **Closed-Form Knight Distance (Recommended)**: the interview answer for the stated constraints: it is the only approach that terminates in constant time for coordinates up to `10^9`.
- **Relative-Gap BFS**: for small coordinates, for validating the closed form during development, or whenever the board gains obstacles that invalidate the closed-form derivation.

### Optimization Notes

- Parity appears in both approaches, rooted in one fact: a knight move has an odd coordinate sum. That flip is why BFS can key `seen` on the gap alone, and it is why the closed form bumps an estimate of the wrong parity by one.
- Deriving the lower bound from the triangle inequality is what turns "the answer looks like the knight distance" into a proof; quoting the closed form without it leaves the turn-order question open.
- When implementing the closed form, compute the ceilings with `(large + 1) // 2` and `(large + small + 2) // 3` rather than float arithmetic, which loses precision near `10^9`.
