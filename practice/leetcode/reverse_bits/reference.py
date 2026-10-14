"""Reverse Bits — https://leetcode.com/problems/reverse-bits/

Write-up & approaches: ../../docs/problems/reverse_bits.md
Reference implementation of the write-up's Build-by-Shift Loop solution,
kept next to the harness so authored cases stay falsifiable. Your own
attempt lives in solution.py.

  uv run python reverse_bits/reference.py   # replay the example cases
  uv run pytest reverse_bits/               # run the test sets
"""

from harness import pick_case

BIT_COUNT = 32


class Solution:
    def reverseBits(self, n: int) -> int:
        """Return `n`'s 32 bits in reverse order.

        Builds the answer one bit per pass: shift `result` left to make
        room, append `n`'s lowest bit, and drop that bit from `n`. After
        32 passes every bit has moved from position `i` to position
        `31 - i`.

        Args:
            n: An unsigned 32-bit integer, `0 <= n < 2^32`.

        Returns:
            The bit-reversed 32-bit integer.

        Time:  O(1): exactly 32 constant-work passes.
        Space: O(1): the two working integers.
        """
        result = 0
        for _ in range(BIT_COUNT):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result


if __name__ == "__main__":
    # Debug playground: cases.json is empty (binary-literal example input),
    # so the write-up's Example 1 stands in.
    case_id = "example_1_value_21"
    case = pick_case(__file__, case_id)
    result = Solution().reverseBits(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
