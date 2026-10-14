"""Reverse Binary String — https://www.fastprep.io/problems/amazon-reverse-binary-string

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-reverse-binary-string.md

You are given a binary string. Find the minimum number of operations required to reverse it. An operation is defined as:

  uv run python amazon_oa/amazon-reverse-binary-string/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-reverse-binary-string/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def reverseBinaryString(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in reverseBinaryString above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().reverseBinaryString(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
