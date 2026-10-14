# [Get Maximum Count](https://www.fastprep.io/problems/amazon-get-maximum-count)

**Hard** | **NN minutes** | **Array, Hash Table, Sliding Window**

Amazon has launched a "Play to Win" game where users get a chance to earn free gift vouchers. The game presents you with an array of integers (arr) and an integer k. You are allowed to choose any contiguous subarray within arr and add an integer x of your choice to all the elements within that subarray. You can do this at most once.



The goal is to maximize the number of elements in the entire array that have a value equal to k after performing this operation (choosing a subarray and adding x to it).



You need to complete the function getMaximumCount which takes the integer array arr and the target value k as input, and returns the maximum number of elements equal to k that can be achieved.

## Examples

### Example 1

**Input:** `arr = [2, 3, 2, 4, 3, 2]`, `k = 2`

**Output:** `4`

**Explanation:** If we choose the subarray [4, 3] (from index 3 to 4) and add x = -2 to it, the array becomes [2, 3, 2, 2, 1, 2]. In this new array, there are four elements with the value 2. It's stated that this is the maximal count achievable, so the answer would be 4.

### Example 2

**Input:** `arr = [6, 4, 4, 6, 4, 4]`, `k = 6`

**Output:** `5`

**Explanation:** By choosing the subarray from index 1 to 5 (inclusive, assuming 0-based indexing, so the subarray is [4,4,6,4,4]) and adding x=2 to it, the subarray becomes [6,6,8,6,6]. The resulting array would be [6,6,6,8,6,6]. This gives us 5 elements equal to k=6, which is stated to be maximal.

## Constraints

- `1≤n≤2 · 10^5 (where n is the size of the array arr)`
- `1≤arr[i]≤2 · 10^5 (for each element in arr)`
- `1≤k≤2 · 10^5`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
