"""Match Strings — https://www.fastprep.io/problems/amazon-match-strings

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-match-strings.md

Special thanks: MasterKhan contributed this problem.

  uv run python amazon_oa/amazon-match-strings/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-match-strings/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def matchStrings(self, text, pat):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in matchStrings above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().matchStrings(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
