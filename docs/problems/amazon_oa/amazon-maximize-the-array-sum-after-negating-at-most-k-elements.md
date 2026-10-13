# [Max Negation](https://www.fastprep.io/problems/amazon-maximize-the-array-sum-after-negating-at-most-k-elements)

**Medium** | **NN minutes** | **Array, Greedy, Prefix Sum**

Given an array A with only positive numbers. We are allowed to negate any entries in the array, 
(i.e set A[i] = -A[i]). What is the maximum number of entries you can negate in the array such 
that every prefix sum after the negate operations is positive.

## Examples

### Example 1

**Input:** `A = [4, 1, 1, 1]`

**Output:** `3`

**Explanation:** We can apply only at-most 3 negate operations, to make A = [4, -1, -1, -1], after the negate operation, 

The prefix sums of A, p(A) = [4, 3, 2, 1] which are all positive. So that the answer for A is 3.

## Constraints

- `N/A`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
