# [Tallest Billboard](https://www.fastprep.io/problems/amazon-tallest-billboard)

**Hard** | **NN minutes** | **Dynamic Programming, Array, Hash Table**

Partition any subset of rods into two groups with equal sums. Return the greatest possible common sum. A rod may be unused.

## Examples

### Example 1

**Input:** `rods = [1,2,3,6]`

**Output:** `6`

**Explanation:** Use 6 on one side and 1+2+3 on the other.

### Example 2

**Input:** `rods = [1,2]`

**Output:** `0`

**Explanation:** No positive equal-height partition exists.

## Constraints

- `1 <= rods.length <= 20.`
- `1 <= rods[i] <= 1000.`
- `The total length is at most 5000.`

## Deriving the Solution

Every rod plays one of three roles: it supports the left billboard, it supports the right billboard, or it sits unused in the yard. The answer is the largest `S` for which some assignment makes both supporting groups sum to `S`. Tracking the two sums separately drowns the search in duplicates; the only thing the future cares about is the height difference between the supports. The ladder collapses the state onto that one number:

1. **Start literal.** Walk the rods once, sending each to left, right, or unused, and report the largest level ending: correct, and `3^n` paths: see [Brute Force Assignment Enumeration](#brute-force-assignment-enumeration).
2. **Keep one number per partial assignment.** Two partial assignments that landed the same height difference are interchangeable, no matter how differently they got there, so a memo keyed by (rods so far, difference) decides every distinct question once: see [Top-Down Memoization](#top-down-memoization).
3. **Fill the table bottom-up.** The memo is a table over (rods so far, difference) whose every transition stays inside one row, so a single array rolled forward per rod replaces the grid: see [Bottom-Up Difference DP](#bottom-up-difference-dp).
4. **Hand the offsets to the library.** The bottom-up version pays for its speed with an offset array and a sentinel; a `defaultdict` keyed by the difference deletes both: see [Tidied with defaultdict](#tidied-with-defaultdict).

## Solutions

### Brute Force Assignment Enumeration

#### Derivation

The statement's most literal reading: give every rod one of three roles, level the two supporting groups or score nothing, and keep the best level. A recursion over the rods with two running sums asks exactly that:

1. Define `best_from(index, left_sum, right_sum)`: the best final level from the rods at `index` onward, given the supports built so far.
2. Base case: with every rod placed, return `left_sum` when it equals `right_sum`, else `0`.
3. Transition: try all three roles for `rods[index]`: skip it, add it to `left_sum`, add it to `right_sum`; return the best of the three recursive results.
4. Return `best_from(0, 0, 0)`.

#### Walkthrough

Example 1 (`rods = [1,2,3,6]`) has `3^4 = 81` paths. Every path whose two supports end level:

```text
rods [1, 2, 3, 6], paths that end level:

  L 1, R -        left 1, right 0        uneven
  L 1+2, R 3      left 3, right 3        -> level 3
  L 6, R 1+2+3    left 6, right 6        -> level 6   <- best
  L -, R -        left 0, right 0        -> level 0
```

The best level ending is `6`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def tallestBillboard(self, rods: List[int]) -> int:
        def best_from(index: int, left_sum: int, right_sum: int) -> int:
            if index == len(rods):
                return left_sum if left_sum == right_sum else 0
            skip = best_from(index + 1, left_sum, right_sum)
            on_left = best_from(index + 1, left_sum + rods[index], right_sum)
            on_right = best_from(index + 1, left_sum, right_sum + rods[index])
            return max(skip, on_left, on_right)

        return best_from(0, 0, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(3^n)`

Every one of the `n` rods branches three ways, and each call does constant work.

##### Space Complexity: `O(n)`

The recursion walks one path at a time, `n` frames deep.

#### Key Insights

- The enumeration is the definition of the answer, which makes it the oracle every other approach is checked against.
- Most branches are wasted: two partial assignments that built the same supports in a different order recur identically, and that waste is the ladder's next rung.
- Scoring only at the leaves keeps the code honest: a path pays nothing for being unlevel halfway, because rods still to come can rebalance it.

### Top-Down Memoization

#### Derivation

The brute force re-decides the same suffix questions. What does the future actually depend on? Not `left_sum` and `right_sum` separately, only their difference: two partial assignments with the same height difference accept exactly the same completions. Shifting both supports down by the shorter one's height changes nothing about what can still be built, so the recursion can carry the difference alone and return the amount the shorter support can still grow:

1. Define `grow_from(index, difference)`: the largest height the shorter support can gain from the rods at `index` onward, over completions that end level, when the supports currently differ by `difference` and the shorter one is treated as height zero.
2. Base case: `index == len(rods)` returns `0` when `difference == 0`, else negative infinity for an unlevel dead end.
3. Skip `rods[index]`: `grow_from(index + 1, difference)`.
4. Add it to the taller support: `grow_from(index + 1, difference + rods[index])`.
5. Add it to the shorter support: the support gains `min(difference, rods[index])`, and the sides swap when the rod overtook the gap, leaving `min(difference, rods[index]) + grow_from(index + 1, abs(difference - rods[index]))`.
6. Memoize every `(index, difference)` pair and return `grow_from(0, 0)`.

#### Walkthrough

Example 1 (`rods = [1,2,3,6]`), the decisive state. Rods 1 and 2 both went to the taller side, so the supports are `(3, 0)` and the recursion sits at `grow_from(2, 3)`, three roles for rod 3:

```text
grow_from(2, 3)                        supports (3, 0), difference 3

  rod 3 shorter  min(3, 3) + grow_from(3, 0) = 3 + grow_from(3, 0)
    grow_from(3, 0)                    supports (3, 3), difference 0
      rod 6 skip:    grow_from(4, 0) = 0     -> level 3
      rod 6 either:  grow_from(4, 6) dead    (6 alone can never level)
    = 3 + 0 = 3                            -> level 3

  rod 3 taller   grow_from(3, 6)         supports (6, 0), difference 6
    rod 6 shorter: min(6, 6) + grow_from(4, 0) = 6 + 0 = 6
  = 6                                    -> level 6   <- best

  rod 3 skip     grow_from(3, 3)         supports (3, 0), difference 3
    rod 6 shorter: min(3, 6) + grow_from(4, 3) = 3 + dead = dead
  dead                                   (a gap of 3 cannot close with 6 left)
```

`grow_from(2, 3) = max(3, 6, dead) = 6`: rods 1, 2, 3 on one side and rod 6 on the other end level at 6, matching the expected Output.

#### Solution

```python
from typing import Dict, List, Tuple


class Solution:
    def tallestBillboard(self, rods: List[int]) -> int:
        rod_count = len(rods)
        memo: Dict[Tuple[int, int], float] = {}
        unreachable = float("-inf")

        def grow_from(index: int, difference: int) -> float:
            if index == rod_count:
                return 0 if difference == 0 else unreachable
            state = (index, difference)
            if state in memo:
                return memo[state]
            rod = rods[index]
            best = grow_from(index + 1, difference)
            best = max(best, grow_from(index + 1, difference + rod))
            grown = min(difference, rod) + grow_from(index + 1, abs(difference - rod))
            if grown > best:
                best = grown
            memo[state] = best
            return best

        return int(grow_from(0, 0))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * S)`

At most `(n + 1) * (S + 1)` distinct `(index, difference)` states with `S = sum(rods) <= 5000`, each decided in constant time from three successors. States whose difference no completion can close are pruned by the negative-infinity dead end.

##### Space Complexity: `O(n * S)`

The memo holds one entry per visited state, plus `O(n)` recursion depth.

#### Key Insights

- The whole reformulation is one subtraction: track `difference` instead of the two sums, and the exponential state space collapses to a rectangle over `(index, difference)`.
- The shorter side is the right value to carry: it is the only number a level ending can still improve, and `min(difference, rod)` prices exactly what a rod contributes when it lands there.
- `abs(difference - rod)` hides a swap of sides; the difference is unsigned precisely so that the two roles stay symmetric and no sign bookkeeping leaks into the memo.

### Bottom-Up Difference DP

#### Derivation

The memo is a table with one row per rod prefix and one column per difference, and row `index + 1` is computed entirely from row `index`, whose cells no later row reads again. A single array rolled forward per rod reproduces the table: before processing a rod, `best_shorter[d]` holds the tallest shorter support over assignments of the rods so far whose sides differ by exactly `d`, with `-1` marking an unreachable difference. Each reachable cell hands its value to up to three cells of the next row: the same difference (rod unused), a larger difference (rod on the taller side), and the rod-swallowed difference (rod on the shorter side):

1. Allocate `best_shorter[0..total]`, `-1` everywhere but `best_shorter[0] = 0`: with no rods placed, both supports are empty.
2. For each `rod`, copy the row into `updated`, then for every reachable `difference`: write `shorter` into `updated[difference + rod]`, and write `shorter + min(difference, rod)` into `updated[abs(difference - rod)]`.
3. Return `best_shorter[0]` after the last rod: difference zero is a level ending, and its value is the common height.

#### Walkthrough

Example 2 (`rods = [1,2]`), the whole array indexed by difference (`-1` shown as `.`):

```text
difference     0  1  2  3
start          0  .  .  .
rod 1          0  0  .  .
rod 2          0  1  0  0
```

After rod 1: difference 1 holds a lone support at height 0. After rod 2: difference 3 rises from rods 1 and 2 on one side, difference 2 from rod 2 alone, and difference 1 is taken over by the page's first split: rod 2 lands on the shorter side of the difference-1 state, overtakes it, and the new shorter support stands at `0 + min(1, 2) = 1`. `best_shorter[0]` stays `0`: no split of `[1,2]` levels above the empty one, matching the expected Output.

#### Solution

The code is the row update from the derivation: one copied row and two writes per reachable difference.

```python
from typing import List


class Solution:
    def tallestBillboard(self, rods: List[int]) -> int:
        total = sum(rods)
        best_shorter = [-1] * (total + 1)
        best_shorter[0] = 0

        for rod in rods:
            updated = best_shorter[:]
            for difference in range(total - rod + 1):
                shorter = best_shorter[difference]
                if shorter < 0:
                    continue
                if shorter > updated[difference + rod]:
                    updated[difference + rod] = shorter
                split = abs(difference - rod)
                grown = shorter + min(difference, rod)
                if grown > updated[split]:
                    updated[split] = grown
            best_shorter = updated

        return best_shorter[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * S)`

One sweep of at most `total + 1` differences per rod, `n` rods, with `S = sum(rods) <= 5000`.

##### Space Complexity: `O(S)`

Two rows of `total + 1` cells: the rolling `best_shorter` and its `updated` copy.

#### Key Insights

- The copy-then-write pattern is the skip transition: `updated` starts as the previous row, so every state silently survives into the next row without an explicit third write.
- Sweeping `difference` only up to `total - rod` keeps both writes in bounds; the taller-side write is the one that could otherwise run past the array.
- `-1` as the unreachable sentinel does double duty: it prunes unreached differences and can never win a `max` against a real height, since real heights are nonnegative.

### Tidied with defaultdict

#### Derivation

The bottom-up version carries two pieces of bookkeeping that are not the algorithm: the offset-free `total + 1` array sized before the first rod, and the `-1` sentinel distinguishing unreachable from reachable-but-empty. A `defaultdict(int)` keyed by the difference removes both: a missing key simply means the empty-support height `0`, which is the honest value for any difference built by stacking rods on one side only:

1. Start `best_shorter = defaultdict(int)` and seed `best_shorter[0] = 0`: with no rods placed, both supports are empty, and a `defaultdict` materializes a key only when written, so the level state must be explicit.
2. For each `rod`: copy the dict into `updated`, then for every `(difference, shorter)` pair apply the same two writes as the array version.
3. Return `best_shorter[0]`.

#### Walkthrough

Example 2 (`rods = [1,2]`) again; the dict's keys after each rod:

```text
start          {0: 0}
rod 1          {0: 0, 1: 0}
rod 2          {0: 0, 1: 1, 2: 0, 3: 0}
```

The dict grows exactly along the differences some placement can build, difference 1 ending at height 1 once the `{2}` against `{1}` split lands, and `best_shorter[0]` stays `0`, matching the expected Output.

#### Solution

```python
from collections import defaultdict
from typing import List


class Solution:
    def tallestBillboard(self, rods: List[int]) -> int:
        best_shorter = defaultdict(int)
        best_shorter[0] = 0

        for rod in rods:
            updated = best_shorter.copy()
            for difference, shorter in best_shorter.items():
                if shorter > updated[difference + rod]:
                    updated[difference + rod] = shorter
                split = abs(difference - rod)
                grown = shorter + min(difference, rod)
                if grown > updated[split]:
                    updated[split] = grown
            best_shorter = updated

        return best_shorter[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * S)`

The same states as the array sweep; each dict operation adds a hashing constant.

##### Space Complexity: `O(S)`

Two dicts live at once, the rolling `best_shorter` and its `updated` copy, and each holds only reachable differences, never more than `total + 1` keys.

#### Key Insights

- The dict is honest about sparsity: differences no placement can build never appear, where the array version pays for every column from `0` to `total`.
- `defaultdict(int)` makes the sentinel unnecessary: an absent difference already reads as the empty-support height `0`.
- The array remains the recommended form at this problem's tiny bounds: `total <= 5000` makes the dense row cheaper than any hash, and the sweep has no cache misses worth avoiding.

## Comparison of Solutions

### Time Complexity

- **Brute Force Assignment Enumeration**: `O(3^n)` - every path in the ternary tree walked.
- **Top-Down Memoization**: `O(n * S)` - one constant decision per `(index, difference)` state.
- **Bottom-Up Difference DP**: `O(n * S)` - one sweep of the difference axis per rod.
- **Tidied with defaultdict**: `O(n * S)` - the same states with a hashing constant.

### Space Complexity

- **Brute Force Assignment Enumeration**: `O(n)` - one recursion path at a time.
- **Top-Down Memoization**: `O(n * S)` - the memo plus recursion depth.
- **Bottom-Up Difference DP**: `O(S)` - two dense rows over the difference axis.
- **Tidied with defaultdict**: `O(S)` - two sparse dicts over reachable differences.

### Trade-offs

- **Brute Force Assignment Enumeration**: the definition, usable as the oracle; `3^20` paths rule it out at the statement's bound of 20 rods.
- **Top-Down Memoization**: visits only the states a given instance can reach, at the cost of recursion depth and memo code.
- **Bottom-Up Difference DP**: the smallest footprint at the same time bound, with no recursion to blow a stack.
- **Tidied with defaultdict**: the same DP with the offset bookkeeping removed; pays a hashing constant that buys nothing at `S <= 5000`.

### When to Use Each

- **Brute Force Assignment Enumeration**: for tiny `n`, and always as the independent checker for the other three.
- **Top-Down Memoization**: when writing the recursion first is the fastest path to a correct answer, before deciding how to store it.
- **Bottom-Up Difference DP (Recommended)**: the interview default on this statement: `20 * 5001` cells of work, one array of memory.
- **Tidied with defaultdict**: when the difference axis would be huge and sparse on some other statement; here it is a readability variant.

### Optimization Notes

- **Bottom-Up Difference DP** is the recommended choice: `O(n * S)` with `S <= 5000` is at most about a hundred thousand cell updates, microseconds in any language.
- The difference axis caps at `sum(rods)`: a difference larger than the total remaining rod length can never close, which is why the sweep bound `total - rod` is safe rather than optimistic.
- Statement corner: `n = 1` leaves only the empty assignment, so the answer is `0`; the array version returns `best_shorter[0] = 0` without ever finding a second reachable state.
- Every rod length is at least 1, so `min(difference, rod)` in the shorter-side write is well defined and nonnegative; zero-length rods would make that write a no-op source of stale states.
