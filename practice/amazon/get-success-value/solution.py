"""Get Success Value — https://www.fastprep.io/problems/get-success-value

Write-up & approaches: ../../../docs/problems/amazon_oa/get-success-value.md

Amazon Prime Video has recently released an exclusive series on its platform. They collected the number of viewers from n

  uv run python amazon_oa/get-success-value/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/get-success-value/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findSuccessValue(self, num_viewers, queries):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findSuccessValue above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findSuccessValue(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
