"""Non Overlapping Intervals — https://leetcode.com/problems/non-overlapping-intervals/

Write-up & approaches: ../../docs/problems/non_overlapping_intervals.md
Reference implementation of the write-up's Greedy Earliest End solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python non_overlapping_intervals/reference.py   # replay the example cases
  uv run pytest non_overlapping_intervals/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        """Return the minimum removals leaving no overlapping intervals.

        Time:  O(n log n): the end-sort dominates; the keep sweep is linear.
        Space: O(1): a counter and the running end.
        """
        intervals.sort(key=lambda interval: interval[1])

        kept = 0
        prev_end = float("-inf")
        for start, end in intervals:
            if start >= prev_end:
                kept += 1
                prev_end = end

        return len(intervals) - kept


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().eraseOverlapIntervals(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
