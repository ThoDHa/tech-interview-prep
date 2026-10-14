"""Middle of the Linked List: https://leetcode.com/problems/middle-of-the-linked-list/

Write-up & approaches: ../../docs/problems/middle_of_the_linked_list.md

Given the `head` of a singly linked list, return the middle node. If there are
two middle nodes, return the second middle node.

  uv run python middle_of_the_linked_list/solution.py   # debug one case (see CASE below)
  uv run pytest middle_of_the_linked_list/              # run the test sets
"""

from typing import Optional

from harness import NotSolved, ListNode, build_linked_list, linked_list_to_list, pick_case


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in middleNode above, then run this file.
    # The case stores the list as a plain array; we marshal it to ListNode here.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    head = build_linked_list(case["args"][0])
    result = Solution().middleNode(head)
    print(f"case {case['id']}: list = {case['args'][0]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {linked_list_to_list(result)}")
