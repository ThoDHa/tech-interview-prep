"""Binary Tree Right View — https://www.fastprep.io/problems/amazon-binary-tree-right-view

Write-up & approaches: ../../../docs/amazon/amazon-binary-tree-right-view.md

Canonical reference implementation: the write-up's Iterative BFS
solution (level-size snapshot, last dequeue per level). Your own
attempt lives in solution.py.

Given the root of a binary tree, imagine viewing the tree from its right side.

Return the value of the visible node at each depth, ordered from the root level downward. For an empty tree, return an empty array.

  uv run python amazon/amazon-binary-tree-right-view/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-binary-tree-right-view/                          # run the test sets
"""

from collections import deque
from typing import List, Optional

from harness import TreeNode, build_tree


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        """Return the rightmost node's value on every level, top down.

        Processes the tree one level at a time: the queue is snapshotted
        as `level_size` before the level drains, and the node dequeued at
        index `level_size - 1` is the level's rightmost node, which is
        precisely the one a viewer on the right sees. Children are
        enqueued left before right, so each next level stays ordered left
        to right and "last of the level" keeps meaning "rightmost". The
        explicit queue is also immune to the recursion limit a skewed
        10,000-node input would trigger in the DFS variants.

        Args:
            root: Root of the tree; may be None (no visible levels).

        Returns:
            The right-side view, one value per depth, root level first.

        Time:  O(n): each of the n nodes is enqueued and dequeued exactly
            once with constant work.
        Space: O(n): the queue holds at most one full level, which is
            O(n) wide on a complete tree.
        """
        if root is None:
            return []

        visible: List[int] = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            for position_in_level in range(level_size):
                node = queue.popleft()
                if position_in_level == level_size - 1:
                    visible.append(node.val)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
        return visible


if __name__ == "__main__":
    # Debug playground: set a breakpoint in rightSideView above, then run
    # this file. cases.json is empty (not JSON-representable input), so a
    # literal example stands in.
    values = [1, 2, 3, None, 5, None, 4]
    result = Solution().rightSideView(build_tree(values))
    print(f"args = root = {values}")
    print(f"expected: [1, 3, 4]")
    print(f"got:      {result}")
