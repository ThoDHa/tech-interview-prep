# [Merge Triplets to Form Target Triplet](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/)

**Medium** | **25 minutes** | **Array, Greedy**

**Pattern:** [Greedy Core](../patterns/greedy_core/intuition.md)

**Algorithm:** [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) · [Array data structure](https://en.wikipedia.org/wiki/Array_data_structure)

**Practice:** [`practice/merge_triplets_to_form_target_triplet/solution.py`](../../practice/merge_triplets_to_form_target_triplet/solution.py)

You are given a 2D array of integers `triplets`, where `triplets[i] = [ai, bi, ci]` represents the `ith` **triplet**. You are also given an array of integers `target = [x, y, z]` which is the triplet we want to obtain.

To obtain `target`, you may apply the following operation on `triplets` zero or more times:

Choose two **different** triplets `triplets[i]` and `triplets[j]` and update `triplets[j]` to become `[max(ai, aj), max(bi, bj), max(ci, cj)]`.
    * E.g. if `triplets[i] = [1, 3, 1]` and `triplets[j] = [2, 1, 2]`, `triplets[j]` will be updated to `[max(1, 2), max(3, 1), max(1, 2)] = [2, 3, 2]`.

Return `true` if it is possible to obtain `target` as an **element** of `triplets`, or `false` otherwise.

## Examples

### Example 1

**Input:** `triplets = [[1,2,3],[7,1,1]], target = [7,2,3]`

**Output:** `true`

**Explanation:** Choose the first and second triplets, update the second triplet to be [max(1, 7), max(2, 1), max(3, 1)] = [7, 2, 3].

### Example 2

**Input:** `triplets = [[2,5,6],[1,4,4],[5,7,5]], target = [5,4,6]`

**Output:** `false`

## Constraints

- `1 <= triplets.length <= 1000`
- `1 <= ai, bi, ci, x, y, z <= 100`

## Deriving the Solution

The operation only ever raises components, so the whole process is monotone: once a value appears somewhere it never disappears, and a triplet that has gone past `target` in some component can never come back down. Monotonicity is what makes the question decidable by inspection instead of by search: `target` is reachable exactly when some triplet that never overshoots `target` supplies each of `x`, `y`, `z`, and the solutions below differ only in how much of that check they carry out explicitly.

1. **Start literal.** Apply the operation by simulation: repeatedly merge any
   pair whose destination stays within `target` until a full sweep merges
   nothing, then look for `target` among the triplets. Correct, but the sweeps
   re-merge the same material over and over, and each sweep costs `O(n^2)`
   pair checks: see [Brute Force Merge Simulation](#brute-force-merge-simulation).
2. **Spot the waste.** The simulation tracks where each merged triplet sits,
   yet position is irrelevant: merging is componentwise max, so the only fact
   that matters is the largest value ever assembled in each component, and
   that maximum is just the componentwise max over the triplets that never
   overshoot `target`.
3. **Fold the survivors.** Discard every triplet that overshoots `target` in
   any component, fold the rest into one componentwise maximum, and compare
   the candidate with `target`. One pass, `O(n)`: see
   [Candidate Fold](#candidate-fold).
4. **Keep only the question.** The fold still builds a full candidate vector,
   but the answer needs only three yes/no facts: does some surviving triplet
   attain `x`, attain `y`, attain `z`? Three flags answer that with one scan
   and no second structure: see
   [Greedy Component Flags](#greedy-component-flags).

## Solutions

### Brute Force Merge Simulation

#### Derivation

The most direct reading applies the operation exactly as written and waits to see whether `target` shows up. Left unchecked the simulation never halts: merging is idempotent at best and the loop would keep finding pairs to "merge" forever. The repair is to merge only pairs whose destination stays within `target`, since a destination past `target` in any component can never equal it later, and to stop when a sweep produces no change:

1. Copy the triplets into a mutable `pool`.
2. Sweep every ordered pair `(i, j)` with `i != j`; compute `candidate` as the
   componentwise max of `pool[i]` and `pool[j]`.
3. If `candidate` stays within `target` componentwise and differs from
   `pool[j]`, write it into `pool[j]` and remember that the sweep merged.
4. Repeat whole sweeps until one merges nothing, then return whether `target`
   is an element of `pool`.

The `!=` guard is what makes sweeps finite: every recorded merge strictly raises some component, and under the constraints each component can rise at most 99 times.

#### Walkthrough

Trace the simulation on Example 1: `triplets = [[1,2,3],[7,1,1]]`, `target = [7,2,3]`. The `pool` starts as the input, and the sweep visits the two ordered pairs `(0, 1)` and `(1, 0)`. Each row is one pair check:

| Sweep | `(i, j)` | `candidate` | Within `target`? | `candidate != pool[j]`? | `pool` after |
|-------|----------|-------------|------------------|-------------------------|--------------|
| 1 | `(0, 1)` | `[max(1,7), max(2,1), max(3,1)] = [7,2,3]` | yes | yes (`[7,1,1]`) | `[[1,2,3],[7,2,3]]` |
| 1 | `(1, 0)` | `[max(7,1), max(2,2), max(3,3)] = [7,2,3]` | yes | yes (`[1,2,3]`) | `[[7,2,3],[7,2,3]]` |
| 2 | both | every `candidate` equals its destination | yes | no | unchanged |

Sweep 1 merged twice, so another sweep ran; sweep 2 found every `candidate` identical to its destination, recorded no merge, and stopped the loop. `target = [7,2,3]` is now an element of `pool`, so the function returns `True`, matching the expected Output for Example 1. On Example 2 every one of the six pair checks produces a `candidate` with a middle component of `5` or `7` against a target middle of `4`, so no merge ever lands, the pool never changes, `target` is absent, and the function returns `False`.

#### Solution

The code is the walkthrough's sweep loop: pair checks under a within-target gate, repeated until a sweep merges nothing.

```python
from typing import List


class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        pool = [list(triplet) for triplet in triplets]

        merged = True
        while merged:
            merged = False
            for i in range(len(pool)):
                for j in range(len(pool)):
                    if i == j:
                        continue
                    candidate = [
                        max(pool[i][k], pool[j][k]) for k in range(len(target))
                    ]
                    # A destination past target can never come back down:
                    # merges only raise components, never lower them.
                    within = all(candidate[k] <= target[k] for k in range(len(target)))
                    if within and candidate != pool[j]:
                        pool[j] = candidate
                        merged = True

        return target in pool
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

Each sweep checks all `O(n^2)` ordered pairs with constant work per pair, and in the worst case a sweep lands only one productive merge, so up to `n` sweeps run. The small value range caps the real merge count (each of the three components can rise at most 99 times under the constraints), but the general worst-case shape of the loop is cubic.

##### Space Complexity: `O(n)`

The `pool` holds a mutable copy of all `n` triplets.

#### Key Insights

- Merging only raises components, which both bounds the simulation (every recorded merge strictly grows its destination) and licenses the within-`target` gate: an overshooting destination is dead on arrival.
- The simulation is correct but computes far more than the question asks: it tracks every intermediate arrangement when only the best-assembled value per component matters.
- As an oracle it is invaluable: the fold and flag solutions below can be checked against it on small random inputs.

### Candidate Fold

#### Derivation

The simulation's waste is bookkeeping it does not need: tracking where each merged triplet sits. Componentwise max is associative and commutative, so the final merged value of any component is just the max of the starting values that fed into it, and every triplet that never overshoots `target` is eligible to contribute. That collapses the whole merge schedule into one fold: discard the overshooting triplets, then take the componentwise max of the survivors and compare it with `target`:

1. Build `usable`, the triplets whose every component is `<=` the matching
   target component.
2. Seed `candidate` at `[0, 0, 0]`; every stored value is at least `1`, so the
   seed is always overwritten by the first survivor.
3. Fold: `candidate = [max(candidate[k], triplet[k]) for each component k]`
   per survivor.
4. Return `candidate == target`.

The comparison answers the question because `candidate[k]` equals `target[k]` exactly when some survivor attains `target[k]`, and the invariant below says that is precisely when `target` is obtainable.

#### Walkthrough

Let us fold Example 1: `triplets = [[1,2,3],[7,1,1]]`, `target = [7,2,3]`. Both triplets pass the usability gate, and each row folds one of them into `candidate`:

```text
start          candidate = [0, 0, 0]
t0 = [1,2,3]   all(1<=7, 2<=2, 3<=3) usable   -> candidate = [max(0,1), max(0,2), max(0,3)] = [1, 2, 3]
t1 = [7,1,1]   all(7<=7, 1<=2, 1<=3) usable   -> candidate = [max(1,7), max(2,1), max(3,1)] = [7, 2, 3]
candidate == target  [7,2,3] == [7,2,3]  -> True
```

The fold absorbs each usable triplet's components and ends at exactly `target`, so the function returns `True`, matching the expected Output for Example 1. The gate does real work on Example 2: `[2,5,6]` and `[5,7,5]` both fail it (a middle component of `5` and `7` against `4`), leaving `usable = [[1,4,4]]`, so `candidate` stays `[1,4,4]`, the comparison fails, and the function returns `False` there.

#### Solution

The code is the walkthrough's two passes: a filter, then a componentwise max fold.

```python
from typing import List


class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        usable = [
            triplet
            for triplet in triplets
            if all(triplet[k] <= target[k] for k in range(len(target)))
        ]

        candidate = [0, 0, 0]
        for triplet in usable:
            candidate = [max(candidate[k], triplet[k]) for k in range(len(target))]

        return candidate == target
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass filters the `n` triplets with three comparisons each, and the fold does constant work per survivor.

##### Space Complexity: `O(1)`

`usable` references the existing triplet lists rather than copying them, and `candidate` is a fixed three entries.

#### Key Insights

- Componentwise max being a semilattice operation is the whole reason the merge schedule can be discarded: the fold computes the same fixed point the simulation crawls to.
- The `[0, 0, 0]` seed installs the empty fold safely: it is below every stored value, and an all-discarded input leaves the seed in place, which cannot equal a `target` whose components are all at least `1`.
- This is the flags solution below with redundant information kept: `candidate` records values, but only the equality events with `target` decide the answer.

#### Invariant

Let `usable` be the triplets with every component `<=` the matching target component. The discard step is only legal because of this equivalence:

$$ \text{target obtainable from triplets} \iff \text{target obtainable from usable} $$

```text
target obtainable from the input triplets
  if and only if
target obtainable from the usable triplets only
```

Forward: a winning merge chain never needs a discarded triplet, because merging a triplet with a component over `target` into anything raises that destination over `target`, knocking it out of every chain that ends at `target`; and merging a discarded triplet into the void leaves it overshooting, still unusable. Backward: every merge whose destination stays within `target` uses only usable sources (a usable destination merged from usable sources stays usable), so every chain the full input can run, `usable` can run too. Collapsing `usable` by the fold then gives the decidable form the code tests:

$$ \text{target obtainable} \iff \forall k\ \exists\, t \in \text{usable} : t_k = \text{target}_k $$

```text
target obtainable  if and only if  every component k is attained by some
                                   usable triplet t (t[k] == target[k])
```

### Greedy Component Flags

#### Derivation

The fold builds `candidate`, a full three-component record, when the question asked of it is only "did some survivor attain each target component?". Answers to that question are three booleans, so the record can shrink to three flags, updated the moment a survivor attains a component and never stored again. Nothing about the decision changes; only the remembered state does:

1. Start `good = [False, False, False]`.
2. For each triplet, discard it when any component exceeds the matching target
   component.
3. Among survivors, set `good[k]` whenever the triplet's `k`th component
   equals the `k`th target component.
4. Return `all(good)`.

The discard reuses the invariant proved above, and the equality tests reuse its decidable form; the flags are just those tests recorded instead of re-asked at the end.

#### Walkthrough

Trace the flags on Example 2: `triplets = [[2,5,6],[1,4,4],[5,7,5]]`, `target = [5,4,6]`, the input where both rejections and a partial match occur:

```text
start              good = [False, False, False]
t0 = [2,5,6]       b: 5 > 4 -> discard
t1 = [1,4,4]       usable   a: 1 == 5 no   b: 4 == 4 yes   c: 4 == 6 no
                   good = [False, True, False]
t2 = [5,7,5]       b: 7 > 4 -> discard
all(good)          False, False ... -> return False
```

Only the middle flag ever lights: `[1,4,4]` attains `y = 4`, but no usable triplet attains `x = 5` and `z = 6` simultaneously with it, and the discarded triplets are barred from supplying either. `all(good)` reads `False`, matching the expected Output for Example 2. On Example 1 the same three lines light all the flags: `[1,2,3]` attains `y` and `z`, `[7,1,1]` attains `x`, and `all(good)` reads `True`.

#### Solution

The code is the walkthrough's three states: the gate, the three equality updates, and the final `all`.

```python
from typing import List


class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        good = [False, False, False]
        for a, b, c in triplets:
            # A triplet past target in any component can never join a chain
            # that ends at target: merges only raise components.
            if a > target[0] or b > target[1] or c > target[2]:
                continue
            good[0] = good[0] or a == target[0]
            good[1] = good[1] or b == target[1]
            good[2] = good[2] or c == target[2]
        return all(good)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass with a constant number of comparisons per triplet; nothing is revisited.

##### Space Complexity: `O(1)`

Three booleans, regardless of `n`.

#### Key Insights

- The discard is safe only because merges are monotone; this one greedy fact replaces both the merge schedule and the reachability search.
- `good[k]` is checked and set in the same visit, so a triplet may supply several components at once and a component may be supplied by any of several triplets; both shapes are covered without special cases.
- Keep the brute force simulation in mind as the oracle when testing: the flags solution should agree with it on every input, and disagreements point at a discard bug.

## Comparison of Solutions

The practice harness's `practice/merge_triplets_to_form_target_triplet/reference.py` implements the **Greedy Component Flags** solution.

### Time Complexity

- **Brute Force Merge Simulation**: `O(n^3)` - `O(n^2)` pair checks per sweep, up to `n` productive sweeps.
- **Candidate Fold**: `O(n)` - one filter pass and one constant-work fold per survivor.
- **Greedy Component Flags**: `O(n)` - one pass, a constant number of comparisons per triplet.

### Space Complexity

- **Brute Force Merge Simulation**: `O(n)` - a mutable copy of the triplet list.
- **Candidate Fold**: `O(1)` - a reference list plus a fixed three-entry candidate.
- **Greedy Component Flags**: `O(1)` - three booleans.

### Trade-offs

- The simulation writes out the operation verbatim, which makes it the easiest to trust and the natural testing oracle, but it is the only approach here that misses the constraint budget.
- The fold trades the schedule for one linear pass, at the cost of remembering full component values that the answer never reads.
- The flags shrink the state to the question's exact size; the price is that the discard's correctness rests entirely on the monotonicity argument, which the fold version states and the flags version inherits.

### When to Use Each

- **Brute Force Merge Simulation**: as a correctness oracle for the linear
  versions on small inputs, not as a submitted answer.
- **Candidate Fold**: when a written-down merge fixed point is wanted and the
  fold reads more naturally than three flag updates.
- **Greedy Component Flags** (recommended): the interview answer: one scan, constant space, and a correctness argument of one sentence.

### Optimization Notes

- Both linear solutions are the same greedy: the fold's `candidate[k] == target[k]` events are exactly the flag updates, so disagreement between the two implementations signals a bug, not a judgement call.
- Overshoot checks must be strict-inequality per component against the whole triplet; testing only equality matches (the tempting shortcut) wrongly accepts inputs like `[[5,5,9],[1,1,2]]` against `[5,5,2]`, where the only `z = 2` supplier is barred.
- The value bounds (`<= 100`) are what keep the simulation's merge count finite in practice; on unbounded values the within-target gate still bounds it, but the cubic worst-case shape is the honest headline.
