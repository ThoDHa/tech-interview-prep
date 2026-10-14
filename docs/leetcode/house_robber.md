# [House Robber](https://leetcode.com/problems/house-robber/)

**Medium** | **25 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Recurrence relation](https://en.wikipedia.org/wiki/Recurrence_relation)

**Practice:** [`practice/house_robber/solution.py`](../../practice/house_robber/solution.py)

You are given an integer array `nums` where `nums[i]` represents the amount of money the `i`th house has. The houses are arranged in a straight line, i.e. the `i`th house is the neighbor of the `(i-1)`th and `(i+1)`th house.

You are planning to rob money from the houses, but you cannot rob **two adjacent houses** because the security system will automatically alert the police if two adjacent houses were *both* broken into.

Return the *maximum* amount of money you can rob **without** alerting the police.

## Examples

### Example 1

**Input:** `nums = [1,1,3,3]`

**Output:** `4`

**Explanation:** `nums[0]` + `nums[2]` = `1` + `3` = `4`.

### Example 2

**Input:** `nums = [2,9,8,3,6]`

**Output:** `16`

**Explanation:** `nums[0]` + `nums[2]` + `nums[4]` = `2` + `8` + `6` = `16`.

## Constraints

- `1 <= nums.length <= 100`
- `0 <= nums[i] <= 100`

## Deriving the Solution

Each house forces a binary choice, rob it or skip it, and robbing it makes its neighbor off limits. The choice's consequences reach only two houses back: whatever the plan did before house `i - 2` is already summarized by the most money robbable among the houses up to that point. So one number per prefix, the best total through house `i`, is all any decision ever needs, and the approaches below differ in how they compute that number.

1. **Start literal.** Recurse on the newest house: the best plan through house
   `i` either skips it, keeping the best through `i - 1`, or robs it, adding
   `nums[i]` to the best through `i - 2`. Correct, but every route through the
   street re-decides the same prefix, costing `O(2^n)`: see [Brute Force](#brute-force).
2. **Spot the waste.** `decide(i)` is a question about the houses up to `i` and
   nothing else: two different routes reach house `i`, get the same answer
   twice, and pay the full subtree both times.
3. **Cache it.** Store each prefix's answer the first time it is computed;
   every later visit is a dictionary lookup and the tree collapses to one
   computation per house, `O(n)`: see [Top-Down Memoization](#top-down-memoization).
4. **Flip the direction.** The memo fills from the street's start anyway, since
   the deepest calls are the shortest prefixes: skip the recursion and fill a
   `dp` table upward with a plain loop: see [Bottom-Up DP](#bottom-up-dp).
5. **Shrink the state.** `dp[i]` reads only the two entries just below it, so
   two rolling totals replace the whole array and the space drops to `O(1)`:
   see [Space-Optimized DP](#space-optimized-dp).
6. **Hand the cache to the library.** Step 3 stacked two ideas: the recurrence,
   and a dictionary keeping it from redoing work. Only the recurrence is the
   algorithm, so decorating the Brute Force function with `functools.cache`
   deletes the bookkeeping and leaves the recursion untouched: see
   [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force

#### Derivation

The most direct reading walks the street once and, standing at each house, asks a question about everything before it: what is the most money robbable among houses `0..i`? House `i` is either skipped, in which case the answer is whatever house `i - 1` allowed, or robbed, in which case house `i - 1` is off limits and the take is `nums[i]` plus whatever house `i - 2` allowed:

1. Define `decide(i)` as the most money robbable among houses `0..i`, with
   `decide(i) = 0` for every `i < 0` (no houses, no money).
2. Skip branch: `decide(i - 1)`, the best plan that ignores house `i`.
3. Rob branch: `nums[i] + decide(i - 2)`, since robbing `i` silences `i - 1`.
4. Return `max(skip, rob_here)`; the answer is `decide(len(nums) - 1)`.

Nothing is remembered between calls, so the two branches re-decide the same shorter prefixes over and over: the call tree fans out two ways per level and the same subtree is grown once per route that reaches it.

#### Walkthrough

Trace the recursion on Example 1: `nums = [1, 1, 3, 3]`. The entry call is `decide(3)`, and each call splits into its skip branch (`decide(i - 1)`) and its rob branch (`nums[i] + decide(i - 2)`), with `decide` returning `0` for negative indices:

```text
decide(3)                        max(skip, 3 + decide(1))
├── skip: decide(2)              max(skip, 3 + decide(0))
│     ├── skip: decide(1)        max(skip, 1 + decide(-1))
│     │     ├── skip: decide(0)  max(skip, 1 + decide(-2))
│     │     │     ├── skip: decide(-1) -> 0    base case
│     │     │     └── rob:  1 + 0 = 1
│     │     │     -> decide(0) = 1
│     │     └── rob:  1 + decide(-1) = 1 + 0 = 1
│     │     -> decide(1) = 1
│     └── rob:  3 + decide(0) = 3 + 1 = 4
│     -> decide(2) = 4
└── rob:  3 + decide(1) = 3 + 1 = 4
-> decide(3) = max(4, 4) = 4
```

Both branches at the root reach `4`: skipping house `3` keeps houses `0` and `2`, robbing it keeps houses `1` and `3`, and the two plans happen to be worth the same. The call returns `4`, matching the expected Output for Example 1. The tree is small only because the example is: every level repeats the prefixes the level above already decided, which is exactly the rework the next solution removes.

#### Solution

The code is the walkthrough's two branches around the negative-index base case.

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        def decide(i: int) -> int:
            if i < 0:
                return 0
            # Skip house i, keeping whatever house i - 1 allowed
            skip = decide(i - 1)
            # Rob house i, so house i - 1 is off limits
            rob_here = nums[i] + decide(i - 2)
            return max(skip, rob_here)

        return decide(len(nums) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each call forks into two more, so the call tree roughly doubles at every level of the `n` houses; it grows like the Fibonacci numbers, which is exponential. Nothing is shared between the branches, so every route pays in full.

##### Space Complexity: `O(n)`

No table is kept, but the recursion stack reaches depth `n` along the deepest chain of skip branches.

#### Key Insights

- The two branches encode the whole constraint: robbing `i` jumps the recursion to `i - 2`, skipping stays at `i - 1`, so no adjacency check is ever needed.
- The negative-index base case folds both "no houses yet" and "house `0` has no `i - 2` neighbor" into a single `0` return.
- The recursion is correct but recomputes each prefix once per route reaching it, which is the waste every later solution attacks.

### Top-Down Memoization

#### Derivation

The Brute Force re-decides the same prefixes relentlessly, yet `decide(i)` depends on nothing but `i`: every route that reaches house `i` gets the same answer. The repair is to [cache each prefix's result](https://en.wikipedia.org/wiki/Memoization) in a dictionary keyed by the house index, so the two routes into house `i` share one computation:

1. Keep `decide(i)` verbatim from the Brute Force, base case included.
2. Before computing, check the `memo` dictionary and return a stored answer.
3. Otherwise compute `max(decide(i - 1), nums[i] + decide(i - 2))` and store it
   under key `i` before returning.
4. Each house from `0` to `n - 1` now runs its body exactly once, so the tree
   collapses from `O(2^n)` nodes to `O(n)`.

#### Walkthrough

Trace the recursion on Example 2: `nums = [2, 9, 8, 3, 6]`, the longer of the two examples, so the tree has real height. The trace indents one level per call; marked lines are memo hits:

```text
decide(4)               4 not in memo -> recurse
  decide(3)             3 not in memo -> recurse
    decide(2)           2 not in memo -> recurse
      decide(1)         1 not in memo -> recurse
        decide(0)       0 not in memo -> recurse
          decide(-1) -> 0     base case
          decide(-2) -> 0     base case
        decide(0) -> 2        max(0, 2+0), memo[0] = 2
        decide(-1) -> 0       base case
      decide(1) -> 9          max(2, 9+0), memo[1] = 9
      decide(0) -> 2          ** memo hit **
    decide(2) -> 10           max(9, 8+2), memo[2] = 10
    decide(1) -> 9            ** memo hit **
  decide(3) -> 12             max(10, 3+9), memo[3] = 12
  decide(2) -> 10             ** memo hit **
decide(4) -> 16               max(12, 6+10), memo[4] = 16
```

Every rob branch reaches two houses back and finds the prefix already decided: house `2`'s rob reuses the stored `decide(0)`, house `3`'s rob reuses `decide(1)`, and house `4`'s rob reuses `decide(2)`. Each stored value runs its body exactly once, on the first visit, and the call returns `16`, matching the expected Output for Example 2.

#### Solution

The code is the Brute Force recursion with the memo check and store wrapped around the split.

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        memo = {}

        def decide(i: int) -> int:
            if i < 0:
                return 0
            if i in memo:
                return memo[i]

            # The same two branches as the Brute Force
            memo[i] = max(decide(i - 1), nums[i] + decide(i - 2))
            return memo[i]

        return decide(len(nums) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each house from `0` to `n - 1` enters the body exactly once and does constant work combining two already-known values; every other call is a dictionary hit.

##### Space Complexity: `O(n)`

The memo stores one entry per house, and the recursion stack reaches depth `n` along the deepest skip chain.

#### Key Insights

- The dictionary is keyed by the house index alone, which works because the prefix through `i` fully determines the answer: no other state exists.
- Writing the check-compute-store cycle by hand shows the mechanism a decorator would hide, which is worth seeing once; `functools.cache` collapses those three lines, see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).
- Memoization converts the exponential tree into linear time without touching the recursion's shape, which makes the correctness argument easy to carry over.

### Bottom-Up DP

#### Derivation

The memoized recursion still starts at the last house and unwinds all the way down to the empty prefix before producing its first useful value, paying call overhead and stack depth along the way. Watch the order its memo actually fills: `decide(0)` first, then `decide(1)`, then onward toward the street's end. [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) with tabulation produces that same table in that same order with a plain loop and no recursion at all:

1. Let `dp[i]` be the most money robbable among houses `0..i`, matching
   `decide(i)` exactly.
2. Seed the base cases `dp[0] = nums[0]` and
   `dp[1] = max(nums[0], nums[1])`.
3. Apply `dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])` left to right.
4. Return `dp[n - 1]`, the best plan over the whole street.

A street of one house never reaches step 3, and `dp[1]` would index out of bounds, so the single-house street returns `nums[0]` directly.

#### Recurrence

Let `dp[i]` be the most money robbable among houses `0..i`:

$$ dp[i] = \begin{cases} \text{nums}[0], & i = 0 \\[4pt] \max(\text{nums}[0],\ \text{nums}[1]), & i = 1 \\[4pt] \max(dp[i-1],\ dp[i-2] + \text{nums}[i]), & i \ge 2 \end{cases} $$

```text
dp[0] = nums[0]
dp[1] = max(nums[0], nums[1])
dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])   for i >= 2
```

The base cases are the recurrence applied to the two virtual entries `dp[-1] = dp[-2] = 0`: with no houses before the street's start, skipping house `0` is worth nothing and robbing it banks `nums[0]`. The answer is read from the last entry, `dp[n - 1]`.

#### Walkthrough

Let us fill the table on Example 2: `nums = [2, 9, 8, 3, 6]`. Each entry combines the two just below it:

```text
start    dp = [2, 0, 0, 0, 0]           dp[0] = nums[0] = 2
i = 1    dp[1] = max(2, 9) = 9          dp = [2, 9, 0, 0, 0]
i = 2    dp[2] = max(9, 2+8) = 10       dp = [2, 9, 10, 0, 0]
i = 3    dp[3] = max(10, 9+3) = 12      dp = [2, 9, 10, 12, 0]
i = 4    dp[4] = max(12, 10+6) = 16     dp = [2, 9, 10, 12, 16]
```

At `i = 2` the rob branch wins for the first time: `dp[0] + nums[2] = 10` beats skipping through to `dp[1] = 9`, because robbing house `2` frees house `0` to stay robbed. At `i = 4` the same shape repeats: `dp[2] + 6 = 16` beats `dp[3] = 12`. The method returns `dp[4] = 16`, matching the expected Output for Example 2.

#### Solution

The code is the table fill from the walkthrough: seed two base cases, then loop the recurrence upward.

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]

        # dp[i] = most money robbable among houses 0..i
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        for i in range(2, n):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])

        return dp[n - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass seeds the base cases and one pass applies the recurrence, constant work per house.

##### Space Complexity: `O(n)`

The `dp` table stores one entry per house.

#### Key Insights

- The table is the memo turned upright: same entries, same values, filled in the order the recursion used to discover them.
- The explicit table needs a `n == 1` guard because `dp[1]` must exist before the loop; the rolling version below folds the base cases into its seeds and needs none.
- Having every prefix's answer on hand is what makes variants answerable (for example, the best plan over any sub-street), which is worth the array when the extra queries exist.

### Space-Optimized DP

#### Derivation

The table loop reads only the two entries just below the one it writes: `dp[i - 1]` and `dp[i - 2]`. Everything older is dead weight, so the whole array collapses into two rolling totals, `two_back` standing in for `dp[i - 2]` and `one_back` for `dp[i - 1]`. Seeding both at `0` installs the recurrence's virtual entries `dp[-1] = dp[-2] = 0`, which folds the base cases into the loop and removes the single-house guard:

1. Start with `two_back = 0` and `one_back = 0`, the values before the first
   house.
2. For each house's `money`, compute
   `best_here = max(one_back, two_back + money)`: skip the house and keep
   `one_back`, or rob it and add to `two_back`.
3. Shift the window: `two_back = one_back`, then `one_back = best_here`.
4. After the last house, `one_back` holds the answer.

#### Walkthrough

Let us roll the two totals through Example 2: `nums = [2, 9, 8, 3, 6]`. Before each house, `one_back` holds the best through the previous house and `two_back` the best through the house before that:

```text
start      two_back = 0    one_back = 0
nums[0]=2  best_here = max(0, 0+2) = 2     -> two_back = 0,  one_back = 2
nums[1]=9  best_here = max(2, 0+9) = 9     -> two_back = 2,  one_back = 9
nums[2]=8  best_here = max(9, 2+8) = 10    -> two_back = 9,  one_back = 10
nums[3]=3  best_here = max(10, 9+3) = 12   -> two_back = 10, one_back = 12
nums[4]=6  best_here = max(12, 10+6) = 16  -> two_back = 12, one_back = 16
```

Each row reproduces exactly one `dp` entry from the Bottom-Up walkthrough: `best_here` is `dp[i]`, computed from `dp[i - 1]` and `dp[i - 2]` before the shift renames them. After the last house `one_back` holds `dp[4] = 16`, matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's three lines per house: combine, then shift the window.

```python
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        two_back = 0  # dp[i - 2]: best total through house i - 2
        one_back = 0  # dp[i - 1]: best total through house i - 1
        for money in nums:
            best_here = max(one_back, two_back + money)
            two_back = one_back
            one_back = best_here
        return one_back
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass over the houses with constant work each: one max, two assignments.

##### Space Complexity: `O(1)`

Two rolling totals, regardless of how long the street is.

#### Key Insights

- Only a two-entry window of the table is ever alive, which is the defining feature of a linear 1-D recurrence and the reason the space collapses to constants.
- Seeding both totals at `0` is not sloppiness: it installs the recurrence's virtual `dp[-1] = dp[-2] = 0` entries, so the first house is handled by the same `max` as every other and no length guard survives.
- This is the optimal trade for the single-query problem: the explicit table buys reusable per-prefix answers that this version deliberately gives up.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution stacks two separate things: the rob-or-skip recurrence, and a dictionary that stops the recursion from recomputing a prefix it has already answered. Only the first is the algorithm. The second is pure bookkeeping, and the standard library already implements it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recurrence and its base case stay on the page exactly as the Brute Force wrote them:

1. Keep `decide(i)` verbatim from the Brute Force: return `0` for `i < 0`,
   otherwise return `max(decide(i - 1), nums[i] + decide(i - 2))`.
2. Decorate it with `@cache`, so each distinct `i` runs the body at most once
   and every later request for that prefix is answered from the cache.
3. Delete the three bookkeeping lines the decorator now owns: the `memo = {}`
   declaration, the `if i in memo` lookup, and the `memo[i] = ...` store.
4. Because `decide` is defined inside `rob`, each call builds a fresh function
   object with a fresh cache, so nothing leaks between inputs; a `@cache` on a
   method or a module-level function would instead live for the whole process.

One behavioural difference follows from where the decorator sits. The hand-rolled version answers `i < 0` before it ever consults `memo`, so the base-case keys are never stored; `@cache` wraps the entire body, so the negative indices are cached like any other house.

#### Walkthrough

Run it on Example 1, `nums = [1, 1, 3, 3]`. The trace indents one level per call and notes whether the decorator ran the body or answered from the cache:

```text
decide(3)   miss, run the body
  decide(2)   miss, run the body
    decide(1)   miss, run the body
      decide(0)   miss, run the body
        decide(-1) -> 0     base case, now cached under key -1
        decide(-2) -> 0     base case, now cached under key -2
      decide(0) -> 1        max(0, 1+0), cached under key 0
      decide(-1) -> 0       ** cache hit, the body does not run **
    decide(1) -> 1          max(1, 1+0), cached under key 1
    decide(0) -> 1          ** cache hit, the body does not run **
  decide(2) -> 4            max(1, 3+1), cached under key 2
  decide(1) -> 1            ** cache hit, the body does not run **
decide(3) -> 4              max(4, 3+1), cached under key 3
```

`decide(3)` needs both `decide(2)` and `decide(1)`. Resolving `decide(2)` first computes and caches `decide(1)` and `decide(0)`, so the later requests for those prefixes, including the one inside `decide(3)`'s own rob branch, are answered from the cache. The outer call returns `4`, matching the expected Output for Example 1.

#### Solution

The Brute Force recursion, unchanged, with one decorator standing in for the memo dictionary.

```python
from functools import cache
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        # The cache lives on this inner function object, which is rebuilt on
        # every call, so results never carry over between inputs.
        @cache
        def decide(i: int) -> int:
            if i < 0:
                return 0
            # Skip house i, or rob it and silence house i - 1
            return max(decide(i - 1), nums[i] + decide(i - 2))

        return decide(len(nums) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- The cache admits each house from `0` to `n - 1` into the body exactly once,
  and each admission does one addition and one max of two already-known values
- Every other call is a dictionary lookup on a small integer key, which is
  constant time, so the total is linear in `n`

##### Space Complexity: `O(n)`

- The decorator's cache holds one entry per distinct argument, the `n` houses
  plus the two negative base-case keys
- The recursion still descends to depth `n` before the first value returns, so
  the stack matches the cache in order of growth

#### Key Insights

- The algorithm is untouched: the recurrence and the base case read exactly as they do in the Brute Force, which makes plain that memoization is an execution strategy rather than a change to the recursion.
- `@cache` keys on the argument tuple, so it is a drop-in replacement only when the arguments are hashable and the function is genuinely pure; `decide` reads nothing but `i` and `nums`, which is what licenses the substitution.
- Defining the cached function inside the method scopes the cache to a single call, avoiding the stale-results and unbounded-growth hazards of decorating a method or a module-level function.
- Use `functools.lru_cache(maxsize=...)` instead when the key space is unbounded and eviction matters; `cache` is `lru_cache(maxsize=None)`, which never evicts.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^n)` - every route re-decides the prefixes before it, and the tree doubles per house.
- **Top-Down Memoization**: `O(n)` - one body run per house, later visits are dictionary hits.
- **Bottom-Up DP**: `O(n)` - one pass seeds two base cases, one pass applies the recurrence.
- **Space-Optimized DP**: `O(n)` - the same single pass with two totals instead of a table.
- **Top-Down Memoization with functools.cache**: `O(n)` - the decorator reproduces the memoized run times.

### Space Complexity

- **Brute Force**: `O(n)` - recursion stack depth only.
- **Top-Down Memoization**: `O(n)` - one memo entry per house plus the stack.
- **Bottom-Up DP**: `O(n)` - the explicit table.
- **Space-Optimized DP**: `O(1)` - two rolling totals.
- **Top-Down Memoization with functools.cache**: `O(n)` - the decorator's cache plus the stack.

### Trade-offs

- The Brute Force is the direct transcription of the rob-or-skip rule and needs no auxiliary structure, but it is the only approach here that misses the constraint budget for large streets.
- Both memoized versions keep the recursion's shape, which makes correctness easy to argue, at the price of stack depth `n` on top of the memo.
- The Bottom-Up DP pays the same linear time without recursion and keeps every prefix's answer, which matters only when those answers are queried again later.
- The Space-Optimized DP gives up random access to old prefixes and keeps just the two live entries, reaching constant space with no new risk.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for checking the faster versions on small streets.
- **Top-Down Memoization**: when the recurrence is easiest to trust in its recursive form and street lengths stay modest.
- **Bottom-Up DP**: when the per-prefix answers are reused by follow-up queries or variants of the problem.
- **Space-Optimized DP** (recommended): the default; the same linear pass at constant space, with the base cases folded into the seeds so no edge-case guard remains.
- **Top-Down Memoization with functools.cache**: the Pythonic tidy-up when the recursive shape is wanted and the memo should not be hand-maintained.

### Optimization Notes

- The two-lookback window is not an approximation: robbing house `i` can never combine with houses older than `i - 2` directly, because anything older is already folded into the best total through `i - 2`, which is why two rolling slots suffice for any street length.
- The rolling seeds `two_back = one_back = 0` are only safe because values are non-negative (`0 <= nums[i]`): the `max` then never prefers a negative take, and the virtual `dp[-1] = dp[-2] = 0` entries behave exactly like the table's base cases.
- The memoized versions recurse to depth `n`, so a street at the constraint cap of 100 houses sits far below Python's default recursion limit; for much longer streets the iterative table or the rolling totals avoid the stack entirely.
- The same prefix recurrence, read backwards, drives House Robber II's circular street: that variant has to break the circle (fix the first house's fate and run the linear pass twice) because the two ends become neighbors.
