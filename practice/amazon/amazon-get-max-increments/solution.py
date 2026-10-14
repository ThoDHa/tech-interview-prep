"""Get Max Increments — https://www.fastprep.io/problems/amazon-get-max-increments

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-increments.md

IMDB, an Amazon-owned company, is a widely used platform for discovering scores of films and television series.

  uv run python amazon_oa/amazon-get-max-increments/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-increments/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxIncrements(self, scores):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxIncrements above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxIncrements(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
