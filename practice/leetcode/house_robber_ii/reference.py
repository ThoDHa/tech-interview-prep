"""House Robber II — https://leetcode.com/problems/house-robber-ii/

Write-up & approaches: ../../docs/problems/house_robber_ii.md
Reference implementation of the write-up's Space-Optimized DP solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python house_robber_ii/reference.py   # replay the example cases
  uv run pytest house_robber_ii/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def rob(self, nums: List[int]) -> int:
        """Return the most money robbable in the circular street.

        Time:  O(n): two linear sweeps, one over each cut street.
        Space: O(n) for the two street slices; each sweep itself keeps two
               rolling totals, O(1) beyond the slices.
        """
        def rob_linear(houses: List[int]) -> int:
            two_back = 0  # best total over the street's houses up to i - 2
            one_back = 0  # best total over the street's houses up to i - 1
            for money in houses:
                best_here = max(one_back, two_back + money)
                two_back = one_back
                one_back = best_here
            return one_back

        if len(nums) == 1:
            return nums[0]
        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().rob(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
