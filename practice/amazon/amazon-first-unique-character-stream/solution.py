"""First Unique Character in a Stream — https://www.fastprep.io/problems/amazon-first-unique-character-stream

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-first-unique-character-stream.md

Characters arrive in the order of the string stream. After each arrival, append the earliest character seen so far whose frequency in the processed prefix is exactly one.

  uv run python amazon_oa/amazon-first-unique-character-stream/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-first-unique-character-stream/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def firstUniqueAfterEach(self, stream):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in firstUniqueAfterEach above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().firstUniqueAfterEach(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
