# [Calculate Beauty Values](https://www.fastprep.io/problems/amazon-calculate-beauty-values)

**Medium** | **NN minutes** | **Array, Sorting, Prefix Sum**

Source note: The judged core task matches the visible source at about 100%. The source images do not show numeric bounds or the original callable signature.

Special thanks: A special thank you to a lovely, amazing fren who shared that this question appeared again on September 14, 2026! 🩷

Amazon's development team is working on a feature for a new product, a smart array processor. In this smart processor, quite simply, given an array of numbers and instructions on which parts of the array to pick and combine into a new array, for each number in the original array, if it's included in the new array, its efficiency is 0; otherwise, the efficiency is the count of smaller numbers in the new array. The goal is to add up the efficiencies for all numbers in the original array.

A user has provided an integer array called arr of size n and a 2-dimensional array called pairs of size m x 2. Each pair in the pairs array represents the starting and ending indices of a subarray within arr.

For each subarray of arr represented by the array pairs, the goal is to merge and concatenate them into a nefficiency callew efficient.

The efficiency of an element at index i in arr is defined as follows: if the index i has not contributed to the formation of the array efficient, the efficiency is the count of integers in efficient that have a value strictly smaller than arr[i]. If the index i has contributed to the formation of the array efficient, its efficiency is 0.

Find the sum of the effiemncy of all the efficients in the array arr.

## Examples

### Example 1

**Input:** `arr = [1, 2, 3, 2, 4, 5]`, `pairs = [[0, 1], [3, 4], [0, 0], [3, 4]]`

**Output:** `12`

**Explanation:** $24

## Constraints

- `arr is an integer array of size n.`
- `pairs is an integer array of size m × 2.`
- `Each pair contains valid inclusive start and end indices for a subarray of arr.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
