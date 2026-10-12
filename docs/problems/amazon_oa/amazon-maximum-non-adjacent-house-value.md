# [Maximum Non-Adjacent House Value](https://www.fastprep.io/problems/amazon-maximum-non-adjacent-house-value)

**Medium** | **NN minutes** | **Array, Dynamic Programming**

You are given an array values where values[i] is the amount available in the ith house arranged in a line.

You may choose any subset of houses, but you cannot choose two adjacent houses.

Return the maximum total value that can be collected.

## Examples

### Example 1

**Input:** `values = [6,7,1,3,8,2,4]`

**Output:** `19`

**Explanation:** Choose houses with values 7, 8, and 4 for a total of 19.

## Constraints

- `values contains the amount available in each house, with houses arranged in a line.`
- `values has at least one element.`
- `Each values[i] is a non-negative integer.`
- `You cannot choose two adjacent houses.`

## Solutions

Each house forces a binary choice, collect its value or skip it, and collecting it makes its neighbor off limits. The approaches below all encode that rule the same way, collecting from house `i` jumps the decision two houses back; they differ in how much repeated work the decisions cost.

### Brute Force

#### Derivation

The most direct reading walks the street once and, standing at each house, asks a question about everything before it: what is the most value collectible among houses `0..house_idx`? House `house_idx` is either skipped, in which case the answer is whatever house `house_idx - 1` allowed, or collected, in which case house `house_idx - 1` is off limits and the take is `values[house_idx]` plus whatever house `house_idx - 2` allowed:

1. Define `decide(house_idx)` as the most value collectible among houses
   `0..house_idx`, with `decide(house_idx) = 0` for every `house_idx < 0`
   (no houses, no value).
2. Skip branch: `decide(house_idx - 1)`, the best plan that ignores the house.
3. Collect branch: `values[house_idx] + decide(house_idx - 2)`, since
   collecting house `house_idx` silences its neighbor.
4. Return `max(skip, collect)`; the answer is `decide(len(values) - 1)`.

Nothing is remembered between calls, so the two branches re-decide the same shorter prefixes over and over: the call tree fans out two ways per level and the same subtree is grown once per route that reaches it.

#### Walkthrough

Trace the recursion on Example 1: `values = [6,7,1,3,8,2,4]`. The entry call is `decide(6)`; each call splits into its skip branch (`decide(house_idx - 1)`) and its collect branch (`values[house_idx] + decide(house_idx - 2)`), with `decide` returning `0` for negative indices. The full tree has `2^7 = 128` leaves, so the trace shows the top levels and the branches that win:

```text
decide(6)                    -> max(skip 15, 4 + decide(4) = 19) = 19
├─ skip: decide(5)           -> max(skip 15, 2 + decide(3) = 12) = 15
│   ├─ skip: decide(4)       -> max(skip 10, 8 + decide(2) = 15) = 15
│   │                        (this subtree is grown a second time below)
│   └─ collect: 2 + decide(3) = 12
└─ collect: 4 + decide(4)    -> 19
    decide(4)                -> max(skip 10, 8 + decide(2) = 15) = 15
    ├─ skip: decide(3)       -> max(skip 7, 3 + decide(1) = 10) = 10
    └─ collect: 8 + decide(2) = 15
        decide(2)            -> max(skip 7, 1 + decide(0) = 7) = 7
```

`decide(4)` was computed twice, once under `decide(5)`'s skip branch and once under `decide(6)`'s collect branch, and each copy regrew everything below it. The root keeps the larger branch, `4 + 15 = 19`, which collects houses with values `7`, `8`, and `4`, matching the expected Output of `19`. The example is small enough to afford the duplication; the tree doubles per house, which is the cost the next solution removes.

#### Solution

The code is the walkthrough's two branches around the negative-index base case.

```python
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        """Return the maximum total value collectible from non-adjacent houses.

        Time:  O(2^n): every house branches into collect or skip, and the
            same prefixes are re-decided once per route reaching them.
        Space: O(n): recursion depth along the deepest skip chain.
        """

        def decide(house_idx: int) -> int:
            if house_idx < 0:
                return 0
            skip = decide(house_idx - 1)
            collect = values[house_idx] + decide(house_idx - 2)
            return max(skip, collect)

        return decide(len(values) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each call forks into two more, so the call tree roughly doubles at every house; it grows like the Fibonacci numbers, which is exponential. Nothing is shared between the branches, so every route pays in full.

##### Space Complexity: `O(n)`

No table is kept, but the recursion stack reaches depth `n` along the deepest chain of skip branches.

#### Key Insights

- The two branches encode the whole constraint: collecting house `i` jumps the recursion to `i - 2`, skipping stays at `i - 1`, so no adjacency check is ever written.
- The negative-index base case folds both "no houses yet" and "house `0` has no two-back neighbor" into a single `0` return.
- The recursion is correct but recomputes each prefix once per route reaching it, which is the waste every later solution attacks.

### Top-Down Memoization

#### Derivation

The Brute Force re-decides the same prefixes relentlessly, yet `decide(house_idx)` depends on nothing but `house_idx`: every route that reaches a house gets the same answer. The repair is to [cache each prefix's result](https://en.wikipedia.org/wiki/Memoization) in a dictionary keyed by the house index, so the two routes into a house share one computation:

1. Keep `decide(house_idx)` verbatim from the Brute Force, base case included.
2. Before computing, check the `memo` dictionary and return a stored answer.
3. Otherwise compute
   `max(decide(house_idx - 1), values[house_idx] + decide(house_idx - 2))`
   and store it under key `house_idx` before returning.
4. Each house from `0` to `n - 1` now runs its body exactly once, so the tree
   collapses from `O(2^n)` nodes to `O(n)`.

#### Walkthrough

Trace the recursion on Example 1, `values = [6,7,1,3,8,2,4]`. The trace indents one level per call; marked lines are memo hits:

```text
decide(6)   miss -> recurse
  decide(5)   miss -> recurse
    decide(4)   miss -> recurse
      decide(3)   miss -> recurse
        decide(2)   miss -> recurse
          decide(1)   miss -> recurse
            decide(0)   miss -> recurse
              decide(-1) -> 0     base case
              decide(-2) -> 0     base case
            decide(0) -> 6        max(0, 6+0), memo[0] = 6
            decide(-1) -> 0       base case
          decide(1) -> 7          max(6, 7+0), memo[1] = 7
          decide(0) -> 6          ** memo hit **
        decide(2) -> 7            max(7, 1+6), memo[2] = 7
        decide(1) -> 7            ** memo hit **
      decide(3) -> 10             max(7, 3+7), memo[3] = 10
      decide(2) -> 7              ** memo hit **
    decide(4) -> 15               max(10, 8+7), memo[4] = 15
    decide(3) -> 10               ** memo hit **
  decide(5) -> 15                 max(15, 2+10), memo[5] = 15
  decide(4) -> 15                 ** memo hit **
decide(6) -> 19                   max(15, 4+15), memo[6] = 19
```

Every collect branch reaches two houses back and finds the prefix already decided: house `2`'s collect reuses the stored `decide(0)`, house `6`'s collect reuses the stored `decide(4)` that the skip branch grew in full. Each stored value runs its body exactly once, and the call returns `19`, matching the expected Output for Example 1.

#### Solution

The code is the Brute Force recursion with the memo check and store wrapped around the split.

```python
from typing import Dict, List


class Solution:
    def solve(self, values: List[int]) -> int:
        """Return the maximum total value collectible from non-adjacent houses.

        Time:  O(n): each house enters the body exactly once; every other
            call is a dictionary hit.
        Space: O(n): the memo stores one entry per house, on top of the
            recursion stack.
        """
        memo: Dict[int, int] = {}

        def decide(house_idx: int) -> int:
            if house_idx < 0:
                return 0
            if house_idx in memo:
                return memo[house_idx]

            memo[house_idx] = max(
                decide(house_idx - 1),
                values[house_idx] + decide(house_idx - 2),
            )
            return memo[house_idx]

        return decide(len(values) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each house from `0` to `n - 1` enters the body exactly once and does constant work combining two already-known values; every other call is a dictionary hit.

##### Space Complexity: `O(n)`

The memo stores one entry per house, and the recursion stack reaches depth `n` along the deepest skip chain.

#### Key Insights

- The dictionary is keyed by the house index alone, which works because the prefix through a house fully determines the answer: no other state exists.
- Writing the check-compute-store cycle by hand shows the mechanism a decorator would hide; `functools.cache` collapses those three lines, see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).
- Memoization converts the exponential tree into linear time without touching the recursion's shape, which makes the correctness argument easy to carry over.

### Bottom-Up DP

#### Derivation

The memoized recursion still starts at the last house and unwinds all the way down to the empty prefix before producing its first useful value, paying call overhead and stack depth along the way. Watch the order its memo actually fills: `decide(0)` first, then `decide(1)`, then onward toward the street's end. [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) with tabulation produces that same table in that same order with a plain loop and no recursion at all:

1. Let `dp[house_idx]` be the most value collectible among houses
   `0..house_idx`, matching `decide(house_idx)` exactly.
2. Seed the base cases `dp[0] = values[0]` and
   `dp[1] = max(values[0], values[1])`.
3. Apply `dp[house_idx] = max(dp[house_idx - 1], dp[house_idx - 2] +
   values[house_idx])` left to right.
4. Return `dp[n - 1]`, the best plan over the whole street.

A street of one house never reaches step 3, and `dp[1]` would index out of bounds, so the single-house street returns `values[0]` directly.

#### Recurrence

Let `dp[house_idx]` be the most value collectible among houses `0..house_idx`:

$$ dp[i] = \begin{cases} \text{values}[0], & i = 0 \\[4pt] \max(\text{values}[0],\ \text{values}[1]), & i = 1 \\[4pt] \max(dp[i-1],\ dp[i-2] + \text{values}[i]), & i \ge 2 \end{cases} $$

```text
dp[0] = values[0]
dp[1] = max(values[0], values[1])
dp[i] = max(dp[i - 1], dp[i - 2] + values[i])   for i >= 2
```

The base cases are the recurrence applied to the two virtual entries `dp[-1] = dp[-2] = 0`: with no houses before the street's start, skipping house `0` is worth nothing and collecting it banks `values[0]`. The answer is read from the last entry, `dp[n - 1]`.

#### Walkthrough

Let us fill the table on Example 1: `values = [6,7,1,3,8,2,4]`. Each entry combines the two just below it:

```text
start    dp = [6, 0, 0, 0, 0, 0, 0]     dp[0] = values[0] = 6
i = 1    dp[1] = max(6, 7) = 7          dp = [6, 7, 0, 0, 0, 0, 0]
i = 2    dp[2] = max(7, 6+1) = 7        dp = [6, 7, 7, 0, 0, 0, 0]
i = 3    dp[3] = max(7, 7+3) = 10       dp = [6, 7, 7, 10, 0, 0, 0]
i = 4    dp[4] = max(10, 7+8) = 15      dp = [6, 7, 7, 10, 15, 0, 0]
i = 5    dp[5] = max(15, 10+2) = 15     dp = [6, 7, 7, 10, 15, 15, 0]
i = 6    dp[6] = max(15, 15+4) = 19     dp = [6, 7, 7, 10, 15, 15, 19]
```

At `i = 2` the collect branch only ties: `dp[0] + 1 = 7` equals `dp[1] = 7`, so house `1` alone and houses `0` and `2` are equally good openings, a fact the final answer absorbs either way. At `i = 4` the collect branch wins outright: `dp[2] + 8 = 15` beats `dp[3] = 10`, and at `i = 6` the same shape repeats with `dp[4] + 4 = 19`. The method returns `dp[6] = 19`, matching the expected Output for Example 1.

#### Solution

The code is the table fill from the walkthrough: seed two base cases, then loop the recurrence upward.

```python
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        """Return the maximum total value collectible from non-adjacent houses.

        Time:  O(n): one pass seeds the base cases and one pass applies the
            recurrence, constant work per house.
        Space: O(n): the dp table stores one entry per house.
        """
        house_count = len(values)
        if house_count == 1:
            return values[0]

        dp = [0] * house_count
        dp[0] = values[0]
        dp[1] = max(values[0], values[1])

        for house_idx in range(2, house_count):
            dp[house_idx] = max(
                dp[house_idx - 1], dp[house_idx - 2] + values[house_idx]
            )

        return dp[house_count - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass seeds the base cases and one pass applies the recurrence, constant work per house.

##### Space Complexity: `O(n)`

The `dp` table stores one entry per house.

#### Key Insights

- The table is the memo turned upright: same entries, same values, filled in the order the recursion used to discover them.
- The explicit table needs a `house_count == 1` guard because `dp[1]` must exist before the loop; the rolling version below folds the base cases into its seeds and needs none.
- Having every prefix's answer on hand is what makes variants answerable (for example, the best plan over any sub-street), which is worth the array when extra queries exist.

### Space-Optimized DP

#### Derivation

The table loop reads only the two entries just below the one it writes: `dp[house_idx - 1]` and `dp[house_idx - 2]`. Everything older is dead weight, so the whole array collapses into two rolling totals, `two_back` standing in for `dp[house_idx - 2]` and `one_back` for `dp[house_idx - 1]`. Seeding both at `0` installs the recurrence's virtual entries `dp[-1] = dp[-2] = 0`, which folds the base cases into the loop and removes the single-house guard:

1. Start with `two_back = 0` and `one_back = 0`, the values before the first
   house.
2. For each house's `house_value`, compute
   `best_here = max(one_back, two_back + house_value)`: skip the house and
   keep `one_back`, or collect it and add to `two_back`.
3. Shift the window: `two_back = one_back`, then `one_back = best_here`.
4. After the last house, `one_back` holds the answer.

#### Walkthrough

Let us roll the two totals through Example 1: `values = [6,7,1,3,8,2,4]`. Before each house, `one_back` holds the best through the previous house and `two_back` the best through the house before that:

```text
start         two_back = 0    one_back = 0
values[0]=6   best_here = max(0, 0+6) = 6     -> two_back = 0,  one_back = 6
values[1]=7   best_here = max(6, 0+7) = 7     -> two_back = 6,  one_back = 7
values[2]=1   best_here = max(7, 6+1) = 7     -> two_back = 7,  one_back = 7
values[3]=3   best_here = max(7, 7+3) = 10    -> two_back = 7,  one_back = 10
values[4]=8   best_here = max(10, 7+8) = 15   -> two_back = 10, one_back = 15
values[5]=2   best_here = max(15, 10+2) = 15  -> two_back = 15, one_back = 15
values[6]=4   best_here = max(15, 15+4) = 19  -> two_back = 15, one_back = 19
```

Each row reproduces exactly one `dp` entry from the Bottom-Up walkthrough: `best_here` is `dp[house_idx]`, computed from `dp[house_idx - 1]` and `dp[house_idx - 2]` before the shift renames them. After the last house `one_back` holds `dp[6] = 19`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's three lines per house: combine, then shift the window.

```python
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        """Return the maximum total value collectible from non-adjacent houses.

        Time:  O(n): one pass over the houses with constant work each.
        Space: O(1): two rolling totals, regardless of street length.
        """
        two_back = 0
        one_back = 0
        for house_value in values:
            best_here = max(one_back, two_back + house_value)
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
- Seeding both totals at `0` is sound because house values are non-negative: the `max` then never prefers a negative take, and the virtual `dp[-1] = dp[-2] = 0` entries behave exactly like the table's base cases.
- This is the optimal trade for the single-query problem: the explicit table buys reusable per-prefix answers that this version deliberately gives up.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution stacks two separate things: the collect-or-skip recurrence, and a dictionary that stops the recursion from recomputing a prefix it has already answered. Only the first is the algorithm. The second is pure bookkeeping, and the standard library already implements it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the recurrence and its base case stay on the page exactly as the Brute Force wrote them:

1. Keep `decide(house_idx)` verbatim from the Brute Force: return `0` for
   `house_idx < 0`, otherwise return
   `max(decide(house_idx - 1), values[house_idx] + decide(house_idx - 2))`.
2. Decorate it with `@cache`, so each distinct index runs the body at most
   once and every later request for that prefix is answered from the cache.
3. Delete the three bookkeeping lines the decorator now owns: the
   `memo = {}` declaration, the `if house_idx in memo` lookup, and the
   `memo[house_idx] = ...` store.
4. Because `decide` is defined inside `solve`, each call builds a fresh
   function object with a fresh cache, so nothing leaks between inputs; a
   `@cache` on a method or a module-level function would instead live for
   the whole process.

One behavioural difference follows from where the decorator sits. The hand-rolled version answers `house_idx < 0` before it ever consults `memo`, so the base-case keys are never stored; `@cache` wraps the entire body, so the negative indices are cached like any other house.

#### Walkthrough

Run it on Example 1, `values = [6,7,1,3,8,2,4]`. The trace follows the first descent and the returns back up, noting whether the decorator ran the body or answered from the cache:

```text
decide(6)   miss, run the body
  decide(5)   miss, run the body
    decide(4)   miss, run the body
      decide(3)   miss, run the body
        decide(2)   miss, run the body
          decide(1)   miss, run the body
            decide(0)   miss, run the body
              decide(-1) -> 0   base case, cached under key -1
              decide(-2) -> 0   base case, cached under key -2
            decide(0) -> 6      max(0, 6+0), cached under key 0
          decide(1) -> 7        max(6, 7+0), cached under key 1
          decide(0) -> 6        ** cache hit, the body does not run **
        decide(2) -> 7          max(7, 1+6), cached under key 2
        decide(1) -> 7          ** cache hit, the body does not run **
      decide(3) -> 10           max(7, 3+7), cached under key 3
      decide(2) -> 7            ** cache hit, the body does not run **
    decide(4) -> 15             max(10, 8+7), cached under key 4
    decide(3) -> 10             ** cache hit, the body does not run **
  decide(5) -> 15               max(15, 2+10), cached under key 5
  decide(4) -> 15               ** cache hit, the body does not run **
decide(6) -> 19                 max(15, 4+15), cached under key 6
```

The decisive hit is the last one: `decide(6)`'s collect branch requests `decide(4)`, which the skip branch already computed in full, so the entire subtree below house `4` is answered with one dictionary lookup. The outer call returns `19`, matching the expected Output for Example 1.

#### Solution

The Brute Force recursion, unchanged, with one decorator standing in for the memo dictionary.

```python
from functools import cache
from typing import List


class Solution:
    def solve(self, values: List[int]) -> int:
        """Return the maximum total value collectible from non-adjacent houses.

        Time:  O(n): the cache admits each house into the body exactly once.
        Space: O(n): the decorator's cache holds one entry per distinct
            argument, plus the recursion stack.
        """

        @cache
        def decide(house_idx: int) -> int:
            if house_idx < 0:
                return 0
            return max(
                decide(house_idx - 1),
                values[house_idx] + decide(house_idx - 2),
            )

        return decide(len(values) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The cache admits each house from `0` to `n - 1` into the body exactly once, and each admission does one addition and one max of two already-known values; every other call is a dictionary lookup on a small integer key.

##### Space Complexity: `O(n)`

The decorator's cache holds one entry per distinct argument, the `n` houses plus the two negative base-case keys, and the recursion descends to depth `n` before the first value returns.

#### Key Insights

- The algorithm is untouched: the recurrence and the base case read exactly as they do in the Brute Force, which makes plain that memoization is an execution strategy rather than a change to the recursion.
- `@cache` keys on the argument tuple, so it is a drop-in replacement only when the arguments are hashable and the function is genuinely pure; `decide` reads nothing but `house_idx` and `values`, which is what licenses the substitution.
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

- **Brute Force**: the direct transcription of the collect-or-skip rule and needs no auxiliary structure, but its exponential branching makes it unusable beyond a dozen or so houses.
- **Top-Down Memoization** and **Top-Down Memoization with functools.cache**: keep the recursion's shape, which makes correctness easy to argue, at the price of stack depth `n` on top of the memo.
- **Bottom-Up DP**: pays the same linear time without recursion and keeps every prefix's answer, which matters only when those answers are queried again later.
- **Space-Optimized DP**: gives up random access to old prefixes and keeps just the two live entries, reaching constant space with no new risk.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for checking the faster versions on small streets.
- **Top-Down Memoization**: when the recurrence is easiest to trust in its recursive form and streets stay modest.
- **Bottom-Up DP**: when the per-prefix answers are reused by follow-up queries or variants of the problem.
- **Space-Optimized DP (Recommended)**: the default; the same linear pass at constant space, with the base cases folded into the seeds so no edge-case guard remains.
- **Top-Down Memoization with functools.cache**: the Pythonic tidy-up when the recursive shape is wanted and the memo should not be hand-maintained.

### Optimization Notes

- The two-lookback window is not an approximation: collecting house `i` can never combine with houses older than `i - 2` directly, because anything older is already folded into the best total through `i - 2`, which is why two rolling slots suffice for any street length.
- The rolling seeds `two_back = one_back = 0` lean on the problem's guarantee that values are non-negative; with negative amounts allowed, the recurrence and its base cases would need a second look.
- The memoized versions recurse to depth `n`, so very long streets approach Python's default recursion limit; the iterative table or the rolling totals avoid the stack entirely.
- The same prefix recurrence, read backwards, drives the circular-street variant where the first and last houses are neighbors: that variant has to break the circle by fixing the first house's fate and running the linear pass twice.
