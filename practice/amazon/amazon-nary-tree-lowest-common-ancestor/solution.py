"""Lowest Common Ancestor in an N-ary Tree — https://www.fastprep.io/problems/amazon-nary-tree-lowest-common-ancestor

Write-up & approaches: ../../../docs/amazon/amazon-nary-tree-lowest-common-ancestor.md

A rooted N-ary tree has nodes labeled from 0 through n - 1. It is encoded by parent, where parent[root] = -1 and every other value gives the node's direct parent.

  uv run python amazon/amazon-nary-tree-lowest-common-ancestor/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-nary-tree-lowest-common-ancestor/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def lowestCommonAncestor(self, parent, p, q):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in lowestCommonAncestor above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().lowestCommonAncestor(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
