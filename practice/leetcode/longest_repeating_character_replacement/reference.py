"""Longest Repeating Character Replacement — https://leetcode.com/problems/longest-repeating-character-replacement/

Write-up & approaches: ../../docs/problems/longest-repeating-character-replacement/

Canonical reference implementation: the write-up's optimal approach
(sliding window with a max-frequency counter), kept next to the harness so
authored cases stay falsifiable. Your own attempt lives in solution.py.

  uv run python longest_repeating_character_replacement/reference.py   # debug one case (see below)
  uv run pytest longest_repeating_character_replacement/               # run the test sets
"""

from harness import pick_case


class Solution:
    def characterReplacement(self, s, k):
        """Grow a window whose non-dominant letters fit within k replacements.

        The window is valid while window length minus the most frequent
        letter's count stays at most k; when a shift breaks that budget the
        left edge advances once, so both edges sweep forward monotonically.

        Time:  O(n): each character enters and leaves the window at most once.
        Space: O(1): counts for at most 26 uppercase letters.
        """
        counts = {}
        left = 0
        max_frequency = 0
        longest = 0
        for right, char in enumerate(s):
            counts[char] = counts.get(char, 0) + 1
            max_frequency = max(max_frequency, counts[char])
            while (right - left + 1) - max_frequency > k:
                counts[s[left]] -= 1
                left += 1
            longest = max(longest, right - left + 1)
        return longest


if __name__ == "__main__":
    # Debug playground: set a breakpoint in characterReplacement above, then
    # run this file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().characterReplacement(*case["args"])
    print(f"case {case['id']}: expected = {case['expected']}")
    print(f"got:      {result}")
