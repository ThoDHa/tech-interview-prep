"""Calculate Max Salary — https://www.fastprep.io/problems/amazon-calculate-max-salary

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-calculate-max-salary.md

You work at a company that has 5 offices, each with a distinct salary level and a priority ranking from lowest to highest as follows: Office A ($1)<OfficeB($10)< Office C ($100)<OfficeD($1,000)< Offic

  uv run python amazon_oa/amazon-calculate-max-salary/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-calculate-max-salary/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def calculateMaxSalary(self, schedule):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in calculateMaxSalary above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calculateMaxSalary(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
