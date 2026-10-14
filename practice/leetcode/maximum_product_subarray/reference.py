"""Maximum Product Subarray — https://leetcode.com/problems/maximum-product-subarray/

Write-up & approaches: ../../docs/problems/maximum_product_subarray.md
Reference implementation of the write-up's Kadane's Algorithm with Min-Max
Tracking solution, kept next to the harness so authored cases stay falsifiable.
Your own attempt lives in solution.py.

  uv run python maximum_product_subarray/reference.py   # replay the example cases
  uv run pytest maximum_product_subarray/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        """Return the largest product of any contiguous non-empty subarray.

        Carries the largest and smallest product of a subarray ending at the
        current index: multiplying by a negative value swaps which of the two
        extremes can become the largest, so both must be tracked.

        Args:
            nums: Non-empty integer array; each product fits a 32-bit int.

        Returns:
            The largest product over all contiguous non-empty subarrays.

        Time:  O(n): one pass, three candidates and two overwrites per element.
        Space: O(1): two rolling scalars plus the running answer.
        """
        best_ending = nums[0]
        worst_ending = nums[0]
        answer = nums[0]

        for i in range(1, len(nums)):
            candidates = (nums[i], nums[i] * best_ending, nums[i] * worst_ending)
            best_ending = max(candidates)
            worst_ending = min(candidates)
            answer = max(answer, best_ending)

        return answer


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().maxProduct(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
