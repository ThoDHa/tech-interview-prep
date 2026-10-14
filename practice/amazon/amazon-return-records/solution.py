"""Return Records — https://www.fastprep.io/problems/amazon-return-records

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-return-records.md

Simulate a website authentication service. Initially, no users are registered and no user is logged in. Process each request in attempts from left to right.

  uv run python amazon_oa/amazon-return-records/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-return-records/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def returnRecords(self, attempts):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in returnRecords above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().returnRecords(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
