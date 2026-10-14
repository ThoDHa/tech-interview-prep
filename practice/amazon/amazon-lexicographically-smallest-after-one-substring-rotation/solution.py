"""Lexicographically Smallest After One Substring Rotation — https://www.fastprep.io/problems/amazon-lexicographically-smallest-after-one-substring-rotation

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-lexicographically-smallest-after-one-substring-rotation.md

You are given a string s. You must choose one non-empty contiguous substring of s and rotate that substring to the right by one position exactly once.

  uv run python amazon_oa/amazon-lexicographically-smallest-after-one-substring-rotation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-lexicographically-smallest-after-one-substring-rotation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def smallestStringAfterOneRotation(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in smallestStringAfterOneRotation above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().smallestStringAfterOneRotation(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
