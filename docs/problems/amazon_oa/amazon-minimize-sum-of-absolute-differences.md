# [Minimize Sum of Absolute Differences](https://www.fastprep.io/problems/amazon-minimize-sum-of-absolute-differences)

**Easy** | **NN minutes** | **Array, Sorting, Greedy**

Given two arrays a[] and b[] of equal length n. The task is to pair each element of array a to an element in array b, such that sum S of absolute differences of all the pairs is minimum.



Suppose, two elements a[i] and a[j] (i!=j) of a are paired with elements b[p] and b[q] of b respectively, then p should not be equal to q.



Complete the function minimizeSumOfAbsoluteDifferences in the editor.



minimizeSumOfAbsoluteDifferences has the following parameters:


int a[n]: an array of integersint b[n]: an array of integers
int: the minimum sum of absolute differences

## Examples

### Example 1

**Input:** `a = [3, 2, 1]`, `b = [2, 1, 3]`

**Output:** `0`

**Explanation:** 1st pairing: |3 - 2| + |2 - 1| + |1 - 3| = 1 + 1 + 2 = 4

2nd pairing: |3 - 2| + |1 - 1| + |2 - 3| = 1 + 0 + 1 = 2

3rd pairing: |2 - 2| + |3 - 1| + |1 - 3| = 0 + 2 + 2 = 4

4th pairing: |1 - 2| + |2 - 1| + |3 - 3| = 1 + 1 + 0 = 2

5th pairing: |2 - 2| + |1 - 1| + |3 - 3| = 0 + 0 + 0 = 0

6th pairing: |1 - 2| + |3 - 1| + |2 - 3| = 1 + 2 + 1 = 4

Therefore, 5th pairing has minimum sum of absolute difference.

### Example 2

**Input:** `a = [4, 1, 8, 7]`, `b = [2, 3, 6, 5]`

**Output:** `6`

**Explanation:** The minimum sum of absolute differences can be obtained by the following pairing:

|4 - 3| + |1 - 2| + |8 - 6| + |7 - 5| = 1 + 1 + 2 + 2 = 6

## Constraints

- `Unknown for now. Will add once find out 🤝`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
