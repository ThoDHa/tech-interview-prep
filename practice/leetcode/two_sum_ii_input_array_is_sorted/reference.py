"""Two Sum II Input Array Is Sorted — https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Write-up & approaches: ../../docs/problems/two_sum_ii_input_array_is_sorted.md

Canonical reference implementation: the write-up's optimal approach (two
pointers converging on the sorted array), kept next to the harness so
authored cases stay falsifiable. Your own attempt lives in solution.py.

  uv run python two_sum_ii_input_array_is_sorted/reference.py   # debug one case (see CASE below)
  uv run pytest two_sum_ii_input_array_is_sorted/               # run the test sets
"""

from harness import pick_case


class Solution:
    def twoSum(self, numbers, target):
        """Converge two pointers on the sorted array until the pair matches.

        The array's order lets each sum comparison retire one candidate for
        good: too small advances the left end, too large retreats the right
        end, so the pointers meet on the unique answer without extra space.

        Time:  O(n): each step retires one element, so at most n - 1 steps.
        Space: O(1): two indices and one running sum.
        """
        left, right = 0, len(numbers) - 1
        while left < right:
            current_sum = numbers[left] + numbers[right]
            if current_sum == target:
                return [left + 1, right + 1]
            if current_sum < target:
                left += 1
            else:
                right -= 1
        return []


if __name__ == "__main__":
    # Debug playground: set a breakpoint in twoSum above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().twoSum(*case["args"])
    print(f"case {case['id']}: expected = {case['expected']}")
    print(f"got:      {result}")
