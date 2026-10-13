# [Cinema Shows](https://www.fastprep.io/problems/amazon-cinema-shows)

**Medium** | **NN minutes** | **Dynamic Programming, Binary Search, Intervals**

SDE II



A prominent media company (AMZ MGM) has partnered with select theaters to showcase exclusive video content, including feature films, episodic series, live performances, and more.



You are given an integer n, representing the number of scheduled screenings. Each screening has a start time, duration, and expected audience size, which are provided as integer arrays start, duration, and volume, respectively.



Your task is to determine the highest possible total audience size while ensuring that no two selected screenings overlap. Two screenings are considered non-overlapping if one fully concludes before the next one begins.

## Examples

### Example 1

**Input:** `start = [10, 5, 15, 18, 30]`, `duration = [20, 12, 20, 35, 35]`, `volume = [50, 51, 20, 25, 10]`

**Output:** `76`

### Example 2

**Input:** `start = [1, 2, 4]`, `duration = [2, 2, 1]`, `volume = [1, 2, 3]`

**Output:** `4`

**Explanation:** Will udpate once find more reliable resources :) As always 🐳

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ start[i] ≤ 10^9`
- `1 ≤ duration[i] ≤ 10^9`
- `1 ≤ volume[i] ≤ 10^3`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
