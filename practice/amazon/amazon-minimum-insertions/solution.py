"""Min Insertions — https://www.fastprep.io/problems/amazon-minimum-insertions

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-insertions.md

Amazon CodeCraft introduces you to an engaging problem-solving challenge. You are

  uv run python amazon_oa/amazon-minimum-insertions/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-insertions/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumInsertions(self, finalList, initialList):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumInsertions above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumInsertions(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
