"""Word Dictionary with Wildcard Find — https://www.fastprep.io/problems/amazon-wildcard-word-dictionary

Write-up & approaches: ../../../docs/amazon/amazon-wildcard-word-dictionary.md

Build a word dictionary that supports inserting words and finding words with wildcards. Process the rows of operations from left to right. The dictionary starts empty, and each row has one of these fo

  uv run python amazon/amazon-wildcard-word-dictionary/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-wildcard-word-dictionary/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, operations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    CASE = None
    if CASE is None:
        print("no cases authored yet; add cases to cases.json or cases_full.json, then set CASE to an id")
    else:
        case = pick_case(__file__, CASE)
        result = Solution().solve(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
