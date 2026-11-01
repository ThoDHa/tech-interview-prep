"""Climbing Stairs — https://www.fastprep.io/problems/amazon-climbing-stairs

Write-up & approaches: ../../../docs/amazon/amazon-climbing-stairs.md

Reference implementation of the write-up's recommended Space-Optimized
Bottom-Up DP solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-climbing-stairs/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-climbing-stairs/              # run the test sets
"""

from harness import pick_case


class Solution:
    def climbStairs(self, n: int) -> int:
        """Count the distinct move sequences that reach exactly step `n`.

        The last move of any climb is a 1-step from step `n - 1` or a
        2-step from step `n - 2`, so the counts follow the recurrence
        `dp[i] = dp[i - 1] + dp[i - 2]` with `dp[0] = dp[1] = 1`. The
        loop keeps only the last two counts in rolling variables.

        Args:
            n: The top step; the page constraints give 1 <= n <= 45.

        Returns:
            The number of distinct sequences of 1-step and 2-step moves
            that reach exactly step `n`.

        Time:  O(n): one addition per step from 2 through n.
        Space: O(1): two rolling counters regardless of n.
        """
        if n <= 1:
            return 1

        previous, current = 1, 1

        for _ in range(2, n + 1):
            saved_current = current
            current = previous + current
            previous = saved_current

        return current


if __name__ == "__main__":
    # Debug playground: set a breakpoint in climbStairs above, then run this file.
    case = pick_case(__file__, "example_2")
    result = Solution().climbStairs(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
