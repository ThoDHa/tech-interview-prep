"""3Sum: https://leetcode.com/problems/3sum/

Write-up & approaches: ../../../docs/leetcode/3sum.md

Given an integer array `nums`, return all unique triplets
`[nums[i], nums[j], nums[k]]` with distinct indices such that they sum to zero.
The solution set must not contain duplicate triplets; order does not matter.

  uv run python 3sum/solution.py     # debug one case (see CASE below)
  uv run pytest 3sum/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        """
        n = len(nums)
        seen = set()
        result = []

        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        temp = [nums[i], nums[j], nums[k]]
                        temp.sort()
                        temp_set = (temp[0], temp[1], temp[2])
                        if temp_set not in seen:
                            seen.add(temp_set)
                            result.append(temp)

        return result
        """

        n = len(nums)
        nums.sort()
        result = []

        for i in range(n - 2):
            left = i + 1
            right = n - 1

            if i > 0 and nums[i] == nums[i-1]:
                continue

            while left < right:
                sum = nums[i] + nums[left] + nums[right]
                if sum == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif sum < 0:
                    left += 1
                else:
                    right -= 1
        return result


if __name__ == "__main__":
    # Debug playground: set a breakpoint in threeSum above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().threeSum(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
