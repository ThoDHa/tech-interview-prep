"""Daily Temperatures — https://leetcode.com/problems/daily-temperatures/

Write-up & approaches: ../../docs/problems/daily_temperatures.md

You are given an array of integers `temperatures` where `temperatures[i]` represents the daily temperatures on the `ith` day. Return an array `result` where `result[i]` is the number of days after the

  uv run python daily_temperatures/solution.py   # debug one case (see CASE below)
  uv run pytest daily_temperatures/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def dailyTemperatures(self, temperatures):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in dailyTemperatures above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().dailyTemperatures(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
