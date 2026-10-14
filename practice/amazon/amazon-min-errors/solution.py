"""Minimum Total Errors — https://www.fastprep.io/problems/amazon-min-errors

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-min-errors.md

See the Image Source section for the original statement :)

  uv run python amazon_oa/amazon-min-errors/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-min-errors/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minTotalErrors(self, errorString, x, y):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minTotalErrors above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minTotalErrors(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
