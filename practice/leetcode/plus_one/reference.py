"""Plus One — https://leetcode.com/problems/plus-one/

Write-up & approaches: ../../docs/problems/plus_one.md
Canonical reference implementation: the write-up's Right-to-Left Carry
Ripple solution. Your own attempt lives in solution.py.

You are given an integer array `digits`, where each `digits[i]` is the `ith`
digit of a large integer. It is ordered from most significant to least
significant digit, and it will not contain any leading zero. Return the
digits of the given integer after incrementing it by one.

  uv run python plus_one/reference.py   # replay the example cases
  uv run pytest plus_one/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        """Increment the big-integer digit array by one.

        Walks from the least significant digit: the first digit below 9
        absorbs the carry and the array returns immediately, each 9 rolls
        over to 0, and a full roll prepends the final carry 1.

        Args:
            digits: Most-significant-first digits, no leading zero,
                0 <= digits[i] <= 9. Mutated in place when the increment
                fits; returned as the result either way.

        Returns:
            The digits of the incremented integer, `n + 1` long exactly
            when every input digit was 9.

        Time:  O(n): stops at the first non-nine, worst case one full pass.
        Space: O(1): in-place ripple; the all-nines return list is the
            required output, not scratch.
        """
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                # Carry absorbed here: nothing to the left changes
                digits[i] += 1
                return digits
            digits[i] = 0
        return [1] + digits


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().plusOne(list(case["args"][0]))
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
