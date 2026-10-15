"""Maximum Sum BST in a Binary Tree — https://www.fastprep.io/problems/amazon-maximum-sum-bst

Write-up & approaches: ../../../docs/amazon/amazon-maximum-sum-bst.md

Canonical reference implementation: the write-up's One-Pass Post-Order
DFS solution (a four-part validity report folded bottom-up). Your own
attempt lives in solution.py.

Given the root of a binary tree, find the maximum sum of node values among all subtrees that are valid binary search trees.

A valid BST has every left-subtree value strictly smaller than its root and every right-subtree value strictly larger. Return 0 when every valid non-empty BST subtree has a negative sum.

  uv run python amazon/amazon-maximum-sum-bst/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-maximum-sum-bst/                          # run the test sets
"""

from typing import Optional, Tuple

from harness import TreeNode, build_tree


class Solution:
    def maxSumBST(self, root: Optional[TreeNode]) -> int:
        """Return the maximum sum over all valid BST subtrees, 0 if none is positive.

        One post-order fold carries `(is_valid, subtree_min, subtree_max,
        subtree_sum)` up from every node. The `None` report
        `(True, +inf, -inf, 0)` composes correctly for leaves and
        one-sided subtrees with no special cases. A node is a valid BST
        exactly when both children report valid and
        `left_max < node.val < right_min` (strict on both sides, because
        equal values violate the BST definition); only on that branch is
        the composed sum folded into `max_bst_sum`, which is seeded at 0
        to encode the all-negative rule.

        Args:
            root: Root of the tree; may be None (no subtree exists, so
                the answer is 0).

        Returns:
            The largest sum over all valid BST subtrees, or 0 when no
            valid BST subtree has a positive sum.

        Time:  O(n): every node is visited once and combines its
            children's reports in O(1).
        Space: O(h): recursion stack bounded by the tree's height.
        """
        max_bst_sum = 0

        def postorder(node: Optional[TreeNode]) -> Tuple[bool, float, float, int]:
            nonlocal max_bst_sum
            if node is None:
                return (True, float("inf"), float("-inf"), 0)

            left_valid, left_min, left_max, left_sum = postorder(node.left)
            right_valid, right_min, right_max, right_sum = postorder(node.right)

            if left_valid and right_valid and left_max < node.val < right_min:
                subtree_min = min(left_min, node.val, right_min)
                subtree_max = max(left_max, node.val, right_max)
                subtree_sum = left_sum + node.val + right_sum
                max_bst_sum = max(max_bst_sum, subtree_sum)
                return (True, subtree_min, subtree_max, subtree_sum)

            return (False, 0.0, 0.0, 0)

        postorder(root)
        return max_bst_sum


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxSumBST above, then run this
    # file. cases.json is empty (not JSON-representable input), so a
    # literal example stands in.
    values = [1, 4, 3, 2, 4, 2, 5, None, None, None, None, None, None, 4, 6]
    result = Solution().maxSumBST(build_tree(values))
    print(f"args = root = {values}")
    print(f"expected: 20")
    print(f"got:      {result}")
