"""Nodes at a Given N-ary Tree Level — https://www.fastprep.io/problems/amazon-nary-tree-nodes-at-level

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-nary-tree-nodes-at-level.md

An N-ary tree uses node IDs from 0 through children.length - 1, with root ID 0. For each node ID, children[id] lists its child IDs from left to right.

  uv run python amazon_oa/amazon-nary-tree-nodes-at-level/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-nary-tree-nodes-at-level/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def nodesAtLevel(self, children, level):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in nodesAtLevel above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().nodesAtLevel(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
