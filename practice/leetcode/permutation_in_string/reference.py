"""Permutation In String — https://leetcode.com/problems/permutation-in-string/

Write-up & approaches: ../../docs/problems/permutation-in-string/

Canonical reference implementation: the write-up's optimal approach
(sliding window with a fixed 26-letter deficit count), kept next to the
harness so authored cases stay falsifiable. Your own attempt lives in
solution.py.

  uv run python permutation_in_string/reference.py   # debug one case (see CASE below)
  uv run pytest permutation_in_string/               # run the test sets
"""

from harness import pick_case


class Solution:
    def checkInclusion(self, s1, s2):
        """Slide a fixed-width window over s2, tracking the letter deficit.

        need holds how many of each letter the window still owes to match
        s1's multiset; matches tracks letters fully settled. A window of
        len(s1) whose matches reach 26 is exactly a permutation of s1.

        Time:  O(n1 + n2): seeding is linear, then the window sweeps once.
        Space: O(1): two 26-slot count arrays.
        """
        n1, n2 = len(s1), len(s2)
        if n1 > n2:
            return False
        need = [0] * 26
        window = [0] * 26
        base = ord("a")
        for i in range(n1):
            need[ord(s1[i]) - base] += 1
            window[ord(s2[i]) - base] += 1
        matches = sum(1 for i in range(26) if need[i] == window[i])
        if matches == 26:
            return True
        for right in range(n1, n2):
            index = ord(s2[right]) - base
            window[index] += 1
            if window[index] == need[index]:
                matches += 1
            elif window[index] == need[index] + 1:
                matches -= 1
            left_index = ord(s2[right - n1]) - base
            window[left_index] -= 1
            if window[left_index] == need[left_index]:
                matches += 1
            elif window[left_index] == need[left_index] - 1:
                matches -= 1
            if matches == 26:
                return True
        return False


if __name__ == "__main__":
    # Debug playground: set a breakpoint in checkInclusion above, then run
    # this file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().checkInclusion(*case["args"])
    print(f"case {case['id']}: expected = {case['expected']}")
    print(f"got:      {result}")
