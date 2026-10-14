"""Distributed Packages — https://www.fastprep.io/problems/amazon-distribute-packages

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-distribute-packages.md

Amazon has to distribute multiple packages across all of their delivery trucks. Given an array of trucks where trucks[i] represents the ith truck quantity. We also have another input to_distribute whi

  uv run python amazon_oa/amazon-distribute-packages/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-distribute-packages/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def distributePackages(self, trucks, to_distribute):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in distributePackages above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().distributePackages(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
