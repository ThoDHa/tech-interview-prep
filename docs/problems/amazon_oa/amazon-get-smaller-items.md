# [Get Smaller Items](https://www.fastprep.io/problems/amazon-get-smaller-items)

**Hard** | **NN minutes** | **Prefix Sum, Binary Search, Sorting**

Special thanks: 🐳 Manyyy thanks to the GG of Error-Free Excellence 👉 ✨ spike ✨! 🐝


An Amazon fulfillment center receives a large number of orders each day. Each order is associated with a range of prices of items that need to be picked from the warehouse and packed into a box. There are n items in the warehouse, which are represented as an array items[n]. The value of items[i] represents the value of ith item in the warehouse, and subsequently there are m orders. The start_index and end_index for the order are represented in the arrays start[i] and end[i]. Also start[i] and end[i] are 0-index based. For each order, all the items are picked from the inclusive range from start[i] through end[i].



Given array items, start, end, and query. For each query[i], find the count of elements in the range with a value strictly less than query[i].

## Examples

### Example 1

**Input:** `items = [1, 2, 5, 4, 5]`, `start = [0, 0, 1]`, `end = [1, 2, 2]`, `query = [2, 4]`

**Output:** `[2, 5]`

**Explanation:** Over the 3 orders, the picked items are [1, 2], [1, 2, 5], and [2, 5].



For the first query, 2 picked items have values less than 2.



5 picked items have values less than 4.



Hence the answer is [2, 5].

### Example 2

**Input:** `items = [1, 2, 3, 2, 4, 1]`, `start = [2, 0]`, `end = [4, 0]`, `query = [5, 3]`

**Output:** `[4, 2]`

**Explanation:** In the first move, pick items from index 2 to 4, items = [3, 2, 4]

In the second move, pick the items from index 0, items = [1]

The picked items are [3, 2, 4, 1] -

For the first query, all items have values strictly less than 5.
For the second query, 2 items have values strictly less than 3.

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ items[i] ≤ 10^9, where 0 ≤ i < n`
- `0 < m ≤ 10^5`
- `0 ≤ start[i] ≤ end[i] < n, where 0 ≤ i < m`
- `1 ≤ q ≤ 10^5`
- `1 ≤ query[i] ≤ 10^9, where 0 ≤ i < q`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
