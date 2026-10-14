"""Sum of All Days Numbers on Which the Data of the Xth Will Be Dependent — https://www.fastprep.io/problems/amazon-sum-of-all-days-numbers-on-which-the-data-of-the-xth-will-be-dependent

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-sum-of-all-days-numbers-on-which-the-data-of-the-xth-will-be-dependent.md

Data analysts at Amazon are analyzing time series data. It was concluded that the data of the nth item was dependent on the data of the some xth day if there is a positive integer k such that the floo

  uv run python amazon_oa/amazon-sum-of-all-days-numbers-on-which-the-data-of-the-xth-will-be-dependent/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-sum-of-all-days-numbers-on-which-the-data-of-the-xth-will-be-dependent/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def sumOfAllDaysNumbers(self, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in sumOfAllDaysNumbers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().sumOfAllDaysNumbers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
