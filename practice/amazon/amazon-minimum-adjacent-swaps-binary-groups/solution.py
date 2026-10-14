"""Minimum Adjacent Swaps to Group Binary Values — https://www.fastprep.io/problems/amazon-minimum-adjacent-swaps-binary-groups

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-adjacent-swaps-binary-groups.md

You are given a binary array bits. Using adjacent swaps, rearrange it so that equal values form two contiguous groups.

  uv run python amazon_oa/amazon-minimum-adjacent-swaps-binary-groups/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-adjacent-swaps-binary-groups/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minimumAdjacentSwaps(self, bits):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minimumAdjacentSwaps above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minimumAdjacentSwaps(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
