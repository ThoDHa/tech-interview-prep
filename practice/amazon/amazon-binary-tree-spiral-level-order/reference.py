"""Binary Tree Spiral Level Order — https://www.fastprep.io/problems/amazon-binary-tree-spiral-level-order

Write-up & approaches: ../../../docs/amazon/amazon-binary-tree-spiral-level-order.md

Reference implementation of the write-up's recommended Level-Size BFS
solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-binary-tree-spiral-level-order/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-binary-tree-spiral-level-order/              # run the test sets
"""

from collections import deque
from typing import List, Optional

from harness import TreeNode, build_tree, pick_case


class Solution:
    def zigzagLevels(self, root: Optional[TreeNode]) -> List[List[int]]:
        """Return the tree's values one level per list, alternating direction.

        A queue drains the tree one level at a time: before a level
        drains, its nodes are snapshotted in left-to-right order, so the
        snapshot of their values is exactly the level read left to
        right. Even depths (0-based) are kept as snapshotted and odd
        depths are reversed, which alternates the reading direction
        starting left to right at the root. Children enqueue left before
        right, so every next snapshot starts ordered left to right.

        Args:
            root: The tree's root node, or None for an empty tree.

        Returns:
            One list of node values per level, root level first; an
            empty tree yields an empty list.

        Time:  O(n): every node is enqueued once, dequeued once, and its
            value copied once.
        Space: O(n): the output holds all n values and the queue holds
            at most one level, which is O(n) wide on a complete tree.
        """
        levels: List[List[int]] = []
        frontier: deque = deque([root] if root is not None else [])

        while frontier:
            level_values = [node.val for node in frontier]
            levels.append(level_values[::-1] if len(levels) % 2 else level_values)
            for _ in range(len(frontier)):
                node = frontier.popleft()
                if node.left is not None:
                    frontier.append(node.left)
                if node.right is not None:
                    frontier.append(node.right)

        return levels


if __name__ == "__main__":
    # Debug playground: set a breakpoint in zigzagLevels above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().zigzagLevels(build_tree(case["args"][0]))
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
