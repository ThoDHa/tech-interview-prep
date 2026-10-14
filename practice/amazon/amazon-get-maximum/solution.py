"""Get Maximum — https://www.fastprep.io/problems/amazon-get-maximum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-maximum.md

Amazon Fresh is a grocery store designed from the ground up to offer a seamless grocery shopping experience to consumers. As part of a stock clearance exercise at the store, given the number of fresh 

  uv run python amazon_oa/amazon-get-maximum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-maximum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaximum(self, numProducts):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaximum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaximum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
