"""Sum Max Plus Min After Decrement Operations — https://www.fastprep.io/problems/amazon-sum-max-plus-min-after-decrement-operations

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-sum-max-plus-min-after-decrement-operations.md

You are given an integer array arr and an integer requests.

  uv run python amazon_oa/amazon-sum-max-plus-min-after-decrement-operations/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-sum-max-plus-min-after-decrement-operations/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def sumMaxPlusMinAfterOperations(self, arr, requests):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in sumMaxPlusMinAfterOperations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().sumMaxPlusMinAfterOperations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
