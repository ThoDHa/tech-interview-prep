# [Find Maximum Calories](https://www.fastprep.io/problems/amazon-find-maximum-calories)

**Hard** | **NN minutes** | **Array, Math, Greedy**

You start on the ground at height 0. There are n stones, and stone i has height height[i].

You must visit every stone exactly once, in any order. After jumping from the ground to the first stone, you cannot return to the ground. A jump between heights x and y burns (x - y)² calories.

Return the maximum total calories that can be burned.

## Examples

### Example 1

**Input:** `height = [5, 2, 5]`

**Output:** `43`

**Explanation:** Use the order ground 0 → third stone 5 → second stone 2 → first stone 5. The total is (0 - 5)² + (5 - 2)² + (2 - 5)² = 25 + 9 + 9 = 43, which is optimal.

## Constraints

- `1 ≤ n ≤ 10^5`
- `height.length = n`
- `1 ≤ height[i] ≤ 46340`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
