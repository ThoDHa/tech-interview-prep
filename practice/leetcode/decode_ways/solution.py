"""Decode Ways — https://leetcode.com/problems/decode-ways/

Write-up & approaches: ../../docs/problems/decode_ways.md

A string consisting of uppercase english characters can be encoded to a number using the following mapping: ```java 'A' -> "1" 'B' -> "2" ... 'Z' -> "26" ``` To **decode** a message, digits must be gr

  uv run python decode_ways/solution.py   # debug one case (see CASE below)
  uv run pytest decode_ways/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def numDecodings(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in numDecodings above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().numDecodings(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
