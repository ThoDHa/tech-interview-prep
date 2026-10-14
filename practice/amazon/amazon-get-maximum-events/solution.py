"""Get Max Events — https://www.fastprep.io/problems/amazon-get-maximum-events

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-maximum-events.md

You are given an array payload of size n, where payload[i] represents the size of the (i)-th event payload. The task is to select a subset of events and rearrange them into a new array optimizedPayloa

  uv run python amazon_oa/amazon-get-maximum-events/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-maximum-events/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaximumEvents(self, payload):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaximumEvents above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaximumEvents(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
