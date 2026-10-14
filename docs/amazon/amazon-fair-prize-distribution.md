# [Fair Prize Distribution](https://www.fastprep.io/problems/amazon-fair-prize-distribution)

**unknown difficulty** | **NN minutes** | **unknown categories**

A coding challenge has n participants. Participant i earned score points[i]. There are m available prizes, and values[j] is the value of the j-th prize.

Assign one prize value to each participant using the available prize multiset such that:

Participants with the same score receive the same prize value.Participants with higher scores receive strictly higher prize values than participants with lower scores.If multiple fair distributions are possible, return the lexicographically smallest distribution in the original participant order.

## Examples

### Example 1

**Input:** `points = [5,5,5]`, `values = [2,2,2,3,3,3]`

**Output:** `[2,2,2]`

**Explanation:** All participants have the same score, so they must receive equal prize values. [2,2,2] is lexicographically smaller than [3,3,3].

## Constraints

- `1 <= points.length, values.length <= 2 * 10^5`
- `1 <= points[i], values[i] <= 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
