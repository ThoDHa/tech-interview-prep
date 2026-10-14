# [Find Median Of Subarray Uniqueness](https://www.fastprep.io/problems/find-median-of-subarray-uniqueness)

**Hard** | **NN minutes** | **Binary Search, Sliding Window**

In an Amazon coding marathon, the following challenge was given.



The uniqueness of an array of integers is defined as the number of distinct elements present. For example, the uniqueness of [1, 5, 2, 1, 3, 5] is 4, element values 1, 2, 3, and 5. For an array arr of n integers, the uniqueness values of its subarrays is generated and stored in another array, call it subarray_uniqueness for discussion. Find the median of the generated array subarray_uniqueness.



Notes:


The median of a list is defined as the middle value of the list when it is sorted in non-decreasing order. If there are multiple choices for median, the smaller of the two values is taken. For example, the median of [1, 5, 8] is 5, and of [2, 3, 7, 11] is 3.A subarray is a contiguous part of the array. For example, [1, 2, 3] is a subarray of [6, 1, 2, 3, 5] but [6, 2] is not.

## Examples

### Example 1

**Input:** `arr = [1, 1]`

**Output:** `1`

**Explanation:** The subarrays along with their uniqueness values are:



[1]: uniqueness = 1[1, 1]: uniqueness = 1[1]: uniqueness = 1subarray_uniqueness is [1, 1, 1].

### Example 2

**Input:** `arr = [1, 2, 3]`

**Output:** `1`

**Explanation:** Given n = 3 and arr = [1, 2, 3], the subarrays along with their uniqueness values are:



[1]: uniqueness = 1[1, 2]: uniqueness = 2[1, 2, 3]: uniqueness = 3[2]: uniqueness = 1[2, 3]: uniqueness = 2[3]: uniqueness = 1subarray_uniqueness is [1, 2, 3, 1, 2, 1], and after sorting it is [1, 1, 1, 2, 2, 3].

### Example 3

**Input:** `arr = [1, 2, 1]`

**Output:** `1`

**Explanation:** The subarrays with their uniqueness values are:

[1]: uniqueness = 1
[1, 2]: uniqueness = 2
[1, 2, 1]: uniqueness = 2
[2]: uniqueness = 1
[2, 1]: uniqueness = 2
[1]: uniqueness = 1

The subarray_uniqueness array is [1, 2, 2, 1, 2, 1]. After sorting, the arr is [1, 1, 1, 2, 2, 2]. The choice is between the two bold values. Return the min of the two, 1.

[1]: uniqueness = 1

## Constraints

- `N/A`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
