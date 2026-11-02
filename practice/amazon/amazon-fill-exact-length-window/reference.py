"""Fill One Exact-Length Binary Window — https://www.fastprep.io/problems/amazon-fill-exact-length-window

Write-up & approaches: ../../../docs/amazon/amazon-fill-exact-length-window.md

Reference implementation of the write-up's recommended Prefix Sums
solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-fill-exact-length-window/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-fill-exact-length-window/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def solve(self, log: str, k: int) -> int:
        """Return the largest count of ones obtainable by filling exactly
        one length-`k` window of the binary string `log` with ones.

        Filling a window adds exactly its number of zeros to the string's
        ones count, so the answer is the string's total ones plus the
        largest zero count of any length-`k` window. A prefix-sum array
        turns each window's zero count into one subtraction: zeros in
        `log[s:s+k]` equal `k - (prefix[s + k] - prefix[s])`.

        Args:
            log: A nonempty binary string.
            k: The window length, at least 1 and at most `len(log)`, so a
                length-`k` substring exists.

        Returns:
            The maximum total ones after filling one window.

        Time:  O(n): one pass builds the prefix array, one pass evaluates
            the windows, n = len(log).
        Space: O(n): the prefix array of `n + 1` running totals.
        """
        prefix: List[int] = [0]
        for digit in log:
            prefix.append(prefix[-1] + (digit == "1"))
        total_ones = prefix[-1]
        best_zeros = 0
        for start in range(len(log) - k + 1):
            ones_in_window = prefix[start + k] - prefix[start]
            best_zeros = max(best_zeros, k - ones_in_window)
        return total_ones + best_zeros


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
