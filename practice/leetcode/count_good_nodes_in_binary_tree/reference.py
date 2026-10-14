"""Count Good Nodes In Binary Tree — https://leetcode.com/problems/count-good-nodes-in-binary-tree/

Write-up & approaches: ../../docs/problems/count_good_nodes_in_binary_tree.md

Canonical reference implementation: the write-up's Recursive DFS solution
(the path maximum threaded as a parameter). Your own attempt lives in
solution.py.

Within a binary tree, a node `x` is considered good if the path from the root to `x` contains no nodes with a value greater than `x`'s. Return the number of good nodes.

  uv run python count_good_nodes_in_binary_tree/reference.py   # debug one case (see below)
  uv run pytest count_good_nodes_in_binary_tree/               # run the test sets
"""

from typing import Optional

from harness import TreeNode, build_tree


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        """Count nodes at least as large as every ancestor on their path.

        A depth-first walk threads `max_so_far` (the largest value on the
        path from the root to the node's parent) into every visit. A node is
        good when its own value meets that maximum, and every child sees the
        maximum updated with the current node's value regardless of the
        node's own verdict, because a bad node still raises the bar for its
        descendants.

        Args:
            root: Root of the tree, never None (constraints guarantee at
                least one node).

        Returns:
            The number of good nodes in the tree.

        Time:  O(n): one visit per node with constant work each.
        Space: O(h): recursion stack bounded by the tree's height.
        """

        def dfs(node: Optional[TreeNode], max_so_far: int) -> int:
            if node is None:
                return 0
            good = 1 if node.val >= max_so_far else 0
            next_max = max(max_so_far, node.val)
            return good + dfs(node.left, next_max) + dfs(node.right, next_max)

        return dfs(root, root.val)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in goodNodes above, then run this
    # file. cases.json is empty (multi-method starter), so a literal example
    # stands in.
    values = [2, 1, 1, 3, None, 1, 5]
    result = Solution().goodNodes(build_tree(values))
    print(f"args = root = {values}")
    print(f"expected: 3")
    print(f"got:      {result}")
