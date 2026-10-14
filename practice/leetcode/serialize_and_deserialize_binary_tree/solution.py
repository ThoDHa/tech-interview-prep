"""Serialize and Deserialize Binary Tree — https://leetcode.com/problems/serialize-and-deserialize-binary-tree/

Write-up & approaches: ../../docs/problems/serialize_and_deserialize_binary_tree.md

Design a codec that serializes a binary tree to a string and deserializes that
string back into the identical tree (the round-trip must reproduce the tree).

  uv run python serialize_and_deserialize_binary_tree/solution.py   # debug one case (see CASE below)
  uv run pytest serialize_and_deserialize_binary_tree/              # run the test sets
"""

from typing import Optional

from harness import NotSolved, TreeNode, build_tree, pick_case, tree_to_list


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in serialize/deserialize above, then run
    # this file. The case stores the tree as a level-order array; we marshal it to
    # TreeNode, round-trip it through your Codec, and serialize the result back to
    # an array to compare. Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    arr = case["args"][0]
    print(f"case {case['id']}: tree = {arr}")
    print(f"expected: {case['expected']}")
    try:
        codec = Codec()
        restored = codec.deserialize(codec.serialize(build_tree(arr)))
        print(f"got:      {tree_to_list(restored)}")
    except NotSolved:
        print("got:      implement Codec.serialize and Codec.deserialize first")
