"""Currency Conversion Rate — https://www.fastprep.io/problems/amazon-currency-conversion-rate

Write-up & approaches: ../../../docs/amazon/amazon-currency-conversion-rate.md

You are given currency conversion rates. Each row contains a source currency, a target currency, and the value of one unit of the source currency in the target currency.

  uv run python amazon_oa/amazon-currency-conversion-rate/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-currency-conversion-rate/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findConversionRate(self, rates, query):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findConversionRate above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findConversionRate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
