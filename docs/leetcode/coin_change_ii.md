# [Coin Change II](https://leetcode.com/problems/coin-change-ii/)

**Medium** | **25 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP Knapsack/Subset](../patterns/dp_knapsack_subset/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization)

**Practice:** [`practice/coin_change_ii/solution.py`](../../practice/coin_change_ii/solution.py)

You are given an integer array `coins` representing coins of different denominations (e.g. 1 dollar, 5 dollars, etc) and an integer `amount` representing a target amount of money.

Return the number of distinct combinations that total up to `amount`. If it's impossible to make up the amount, return `0`.

You may assume that you have an unlimited number of each coin and that each value in `coins` is unique.

## Examples

### Example 1

**Input:** `amount = 4, coins = [1,2,3]`

**Output:** `4`

**Explanation:** * 1+1+1+1 = 4
* 1+1+2 = 4
* 2+2 = 4
* 1+3 = 4

### Example 2

**Input:** `amount = 7, coins = [2,4]`

**Output:** `0`

## Constraints

- `1 <= coins.length <= 100`
- `1 <= coins[i] <= 5000`
- `0 <= amount <= 5000`

## Deriving the Solution

A combination is a multiset of coins whose values sum to `amount`: order carries no information, so `[1, 2, 1]` and `[2, 1, 1]` are one combination. Every solution below walks the denominations in a fixed order and, for each, decides how many copies join the combination; the difference between counting combinations and counting permutations is exactly whether the coin order is allowed to vary.

1. **Start literal.** Walk the coin list with an index and a remaining amount,
   deciding at each coin to skip it forever or take it and stay. The recursion
   tree has two branches per decision and costs `O(2^(amount / min(coins)))`:
   see [Recursive Enumeration](#recursive-enumeration).
2. **Cache the states.** A branch's answer depends only on `(coin index,
   remaining amount)`, never on the coins already taken, so the same few
   states are re-derived countless times. Memoizing them collapses the tree
   to one solve per state: see [Top-Down Memoization](#top-down-memoization).
3. **Tabulate the states.** The pairs form a table with one row per coin
   prefix and one column per amount, each cell reading only the row above
   and cells to its left in the same row. Filling row by row needs no
   recursion: see [Bottom-Up 2-D DP](#bottom-up-2-d-dp).
4. **Keep one row.** Each cell needs the row above and earlier cells of the
   current row, so a single row updated in place carries the whole table:
   `O(amount)` space, same time: see
   [Space-Optimized 1-D DP](#space-optimized-1-d-dp).
5. **Hand the cache to the library.** Step 2's memo dict is bookkeeping, not
   logic. Decorating the recursion with `functools.cache` deletes the lookup
   and the store while the two base cases and the skip/take sum stay exactly
   as written: see
   [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Recursive Enumeration

#### Derivation

The most literal reading of "count the combinations" builds them coin by coin. Fix an order on the coins and process them by index: at each coin, either it appears no more (skip to the next index) or one more copy joins the combination (take it and stay at the same index, since copies are unlimited). The remaining amount is the only other thing the future depends on:

1. Define `dfs(i, remaining)` as the number of combinations using only coins
   `i..` that total `remaining`.
2. Return `1` when `remaining == 0` (the combination is complete).
3. Return `0` when `remaining < 0` (overdrawn) or `i == len(coins)` (no
   denominations left).
4. Otherwise return `dfs(i + 1, remaining) + dfs(i, remaining - coins[i])`:
   skip the coin, or take one more copy of it.
5. Return `dfs(0, amount)`.

The fixed coin order is what keeps each multiset counted once: a combination can only use coins in index order, so its coin sequence is unique.

#### Walkthrough

The full tree on Example 1 (`amount = 4, coins = [1,2,3]`) has 35 nodes, most of them dead ends (`remaining < 0` or the coin list exhausted). Listing only the branches that reach `remaining == 0`, in the order the recursion discovers them, shows the four combinations:

```text
take 1, take 1, take 1, take 1            -> remaining 0: [1, 1, 1, 1]
take 1, take 1, take 2                    -> remaining 0: [1, 1, 2]
take 1, take 3                            -> remaining 0: [1, 3]
take 2, take 2                            -> remaining 0: [2, 2]
```

Each hit contributes `1`, and every other path dies at an overdrawn amount or a coin index past the end, so the root sums its children to `4`, matching the expected Output for Example 1. Example 2 (`amount = 7, coins = [2,4]`) never reaches `remaining == 0`: every path either lands on an odd remaining amount that no even coin can finish or overdraws, so the root sums to `0`.

#### Solution

The code is the walkthrough's decision tree: one skip/take fork per state, two base rules.

```python
from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        def dfs(i: int, remaining: int) -> int:
            if remaining == 0:
                return 1
            if remaining < 0 or i == len(coins):
                return 0
            # Skip coin i forever, or take one more copy of it
            return dfs(i + 1, remaining) + dfs(i, remaining - coins[i])

        return dfs(0, amount)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^(amount / min(coins)))`

Each level of the tree either advances the coin index or consumes at least the smallest coin from `remaining`, so the depth is bounded by `len(coins) + amount / min(coins)`; with two branches per interior node the tree grows exponentially in that bound.

##### Space Complexity: `O(amount / min(coins))`

The recursion stack: at most one frame per take along the current branch plus one per skipped denomination.

#### Key Insights

- Transcribes the counting rule directly: skip a coin for good, or take
  another copy. Correctness needs no insight beyond the rules.
- Processing coins by index (rather than trying every coin at every step) is
  what counts combinations instead of permutations: `[1, 2]` can only appear
  as take `1`, then take `2`.
- The same `(i, remaining)` states are re-derived across different
  combination prefixes, which is the waste the next solution removes.

### Top-Down Memoization

#### Derivation

The enumeration re-solves futures it has already seen: after `take 1, take 1` and after `take 2`, the state is the same `(coin index 0, remaining 2)`, yet the tree walks everything that follows twice. A branch's future depends only on `(i, remaining)`, never on the coins already chosen, so each pair is a [memoizable](https://en.wikipedia.org/wiki/Memoization) state with `len(coins) × (amount + 1)` of them at most:

1. Keep the enumeration's recursion unchanged.
2. Add a `memo` keyed by `(i, remaining)`; check it on entry and store before
   every return.

#### Walkthrough

Trace the full recursion with hits marked on Example 1: `amount = 4, coins = [1,2,3]`. `skip` is the child at the next index, `take` the child that stays:

```text
dfs(0, 4)
  dfs(1, 4)
    dfs(2, 4)
      dfs(3, 4) -> 0        base: coins exhausted
      dfs(2, 1)
        dfs(3, 1) -> 0      base
        dfs(2, -2) -> 0     base
      dfs(2, 1) -> 0        stored
    dfs(2, 4) -> 0          stored
    dfs(1, 2)
      dfs(2, 2) -> 0        stored
      dfs(1, 0) -> 1        base: amount met      [1, 2]
    dfs(1, 2) -> 1          stored
  dfs(1, 4) -> 1             stored
  dfs(0, 3)
    dfs(1, 3)
      dfs(2, 3) -> 1         stored                [1, 3]... via dfs(2, 0)
      dfs(1, 1)
        dfs(2, 1) -> 0       ** memo hit **
        dfs(1, -1) -> 0      base
      dfs(1, 1) -> 0         stored
    dfs(1, 3) -> 1           stored
    dfs(0, 2)
      dfs(1, 2) -> 1         ** memo hit **
      dfs(0, 1)
        dfs(1, 1) -> 0       ** memo hit **
        dfs(0, 0) -> 1       base: amount met      [1, 1, 1, 1]
      dfs(0, 1) -> 1         stored
    dfs(0, 2) -> 2           stored                [2, 2] + [1, 1, 2]
  dfs(0, 3) -> 3             stored
dfs(0, 4) -> 4               stored
```

Three repeat arrivals are answered from the memo: `dfs(2, 1)` (reached once after taking `3`, once after taking `1` then `2`), `dfs(1, 2)` (after taking `2`, after taking `1, 1`), and `dfs(1, 1)` (after taking `2`, after taking `1, 1, 1`). Only 12 states are computed against the brute tree's 35 nodes. The root sums to `4`, matching the expected Output for Example 1; Example 2 computes `0` for every reachable state and returns `0`.

#### Solution

The code is the enumeration with a dict in front of it.

```python
from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        memo = {}

        def dfs(i: int, remaining: int) -> int:
            if remaining == 0:
                return 1
            if remaining < 0 or i == len(coins):
                return 0
            if (i, remaining) in memo:
                return memo[(i, remaining)]
            memo[(i, remaining)] = dfs(i + 1, remaining) + dfs(
                i, remaining - coins[i]
            )
            return memo[(i, remaining)]

        return dfs(0, amount)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(len(coins) × amount)`

At most one solve per distinct `(i, remaining)` state, constant work each; the negative-`remaining` and exhausted-index exits are constant per parent.

##### Space Complexity: `O(len(coins) × amount)`

The memo's entries plus a recursion stack of up to `len(coins) + amount / min(coins)` frames.

#### Key Insights

- The state `(i, remaining)` is a complete summary of the past: which coins
  were taken and how many copies cannot change the future.
- The `remaining == 0` and `remaining < 0` base cases stay outside the memo:
  they are constant, so caching them saves nothing.
- Memoization keeps the skip/take shape of the enumeration, which makes the
  correctness argument ("each multiset counted once, in coin order") carry
  over unchanged.

### Bottom-Up 2-D DP

#### Derivation

The memoized recursion still asks from the top: "how many combinations do coins `i..` make for `remaining`?". Flip it: build a table `dp` where `dp[i][a]` is the number of combinations using only the first `i` coins that total `a`. Row 0 says the empty coin set makes `0` in exactly one way and nothing else; each interior cell copies the count without coin `i` and adds the counts of the amounts `a - coins[i - 1]` reachable while still allowed to use coin `i`. Filling row by row, top to bottom, left to right, never reads a cell that is not ready:

1. Allocate `dp` of size `(len(coins) + 1) x (amount + 1)`; set `dp[0][0] = 1`
   and the rest of row 0 to `0`.
2. For each coin index `i` in `1..len(coins)`, with `coin = coins[i - 1]`, and
   each amount `a` in `0..amount`:
   - `dp[i][a] = dp[i - 1][a]` (skip the coin),
   - plus `dp[i][a - coin]` when `a >= coin` (take one more copy).
3. Return `dp[len(coins)][amount]`.

The `- 1` offsets exist because the table counts coin prefixes while the list is position-indexed: row `i` decides with `coins[i - 1]`.

#### Walkthrough

Trace the fill on Example 1: `amount = 4, coins = [1,2,3]`. Rows are coin prefixes, columns are amounts `0..4`:

```text
            ''   a=0  a=1  a=2  a=3  a=4
  (none)         1    0    0    0    0
  coin 1         1    1    1    1    1
  coin 2         1    1    2    2    3
  coin 3         1    1    2    3    4
```

Row `coin 1` marks the single all-ones combination for every amount; row `coin 2` gets `dp[2][2] = dp[1][2] + dp[2][0] = 1 + 1 = 2` (`[1,1]` and `[2]`) and `dp[2][4] = 1 + dp[2][2] = 3` (`[1,1,1,1]`, `[1,1,2]`, `[2,2]`); row `coin 3` adds the `[1,3]` combination at `a = 4` for `dp[3][4] = 3 + dp[3][1] = 3 + 1 = 4`. The bottom-right cell is `4`, matching the expected Output for Example 1. Example 2's table stays `0` in every column except `a = 0`, so it returns `0`.

#### Solution

The code is the row-by-row fill of the walkthrough's table.

```python
from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        rows, cols = len(coins) + 1, amount + 1
        dp = [[0] * cols for _ in range(rows)]
        dp[0][0] = 1
        for i in range(1, rows):
            coin = coins[i - 1]
            for a in range(cols):
                dp[i][a] = dp[i - 1][a]
                if a >= coin:
                    dp[i][a] += dp[i][a - coin]
        return dp[rows - 1][cols - 1]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(len(coins) × amount)`

One copy plus one conditional add per table cell.

##### Space Complexity: `O(len(coins) × amount)`

The full table.

#### Key Insights

- The take branch reads the current row (`dp[i][a - coin]`), not the row
  above: unlimited copies are one cell of indirection.
- The column sweep runs left to right precisely so that `dp[i][a - coin]` is
  already updated when read.
- Row 0's single `1` at amount `0` encodes "the empty combination makes zero"
  and seeds every other count.

### Space-Optimized 1-D DP

#### Derivation

Cell `(i, a)` reads only `dp[i - 1][a]` and `dp[i][a - coin]`: the cell above and an earlier cell of the same row. Row `i - 1` in older generations is dead weight, so the whole table collapses to one row `dp` updated in place, where `dp[a]` counts the combinations of the coins processed so far that make `a`. Sweeping `a` left to right makes `dp[a - coin]` already include the current coin, which is exactly the take branch; `dp[a]`'s old value is the skip branch:

1. Initialize `dp` of size `amount + 1` with `dp[0] = 1`.
2. For each `coin`, sweep `a` from `coin` through `amount`, updating
   `dp[a] += dp[a - coin]`.
3. Return `dp[amount]`.

Processing one coin per full sweep is what separates combinations from permutations: a combination is built in coin order, so `[1, 2]` and `[2, 1]` cannot both occur.

#### Recurrence

Let \(dp_k[a]\) be the number of combinations of the first `k` coins summing to `a`:

$$ dp_k[a] = dp_{k-1}[a] + dp_k[a - \text{coins}[k-1]], \qquad dp_0[0] = 1,\ dp_0[a \neq 0] = 0 $$

```text
dp_0[0] = 1, dp_0[a] = 0 for a != 0
dp_k[a] = dp_(k-1)[a] + dp_k[a - coins[k - 1]]
          (second term only when a >= coins[k - 1])
```

The take term reads row `k`, not row `k - 1`: taking another copy of the current coin must stay available. Sweeping `a` upward inside one row produces exactly that; sweeping downward would turn the same loop into the 0/1 knapsack, where each coin may be used once. The answer is \(dp_K[\text{amount}]\) after all `K` coins.

#### Walkthrough

Trace the single row on Example 1: `amount = 4, coins = [1,2,3]`:

```text
start       dp = [1, 0, 0, 0, 0]
coin 1      dp = [1, 1, 1, 1, 1]
coin 2      dp = [1, 1, 2, 2, 3]
coin 3      dp = [1, 1, 2, 3, 4]
```

Each sweep is the corresponding table row of the Bottom-Up 2-D DP, built in place. During the `coin 2` sweep, `dp[2]` reads the already-updated `dp[0] = 1` (take two 2s) on top of the old `dp[2] = 1` (`[1,1]`), and `dp[4]` later reads the new `dp[2] = 2`, producing `3`. The final `dp[amount]` is `4`, matching the expected Output for Example 1; Example 2's sweeps never touch odd amounts and the final `dp[7]` stays `0`.

#### Solution

The code is the walkthrough's sweeps: one left-to-right pass per coin.

```python
from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1
        for coin in coins:
            for a in range(coin, amount + 1):
                dp[a] += dp[a - coin]
        return dp[amount]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(len(coins) × amount)`

One add per (coin, amount) pair, exactly as in the full table.

##### Space Complexity: `O(amount)`

The single row.

#### Key Insights

- The loop order is the algorithm: coins outer, amounts ascending inner
  counts combinations; amounts outer, coins inner would count permutations
  (`[1,2]` and `[2,1]` as different).
- The ascending inner sweep is the one-line difference from 0/1 knapsack
  (Partition Equal Subset Sum's descending sweep), because the take branch
  must read the current coin's row.
- `dp[0] = 1` says the empty combination is the one way to make `0`, and it
  is the seed every take branch ultimately chains back to.

### Top-Down Memoization with functools.cache

#### Derivation

Step 2's memo is not part of the recurrence. The dict, the membership test, and the store all exist to remember what `dfs(i, remaining)` returned, which is precisely what [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) does around any pure function. Decorating the recursion deletes all three pieces of bookkeeping and leaves the base cases and the skip/take sum untouched:

1. Keep the memoized recursion's structure: the same two base cases, the same
   skip/take sum.
2. Replace the `memo` dict with `@cache` on `dfs`, keyed automatically by the
   arguments `(i, remaining)`.
3. Return `dfs(0, amount)`.

The one behavioral cost: `@cache` also stores the constant base-case results and keeps every pair alive for the life of the process, so the memory profile matches or slightly exceeds the dict version.

#### Walkthrough

Trace the decorated recursion on Example 1: `amount = 4, coins = [1,2,3]`. The call sequence is identical to the Top-Down Memoization walkthrough; the only difference is where a repeat lookup lands:

```text
dfs(0, 4) -> dfs(1, 4) + dfs(0, 3)
  ... identical descent ...
dfs(2, 1) -> 0                       ** cached: no recompute **
dfs(1, 2) -> 1                       ** cached: no recompute **
dfs(1, 1) -> 0                       ** cached: no recompute **
dfs(0, 4) -> 4
```

22 distinct `(i, remaining)` calls are cached (the dict version stored only the 12 non-base states), each of the 3 repeat arrivals is a hit, and the answer is `4`, matching the expected Output for Example 1.

#### Solution

The code is the memoized recursion with the dict replaced by the decorator.

```python
from functools import cache
from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        @cache
        def dfs(i: int, remaining: int) -> int:
            if remaining == 0:
                return 1
            if remaining < 0 or i == len(coins):
                return 0
            return dfs(i + 1, remaining) + dfs(i, remaining - coins[i])

        return dfs(0, amount)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(len(coins) × amount)`

The cache admits each `(i, remaining)` pair once; the body is constant work.

##### Space Complexity: `O(len(coins) × amount)`

The decorator's cache plus the recursion stack.

#### Key Insights

- `functools.cache` is the dict-based memo with the ceremony removed: same
  asymptotics, three fewer lines, no key-tuple mistakes.
- Unlike the dict version it also caches the base cases, harmless here
  because there are only two distinct results (`0` and `1`).
- The recursion body is the recurrence in its purest form, which makes this
  the version to quote in an interview after sketching the skip/take idea.

## Comparison of Solutions

### Time Complexity

- **Recursive Enumeration**: `O(2^(amount / min(coins)))` - the full decision tree.
- **Top-Down Memoization**: `O(len(coins) × amount)` - one solve per state.
- **Bottom-Up 2-D DP**: `O(len(coins) × amount)` - one update per cell.
- **Space-Optimized 1-D DP**: `O(len(coins) × amount)` - the same cells, one row at a time.
- **Top-Down Memoization with functools.cache**: `O(len(coins) × amount)` - the dict memo with library bookkeeping.

### Space Complexity

- **Recursive Enumeration**: `O(amount / min(coins))` - the recursion stack.
- **Top-Down Memoization**: `O(len(coins) × amount)` - the memo dict plus the stack.
- **Bottom-Up 2-D DP**: `O(len(coins) × amount)` - the full table.
- **Space-Optimized 1-D DP**: `O(amount)` - the single row.
- **Top-Down Memoization with functools.cache**: `O(len(coins) × amount)` - the decorator's cache plus the stack.

### Trade-offs

- Enumeration is the definitional baseline; exponential time makes it a
  correctness oracle rather than a solution.
- The memoized recursions carry a call stack and an `O(len(coins) × amount)` cache;
  the table versions trade the stack for an evaluation order.
- The one-row table is the production form: same time as everything else at
  linear memory.

### When to Use Each

- **Recursive Enumeration**: tiny inputs, or as the brute-force oracle when
  checking the DP versions.
- **Top-Down Memoization**: when deriving the recurrence live; the skip/take
  structure writes itself from the counting rules.
- **Bottom-Up 2-D DP**: when the full table matters, for example to read off
  which coins a count came from by walking backward.
- **Space-Optimized 1-D DP**: the answer to the problem as stated
  (recommended here).
- **Top-Down Memoization with functools.cache**: Python code that wants the
  memoized recursion without the dict ceremony.

### Optimization Notes

- The inner sweep starts at `coin`, not `0`: amounts below the coin cannot
  take another copy, and the skip branch is the value already in `dp[a]`.
- This problem is the unbounded twin of Partition Equal Subset Sum: flipping
  the inner sweep's direction (ascending here, descending there) is the
  entire difference between unlimited copies and use-once.
- Counts fit comfortably in Python's arbitrary-precision integers; in
  fixed-width languages the worst case is large (229 bits for
  `coins = [1..100]`, `amount = 5000`), so 32-bit counts overflow.
