# [Fortune Telling](https://www.fastprep.io/problems/amazon-minimize-the-range)

**Hard** | **NN minutes** | **Sliding Window, Sorting, Greedy**

Given a collection of n cards. The i-th card (1 ≤ i ≤ n) has a number Ai on its front and a number Bi on its back. At the start, all the cards are facing upwards. He wants to minimize the range of numbers (i.e. the difference between the maximum and minimum values) on the face-up side. He is allowed to flip a maximum of m cards. Flipping a card will transition Bi to the face up side and Ai to the back. Help him find the minimum possible range after using at most m flips.



Input



The first line of the input consists of 2 integers n and m. The next line contains n integers, i-th of which denotes Ai. The next line contains n integers, i-th of which denotes Bi.



Output



Output a single integer, the minimum possible range.

## Examples

### Example 1

**Input:** `n = 5`, `m = 2`, `A = [1, 2, 17, 16, 9]`, `B = [3, 4, 5, 6, 11]`

**Output:** `8`

**Explanation:** By flipping card 3 and 4, we get the face up numbers {1, 2, 5, 6, 9}. This makes range=9-1=8.

## Constraints

- `1 <= m <= n`
- `1 <= Ai, Bi <= 107`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
