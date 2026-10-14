"""Merge k Sorted Lists: https://leetcode.com/problems/merge-k-sorted-lists/

Write-up & approaches: ../../docs/problems/merge_k_sorted_lists.md

You are given an array of `k` linked lists, each sorted in ascending order. Merge
all the linked lists into one sorted linked list and return its head.

  uv run python merge_k_sorted_lists/solution.py   # debug one case (see CASE below)
  uv run pytest merge_k_sorted_lists/              # run the test sets
"""

from typing import List, Optional

from harness import NotSolved, ListNode, build_linked_list, linked_list_to_list, pick_case


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mergeKLists above, then run this file.
    # Each list is stored as a plain value array; we marshal them to ListNodes here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    lists = [build_linked_list(values) for values in case["args"][0]]
    result = Solution().mergeKLists(lists)
    print(f"case {case['id']}: lists = {case['args'][0]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {linked_list_to_list(result)}")
