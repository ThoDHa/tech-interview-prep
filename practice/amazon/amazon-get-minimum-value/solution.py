"""Get Min Value — https://www.fastprep.io/problems/amazon-get-minimum-value

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-minimum-value.md

Amazon Prime Games is designing a game. The player needs to pass n rounds sequentially in this game. Rules of play are as follows:

  uv run python amazon_oa/amazon-get-minimum-value/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-minimum-value/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMinimumValue(self, power, armor):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMinimumValue above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMinimumValue(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
