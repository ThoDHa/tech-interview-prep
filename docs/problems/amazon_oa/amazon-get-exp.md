# [Get Experience](https://www.fastprep.io/problems/amazon-get-exp)

**Easy** | **NN minutes** | **Sorting, Hash Table**

Note --> Feel free to check the source image below for the original problem statement :)



At a bustling tech company, there are n developers, each with their own set of experience points. The company is gearing up for an exciting hackathon and has come up with a unique way to form pairs of developers for the event. Their plan is to create pairs by matching the developer with the highest experience points with the one with the lowest experience points, and then move inward from both ends.



As the developers are paired, the company is interested in analyzing the combined experience of each pair. The combined experience of a pair is calculated as the average of the experience points of the two developers.



Your challenge is to determine how many unique values there are among these combined experience points.



In simpler terms, given the list of experience points for all developers, you need to find out how many distinct average values result from pairing the highest and lowest remaining experience points iteratively.

## Examples

### Example 1

**Input:** `exp = [1, 4, 1, 3, 5, 6]`

**Output:** `2`

**Explanation:** $24

### Example 2

**Input:** `exp = [1, 1, 1, 1, 1, 1]`

**Output:** `1`

**Explanation:** $25

### Example 3

**Input:** `exp = [1, 100, 10, 1000]`

**Output:** `2`

**Explanation:** The In a vibrant tech company, 4 developers are gearing up for a hackathon. To make things interesting, the company decides to pair them up in a unique way. They match the developer at index 0 with the one at index 3, and the developer at index 1 with the one at index 2.

Here’s how the pairs are formed:

The first pair consists of the developers at indices 0 and 3.
The second pair consists of the developers at indices 1 and 2.
After calculating the combined experience for each pair, you get:

The combined experience for the pair (0, 3) is 500.5.
The combined experience for the pair (1, 2) is 55.
When you look at these combined experience values, you find that there are 2 distinct values: 500.5 and 55.

Thus, the number of unique combined experience values among the pairs is 2.

## Constraints

- `2 ≤ n ≤ 10^5`
- `0 ≤ exp[i] ≤ 10^9`
- `n is an even number`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
