# [Maximum Stock Profit with At Most Two Transactions](https://www.fastprep.io/problems/amazon-best-time-to-buy-and-sell-stock-iii)

**Medium** | **NN minutes** | **Array, Dynamic Programming**

You are given an array prices, where prices[i] is the price of one stock on day i. Return the maximum profit you can earn by completing at most two transactions.

A transaction consists of buying one share and selling that share on a later day. You may hold at most one share at a time, so a second transaction can begin only after the first transaction has been sold. You may also complete fewer than two transactions.

## Examples

### Example 1

**Input:** `prices = [3,3,5,0,0,3,1,4]`

**Output:** `6`

**Explanation:** Buy at 0 and sell at 3, then buy at 1 and sell at 4. The total profit is 3 + 3 = 6.

### Example 2

**Input:** `prices = [1,2,3,4,5]`

**Output:** `4`

**Explanation:** One transaction from price 1 to price 5 earns the maximum profit of 4.

### Example 3

**Input:** `prices = [7,6,4,3,1]`

**Output:** `0`

**Explanation:** No later price exceeds an earlier price, so the best choice is to make no transaction.

## Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^5`
- `A buy must occur before its matching sell.`
- `Transactions may not overlap.`

## Solutions

### Brute Force

#### Derivation

The most direct reading turns "at most two transactions" into geometry: every plan that uses two transactions has a boundary day, the day the first sale settles on, after which the second buy happens. Split the array at that boundary and the two halves become two independent copies of the single-transaction problem, [Best Time to Buy and Sell Stock](../best_time_to_buy_and_sell_stock.md):

1. Define `best_single_transaction(start, end)` as the largest profit of one
   buy-then-sell inside `prices[start..end]`, floored at `0` (no transaction).
2. For every `split` from `0` to `n - 2`, sell the first transaction on day
   `split` and start the second on day `split + 1`.
3. The two-leg candidate is
   `best_single_transaction(0, split) + best_single_transaction(split + 1, n - 1)`.
4. One transaction is also allowed, so `best_single_transaction(0, n - 1)`
   joins the candidates too.
5. Return the largest candidate, floored at `0` by its own initialization.

Each call to `best_single_transaction` re-scans its slice with a fresh running minimum, so the same early prices are re-read once per split. That repeated scanning is the waste the next approach removes, and the re-reads cost `O(n^2)` in total.

#### Walkthrough

Let us run the split table by hand on Example 2: `prices = [1,2,3,4,5]`, expected output `4`. Each row fixes one `split`, rescans both sides, and combines the legs:

| `split` | first leg `0..split` | second leg `split+1..n-1` | `first_leg` | `second_leg` | total |
| --- | --- | --- | --- | --- | --- |
| `0` | `[1]` | `[2,3,4,5]` | `0` | `3` | `3` |
| `1` | `[1,2]` | `[3,4,5]` | `1` | `2` | `3` |
| `2` | `[1,2,3]` | `[4,5]` | `2` | `1` | `3` |
| `3` | `[1,2,3,4]` | `[5]` | `3` | `0` | `3` |

Every split totals `3`, yet the expected output is `4`. The single transaction that buys at `1` and sells at `5` spans every possible split, so no split ever captures it. Step 4's extra candidate rescues the answer: `best_single_transaction(0, n - 1) = 4`, and the method returns `max(3, 4) = 4`, matching the expected Output. Example 2 is the case that proves "at most two" needs the one-transaction candidate, not just the split table.

#### Solution

The code is the split table from the walkthrough, with the running-minimum rescan as the single-transaction helper.

```python
from typing import List


class Solution:
    def maxProfitAtMostTwo(self, prices: List[int]) -> int:
        n = len(prices)

        def best_single_transaction(start: int, end: int) -> int:
            min_price = prices[start]
            top_profit = 0
            for day in range(start + 1, end + 1):
                if prices[day] < min_price:
                    min_price = prices[day]
                elif prices[day] - min_price > top_profit:
                    top_profit = prices[day] - min_price
            return top_profit

        top_total = 0
        for split in range(n - 1):
            first_leg = best_single_transaction(0, split)
            second_leg = best_single_transaction(split + 1, n - 1)
            top_total = max(top_total, first_leg + second_leg)
        return max(top_total, best_single_transaction(0, n - 1))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

There are `n - 1` splits and each one pays for two fresh scans of length up to `n`, so the scans total `O(n^2)`; the final whole-array scan is `O(n)` on top. At `prices.length` up to `10^5` this is far too slow for the constraint, but it is a correct baseline.

##### Space Complexity: `O(1)`

Only the running scalars `min_price`, `top_profit`, `top_total`, `first_leg`, and `second_leg` live across the loops; nothing grows with `n`.

#### Key Insights

- Any two-transaction plan has a boundary between the transactions, so splitting there decouples the problem into two independent single-transaction halves.
- The single-transaction candidate is not optional: Example 2's best plan spans every split, which is exactly how a split-only version returns `3` instead of `4`.
- The helper is the Running Minimum pass from the single-transaction problem, so the baseline already contains the machinery the faster approaches reuse.

### Prefix and Suffix Arrays

#### Derivation

The Brute Force rescans each slice only to ask one question per split: what is the best single transaction here? Ask each question once instead. Sweep left to right and record `best_left[day]`, the best single transaction inside `prices[0..day]`; sweep right to left and record `best_right[day]`, the best single transaction inside `prices[day..n-1]` (a sell after a buy within the suffix). The split table then reads straight off the two arrays, and the whole-array single-transaction candidate is `best_left[n - 1]`:

1. Fill `best_left` in one pass: carry `min_price`, the cheapest day so far, and
   set `best_left[day] = max(best_left[day - 1], prices[day] - min_price)`.
2. Fill `best_right` in one pass backward: carry `max_price`, the highest day
   seen from the right, and set
   `best_right[day] = max(best_right[day + 1], max_price - prices[day])`.
3. Combine: `top_total` starts at `best_left[n - 1]` (the one-transaction
   candidate) and takes `best_left[split] + best_right[split + 1]` for every
   `split` from `0` to `n - 2`.
4. Return `top_total`.

Folding the current day into `min_price` before or after computing the day's candidate is safe either way: including day `day` in its own minimum can only yield the harmless `0` of a same-day degenerate transaction, which the floor already allows.

#### Walkthrough

Let us fill both arrays on Example 1: `prices = [3,3,5,0,0,3,1,4]`, expected output `6`. The left sweep carries `min_price`, the right sweep carries `max_price`:

```text
left sweep    day 0    day 1    day 2    day 3    day 4    day 5    day 6    day 7
prices          3        3        5        0        0        3        1        4
min_price       3        3        3        0        0        0        0        0
best_left       0        0        2        2        2        3        3        4

right sweep   day 7    day 6    day 5    day 4    day 3    day 2    day 1    day 0
prices          4        1        3        0        0        5        3        3
max_price       4        4        4        4        4        5        5        5
best_right      0        3        3        4        4        4        4        4
```

Now read the split table off the two rows, combining `best_left[split]` with `best_right[split + 1]`:

```text
split=0   0 + 3 = 3      split=4   2 + 4 = 6
split=1   0 + 3 = 3      split=5   3 + 3 = 6
split=2   2 + 4 = 6      split=6   3 + 0 = 3
split=3   2 + 4 = 6      start     best_left[7] = 4 (one transaction)
```

The split table peaks at `6`, which beats the one-transaction candidate `4`, so the method returns `6`, matching the expected Output for Example 1. The winning split `5` is the plan from the Explanation: buy at `0`, sell at `3` on the left of the boundary, then buy at `1` and sell at `4` on the right.

#### Solution

The code is the two sweeps plus the split scan from the walkthrough.

```python
from typing import List


class Solution:
    def maxProfitAtMostTwo(self, prices: List[int]) -> int:
        n = len(prices)

        best_left = [0] * n
        min_price = prices[0]
        for day in range(1, n):
            min_price = min(min_price, prices[day])
            best_left[day] = max(best_left[day - 1], prices[day] - min_price)

        best_right = [0] * (n + 1)
        max_price = prices[n - 1]
        for day in range(n - 2, -1, -1):
            max_price = max(max_price, prices[day])
            best_right[day] = max(best_right[day + 1], max_price - prices[day])

        top_total = best_left[n - 1]
        for split in range(n - 1):
            top_total = max(top_total, best_left[split] + best_right[split + 1])
        return top_total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three linear passes: the left sweep, the right sweep, and the split scan, each doing constant work per day.

##### Space Complexity: `O(n)`

The two arrays `best_left` and `best_right` store one entry per day.

#### Key Insights

- Precomputing both directions converts the per-split rescans of the Brute Force into two array lookups, dropping `O(n^2)` to `O(n)`.
- `best_right[day]` is a single transaction inside the suffix, so the sell day of the second leg always sits strictly right of the split, keeping the two legs in the required order.
- Seeding `best_right` with one extra slot (`best_right[n] = 0`) lets the combine loop read `split + 1` without a bounds branch; the whole-array single-transaction candidate rides along as `best_left[n - 1]`.

### State Machine DP

#### Derivation

The split formulation asks "where is the boundary?" and pays an array per side. A different question removes the boundary entirely: as the prices scroll by day by day, what are all the states a trader can stand in? There are four: holding the first share, having sold the first, holding the second share, and having sold the second. Each day's price moves every state to its best value, and the best final value is simply the last state:

1. Name the four wallets `hold_first`, `sold_first`, `hold_second`, and
   `sold_second`, each holding the maximum cash in that state.
2. Seed before any price moves: `hold_first = hold_second = -prices[0]`
   (buy the first share on day `0`; buying the "second" share there is the
   degenerate plan that will net `0`), `sold_first = sold_second = 0`.
3. For each later `price`, update in place, each state taking the better of
   staying put or arriving from its predecessor:
   `hold_first = max(hold_first, -price)`,
   `sold_first = max(sold_first, hold_first + price)`,
   `hold_second = max(hold_second, sold_first - price)`,
   `sold_second = max(sold_second, hold_second + price)`.
4. Return `sold_second`.

Because the updates run left to right in one sweep, `sold_first` already includes today when `hold_second` reads it, so the second transaction may buy and sell on the very day the first one closed. That degenerate second trade nets exactly `0`, which is why `sold_second` never falls below the best single transaction: "at most two" is handled with no extra candidate, unlike the split-based approaches.

#### Recurrence

Let `hold_first[t]`, `sold_first[t]`, `hold_second[t]`, and `sold_second[t]` be the maximum cash in each state after day `t`:

$$ \begin{aligned} \text{hold\_first}[t] &= \max(\text{hold\_first}[t-1],\ -\text{prices}[t]) \\[2pt] \text{sold\_first}[t] &= \max(\text{sold\_first}[t-1],\ \text{hold\_first}[t] + \text{prices}[t]) \\[2pt] \text{hold\_second}[t] &= \max(\text{hold\_second}[t-1],\ \text{sold\_first}[t] - \text{prices}[t]) \\[2pt] \text{sold\_second}[t] &= \max(\text{sold\_second}[t-1],\ \text{hold\_second}[t] + \text{prices}[t]) \end{aligned} $$

```text
hold_first[t]  = max(hold_first[t-1],  -prices[t])
sold_first[t]  = max(sold_first[t-1],  hold_first[t]  + prices[t])
hold_second[t] = max(hold_second[t-1], sold_first[t]  - prices[t])
sold_second[t] = max(sold_second[t-1], hold_second[t] + prices[t])

seeds at day 0: hold_first = hold_second = -prices[0], sold_first = sold_second = 0
answer: sold_second[n-1]
```

Each row keeps the better of two options: stay in the state, or enter it from the state one row above (buy: subtract today's price; sell: add it). The negative seeds mean "a share was bought at day `0`'s price"; the answer is the fully-cashed-out state, which dominates the intermediate ones because every value is a valid plan.

#### Walkthrough

Let us push Example 1 through the four wallets: `prices = [3,3,5,0,0,3,1,4]`, expected output `6`. Each line shows the state after one `price` is processed:

```text
price=3   hold_first=-3   sold_first=0   hold_second=-3   sold_second=0   seeds
price=3   hold_first=-3   sold_first=0   hold_second=-3   sold_second=0   nothing improves
price=5   hold_first=-3   sold_first=2   hold_second=-3   sold_second=2   1st sell 3->5
price=0   hold_first=0    sold_first=2   hold_second=2    sold_second=2   rebuy at 0
price=0   hold_first=0    sold_first=2   hold_second=2    sold_second=2   nothing improves
price=3   hold_first=0    sold_first=3   hold_second=2    sold_second=5   2nd sell 0->3
price=1   hold_first=0    sold_first=3   hold_second=2    sold_second=5   nothing improves
price=4   hold_first=0    sold_first=4   hold_second=2    sold_second=6   2nd sell 2->6
```

The row for `price=0` is the pivotal beat: `hold_first` jumps from `-3` to `0` (a cheaper first buy) and `hold_second` jumps to `2` (buying at `0` right after the `3 -> 5` sale closed). Two prices later the final sale lifts `sold_second` to `6`, matching the expected Output for Example 1. The walk also shows the degenerate trade at work on the `price=5` row: `sold_second` reaches `2` there because the first transaction bought and sold on day `0` itself (its seeded wallets show it netting `0`), which freed the second transaction to carry the entire `3 -> 5` move.

#### Solution

The code is the four-wallet sweep from the walkthrough: one in-place update per price, in dependency order.

```python
from typing import List


class Solution:
    def maxProfitAtMostTwo(self, prices: List[int]) -> int:
        hold_first = -prices[0]
        sold_first = 0
        hold_second = -prices[0]
        sold_second = 0

        for price in prices[1:]:
            hold_first = max(hold_first, -price)
            sold_first = max(sold_first, hold_first + price)
            hold_second = max(hold_second, sold_first - price)
            sold_second = max(sold_second, hold_second + price)

        return sold_second
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass over the prices with four `max` updates each, constant work per day.

##### Space Complexity: `O(1)`

The whole table is four scalars; no array survives a single day.

#### Key Insights

- Four states suffice because the only facts a future decision needs are which transaction is open and how much cash it carries; the calendar is irrelevant.
- Same-day sell-then-rebuy is a feature, not a bug: it implements the zero-profit second transaction that makes `sold_second` dominate the best single transaction, so "at most two" needs no separate candidate.
- This is the split formulation with the boundary summed out: each `hold_second` update implicitly considers every possible split on every day, which is why the two prefix/suffix arrays collapse into four scalars.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - two fresh running-minimum rescans per split, one split per boundary day.
- **Prefix and Suffix Arrays**: `O(n)` - two directional sweeps plus one split scan.
- **State Machine DP**: `O(n)` - one pass with four constant-time state updates per day.

### Space Complexity

- **Brute Force**: `O(1)` - running scalars only, no arrays.
- **Prefix and Suffix Arrays**: `O(n)` - one stored entry per day in each direction.
- **State Machine DP**: `O(1)` - four scalars, one per trader state.

### Trade-offs

- The Brute Force states the geometry of the problem most plainly (a boundary splits two single-transaction problems) but pays quadratic time for rescanning, and it must add the single-transaction candidate by hand.
- The Prefix and Suffix Arrays approach pays one array per direction to eliminate the rescans, and it exposes every per-split answer, which follow-up queries could reuse.
- The State Machine DP reaches constant space by discovering that only four states matter; the derivation is less obvious, but the code is the shortest and the same shape extends to any transaction cap.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for small inputs.
- **Prefix and Suffix Arrays**: when the interview wants the two-pass idea, or when the best profit of every prefix and suffix is itself useful.
- **State Machine DP** (recommended): the default answer; linear time, constant space, and no special-casing of the one-transaction plans.

### Optimization Notes

- The State Machine DP generalizes mechanically to at most `k` transactions: `2k` wallet scalars updated in the same dependency order, `O(k n)` time and `O(k)` space.
- The in-place update order is load-bearing: `sold_first` must be refreshed before `hold_second` reads it, and `hold_first` before `sold_first`, or a day's price would be applied with stale state and undercount the degenerate same-day trade.
- Each state can imitate the one above it through the degenerate same-day trades (buy at today's price right after selling into it, sell right after buying), so `sold_second` dominates `sold_first` and both intermediate wallets; that is why the answer can be read from `sold_second` alone, without a final `max` over all four states.
