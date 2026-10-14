"""Find Number — https://www.fastprep.io/problems/amazon-find-number

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-number.md

In order to ensure maximum security, the developers at Amazon employ multiple encryption methods to keep user data protected.

  uv run python amazon_oa/amazon-find-number/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-number/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findNumber(self, numbers):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findNumber above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findNumber(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
