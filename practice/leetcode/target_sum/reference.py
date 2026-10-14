"""Target Sum — https://leetcode.com/problems/target-sum/

Write-up & approaches: ../../docs/problems/target_sum.md
Reference implementation of the write-up's Space-Optimized 1-D DP solution.

You are given an array of integers `nums` and an integer `target`. For each number you choose to either add or subtract it, building an expression; return the number of different expressions whose total equals `target`.

  uv run python target_sum/reference.py   # debug one case (see CASE below)
  uv run pytest target_sum/              # run the test sets
"""

from harness import pick_case


class Solution:
    def findTargetSumWays(self, nums, target):
        """Count sign assignments reaching `target` via a subset-sum count.

        Splits the numbers into positives `P` and negatives `N`; every
        expression satisfies `P - N = target` with `P + N = sum(nums)`, so
        the positives must be a subset summing to `(sum(nums) + target) / 2`.
        Counting those subsets is a 0/1 knapsack over one row `dp`, swept
        right to left so each number is used at most once. Numbers equal to
        zero double the ways, which the count handles naturally.

        Args:
            nums: Non-negative numbers, 1 <= len(nums) <= 20,
                0 <= nums[i] <= 1000.
            target: Desired expression total, -1000 <= target <= 1000.

        Returns:
            The number of sign assignments whose total equals `target`,
            0 when the subset sum has no integral solution.

        Time:  O(len(nums) * sum(nums)): one row sweep per number.
        Space: O(sum(nums)): the single row of subset-sum counts.
        """
        total = sum(nums)
        if abs(target) > total or (total + target) % 2 != 0:
            return 0
        positive_sum = (total + target) // 2
        dp = [0] * (positive_sum + 1)
        dp[0] = 1
        for num in nums:
            for a in range(positive_sum, num - 1, -1):
                dp[a] += dp[a - num]
        return dp[positive_sum]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findTargetSumWays above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findTargetSumWays(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
