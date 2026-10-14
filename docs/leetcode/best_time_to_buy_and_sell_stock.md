# [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

**Easy** | **20 minutes** | **Array**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Kadane's algorithm](https://en.wikipedia.org/wiki/Maximum_subarray_problem)

**Practice:** [`practice/best_time_to_buy_and_sell_stock/solution.py`](../../practice/best_time_to_buy_and_sell_stock/solution.py)

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.

## Examples

### Example 1

**Input:** `prices = [7,1,5,3,6,4]`

**Output:** `5`

**Explanation:** Buy on day 2 (price = `1`) and sell on day 5 (price = `6`), profit = `6-1 = 5`. Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

### Example 2

**Input:** `prices = [7,6,4,3,1]`

**Output:** `0`

**Explanation:** In this case, no transactions are done and the max profit = `0`.

## Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`

## Deriving the Solution

A transaction is an ordered pair of days: buy on day `buy`, sell on a later day `sell`, for a profit of `prices[sell] - prices[buy]`. The answer is the largest such difference, floored at `0` because doing nothing is always allowed. Both solutions maximize that same expression; they differ in how many pairs they actually look at.

1. **Start literal.** Try every valid pair: for each `buy` day, scan every
   later `sell` day and keep the best difference. That examines all `n * (n - 1) / 2` pairs and costs `O(n^2)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Fix the sell day. Among all earlier buy days, only one
   matters: the cheapest. Yet the brute force re-scans the same early prices for every later sell day, recomputing that minimum over and over.
3. **Carry the minimum along.** Walk the array once, maintaining `min_price`,
   the cheapest price seen so far. At each day the best sale ending there is `price - min_price`, so one linear pass with two scalars finds the answer: see [Running Minimum](#running-minimum).

## Solutions

### Brute Force

#### Derivation

The most direct reading of the problem is to try every valid pair of days: buy on day `buy`, sell on a later day `sell`, and keep the largest difference.

1. Initialize `max_profit` to `0` so that an all-losses input returns `0`.
2. For each candidate buy day `buy`, scan every later sell day `sell`.
3. Compute `prices[sell] - prices[buy]` and update `max_profit` when it is larger.
4. Return `max_profit` after every pair has been considered.

Restricting the inner loop to `sell > buy` enforces the rule that the sale must happen strictly after the purchase, so no invalid transaction is ever counted.

#### Walkthrough

Trace the Brute Force on Example 1: `prices = [7,1,5,3,6,4]`. The outer loop fixes a `buy` day, the inner loop tries every later `sell` day, and `max_profit` only ever moves up. Each row shows the pair being tested, the candidate profit `prices[sell] - prices[buy]`, and `max_profit` after the `max(...)` update.

| `buy` (price) | `sell` (price) | candidate | `max_profit` after |
| --- | --- | --- | --- |
| `0` (`7`) | `1` (`1`) | `-6` | `0` |
| `0` (`7`) | `2` (`5`) | `-2` | `0` |
| `0` (`7`) | `3` (`3`) | `-4` | `0` |
| `0` (`7`) | `4` (`6`) | `-1` | `0` |
| `0` (`7`) | `5` (`4`) | `-3` | `0` |
| `1` (`1`) | `2` (`5`) | `4` | `4` |
| `1` (`1`) | `3` (`3`) | `2` | `4` |
| `1` (`1`) | `4` (`6`) | `5` | `5` |
| `1` (`1`) | `5` (`4`) | `3` | `5` |
| `2` (`5`) | `3` (`3`) | `-2` | `5` |
| `2` (`5`) | `4` (`6`) | `1` | `5` |
| `2` (`5`) | `5` (`4`) | `-1` | `5` |
| `3` (`3`) | `4` (`6`) | `3` | `5` |
| `3` (`3`) | `5` (`4`) | `1` | `5` |
| `4` (`6`) | `5` (`4`) | `-2` | `5` |

The first `buy = 0` block buys at the highest price (`7`), so every candidate is negative and `max_profit` stays at its `0` floor. The breakthrough comes with `buy = 1` (price `1`): pairing it with `sell = 4` (price `6`) gives `6 - 1 = 5`, the best pair in the whole array. No later pair beats it, so the loops finish and the method returns `max_profit = 5`, matching the expected Output of `5`.

#### Solution

The code is the pair table from the walkthrough as two nested loops.

```python
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        n = len(prices)
        for buy in range(n):
            for sell in range(buy + 1, n):
                max_profit = max(max_profit, prices[sell] - prices[buy])
        return max_profit
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The nested loops examine every ordered pair of days, which is about `n * (n - 1) / 2` comparisons. With `prices.length` up to `10^5`, this quadratic work is too slow in practice but is the natural baseline.

##### Space Complexity: `O(1)`

Only the scalar accumulator `max_profit` and the loop indices are kept, independent of the input size.

#### Key Insights

- Exhaustively checking pairs guarantees correctness and is easy to reason about.
- The `sell > buy` bound is what encodes the buy-before-sell constraint.
- The redundant rescanning of earlier prices is exactly what the next approach removes.

### Running Minimum

#### Derivation

The Brute Force re-scans every earlier day for each candidate sell day, but for a fixed sell day only one earlier day can matter: the cheapest one. The best sell day only ever pairs with the minimum price seen up to that point, so a single pass suffices if we remember the lowest price encountered so far.

1. Track `min_price`, the smallest price seen so far, starting at infinity.
2. Track `max_profit`, the best profit seen so far, starting at `0`.
3. For each `price`, if it is a new minimum, update `min_price` (a better future buy).
4. Otherwise, the profit of selling today is `price - min_price`; update `max_profit`
   when that exceeds the current best.
5. Return `max_profit` after the single pass.

Because `min_price` always holds the cheapest day at or before the current index, the candidate profit `price - min_price` is the best achievable sale ending on that day. This is [Kadane's algorithm](https://en.wikipedia.org/wiki/Maximum_subarray_problem) applied to the array of day-to-day differences.

#### Formula

Stated directly, the problem maximizes over ordered pairs of days:

$$ \text{answer} = \max\Bigl(0,\ \max_{0 \le i < j < n}\bigl(\text{prices}[j] - \text{prices}[i]\bigr)\Bigr) $$

```text
max_profit = max(0, max(prices[j] - prices[i]) over 0 <= i < j < n)
```

Fixing the sell day `j` and pushing the inner maximum onto the buy day turns that into one pass, because \(\text{prices}[j]\) is constant with respect to `i`:

$$ \max_{i < j}\bigl(\text{prices}[j] - \text{prices}[i]\bigr) = \text{prices}[j] - \min_{i < j} \text{prices}[i] $$

```text
max(prices[j] - prices[i]) over i < j  ==  prices[j] - min(prices[i]) over i < j
```

So with \(m[j] = \min_{0 \le i \le j} \text{prices}[i]\), which starts at \(m[0] = \text{prices}[0]\) and satisfies the one-step recurrence \(m[j] = \min(m[j-1], \text{prices}[j])\) for \(j \ge 1\):

$$ \text{answer} = \max_{0 \le j < n} \bigl(\text{prices}[j] - m[j]\bigr) $$

```text
min_price[0] = prices[0]
min_price[j] = min(min_price[j-1], prices[j]),  for j >= 1
max_profit   = max(prices[j] - min_price[j]) over 0 <= j < n
```

The outer \(\max\) with `0` is the "do nothing" option, which is why `max_profit` starts at `0` rather than at negative infinity.

#### Walkthrough

Let us run the single pass by hand on Example 1: `prices = [7,1,5,3,6,4]`. Each line shows the two scalars after one `price` is processed:

```text
price=7   min_price=7   max_profit=0    first price becomes the minimum
price=1   min_price=1   max_profit=0    new minimum: a better future buy
price=5   min_price=1   max_profit=4    5 - 1 = 4 beats 0
price=3   min_price=1   max_profit=4    3 - 1 = 2 does not beat 4
price=6   min_price=1   max_profit=5    6 - 1 = 5 beats 4
price=4   min_price=1   max_profit=5    4 - 1 = 3 does not beat 5
```

The day with price `1` (day 2 in the Explanation's one-based counting) becomes `min_price` and never loses that role; the day with price `6` (day 5) pairs against it for the winning profit `6 - 1 = 5`. The pass ends and the function returns `max_profit = 5`, matching the expected Output of `5`.

#### Solution

The code is the two-scalar update from the walkthrough, one branch for a new minimum and one for a candidate profit.

```python
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float("inf")
        max_profit = 0
        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price
        return max_profit
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each price is visited once and processed with constant-time comparisons and arithmetic, giving a single linear pass over the array.

##### Space Complexity: `O(1)`

Only the two scalars `min_price` and `max_profit` are maintained regardless of the input size.

#### Key Insights

- The optimal sell day is paired with the minimum price seen strictly before it, so
  one running minimum captures every useful buy opportunity.
- Initializing `max_profit` to `0` makes a strictly decreasing input return `0` for
  free, matching the "no transaction" rule.
- Updating `min_price` before measuring profit naturally preserves the buy-before-sell
  ordering without any extra bookkeeping.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - every ordered pair of days is compared.
- **Running Minimum**: `O(n)` - a single pass tracks the best buy seen so far.

### Space Complexity

- **Brute Force**: `O(1)` - only an accumulator and loop indices.
- **Running Minimum**: `O(1)` - two scalar trackers.

### Trade-offs

- Brute Force is the most transparent statement of the problem but rescans earlier
  prices repeatedly, making it impractical for large inputs.
- Running Minimum trades that redundant work for one remembered value, the minimum
  price so far, collapsing the quadratic scan into a linear one with no extra memory.

### When to Use Each

- **Brute Force**: Only as a conceptual baseline or for tiny inputs where clarity
  outweighs speed.
- **Running Minimum**: The right call in practice and the expected interview answer,
  since it meets the `10^5` constraint comfortably.

### Optimization Notes

- The running-minimum pass is Kadane's algorithm over the difference array
  `prices[i] - prices[i - 1]`; recognizing this connects the problem to maximum subarray.
- Using `float("inf")` as the initial minimum avoids a special case for the first
  element; an equivalent alternative is to seed `min_price = prices[0]` when the array is known to be non-empty.
- The popular "two pointers" telling of this problem (a buy pointer that jumps
  forward to the sell pointer whenever the price drops below it) is the running minimum in disguise: the left pointer always rests on the minimum price seen so far, so the two versions perform identical comparisons.
