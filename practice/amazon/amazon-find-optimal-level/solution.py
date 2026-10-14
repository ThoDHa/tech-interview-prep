"""Optimal Level — https://www.fastprep.io/problems/amazon-find-optimal-level

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-optimal-level.md

Amazon is dedicated to leveraging advanced methods to streamline stock movement across its distribution centers. In this scenario, you are assigned a challenge involving a specific process with a sequ

  uv run python amazon_oa/amazon-find-optimal-level/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-optimal-level/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findOptimalLevel(self, stockArr, incVal, decVal):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findOptimalLevel above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findOptimalLevel(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
