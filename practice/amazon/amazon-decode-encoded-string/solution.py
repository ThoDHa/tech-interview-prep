"""Decode an Encoded String — https://www.fastprep.io/problems/amazon-decode-encoded-string

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-decode-encoded-string.md

An encoded string uses positive repeat counts followed by bracketed segments. Decode it using these rules:

  uv run python amazon_oa/amazon-decode-encoded-string/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-decode-encoded-string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def decodeString(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in decodeString above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().decodeString(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
