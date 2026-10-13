# [Sum of Max Subarrys](https://www.fastprep.io/problems/amazon-sum-of-max-subarrays)

**Hard** | **NN minutes** | **Array, Stack**

Find the sum of the maximum of all subarrays multiplied by their length in O(n).



For example, given an array arr = [4,2,1,2], the output should be 59.


Function Description 
Complete the function sumOfMaxOfSubarrays in the editor.



sumOfMaxOfSubarrays has the following parameter:



int[] arr: an array of integers
Returns 
long integer: the sum of the maximum of all subarrays multiplied by their length

## Examples

### Example 1

**Input:** `arr = [4, 2, 1, 2]`

**Output:** `59`

**Explanation:** Here's how the sum is calculated:

[4] 1 4 1 * 4 = 4

[4, 2] 2 4 2 * 4 = 8

[4, 2, 1] 3 4 3 * 4 = 12

[4, 2, 1, 2] 4 4 4 * 4 = 16

[2] 1 2 1 * 2 = 2

[2, 1] 2 2 2 * 2 = 4

[2, 1, 2] 3 2 3 * 2 = 6

[1] 1 1 1 * 1 = 1

[1, 2] 2 2 2 * 2 = 4

[2] 1 2 1 * 2 = 2

Sum == 59 ☕️

## Constraints

- `:)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
