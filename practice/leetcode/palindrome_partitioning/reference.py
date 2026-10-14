"""Palindrome Partitioning — https://leetcode.com/problems/palindrome-partitioning/

Write-up & approaches: ../../docs/problems/palindrome_partitioning.md
Reference implementation of the write-up's Backtracking solution, kept next
to the harness so authored cases stay falsifiable. Your own attempt lives in
solution.py.

  uv run python palindrome_partitioning/reference.py   # debug one case (see below)
  uv run pytest palindrome_partitioning/               # run the test sets
"""

from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        """Return every split of `s` into palindromic pieces, in any order.

        Backtracks over cut positions from the left: `backtrack(start)`
        proposes every prefix `s[start:end]`, pushes it onto `path` only
        when `prefix == prefix[::-1]`, recurses on the remainder, and pops
        on the way out. A prefix that is not a palindrome can never be
        repaired by what follows, so every explored branch ends in a
        recorded partition and none is walked in vain.

        Args:
            s: Lowercase English letters; 1 <= len(s) <= 20.

        Returns:
            All palindromic partitions of `s`. The order of the partitions,
            and of equal-length alternatives within the list, is arbitrary;
            each partition appears exactly once because each cut set is
            generated exactly once.

        Time:  O(n x 2^n): up to 2^(n-1) partitions are copied at the
            leaves in O(n) each, and the slice tests across the whole
            tree cost O(n x 2^n) character comparisons in total.
        Space: O(n) excluding the output: the shared `path` plus the
            recursion stack, both at most n pieces deep.
        """
        result: List[List[str]] = []
        path: List[str] = []

        def backtrack(start: int) -> None:
            if start == len(s):
                result.append(path[:])
                return
            for end in range(start + 1, len(s) + 1):
                prefix = s[start:end]
                if prefix == prefix[::-1]:
                    path.append(prefix)
                    backtrack(end)
                    path.pop()

        backtrack(0)
        return result


if __name__ == "__main__":
    # Debug playground: set a breakpoint in partition above, then run this
    # file. cases.json is empty (any-order output), so a literal example
    # stands in.
    s = "aab"
    result = Solution().partition(s)
    print(f"args = s {s!r}")
    print(f"got: {sorted(map(sorted, result))}")
