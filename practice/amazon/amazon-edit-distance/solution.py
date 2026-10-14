"""Edit Distance — https://www.fastprep.io/problems/amazon-edit-distance

Write-up & approaches: ../../../docs/amazon/amazon-edit-distance.md

Given two strings word1 and word2, return the minimum number of single-character operations needed to transform word1 into word2.

  uv run python amazon_oa/amazon-edit-distance/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-edit-distance/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minDistance(self, word1, word2):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minDistance above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minDistance(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
