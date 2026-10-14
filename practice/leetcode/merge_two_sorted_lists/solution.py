"""Merge Two Sorted Lists: https://leetcode.com/problems/merge-two-sorted-lists/

Write-up & approaches: ../../docs/problems/merge_two_sorted_lists.md

You are given the heads of two sorted linked lists `list1` and `list2`. Splice
their nodes together into one sorted list and return the head of the merged list.

  uv run python merge_two_sorted_lists/solution.py   # debug one case (see CASE below)
  uv run pytest merge_two_sorted_lists/              # run the test sets
"""

from typing import Optional

from harness import NotSolved, ListNode, build_linked_list, linked_list_to_list, pick_case


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mergeTwoLists above, then run this file.
    # The case stores each list as a plain array; we marshal them to ListNode here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    list1 = build_linked_list(case["args"][0])
    list2 = build_linked_list(case["args"][1])
    result = Solution().mergeTwoLists(list1, list2)
    print(f"case {case['id']}: list1 = {case['args'][0]}, list2 = {case['args'][1]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {linked_list_to_list(result)}")
