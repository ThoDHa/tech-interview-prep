# [Get Min Moves](https://www.fastprep.io/problems/amazon-get-min-moves)

**Medium** | **NN minutes** | **Bit Manipulation, Greedy**

Developers at Amazon are working on a new algorithm using the Bitwise XOR operation.



Given an array arr of even length n, Developers can perform an operation on a given array which is defined below as many times as necessary:


Choose two indices L and R, where 0 ≤ L ≤ R < N.Let x be the bitwise XOR of all elements of the subarray represented by indices L and R of the given array.Assign all elements of the chosen subarray to x.
Given an integer array arr[], find the minimum number of elements of the required to make all operations given array equal to zero.



Note: Bitwise XOR for an array of numbers is determined by counting each bit position across all numbers in the array. If the total count of set bits at a bit-position is odd, the resulting bit in output is set to 1. Otherwise, the resulting bit is set to 0..



Complete the function getMinMoves in the editor below. getMinMoves has the following parameter(s):



int arr[n]: the array

int: the minimum number of moves to make all elements of the array equal to zero



𓇼 ⋆.˚All Credit Goes to Spike!𓆝  𓆡⋆.˚ 𓇼

## Examples

### Example 1

**Input:** `arr = [0, 2, 2, 0]`

**Output:** `1`

**Explanation:** Choose L = 1 and R = 2. This corresponds to the subarray [2, 2]. The value of x for [2, 2] is 0. We replace the elements with 0 making all elements 0. Hence, the minimum number of operations required is 1.

### Example 2

**Input:** `arr = [0, 2, 3, 0, 2]`

**Output:** `2`

**Explanation:** This example could be invalid given that the problem statement saying the input arr len is supposed to be even..

## Constraints

- `n is supposed to be even`
- `0 ≤ arr[i] < 2^20`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
