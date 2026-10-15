"""Root-to-Leaf Paths with a Target Sum — https://www.fastprep.io/problems/amazon-root-to-leaf-target-sum-paths

Write-up & approaches: ../../../docs/amazon/amazon-root-to-leaf-target-sum-paths.md

Canonical reference implementation: the write-up's Backtracking with a
Shared Path solution (append on entry, pop on exit, one copy per match).
Your own attempt lives in solution.py.

Given the root of a binary tree and an integer targetSum, return every root-to-leaf path whose node values add up to targetSum.

A leaf has no children. Return paths in left-to-right depth-first order, with each path listed from the root to its leaf.

  uv run python amazon/amazon-root-to-leaf-target-sum-paths/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-root-to-leaf-target-sum-paths/                          # run the test sets
"""

from typing import List, Optional

from harness import TreeNode, build_tree


class Solution:
    def pathSum(self, root: Optional[TreeNode], target_sum: int) -> List[List[int]]:
        """Return every root-to-leaf path summing to target_sum.

        Carries one shared `path` list down the recursion as a stack of
        the current route: a node's value is appended on entry and popped
        on exit, and the running total `remaining` is threaded through
        the calls. The only copy happens once, at a leaf whose remaining
        total hits 0, so each matching path is materialized exactly once.
        Left-to-right output order falls out of recursing into the left
        child before the right. Negative node values make the total dip
        and recover, so `remaining < 0` must never prune; only the leaf
        check decides.

        Args:
            root: Root of the tree; may be None (no root-to-leaf path
                exists).
            target_sum: The sum every returned path must add up to.

        Returns:
            The matching root-to-leaf paths, each root-first, in
            left-to-right depth-first order.

        Time:  O(n + matches * h): every node is appended and popped
            exactly once, and each matching path is copied once at its
            leaf.
        Space: O(h): the shared path and the recursion stack, plus the
            returned lists.
        """
        matching: List[List[int]] = []
        path: List[int] = []

        def dfs(node: Optional[TreeNode], remaining: int) -> None:
            if node is None:
                return
            path.append(node.val)
            remaining -= node.val
            if node.left is None and node.right is None:
                if remaining == 0:
                    matching.append(path.copy())
            else:
                dfs(node.left, remaining)
                dfs(node.right, remaining)
            path.pop()

        dfs(root, target_sum)
        return matching


if __name__ == "__main__":
    # Debug playground: set a breakpoint in pathSum above, then run this
    # file. cases.json is empty (not JSON-representable input), so a
    # literal example stands in.
    values = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
    target = 22
    result = Solution().pathSum(build_tree(values), target)
    print(f"args = root = {values}, targetSum = {target}")
    print(f"expected: [[5, 4, 11, 2], [5, 8, 4, 5]]")
    print(f"got:      {result}")
