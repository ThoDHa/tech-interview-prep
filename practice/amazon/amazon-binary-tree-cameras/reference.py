"""Binary Tree Cameras — https://www.fastprep.io/problems/amazon-binary-tree-cameras

Write-up & approaches: ../../../docs/amazon/amazon-binary-tree-cameras.md

Canonical reference implementation: the write-up's Greedy Postorder
Placement solution (three-status decision, root fix last). Your own
attempt lives in solution.py.

You are given the root of a binary tree. You may install cameras on its nodes.

A camera installed at a node monitors that node, its parent if one exists, and its immediate children.

Return the minimum number of cameras needed so that every node in the tree is monitored.

  uv run python amazon/amazon-binary-tree-cameras/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-binary-tree-cameras/                          # run the test sets
"""

from typing import Optional

from harness import TreeNode, build_tree

HAS_CAMERA, COVERED, NEEDS_COVER = 0, 1, 2


class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        """Place the fewest cameras so every node is monitored.

        Runs a postorder pass whose single decision reads only the two
        children's statuses. A `None` child returns `COVERED`, which
        removes every presence check: leaves fall out of the same
        three-way rule as interior nodes. When either child
        `NEEDS_COVER`, this node must carry the camera itself (there is
        nobody below left to watch that child), which covers the child,
        itself, and its parent. Otherwise a `HAS_CAMERA` child already
        watches this node; otherwise only the parent can, so the node
        reports `NEEDS_COVER`. The root has no parent, so a root that
        still reports `NEEDS_COVER` takes one final camera.

        Args:
            root: Root of the tree; never None (constraints guarantee at
                least one node).

        Returns:
            The minimum number of cameras that monitor every node.

        Time:  O(n): one postorder visit per node with constant decision
            work each.
        Space: O(h): recursion stack bounded by the tree's height.
        """
        camera_count = 0

        def place_from_bottom(node: Optional[TreeNode]) -> int:
            nonlocal camera_count
            if node is None:
                return COVERED
            left_status = place_from_bottom(node.left)
            right_status = place_from_bottom(node.right)
            if left_status == NEEDS_COVER or right_status == NEEDS_COVER:
                camera_count += 1
                return HAS_CAMERA
            if left_status == HAS_CAMERA or right_status == HAS_CAMERA:
                return COVERED
            return NEEDS_COVER

        if place_from_bottom(root) == NEEDS_COVER:
            camera_count += 1
        return camera_count


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minCameraCover above, then run
    # this file. cases.json is empty (not JSON-representable input), so a
    # literal example stands in.
    values = [0, 0, None, 0, 0]
    result = Solution().minCameraCover(build_tree(values))
    print(f"args = root = {values}")
    print(f"expected: 1")
    print(f"got:      {result}")
