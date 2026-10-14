"""Domain Weight Calculation — https://www.fastprep.io/problems/amazon-domain-weight-calculation

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-domain-weight-calculation.md

Source note: This came from a real onsite interview report. The original report shared the core domain-score task and a concrete example, and FastPrep filled in the runnable function format, ordering 

  uv run python amazon_oa/amazon-domain-weight-calculation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-domain-weight-calculation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def calculateDomainScores(self, domainScores):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in calculateDomainScores above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().calculateDomainScores(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
