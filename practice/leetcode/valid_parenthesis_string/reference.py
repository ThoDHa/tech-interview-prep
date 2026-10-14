"""Valid Parenthesis String — https://leetcode.com/problems/valid-parenthesis-string/

Write-up & approaches: ../../docs/problems/valid_parenthesis_string.md
Reference implementation of the write-up's Greedy Range Tracking solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python valid_parenthesis_string/reference.py   # replay the example cases
  uv run pytest valid_parenthesis_string/               # run the test sets
"""

from harness import pick_case


class Solution:
    def checkValidString(self, s: str) -> bool:
        """Return whether some reading of every `*` makes `s` balanced.

        Time:  O(n): one pass of two integer updates per character.
        Space: O(1): the two interval endpoints.
        """
        low = 0
        high = 0
        for letter in s:
            if letter == "(":
                low += 1
                high += 1
            elif letter == ")":
                low -= 1
                high -= 1
            else:
                low -= 1
                high += 1
            if high < 0:
                return False
            low = max(low, 0)
        return low == 0


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().checkValidString(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
