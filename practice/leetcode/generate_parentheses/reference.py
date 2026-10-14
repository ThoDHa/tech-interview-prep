"""Generate Parentheses — https://leetcode.com/problems/generate-parentheses/

Write-up & approaches: ../../docs/problems/generate_parentheses.md
Reference implementation of the write-up's Backtracking solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

You are given an integer `n`. Return all well-formed parentheses strings that you can generate with `n` pairs of parentheses.

  uv run python generate_parentheses/reference.py   # debug one case (see CASE below)
  uv run pytest generate_parentheses/               # run the test sets
"""

from harness import pick_case


class Solution:
    def generateParenthesis(self, n):
        """Return every well-formed string made of `n` pairs of parentheses.

        Grows one shared `path` buffer along a depth-first decision tree:
        append `'('` while `open_count < n`, append `')'` while
        `close_count < open_count`, and record the join at depth `2 * n`.
        Both guards keep every explored prefix extendable to a well-formed
        string, so no doomed branch is ever built, and each append is
        undone on the way back up.

        Args:
            n: Number of parenthesis pairs, 1 <= n <= 7.

        Returns:
            The Catalan(n) well-formed strings, in the lexicographic
            order produced by trying `'('` before `')'` at every node.

        Time:  O(4^n / sqrt(n)): the tree has Catalan(n) leaves
            (Catalan(n) ~ 4^n / n^1.5), each joined and copied in O(n),
            and the pruned internal nodes stay within the same bound.
        Space: O(n) auxiliary for the shared buffer and the recursion
            stack, plus the output itself.
        """

        result = []
        path = []

        def backtrack(open_count: int, close_count: int) -> None:
            if len(path) == 2 * n:
                result.append("".join(path))
                return
            if open_count < n:
                path.append("(")
                backtrack(open_count + 1, close_count)
                path.pop()
            if close_count < open_count:
                path.append(")")
                backtrack(open_count, close_count + 1)
                path.pop()

        backtrack(0, 0)
        return result


if __name__ == "__main__":
    # Debug playground: set a breakpoint in generateParenthesis above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().generateParenthesis(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
