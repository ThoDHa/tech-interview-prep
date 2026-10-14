"""Find Password Strength — https://www.fastprep.io/problems/amazon-find-password-strength

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-password-strength.md

Hello! Did you navigate here from my sister question Password Strength 🐣?

  uv run python amazon_oa/amazon-find-password-strength/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-password-strength/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findPasswordStrength(self, password):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findPasswordStrength above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findPasswordStrength(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
