"""Number of 1 Bits — https://leetcode.com/problems/number-of-1-bits/

Write-up & approaches: ../../docs/problems/number_of_1_bits.md

You are given an unsigned integer `n`. Return the number of `1` bits in its binary representation. You may assume `n` is a non-negative integer which fits within 32-bits.

  uv run python number_of_1_bits/solution.py   # debug one case (see CASE below)
  uv run pytest number_of_1_bits/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def hammingWeight(self, n):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in hammingWeight above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().hammingWeight(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
