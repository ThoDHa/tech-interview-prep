"""Ensure Non Zero Load Sum — https://www.fastprep.io/problems/amazon-ensure-non-zero-load-sum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-ensure-non-zero-load-sum.md

You are given an integer array queueMessages. Positive values represent messages sent by producers, and negative values represent messages retrieved by consumers. The processing load of a contiguous s

  uv run python amazon_oa/amazon-ensure-non-zero-load-sum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-ensure-non-zero-load-sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minInsertionsToEnsureNonZeroLoadSum(self, queueMessages):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minInsertionsToEnsureNonZeroLoadSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minInsertionsToEnsureNonZeroLoadSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
