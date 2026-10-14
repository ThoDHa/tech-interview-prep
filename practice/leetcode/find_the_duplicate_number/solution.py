"""Find The Duplicate Number — https://leetcode.com/problems/find-the-duplicate-number/

Write-up & approaches: ../../docs/problems/find_the_duplicate_number.md

You are given an array of integers `nums` containing `n + 1` integers. Each integer in `nums` is in the range `[1, n]` inclusive. There is exactly **one repeated integer** in `nums`, and every other i

  uv run python find_the_duplicate_number/solution.py   # debug one case (see CASE below)
  uv run pytest find_the_duplicate_number/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findDuplicate(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findDuplicate above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findDuplicate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
