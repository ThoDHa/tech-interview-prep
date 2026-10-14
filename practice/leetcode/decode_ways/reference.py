"""Decode Ways — https://leetcode.com/problems/decode-ways/

Write-up & approaches: ../../docs/problems/decode_ways.md
Reference implementation of the write-up's Space-Optimized DP solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python decode_ways/reference.py   # replay the example cases
  uv run pytest decode_ways/               # run the test sets
"""

from harness import pick_case


class Solution:
    def numDecodings(self, s: str) -> int:
        """Return the number of ways to decode the digit string.

        Time:  O(n): one pass over the string, constant work per digit.
        Space: O(1): the dp table collapses to two rolling totals.
        """
        one_back, two_back = 1, 0  # dp[i - 1], dp[i - 2]
        for i in range(1, len(s) + 1):
            current = 0
            if s[i - 1] != "0":
                current += one_back
            if i >= 2 and s[i - 2] != "0" and int(s[i - 2 : i]) <= 26:
                current += two_back
            two_back = one_back
            one_back = current
        return one_back


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().numDecodings(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
