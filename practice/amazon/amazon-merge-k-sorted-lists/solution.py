"""Merge k Sorted Lists — https://www.fastprep.io/problems/amazon-merge-k-sorted-lists

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-merge-k-sorted-lists.md

You are given an array lists containing k linked-list heads. Every linked list is sorted in ascending order.

  uv run python amazon_oa/amazon-merge-k-sorted-lists/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-merge-k-sorted-lists/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def mergeKLists(self, lists):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mergeKLists above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().mergeKLists(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
