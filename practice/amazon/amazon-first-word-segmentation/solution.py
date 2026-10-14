"""First Valid Word Segmentation — https://www.fastprep.io/problems/amazon-first-word-segmentation

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-first-word-segmentation.md

Given a continuous lowercase string s and an array dictionary representing the words accepted by isWord, split s into a sequence of dictionary words whose concatenation is exactly s.

  uv run python amazon_oa/amazon-first-word-segmentation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-first-word-segmentation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def segmentWords(self, s, dictionary):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in segmentWords above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().segmentWords(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
