# [Coin Change](https://leetcode.com/problems/coin-change/)

**Medium** | **25 minutes** | **Dynamic Programming**

**Pattern:** [DP Knapsack/Subset](../patterns/dp_knapsack_subset/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/coin_change/solution.py`](../../practice/coin_change/solution.py)

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.

You may assume that you have an infinite number of each kind of coin.

## Examples

### Example 1

**Input:** `coins = [1,3,4]`, `amount = 6`

**Output:** `2`

**Explanation:** The answer is `2` because `6 = 3 + 3`.

### Example 2

**Input:** `coins = [2]`, `amount = 3`

**Output:** `-1`

### Example 3

**Input:** `coins = [1]`, `amount = 0`

**Output:** `0`

## Constraints

- `1 <= coins.length <= 12`
- `1 <= coins[i] <= 2^31 - 1`
- `0 <= amount <= 10^4`

## Deriving the Solution

The fewest coins for an amount contains a smaller copy of itself: whichever coin is chosen last, the remaining coins must make `amount - coin` as cheaply as possible. Every solution below exploits this optimal substructure; they differ in how much repeated work they spend exploring it.

1. **Start literal.** Ask recursively: for the remaining amount, try every coin,
   solve what each choice leaves behind, and keep the cheapest branch. Correct, but the same remaining amounts are re-solved across countless branches, costing `O(coins.length^amount)`: see [Brute Force Recursion](#brute-force-recursion).
2. **Cache the repeats.** The answer for a remaining amount does not depend on
   how the recursion reached it, so store each amount's answer the first time it is computed and serve every revisit from the cache. Work collapses to one computation per distinct amount, `O(amount × coins.length)`: see [Top-Down Memoization](#top-down-memoization).
3. **Flip the direction.** The cached recursion still burns one stack frame per
   coin subtracted, which can reach `amount` frames. Building a table upward from `dp[0]` computes the same values iteratively, with no recursion at all: see [Bottom-Up DP](#bottom-up-dp).
4. **Reframe as a shortest path.** A lateral alternative: treat every amount as a
   node and every coin as a unit-weight edge, so "fewest coins" becomes "fewest edges" from `0` to `amount`, which breadth-first search finds level by level: see [BFS](#bfs).
5. **Hand the cache to the library.** Step 2's memo is not part of the
   recurrence, only a dictionary bolted onto it. Decorating the brute-force function with `functools.cache` deletes the lookup and the store while leaving the coin loop and both base cases untouched, at the price of also caching the negative amounts the guard rejects: see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force Recursion

#### Derivation

The most literal reading of the problem is a question that answers itself recursively: what is the fewest number of coins making `remaining_amount`? If some coin is used, the rest of the coins must make `remaining_amount - coin`, so try every coin and keep the cheapest branch. This naive [recursive](https://en.wikipedia.org/wiki/Recursion_(computer_science)) approach explores all possible combinations of coins with no cleverness at all:

1. Define `backtrack(remaining_amount)` as the fewest coins making that amount,
   or `-1` when it cannot be made.
2. Base cases: an amount of `0` needs `0` coins; a negative amount means the last
   coin overshot, so return `-1`.
3. Otherwise try each `coin`: recurse on `remaining_amount - coin`, and whenever
   the branch is possible (`result != -1`), fold `1 + result` into `min_coins`.
4. Return `min_coins`, or `-1` when every branch failed.

While conceptually simple, this approach has exponential time complexity due to overlapping subproblems being solved multiple times.

#### Walkthrough

Example 1 (`coins = [1,3,4]`, `amount = 6`) makes 46 recursive calls, which is too many to follow by hand. To keep the call tree readable while showing the exact same mechanism, we trace a smaller constructed input: `coins = [1,3,4]`, `amount = 4`, whose answer is `1` (the single coin `4`).

Each call is `backtrack(remaining_amount)`. It tries every coin in order (`1`, then `3`, then `4`), subtracting the coin from `remaining_amount` and recursing. A call returns `0` when the amount hits exactly `0`, returns `-1` when the amount goes negative (that path is impossible), and otherwise returns `1 + the best result among its valid coin branches`.

The indented call tree below shows each call, what it returns, and how the returns combine back up. Branches that immediately go negative are collapsed to keep the focus on the meaningful paths.

```text
backtrack(4)                       try coin 1 -> backtrack(3)
  backtrack(3)                     try coin 1 -> backtrack(2)
    backtrack(2)                   try coin 1 -> backtrack(1)
      backtrack(1)                 try coin 1 -> backtrack(0)
        backtrack(0)  -> 0         base case: amount is 0
        (coins 3, 4 -> negative, return -1)
      -> 1                         best for 1 is 1 + 0
      (coins 3, 4 -> negative, return -1)
    -> 2                           best for 2 is 1 + 1
    backtrack(0)  -> 0             try coin 3: backtrack(0) returns 0
    (coin 4 -> negative, return -1)
  -> 1                             best for 3 is min(1 + 2, 1 + 0) = 1
  backtrack(1)                     try coin 3 -> backtrack(1)
    backtrack(0)  -> 0             best for 1 is 1 + 0
  -> 1
  backtrack(0)  -> 0              try coin 4: backtrack(0) returns 0
-> 1                              best for 4 is min(1 + 1, 1 + 1, 1 + 0) = 1
```

At the top, `backtrack(4)` compares its three coin branches: coin `1` gives `1 + backtrack(3)` = `1 + 1` = `2`, coin `3` gives `1 + backtrack(1)` = `1 + 1` = `2`, and coin `4` gives `1 + backtrack(0)` = `1 + 0` = `1`. The smallest is `1`, so the function returns `1`, matching the constructed example's expected answer of `1` (a single coin `4`).

Notice that `backtrack(1)` and `backtrack(0)` were each computed more than once across different branches: this repeated recomputation is exactly the overlapping-subproblems waste that memoization and bottom-up DP eliminate.

#### Solution

The code is the call tree from the walkthrough: two base cases, then the `min` over one recursive call per coin.

```python
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        def backtrack(remaining_amount):
            # Base cases
            if remaining_amount == 0:
                return 0
            if remaining_amount < 0:
                return -1

            min_coins = float('inf')

            # Try each coin denomination
            for coin in coins:
                # Recursively solve for remaining amount
                result = backtrack(remaining_amount - coin)

                # If it's possible to make the remaining amount
                if result != -1:
                    min_coins = min(min_coins, 1 + result)

            return -1 if min_coins == float('inf') else min_coins

        return backtrack(amount)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(coins.length^amount)`

In the worst case, we make `coins.length` recursive calls for each level, and the depth can go up to `amount`.

##### Space Complexity: `O(amount)`

Space for the recursion stack, which can be up to `amount` levels deep.

#### Key Insights

- The recurrence is simple: the minimum coins for amount `x` is `1 + min(backtrack(x - coin))` over all coins `c` that keep `x - coin` non-negative.
- It exposes the optimal substructure of the problem, which every faster approach exploits.
- Without caching, the same remaining amounts are recomputed exponentially many times, so this is only viable for tiny inputs.

### Top-Down Memoization

#### Derivation

The brute force pays for its honesty by re-deriving `backtrack(1)` and `backtrack(0)` in branch after branch. The observation that saves it is that a call's answer depends only on its argument: the fewest coins for a remaining amount is the same no matter which coin choices led there. That makes each distinct `remaining_amount` a cacheable state, so [memoization](https://en.wikipedia.org/wiki/Memoization) keeps the natural top-down recursion and puts a dictionary in front of it:

1. Keep the brute-force recursion, now named `dp(remaining_amount)`, with the
   same base cases.
2. Before trying coins, look `remaining_amount` up in `memo`; on a hit, return
   the stored answer without recursing.
3. Otherwise compute `min_coins` over the coins exactly as before, record the
   result in `memo[remaining_amount]` (`-1` when impossible), and return it.

One practical guard is required: each recursive call subtracts a single coin, so when the smallest coin is small relative to `amount` the call chain can approach `amount` frames. With `amount` up to `10^4` under the stated constraints, that comfortably exceeds CPython's default recursion limit of 1000 and raises `RecursionError`, so `coinChange` raises the limit with `sys.setrecursionlimit` before recursing.

#### Walkthrough

Example 1 costs the brute force 46 calls, too many to trace, so we reuse the same tailored input as the Brute Force walkthrough: `coins = [1,3,4]`, `amount = 4`. It is small enough to follow in full and reaches a memo hit within a dozen lines.

The tree below indents one level per recursive call. Watch `memo` fill as calls resolve, then pay off when `dp(4)` tries coin `3`:

```text
dp(4)                              try coin 1 -> dp(3)
  dp(3)                            try coin 1 -> dp(2)
    dp(2)                          try coin 1 -> dp(1)
      dp(1)                        try coin 1 -> dp(0)
        dp(0)  -> 0                base case
        (coins 3, 4 -> negative, return -1)
      -> 1, memo[1] = 1            best for 1 is 1 + 0
      (coins 3, 4 -> negative, return -1)
    -> 2, memo[2] = 2              best for 2 is 1 + 1
    dp(0)  -> 0                    try coin 3: base case
    (coin 4 -> negative, return -1)
  -> 1, memo[3] = 1                min(1 + 2, 1 + 0) = 1
  dp(1)   -> 1                     try coin 3  ** memo hit, no recursion **
  dp(0)   -> 0                     try coin 4: base case
-> 1, memo[4] = 1                  min(1 + 1, 1 + 1, 1 + 0) = 1
```

In the brute-force tree, the coin-3 branch of `backtrack(4)` re-derived `backtrack(1)` and its children from scratch; here `dp(1)` answers from `memo` in a single lookup. On this small input that saves only a few calls, but for amounts near `10^4` the same mechanism is what collapses `O(coins.length^amount)` into one computation per distinct amount. The final answer is `1` (the single coin `4`), matching the tailored example's expected result.

#### Solution

The code is the Brute Force recursion with the memo lookup and store wrapped around the coin loop, plus the recursion-limit guard.

```python
import sys
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # The call chain can reach one frame per unit of amount when the
        # smallest coin is small, which overflows CPython's default limit of
        # 1000 for amounts up to 10^4. Raise it before recursing.
        sys.setrecursionlimit(max(sys.getrecursionlimit(), amount + 100))

        # Memoization cache to store computed results
        memo = {}

        def dp(remaining_amount):
            # Base cases
            if remaining_amount == 0:
                return 0
            if remaining_amount < 0:
                return -1

            # Check if result is already computed
            if remaining_amount in memo:
                return memo[remaining_amount]

            min_coins = float('inf')

            # Try each coin denomination
            for coin in coins:
                # Recursively solve for remaining amount after using this coin
                result = dp(remaining_amount - coin)

                # If it's possible to make the remaining amount
                if result != -1:
                    min_coins = min(min_coins, 1 + result)

            # Store result in memo: -1 if impossible, otherwise minimum coins
            memo[remaining_amount] = -1 if min_coins == float('inf') else min_coins
            return memo[remaining_amount]

        return dp(amount)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(amount × coins.length)`

Each unique amount from 0 to `amount` is computed exactly once, and for each amount we try all coins.

##### Space Complexity: `O(amount)`

Space for the memoization table plus recursion stack depth (worst case O(amount)).

#### Key Insights

- Memoization keeps the natural recursive framing of the brute force while collapsing the exponential blow-up to one computation per distinct remaining amount.
- It only evaluates the subproblems actually reachable from the target, so it can skip amounts that bottom-up would still compute.
- Deep recursion can approach `amount` stack frames, which is why the code raises the interpreter's recursion limit up front; an iterative formulation avoids the issue entirely.

### Bottom-Up DP

#### Derivation

The memoized recursion still asks from the top ("what does `amount` need?") and pays for that framing with a call stack that can grow one frame per unit of amount. Turn the direction around: instead of waiting for the recursion to demand a subproblem, compute every amount's answer in increasing order, so that by the time `current_amount` is considered, every smaller answer it depends on already sits in a table. To make amount `i`, use any coin `c` with `c <= i` and then optimally make the remainder `i - c`, which gives the relation `dp[i] = min(dp[i], 1 + dp[i - c])`. This is the iterative [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) form of the exact same recurrence the recursion evaluated:

1. Create `dp` of size `amount + 1`, filled with the sentinel `amount + 1` (an
   impossible coin count standing in for infinity), and set `dp[0] = 0`: zero coins make amount `0`.
2. For each `current_amount` from `1` to `amount`, try every `coin` with
   `coin <= current_amount` and relax `dp[current_amount] = min(dp[current_amount], 1 + dp[current_amount - coin])`.
3. Return `dp[amount]`, or `-1` when it still holds the sentinel, meaning no
   combination of coins reaches it.

#### Recurrence

Let `dp[i]` be the fewest coins that sum to exactly `i`:

$$ dp[i] = \begin{cases} 0, & i = 0 \\[4pt] \displaystyle\min_{\substack{c \in \text{coins} \\ c \le i}} \bigl(dp[i - c] + 1\bigr), & i > 0 \end{cases} $$

```text
dp[0] = 0
dp[i] = min(dp[i - c] + 1) over coins c <= i,  for i > 0
        (min over an empty set is infinity: no coin fits)
```

The minimum over an empty set is \(\infty\): when no coin fits, amount `i` is unreachable. The code stands in the sentinel `amount + 1` for that infinity, which is larger than any achievable answer but small enough not to overflow. The result is `dp[amount]`, or `-1` if it never fell below the sentinel.

#### Walkthrough

Let us fill the table by hand on Example 1: `coins = [1,3,4]`, `amount = 6`, so the sentinel is `7` and `dp` starts as `[0, 7, 7, 7, 7, 7, 7]`. Each line below is one pass of the outer loop, showing which coins fit and the `min` they produce:

```text
start               dp = [0, 7, 7, 7, 7, 7, 7]                    only dp[0] known
current_amount = 1  dp[1] = 1 + dp[0] = 1                         coin 1 only
current_amount = 2  dp[2] = 1 + dp[1] = 2                         coin 1 only
current_amount = 3  dp[3] = min(1 + dp[2], 1 + dp[0]) = 1         coins 1, 3
current_amount = 4  dp[4] = min(1 + dp[3], 1 + dp[1], 1 + dp[0]) = 1   coins 1, 3, 4
current_amount = 5  dp[5] = min(1 + dp[4], 1 + dp[2], 1 + dp[1]) = 2   coins 1, 3, 4
current_amount = 6  dp[6] = min(1 + dp[5], 1 + dp[3], 1 + dp[2]) = 2   coins 1, 3, 4
```

The finished table is `[0, 1, 2, 1, 1, 2, 2]`. The winning term for `dp[6]` was `1 + dp[3]`: one coin `3` on top of the one-coin answer for amount `3`, which is the combination `6 = 3 + 3`. The function returns `dp[6] = 2`, matching the expected Output for Example 1.

#### Solution

The code is the table fill from the walkthrough: one relaxation per fitting coin per amount.

```python
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # dp[i] represents the minimum coins needed to make amount i
        # Initialize with amount + 1 (impossible value) for all amounts
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0  # Base case: 0 coins needed to make amount 0

        # For each amount from 1 to target amount
        for current_amount in range(1, amount + 1):
            # Try each coin denomination
            for coin in coins:
                # If this coin can be used (coin <= current_amount)
                if coin <= current_amount:
                    # Update minimum coins needed for current_amount
                    # Either keep existing value or use (1 + coins for remaining amount)
                    dp[current_amount] = min(dp[current_amount],
                                           1 + dp[current_amount - coin])

        # Return result: -1 if impossible, otherwise minimum coins needed
        return dp[amount] if dp[amount] != amount + 1 else -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(amount × coins.length)`

We iterate through each amount from 1 to `amount` (O(amount)) and for each amount, we check all coin denominations (O(coins.length)).

##### Space Complexity: `O(amount)`

We use a DP array of size `amount + 1` to store the minimum coins needed for each amount.

#### Key Insights

- This is the classic unbounded-knapsack minimization pattern: unlimited copies of each item (coin), optimizing the count for a target capacity (amount).
- Initializing every entry to the sentinel `amount + 1` exceeds any valid answer yet avoids overflow, so an unreachable amount is detected cleanly by checking against the sentinel at the end.
- Being iterative, it carries no recursion overhead and no stack-depth risk, which makes it the most robust choice for large amounts.

### BFS

#### Derivation

The three approaches above all refine one recursion. This one steps sideways and reframes the problem as a graph search: every amount from `0` to `amount` is a node, and adding one coin is a unit-weight edge from `current_amount` to `current_amount + coin`. The fewest coins making `amount` is then the fewest edges on a path from `0` to `amount`, and fewest edges on a unit-weight graph is exactly what [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) computes: it explores every amount reachable with one coin before any reachable with two, so the first time the target is reached is guaranteed optimal. This reframing is a clever lateral leap rather than a direct refinement of the recursion, which is why it lands last among the approaches.

1. Return `0` immediately when `amount == 0`: no coins are needed.
2. Start `queue` holding amount `0`, a `visited` set holding `0`, and
   `steps = 0`.
3. Each pass of the `while` loop processes one full level: increment `steps`,
   then pop every amount currently in the queue. For each popped `current_amount` and each `coin`, form `new_amount = current_amount + coin`.
4. If `new_amount == amount`, return `steps`: the target was reached using
   `steps` coins. Otherwise enqueue `new_amount` when it is below `amount` and not yet in `visited`.
5. If the queue drains without reaching the target, return `-1`.

#### Walkthrough

Let us run the search on Example 1: `coins = [1,3,4]`, `amount = 6`. The queue starts as `[0]` with `visited = {0}`. Each level below adds one more coin to every amount discovered on the previous level:

```text
start      queue = [0]          visited = {0}
steps = 1  pop 0: 0+1=1 enqueue, 0+3=3 enqueue, 0+4=4 enqueue
           queue = [1, 3, 4]    visited = {0, 1, 3, 4}    every 1-coin amount
steps = 2  pop 1: 1+1=2 enqueue, 1+3=4 in visited (skip), 1+4=5 enqueue
           pop 3: 3+1=4 in visited (skip), 3+3=6 == amount -> return steps = 2
```

Level one discovers every amount a single coin can make: `1`, `3`, and `4`. On level two, popping `3` and adding coin `3` produces `new_amount == 6`, so the function returns `steps = 2` without even finishing the level. The path `0 -> 3 -> 6` is the combination `6 = 3 + 3`, and the returned `2` matches the expected Output. Note the `visited` skips: amount `4` was already discovered on level one as `0 + 4`, so rediscovering it two coins deep could never improve on that and is pruned.

#### Solution

The code is the level sweep from the walkthrough: one `steps` increment per level, returning the moment `new_amount` hits `amount`.

```python
from collections import deque
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount == 0:
            return 0

        # BFS to find minimum steps (coins) to reach target amount
        queue = deque([0])  # Start with amount 0
        visited = {0}       # Track visited amounts to avoid cycles
        steps = 0           # Number of coins used so far

        while queue:
            steps += 1
            # Process all amounts reachable with current number of coins
            for _ in range(len(queue)):
                current_amount = queue.popleft()

                # Try adding each coin denomination
                for coin in coins:
                    new_amount = current_amount + coin

                    # If we reached the target amount
                    if new_amount == amount:
                        return steps

                    # If this amount is valid and not visited yet
                    if new_amount < amount and new_amount not in visited:
                        visited.add(new_amount)
                        queue.append(new_amount)

        return -1  # Target amount is unreachable
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(amount × coins.length)`

In the worst case, we visit each amount from 0 to `amount - 1`, and for each amount we try all coins.

##### Space Complexity: `O(amount)`

Space for the queue and visited set, both of which can contain up to `amount` elements.

#### Key Insights

- Modeling each reachable amount as a graph node turns "fewest coins" into "shortest path," which BFS solves directly.
- Because every edge has unit weight, the first level at which we hit the target amount is guaranteed to be optimal.
- The `visited` set is essential: without it, the same amounts would be enqueued repeatedly and the search would degrade badly.

### Top-Down Memoization with functools.cache

#### Derivation

The [Top-Down Memoization](#top-down-memoization) solution is the Brute Force recursion plus a dictionary that keeps it from re-solving a remaining amount it has already answered. The recursion is the algorithm; the dictionary is bookkeeping, and the standard library supplies it. Decorating the function with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) attaches an unbounded cache keyed by the call's arguments, consulted before the body runs and filled with whatever the body returns, so the coin loop and both base cases stay exactly as the Brute Force wrote them:

1. Keep `dp(remaining_amount)` verbatim from the Brute Force: return `0` at
   amount `0`, return `-1` when the amount has gone negative, otherwise take the `min` of `1 + dp(remaining_amount - coin)` over every coin whose branch is possible.
2. Decorate it with `@cache`, so each distinct `remaining_amount` runs the body
   at most once and every later request for it is served from the cache.
3. Delete the three bookkeeping lines the decorator now owns: the `memo = {}`
   declaration, the `if remaining_amount in memo` lookup, and the `memo[remaining_amount] = ...` store.
4. Keep the `sys.setrecursionlimit` guard. Caching removes repeated work, not
   depth: with `coins = [1]` the chain still descends one frame per unit of amount, reaching `10^4` frames under the stated constraints, far past CPython's default limit of 1000.

Where the decorator sits changes what gets stored. The hand-rolled version returns `-1` from its `remaining_amount < 0` guard before it ever touches `memo`, so negatives are never cached; `@cache` wraps the whole body, so every undershoot becomes its own entry. With small coins that adds a handful of keys, but a coin larger than `amount` produces a distinct negative for every amount it is subtracted from, which is what lifts the space bound below.

#### Walkthrough

Run it on Example 1: `coins = [1,3,4]`, `amount = 6`. The trace indents one level per call, tries the coins in the order `1`, `3`, `4`, and marks every request the decorator answers without running the body:

```text
dp(6)                        try coin 1 -> dp(5)
  dp(5)                      try coin 1 -> dp(4)
    dp(4)                    try coin 1 -> dp(3)
      dp(3)                  try coin 1 -> dp(2)
        dp(2)                try coin 1 -> dp(1)
          dp(1)              try coin 1 -> dp(0)
            dp(0)  -> 0      base case: amount is 0, now cached
            dp(-2) -> -1     base case: negative, now cached
            dp(-3) -> -1     base case: negative, now cached
          -> 1               best for 1 is 1 + 0
          dp(-1) -> -1       base case: negative, now cached
          dp(-2) -> -1       ** cache hit **
        -> 2                 best for 2 is 1 + 1
        dp(0)  -> 0          ** cache hit ** (coin 3)
        dp(-1) -> -1         ** cache hit ** (coin 4)
      -> 1                   min(1 + 2, 1 + 0) = 1
      dp(1)  -> 1            ** cache hit ** (coin 3)
      dp(0)  -> 0            ** cache hit ** (coin 4)
    -> 1                     min(1 + 1, 1 + 1, 1 + 0) = 1
    dp(2)  -> 2              ** cache hit ** (coin 3)
    dp(1)  -> 1              ** cache hit ** (coin 4)
  -> 2                       min(1 + 1, 1 + 2, 1 + 1) = 2
  dp(3)  -> 1                ** cache hit ** (coin 3)
  dp(2)  -> 2                ** cache hit ** (coin 4)
-> 2                         min(1 + 2, 1 + 1, 1 + 2) = 2
```

Nineteen calls are made in total. Ten of them reach the body, one per distinct argument: the seven amounts `0` through `6` and the three negatives `-1`, `-2`, `-3`. The other nine are cache hits, two of them on the negative keys `-1` and `-2`, which the hand-rolled memo never stores at all. The winning branch at the top is coin `3` laid on top of `dp(3) = 1`, the combination `6 = 3 + 3`. The call returns `2`, matching the expected Output `2` for Example 1.

#### Solution

The Brute Force recursion, unchanged, with one decorator standing in for the memo dictionary and the recursion-limit guard still in place.

```python
import sys
from functools import cache
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # Caching removes repeated work but not stack depth: the chain can still
        # reach one frame per unit of amount when the smallest coin is small.
        sys.setrecursionlimit(max(sys.getrecursionlimit(), amount + 100))

        # The cache lives on this inner function object, which is rebuilt on
        # every call, so results never carry over between different coin sets.
        @cache
        def dp(remaining_amount: int) -> int:
            # Base cases
            if remaining_amount == 0:
                return 0
            if remaining_amount < 0:
                return -1

            min_coins = float("inf")

            # Try each coin denomination
            for coin in coins:
                # Recursively solve for remaining amount after using this coin
                result = dp(remaining_amount - coin)

                # If it's possible to make the remaining amount
                if result != -1:
                    min_coins = min(min_coins, 1 + result)

            return -1 if min_coins == float("inf") else min_coins

        return dp(amount)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(amount × coins.length)`

The cache admits each distinct remaining amount into the body exactly once, and that one admission loops over all `coins.length` denominations. Every other call is a dictionary lookup on an integer key, which is constant time, so the totals match the hand-rolled memo: one coin loop per reachable amount from `0` to `amount`.

##### Space Complexity: `O(amount × coins.length)`

The non-negative keys number at most `amount + 1`, and the recursion stack descends at most `amount` frames, so both match the hand-rolled version. The negative keys are the difference: `remaining_amount - coin` undershoots zero for every coin larger than the amount it is subtracted from, and each distinct undershoot is cached, which in the worst case (denominations far larger than `amount`, permitted up to `2^31 - 1` here) adds up to `amount × coins.length` entries. When every coin is small relative to `amount`, only a few negatives are ever produced and the bound collapses back to `O(amount)`.

#### Key Insights

- The algorithm is untouched: the coin loop, the `min`, and both base cases read
  exactly as they do in the Brute Force, which shows that memoization is an execution strategy rather than a change to the recurrence.
- `@cache` keys on the argument tuple, so it substitutes cleanly only when the
  arguments are hashable and the function is genuinely pure; `dp` reads `remaining_amount` and the enclosing `coins`, which is fixed for the lifetime of the cache, so the substitution holds.
- Wrapping the entire body means the negative-amount rejections are cached too,
  which is free speed on small denominations and a real space cost on huge ones: the trade-off the hand-rolled `< 0` guard avoided by returning before the memo.
- The decorator does nothing about recursion depth, so `sys.setrecursionlimit`
  stays; when `amount` is large enough for that to worry you, the fix is [Bottom-Up DP](#bottom-up-dp) rather than a bigger stack.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(coins.length^amount)` - exponential, making `coins.length` recursive calls per level to a depth of `amount`.
- **Top-Down Memoization**: `O(amount × coins.length)` - each unique amount is computed once via memoization, trying all coins per amount.
- **Bottom-Up DP**: `O(amount × coins.length)` - iterates every amount from 1 to target and checks all coin denominations for each.
- **BFS**: `O(amount × coins.length)` - visits each amount once and tries all coins from it, like a shortest-path search.
- **Top-Down Memoization with functools.cache**: `O(amount × coins.length)`: the
  same one-coin-loop-per-amount bound, with the decorator's lookup standing in for the hand-written one.

### Space Complexity

- **Brute Force Recursion**: `O(amount)` - recursion stack up to `amount` levels deep.
- **Top-Down Memoization**: `O(amount)` - memoization table plus recursion stack depth up to `amount`.
- **Bottom-Up DP**: `O(amount)` - a single DP array of size `amount + 1`.
- **BFS**: `O(amount)` - queue and visited set, each holding up to `amount` elements.
- **Top-Down Memoization with functools.cache**: `O(amount × coins.length)`: the
  only approach whose space exceeds `O(amount)`, because the decorator caches the negative amounts the hand-rolled guard discarded; it falls back to `O(amount)` whenever the denominations are small relative to `amount`.

### Trade-offs

- **Brute Force Recursion**: Simplest to understand, but exponential time makes it impractical for large inputs.
- **Top-Down Memoization**: Intuitive recursion that only computes the subproblems actually required, at the cost of recursion overhead and stack space.
- **Bottom-Up DP**: Iterative with clear logic and optimal complexity, but builds every subproblem even when some are not needed.
- **BFS**: Models the problem cleanly as a shortest-path search, but adds queue and visited-set overhead.
- **Top-Down Memoization with functools.cache**: Keeps that recursion and its
  time complexity while cutting three lines of memo plumbing, paying an import, the cached negative amounts, and the loss of direct control over what the cache keys on and how long it lives.

### When to Use Each

- **Brute Force Recursion**: Only for understanding the problem or very small inputs. Demonstrates the need for optimization.
- **Top-Down Memoization**: When recursive thinking feels more natural or when you only need to compute specific subproblems.
- **Bottom-Up DP (Recommended)**: Best for interviews and production code. Clear, efficient, and iterative.
- **BFS**: When you want to model the problem as a graph shortest path problem. Good for educational purposes.
- **Top-Down Memoization with functools.cache**: The Pythonic default whenever the
  recursive framing is the one worth showing. Prefer it over the hand-rolled memo for readability, and fall back to the explicit dictionary when an interviewer asks to see the caching mechanism itself or when the cached negatives are a space cost you cannot pay.

### Optimization Notes

- The Bottom-Up DP solution is the recommended choice for interviews and production: it is iterative, optimal at `O(amount × coins.length)`, and free of recursion overhead.
- Initialize the DP array with `amount + 1` as a sentinel "impossible" value; it exceeds any valid answer yet avoids overflow, letting you detect unreachable amounts cleanly at the end.
- Both DP approaches share the same complexity, so prefer bottom-up unless recursive framing is clearer; reserve BFS for when a shortest-path mental model helps and avoid plain brute-force recursion for anything but tiny inputs.
- When the recursive framing is the one you want, write it as `@cache` on the brute-force function rather than as a hand-rolled dictionary: the time complexity is identical, and the decorator removes the three lines where a missed lookup or a forgotten store could hide.
- Neither memoized form escapes the stack: both descend one frame per coin subtracted, so an `amount` near `10^4` needs `sys.setrecursionlimit` in either case, which is the concrete reason Bottom-Up DP remains the recommendation.
