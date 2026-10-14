"""Missing Number — https://leetcode.com/problems/missing-number/

Write-up & approaches: ../../docs/problems/missing_number.md
Reference implementation of the write-up's Gauss Sum Formula solution,
kept next to the harness so authored cases stay falsifiable. Your own
attempt lives in solution.py.

  uv run python missing_number/reference.py   # replay the example cases
  uv run pytest missing_number/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        """Return the one value in `0..n` absent from `nums`.

        The full range `0..n` sums to `n * (n + 1) // 2`; subtracting
        the array's actual sum leaves exactly the missing value.

        Args:
            nums: `n` distinct integers, each in `0..n`.

        Returns:
            The single value from `0..n` not present in `nums`.

        Time:  O(n): one pass to sum the array.
        Space: O(1): one accumulator.
        """
        n = len(nums)
        return n * (n + 1) // 2 - sum(nums)


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().missingNumber(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
