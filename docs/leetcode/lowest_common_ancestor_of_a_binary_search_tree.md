# [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)

**Medium** | **20 minutes** | **Binary Search Tree, Tree, Recursion**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor) · [Binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree)

**Practice:** [`practice/lowest_common_ancestor_of_a_binary_search_tree/solution.py`](../../practice/lowest_common_ancestor_of_a_binary_search_tree/solution.py)

Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.

According to the definition of LCA on Wikipedia: "The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself)."

## Examples

### Example 1

![Lowest Common Ancestor Tree Example](assets/lowest_common_ancestor_binary_search_tree_example1.png)

**Input:** `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 8`

**Output:** `6`

**Explanation:** The LCA of nodes `2` and `8` is `6`.

### Example 2

![Lowest Common Ancestor Tree Example](assets/lowest_common_ancestor_binary_search_tree_example1.png)

**Input:** `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 4`

**Output:** `2`

**Explanation:** The LCA of nodes `2` and `4` is `2`, since a node can be a descendant of itself according to the LCA definition.

### Example 3

**Input:** `root = [2,1]`, `p = 2`, `q = 1`

**Output:** `2`

## Constraints

- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`
- `p` and `q` will exist in the BST.

## Deriving the Solution

The lowest common ancestor is the node where the root-to-`p` path and the root-to-`q` path part ways: the two paths share a prefix from the root down, and the last node of that shared prefix is the LCA. Every solution below finds that divergence point; they differ in how much of the tree they must inspect to locate it.

1. **Start literal.** Build both root-to-target paths explicitly with a DFS,
   then walk them in lockstep until they disagree. Two full searches and two stored paths cost `O(n)` time and space: see [Brute Force DFS](#brute-force-dfs).
2. **Spot the waste.** The paths are only ever compared, never kept. One
   post-order traversal can detect the split directly: a node whose left and right subtrees each report one target is the divergence point. Still `O(n)` time, but no path storage: see [Generic Post-Order DFS](#generic-post-order-dfs).
3. **Use the ordering.** Both previous approaches ignore that this tree is a
   BST. Comparing `p.val` and `q.val` against a node's value tells us which side both targets lie on, so the divergence point can be found by walking a single root-to-LCA path in `O(h)`: see [Recursive Using BST Properties](#recursive-using-bst-properties).
4. **Drop the stack.** That descent is tail-recursive: each call makes at most
   one further call and returns its result unchanged, so a simple loop replaces the recursion and the `O(h)` call stack becomes `O(1)`: see [Iterative Using BST Properties](#iterative-using-bst-properties).

## Solutions

### Brute Force DFS

#### Derivation

The most direct idea, without relying on any tree property, is to find the full path from the root down to each target, then compare the two paths. The [lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor) is simply the last node the two paths share before they diverge. This works on any binary tree because it only uses parent-to-child links, not value ordering.

1. For each target, run a DFS that returns the list of nodes from `root` down to that target, recording a node only on the branch that actually reaches the target.
2. Walk the two paths in parallel from the root.
3. Track the last node both paths agree on; stop at the first position where they differ.
4. Return that last shared node as the LCA.

Because the problem guarantees both nodes exist, each DFS finds a non-empty path, and the two paths share at least the root.

#### Walkthrough

Let us trace this brute force on Example 1: `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 8`. The tree looks like this:

```text
          6
        /   \
       2     8
      / \   / \
     0   4 7   9
        / \
       3   5
```

**Step 1: build the path to `p = 2` with `find_path(root, 2)`.** Each call returns a node only on the branch that actually reaches the target:

| Call | `node.val` | What happens | Returns |
| --- | --- | --- | --- |
| `find_path(6, 2)` | `6` | not target. Recurse left into `2` | `[6] + [2]` = `[6, 2]` |
| `find_path(2, 2)` | `2` | `node.val == target.val`, base case | `[2]` |

So `path_p = [6, 2]`.

**Step 2: build the path to `q = 8` with `find_path(root, 8)`:**

| Call | `node.val` | What happens | Returns |
| --- | --- | --- | --- |
| `find_path(6, 8)` | `6` | not target. Left subtree `2` returns `[]`, so recurse right into `8` | `[6] + [8]` = `[6, 8]` |
| `find_path(8, 8)` | `8` | `node.val == target.val`, base case | `[8]` |

So `path_q = [6, 8]`.

**Step 3: walk both paths in lockstep, tracking the last shared node.** `lca` starts as `root` (`6`):

| Step | `node_p.val` | `node_q.val` | Match? | `lca` after |
| --- | --- | --- | --- | --- |
| 1 | `6` | `6` | yes | `6` |
| 2 | `2` | `8` | no, `break` | `6` |

The paths agree on `6`, then diverge at `2` versus `8`, so the loop breaks. The function returns `lca = 6`, which matches the expected Output `6`.

#### Solution

The code is the walkthrough's three steps written down: two path searches, then the lockstep comparison.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List


class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        # Collect the root-to-target path for each node, ignoring BST ordering.
        def find_path(node: TreeNode, target: TreeNode) -> List[TreeNode]:
            if node is None:
                return []
            if node.val == target.val:
                return [node]
            left = find_path(node.left, target)
            if left:
                return [node] + left
            right = find_path(node.right, target)
            if right:
                return [node] + right
            return []

        path_p = find_path(root, p)
        path_q = find_path(root, q)

        # Walk both paths in lockstep; the last shared node is the LCA.
        lca = root
        for node_p, node_q in zip(path_p, path_q):
            if node_p.val == node_q.val:
                lca = node_p
            else:
                break
        return lca
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. Each `find_path` call may visit every node in the worst case, and comparing the paths is bounded by the tree height, so the total is linear.

##### Space Complexity: `O(n)`

Both paths together store up to `O(h)` nodes, and the recursion stack reaches depth `O(h)`; in the worst case of a skewed tree this is `O(n)`.

#### Key Insights

- Works for any binary tree, not only BSTs, because it relies on paths rather than value ordering.
- The LCA is exactly the divergence point of the two root-to-target paths.
- Building explicit paths is wasteful, but it makes the definition of LCA concrete and easy to verify.

### Generic Post-Order DFS

#### Derivation

This refines the brute force by collapsing the two separate path searches into a single traversal that never builds explicit path lists. It still ignores the BST ordering and works for any binary tree, searching both subtrees with a [post-order traversal](https://en.wikipedia.org/wiki/Tree_traversal). If each subtree reports back one target, the current node is the split point and therefore the LCA. If only one subtree reports a target, the LCA lies entirely within that subtree.

1. Return `None` for an empty subtree.
2. If the current node matches `p` or `q`, return it as a candidate.
3. Recurse into both children.
4. If both children return non-`None`, the targets diverge here, so return the current node.
5. Otherwise propagate whichever child found a target upward.

Because a matching node short-circuits its subtree, a node that is itself an ancestor of the other target is returned correctly without descending further.

#### Walkthrough

Let us run the single traversal on Example 1: `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 8`, the tree

```text
          6
        /   \
       2     8
      / \   / \
     0   4 7   9
        / \
       3   5
```

The indentation below shows the recursion; each call either matches a target and returns immediately, or waits for both children to report:

```text
lowestCommonAncestor(6)    6 is neither 2 nor 8; recurse into both sides
  lowestCommonAncestor(2)  2 == p.val -> return node 2   (0 and 4 never visited)
  lowestCommonAncestor(8)  8 == q.val -> return node 8   (7 and 9 never visited)
back at 6: left = 2, right = 8, both non-None -> return 6
```

The left recursion stops the instant it lands on `2`: a matching node short-circuits its whole subtree, so `0`, `4`, `3`, `5` are never examined. Likewise the right recursion returns `8` without touching `7` or `9`. Back at the root, `left` and `right` are both non-`None`, meaning one target was found on each side, so `6` is the split point and is returned. That matches the expected Output `6`, with no path list ever built.

#### Solution

The code is the walkthrough's report-and-combine step: match, recurse both sides, and return the node where both sides answer.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        if root is None:
            return None
        # Finding either target here makes root a candidate ancestor.
        if root.val == p.val or root.val == q.val:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # Targets found on both sides: root is the split point.
        if left and right:
            return root
        # Otherwise the LCA is whichever side returned a node.
        return left or right
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. Without the BST ordering, the search may visit every node in the tree.

##### Space Complexity: `O(h)`

The recursion stack can grow as deep as the height of the tree, but no separate path lists are stored.

#### Key Insights

- Works for any binary tree, not only BSTs, at the cost of efficiency.
- Post-order traversal: children are resolved before the current node decides.
- A node equal to one target short-circuits, naturally handling the ancestor-of-itself case.
- Trims the brute force's two passes and explicit path storage into a single recursion.

### Recursive Using BST Properties

#### Derivation

Both previous approaches treat the tree as an arbitrary binary tree and may scan all of it. This solution leverages the [Binary Search Tree](https://en.wikipedia.org/wiki/Binary_search_tree) property: values smaller than a node sit in its left subtree, and values greater sit in its right subtree. We navigate down the tree, recursing into one side only when both targets fall on that side. The first node where the targets diverge (one on each side, or one equal to the node itself) is the lowest common ancestor.

1. Compare both `p.val` and `q.val` against `root.val`.
2. If both are smaller, recurse into `root.left`.
3. If both are larger, recurse into `root.right`.
4. Otherwise the targets split here, so `root` is the LCA. Return it.

Because the problem guarantees both nodes exist in the BST, the recursion always reaches a valid split point and never falls off the tree.

#### Walkthrough

Let us descend through Example 2, which needs more than one step and exercises the ancestor-of-itself case: `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 4`, the tree

```text
          6
        /   \
       2     8
      / \   / \
     0   4 7   9
        / \
       3   5
```

Each call compares both target values against `root.val` and picks exactly one direction, or stops:

```text
lowestCommonAncestor(6)    p.val=2 < 6 and q.val=4 < 6   both smaller -> recurse left
  lowestCommonAncestor(2)  p.val=2 < 2? no.  p.val=2 > 2? no.  -> split: return node 2
```

At the root, both `2` and `4` are smaller than `6`, so the entire right half of the tree is dismissed without a glance and the search moves to `2`. There, neither comparison holds: `p.val` equals the node's value, so the targets no longer lie strictly on one side. That is the split condition, and `2` is returned: `p` is its own ancestor and `q = 4` sits in its right subtree. The result matches the expected Output `2`, reached after inspecting just two nodes.

#### Solution

The code is the walkthrough's three-way comparison, applied once per level of the descent.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        # Both targets smaller than root: the LCA lives in the left subtree.
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)
        # Both targets larger than root: the LCA lives in the right subtree.
        if p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)
        # Targets straddle root, or one equals root: root is the LCA.
        return root
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(h)`

Where `h` is the height of the tree. Each call descends one level, so we make at most `h` calls before reaching the split point. For a balanced BST this is `O(log n)`; for a skewed tree it degrades to `O(n)`.

##### Space Complexity: `O(h)`

The recursion stack can grow as deep as the height of the tree.

#### Key Insights

- The BST ordering invariant lets us pick a direction without exploring both subtrees.
- Each step eliminates roughly half of the remaining tree in the balanced case.
- We only walk the path from the root to the divergence point, never the whole tree.

### Iterative Using BST Properties

#### Derivation

The recursive descent has a telling shape: every call either returns immediately or returns whatever its single recursive call returns. Nothing happens after the recursion, so the call stack is dead weight. This solution uses the same [BST](https://en.wikipedia.org/wiki/Binary_search_tree) logic as the recursive approach but replaces the call stack with a single loop. We start at the root and descend, moving left when both targets are smaller than the current node and right when both are larger. The first node where the targets diverge (or where one of them equals the current node) is the LCA.

1. Set `current` to `root`.
2. While `current` is not `None`, compare both target values against `current.val`.
3. Move `current` left or right while both targets fall on the same side.
4. Return `current` as soon as the targets split.

The loop is guaranteed to terminate at a real node because both targets exist in the tree, so a split point always appears before we run off the end.

#### Walkthrough

Let us re-run Example 2 as a loop: `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 4`, the same tree drawn in the recursive walkthrough above. The single pointer `current` starts at the root, and each line is one loop iteration:

```text
current = 6   p.val=2 < 6 and q.val=4 < 6      -> current = current.left = 2
current = 2   2 < 2? no.  2 > 2? no.           -> split: return current = 2
```

The comparisons are identical to the recursive version; the only difference is that instead of a recursive call carrying the answer back up, `current` is reassigned in place. The loop stops at node `2`, where the targets no longer fall on one side, and returns it: the expected Output `2`, computed with one pointer and no stack.

#### Solution

The code is the walkthrough's loop: reassign `current` while both targets sit on one side, return it at the split.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        current = root
        while current:
            # Both targets smaller than current: go left.
            if p.val < current.val and q.val < current.val:
                current = current.left
            # Both targets larger than current: go right.
            elif p.val > current.val and q.val > current.val:
                current = current.right
            # Split point reached: current is the LCA.
            else:
                return current
        return None
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(h)`

Same as the recursive approach: at most one iteration per level of the tree, where `h` is the height.

##### Space Complexity: `O(1)`

Only a single pointer is tracked, independent of input size, since there is no recursion or auxiliary structure.

#### Key Insights

- Eliminates recursion overhead and the stack space it consumes.
- Identical decision logic to the recursive version, just driven by a loop.
- Preferred for very deep or skewed trees, where the recursive stack could grow large.

## Comparison of Solutions

### Time Complexity

- **Brute Force DFS**: `O(n)`: searches for both targets' paths, possibly visiting every node.
- **Generic Post-Order DFS**: `O(n)`: a single traversal that may still visit every node.
- **Recursive Using BST Properties**: `O(h)`: leverages the BST property to navigate directly to the split point.
- **Iterative Using BST Properties**: `O(h)`: the same path as the recursive version, without stack overhead.

### Space Complexity

- **Brute Force DFS**: `O(n)`: stores explicit root-to-target paths plus the recursion stack.
- **Generic Post-Order DFS**: `O(h)`: recursion stack proportional to tree height, no path lists.
- **Recursive Using BST Properties**: `O(h)`: recursion stack proportional to tree height.
- **Iterative Using BST Properties**: `O(1)`: only a single pointer of extra state.

### Trade-offs

- Brute Force DFS makes the LCA definition concrete by comparing paths, but wastes time and space building those paths explicitly.
- Generic Post-Order DFS trims the path storage into one traversal and works on any binary tree, but still ignores the BST ordering and may scan every node.
- The BST solutions are significantly more efficient for this specific problem but require the binary search tree property.
- The iterative solution provides the best space efficiency but might be slightly less readable.

### When to Use Each

- **Brute Force DFS**: As a teaching baseline that makes the LCA definition explicit.
- **Generic Post-Order DFS**: When the tree doesn't have the BST property, or when writing a general utility function.
- **Recursive Using BST Properties**: When dealing with a BST and code readability is prioritized.
- **Iterative Using BST Properties**: When dealing with a BST and memory efficiency is important, or for very deep trees.

### Optimization Notes

- The BST property allows us to eliminate about half the tree at each step, dropping from `O(n)` to `O(h)`.
- The iterative solution avoids recursion overhead and is generally preferred for production environments.
- For very unbalanced trees (approaching a linked list), even the BST approach could degrade to `O(n)` time complexity.
