"""Sum of Two Integers — https://leetcode.com/problems/sum-of-two-integers/

Write-up & approaches: ../../docs/problems/sum_of_two_integers.md
Reference implementation of the write-up's Masked Half-Adder Loop solution,
kept next to the harness so authored cases stay falsifiable. Your own
attempt lives in solution.py.

  uv run python sum_of_two_integers/reference.py   # replay the example cases
  uv run pytest sum_of_two_integers/               # run the test sets
"""

from harness import pick_case

MASK = 0xFFFFFFFF
SIGN_BIT = 1 << 31


class Solution:
    def getSum(self, a: int, b: int) -> int:
        """Return `a + b` using no `+` or `-` operator.

        A half-adder in hardware: exclusive or adds the bits where at
        most one operand is set, and the AND shifted left one carries
        where both are set. Loop until the carry dies. Both operands
        live masked to 32 bits so Python's open-ended integers behave
        like a fixed-width register, and the result is converted back
        to a signed value from its two's complement at the end.

        Args:
            a: First addend, in the signed 32-bit range.
            b: Second addend, in the signed 32-bit range.

        Returns:
            The signed 32-bit sum.

        Time:  O(1): at most 32 carry-propagation passes.
        Space: O(1): the two working registers.
        """
        a &= MASK
        b &= MASK
        while b:
            carry = ((a & b) << 1) & MASK
            a = (a ^ b) & MASK
            b = carry
        return a if a < SIGN_BIT else ~(a ^ MASK)


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().getSum(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
