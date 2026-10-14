"""Palindromic Substrings — https://leetcode.com/problems/palindromic-substrings/

Write-up & approaches: ../../docs/problems/palindromic_substrings.md
Reference implementation of the write-up's Expand Around Center solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python palindromic_substrings/reference.py   # replay the example cases
  uv run pytest palindromic_substrings/               # run the test sets
"""

from harness import pick_case


class Solution:
    def countSubstrings(self, s: str) -> int:
        """Return the number of substrings of s that are palindromes.

        Time:  O(n^2): 2n - 1 centers, each expansion up to O(n) steps.
        Space: O(1): counters and two pointers only.
        """
        n = len(s)

        def expand(left: int, right: int) -> int:
            # Each successful comparison confirms one palindromic substring
            # centered on this pair of pointers.
            count = 0
            while left >= 0 and right < n and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
            return count

        total = 0
        for i in range(n):
            # Odd-length palindromes centered on the character at i.
            total += expand(i, i)
            # Even-length palindromes centered on the gap after i.
            total += expand(i, i + 1)
        return total


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().countSubstrings(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
