# [Jump Game](https://leetcode.com/problems/jump-game/)

**Medium** | **25 minutes** | **Array, Dynamic Programming, Greedy**

**Pattern:** [Greedy](../patterns/greedy_core/intuition.md)

**Algorithm:** [Recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm)

**Practice:** [`practice/jump_game/solution.py`](../../practice/jump_game/solution.py)

You are given an integer array `nums` where each element `nums[i]` indicates your maximum jump length at that position.

Return `true` if you can reach the last index starting from index `0`, or `false` otherwise.

## Examples

### Example 1

**Input:** `nums = [1,2,0,1,0]`

**Output:** `true`

**Explanation:** First jump from index 0 to 1, then from index 1 to 3, and lastly from index 3 to 4.

### Example 2

**Input:** `nums = [1,2,1,0,1]`

**Output:** `false`

## Constraints

- `1 <= nums.length <= 1000`
- `0 <= nums[i] <= 1000`

## Deriving the Solution

A jump length of `nums[i]` really means "any length from `1` to `nums[i]`", so the question is reachability over a graph whose edges go from `i` to each of the next `nums[i]` indices. Every solution below answers that reachability question; they differ in how much of the graph each one actually has to look at.

1. **Start literal.** From each index, try every jump length and recurse.
   Jumps only move right, so the search terminates, and it explores every
   route: correct, at exponential cost: see [Brute Force](#brute-force).
2. **Spot the waste.** The only thing any call needs to know about an index is
   whether the last index is reachable from it; different routes re-ask that
   about the same index. Cache one boolean per index: see
   [Top-Down Memoization](#top-down-memoization).
3. **Flip the direction.** Every call only reads indices to its right, so a
   right-to-left table fill answers the same question with no recursion: see
   [Bottom-Up DP](#bottom-up-dp).
4. **Keep one target instead of a table.** An index is good the moment it can
   reach any single good index, and the nearest good one is all that matters.
   Sweeping right to left and dragging a `target` boundary leftward answers
   every index without storing anything: `O(n)` time, `O(1)` space: see
   [Greedy](#greedy).

## Solutions

### Brute Force

#### Derivation

The most literal reading simulates every route: standing at index `i`, try each jump length `1` through `nums[i]`, recurse, and succeed the moment any route lands on the last index. Since jump lengths are non-negative the position never decreases, so the recursion always terminates even though it may branch widely:

1. Define `can_reach(i)` as whether the last index is reachable from `i`.
2. Base case: `i >= len(nums) - 1` is already the goal, return `True`.
3. For each `step` in `1 .. nums[i]`, return `True` as soon as
   `can_reach(i + step)` does.
4. If no step leads to the goal, return `False`; the answer is
   `can_reach(0)`.

The early `return True` prunes successful searches, but a failing input must watch every route die.

#### Walkthrough

Trace the recursion on Example 2: `nums = [1, 2, 1, 0, 1]`, a failing input, so the whole tree dies and the trace shows the exhaustive search the successful case would prune. Each line is a call returning; children print above their parent, and `s1`/`s2` name the jump step taken:

```text
            c0.s1.s1.s1: can_reach(3) -> False    every step dead-ends
        c0.s1.s1: can_reach(2) -> False    every step dead-ends
        c0.s1.s2: can_reach(3) -> False    every step dead-ends
    c0.s1: can_reach(1) -> False    every step dead-ends
c0: can_reach(0) -> False    every step dead-ends
-> False
```

Index `3` holds `0` (a frozen position, no jumps available) and is reached twice, once via `2` and once directly from `1`; both routes ask the same question and both pay in full. `can_reach(0)` returns `False`, matching the expected Output for Example 2. The repeated `can_reach(3)` is the waste the next solution removes.

#### Solution

The code is the walkthrough's step loop around the goal base case.

```python
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        def can_reach(i: int) -> bool:
            if i >= len(nums) - 1:
                return True
            for step in range(1, nums[i] + 1):
                if can_reach(i + step):
                    return True
            return False

        return can_reach(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each index branches into `nums[i]` recursive calls, and on a failing input every branch runs to completion; overlapping suffixes are re-derived once per route, which stacks into exponential growth on adversarial inputs.

##### Space Complexity: `O(n)`

The recursion stack reaches depth `n` along the longest jump chain.

#### Key Insights

- The `i >= len(nums) - 1` base case absorbs "land beyond the array": any jump
  overshooting the last index is a success, which keeps the step loop free of
  bounds checks.
- Jumps move strictly right, so no cycle handling is ever needed; a plain
  visited set, which general graph search would require, is unnecessary here.
- The failure mode is the expensive one: success often returns early, while
  `false` inputs make the search prove that every route dies.

### Top-Down Memoization

#### Derivation

The Brute Force re-asks one question per index, "can the last index be reached from here?", once per route that arrives, and the answer never depends on the route. [Caching](https://en.wikipedia.org/wiki/Memoization) one boolean per index makes every repeat a lookup:

1. Keep `can_reach(i)` verbatim from the Brute Force, base case included.
2. Before computing, check `memo` for `i` and return the stored boolean.
3. Otherwise try the step loop, store the outcome in `memo[i]`, and return it.
4. At most `n` distinct indices exist and each tries up to `nums[i]` steps, so
   the cost drops to `O(n^2)` in the worst case, the sum of all jump widths.

#### Walkthrough

Trace Example 1: `nums = [1, 2, 0, 1, 0]`, a succeeding input, so the first route that works ends the search early:

```text
    can_reach(2) -> False    frozen (nums[i] = 0)
      can_reach(4) -> True    last index reached
    can_reach(3) -> True    s1: True
  can_reach(1) -> True    s1: False;  s2: True
can_reach(0) -> True    s1: True
-> True
```

Index `1`'s first step lands on the frozen `2`, whose `False` is cached; its second step reaches `3`, which hops straight to the last index. The root takes its single step to `1` and the search returns `True`, matching the expected Output for Example 1. On this input no state is visited twice, so no memo hit fires; the caching earns its keep on inputs whose step windows overlap, where each repeat becomes a lookup instead of a subtree.

#### Solution

The Brute Force recursion with the memo check and store wrapped around the step loop.

```python
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        memo = {}

        def can_reach(i: int) -> bool:
            if i >= len(nums) - 1:
                return True
            if i in memo:
                return memo[i]
            answer = False
            for step in range(1, nums[i] + 1):
                if can_reach(i + step):
                    answer = True
                    break
            memo[i] = answer
            return answer

        return can_reach(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` indices computes its body once and tries up to `nums[i]` steps, and the sum of all jump widths is bounded by `n` times the maximum width; every repeat visit is a dictionary hit.

##### Space Complexity: `O(n)`

The memo holds one boolean per index, and the recursion stack reaches depth `n`.

#### Key Insights

- One boolean per index is the entire state: reachability from `i` depends on
  nothing but `i`.
- The `break` on the first successful step matters for constants, not
  correctness: a failed index still pays for its whole step loop exactly once.
- Frozen indices (`nums[i] = 0`) are the natural dead ends; every route
  through one dies, and the memo makes proving that a one-time cost.

### Bottom-Up DP

#### Derivation

The memoized recursion always evaluates indices right to left: every call reads strictly larger indices first. [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) with tabulation produces that same table with a plain loop, filling a `good` array from the last index down to the first:

1. Let `good[i]` record whether the last index is reachable from `i`.
2. Seed `good[n - 1] = True`: the goal is its own answer.
3. Sweep `i` from `n - 2` down to `0`; mark `good[i]` true when any of
   `good[i + 1] .. good[i + nums[i]]` is true.
4. Return `good[0]`.

#### Recurrence

Let `good[i]` record whether the last index is reachable from index `i`:

$$ good[i] = \begin{cases}
\text{true}, & i = n - 1 \\[4pt]
\bigvee\limits_{1 \le s \le nums[i],\ i + s \le n - 1} good[i + s], & i < n - 1
\end{cases} $$

```text
good[n - 1] = true
good[i]     = good[i + 1] or good[i + 2] or ... or good[i + nums[i]]
              (only entries with i + s <= n - 1)
answer      = good[0]
```

The base case names the goal itself; the disjunction is the step loop of the recursion, reading only entries the right-to-left sweep has already finalized. The answer is `good[0]`, the start.

#### Walkthrough

Let us fill the table on Example 2: `nums = [1, 2, 1, 0, 1]`, a failing input, so the disjunction never fires:

```text
seed     good[4] = True    the last index is its own goal
i = 3 (nums[3] = 0)    frozen (nums[i] = 0)   -> good[3] = False
i = 2 (nums[2] = 1)    +1: good[3] = False   -> good[2] = False
i = 1 (nums[1] = 2)    +1: good[2] = False;  +2: good[3] = False   -> good[1] = False
i = 0 (nums[0] = 1)    +1: good[1] = False   -> good[0] = False
-> good[0] = False
```

Every index's step window lands only on `False` entries: the frozen `3` poisons `2` and `1`, and the root dies with them. `good[0] = False` matches the expected Output for Example 2. On a succeeding input the same sweep fires at the first `True` it can reach, exactly where the recursion found its winning step.

#### Solution

The code is the walkthrough's right-to-left sweep over the `good` array.

```python
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        # good[i] = can the last index be reached from i
        good = [False] * n
        good[n - 1] = True
        for i in range(n - 2, -1, -1):
            for step in range(1, nums[i] + 1):
                if i + step <= n - 1 and good[i + step]:
                    good[i] = True
                    break
        return good[0]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The sweep pairs each index with up to `nums[i]` later indices, and the sum of jump widths over all indices is `O(n^2)` in the worst case; each pair is examined once.

##### Space Complexity: `O(n)`

The `good` array stores one boolean per index.

#### Key Insights

- Seeding `good[n - 1] = True` and guarding `i + step <= n - 1` together
  replace the recursion's overshoot base case: overshooting is handled by
  never reading past the array.
- The `break` after the first `True` is what makes succeeding inputs cheap;
  failing inputs always pay the full window.
- A zero-jump index never enters the inner loop, so frozen positions are
  handled without a special case.

### Greedy

#### Derivation

The table answers one boolean per index, but no route ever needs most of them: index `i` is good the moment it can reach *any* good index, and the nearest good index is as good as any other. So instead of recording every good index, track one: `target`, the leftmost index known to be good. Sweeping right to left, each index simply asks whether it can reach `target`; if it can, it becomes the new `target`, because everything to its left only needs to reach it. When the sweep ends, the start is reachable exactly when it became the final `target`:

1. Set `target = n - 1`, the only known-good index.
2. Sweep `i` from `n - 2` down to `0`.
3. If `i + nums[i] >= target`, index `i` reaches the current target, so set
   `target = i`.
4. Return `target == 0`.

This is the [greedy](https://en.wikipedia.org/wiki/Greedy_algorithm) core of the reachability structure: one boundary, dragged left, replaces the whole table.

#### Walkthrough

Trace Example 2: `nums = [1, 2, 1, 0, 1]`, where the boundary never moves:

```text
start    target = 4
i = 3    3 + 0 = 3 < target 4   -> target stays 4
i = 2    2 + 1 = 3 < target 4   -> target stays 4
i = 1    1 + 2 = 3 < target 4   -> target stays 4
i = 0    0 + 1 = 1 < target 4   -> target stays 4
-> target == 0 is False
```

Every index falls one short of the frozen `4`, so `target` never leaves the last index and `target == 0` is `False`, matching the expected Output for Example 2. On Example 1 (`nums = [1, 2, 0, 1, 0]`) the sweep moves the boundary twice: `i = 3` reaches `4` (`target` becomes `3`), then `i = 1` reaches `3` (`target` becomes `1`), then `i = 0` reaches `1`, ending with `target == 0` and `True`.

#### Solution

The code is the walkthrough's backward sweep with the one boundary check.

```python
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        target = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= target:
                target = i
        return target == 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One backward pass with a constant-time comparison per index.

##### Space Complexity: `O(1)`

One integer of state, regardless of input length.

#### Key Insights

- An index only ever needs the *nearest* good index: reaching any good index
  makes this one good, and nearer good indexes are strictly easier to reach,
  so keeping one boundary loses nothing.
- The direction matters: sweeping right to left lets a single comparison
  collapse the table's disjunction, because the target is always the tightest
  possible goal for everything remaining on the left.
- The final `target == 0` is the whole answer: the start is good exactly when
  the sweep adopted it, directly or through a chain of adoptions.

## Comparison of Solutions

The practice harness's `practice/jump_game/reference.py` implements the **Greedy** solution.

### Time Complexity

- **Brute Force**: `O(2^n)` - every route through a failing input is explored in full.
- **Top-Down Memoization**: `O(n^2)` - one body per index, trying up to `nums[i]` steps.
- **Bottom-Up DP**: `O(n^2)` - the same index/step pairs as a table sweep.
- **Greedy**: `O(n)` - one backward pass, one comparison per index.

### Space Complexity

- **Brute Force**: `O(n)` - recursion stack only.
- **Top-Down Memoization**: `O(n)` - memo booleans plus the stack.
- **Bottom-Up DP**: `O(n)` - the `good` array.
- **Greedy**: `O(1)` - one boundary integer.

### Trade-offs

- The Brute Force is the direct transcription of the jump rules and the easiest
  version to trust, but it is the only one here that misses the constraint
  budget, and failing inputs are exactly the ones that hurt it most.
- Both `O(n^2)` versions compute per-index reachability, which variants asking
  "which indices are reachable" get for free; the Greedy computes only the
  start's verdict.
- The Greedy drops all per-index answers and all recursion for one boundary
  and one pass, at the cost of trusting the nearest-good-index argument.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for
  checking the faster versions on tiny inputs.
- **Top-Down Memoization**: when the recursive reachability question is easiest
  to trust and inputs stay modest.
- **Bottom-Up DP**: when every index's reachability is wanted, or as the
  stepping stone that makes the Greedy's boundary visible.
- **Greedy** (recommended): the default; one pass, constant space, and the
  reachability structure read directly off the sweep.

### Optimization Notes

- The Greedy's backward sweep and Jump Game II's forward reach window are the
  two greedy shapes over the same structure: this problem asks "can the start
  reach the end", the sequel asks "how many windows does crossing take".
- Overshooting needs no special case in any solution: the recursion folds it
  into the base case, the table's bound guard ignores it, and the Greedy's
  `>=` accepts it, all for the same reason, that landing past the last index
  is at least as good as landing on it.
- The memoized version's recursion depth reaches `n` on long step-one chains;
  at the constraint cap of 1000 that is far below Python's limit, but the
  Bottom-Up and Greedy forms carry no stack at all.
