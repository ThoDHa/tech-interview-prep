"""Get Max Programs — https://www.fastprep.io/problems/amazon-get-max-programs

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-programs.md

Within an Amazon software management tool, there's a collection of software programs and time slots. Each time slot lasts k seconds, and within that time the slots do not overlap. The software program

  uv run python amazon_oa/amazon-get-max-programs/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-programs/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxPrograms(self, time, m, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxPrograms above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxPrograms(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
