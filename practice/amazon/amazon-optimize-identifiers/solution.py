"""Optimize Identifiers — https://www.fastprep.io/problems/amazon-optimize-identifiers

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-optimize-identifiers.md

Special thanks: 𓇼 ⋆.˚Manyy Manyyy thanks to Nachos and spike!𓆝 𓆡⋆.˚ 𓇼

  uv run python amazon_oa/amazon-optimize-identifiers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-optimize-identifiers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def optimizeIdentifiers(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in optimizeIdentifiers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().optimizeIdentifiers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
