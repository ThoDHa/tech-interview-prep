"""Encode and Decode Strings — https://leetcode.com/problems/encode-and-decode-strings/

Write-up & approaches: ../../../docs/leetcode/encode_and_decode_strings.md

Design an algorithm to encode **a list of strings** to **a string**. The **encoded string** is then sent over the network and is **decoded** back to the **original list** of strings. **Machine 1 (send

  uv run python leetcode/encode_and_decode_strings/solution.py   # debug one case (see CASE below)
  uv run pytest leetcode/encode_and_decode_strings/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case, run_operations


class Solution:
    def encode(self, strs: List[str]) -> str:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def decode(self, s: str) -> List[str]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a Solution method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "encode_empty_list"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(Solution, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement Solution's methods first")
