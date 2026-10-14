"""Count Uni-Valued Subtrees — https://www.fastprep.io/problems/amazon-count-univalued-subtrees

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-univalued-subtrees.md

Given the root of a binary tree, return the number of subtrees whose nodes all have the same value.

  uv run python amazon_oa/amazon-count-univalued-subtrees/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-univalued-subtrees/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countUnivalSubtrees(self, root):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countUnivalSubtrees above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countUnivalSubtrees(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
