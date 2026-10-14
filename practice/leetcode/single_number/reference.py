"""Single Number — https://leetcode.com/problems/single-number/

Write-up & approaches: ../../docs/problems/single_number.md
Reference implementation of the write-up's Exclusive-Or Accumulator solution,
kept next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python single_number/reference.py   # replay the example cases
  uv run pytest single_number/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """Return the value appearing an odd number of times.

        Folds every value into one accumulator with exclusive or. Each
        pair of equal values cancels to zero (`x ^ x == 0`), exclusive or
        is commutative and associative so fold order never matters, and
        `0 ^ v == v`, so after the fold only the unpaired value survives.

        Args:
            nums: Non-empty; every value appears exactly twice except one,
                which appears once.

        Returns:
            The single unpaired value.

        Time:  O(n): one exclusive-or per element.
        Space: O(1): one integer accumulator.
        """
        acc = 0
        for num in nums:
            acc ^= num
        return acc


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().singleNumber(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
