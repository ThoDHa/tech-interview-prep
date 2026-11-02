"""Longest Equal-Value Run — https://www.fastprep.io/problems/amazon-longest-equal-value-run

Write-up & approaches: ../../../docs/amazon/amazon-longest-equal-value-run.md

Reference implementation of the write-up's recommended Single-Pass Run
Counter solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-longest-equal-value-run/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-longest-equal-value-run/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def solve(self, nums: List[int]) -> int:
        """Return the length of the longest contiguous run of equal values.

        Walks the array once, carrying `current_run`, the length of the
        run ending at the previous element. An element equal to its
        predecessor extends that run and raises `longest_run` when the
        run becomes the longest seen; any different value restarts the
        run at length 1.

        Args:
            nums: Integer array; the statement grants the empty array
                with an expected result of 0.

        Returns:
            The length of the longest contiguous stretch of equal values.

        Time:  O(n): one predecessor comparison per element.
        Space: O(1): two counters regardless of input size.
        """
        if not nums:
            return 0
        longest_run = 1
        current_run = 1
        for index in range(1, len(nums)):
            if nums[index] == nums[index - 1]:
                current_run += 1
                longest_run = max(longest_run, current_run)
            else:
                current_run = 1
        return longest_run


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
