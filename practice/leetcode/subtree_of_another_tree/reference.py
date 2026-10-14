"""Subtree of Another Tree — https://leetcode.com/problems/subtree-of-another-tree/

Write-up & approaches: ../../docs/problems/subtree_of_another_tree.md

Canonical reference implementation: the write-up's Subtree Serialization
Set solution (one lossless fingerprint per subtree, one membership test).
Your own attempt lives in solution.py.

Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise.

  uv run python subtree_of_another_tree/reference.py   # debug one case (see below)
  uv run pytest subtree_of_another_tree/               # run the test sets
"""

from typing import Optional

from harness import TreeNode, build_tree


class Solution:
    def isSubtree(self, root: TreeNode, subRoot: TreeNode) -> bool:
        """Report whether `subRoot` appears inside `root` as a subtree.

        Every subtree of `root` is serialized bottom-up into a
        self-delimiting string (a leading comma per token, `,#` for a
        missing child) and recorded in a set as it is composed. `subRoot`
        matches some subtree exactly when its serialization is in that set,
        so the whole anchor scan collapses into one membership test.

        Args:
            root: Root of the tree to search, never None (constraints
                guarantee at least one node).
            subRoot: Root of the candidate subtree, never None.

        Returns:
            True when a structurally and by-value identical subtree of
            `root` exists, False otherwise.

        Time:  O(n * h_root + m * h_sub): each serialization string costs
               its own subtree's length to compose; the membership test
               compares one string against the set.
        Space: O(n * h_root): the set stores every subtree's serialization.
        """

        def serialize(node: Optional[TreeNode]) -> str:
            if node is None:
                return ",#"
            return f",{node.val}" + serialize(node.left) + serialize(node.right)

        serials = set()

        def collect(node: Optional[TreeNode]) -> str:
            if node is None:
                return ",#"
            serial = f",{node.val}" + collect(node.left) + collect(node.right)
            serials.add(serial)
            return serial

        collect(root)
        return serialize(subRoot) in serials


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isSubtree above, then run this
    # file. cases.json is empty (multi-method starter), so literal examples
    # stand in.
    root_values = [1, 2, 3, 4, 5]
    sub_values = [2, 4, 5]
    result = Solution().isSubtree(build_tree(root_values), build_tree(sub_values))
    print(f"args = root = {root_values}, subRoot = {sub_values}")
    print(f"expected: True")
    print(f"got:      {result}")
