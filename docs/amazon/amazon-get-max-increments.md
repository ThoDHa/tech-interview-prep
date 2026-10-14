# [Get Max Increments](https://www.fastprep.io/problems/amazon-get-max-increments)

**Easy** | **NN minutes** | **Array, Sorting, Greedy**

IMDB, an Amazon-owned company, is a widely used platform for discovering scores of films and television series.



Researchers are examining audience preferences by studying sequences of film scores. One specific metric they focus on is counting how many positions exist where a score is directly followed by a higher score. Their goal is to determine the largest possible count of such positions by rearranging the scores in the most efficient manner.



Given an array scores consisting of n integers, compute the highest possible number of indices i such that scores[i] < scores[i + 1] after optimally reordering the array.

## Examples

### Example 1

**Input:** `scores = [2, 1, 3]`

**Output:** `2`

### Example 2

**Input:** `scores = [2, 1, 1, 2]`

**Output:** `2`

**Explanation:** In this scenairo, an optimal arrangement of the arr scores is [1, 2, 1, 2].

The indices i such that scores[i] < scores[i + 1], are [0, 1].

So answer is 2.

P.S. This test cases was added on 04-13-2025 :) Relevant ss was attached in the Problem Source section.

### Example 3

**Input:** `scores = [2, 3, 1, 5, 4]`

**Output:** `4`

**Explanation:** In this case, an very optimal arrangement of the arr scores is [1, 2, 3, 4, 5].

the indices i such that scores[i] < scores[i + 1], are [0, 1, 2, 3].

So answer is 4.

P.S. This test cases was added on 04-13-2025 :) Relevant ss was attached in the Problem Source section.

## Constraints

- `2 ≤ n ≤ 2 * 10^5`
- `1 ≤ scores[i] ≤ 2 * 10^5`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
