"""Employee Ratings Management System — https://www.fastprep.io/problems/amazon-employee-ratings-data-structure

Write-up & approaches: ../../../docs/amazon/amazon-employee-ratings-data-structure.md

Process a sequence of operations on an initially empty ordered list of employee ratings. Operation [1, rating] appends a rating. Operation [2, index] deletes the rating at the current zero-based index

  uv run python amazon/amazon-employee-ratings-data-structure/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-employee-ratings-data-structure/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case, run_operations


class EmployeeRatings:
    def __init__(self, operation_bound: int) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def append(self, rating: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def delete(self, index: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def query(self) -> List[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in an EmployeeRatings method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(EmployeeRatings, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement EmployeeRatings's methods first")
