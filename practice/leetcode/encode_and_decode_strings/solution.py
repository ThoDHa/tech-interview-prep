"""Encode and Decode Strings — https://leetcode.com/problems/encode-and-decode-strings/

Write-up & approaches: ../../docs/problems/encode_and_decode_strings.md

Design an algorithm to encode **a list of strings** to **a string**. The **encoded string** is then sent over the network and is **decoded** back to the **original list** of strings. **Machine 1 (send

  uv run python encode_and_decode_strings/solution.py   # debug one case (see CASE below)
  uv run pytest encode_and_decode_strings/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, *args):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
