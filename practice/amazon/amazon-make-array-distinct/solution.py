"""Make Array Distinct — https://www.fastprep.io/problems/amazon-make-array-distinct

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-make-array-distinct.md

Amazon OA problem.

  uv run python amazon_oa/amazon-make-array-distinct/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-make-array-distinct/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def makeArrayDistinct(self, size, cost):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in makeArrayDistinct above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().makeArrayDistinct(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
