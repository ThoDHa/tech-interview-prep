"""Get Maximum Count — https://www.fastprep.io/problems/amazon-get-maximum-count

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-maximum-count.md

Amazon has launched a "Play to Win" game where users get a chance to earn free gift vouchers. The game presents you with an array of integers (arr) and an integer k. You are allowed to choose any cont

  uv run python amazon_oa/amazon-get-maximum-count/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-maximum-count/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaximumCount(self, arr, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaximumCount above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaximumCount(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
