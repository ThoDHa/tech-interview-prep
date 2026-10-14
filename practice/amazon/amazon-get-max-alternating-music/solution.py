"""Get Max Alternating Music — https://www.fastprep.io/problems/amazon-get-max-alternating-music

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-alternating-music.md

Amazon Music is working on harmonizing their music playlist.

  uv run python amazon_oa/amazon-get-max-alternating-music/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-alternating-music/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxAlternatingMusic(self, music, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxAlternatingMusic above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxAlternatingMusic(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
