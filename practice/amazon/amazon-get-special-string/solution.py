"""Special String — https://www.fastprep.io/problems/amazon-get-special-string

Write-up & approaches: ../../../docs/amazon/amazon-get-special-string.md

Developers at Amazon are working on a text generation utility for one of their new products.

  uv run python amazon/amazon-get-special-string/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-get-special-string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getSpecialString(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getSpecialString above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getSpecialString(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
