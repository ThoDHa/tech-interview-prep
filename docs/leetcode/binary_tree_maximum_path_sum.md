# [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

**Hard** | **35 minutes** | **Tree**

**Pattern:** [Tree DP](../patterns/tree_dp/intuition.md)

**Algorithm:** [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)

**Practice:** [`practice/binary_tree_maximum_path_sum/solution.py`](../../practice/binary_tree_maximum_path_sum/solution.py)

A **path** in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence **at most once**. Note that the path does not need to pass through the root.

The **path sum** of a path is the sum of the node's values in the path.

Given the `root` of a binary tree, return the **maximum path sum** of any **non-empty** path.

## Examples

### Example 1

![Binary Tree Maximum Path Sum Example1](assets/binary_tree_maximum_path_sum_example1.jpg)

**Input:** `root = [1,2,3]`

**Output:** `6`

**Explanation:** The optimal path is `2 -> 1 -> 3` with a path sum of `2 + 1 + 3 = 6`.

### Example 2

![Binary Tree Maximum Path Sum Example2](assets/binary_tree_maximum_path_sum_example2.jpg)

**Input:** `root = [-10,9,20,null,null,15,7]`

**Output:** `42`

**Explanation:** The optimal path is `15 -> 20 -> 7` with a path sum of `15 + 20 + 7 = 42`.

## Constraints

- The number of nodes in the tree is in the range `[1, 3 * 10^4]`.
- `-1000 <= Node.val <= 1000`

## Deriving the Solution

Every path in a tree has a unique highest node: the point where it bends from one subtree into the other, or from which it descends one side only. Fixing that bend point decomposes the path into the node itself plus at most one downward path into each child, so both solutions reduce the problem to measuring best downward paths.

1. **Start literal.** Try every node as the bend point: for each candidate,
   measure the best downward path into its left and right subtrees with a helper, and keep the largest `node.val + left_gain + right_gain`. Correct, but the helper re-walks whole subtrees for every candidate, costing `O(n^2)`: see [Brute Force](#brute-force).
2. **Spot the waste.** The helper's answer for a node never changes between
   calls, yet the brute force recomputes it once for the node itself and once more for every one of its ancestors.
3. **Compute each gain once.** A post-order traversal finishes both children
   before their parent, so each node can record its own bent sum and hand its downward gain up to the parent in the same visit. One pass replaces the nested re-walks, reaching `O(n)`: see [Post-Order DFS](#post-order-dfs).

## Solutions

### Brute Force

#### Derivation

The problem asks for the best path anywhere in the tree, which is hard to grab directly. The reformulation that makes it tractable is to ask, for each node, "what is the best path whose *highest* point is this node?": every path has exactly one highest node where it bends from one branch into the other (or stays straight on one side), so taking the maximum over all bend points covers every path exactly once. For a fixed bend the two halves are independent: the best downward descent into the left subtree and the best downward descent into the right subtree. The most direct plan measures those descents from scratch for each candidate:

1. Define `max_down(node)`: the largest sum of a path that starts at `node` and
   descends through at most one child. Clamp the chosen child at `0` so a negative branch is simply skipped.
2. For each node in the tree, compute the best left descent and best right
   descent, then form `node.val + left_gain + right_gain` as the path that bends at this node.
3. Track the maximum of these bent sums in `self.best` across every node and
   return it.

This recomputes `max_down` from scratch at every node, which is wasteful but needs no insight beyond the definition of a path.

#### Walkthrough

Let us trace the Brute Force on Example 1: the tree `[1,2,3]`, where `1` is the root with left child `2` and right child `3`. We expect the answer `6`.

`self.best` starts at `-inf`. The call `visit(root)` walks the tree as a call tree, and for each node it asks `max_down` to measure the best downward path into each child:

```text
visit(1):
    max_down(2): leaf, returns 2 + max(0, 0, 0) = 2
    max_down(3): leaf, returns 3 + max(0, 0, 0) = 3
    left_gain  = max(2, 0) = 2
    right_gain = max(3, 0) = 3
    bent sum   = 1 + 2 + 3 = 6   ->  best = max(-inf, 6) = 6
    visit(2):
        no children, left_gain = right_gain = 0
        bent sum = 2 + 0 + 0 = 2  ->  best = max(6, 2) = 6
    visit(3):
        no children, left_gain = right_gain = 0
        bent sum = 3 + 0 + 0 = 3  ->  best = max(6, 3) = 6
```

The table below shows `self.best` after each node is visited as a bend point:

| Node visited | `left_gain` | `right_gain` | bent sum | `self.best` |
|--------------|-------------|--------------|----------|-------------|
| `1` (root)   | `2`         | `3`          | `6`      | `6`         |
| `2`          | `0`         | `0`          | `2`      | `6`         |
| `3`          | `0`         | `0`          | `3`      | `6`         |

The best bend happens at the root, where the path descends into both children: `2 -> 1 -> 3`. After every node has been tried, `visit` returns and the method returns `self.best`, which is `6`: matching the expected Output.

#### Solution

The code is the walkthrough's two nested recursions: `visit` enumerates the bend points and `max_down` measures each descent.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # Best downward path that starts at node and descends one side only.
        # Negative branches are dropped by clamping at 0.
        def max_down(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            return node.val + max(max_down(node.left), max_down(node.right), 0)

        self.best = float("-inf")

        # Try every node as the highest point (the "bend") of the path.
        def visit(node: Optional[TreeNode]) -> None:
            if not node:
                return
            left_gain = max(max_down(node.left), 0)
            right_gain = max(max_down(node.right), 0)
            self.best = max(self.best, node.val + left_gain + right_gain)
            visit(node.left)
            visit(node.right)

        visit(root)
        return self.best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

`visit` touches all `n` nodes, and at each node `max_down` walks the entire subtree below it. In a skewed tree this is `O(n)` work per node, giving `O(n^2)` in the worst case.

##### Space Complexity: `O(h)`

Both recursions descend at most to the tree height `h` at once: `O(log n)` for a balanced tree and `O(n)` for a skewed one.

#### Key Insights

- Naming the bend point as the path's highest node makes the enumeration
  concrete: every path is counted exactly once, at its peak.
- `max_down` already captures the "drop a negative branch" rule by clamping at
  `0`, the same rule the optimal solution reuses.
- The waste is purely the repeated `max_down` calls; the gain values it produces
  do not change between visits, which is exactly what the next solution exploits.

### Post-Order DFS

#### Derivation

The Brute Force wastes its time in one place: `max_down(node)` is recomputed for every ancestor of `node`, even though its value never changes. The repair is to compute each node's downward gain exactly once and let its parent reuse it, which a single [post-order traversal](https://en.wikipedia.org/wiki/Tree_traversal) makes possible: children finish before their parent, so the parent can combine the freshly computed child gains on the spot.

The price of merging the two recursions is keeping two quantities apart. A maximum path can take two shapes at any node: it can **bend** through the node, descending into both the left and right subtrees, or it can **pass straight through**, continuing up to the node's parent on only one side. Only the straight shape may be handed upward, because a bent path already uses both children. So the recursion returns the best straight (single-side) path while a global maximum captures the best bent path seen anywhere:

1. Define `max_gain(node)` to return the largest sum of a downward path that
   starts at `node` and goes through at most one child. An empty node contributes `0`.
2. Recurse into both children, clamping each gain with `max(..., 0)`. If a
   subtree's best contribution is negative, we drop it: a single positive node beats a node plus a negative branch.
3. The best path that *peaks* at this node is `node.val + left_gain +
   right_gain`. Compare it against the running global `max_sum`.
4. Return `node.val + max(left_gain, right_gain)` to the parent, because a path
   the parent extends can only pass through one of this node's sides.

Tracking the bent sum separately from the returned straight sum is what lets the single traversal consider every possible path.

#### Recurrence

Two different quantities are in play, and separating them is the whole trick. Let \(g(v)\) be the best sum of a path that starts at `v` and only descends (the value `max_gain` returns):

$$ g(v) = v.\text{val} + \max\bigl(0,\ g(v.\text{left}),\ g(v.\text{right})\bigr), \qquad g(\text{null}) = 0 $$

```text
max_gain(null) = 0
max_gain(v)    = v.val + max(0, max_gain(v.left), max_gain(v.right))
```

Let \(b(v)\) be the best path whose highest point is `v`, which may bend into both subtrees:

$$ b(v) = v.\text{val} + \max\bigl(0, g(v.\text{left})\bigr) + \max\bigl(0, g(v.\text{right})\bigr) $$

```text
b(v) = v.val + max(0, max_gain(v.left)) + max(0, max_gain(v.right))
```

The answer maximizes \(b\) over every node, since any path has exactly one highest point:

$$ \text{answer} = \max_{v \in T} b(v) $$

```text
max_sum = max(b(v)) over all nodes v in T
```

The clamp at \(0\) encodes "a negative branch is better skipped than taken." \(b(v)\) cannot be returned upward: a bent path already uses both children, so extending it through the parent would revisit `v` and no longer be a path. That asymmetry is why the recursion returns \(g\) while \(b\) accumulates into a separate running maximum.

#### Walkthrough

Let us trace the traversal on Example 2: `root = [-10,9,20,null,null,15,7]`, where the best path avoids the root entirely. `self.max_sum` starts at `-inf`, and post-order means every node's children resolve before the node itself:

```text
        -10
        /  \
       9    20
           /  \
         15    7

max_gain(9)      leaf: left_gain = right_gain = 0
                 bent sum 9 + 0 + 0 = 9          max_sum = 9
                 returns 9 + max(0, 0) = 9
max_gain(15)     leaf: bent sum 15               max_sum = 15
                 returns 15
max_gain(7)      leaf: bent sum 7                max_sum stays 15
                 returns 7
max_gain(20)     left_gain = 15, right_gain = 7
                 bent sum 20 + 15 + 7 = 42       max_sum = 42
                 returns 20 + max(15, 7) = 35
max_gain(-10)    left_gain = max(9, 0) = 9
                 right_gain = max(35, 0) = 35
                 bent sum -10 + 9 + 35 = 34      max_sum stays 42
                 returns -10 + 35 = 25           (discarded by the caller)
```

The bent sum at `20` uses both of its children (`15 -> 20 -> 7`), which is why `42` is recorded in `max_sum` but only the straight sum `35` travels up to the root. At the root, even the best bent sum `34` loses to `42`, because the `-10` drags it down. The method returns `max_sum = 42`, matching the expected Output and the optimal path `15 -> 20 -> 7`.

#### Solution

The code is the single traversal from the walkthrough: each call records its bent sum into `max_sum` and returns its straight sum.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float("-inf")

        def max_gain(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            # Best downward path from each child, clamped at 0 so a
            # negative branch is simply dropped rather than dragging us down
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)

            # A path that bends through this node uses both children
            self.max_sum = max(self.max_sum, node.val + left_gain + right_gain)

            # But a path returned to the parent can only descend one side
            return node.val + max(left_gain, right_gain)

        max_gain(root)
        return self.max_sum
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited once, performing constant work (two comparisons and two additions) per visit.

##### Space Complexity: `O(h)`

The recursion stack grows with the tree height `h`: `O(log n)` for a balanced tree and `O(n)` for a skewed one.

#### Key Insights

- The path returned upward and the path measured for the answer differ: only the
  measured one may use both children, since a node can appear at most once.
- Clamping negative gains to `0` cleanly expresses "skip this branch" without
  special-casing.
- Initializing `max_sum` to negative infinity is required because every value
  can be negative and the path must be non-empty.
- One post-order traversal suffices: children must be evaluated before the
  parent can decide its best bent and straight sums.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - recomputes the downward maximum for every node, re-walking each subtree.
- **Post-Order DFS**: `O(n)` - one traversal computes every node's gain exactly once.

### Space Complexity

- **Brute Force**: `O(h)` - two stacked recursions, each bounded by the tree height.
- **Post-Order DFS**: `O(h)` - a single recursion bounded by the tree height.

### Trade-offs

- Brute Force gains a direct mental model (every node is a candidate bend point) but repeats the same downward-path work at every node.
- Post-Order DFS gives up the separate enumeration pass by returning each node's gain to its parent, computing the answer in a single sweep.

### When to Use Each

- **Brute Force**: As a teaching baseline that makes the "bend at the highest node" idea explicit.
- **Post-Order DFS**: The recommended default; linear time on inputs up to `3 * 10^4` nodes.

### Optimization Notes

- The key optimization is recognizing that `max_down(node)` does not change between visits, so it can be returned upward during the same traversal that measures the bent sums.
- Both solutions share the clamp-at-`0` rule to drop negative branches and both initialize the global best to negative infinity, since every node value can be negative and the path must be non-empty.
