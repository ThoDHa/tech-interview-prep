# [Data Dependence Sum](https://www.fastprep.io/problems/amazon-get-data-dependence-sum)

**Hard** | **NN minutes** | **Math**

Data analysts at Amazon are analyzing time-series data. It was concluded that the data of the nth item was dependent on the data of some xth day if there is a positive integer k such that floor(n / k) = x where floor() represents the largest integer less than or equal to z.



Given n, find the sum of all the days' numbers on which the data of the xth (0 ≤ x < n) will be dependent.

## Examples

### Example 1

**Input:** `n = 13`

**Output:** `29`

**Explanation:** The data of the n = 13th day is dependent on [0, 1, 2, 3, 4, 6, 13] obtained for k = [14, 13, 6, 4, 3, 2, 1].

### Example 2

**Input:** `n = 1`

**Output:** `1`

**Explanation:** The only dependency is 1.

### Example 3

**Input:** `n = 5`

**Output:** `8`

**Explanation:** Hence, the answer is 0 + 1 + 2 + 5 == 8 :)

## Constraints

- `1 ≤ n ≤ 10^10`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
