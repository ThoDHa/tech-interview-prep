"""Get Average Standing — https://www.fastprep.io/problems/get-average-standing

Write-up & approaches: ../../../docs/problems/amazon_oa/get-average-standing.md

As an aspiring developer, you are required to develop a result analysis service for a car game on Amazon games.

  uv run python amazon_oa/get-average-standing/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/get-average-standing/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getAverageStanding(self, d, records):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getAverageStanding above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getAverageStanding(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
