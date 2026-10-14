"""Daily Temperatures — https://leetcode.com/problems/daily-temperatures/

Write-up & approaches: ../../docs/problems/daily_temperatures.md
Reference implementation of the write-up's Monotonic Stack solution.

You are given an array of integers `temperatures` where `temperatures[i]` represents the daily temperatures on the `ith` day. Return an array `result` where `result[i]` is the number of days after the `ith` day before a warmer temperature appears on a future day. If there is no day in the future where a warmer temperature will appear for the `ith` day, set `result[i]` to `0` instead.

  uv run python daily_temperatures/reference.py   # debug one case (see CASE below)
  uv run pytest daily_temperatures/              # run the test sets
"""

from harness import pick_case


class Solution:
    def dailyTemperatures(self, temperatures):
        """Return days-until-warmer for every day, 0 when no warmer day exists.

        Walks the days left to right holding unresolved indices on a stack
        whose temperatures are strictly decreasing. A warmer current day
        resolves every colder day it tops.

        Args:
            temperatures: Daily values, 1 <= len(temperatures).

        Returns:
            List `result` of the same length where result[i] counts the days
            from day i to its first warmer day, or 0 when none exists.

        Time:  O(n): each index is pushed once and popped at most once.
        Space: O(n): the stack in the worst case of a strictly decreasing run.
        """
        stack = []
        result = [0] * len(temperatures)
        for day, temperature in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temperature:
                colder_day = stack.pop()
                result[colder_day] = day - colder_day
            stack.append(day)
        return result


if __name__ == "__main__":
    # Debug playground: set a breakpoint in dailyTemperatures above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().dailyTemperatures(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
