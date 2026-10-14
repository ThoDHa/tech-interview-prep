"""Bit at an Index After Repeated Binary Expansion — https://www.fastprep.io/problems/amazon-indexed-bit-after-binary-expansion

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-indexed-bit-after-binary-expansion.md

Start with a binary string bits. In one expansion round, replace every character independently:

  uv run python amazon_oa/amazon-indexed-bit-after-binary-expansion/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-indexed-bit-after-binary-expansion/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def expandedBit(self, bits, rounds, index):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in expandedBit above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().expandedBit(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
