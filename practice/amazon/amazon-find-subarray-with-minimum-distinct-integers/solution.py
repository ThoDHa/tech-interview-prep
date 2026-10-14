"""Find Subarray with Minimum Distinct Integers — https://www.fastprep.io/problems/amazon-find-subarray-with-minimum-distinct-integers

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-subarray-with-minimum-distinct-integers.md

Given an array of integers and two specified numbers, find a subarray from the original array that contains both of these specified numbers, with the requirement that the subarray contains the minimum

  uv run python amazon_oa/amazon-find-subarray-with-minimum-distinct-integers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-subarray-with-minimum-distinct-integers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findSubarrayWithMinimumDistinctIntegers(self, array, series1, series2):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findSubarrayWithMinimumDistinctIntegers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findSubarrayWithMinimumDistinctIntegers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
