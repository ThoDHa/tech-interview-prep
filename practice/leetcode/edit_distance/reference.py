"""Edit Distance — https://leetcode.com/problems/edit-distance/

Write-up & approaches: ../../docs/problems/edit_distance.md
Reference implementation of the write-up's Space-Optimized Two-Row DP solution.

You are given two strings `word1` and `word2`, each consisting of lowercase English letters. You may insert, delete, or replace characters any number of times; return the minimum number of operations to make `word1` equal `word2`.

  uv run python edit_distance/reference.py   # debug one case (see CASE below)
  uv run pytest edit_distance/              # run the test sets
"""

from harness import pick_case


class Solution:
    def minDistance(self, word1, word2):
        """Return the minimum number of insert/delete/replace operations.

        Walks the classic prefix table: `prev[j]` is the edit distance
        between the first `i - 1` characters of `word1` and the first `j`
        of `word2`; `cur[j]` is built for the first `i`. Matching ends are
        free; otherwise the cell takes one plus the best of deleting,
        inserting, or replacing. Only two rows are alive at any time.

        Args:
            word1: Source string, 0 <= len(word1) <= 100, lowercase letters.
            word2: Target string, 0 <= len(word2) <= 100, lowercase letters.

        Returns:
            The fewest operations turning `word1` into `word2`.

        Time:  O(m * n): one comparison per table cell (m = len(word1),
            n = len(word2)).
        Space: O(n): the two live rows.
        """
        m, n = len(word1), len(word2)
        prev = list(range(n + 1))
        for i in range(1, m + 1):
            cur = [i] + [0] * n
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    cur[j] = prev[j - 1]
                else:
                    cur[j] = 1 + min(
                        prev[j],      # delete word1[i-1]
                        cur[j - 1],   # insert word2[j-1]
                        prev[j - 1],  # replace word1[i-1] with word2[j-1]
                    )
            prev = cur
        return prev[n]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minDistance above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minDistance(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
