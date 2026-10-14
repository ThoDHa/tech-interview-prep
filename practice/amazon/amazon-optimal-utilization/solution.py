"""Optimal Utilization — https://www.fastprep.io/problems/amazon-optimal-utilization

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-optimal-utilization.md

You are given a device with a limited amount of memory. Each device must run two applications at the same time: one foreground application and one background application. Each application is identifie

  uv run python amazon_oa/amazon-optimal-utilization/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-optimal-utilization/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def optimalUtilization(self, deviceCapacity, foregroundAppList, backgroundAppList):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in optimalUtilization above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().optimalUtilization(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
