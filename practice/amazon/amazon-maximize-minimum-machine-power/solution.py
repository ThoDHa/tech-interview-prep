"""Maximize Minimum Machine Power — https://www.fastprep.io/problems/amazon-maximize-minimum-machine-power

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximize-minimum-machine-power.md

You are given an integer array sources, where sources[i] is the amount of power available from the i-th power source, and an integer n representing the number of machines.

  uv run python amazon_oa/amazon-maximize-minimum-machine-power/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximize-minimum-machine-power/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximizeMinimumMachinePower(self, sources, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximizeMinimumMachinePower above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximizeMinimumMachinePower(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
