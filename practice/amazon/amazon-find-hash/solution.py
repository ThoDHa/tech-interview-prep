"""Find Hash — https://www.fastprep.io/problems/amazon-find-hash

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-hash.md

The developers at AWS IAM are designing a new checksum logic for an authentication module. The checksum is calculated as an array hash where hash[i] = secretKey[i] % param[i]. There are n parameters f

  uv run python amazon_oa/amazon-find-hash/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-hash/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findHash(self, param):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findHash above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findHash(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
