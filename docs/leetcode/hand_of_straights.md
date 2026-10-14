# [Hand of Straights](https://leetcode.com/problems/hand-of-straights/)

**Medium** | **25 minutes** | **Array, Hash Table, Greedy, Sorting**

**Pattern:** [Greedy](../patterns/greedy_core/intuition.md), [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) · [Sorting](https://en.wikipedia.org/wiki/Sorting_algorithm) · [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure))

**Practice:** [`practice/hand_of_straights/solution.py`](../../practice/hand_of_straights/solution.py)

You are given an integer array `hand` where `hand[i]` is the value written on the `ith` card and an integer `groupSize`.

You want to rearrange the cards into groups so that each group is of size `groupSize`, and card values are consecutively increasing by `1`.

Return `true` if it's possible to rearrange the cards in this way, otherwise, return `false`.

## Examples

### Example 1

**Input:** `hand = [1,2,4,2,3,5,3,4], groupSize = 4`

**Output:** `true`

**Explanation:** The cards can be rearranged as `[1,2,3,4]` and `[2,3,4,5]`.

### Example 2

**Input:** `hand = [1,2,3,3,4,5,6,7], groupSize = 4`

**Output:** `false`

**Explanation:** The closest we can get is `[1,2,3,4]` and `[3,5,6,7]`, but the cards in the second group are not consecutive.

## Constraints

- `1 <= hand.length <= 10000`
- `0 <= hand[i] <= 1000`
- `1 <= groupSize <= hand.length`

## Deriving the Solution

A group is a run of `groupSize` consecutive values, so the question is whether the multiset of cards tiles into such runs. Every solution below builds the tiling one smallest-card-at-a-time; the value of the smallest ungrouped card is never a choice, and once its group is placed the question repeats on what remains.

1. **Start literal.** Repeatedly find the smallest remaining card, remove it
   and one card of each successor value, and repeat. Every group choice is
   forced, so the simulation decides the answer: correct, at `O(n^2)` for the
   repeated scans: see [Brute Force](#brute-force).
2. **Spot the waste.** The scans re-find values and memberships the counts
   already summarize. Sort the distinct values once, count them once, and the
   whole tiling becomes one pass of decrementing runs: see
   [Greedy](#greedy).
3. **Track the frontier with a heap.** The Greedy jumps straight to the next
   open run when a value's count hits zero; a min-heap of pending values
   walks the same frontier explicitly, popping each value as its last copy is
   consumed: see [Min-Heap of Remaining Values](#min-heap-of-remaining-values).

## Solutions

### Brute Force

#### Derivation

The most literal reading plays out the deal by hand: some group must contain the smallest card in the whole hand (its value is the group's low end, since nothing smaller exists to precede it), so remove that card and one card of each successor value, then repeat on what remains. Any missing successor is an immediate `false`, and an empty table is a completed tiling:

1. If `len(hand)` is not a multiple of `groupSize`, return `false`: the groups
   cannot even out.
2. Let `remaining` hold the ungrouped cards.
3. While `remaining` is non-empty: take `smallest = min(remaining)`, remove
   it, then remove one card of each value `smallest + 1` through
   `smallest + groupSize - 1`.
4. If any successor is missing, return `false`; otherwise finish with `true`.

#### Walkthrough

Trace the failing Example 2: `hand = [1, 2, 3, 3, 4, 5, 6, 7]`, `groupSize = 4`:

```text
draw 8: need 9, not in [10, 12] -> return False
```

The first draw succeeds silently: it removes `1, 2, 3, 4` (the run `[1, 2, 3, 4]`, exactly the grouping Example 2's explanation mentions). The second draw takes the smallest survivor `2`, which no longer exists in `remaining`, so the run it needs cannot close and the function returns `false`, matching the expected Output for Example 2. The failure is the whole lesson: the forced run through the first `1` strands the second `3` with no partner below it.

#### Solution

The code is the walkthrough's draw loop around the multiple-of check.

```python
from typing import List


class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0:
            return False
        remaining = list(hand)
        while remaining:
            smallest = min(remaining)
            remaining.remove(smallest)
            for value in range(smallest + 1, smallest + groupSize):
                if value not in remaining:
                    return False
                remaining.remove(value)
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The `while` loop runs `n / groupSize` times, and each round pays `O(n)` for the `min` scan plus an `O(n)` list `remove` per card drawn, of which there are `n` across the whole tiling.

##### Space Complexity: `O(n)`

The `remaining` list copies the hand.

#### Key Insights

- The multiple-of guard is not an optimization: without it, the last round
  would try to draw successors that do not exist and could fail misleadingly
  rather than for the structural reason.
- The smallest card's group is forced, which is why the simulation needs no
  search or backtracking: every choice is the only one available.
- List membership tests and removals are where the quadratic cost lives; both
  are frequency lookups in disguise.

### Greedy

#### Derivation

The Brute Force's `remaining` list is a multiset searched by hand. A [frequency count](https://en.wikipedia.org/wiki/Associative_array) answers every membership question in `O(1)`, and sorting the distinct values once replaces every `min` scan: then a whole *run of groups* can be opened in one step. When the sweep reaches value `card` and finds `count[card] = runs` still ungrouped, every one of those `runs` copies must open a group at `card` (no smaller value can cover them), so the run consumes `runs` cards of each of the next `groupSize - 1` values in a single stroke. Any successor shorter than `runs` is an immediate `false`:

1. If `len(hand) % groupSize != 0`, return `false`.
2. Count the cards into `count`, and sweep the distinct values in sorted
   order.
3. At value `card` with `runs = count[card] > 0`: for each successor value,
   require at least `runs` copies, then decrement each by `runs`. Zero out
   `count[card]`.
4. A shortfall anywhere returns `false`; a completed sweep returns `true`.

#### Walkthrough

Trace Example 1: `hand = [1, 2, 4, 2, 3, 5, 3, 4]`, `groupSize = 4`, whose counts are `{1: 1, 2: 2, 3: 2, 4: 2, 5: 1}`:

```text
count   = {1: 1, 2: 2, 4: 2, 3: 2, 5: 1}
card 1    opens 1 group(s); consume one each of 2..4 (2: 2 >= 1, 3: 2 >= 1, 4: 2 >= 1)    count = {2: 1, 4: 1, 3: 1, 5: 1}
card 2    opens 1 group(s); consume one each of 3..5 (3: 1 >= 1, 4: 1 >= 1, 5: 1 >= 1)    count = {}
-> every opened group covered -> True
```

The single `1` forces one group starting there, which eats one `2`, one `3`, one `4`; the leftover `2` then forces the second group through `3`, `4`, `5`. Every count lands on zero, so the function returns `true`, matching the expected Output for Example 1, with the two groups `[1, 2, 3, 4]` and `[2, 3, 4, 5]`. On Example 2 (`hand = [1, 2, 3, 3, 4, 5, 6, 7]`) the sweep opens the `1`-group, and reaching `card = 3` finds `count[4] = 0 < 1`, the same stranded second `3` the Brute Force died on.

#### Solution

The code is the walkthrough's run-opening sweep over sorted distinct values.

```python
from typing import List


class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0:
            return False
        count = {}
        for card in hand:
            count[card] = count.get(card, 0) + 1
        for card in sorted(count):
            runs = count[card]
            if runs == 0:
                continue
            for value in range(card + 1, card + groupSize):
                if count.get(value, 0) < runs:
                    return False
                count[value] -= runs
            count[card] = 0
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Counting is `O(n)`, sorting the at-most-`n` distinct values is `O(n log n)`, and the sweep touches each distinct value a constant number of times (`groupSize` decrements per opened run, `n / groupSize` runs total, `O(n)` decrement work overall).

##### Space Complexity: `O(n)`

The `count` map holds one entry per distinct value.

#### Key Insights

- Opening groups in runs, not one at a time, is the step that kills the
  simulation: `runs` groups opened at once cost one successor check each, not
  `runs` full group builds.
- The sorted sweep guarantees every card is seen exactly at the moment its
  group must start, which is why no backtracking is ever needed: a deficit is
  a proof of impossibility, not a wrong choice to undo.
- `count.get(value, 0)` folds "value absent from the hand" and "value used
  up" into one `0`, so no sentinel bookkeeping is needed.

### Min-Heap of Remaining Values

#### Derivation

The Greedy jumps its sweep straight over values it has already exhausted. A [min-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) of the not-yet-exhausted values walks the same frontier explicitly: the root is always the smallest live value, and a value is popped at the moment its last copy is consumed. Building each group card by card against the heap keeps the mechanics visible, at the price of one heap operation per distinct exhaustion; [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) is the library's frequency count:

1. Count the hand into a `Counter`; heapify its keys.
2. While the heap is non-empty, let `smallest` be its root and build the group
   `smallest` through `smallest + groupSize - 1`, decrementing each value's
   count.
3. When a value's count hits `0`, it must be the root: pop it. If an
   intermediate value hits `0` before the root does, some exhausted value
   would be buried under live ones, which no later group can repair: return
   `false`.
4. Any missing card, or a value exhausted out of order, returns `false`; an
   emptied heap returns `true`.

#### Walkthrough

Trace Example 1 again, now card by card: `hand = [1, 2, 4, 2, 3, 5, 3, 4]`, `groupSize = 4`:

```text
count   = {1: 1, 2: 2, 4: 2, 3: 2, 5: 1}    heap (root only meaningful) = [1, 2, 3, 4, 5]
root 1: consume [1, 2, 3, 4]    count = {2: 1, 3: 1, 4: 1, 5: 1}
root 2: consume [2, 3, 4, 5]    count = {}
-> heap empty, every group covered -> True
```

The first group exhausts `1` (the root, so it pops cleanly); the second group exhausts `2` at the root, then `3`, `4`, `5`, popping each in turn, and the heap empties. The function returns `true`, matching the expected Output for Example 1. The out-of-order guard exists for inputs like a hand of `{1: 2, 2: 1, 3: 2}` at `groupSize = 3`: the group `1, 2, 3` would exhaust `2` while `1` still lives below it in the heap, and no second group can ever start, which the guard catches at the moment `2` dies out of order.

#### Solution

The counter-and-heap version: build groups from the root, pop values as they die.

```python
import collections
import heapq
from typing import List


class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0:
            return False
        count = collections.Counter(hand)
        heap = list(count)
        heapq.heapify(heap)
        while heap:
            smallest = heap[0]
            for value in range(smallest, smallest + groupSize):
                if count[value] == 0:
                    return False
                count[value] -= 1
                if count[value] == 0:
                    if value != heap[0]:
                        return False
                    heapq.heappop(heap)
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Counting and heapifying the at-most-`n` distinct values cost `O(n)`; the tiling performs `n` decrements plus one root check per distinct exhaustion, each heap operation `O(log n)`.

##### Space Complexity: `O(n)`

The `Counter` and the heap hold one entry per distinct value.

#### Key Insights

- The heap adds nothing the sorted sweep lacks; what it buys is a different
  failure mode to reason about: values die in heap order or the tiling is
  impossible, which makes the impossibility argument local and immediate.
- The out-of-order exhaustion check (`value != heap[0]`) is the heap frame's
  version of the Greedy's shortfall check: both fire the moment a run's
  continuation cannot be supplied.
- Iterating `list(count)` rather than the `Counter` itself matters: the tiling
  mutates counts, and mutating a dict while iterating its keys raises.

## Comparison of Solutions

The practice harness's `practice/hand_of_straights/reference.py` implements the **Greedy** solution.

### Time Complexity

- **Brute Force**: `O(n^2)` - a full list scan and removals per drawn card.
- **Greedy**: `O(n log n)` - one sort of distinct values plus linear decrement work.
- **Min-Heap of Remaining Values**: `O(n log n)` - the same tiling with heap operations replacing the sort's role.

### Space Complexity

- **Brute Force**: `O(n)` - the `remaining` list.
- **Greedy**: `O(n)` - the frequency map.
- **Min-Heap of Remaining Values**: `O(n)` - the `Counter` plus the heap.

### Trade-offs

- The Brute Force is the direct transcription of the dealing rule and the
  easiest version to trust, but per-card list surgery keeps it quadratic.
- The Greedy is the tightest expression of the forced-smallest argument:
  sorted keys, one run-opening stroke per value, no auxiliary frontier to
  maintain.
- The Min-Heap version trades the sort for a heap and per-death pops, which
  costs a little code and buys the local, immediate impossibility check.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for
  checking the faster versions on tiny hands.
- **Greedy** (recommended): the default; the run-opening sweep is the
  shortest correct program and the standard interview answer.
- **Min-Heap of Remaining Values**: when the heap-frontier framing is wanted,
  or as a stepping stone to problems whose frontier cannot be replaced by a
  sort.

### Optimization Notes

- The multiple-of guard is worth keeping in every version: it rejects
  structurally impossible hands before any work, and without it the last
  group's failure mode is a bug away from an infinite loop.
- `groupSize == 1` always succeeds (every card is its own group); all three
  solutions handle it without a special case, but it is a useful first test.
- The run-opening stroke is what separates `O(n log n)` from
  `O(n * groupSize)`: opening one group per smallest card with per-card
  decrements (the common intermediate version) recomputes the same run once
  per duplicate card, while the run version folds duplicates into one pass.
- The same smallest-card-forces-a-group argument drives LC 1296 (the same
  problem with divisibility instead of adjacency); both are the "greedy with
  frequency counts" family, and neither needs backtracking because every
  choice is forced.
