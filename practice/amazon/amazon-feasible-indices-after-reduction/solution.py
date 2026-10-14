"""Feasible Indices After Reduction — https://www.fastprep.io/problems/amazon-feasible-indices-after-reduction

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-feasible-indices-after-reduction.md

You are given an integer array arr of size n. All elements of arr are distinct.

  uv run python amazon_oa/amazon-feasible-indices-after-reduction/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-feasible-indices-after-reduction/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def feasibleIndicesAfterReduction(self, arr):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in feasibleIndicesAfterReduction above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().feasibleIndicesAfterReduction(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
