# [Maximize Sum of Array Multiplication](https://www.fastprep.io/problems/amazon-maximize-sum-of-array-multiplication)

**Easy** | **NN minutes** | **Array, Sorting, Greedy**

You have an array of data (index starting from 1)
data = [3, 6, 1, 4, 2]. Rearrange the data such that after the permutation,
1 * data[1] + 2 * data[2] + 3 * data[3] + ... n * data[n] is the largest.



Return the permutations as an array where each element represents the index after permutation
(also starting from 1). If there are multiple equivalent answers, return the lexicographically
smallest one.


Function Description 
Complete the function maximizeSum in the editor.



maximizeSum has the following parameter:



int[] data: an array of integers
Returns 
int[]: the permutation of indices that maximizes the sum

## Examples

### Example 1

**Input:** `data = [3, 6, 1, 4, 2]`

**Output:** `[3, 5, 1, 4, 2]`

**Explanation:** The permutation [3, 5, 1, 4, 2] is chosen because the sum
1 * 1 + 2 * 2 + 3 * 3 + 4 * 4 + 5 * 6 is the largest sum you can get.



Larger values stay later. Sort the array based on 1. value 2. if there's a tie, based on index.

## Constraints

- `:O`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
