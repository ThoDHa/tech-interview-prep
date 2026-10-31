"""Maximize Shipment Order by Sorting One Window — https://www.fastprep.io/problems/amazon-maximize-shipment-order-one-window

Write-up & approaches: ../../../docs/amazon/amazon-maximize-shipment-order-one-window.md

shipmentOrder is a permutation of 1..n. Choose exactly one contiguous window of length windowSize, sort that window in ascending order, and return the lexicographically largest complete array obtainab

  uv run python amazon/amazon-maximize-shipment-order-one-window/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-maximize-shipment-order-one-window/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, shipmentOrder, windowSize):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
