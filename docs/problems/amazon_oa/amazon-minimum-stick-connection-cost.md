# [Minimum Stick Connection Cost](https://www.fastprep.io/problems/amazon-minimum-stick-connection-cost)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given an integer array sticks, where each element is the length of a stick.

You may connect any two sticks with lengths x and y. The new stick has length x + y, and the cost of this operation is also x + y.

Return the minimum total cost required to connect all sticks into one stick.

## Examples

### Example 1

**Input:** `sticks = [2, 4, 3]`

**Output:** `14`

**Explanation:** Connect 2 and 3 for cost 5, then connect 5 and 4 for cost 9. The total cost is 14.

### Example 2

**Input:** `sticks = [1, 8, 3, 5]`

**Output:** `30`

**Explanation:** One optimal sequence is 1 + 3 = 4, then 4 + 5 = 9, then 8 + 9 = 17, for total cost 4 + 9 + 17 = 30.

## Constraints

- `1 <= sticks.length <= 10^4`
- `1 <= sticks[i] <= 10^4`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
