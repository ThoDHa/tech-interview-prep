# [Find Ideal Days](https://www.fastprep.io/problems/amazon-find-ideal-days)

**Medium** | **NN minutes** | **Array, Sliding Window**

A virtual assistant is being given a feature that recommends ideal days for fishing from a rainfall forecast.

A day is ideal when rainfall is non-increasing throughout the previous window days leading to that day and non-decreasing throughout the following window days.

Given the predicted rainfall for the next n days in forecast, find every ideal day. Formally, an array index i is ideal when:

forecast[i - window] ≥ forecast[i - window + 1] ≥ … ≥ forecast[i - 1] ≥ forecast[i] ≤ forecast[i + 1] ≤ … ≤ forecast[i + window - 1] ≤ forecast[i + window]

Return the ideal day numbers in ascending order. Array index i represents day i + 1, so returned day numbers are 1-based. At least one ideal day is guaranteed.

## Examples

### Example 1

**Input:** `forecast = [3, 2, 2, 2, 3, 4]`, `window = 2`

**Output:** `[3, 4]`

**Explanation:** With window = 2, day 3 satisfies 3 ≥ 2 ≥ 2 ≤ 2 ≤ 3, and day 4 satisfies 2 ≥ 2 ≥ 2 ≤ 3 ≤ 4. Therefore, return [3, 4].

### Example 2

**Input:** `forecast = [1, 0, 1, 0, 1]`, `window = 1`

**Output:** `[2, 4]`

**Explanation:** With window = 1, day 2 satisfies 1 ≥ 0 ≤ 1, and day 4 satisfies 1 ≥ 0 ≤ 1. Therefore, return [2, 4].

### Example 3

**Input:** `forecast = [1, 0, 0, 0, 1]`, `window = 2`

**Output:** `[3]`

**Explanation:** Day 3 is the only day with two complete days on both sides, and it satisfies 1 ≥ 0 ≥ 0 ≤ 0 ≤ 1. Therefore, return [3].

### Example 4

**Input:** `forecast = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]`, `window = 3`

**Output:** `[4, 5, 6, 7]`

**Explanation:** All rainfall values are equal, so equality satisfies both required trends. Every day with three complete days on both sides is ideal: days 4, 5, 6, and 7.

## Constraints

- `1 ≤ window ≤ n ≤ 2 × 10^5`
- `0 ≤ forecast[i] ≤ 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
