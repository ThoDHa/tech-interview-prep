"""Get Min Size — https://www.fastprep.io/problems/amazon-get-min-size

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-min-size.md

Within the Amazon Gaming Distribution System, a logistics coordinator is faced with the task of efficiently distributing n games among k different children. Each game is characterized by its size, den

  uv run python amazon_oa/amazon-get-min-size/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-min-size/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinSize(self, gameSize, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinSize above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinSize(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
