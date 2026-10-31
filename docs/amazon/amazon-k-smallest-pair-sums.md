# [Find K Pairs with Smallest Sums](https://www.fastprep.io/problems/amazon-k-smallest-pair-sums)

**Medium** | **NN minutes** | **Array, Heap, Sorting**

Given two integer arrays nums1 and nums2, both sorted in nondecreasing order, consider every index pair (i, j) and the pair [nums1[i], nums2[j]].

Return the k pairs with the smallest sums. Return them in nondecreasing order of their sums. Different index pairs are distinct, so duplicate value pairs may appear.

## Examples

### Example 1

**Input:** `nums1 = [1,7,11]`, `nums2 = [2,4,6]`, `k = 3`

**Output:** `[[1,2],[1,4],[1,6]]`

**Explanation:** The three smallest pair sums are 3, 5, and 7.

### Example 2

**Input:** `nums1 = [1,1,2]`, `nums2 = [1,2,3]`, `k = 2`

**Output:** `[[1,1],[1,1]]`

**Explanation:** The two occurrences use different indices in nums1.

## Constraints

- `1 <= nums1.length, nums2.length <= 100000.`
- `Both arrays are sorted in nondecreasing order.`
- `Every value is in [-10^9, 10^9].`
- `1 <= k <= nums1.length * nums2.length.`
- `Every pair sum fits in a signed 32-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
