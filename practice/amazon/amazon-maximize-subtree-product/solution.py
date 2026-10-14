"""Maximize Subtree Product — https://www.fastprep.io/problems/amazon-maximize-subtree-product

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-subtree-product.md

You are given a mystical tree with n nodes. Each node is connected to at least one other node by an edge. Your task is to sever one or more edges in the tree to split it into subtrees. The goal is to 

  uv run python amazon_oa/amazon-maximize-subtree-product/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-subtree-product/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximizeSubtreeProduct(self, n, edges):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximizeSubtreeProduct above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximizeSubtreeProduct(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
