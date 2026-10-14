"""Minimize Sum of Absolute Differences — https://www.fastprep.io/problems/amazon-minimize-sum-of-absolute-differences

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimize-sum-of-absolute-differences.md

Given two arrays a[] and b[] of equal length n. The task is to pair each element of array a to an element in array b, such that sum S of absolute differences of all the pairs is minimum.

  uv run python amazon_oa/amazon-minimize-sum-of-absolute-differences/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimize-sum-of-absolute-differences/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimizeSumOfAbsoluteDifferences(self, a, b):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimizeSumOfAbsoluteDifferences above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimizeSumOfAbsoluteDifferences(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
