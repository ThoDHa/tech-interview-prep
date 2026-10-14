"""Maximum Sum BST in a Binary Tree — https://www.fastprep.io/problems/amazon-maximum-sum-bst

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-sum-bst.md

Given the root of a binary tree, find the maximum sum of node values among all subtrees that are valid binary search trees.

  uv run python amazon_oa/amazon-maximum-sum-bst/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-sum-bst/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxSumBST(self, root):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxSumBST above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxSumBST(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
