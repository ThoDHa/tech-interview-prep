# [Sort Permutation](https://www.fastprep.io/problems/amazon-can-sort-permutation-in-given-moves)

**Medium** | **NN minutes** | **Math, Graph**

Amazon recently conducted interviews where the candidates were asked to sort the permutation p of length n. Then the ith candidate sorted the permutation in moves[i] moves. To verify the result once more, the interviewer wants to find if it is possible to sort the given permutation in the given number of moves. Given the original permutation array p and the number of moves made by each of the q candidates, find whether you can sort the permutation p by performing exactly moves[i] moves. In one move, you swap the value at any two distinct indexes. Return the answer as a binary string of length q. The value at the ith index should be 1 if it is possible to sort the permutation in exactly moves[i] moves, otherwise the value should be 0.



Note: A permutation is a sequence of n distinct integers such that each integer between [1, n] appears exactly once. For example, [1, 2, 3, 4] is a permutation of size 4, but [1, 3, 4, 5] or [1, 2, 2, 4] is not.

## Examples

### Example 1

**Input:** `p = [2, 3, 1, 4]`, `moves = [2, 3]`

**Output:** `"10"`

**Explanation:** The cycle (1, 2, 3) needs exactly two swaps, so query 2 succeeds. Every swap changes permutation parity, so an odd count of three cannot finish at the sorted permutation.

### Example 2

**Input:** `p = [4, 5, 1, 3, 2]`, `moves = [1, 2, 3]`

**Output:** `"001"`

**Explanation:** The permutation consists of cycles of lengths three and two, so it needs at least (3 - 1) + (2 - 1) = 3 swaps. Therefore one and two moves fail, while three moves succeed; for example, swap indexes (0, 2), then (1, 4), then (2, 3).

## Constraints

- `1 <= n <= 10^5`
- `1 <= q <= 10^5`
- `1 <= moves[i] <= 10^9`
- `It is guaranteed that p forms a permutation.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
