# [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/)

**Medium** | **30 minutes** | **Depth-First Search, Breadth-First Search, Graph, Topological Sort**

**Pattern:** [Topological Sort](../patterns/topological_sort/intuition.md)

**Algorithm:** [Topological sorting](https://en.wikipedia.org/wiki/Topological_sorting) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/minimum_height_trees/solution.py`](../../practice/minimum_height_trees/solution.py)

A tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.

Given a tree of n nodes labelled from 0 to n - 1, and an array of n - 1 edges where `edges[i] = [ai, bi]` indicates that there is an undirected edge between the two nodes ai and bi in the tree, you can choose any node of the tree as the root. When you pick a node x as the root, the resulting tree has height h. Among all possible rooted trees, those with minimum height h are called **minimum height trees** (MHTs).

Return a list of all MHTs' root labels. You can return the answer in **any order**.

The **height** of a rooted tree is the number of edges on the longest downward path between the root and a leaf.

## Examples

### Example 1

![Tree Example 1](assets/minimum_height_trees_example1.jpg)

**Input:** `n = 4, edges = [[1,0],[1,2],[1,3]]`

**Output:** `[1]`

**Explanation:** As shown, the height of the tree is 1 when the root is the node with label 1 which is the only MHT.

### Example 2

![Tree Example 2](assets/minimum_height_trees_example2.jpg)

**Input:** `n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]`

**Output:** `[3,4]`

**Explanation:** The tree can be rooted at nodes 3 or 4 to achieve minimum height of 2.

## Constraints

- `1 <= n <= 2 * 10^4`
- `edges.length == n - 1`
- `0 <= ai, bi < n`
- `ai != bi`
- All the pairs `(ai, bi)` are distinct.
- The given input is **guaranteed** to be a tree and there will be **no repeated** edges.

