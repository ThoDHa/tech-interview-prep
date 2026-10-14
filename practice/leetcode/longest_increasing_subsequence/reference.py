"""Longest Increasing Subsequence — https://leetcode.com/problems/longest-increasing-subsequence/

Write-up & approaches: ../../docs/problems/longest_increasing_subsequence.md
Reference implementation of the write-up's Patience Sorting with Binary Search
solution, kept next to the harness so authored cases stay falsifiable. Your own
attempt lives in solution.py.

  uv run python longest_increasing_subsequence/reference.py   # replay the example cases
  uv run pytest longest_increasing_subsequence/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """Return the length of the longest strictly increasing subsequence.

        Time:  O(n log n): each of the n elements runs one binary search over
            `tails`, which never exceeds n entries.
        Space: O(n): `tails` holds at most one entry per chain length.
        """
        tails: List[int] = []
        for num in nums:
            lo, hi = 0, len(tails)
            while lo < hi:
                mid = (lo + hi) // 2
                if tails[mid] < num:
                    lo = mid + 1
                else:
                    hi = mid
            if lo == len(tails):
                tails.append(num)
            else:
                tails[lo] = num
        return len(tails)


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().lengthOfLIS(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
