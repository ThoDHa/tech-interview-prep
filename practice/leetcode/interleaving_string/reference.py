"""Interleaving String — https://leetcode.com/problems/interleaving-string/

Write-up & approaches: ../../docs/problems/interleaving_string.md
Reference implementation of the write-up's Space-Optimized Two-Row DP solution.

You are given three strings `s1`, `s2`, and `s3`. Return `true` if `s3` is formed by interleaving `s1` and `s2` together or `false` otherwise: the characters of `s1` and `s2` are merged so that each keeps its own relative order.

  uv run python interleaving_string/reference.py   # debug one case (see CASE below)
  uv run pytest interleaving_string/              # run the test sets
"""

from harness import pick_case


class Solution:
    def isInterleave(self, s1, s2, s3):
        """Return whether `s3` is an interleaving of `s1` and `s2`.

        A length gate first: any interleaving consumes every character of
        all three strings, so `len(s3)` must equal `len(s1) + len(s2)`.
        Then a two-row prefix table decides reachability: `cur[j]` is true
        exactly when the first `i` characters of `s1` and the first `j` of
        `s2` can interleave into the first `i + j` of `s3`, reachable from
        the cell above by consuming an `s1` character or the cell to the
        left by consuming an `s2` character.

        Args:
            s1: First string, 0 <= len(s1) <= 100, lowercase letters.
            s2: Second string, 0 <= len(s2) <= 100, lowercase letters.
            s3: Candidate interleaving, 0 <= len(s3) <= 200, lowercase letters.

        Returns:
            True when `s3` interleaves `s1` and `s2`, False otherwise.

        Time:  O(m * n): one comparison per table cell (m = len(s1),
            n = len(s2)).
        Space: O(n): the two live rows.
        """
        m, n = len(s1), len(s2)
        if len(s3) != m + n:
            return False
        prev = [True] + [False] * n
        for j in range(1, n + 1):
            prev[j] = prev[j - 1] and s2[j - 1] == s3[j - 1]
        for i in range(1, m + 1):
            cur = [False] * (n + 1)
            cur[0] = prev[0] and s1[i - 1] == s3[i - 1]
            for j in range(1, n + 1):
                from_s1 = prev[j] and s1[i - 1] == s3[i + j - 1]
                from_s2 = cur[j - 1] and s2[j - 1] == s3[i + j - 1]
                cur[j] = from_s1 or from_s2
            prev = cur
        return prev[n]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isInterleave above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().isInterleave(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
