# [Predict Answer](https://www.fastprep.io/problems/amazon-predict-answer)

**Medium** | **NN minutes** | **Array, Binary Search, Sorting, Stack**

In this stock price prediction game, Player 1 provides Player 2 with stock market data for n consecutive days, representing the stock prices on each day, represented by stockData[].

The rules of the game are as follows:

1. Player 1 will tell Player 2 a specific day number i (where 1 ≤ i ≤ n).2. Player 2 has to find the nearest day j (where 1 ≤ j < i or i < j ≤ n) in the past or future on which the stock price was lower than on the given day, i.e., stockData[j] < stockData[i].3. If there is more than one j which satisfies Rule 2 (i.e., a tie in distance), then Player 2 will choose the smaller day number (i.e., the smallest j satisfying Rule 2).4. If no such day j exists, then the answer for that case is -1.Given q queries in the array queries, the task is to find the answer for each queries[i] in queries and return a list of answers as per the above rules corresponding to each query.

Note: The description and the answer format both adhere to 1-based indexing for the arrays.

## Examples

### Example 1

**Input:** `stockData = [5, 6, 8, 4, 9, 10, 8, 3, 6, 4]`, `queries = [6, 5, 4]`

**Output:** `[5, 4, 8]`

**Explanation:** On day 6, the stock price is 10. Both 9 and 8 are lower prices one day away. Choose 9 (day 5) because it is before day 6.

On day 5, the stock price is 9. 4 is the closest lower price on day 4.

On day 4, the stock price is 4. The only lower price is on day 8.

So, the output is [5, 4, 8].

### Example 2

**Input:** `stockData = [2,1,3]`, `queries = [2,1]`

**Output:** `[-1,2]`

**Explanation:** Day 2 has no lower stock price. For day 1, day 2 has a lower price.

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ stockData[i] ≤ 10^9`
- `1 ≤ q ≤ 10^5`
- `1 ≤ queries[j] ≤ n`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
