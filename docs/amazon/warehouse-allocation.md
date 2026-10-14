# [Warehouse Distribution](https://www.fastprep.io/problems/warehouse-allocation)

**Easy** | **NN minutes** | **Array, Math, Greedy**

Amazon has a warehouse that stores piles of boxes containing goods to be shipped. There are n piles numbered 1, 2, ..., n, where the i-th pile has boxes[i] boxes.

To achieve an even distribution of boxes, the caretaker can perform the following operation any number of times (possibly zero):

Choose two distinct piles i and j such that boxes[i] > 0.Remove one box from pile i and place it on pile j (increment boxes[j] by 1 and decrement boxes[i] by 1).The caretaker wishes to minimize the difference between the maximum and the minimum number of boxes among the piles. Call this minimum achievable difference d.

Complete the function findMinimumOperations, which returns the minimum number of operations required to reach a configuration whose difference between the maximum and minimum number of boxes equals d.

## Examples

### Example 1

**Input:** `boxes = [5, 5, 8, 7]`

**Output:** `2`

**Explanation:** Consider the number of piles to be n = 4 and the boxes in them are boxes = [5, 5, 8, 7]. The minimum possible difference that can be achieved is 1 by transforming the piles into [6, 6, 7, 6] as below. Hence the answer is 2.

### Example 2

**Input:** `boxes = [2, 4, 1]`

**Output:** `1`

**Explanation:** Move a box from pile 2 to pile 3: [2, 4, 1] -> [2, 3, 2]

### Example 3

**Input:** `boxes = [4, 4, 4, 4, 4]`

**Output:** `0`

## Constraints

- `1 <= n <= 105`
- `1 <= boxes[i] <= 109`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
