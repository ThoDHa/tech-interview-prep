"""Two Sum II Input Array Is Sorted — https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Write-up & approaches: ../../docs/problems/two_sum_ii_input_array_is_sorted.md

Given an array of integers `numbers` that is sorted in **non-decreasing order**. Return the indices (**1-indexed**) of two numbers, `[index1, index2]`, such that they add up to a given target number `

  uv run python two_sum_ii_input_array_is_sorted/solution.py   # debug one case (see CASE below)
  uv run pytest two_sum_ii_input_array_is_sorted/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def twoSum(self, numbers, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in twoSum above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().twoSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
