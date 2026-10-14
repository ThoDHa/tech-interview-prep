"""Count Max Num Teams — https://www.fastprep.io/problems/count-max-num-teams

Write-up & approaches: ../../../docs/problems/amazon_oa/count-max-num-teams.md

Amazon OA problem.

  uv run python amazon_oa/count-max-num-teams/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/count-max-num-teams/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countMaxNumTeams(self, skill, teamSize, maxDiff):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countMaxNumTeams above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countMaxNumTeams(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
