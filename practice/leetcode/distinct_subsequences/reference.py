"""Distinct Subsequences — https://leetcode.com/problems/distinct-subsequences/

Write-up & approaches: ../../docs/problems/distinct_subsequences.md
Reference implementation of the write-up's Space-Optimized One-Row DP solution.

You are given two strings `s` and `t`, both consisting of english letters. Return the number of distinct subsequences of `s` which are equal to `t`.

  uv run python distinct_subsequences/reference.py   # debug one case (see CASE below)
  uv run pytest distinct_subsequences/              # run the test sets
"""

from harness import pick_case


class Solution:
    def numDistinct(self, s, t):
        """Count the subsequences of `s` equal to `t`.

        Sweeps one occurrence-count row in place: `dp[j]` counts how often
        the first `j` characters of `t` appear as a subsequence of the `s`
        prefix processed so far. A matching character may either pair up
        (adding the diagonal count) or sit unused (keeping the count it
        already holds). Iterating `t` from the right lets the single row do
        the work of two: positions right of `j` still hold the previous
        row's values, which is exactly what the diagonal update needs.

        Args:
            s: The source string, 1 <= len(s) <= 1000, English letters.
            t: The target subsequence, 1 <= len(t) <= 1000, English letters.

        Returns:
            The number of distinct subsequences of `s` equal to `t`.

        Time:  O(m * n): one comparison per (s prefix, t prefix) pair
            (m = len(s), n = len(t)).
        Space: O(n): the single row.
        """
        n = len(t)
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(1, len(s) + 1):
            for j in range(min(i, n), 0, -1):
                if s[i - 1] == t[j - 1]:
                    dp[j] += dp[j - 1]
        return dp[n]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in numDistinct above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().numDistinct(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
