"""Lowest Common Ancestor in an Inserted BST — https://www.fastprep.io/problems/amazon-bst-lowest-common-ancestor

Write-up & approaches: ../../../docs/amazon/amazon-bst-lowest-common-ancestor.md

Build a binary search tree by inserting the distinct values of insertionOrder from left to right. For each insertion, values smaller than the current node go left and larger values go right.

  uv run python amazon_oa/amazon-bst-lowest-common-ancestor/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-bst-lowest-common-ancestor/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def bstLowestCommonAncestor(self, insertionOrder, p, q):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in bstLowestCommonAncestor above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().bstLowestCommonAncestor(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
