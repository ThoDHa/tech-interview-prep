"""Count Distinct Passwords — https://www.fastprep.io/problems/amazon-count-distinct-passwords

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-distinct-passwords.md

Weak passwords are likely to be hacked and misused. Due to this, developers at Amazon regularly come up with new algorithms to check the health of user passwords. A new algorithm estimates the variabi

  uv run python amazon_oa/amazon-count-distinct-passwords/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-distinct-passwords/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countDistinctPasswords(self, password):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countDistinctPasswords above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countDistinctPasswords(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
