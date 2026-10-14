"""Find Capable Winners — https://www.fastprep.io/problems/amazon-find-capable-winners

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-capable-winners.md

Amazon games have recently launched a new multi-player tournament on the platform. Each game of the tournament has 3 rounds. The players are provided with exactly three power boosters at the start of 

  uv run python amazon_oa/amazon-find-capable-winners/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-capable-winners/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findCapableWinners(self, power_a, power_b, power_c):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findCapableWinners above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findCapableWinners(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
