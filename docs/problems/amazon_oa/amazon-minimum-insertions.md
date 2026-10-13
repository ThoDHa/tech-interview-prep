# [Min Insertions](https://www.fastprep.io/problems/amazon-minimum-insertions)

**Medium** | **NN minutes** | **Dynamic Programming, Array**

Amazon CodeCraft introduces you to an engaging problem-solving challenge. You are
presented with two integer lists named as: initialList and finalList of length m and
n respectively.



The finalList contains unique integers, while the initialList may contain duplicates.
You are allowed to perform the following operation any number of times (possibly
zero):



Insert any positive integer at any position (including the start and the end of the
list) in the initialList.

Your task is to determine the minimum number of operations required to transform
the initialList into a subsequence of the finalList. It can be proven that it is always
possible to transform the initialList into a subsequence of the finalList.



Note: A subsequence of an array is a sequence that can be derived from the array by
deleting some or no elements, without changing the order of the remaining elements.



For example, [2, 7, 4] is a subsequence of [4, 2, 3, 7, 2, 1, 41], while [2, 4, 2] is not.

## Examples

### Example 1

**Input:** `finalList = [5, 1, 3]`, `initialList = [9, 4, 2, 3, 4]`

**Output:** `2`

**Explanation:** We make the following insertions in the initialList:



Operation 1: Insert 5 such that initialList = [5, 9, 4, 2, 3, 4], so current common
subsequence [5, 3].
Operation 2: Insert 1 such that initialList = [5, 9, 4, 1, 2, 3, 4], so current common
subsequence [5, 1, 3].

Now, consider the subsequence formed from the elements at index (0, 3, 5) of the
initialList, and make up the finalList, hence we require a minimum of 2 operations.

## Constraints

- `🍓🍓`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
