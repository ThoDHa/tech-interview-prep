"""Number of 1 Bits — https://leetcode.com/problems/number-of-1-bits/

Write-up & approaches: ../../docs/problems/number_of_1_bits.md
Reference implementation of the write-up's Brian Kernighan Erase Loop
solution, kept next to the harness so authored cases stay falsifiable.
Your own attempt lives in solution.py.

  uv run python number_of_1_bits/reference.py   # replay the example cases
  uv run pytest number_of_1_bits/               # run the test sets
"""

from harness import pick_case


class Solution:
    def hammingWeight(self, n: int) -> int:
        """Return the number of set bits in the 32-bit representation of `n`.

        Each pass of the loop erases the lowest set bit of `n` with
        `n & (n - 1)`: subtracting one turns that bit off and every bit
        below it on, so the exclusive-and keeps only the bits above it.
        The loop runs once per set bit, not once per position.

        Args:
            n: A non-negative integer below `2^31` (fits in 32 bits).

        Returns:
            The population count, `0` to `32`.

        Time:  O(k): one iteration per set bit, `k <= 32`.
        Space: O(1): the working copy of `n`.
        """
        count = 0
        while n:
            n &= n - 1
            count += 1
        return count


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().hammingWeight(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
