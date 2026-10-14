"""Gas Station — https://leetcode.com/problems/gas-station/

Write-up & approaches: ../../docs/problems/gas_station.md

There are `n` gas stations along a circular route. You are given two integer arrays `gas` and `cost` where: * `gas[i]` is the amount of gas at the `ith` station. * `cost[i]` is the amount of gas neede

  uv run python gas_station/solution.py   # debug one case (see CASE below)
  uv run pytest gas_station/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def canCompleteCircuit(self, gas, cost):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in canCompleteCircuit above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().canCompleteCircuit(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
