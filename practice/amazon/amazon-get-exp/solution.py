"""Get Experience — https://www.fastprep.io/problems/amazon-get-exp

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-exp.md

Note --> Feel free to check the source image below for the original problem statement :)

  uv run python amazon_oa/amazon-get-exp/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-exp/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getExp(self, exp):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getExp above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getExp(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
