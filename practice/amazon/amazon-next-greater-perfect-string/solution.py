"""Next Perfect String — https://www.fastprep.io/problems/amazon-next-greater-perfect-string

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-next-greater-perfect-string.md

A perfect string is a string in which no two adjacent characters are the same.

  uv run python amazon_oa/amazon-next-greater-perfect-string/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-next-greater-perfect-string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def nextGreaterPerfectString(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in nextGreaterPerfectString above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().nextGreaterPerfectString(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
