"""Longest Common Subsequence — https://leetcode.com/problems/longest-common-subsequence/

Write-up & approaches: ../../docs/problems/longest_common_subsequence.md
Reference implementation of the write-up's Space-Optimized Two-Row DP solution.

Given two strings `text1` and `text2`, return the length of the longest common subsequence between the two strings if one exists, otherwise return `0`. A subsequence is a sequence derived by deleting some or no elements without changing the relative order of the remaining characters.

  uv run python longest_common_subsequence/reference.py   # debug one case (see CASE below)
  uv run pytest longest_common_subsequence/              # run the test sets
"""

from harness import pick_case


class Solution:
    def longestCommonSubsequence(self, text1, text2):
        """Return the length of the longest common subsequence of the inputs.

        Walks a prefix table one row at a time: `prev` holds the row for the
        first `i - 1` characters of `text1` and `cur` is built for the first
        `i`. Matching characters extend the diagonal; otherwise the row
        inherits the better of dropping one character from either string.
        Only two rows are alive at any time, so the full table never exists.

        Args:
            text1: First string, 1 <= len(text1) <= 1000, lowercase letters.
            text2: Second string, 1 <= len(text2) <= 1000, lowercase letters.

        Returns:
            The length of the longest common subsequence, 0 when none exists.

        Time:  O(m * n): one comparison per table cell.
        Space: O(n): the two live rows (n = len(text2)).
        """
        width = len(text2)
        prev = [0] * (width + 1)
        for i in range(1, len(text1) + 1):
            cur = [0] * (width + 1)
            for j in range(1, width + 1):
                if text1[i - 1] == text2[j - 1]:
                    cur[j] = prev[j - 1] + 1
                else:
                    cur[j] = max(prev[j], cur[j - 1])
            prev = cur
        return prev[width]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestCommonSubsequence above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestCommonSubsequence(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
