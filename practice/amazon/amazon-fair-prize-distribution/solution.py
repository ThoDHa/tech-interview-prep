"""Fair Prize Distribution — https://www.fastprep.io/problems/amazon-fair-prize-distribution

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-fair-prize-distribution.md

A coding challenge has n participants. Participant i earned score points[i]. There are m available prizes, and values[j] is the value of the j-th prize.

  uv run python amazon_oa/amazon-fair-prize-distribution/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-fair-prize-distribution/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findFairDistribution(self, points, values):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findFairDistribution above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findFairDistribution(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
