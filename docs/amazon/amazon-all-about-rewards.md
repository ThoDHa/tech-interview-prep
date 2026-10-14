# [All About Rewards](https://www.fastprep.io/problems/amazon-all-about-rewards)

**Medium** | **NN minutes** | **Array, Sorting**

SDE II



Amazon Shopping is running a reward collection event for its customers.



There are n customers and the i-th customer has collected initialRewards[i] points so far.



One final tournament is to take place where:


The champion earns n additional pointsThe second place earns n - 1 pointsThe third place earns n - 2 points… and the last place earns 1 point
Given an integer array initialRewards of length n, representing the initial reward points of the customers before the final tournament:



Find the number of customers i (1 ≤ i ≤ n) such that, if the i-th customer wins the final tournament, they would have the highest total points.



Note -



The total points = initialRewards[i] + n (if they win).

Other customers also get points in the tournament depending on their ranks (from n - 1 to 1).

You must check if the i-th customer, upon winning, ends up with the highest total score, regardless of how others place.

## Examples

### Example 1

**Input:** `initialRewards = [1, 3, 4]`, `n = 3`

**Output:** `2`

**Explanation:** $24

### Example 2

**Input:** `initialRewards = [5, 7, 9, 11]`, `n = 4`

**Output:** `1`

**Explanation:** Only the 4th customer is the one such that, if they win the final tournament, they would have the highest total points.

### Example 3

**Input:** `initialRewards = [8, 10, 9]`, `n = 3`

**Output:** `2`

**Explanation:** Only the 2nd and the 3rd customers are the ones such that, if they win the final tournament, they would have the highest total points.

If the 2nd customer wins the final tournament, their total points would be: 10 + 3 = 13, and this is the highest total points, as there are no other customers that can achieve the total point of 13 in this case.

If the 3rd customer wins the final tournament, their total points would be: 9 + 3 = 12, and this is the highest total points in this case.

Even if the 2nd customer with an initial reward of 10 comes 2nd, then they would achieve a total of: 10 + 2 = 12 points which is not greater than 2nd customer points.

## Constraints

- `1 ≤ n ≤ 10^5`
- `0 ≤ initialRewards[i] ≤ 10^5`
- `Complete constraints added on 06-18-2025`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
