"""Next Greater Element I — https://www.fastprep.io/problems/amazon-next-greater-element-i

Write-up & approaches: ../../../docs/amazon/amazon-next-greater-element-i.md

You are given two arrays of distinct integers, query and reference, where every query value appears in reference.

  uv run python amazon/amazon-next-greater-element-i/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-next-greater-element-i/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def nextGreaterElement(self, query, reference):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in nextGreaterElement above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().nextGreaterElement(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
