"""Group Anagrams — https://leetcode.com/problems/group-anagrams/

Write-up & approaches: ../../docs/problems/group_anagrams.md

Canonical reference implementation: the write-up's optimal approach (the
26-slot character-count key), kept next to the harness so authored cases stay
falsifiable. Your own attempt lives in solution.py.

  uv run python group_anagrams/reference.py   # debug one case (see below)
  uv run pytest group_anagrams/               # run the test sets
"""


class Solution:
    def solve(self, *args):
        """Group anagrams by their 26-slot character-count signature.

        Two strings are anagrams exactly when every letter occurs the same
        number of times in both, so the count tuple is a canonical key: equal
        keys land in the same group and no other pair collides.

        Time:  O(n * k): n strings, each scanned for its k characters.
        Space: O(n * k): the key map holds one 26-slot tuple per group.
        """
        (strs,) = args
        groups = {}
        for s in strs:
            counts = [0] * 26
            for c in s:
                counts[ord(c) - ord("a")] += 1
            groups.setdefault(tuple(counts), []).append(s)
        return list(groups.values())


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # cases.json is empty (any-order output), so a literal example stands in.
    strs = ["act", "pots", "tops", "cat", "stop", "hat"]
    result = Solution().solve(strs)
    print(f"args = {strs}")
    print(f"got: {sorted(sorted(group) for group in result)}")
