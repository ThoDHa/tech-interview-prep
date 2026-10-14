"""Remove Nth Node From End of List — https://leetcode.com/problems/remove-nth-node-from-end-of-list/

Write-up & approaches: ../../docs/problems/remove_nth_node_from_end_of_list.md

Canonical reference implementation: the write-up's Two Pointers solution
(single pass with a gap-locked pointer pair). Your own attempt lives in
solution.py.

Given the `head` of a linked list and an integer `n`, remove the `nth` node from the end of the list and return its head.

  uv run python remove_nth_node_from_end_of_list/reference.py   # debug one case (see below)
  uv run pytest remove_nth_node_from_end_of_list/               # run the test sets
"""

from typing import List, Optional

from harness import ListNode, build_linked_list, linked_list_to_list


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """Delete the `n`th node from the end in one traversal.

        Offsets `fast` exactly `n` nodes ahead of `slow` (both anchored at a
        dummy in front of `head`), then advances the pair in lockstep. The
        gap stays `n`, so when `fast` reaches the last node `slow` sits on
        the victim's predecessor and one rewire deletes it. The dummy makes
        deleting the head (`n == sz`) the same code as every other deletion.

        Args:
            head: First node of the list, never None.
            n: Distance from the end, 1 <= n <= list length.

        Returns:
            The head of the list with the victim removed, as fresh linkage
            over the same nodes (the victim is unlinked, not freed).

        Time:  O(sz): `fast` crosses the list exactly once.
        Space: O(1): the dummy node and the two pointers.
        """
        dummy = ListNode(next=head)
        fast = dummy
        slow = dummy
        for _ in range(n):
            fast = fast.next

        while fast.next is not None:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next
        return dummy.next


def remove_nth_from_end(values: List[int], n: int) -> List[int]:
    """Convenience wrapper: list in, list out, for the debug playground."""
    return linked_list_to_list(Solution().removeNthFromEnd(build_linked_list(values), n))


if __name__ == "__main__":
    # Debug playground: set a breakpoint in removeNthFromEnd above, then run
    # this file. cases.json is empty (multi-method starter), so a literal
    # example stands in.
    values = [1, 2, 3, 4]
    n = 2
    print(f"args = head = {values}, n = {n}")
    print(f"expected: [1, 2, 4]")
    print(f"got:      {remove_nth_from_end(values, n)}")
