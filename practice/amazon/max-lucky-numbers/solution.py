"""Max Lucky Numbers — https://www.fastprep.io/problems/max-lucky-numbers

Write-up & approaches: ../../../docs/problems/amazon_oa/max-lucky-numbers.md

Amazon.com is distributing coupons in the form of a lottery system for loyal customers. The coupons are called "lucky numbers" and the customer with the largest lucky number gets the best discount. De

  uv run python amazon_oa/max-lucky-numbers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/max-lucky-numbers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxLuckyNumber(self, x, y, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxLuckyNumber above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxLuckyNumber(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
