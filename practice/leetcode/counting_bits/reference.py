"""Counting Bits — https://leetcode.com/problems/counting-bits/

Write-up & approaches: ../../docs/problems/counting_bits.md
Reference implementation of the write-up's Bottom-Up DP with Lowest Set Bit
solution, kept next to the harness so authored cases stay falsifiable. Your
own attempt lives in solution.py.

  uv run python counting_bits/reference.py   # replay the example cases
  uv run pytest counting_bits/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def countBits(self, n: int) -> List[int]:
        """Return the popcount of every value in `0..n`.

        Fills `dp` bottom-up with the lowest-set-bit recurrence: clearing
        bit `i`'s lowest set bit (`i & (i - 1)`) yields a smaller value
        already counted, so `dp[i]` is that entry plus the one set bit
        just erased. Every entry is written once, in constant work.

        Args:
            n: Upper end of the inclusive range, `0 <= n <= 1000`.

        Returns:
            A list `dp` of length `n + 1` with `dp[i] = popcount(i)`.

        Time:  O(n): one constant-work transition per index.
        Space: O(1) beyond the output list the problem requires.
        """
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i & (i - 1)] + 1
        return dp


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    case = pick_case(__file__, "example_1")
    result = Solution().countBits(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
