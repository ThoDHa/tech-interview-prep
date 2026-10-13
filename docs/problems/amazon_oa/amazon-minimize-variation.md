# [Minimize Variation](https://www.fastprep.io/problems/amazon-minimize-variation)

**Medium** | **NN minutes** | **Array, Sorting, Greedy**

Source note: Examples 3 through 5 were added on 2025-06-25, with relevant source images included in Problem Source. The original poster said Example 5 failed but did not clarify whether the testcase itself was incorrect or merely failed during their attempt, so treat that example with caution.

Special thanks: My deepest thanks to the incredible friend who helped bring the problem to completion. 🐳


As an operations engineer at Amazon, you are responsible for organizing the distribution of n different items in the warehouse. The size of each product is provided in an array productSize, where productSize[i] represents the size of the ith product.



You construct a new array called variation, where each element variation[i] is the difference between the largest and smallest product sizes among the first i products. Mathematically, this is defined as:



variation[i] = max(productSize[1], productSize[2], ..., productSize[i]) - min(productSize[1], productSize[2], ..., productSize[i])



Your goal is to arrange the products in a way that minimizes the total variation, i.e., the sum of variation[1] + variation[2] + ... + variation[n]. Determine the minimum possible value of this sum after you have reordered the products.



Complete the function minimizeVariation in the editor.

## Examples

### Example 1

**Input:** `productSize = [3, 1, 2]`

**Output:** `3`

**Explanation:** By reordering the products as productSize = [2,3,1]:



variation[0] = max(2) - min(2) = 2-2 = 0.
variation[1] = max(2,3) - min(2,3) = 3-2 = 1.
variation[2] = max(2,3,1) - min(2,3,1) = 3-1 = 2.

The sum is variation[0] + variation[1] + variation[2] = 0+1+2 = 3. This is the minimum possible total variation after rearranging.

### Example 2

**Input:** `productSize = [6, 1, 4, 2]`

**Output:** `9`

**Explanation:** By reordering the products as productSize = [1,2,4,6]:



variation[0] = max(1) - min(1) = 1-1 = 0.
variation[1] = max(1,2) - min(1,2) = 2-1 = 1.
variation[2] = max(1,2,4) - min(1,2,4) = 4-1 = 3.
variation[3] = max(1,2,4,6) - min(1,2,4,6) = 6-1 = 5.

The minimum total variation is variation[0] + variation[1] + variation[2] + variation[3] = 0+1+3+5 = 9.

### Example 3

**Input:** `productSize = [4, 5, 4, 2, 6, 1, 1]`

**Output:** `16`

**Explanation:** By reordering the products as productSize = [1, 1, 2, 4, 4, 5, 6]:

variation[0] = max(1) - min(1) = 1 - 1 = 0

variation[1] = max(1,1) - min(1,1) = 1 - 1 = 0

variation[2] = max(1,1,2) - min(1,1,2) = 2 - 1 = 1

variation[3] = max(1,1,2,4) - min(1,1,2,4) = 4 - 1 = 3

variation[4] = max(1,1,2,4,4) - min(1,1,2,4,4) = 4 - 1 = 3

variation[5] = max(1,1,2,4,4,5) - min(1,1,2,4,4,5) = 5 - 1 = 4

variation[6] = max(1,1,2,4,4,5,6) - min(1,1,2,4,4,5,6) = 6 - 1 = 5

variation[0] + variation[1] + variation[2] + variation[3] + variation[4] + variation[5] + variation[6]
= 0 + 0 + 1 + 3 + 3 + 4 + 5 = 16

### Example 4

**Input:** `productSize = [6, 1, 4, 2]`

**Output:** `9`

**Explanation:** By reordering the products as productSize = [1, 2, 4, 6]:

variation[0] = max(1) - min(1) = 1 - 1 = 0

variation[1] = max(1,2) - min(1,2) = 2 - 1 = 1

variation[2] = max(1,2,4) - min(1,2,4) = 4 - 1 = 3

variation[3] = max(1,2,4,6) - min(1,2,4,6) = 6 - 1 = 5

variation[0] + variation[1] + variation[2] + variation[3] = 0 + 1 + 3 + 5 = 9

### Example 5

**Input:** `productSize = [3, 1, 3, 3, 6, 6]`

**Output:** `11`

**Explanation:** Try: sorting based frequency [3, 3, 3, 6, 6, 1]

"I" Subarray Max Min Variation

0 [3] 3 3 0
1 [3, 3] 3 3 0
2 [3, 3, 3] 3 3 0
3 [3, 3, 3, 6] 6 3 3
4 [3, 3, 3, 6, 6] 6 3 3
5 [3, 3, 3, 6, 6,1] 6 1 5

Total = 0 + 0 + 0 + 3 + 3 + 5 = 11

The original OP mentioned this case failed, though it's unclear whether they meant the case itself was incorrect or that they failed to pass it. So, use it with caution!

## Constraints

- `1 <= n <= 2000`
- `1 <= productSize[i] <= 10^9`
- `Complete constraints set was added on 06-22-2025 :)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
