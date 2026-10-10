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

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
