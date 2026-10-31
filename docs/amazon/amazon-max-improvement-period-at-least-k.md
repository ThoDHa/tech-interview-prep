# [Best Improvement Period of at Least K Intervals](https://www.fastprep.io/problems/amazon-max-improvement-period-at-least-k)

**Medium** | **NN minutes** | **Array, Prefix Sum, Dynamic Programming**

A machine learning team tracks how a recommendation model changes over n consecutive time intervals. You are given an integer array changes of length n, where changes[i] is the change in recommendation quality during interval i compared with the interval before it. A positive value is an improvement and a negative value is a decline. You are also given an integer k.

Choose a non-empty period of consecutive intervals [i, j], where 0 <= i <= j < n. The period must contain at least k intervals, so j - i + 1 >= k. Its cumulative improvement is:

## Examples

### Example 1

**Input:** `changes = [3,-2,5,-1,4]`, `k = 2`

**Output:** `10`

**Explanation:** Choose the period [1, 4], which has 4 intervals. Its first change -2 is subtracted, so the score is -(-2) + 5 + (-1) + 4 = 10.

Starting on a decline helps here, because subtracting a negative change adds to the score. The full period [0, 4] scores only -3 + (-2) + 5 + (-1) + 4 = 3, and no other period of at least 2 intervals scores more than 10.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-max-improvement-period-at-least-k; fill them in. -->

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
