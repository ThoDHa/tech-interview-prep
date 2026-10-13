# [Find Minimum Time](https://www.fastprep.io/problems/amazon-find-minimum-time)

**Medium** | **NN minutes** | **Array, Sorting, Greedy**

In the context of an Amazon gaming product involving a snake and apples on a number line, the product simulates a set of unique coordinates representing the positions of the apples. The array named position of size n holds these unique integers, each denoting the coordinate of the nth apple.



The snake, starting at the origin (0 coordinate), decides to consume some of the apples. The snake can move left and right along the line at a constant speed of 1 unit/sec, allowing it to transition from a coordinate x to y (or y to x) in |y - x| seconds. Additionally, the snake can instantly eat an apple when it occupies the same coordinate as the apple.



Given an integer k and the array position, Determine the minimum time required for the snake to consume at least k apples.

## Examples

### Example 1

**Input:** `n = 3`, `k = 3`, `position = [-20, 5, 10]`

**Output:** `40`

**Explanation:** It is optimal to choose the following way:



Initially, the snake is at coordinate 0. As the snake needs to eat all three apples,It will first go right for 5 seconds and eat the apple at position 5.It moves in the same direction for another 5 seconds to reach coordinate 10 and eat the apple there.Now it moves left for 30 seconds to reach the coordinate -20 and eat the apple there.
Time taken will be 5 + 5 + 30 = 40 seconds.
It can be shown that it is not possible for the snake to eat all the apples in less than 40 seconds.
Hence, the answer is 40.

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 <= k <= n`
- `| position[i]| <= 10^8 OR −10^8 ≤ position[i] ≤ 10^8`
- `The array position consists of distinct integers.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
