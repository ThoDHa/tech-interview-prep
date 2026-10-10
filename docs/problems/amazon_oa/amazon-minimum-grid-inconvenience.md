# [Minimum Grid Inconvenience](https://www.fastprep.io/problems/amazon-minimum-grid-inconvenience)

**Hard** | **NN minutes** | **Matrix, Breadth First Search, Binary Search**

A city is represented by a binary grid. A cell marked 1 is a delivery center, and a cell marked 0 is any other place.

The distance between two cells is the maximum of the absolute row-coordinate difference and the absolute column-coordinate difference. The inconvenience of the grid is the maximum, over every 0 cell, of its distance to the nearest delivery center.

Amazon may open one new delivery center by converting at most one 0 cell into 1. Return the minimum possible inconvenience after this conversion.

## Examples

### Example 1

**Input:** `grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]`

**Output:** `2`

**Explanation:** With no existing delivery center, it is optimal to convert the center cell (1,1) to 1. The farthest cells then have distance 2.

### Example 2

**Input:** `grid = [[0]]`

**Output:** `0`

**Explanation:** Convert the only cell to a delivery center, leaving no 0 cell with positive distance.

## Constraints

- `1 <= n, m <= 500`
- `0 <= grid[i][j] <= 1`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
