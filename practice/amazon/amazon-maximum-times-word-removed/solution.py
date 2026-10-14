"""Maxmimum Times Word Removed — https://www.fastprep.io/problems/amazon-maximum-times-word-removed

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-times-word-removed.md

Special thanks: kcho and ketchup contributed this problem and example.

  uv run python amazon_oa/amazon-maximum-times-word-removed/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-times-word-removed/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumTimesWordRemoved(self, s, t):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumTimesWordRemoved above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumTimesWordRemoved(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
