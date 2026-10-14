"""Planning the Campaign — https://www.fastprep.io/problems/amazon-minimum-weekly-input

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-weekly-input.md

A company will launch a series of marketing campaigns over several weeks. Each campaign has a certain cost. They want to launch at least one campaign every week, and to plan the campaigns in a way tha

  uv run python amazon_oa/amazon-minimum-weekly-input/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-weekly-input/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumWeeklyInput(self, costs, weeks):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumWeeklyInput above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumWeeklyInput(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
