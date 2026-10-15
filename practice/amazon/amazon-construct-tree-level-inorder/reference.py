"""Construct a Tree from Level-Order and Inorder Traversals — https://www.fastprep.io/problems/amazon-construct-tree-level-inorder

Write-up & approaches: ../../../docs/amazon/amazon-construct-tree-level-inorder.md

Canonical reference implementation: the write-up's Hash Map Partition
solution (dictionary lookups, membership split, recursion). Your own
attempt lives in solution.py.

Given the levelOrder and inorder traversals of the same binary tree, reconstruct and return its root.

All node values are distinct. Both arrays contain the same values, and together they describe exactly one valid binary tree.

  uv run python amazon/amazon-construct-tree-level-inorder/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-construct-tree-level-inorder/                          # run the test sets
"""

from typing import Dict, List, Optional

from harness import TreeNode, tree_to_list


class Solution:
    def buildTree(self, levelOrder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """Rebuild the binary tree from its level-order and inorder traversals.

        The first level-order value of any subtree is its root, and the
        inorder split places everything left of the root's position in
        the left subtree, everything right of it in the right subtree.
        A dictionary built once from `inorder` answers every root lookup
        in O(1). The remaining level-order values are routed by
        membership, not arrival order: a value belongs left exactly when
        the inorder split put it left of the root. Level-order arrival
        order must never substitute for that test, because level-order
        values do not group by subtree position (left-leaning trees
        interleave the sides). Values are distinct and both traversals
        describe one tree, so the rebuilt structure is unique.

        Args:
            levelOrder: Level-order traversal, at least one value; all
                values distinct.
            inorder: Inorder traversal of the same tree, the same value
                set.

        Returns:
            The root of the reconstructed binary tree.

        Time:  O(n^2) worst case: root lookups are O(1), but building
            the left-side membership set reads an O(n) inorder slice per
            recursion node on a skewed tree.
        Space: O(n): the position dictionary, the per-call level lists
            and membership sets, plus the O(h) recursion stack.
        """
        inorder_position: Dict[int, int] = {
            value: position for position, value in enumerate(inorder)
        }

        def build(in_start: int, in_end: int, level: List[int]) -> Optional[TreeNode]:
            if not level:
                return None
            root_value = level[0]
            root = TreeNode(root_value)
            root_position = inorder_position[root_value]
            left_inorder_values = {
                inorder[position] for position in range(in_start, root_position)
            }
            left_level: List[int] = []
            right_level: List[int] = []
            for value in level[1:]:
                if value in left_inorder_values:
                    left_level.append(value)
                else:
                    right_level.append(value)
            root.left = build(in_start, root_position - 1, left_level)
            root.right = build(root_position + 1, in_end, right_level)
            return root

        return build(0, len(inorder) - 1, levelOrder)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in buildTree above, then run this
    # file. cases.json is empty (not JSON-representable input), so a
    # literal example stands in.
    level_order = [3, 9, 20, 15, 7]
    inorder = [9, 3, 15, 20, 7]
    result = Solution().buildTree(level_order, inorder)
    print(f"args = levelOrder = {level_order}, inorder = {inorder}")
    print(f"expected: [3, 9, 20, None, None, 15, 7]")
    print(f"got:      {tree_to_list(result)}")
