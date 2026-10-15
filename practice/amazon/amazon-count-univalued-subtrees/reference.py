"""Count Uni-Valued Subtrees — https://www.fastprep.io/problems/amazon-count-univalued-subtrees

Write-up & approaches: ../../../docs/amazon/amazon-count-univalued-subtrees.md

Canonical reference implementation: the write-up's Single-Pass Postorder
solution (bottom-up report with one comparison per edge). Your own
attempt lives in solution.py.

Given the root of a binary tree, return the number of subtrees whose nodes all have the same value.

Every node defines one subtree consisting of that node and all of its descendants. A leaf is therefore always a uni-valued subtree.

  uv run python amazon/amazon-count-univalued-subtrees/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-count-univalued-subtrees/                          # run the test sets
"""

from typing import Optional

from harness import TreeNode, build_tree


class Solution:
    def countUnivalSubtrees(self, root: Optional[TreeNode]) -> int:
        """Count the subtrees whose nodes all share one value.

        Recurses children first; each node combines its children's
        reports into a verdict with one value comparison per edge. A
        subtree rooted at `node` is uni-valued exactly when both
        children's subtrees are uni-valued and each present child's root
        value equals `node.val`. The `None` base case returns `True`, so
        an absent child counts as an agreeing one and leaves qualify
        without a special case. Qualifying nodes are counted on the way
        up via the shared `unival_count` cell.

        Args:
            root: Root of the tree; may be None (an empty tree has no
                subtrees and counts 0).

        Returns:
            The number of uni-valued subtrees in the tree.

        Time:  O(n): one visit per node with a constant number of
            comparisons per visit.
        Space: O(h): recursion stack bounded by the tree's height.
        """
        unival_count = 0

        def report(node: Optional[TreeNode]) -> bool:
            nonlocal unival_count
            if node is None:
                return True
            left_report = report(node.left)
            right_report = report(node.right)
            left_agrees = node.left is None or (
                left_report and node.left.val == node.val
            )
            right_agrees = node.right is None or (
                right_report and node.right.val == node.val
            )
            if left_agrees and right_agrees:
                unival_count += 1
            return left_agrees and right_agrees

        report(root)
        return unival_count


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countUnivalSubtrees above, then
    # run this file. cases.json is empty (not JSON-representable input), so
    # a literal example stands in.
    values = [5, 1, 5, 5, 5, None, 5]
    result = Solution().countUnivalSubtrees(build_tree(values))
    print(f"args = root = {values}")
    print(f"expected: 4")
    print(f"got:      {result}")
