"""Find Security Level — https://www.fastprep.io/problems/amazon-find-security-level

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-security-level.md

Source said that the other problem 👇 in the same batch was for Newe Grad, so I assume this problem is for New Grad as well.  

  uv run python amazon_oa/amazon-find-security-level/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-security-level/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findSecurityLevel(self, pid, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findSecurityLevel above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findSecurityLevel(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
