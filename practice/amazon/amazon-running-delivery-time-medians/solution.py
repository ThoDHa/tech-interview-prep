"""Running Delivery Time Medians — https://www.fastprep.io/problems/amazon-running-delivery-time-medians

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-running-delivery-time-medians.md

Given an array deliveryTimes, process the values from left to right. After each new delivery time arrives, output the median of all delivery times seen so far.

  uv run python amazon_oa/amazon-running-delivery-time-medians/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-running-delivery-time-medians/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def runningDeliveryMedians(self, deliveryTimes):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in runningDeliveryMedians above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().runningDeliveryMedians(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
