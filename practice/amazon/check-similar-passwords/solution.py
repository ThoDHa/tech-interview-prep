"""Check Similar Passwords — https://www.fastprep.io/problems/check-similar-passwords

Write-up & approaches: ../../../docs/problems/amazon_oa/check-similar-passwords.md

Amazon would like to enforce a password policy for password changes. For each pair of strings newPasswords[i] and oldPasswords[i], determine whether the two passwords are similar.

  uv run python amazon_oa/check-similar-passwords/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/check-similar-passwords/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def checkSimilarPasswords(self, newPasswords, oldPasswords):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in checkSimilarPasswords above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().checkSimilarPasswords(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
