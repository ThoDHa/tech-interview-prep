"""Lexicographically Maximum Final Sequence — https://www.fastprep.io/problems/amazon-lexicographically-maximum-final-sequence

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-lexicographically-maximum-final-sequence.md

You are given a binary string shipmentData consisting only of '0' and '1'.

  uv run python amazon_oa/amazon-lexicographically-maximum-final-sequence/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-lexicographically-maximum-final-sequence/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def rearrangeShipmentData(self, shipmentData):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in rearrangeShipmentData above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().rearrangeShipmentData(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
