"""Longest Consecutive Sequence — https://leetcode.com/problems/longest-consecutive-sequence/

Write-up & approaches: ../../docs/problems/longest_consecutive_sequence.md

Canonical reference implementation: the write-up's optimal approach (set
membership with sequence-start detection), kept next to the harness so
authored cases stay falsifiable. Your own attempt lives in solution.py.

  uv run python longest_consecutive_sequence/reference.py   # debug one case (see CASE below)
  uv run pytest longest_consecutive_sequence/               # run the test sets
"""

from harness import pick_case


class Solution:
    def longestConsecutive(self, nums):
        """Walk each number's run forward, but only from run starts.

        A number is a run start exactly when num - 1 is absent from the set,
        so every run is walked once from its head and the total work stays
        linear despite the nested loop shape.

        Time:  O(n): each number enters and leaves the walk at most once.
        Space: O(n): the set holds every distinct value.
        """
        numbers = set(nums)
        longest = 0
        for num in numbers:
            if num - 1 in numbers:
                continue
            length = 1
            while num + length in numbers:
                length += 1
            longest = max(longest, length)
        return longest


if __name__ == "__main__":
    # Debug playground: set a breakpoint in longestConsecutive above, then run
    # this file. Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().longestConsecutive(*case["args"])
    print(f"case {case['id']}: expected = {case['expected']}")
    print(f"got:      {result}")
