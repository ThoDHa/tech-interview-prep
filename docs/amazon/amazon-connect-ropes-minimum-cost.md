# [Connect N Ropes With Minimum Cost](https://www.fastprep.io/problems/amazon-connect-ropes-minimum-cost)

**Medium** | **NN minutes** | **Heap, Greedy**

You are given an integer array ropes, where ropes[i] is the length of one rope.

In one operation, choose any two ropes, connect them into one rope, and pay a cost equal to the sum of their lengths. The new rope has that same combined length.

Return the minimum total cost required to connect all ropes into one rope. If there is only one rope, return 0.

## Examples

### Example 1

**Input:** `ropes = [4,3,2,6]`

**Output:** `29`

**Explanation:** Connect lengths 2 and 3 for cost 5, then 4 and 5 for cost 9, and finally 6 and 9 for cost 15. The total is 5 + 9 + 15 = 29.

### Example 2

**Input:** `ropes = [4,2,7,6,9]`

**Output:** `62`

**Explanation:** One optimal sequence has merge costs 6, 12, 16, and 28, for a total of 62.

### Example 3

**Input:** `ropes = [10]`

**Output:** `0`

**Explanation:** Only one rope is present, so no connection operation is needed.

## Constraints

- `1 <= ropes.length <= 10^5`
- `1 <= ropes[i] <= 10^4`
- `The result fits in a signed 64-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
