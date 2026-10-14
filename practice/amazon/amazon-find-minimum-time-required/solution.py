"""Find Min Time Required — https://www.fastprep.io/problems/amazon-find-minimum-time-required

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-minimum-time-required.md

Some developers at Amazon are building a prototype for a simple rate-limiting algorithm. There are n requests to be processed by the server represented by a string requests where the ith character rep

  uv run python amazon_oa/amazon-find-minimum-time-required/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-minimum-time-required/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findMinimumTimeRequired(self, requests, minGap):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findMinimumTimeRequired above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findMinimumTimeRequired(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
