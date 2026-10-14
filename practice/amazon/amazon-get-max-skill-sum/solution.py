"""Get Max Skill Sum — https://www.fastprep.io/problems/amazon-get-max-skill-sum

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-skill-sum.md

A manager at Amazon is managing a team of n employees with IDs numbered from 0 to n - 1. Some employees are marketing experts and others are developers. The employee with id i has a skill level of ski

  uv run python amazon_oa/amazon-get-max-skill-sum/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-skill-sum/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxSkillSum(self, expertise, skill):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxSkillSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxSkillSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
