"""Sort Error Codes by Frequency — https://www.fastprep.io/problems/amazon-sort-error-codes-by-frequency

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-sort-error-codes-by-frequency.md

You are given an integer array codes representing error codes.

  uv run python amazon_oa/amazon-sort-error-codes-by-frequency/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-sort-error-codes-by-frequency/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def sortErrorCodesByFrequency(self, codes):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in sortErrorCodesByFrequency above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().sortErrorCodesByFrequency(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
