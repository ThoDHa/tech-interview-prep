"""Maximize Center A Package Benefit — https://www.fastprep.io/problems/amazon-center-a-package-benefit

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-center-a-package-benefit.md

Two distribution centers, A and B, must allocate n packages. Package i is worth benefitA[i] to Center A and benefitB[i] to Center B.

  uv run python amazon_oa/amazon-center-a-package-benefit/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-center-a-package-benefit/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, benefitA, benefitB, linkedPairs):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
