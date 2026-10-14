"""Employee Ratings Management System — https://www.fastprep.io/problems/amazon-employee-ratings-data-structure

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-employee-ratings-data-structure.md

Process a sequence of operations on an initially empty ordered list of employee ratings. Operation [1, rating] appends a rating. Operation [2, index] deletes the rating at the current zero-based index

  uv run python amazon_oa/amazon-employee-ratings-data-structure/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-employee-ratings-data-structure/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def employeeRatings(self, operations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in employeeRatings above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().employeeRatings(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
