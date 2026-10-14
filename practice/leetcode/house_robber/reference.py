"""House Robber — https://leetcode.com/problems/house-robber/

Write-up & approaches: ../../docs/problems/house_robber.md
Reference implementation of the write-up's Space-Optimized DP solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python house_robber/reference.py   # replay the example cases
  uv run pytest house_robber/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def rob(self, nums: List[int]) -> int:
        """Return the most money robbable without robbing two adjacent houses.

        Time:  O(n): one pass over the houses, constant work per house.
        Space: O(1): the dp table collapses to two rolling totals.
        """
        two_back = 0  # best total over houses 0 .. i-2
        one_back = 0  # best total over houses 0 .. i-1
        for money in nums:
            best_here = max(one_back, two_back + money)
            two_back = one_back
            one_back = best_here
        return one_back


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().rob(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
