"""Single Number — https://leetcode.com/problems/single-number/

Write-up & approaches: ../../docs/problems/single_number.md

You are given a **non-empty** array of integers `nums`. Every integer appears twice except for one. Return the integer that appears only once. You must implement a solution with $O(n)$ runtime complex

  uv run python single_number/solution.py   # debug one case (see CASE below)
  uv run pytest single_number/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def singleNumber(self, nums):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in singleNumber above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().singleNumber(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
