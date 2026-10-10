"""Maximize Consecutive Equal Answers — https://www.fastprep.io/problems/amazon-maximize-answer-key-confusion

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-answer-key-confusion.md

A string contains only T and F. You may change at most maxChanges characters. Return the maximum length of a contiguous substring that can be made entirely equal.

  uv run python amazon_oa/amazon-maximize-answer-key-confusion/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-answer-key-confusion/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximizeConfusion(self, answers, maxChanges):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximizeConfusion above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximizeConfusion(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
