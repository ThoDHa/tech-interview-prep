# [Min Time to Create Beautiful Canvas](https://www.fastprep.io/problems/amazon-find-minimum-time-to-create-beautiful-canvas)

**Hard** | **NN minutes** | **Matrix, Binary Search, Prefix Sum**

Amazon is introducing an innovative smart canvas display for personalized home decor. The canvas is initially painted white, featuring n rows and m columns, waiting to be transformed into a beautiful masterpiece. Each minute, the canvas undergoes a unique coloring process as specified by the user.



A beautiful canvas is defined by the presence of a square with a side length of k where all cells within the square are elegantly colored.



Determine the minimum time required for the canvas to achieve its beauty.



Formally, Given n and m that denote the number of rows and columns of the canvas respectively, k denotes the size of the square, and a 2D array paint of dimensions (n * m) rows and 2 columns, where each entry (paint[i][0], paint[i][1]) represents the coordinates of a cell to be painted black during the ith minute.



Note that each cell is painted only once during this transformation.



Find the minimum time (in minutes) after which the canvas becomes beautiful.

## Examples

### Example 1

**Input:** `n = 2`, `m = 3`, `k = 2`, `paint = [[1, 2], [2, 3], [2, 1], [1, 3], [2, 2], [1, 1]]`

**Output:** `5`

**Explanation:** After the 5th and 6th minutes, the canvas has a square of size 2*2 with all black cells starting at position (1, 2) at minute 5, and two squares at (1,1) and (1,2) at minute 6, so the minimum time after which the canvas becomes beautiful is 5 minutes.

## Constraints

- `1 ≤ n, m ≤ 750`
- `1 ≤ k ≤ min(n, m)`
- `1 ≤ paint[i][0] ≤ n`
- `1 ≤ paint[i][1] ≤ m`
- `paint[i] ≠ paint[j] for any 1 ≤ i < j ≤ n*m`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
