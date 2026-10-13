# [Optimal Level](https://www.fastprep.io/problems/amazon-find-optimal-level)

**Hard** | **NN minutes** | **Array, Binary Search, Greedy**

Amazon is dedicated to leveraging advanced methods to streamline stock movement across its distribution centers. In this scenario, you are assigned a challenge involving a specific process with a sequence of stock quantities.



More specifically, you are provided with an array of positive numbers, stockArr, containing n elements. Additionally, you are given two positive numbers, incVal and decVal, where incVal is less than or equal to decVal. You may execute the stock adjustment operation on stockArr any number of times, including not performing it at all.



The stock adjustment operation is defined as picking two distinct positions p and q in the array (0 ≤ p, q < n), increasing the value at stockArr[p] by incVal, and decreasing the value at stockArr[q] by decVal.



Our goal is to compute the highest achievable value of the minimum stock quantity in stockArr after completing all desired operations.



Note: During the adjustment process, some elements may become negative. However, once all operations have been completed, every number in stockArr must be strictly greater than 0.

## Examples

### Example 1

**Input:** `stockArr = [11, 1, 2]`, `incVal = 2`, `decVal = 3`

**Output:** `3`

### Example 2

**Input:** `stockArr = [1, 5, 9]`, `incVal = 2`, `decVal = 2`

**Output:** `5`

## Constraints

- `2 ≤ n ≤ 2*10^5`
- `1 ≤ stockArr[i] ≤ 10^9`
- `1 ≤ incVal ≤ decVal ≤ 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
