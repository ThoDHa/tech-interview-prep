"""Search for an Element in a Stream — https://www.fastprep.io/problems/amazon-search-element-in-stream

Write-up & approaches: ../../../docs/amazon/amazon-search-element-in-stream.md

Values arrive one at a time in a stream. At any moment, you may be asked whether a given value has already arrived.

  uv run python amazon/amazon-search-element-in-stream/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-search-element-in-stream/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, operations, values):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    CASE = None
    if CASE is None:
        print("no cases authored yet; add cases to cases.json or cases_full.json, then set CASE to an id")
    else:
        case = pick_case(__file__, CASE)
        result = Solution().solve(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
