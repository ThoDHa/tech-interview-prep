# [Find Min Max Difference](https://www.fastprep.io/problems/amazon-find-min-max-difference)

**Hard** | **NN minutes** | **Sorting, Greedy**

Given one unsorted array of size n and integer k.



From subsequences of size n-k, find the max of consecutive element dfferences in the sorted subsequences AND from these max differences return the min difference.



A subsequence is any combination of integers.

## Examples

### Example 1

**Input:** `arr = [1, 4, 3, 6, 5]`, `k = 2`

**Output:** `1`

**Explanation:** Example - [1,4,3,6,5], k = 2, n-k = 3
Some Possible subequences of size 3 :

[4,3,1] (sorted) -> [1,3,4]
Diffs : 4-3 = 1, 3-1 = 1. Max of these is 1

[1,6,4] (sorted) -> [1,4,6]
Diffs : 6-4 = 2, 4-1 = 3. Max of these is 3

[3,6,5] (sorted) -> [3,5,6]
Diffs : 6-5 = 1, 5-3 = 2. Max of these is 2

Other subsequences follow....

Out of all possible sequences, we get the max diff in each subsequence.

Out of these maxes find the minimum diff.

In our case it's 1.

Answer is 1

## Constraints

- `TO-DO`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
