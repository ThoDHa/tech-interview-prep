"""Reverse Linked List: https://leetcode.com/problems/reverse-linked-list/

Write-up & approaches: ../../docs/problems/reverse_linked_list.md

Reverse a singly linked list and return the new head.

  uv run python reverse_linked_list/solution.py   # debug one case (see CASE below)
  uv run pytest reverse_linked_list/              # run the test sets
"""

from typing import Optional

from harness import NotSolved, ListNode, build_linked_list, linked_list_to_list, pick_case


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in reverseList above, then run this file.
    # The case stores the list as a plain array; we marshal it to ListNode here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    head = build_linked_list(case["args"][0])
    result = Solution().reverseList(head)
    print(f"case {case['id']}: list = {case['args'][0]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {linked_list_to_list(result)}")
