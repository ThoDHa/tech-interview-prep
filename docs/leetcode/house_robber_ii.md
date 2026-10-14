# [House Robber II](https://leetcode.com/problems/house-robber-ii/)

**Medium** | **25 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Recurrence relation](https://en.wikipedia.org/wiki/Recurrence_relation) · [Memoization](https://en.wikipedia.org/wiki/Memoization)

**Practice:** [`practice/house_robber_ii/solution.py`](../../practice/house_robber_ii/solution.py)

You are given an integer array `nums` where `nums[i]` represents the amount of money the `i`th house has. The houses are arranged in a circle, i.e. the first house and the last house are neighbors.

You are planning to rob money from the houses, but you cannot rob **two adjacent houses** because the security system will automatically alert the police if two adjacent houses were *both* broken into.

Return the *maximum* amount of money you can rob **without** alerting the police.

## Examples

### Example 1

**Input:** `nums = [3,4,3]`

**Output:** `4`

**Explanation:** You cannot rob `nums[0] + nums[2] = 6` because `nums[0]` and `nums[2]` are adjacent houses. The maximum you can rob is `nums[1] = 4`.

### Example 2

**Input:** `nums = [2,9,8,3,6]`

**Output:** `15`

**Explanation:** You cannot rob `nums[0] + nums[2] + nums[4] = 16` because `nums[0]` and `nums[4]` are adjacent houses. The maximum you can rob is `nums[1] + nums[4] = 15`.

## Constraints

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 200`

## Deriving the Solution

The straight street of [House Robber](house_robber.md) yields to a one-pass recurrence because each house's consequences reach exactly two houses back. The circle adds one adjacency the recurrence cannot express: house `n - 1` neighbors house `0`, so the newest decision would need to know about the oldest one. Every solution below attacks that single extra edge, and each cut street is solved with the same rob-or-skip machinery as before.

1. **Start literal.** Treat every plan as a rob/skip decision per house,
   enumerate all `2^n` of them, and reject any plan that robs two neighbors,
   including the wraparound pair `house n - 1, house 0`. Correct, but `O(n × 2^n)`:
   see [Brute Force](#brute-force).
2. **Spot the known problem inside.** The rejection rule's real content is one
   sentence: `house 0` and `house n - 1` cannot both be robbed. So split on
   `house 0`'s fate; either way the remainder is a straight street, the problem
   the House Robber recursion already solves: see [Two Linear
   Streets](#two-linear-streets).
3. **Spot the waste.** Run twice, the recursion is still the exponential
   tree from the linear problem, re-deciding every prefix of every cut street.
4. **Cache it.** Store each prefix's answer per street the first time it is
   computed; the trees collapse to one computation per house, `O(n)`: see
   [Top-Down Memoization](#top-down-memoization).
5. **Flip the direction, then shrink the state.** The memo fills from each
   street's start anyway, so tabulate both cuts bottom-up with a plain loop:
   see [Bottom-Up DP](#bottom-up-dp). Each table then reads only its two live
   entries, so two rolling totals per street replace the arrays and the space
   drops to `O(1)`: see [Space-Optimized DP](#space-optimized-dp).
6. **Hand the cache to the library.** Step 4's dictionary is pure bookkeeping;
   decorating the untouched recursion with `functools.cache` deletes it: see
   [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force

#### Derivation

The most direct reading writes the problem down clause by clause. A plan is one decision per house, so it encodes as an `n`-bit integer `plan` with bit `i` set when house `i` is robbed. The police alert fires when two adjacent houses are both set, and in a circle the adjacency list closes on itself: house `i` neighbors house `(i + 1) % n`, which makes `{0, 2}` an illegal pair as soon as `n = 3`. Enumerate every plan, keep the legal ones, and return the best total:

1. For each `plan` in `0 .. 2^n - 1`, test `valid`: no bit pair
   `i, (i + 1) % n` both set.
2. For a valid plan, total the robbed houses:
   `sum(nums[i] for i in range(n) if plan & (1 << i))`.
3. Keep the maximum in `best`; return it after the sweep.

Every plan pays its own `O(n)` legality check and sum, so the sweep costs `O(n × 2^n)`.

#### Walkthrough

Let us enumerate by hand on Example 1: `nums = [3,4,3]`, so `n = 3` and there are `2^3 = 8` plans. In a circle of three houses every house neighbors both others, because `(i + 1) % 3` wraps around:

```text
plan=000  {}        total=0   valid
plan=001  {0}       total=3   valid
plan=010  {1}       total=4   valid
plan=011  {0,1}     total=7   adjacent, skipped
plan=100  {2}       total=3   valid
plan=101  {0,2}     total=6   adjacent, skipped
plan=110  {1,2}     total=7   adjacent, skipped
plan=111  {0,1,2}   total=10  adjacent, skipped
```

Four plans survive, and the richest is `{1}` with `total = 4`. The tempting `{0,2}` plan worth `6` is rejected exactly as the problem's Explanation says: `nums[0]` and `nums[2]` are adjacent in a circle. The sweep returns `4`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's sweep: one legality test plus one total per plan.

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]

        def valid(plan: int) -> bool:
            # No two consecutive bits set, wrapping past the ends
            for i in range(n):
                if plan & (1 << i) and plan & (1 << ((i + 1) % n)):
                    return False
            return True

        best = 0
        for plan in range(2**n):
            if not valid(plan):
                continue
            total = sum(nums[i] for i in range(n) if plan & (1 << i))
            best = max(best, total)
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 2^n)`

The `2^n` plans each pay an `O(n)` adjacency scan and an `O(n)` total, so the sweep is linear work per plan.

##### Space Complexity: `O(1)`

Only `plan`, `total`, and `best` are held; no structure grows with `n`.

#### Key Insights

- The bitmask makes the circle free: the wraparound neighbor is just `(i + 1) % n`, so no special case survives beyond the modulo.
- The one-house circle degenerates: with `n = 1` the wraparound index `(0 + 1) % 1 = 0` makes house `0` its own neighbor, so the plan robbing the only house reads as adjacent to itself and the sweep would return `0`; the `n == 1` guard returns `nums[0]` before the sweep, the same load-bearing guard every later solution carries.
- Correct but the only approach that cannot run at the constraint cap: `n = 100` would sweep `2^100` plans, which is why every later solution attacks the enumeration instead of tuning it.

### Two Linear Streets

#### Derivation

The Brute Force pays exponential cost to re-derive one sentence: `house 0` and `house n - 1` cannot both be robbed. Make that sentence the algorithm. Split on `house 0`'s fate:

- `house 0` is skipped: the remaining choice is over houses `1 .. n - 1`, a straight street.
- `house 0` is robbed: houses `1` and `n - 1` are sealed, so the remaining choice is over houses `2 .. n - 2`, also a straight street, and `nums[0]` banks immediately.

Both branches are the House Robber problem, whose prefix recursion `decide(i) = max(decide(i - 1), houses[i] + decide(i - 2))` answers the straight street of any `houses` list. Carrying the street as a parameter saves the two guard cases: each cut is one call of the same recursion:

1. Cut the circle twice: `nums[:-1]` is the rob-allowed cut, where dropping
   `house n - 1` leaves `house 0` free to be robbed; `nums[1:]` is the skip
   cut, the street houses `1 .. n - 1` with `house 0`'s skip baked in.
2. Define `decide(houses, i)` as the most money robbable among the first `i + 1`
   houses of the cut street `houses`, with `decide(houses, i) = 0` for `i < 0`.
3. Skip branch: `decide(houses, i - 1)`. Rob branch:
   `houses[i] + decide(houses, i - 2)`.
4. Return `max(decide(nums[:-1], len(nums) - 2), decide(nums[1:], len(nums) - 2))`.

The single-house street has no pair to split, so it returns `nums[0]` directly. Nothing is cached, so each cut still grows the full exponential tree.

#### Walkthrough

Let us run both cuts by hand on Example 1: `nums = [3,4,3]`. The cut streets have two houses each, so `decide` bottoms out after one step:

```text
street [3, 4]   (house 2 dropped: house 0 may be robbed)
  decide(0) = max(0, 3 + 0) = 3
  decide(1) = max(3, 4 + 0) = 4
street [4, 3]   (house 0 dropped: house 0's plan is skip)
  decide(0) = max(0, 4 + 0) = 4
  decide(1) = max(4, 3 + 0) = 4
answer = max(4, 4) = 4
```

The two cuts tie at `4`. The tie is honest: with three houses in a circle exactly one house can be robbed, and every cut keeps two houses whose own best plan robs the richer middle one, `nums[1] = 4`. The call returns `4`, matching the expected Output for Example 1.

#### Solution

The code is the prefix recursion run twice, once per cut street.

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        def decide(houses: List[int], i: int) -> int:
            if i < 0:
                return 0
            # Skip the last house of the cut, or rob it
            return max(decide(houses, i - 1), houses[i] + decide(houses, i - 2))

        if len(nums) == 1:
            return nums[0]
        # House 0 may be robbed, keeping nums[:-1]; skipped, it keeps nums[1:]
        return max(decide(nums[:-1], len(nums) - 2), decide(nums[1:], len(nums) - 2))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Two uncached recursion trees, one per cut street; each branches two ways per level over `n - 1` houses, so the total is exponential with a small constant factor.

##### Space Complexity: `O(n)`

No table is kept, but the stack reaches depth `n - 1` down the deepest skip chain of a cut, and the two slices each hold `n - 1` values.

#### Key Insights

- The reduction, not the recursion, is the contribution: the circle costs exactly one case split, and everything else is the linear problem verbatim.
- Cutting into `nums[:-1]` and `nums[1:]` installs the case split without an `if` on house `0`: each cut already has house `0`'s decision baked in.
- The one-house street cannot be cut, since both slices would be empty, so the `len(nums) == 1` guard is load-bearing.

### Top-Down Memoization

#### Derivation

Two Linear Streets re-decides the same prefixes relentlessly: within a cut, `decide(houses, i)` depends on nothing but `i`, so every route reaching house `i` recomputes the same subtree. The repair is to [cache each prefix's result](https://en.wikipedia.org/wiki/Memoization) in a `memo` dictionary, one per street:

1. Keep `decide` verbatim from Two Linear Streets, base case included, with a
   `memo` argument threaded through.
2. Before computing, check `memo` and return a stored answer.
3. Otherwise compute `max(decide(houses, i - 1, memo), houses[i] + decide(houses, i - 2, memo))`
   and store it under key `i` before returning.
4. Each call passes a fresh `{}` for its street, so the two cuts never share
   entries.

Each house of each street now runs its body exactly once, so the two trees collapse from `O(2^n)` to `O(n)` combined.

#### Walkthrough

Let us trace both streets on Example 2: `nums = [2,9,8,3,6]`, four houses per cut, so the trees have real height. The trace indents one level per call; marked lines are memo hits:

```text
street [2, 9, 8, 3]          (house 4 dropped: house 0 may be robbed)
decide(3)  3 not in memo -> recurse
  decide(2)  2 not in memo -> recurse
    decide(1)  1 not in memo -> recurse
      decide(0)  0 not in memo -> recurse
        decide(-1) -> 0     base case
        decide(-2) -> 0     base case
      decide(0) -> 2        max(0, 2+0), memo[0] = 2
      decide(-1) -> 0       base case
    decide(1) -> 9          max(2, 9+0), memo[1] = 9
    decide(0) -> 2          ** memo hit **
  decide(2) -> 10           max(9, 8+2), memo[2] = 10
  decide(1) -> 9            ** memo hit **
decide(3) -> 12             max(10, 3+9), memo[3] = 12

street [9, 8, 3, 6]          (house 0 dropped: house 0's plan is skip)
decide(3)  3 not in memo -> recurse
  decide(2)  2 not in memo -> recurse
    decide(1)  1 not in memo -> recurse
      decide(0)  0 not in memo -> recurse
        decide(-1) -> 0     base case
        decide(-2) -> 0     base case
      decide(0) -> 9        max(0, 9+0), memo[0] = 9
      decide(-1) -> 0       base case
    decide(1) -> 9          max(9, 8+0), memo[1] = 9
    decide(0) -> 9          ** memo hit **
  decide(2) -> 12           max(9, 3+9), memo[2] = 12
  decide(1) -> 9            ** memo hit **
decide(3) -> 15              max(12, 6+9), memo[3] = 15
```

Every rob branch reaching into the street finds its two-back prefix already decided; at the street's edge the two-back house lies off the street and the base case answers `0`, as the negative indices are never stored in the memo. The streets end at `12` and `15`, and `max(12, 15) = 15` matches the expected Output for Example 2. Note the streets never share a `memo`: the two dictionaries are separate objects, and each street's `decide(1) = 9` is a coincidence of values, not shared state.

#### Solution

The code is the Two Linear Streets recursion with the memo check and store wrapped around the split.

```python
from typing import Dict, List


class Solution:
    def rob(self, nums: List[int]) -> int:
        def decide(houses: List[int], i: int, memo: Dict[int, int]) -> int:
            if i < 0:
                return 0
            if i in memo:
                return memo[i]
            # The same two branches as Two Linear Streets
            memo[i] = max(
                decide(houses, i - 1, memo),
                houses[i] + decide(houses, i - 2, memo),
            )
            return memo[i]

        if len(nums) == 1:
            return nums[0]
        return max(
            decide(nums[:-1], len(nums) - 2, {}),
            decide(nums[1:], len(nums) - 2, {}),
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each house of each cut street enters the body exactly once and combines two already-known values in constant time; every other call is a dictionary hit.

##### Space Complexity: `O(n)`

Each street keeps one memo entry per house, and the stack reaches depth `n - 1` down the deepest skip chain.

#### Key Insights

- The memo is keyed by `i` alone because the street is a parameter: one dictionary per cut street, and no key can collide across streets.
- Passing a fresh `{}` per call is what scopes the cache; a shared dictionary across streets would still be correct here, since the streets are disjoint house lists, but the scoping makes correctness obvious instead of argued.
- The base case `decide(houses, i) = 0` for `i < 0` folds both the empty street and house `0`'s missing `i - 2` neighbor into one return, exactly as in the linear problem.

### Bottom-Up DP

#### Derivation

The memoized recursion still starts at each street's end and unwinds to the empty prefix before producing its first useful value, paying call overhead and stack depth. Watch the order the memo actually fills: `decide(0)` first, then `decide(1)`, onward to the street's end. [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) with tabulation produces that same table in that same order with a plain loop, per cut street:

1. Define `rob_linear(houses)` as the straight-street answer over the cut
   street `houses`, and `dp[i]` as the most money robbable among its houses
   `0..i`, matching `decide(i)` exactly.
2. Seed `dp[0] = houses[0]` and `dp[1] = max(houses[0], houses[1])`.
3. Apply `dp[i] = max(dp[i - 1], dp[i - 2] + houses[i])` left to right.
4. Return `max(rob_linear(nums[:-1]), rob_linear(nums[1:]))`.

A cut street never has length below `2` for `n >= 3`, but the single-house street still bypasses the cut entirely with its own guard.

#### Recurrence

Let `rob_linear(houses)` be the straight-street answer and `dp[i]` the most money robbable among the cut street's houses `0..i`:

$$ \text{answer} = \max(\text{rob\_linear}(\text{nums}[:-1]),\ \text{rob\_linear}(\text{nums}[1:])) $$

$$ dp[i] = \begin{cases} \text{houses}[0], & i = 0 \\[4pt] \max(\text{houses}[0],\ \text{houses}[1]), & i = 1 \\[4pt] \max(dp[i-1],\ dp[i-2] + \text{houses}[i]), & i \ge 2 \end{cases} $$

```text
answer = max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
dp[0] = houses[0]
dp[1] = max(houses[0], houses[1])
dp[i] = max(dp[i - 1], dp[i - 2] + houses[i])   for i >= 2
```

The reduction is the outer relation: the circle is decided by taking the better of the two cut streets. The inner relation is the linear recurrence, whose base cases are its own virtual entries `dp[-1] = dp[-2] = 0`: with no houses before the cut's start, skipping is worth nothing and robbing the first house banks `houses[0]`. The answer is the larger street answer of the two.

#### Walkthrough

Let us fill both tables on Example 2: `nums = [2,9,8,3,6]`. Each entry combines the two just below it:

```text
street [2, 9, 8, 3]
start    dp = [2, 0, 0, 0]           dp[0] = houses[0] = 2
i = 1    dp[1] = max(2, 9) = 9       dp = [2, 9, 0, 0]
i = 2    dp[2] = max(9, 2+8) = 10    dp = [2, 9, 10, 0]
i = 3    dp[3] = max(10, 9+3) = 12   dp = [2, 9, 10, 12]

street [9, 8, 3, 6]
start    dp = [9, 0, 0, 0]           dp[0] = houses[0] = 9
i = 1    dp[1] = max(9, 8) = 9       dp = [9, 9, 0, 0]
i = 2    dp[2] = max(9, 9+3) = 12    dp = [9, 9, 12, 0]
i = 3    dp[3] = max(12, 9+6) = 15   dp = [9, 9, 12, 15]

answer = max(12, 15) = 15
```

Each table row reproduces exactly one memo entry from the Top-Down walkthrough, filled in the order the recursion used to discover them. The tables end at `12` and `15`; taking the larger matches the expected Output for Example 2.

#### Solution

The code is the table fill from the walkthrough: per cut street, seed two base cases, then loop the recurrence upward.

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        def rob_linear(houses: List[int]) -> int:
            m = len(houses)
            # dp[i] = most money robbable among houses[0..i] of this cut street
            dp = [0] * m
            dp[0] = houses[0]
            if m == 1:
                return dp[0]
            dp[1] = max(houses[0], houses[1])
            for i in range(2, m):
                dp[i] = max(dp[i - 1], dp[i - 2] + houses[i])
            return dp[m - 1]

        if len(nums) == 1:
            return nums[0]
        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two passes, one per cut street, with constant work per house: one addition and one max.

##### Space Complexity: `O(n)`

Each cut street's `dp` table holds one entry per house of that street.

#### Key Insights

- The tables are the two memos turned upright: same entries, same values, filled in the order the recursion used to discover them.
- The `m == 1` guard inside `rob_linear` is dead code for `n >= 3` but earns its keep at `n = 2`, where a cut street is a single house.
- Having every prefix's answer on hand per street is what makes sub-street queries answerable, which is worth the arrays when follow-ups exist.

### Space-Optimized DP

#### Derivation

Each table loop reads only the two entries just below the one it writes: `dp[i - 1]` and `dp[i - 2]`. Everything older is dead weight, so each street's array collapses into two rolling totals, `two_back` standing in for `dp[i - 2]` and `one_back` for `dp[i - 1]`. Seeding both at `0` installs the recurrence's virtual entries `dp[-1] = dp[-2] = 0`, which folds the base cases into the loop and removes the length guards inside `rob_linear`:

1. Start each street with `two_back = 0` and `one_back = 0`, the values before
   the street's first house.
2. For each house's `money`, compute
   `best_here = max(one_back, two_back + money)`: skip the house and keep
   `one_back`, or rob it and add to `two_back`.
3. Shift the window: `two_back = one_back`, then `one_back = best_here`.
4. After the last house, `one_back` holds the street's answer; return the
   larger of the two streets' `one_back`.

#### Walkthrough

Let us roll the two totals through Example 2: `nums = [2,9,8,3,6]`. Before each house, `one_back` holds the best through the previous house of that street and `two_back` the best through the house before that:

```text
street [2, 9, 8, 3]
start      two_back = 0    one_back = 0
money=2    best_here = max(0, 0+2) = 2    -> two_back = 0,  one_back = 2
money=9    best_here = max(2, 0+9) = 9    -> two_back = 2,  one_back = 9
money=8    best_here = max(9, 2+8) = 10   -> two_back = 9,  one_back = 10
money=3    best_here = max(10, 9+3) = 12  -> two_back = 10, one_back = 12

street [9, 8, 3, 6]
start      two_back = 0    one_back = 0
money=9    best_here = max(0, 0+9) = 9    -> two_back = 0,  one_back = 9
money=8    best_here = max(9, 0+8) = 9    -> two_back = 9,  one_back = 9
money=3    best_here = max(9, 9+3) = 12   -> two_back = 9,  one_back = 12
money=6    best_here = max(12, 9+6) = 15  -> two_back = 12, one_back = 15

answer = max(12, 15) = 15
```

Each row reproduces exactly one `dp` entry from the Bottom-Up walkthrough: `best_here` is `dp[i]`, computed from `dp[i - 1]` and `dp[i - 2]` before the shift renames them. The streets end at `12` and `15`; taking the larger matches the expected Output for Example 2.

#### Solution

The code is the walkthrough's three lines per house, run over each cut street.

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        def rob_linear(houses: List[int]) -> int:
            two_back = 0  # best total over this street's houses up to i - 2
            one_back = 0  # best total over this street's houses up to i - 1
            for money in houses:
                best_here = max(one_back, two_back + money)
                two_back = one_back
                one_back = best_here
            return one_back

        if len(nums) == 1:
            return nums[0]
        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two linear passes, one per cut street, with constant work each: one max, two assignments.

##### Space Complexity: `O(1)`

Two rolling totals live at a time per pass: `O(1)` auxiliary beyond the `O(n)` transient street slices.

#### Key Insights

- The reduction survives the shrinking untouched: the circle is still exactly one case split, and each split street is still the two-total linear pass.
- The rolling seeds `two_back = one_back = 0` are only safe because values are non-negative (`0 <= nums[i]`): the `max` then never prefers a phantom take, so the virtual `dp[-1] = dp[-2] = 0` entries behave exactly like the table's base cases.
- Slicing costs `O(n)` transient space per street; folding the cut into index bounds (`rob_linear` over a range instead of a slice) recovers it, at the price of two flag parameters wiring house `0`'s fate into the pass.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution stacks two separate things: the rob-or-skip recurrence, and a dictionary that stops the recursion from recomputing a prefix it has already answered. Only the first is the algorithm. The second is pure bookkeeping, and the standard library already implements it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recurrence and its base case stay on the page exactly as Two Linear Streets wrote them:

1. Keep `decide(houses, i)` verbatim from Two Linear Streets: return `0` for
   `i < 0`, otherwise return
   `max(decide(houses, i - 1), houses[i] + decide(houses, i - 2))`.
2. Decorate it with `@cache`, so each distinct `(houses, i)` pair runs the body
   at most once and every later request is answered from the cache.
3. Delete the bookkeeping the decorator now owns: the `memo` parameter, the
   `if i in memo` lookup, and the `memo[i] = ...` store.
4. Hand the decorator hashable streets: lists are not hashable, so the two cut
   streets enter as `tuple(nums[:-1])` and `tuple(nums[1:])`.

One behavioural difference follows from where the decorator sits. The hand-rolled version answers `i < 0` before it ever consults `memo`, so the base-case keys are never stored; `@cache` wraps the entire body, so the negative indices are cached like any other house. And because the cache keys on the whole argument tuple, the two cut streets coexist in one cache without colliding, which is why no per-street dictionary is needed.

#### Walkthrough

Run it on Example 1, `nums = [3,4,3]`: both cut streets are two-house tuples, so each tree bottoms out after one step. The trace indents one level per call and notes whether the decorator ran the body or answered from the cache:

```text
street (3, 4)
decide(1)   miss, run the body
  decide(0)   miss, run the body
    decide(-1) -> 0     base case, now cached under key -1
    decide(-2) -> 0     base case, now cached under key -2
  decide(0) -> 3        max(0, 3+0), cached under key 0
  decide(-1) -> 0       ** cache hit, the body does not run **
decide(1) -> 4          max(3, 4+0), cached under key 1

street (4, 3)
decide(1)   miss, run the body
  decide(0)   miss, run the body
    decide(-1) -> 0     base case, now cached under key -1
    decide(-2) -> 0     base case, now cached under key -2
  decide(0) -> 4        max(0, 4+0), cached under key 0
  decide(-1) -> 0       ** cache hit, the body does not run **
decide(1) -> 4          max(4, 3+0), cached under key 1

answer = max(4, 4) = 4
```

Each street's `decide(1)` needs `decide(0)` and `decide(-1)`; resolving `decide(0)` first caches `decide(-1)`, so the later request inside `decide(1)`'s own rob branch is answered from the cache. Both streets return `4`, and `max(4, 4) = 4` matches the expected Output for Example 1.

#### Solution

The Two Linear Streets recursion, unchanged, with one decorator standing in for the memo dictionaries.

```python
from functools import cache
from typing import List, Tuple


class Solution:
    def rob(self, nums: List[int]) -> int:
        # The cache lives on this inner function object, which is rebuilt on
        # every call, so results never carry over between inputs or streets.
        @cache
        def decide(houses: Tuple[int, ...], i: int) -> int:
            if i < 0:
                return 0
            # Skip house i, or rob it and silence house i - 1
            return max(decide(houses, i - 1), houses[i] + decide(houses, i - 2))

        if len(nums) == 1:
            return nums[0]
        return max(
            decide(tuple(nums[:-1]), len(nums) - 2),
            decide(tuple(nums[1:]), len(nums) - 2),
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- The cache admits each `(street, house)` pair into the body exactly once,
  and each admission does one addition and one max of two already-known values
- Every other call is a dictionary lookup on a small tuple key, which is
  constant time, so the total is linear in `n`

##### Space Complexity: `O(n)`

- The decorator's cache holds one entry per distinct `(houses, i)` pair, the
  `2 × (n - 1)` street-house pairs plus the negative base-case keys
- The recursion still descends to depth `n - 1` before the first value
  returns, so the stack matches the cache in order of growth

#### Key Insights

- The algorithm is untouched: the recurrence and the base case read exactly as they do in Two Linear Streets, which makes plain that memoization is an execution strategy rather than a change to the recursion.
- Keying on the whole `(houses, i)` tuple is what absorbs the case split: two streets in one cache, no per-street dictionary, and no risk of a cross-street collision because the street tuples differ.
- Lists are unhashable, so the cut streets must enter as tuples; the conversion is `O(n)` per street and does not change the bound.
- Defining the cached function inside the method scopes the cache to a single call, avoiding the stale-results and unbounded-growth hazards of decorating a method or a module-level function.

## Comparison of Solutions

The practice harness's `practice/house_robber_ii/reference.py` implements the **Space-Optimized DP** solution.

### Time Complexity

- **Brute Force**: `O(n × 2^n)` - every one of the `2^n` plans pays an `O(n)` legality check and total.
- **Two Linear Streets**: `O(2^n)` - two uncached recursion trees, one per cut street.
- **Top-Down Memoization**: `O(n)` - one body run per house of each cut street, later visits are dictionary hits.
- **Bottom-Up DP**: `O(n)` - two linear table fills, one per cut street.
- **Space-Optimized DP**: `O(n)` - the same two linear passes with two totals instead of tables.
- **Top-Down Memoization with functools.cache**: `O(n)` - the decorator reproduces the memoized run times.

### Space Complexity

- **Brute Force**: `O(1)` - only `plan`, `total`, and `best`.
- **Two Linear Streets**: `O(n)` - recursion stack plus the two slices.
- **Top-Down Memoization**: `O(n)` - one memo entry per house per street plus the stack.
- **Bottom-Up DP**: `O(n)` - the two `dp` tables.
- **Space-Optimized DP**: `O(1)` - two rolling totals per pass, beyond the slice handed in.
- **Top-Down Memoization with functools.cache**: `O(n)` - the decorator's cache plus the stack.

### Trade-offs

- The Brute Force is the problem statement transcribed, adjacency wraparound included, and needs no insight at all; it is also the only approach that cannot run at the constraint cap.
- Two Linear Streets isolates the entire difficulty of the circle into one case split and inherits the linear recursion verbatim, but without caching it keeps the exponential tree.
- Both memoized versions keep the recursion's shape, which makes correctness easy to argue, at the price of stack depth `n` on top of the memo.
- The Bottom-Up DP pays the same linear time without recursion and keeps every prefix's answer per street, which matters only when those answers are queried again later.
- The Space-Optimized DP gives up random access to old prefixes and keeps just the two live entries per street, reaching constant space with no new risk.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for checking the faster versions on small circles.
- **Two Linear Streets**: when deriving the reduction fresh and street lengths stay tiny.
- **Top-Down Memoization**: when the recursive shape is easiest to trust and the memo should be visible.
- **Bottom-Up DP**: when the per-prefix answers are reused by follow-up queries or variants of the problem.
- **Space-Optimized DP** (recommended): the default; the same two linear passes at constant space, with the base cases folded into the seeds so no guard survives inside the pass.
- **Top-Down Memoization with functools.cache**: the Pythonic tidy-up when the recursive shape is wanted and the memo should not be hand-maintained.

### Optimization Notes

- The reduction is exact, not a heuristic: in the skip branch the circle's remaining constraint is the straight street `nums[1: n]`, and in the rob branch robbing `nums[0]` banks it and deletes both its neighbors, leaving the straight street `nums[2: n - 1]`. Every legal circular plan falls into exactly one branch, so the max over the two cuts is the circle's optimum.
- The cut streets for `n >= 2` have length `n - 1 >= 1`, which is why only the full street needs the single-house guard, not the passes: the rolling pass handles a one-house street on its own, while the cut of a one-house circle would be empty and is never taken.
- Slicing each street costs `O(n)` transient space; the Space-Optimized DP keeps it for readability, and the index-bounds variant noted in its Key Insights is the drop to true `O(1)` if the allocator cares.
- The same reduction pattern, one case split plus a straight-street solver, covers the circular variants of other linear DP problems: the circle is never unrolled, it is cut twice.
