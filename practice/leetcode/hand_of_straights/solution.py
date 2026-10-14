"""Hand of Straights — https://leetcode.com/problems/hand-of-straights/

Write-up & approaches: ../../docs/problems/hand_of_straights.md

You are given an integer array `hand` where `hand[i]` is the value written on the `ith` card and an integer `groupSize`. You want to rearrange the cards into groups so that each group is of size `grou

  uv run python hand_of_straights/solution.py   # debug one case (see CASE below)
  uv run pytest hand_of_straights/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def isNStraightHand(self, hand, groupSize):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isNStraightHand above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isNStraightHand(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
