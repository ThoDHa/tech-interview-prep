"""Regular Expression Matching — https://leetcode.com/problems/regular-expression-matching/

Write-up & approaches: ../../docs/problems/regular_expression_matching.md
Reference implementation of the write-up's Top-Down Memoization solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python regular_expression_matching/reference.py   # replay the example cases
  uv run pytest regular_expression_matching/               # run the test sets
"""

from harness import pick_case


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """Return whether `p` matches all of `s`, with '.' and 'x*' tokens.

        Time:  O(m * n): O(m * n) states, each deciding in O(1); the naive
            recursion's exponential blowup comes from re-deciding states.
        Space: O(m * n): one memo entry per consumed prefix pair plus the
            recursion stack.
        """
        memo = {}

        def match(i: int, j: int) -> bool:
            if j == len(p):
                return i == len(s)
            if (i, j) in memo:
                return memo[(i, j)]
            first = i < len(s) and (p[j] == s[i] or p[j] == ".")
            if j + 1 < len(p) and p[j + 1] == "*":
                answer = match(i, j + 2) or (first and match(i + 1, j))
            else:
                answer = first and match(i + 1, j + 1)
            memo[(i, j)] = answer
            return answer

        return match(0, 0)


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2", "example_3"):
        case = pick_case(__file__, case_id)
        result = Solution().isMatch(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
