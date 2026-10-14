# [Best Time to Buy And Sell Stock With Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

**Medium** | **25 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Memoization](https://en.wikipedia.org/wiki/Memoization) · [Recursion (computer science)](https://en.wikipedia.org/wiki/Recursion_(computer_science))

**Practice:** [`practice/best_time_to_buy_and_sell_stock_with_cooldown/solution.py`](../../practice/best_time_to_buy_and_sell_stock_with_cooldown/solution.py)

You are given an integer array `prices` where `prices[i]` is the price of NeetCoin on the `ith` day.

You may buy and sell one NeetCoin multiple times with the following restrictions:
* After you sell your NeetCoin, you cannot buy another one on the next day (i.e., there is a cooldown period of one day).
* You may only own at most one NeetCoin at a time.

You may complete as many transactions as you like.

Return the **maximum profit** you can achieve.

## Examples

### Example 1

**Input:** `prices = [1,3,4,0,4]`

**Output:** `6`

**Explanation:** Buy on day 0 (price = 1) and sell on day 1 (price = 3), profit = 3-1 = 2. Then buy on day 3 (price = 0) and sell on day 4 (price = 4), profit = 4-0 = 4. Total profit is 2 + 4 = 6.

### Example 2

**Input:** `prices = [1]`

**Output:** `0`

## Constraints

- `1 <= prices.length <= 5000`
- `0 <= prices[i] <= 1000`

## Deriving the Solution

At any moment on day `i` exactly one thing is true: you hold a share, you sold today, or you are free to act. The cooldown is not a global rule but a local one: buying is forbidden only on the day right after a sale, which means the answer for a day is computable from the answers of the previous day plus the knowledge of which of those three situations held. Every solution below tracks those situations; they differ in how exhaustively.

1. **Start literal.** Try every buy day and every sell day after it, sell
   before a cooldown-forbidden rebuy by recursing on the rest of the
   timeline, and take the best total. The branches multiply into `O(2^n)`:
   see [Brute Force Recursion](#brute-force-recursion).
2. **Cache the states.** A branch's future depends only on `(day, holding or
   not)`-shaped facts, not on the trade history that produced them, so the
   recursion's states are cacheable and the work collapses to a constant
   number of states per day: see
   [Top-Down Memoization](#top-down-memoization).
3. **Roll the states forward.** Three states per day, each reading only the
   previous day, is a state machine: `hold`, `sold`, `rest`, updated in one
   pass with three scalars, `O(n)` time and `O(1)` space: see
   [Bottom-Up State Machine](#bottom-up-state-machine).

## Solutions

### Brute Force Recursion

#### Derivation

The most literal reading enumerates the decisions. On each day you either hold a share (then you may sell or keep holding) or you do not (then you may buy, unless yesterday was a sale). Try every legal decision and keep the best outcome:

1. Define `dfs(day, holding, cooldown)` as the best profit from `day`
   onward, where `cooldown` marks that today is a forbidden-buy day because
   yesterday's sale.
2. On the last day return `0`.
3. While holding: the best of selling today (`prices[day]` plus the rest) or
   holding on.
4. While free: the best of buying today (`-prices[day]` plus the rest) or
   resting, but only when `cooldown` is false.
5. Return `dfs(0, False, False)`.

#### Walkthrough

Trace the decision tree on a constructed input, `prices = [1, 2, 1, 2]`, small enough to list its branches (introduced as such; Example 1's tree already holds 47 nodes):

```text
buy 1 -> sell 2 -> rest -> rest        total 1
buy 1 -> rest -> rest -> sell 2        total 1
rest -> rest -> buy 1 -> sell 2        total 1
buy 1 -> sell 2 -> buy 1 -> ...        forbidden: day 2 is the cooldown day
buy 1 -> rest -> sell 1 -> buy 2 ...   totals <= 1, all worse
rest -> rest -> rest -> rest           total 0
```

The best branches reach `1`: one profitable trade, with the cooldown blocking any second trade that would help. Every candidate path appears in the tree, so `1` is exact for this input.

#### Solution

The code is the walkthrough's decision tree: one fork per state, three base rules.

```python
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        def dfs(day: int, holding: bool, cooldown: bool) -> int:
            if day == len(prices):
                return 0
            if holding:
                return max(
                    dfs(day + 1, False, True) + prices[day],  # sell
                    dfs(day + 1, True, False),                # hold
                )
            if cooldown:
                return dfs(day + 1, False, False)             # forced rest
            return max(
                dfs(day + 1, True, False) - prices[day],      # buy
                dfs(day + 1, False, False),                   # rest
            )

        return dfs(0, False, False)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Each free day branches into buy/rest and each held day into sell/hold, so the tree's leaves grow exponentially in the number of days.

##### Space Complexity: `O(n)`

The recursion stack, one frame per day along the current branch.

#### Key Insights

- The cooldown lives entirely in one parameter: selling today makes today+1
  a buy-forbidden day.
- Correct without any insight beyond the rules; every faster solution is
  this tree with repeated work removed.
- The branching factor of 2 per day is what the next solution collapses.

### Top-Down Memoization

#### Derivation

The brute force re-solves futures it has already seen: after `buy 1, sell 2`, the remaining timeline is the same problem as after `rest, rest, buy 1, sell 2`, yet the tree walks it twice. A branch's future depends on three facts, the day and the two booleans, and on nothing about the trade history, so each `(day, holding, cooldown)` triple is a cacheable state with only `3n` of them:

1. Keep the brute-force recursion unchanged.
2. Add a `memo` keyed by `(day, holding, cooldown)`; check it on entry and
   store before every return.

#### Walkthrough

Trace the caching effect on Example 1: `prices = [1,3,4,0,4]`. From day 2 the state `(day 3, free, no cooldown)` is reached by more than one path, and the second arrival is a hit:

```text
buy 1 -> sell 3 -> rest          -> state (day 3, free, off)
buy 1 -> rest -> rest            -> state (day 3, free, off)  ** memo hit **
```

Every distinct state is solved once: 12 states on this input instead of the brute tree's 47 nodes. The final answer is `6`, matching the expected Output for Example 1 (buy at 1, sell at 3, buy at 0, sell at 4).

#### Solution

The code is the brute-force recursion with a dict in front of it.

```python
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        memo = {}

        def dfs(day: int, holding: bool, cooldown: bool) -> int:
            if day == len(prices):
                return 0
            if (day, holding, cooldown) in memo:
                return memo[(day, holding, cooldown)]
            if holding:
                best = max(
                    dfs(day + 1, False, True) + prices[day],
                    dfs(day + 1, True, False),
                )
            elif cooldown:
                best = dfs(day + 1, False, False)
            else:
                best = max(
                    dfs(day + 1, True, False) - prices[day],
                    dfs(day + 1, False, False),
                )
            memo[(day, holding, cooldown)] = best
            return best

        return dfs(0, False, False)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

At most `3n` distinct states, each solved once in constant work.

##### Space Complexity: `O(n)`

The memo's `3n` entries plus the recursion stack.

#### Key Insights

- The state `(day, holding, cooldown)` is a complete summary of the past:
  nothing else about the trade history affects the future.
- The `(day, holding, cooldown=False)` state on a day right after a forced
  rest is unreachable, so the true state count is below `3n`.
- Recursion depth is `n` frames, which crosses CPython's default recursion
  limit near the top of the constraint range (`n` up to 5000); the state
  machine removes the stack entirely.

### Bottom-Up State Machine

#### Derivation

Three states per day, each depending only on yesterday: that is a [state machine](https://en.wikipedia.org/wiki/Finite-state_machine), and a machine with constant states needs no table at all, just one scalar per state rolled forward. Name the states `hold` (owning a share), `sold` (sold today, the cooldown day), and `rest` (free to act without having sold today). The transitions follow the rules directly: `hold` continues holding or buys from a free day, `sold` is exactly a sale, and `rest` continues resting or expires a yesterday sale. Buying from `rest` rather than from `sold` is the cooldown, encoded in one edge's absence:

1. Initialize `hold = sold = -infinity` (impossible before day 0) and
   `rest = 0` (no trades, no profit).
2. Per day, using yesterday's values: `sold = hold + price`,
   `hold = max(hold, rest - price)`, `rest = max(rest, old sold)`.
3. Return `max(sold, rest)`: the last day can only end held (worthless,
   never better than never buying) or free.

#### Walkthrough

Trace the three scalars on Example 1: `prices = [1,3,4,0,4]`:

```text
day  price   hold     sold      rest
start  -    -inf     -inf        0
 0     1    -1       -inf        0
 1     3    -1        2          0
 2     4    -1        3          2
 3     0     2       -1          3
 4     4     2        6          3
```

Day 0 buys at 1 (`hold = -1`); day 1 sells it (`sold = -1 + 3 = 2`); day 2's sale of the day-0 share at 4 gives `sold = 3`, but holding on (`hold` stays `-1`) is worse than rebuying, so day 2 also parks `sold = 2` into `rest` for later. Day 3 buys at `0` using day 2's `rest`: `rest - price = 2 - 0 = 2`, and `hold = max(-1, 2) = 2`. Day 4 sells at 4 for `sold = 2 + 4 = 6`, matching the expected Output `6`. Example 2's single day leaves `sold` at `-infinity` and `rest` at `0`, so `max` returns `0`.

#### Solution

The code is the walkthrough's transition table, one assignment per edge.

```python
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        hold = float("-inf")
        sold = float("-inf")
        rest = 0
        for price in prices:
            prev_sold = sold
            sold = hold + price
            hold = max(hold, rest - price)
            rest = max(rest, prev_sold)
        return max(sold, rest)
```

#### Recurrence

Let \(s_d\), \(h_d\), and \(r_d\) be the `sold`, `hold`, and `rest` values after day `d` closes, with price \(p_d\):

$$ h_d = \max(h_{d-1},\ r_{d-1} - p_d), \qquad s_d = h_{d-1} + p_d, \qquad r_d = \max(r_{d-1},\ s_{d-1}), \qquad h_{-1} = s_{-1} = -\infty,\ r_{-1} = 0 $$

```text
h_d = max(h_(d-1), r_(d-1) - p_d)      (keep holding, or buy from a free day)
s_d = h_(d-1) + p_d                    (sell the share held through day d - 1)
r_d = max(r_(d-1), s_(d-1))            (keep resting, or expire yesterday's sale)
```

Each right-hand side reads only day `d - 1` values, so three scalars roll forward with no table. Buying from `r` and never from `s` is the cooldown: the code's simultaneous update (saving `prev_sold`) is what makes every read the old value. The answer is \(\max(s_{n-1}, r_{n-1})\), since ending still holding is never better than never buying.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One constant-work transition per day.

##### Space Complexity: `O(1)`

Three scalars plus the `prev_sold` snapshot.

#### Key Insights

- The cooldown is one missing edge: no transition from `sold` to a buy.
  Every correct formulation of this problem reduces to that.
- Reading yesterday's `sold` before overwriting it (`prev_sold`) is the
  whole implementation trick; the three states share a timestep.
- `hold = max(hold, rest - price)` keeps the option of never selling an
  older, better-positioned share: `hold` never decays, it only improves.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(2^n)` - two branches per day over the whole tree.
- **Top-Down Memoization**: `O(n)` - at most `3n` states, one solve each.
- **Bottom-Up State Machine**: `O(n)` - one transition per day.

### Space Complexity

- **Brute Force Recursion**: `O(n)` - the recursion stack.
- **Top-Down Memoization**: `O(n)` - the memo plus the stack.
- **Bottom-Up State Machine**: `O(1)` - three scalars.

### Trade-offs

- The brute force derives straight from the rules and is correct by
  construction, but unusable past ~25 days.
- Memoization is the brute force plus a dict: the smallest step to linear.
- The state machine is the memoization with the stack and the dict removed,
  the form to write in production.

### When to Use Each

- **Brute Force Recursion**: building intuition, or as an oracle on tiny
  inputs when checking the faster versions.
- **Top-Down Memoization**: when deriving live in an interview; the state
  discovery happens naturally.
- **Bottom-Up State Machine**: the answer to the problem as stated
  (recommended here).

### Optimization Notes

- A price of `0` on a free day is a free share; the transitions handle it
  without special cases (`hold = rest - 0`), which is exactly Example 1's
  day 3.
- The transaction-fee variant (LeetCode 714) changes one transition: add the
  fee at sale. The cooldown variant is unusual precisely because its rule is
  a missing edge rather than an adjusted cost.
- `hold` initialized to `-infinity` matters: a dict-of-zeros initialization
  would let day 0 "sell" a share it never bought.

