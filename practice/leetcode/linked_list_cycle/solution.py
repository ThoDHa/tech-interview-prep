"""Linked List Cycle: https://leetcode.com/problems/linked-list-cycle/

Write-up & approaches: ../../docs/problems/linked_list_cycle.md

Given `head`, the head of a linked list, determine if the linked list has a
cycle in it. `pos` denotes the index the tail's `next` connects to (-1 = none)
and is not passed to your method; the harness builds the cyclic list for you.

  uv run python linked_list_cycle/solution.py   # debug one case (see CASE below)
  uv run pytest linked_list_cycle/              # run the test sets
"""

from typing import Optional

from harness import NotSolved, ListNode, build_linked_list_with_cycle, pick_case


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in hasCycle above, then run this file.
    # The case stores [values, pos]; we marshal it to a (possibly cyclic) list.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    values, pos = case["args"]
    head = build_linked_list_with_cycle(values, pos)
    result = Solution().hasCycle(head)
    print(f"case {case['id']}: values = {values}, pos = {pos}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
