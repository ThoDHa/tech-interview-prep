"""Count Games Won By Group1 (AMZ CN) — https://www.fastprep.io/problems/amazon-how-many-games-did-the-team-win

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-how-many-games-did-the-team-win.md

Amazon Games is organizing a tournament of pair games. There are two groups, firstTeam and secondTeam, each containing n players. The skill level of the i-th player in each group is firstTeam[i] and s

  uv run python amazon_oa/amazon-how-many-games-did-the-team-win/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-how-many-games-did-the-team-win/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def howManyGamesDidTheyWin(self, n, firstTeam, secondTeam):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in howManyGamesDidTheyWin above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().howManyGamesDidTheyWin(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
