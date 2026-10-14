"""Reverse Nodes In K Group — https://leetcode.com/problems/reverse-nodes-in-k-group/

Write-up & approaches: ../../docs/problems/reverse_nodes_in_k_group.md

Canonical reference implementation: the write-up's Iterative In-place
Reversal solution (per-group lookahead, flip, and stitch in O(1) space).
Your own attempt lives in solution.py.

You must reverse the first `k` nodes in the linked list, then the next `k`,
and so on; a trailing group smaller than `k` stays as it is.

  uv run python reverse_nodes_in_k_group/reference.py   # debug one case (see below)
  uv run pytest reverse_nodes_in_k_group/               # run the test sets
"""

from typing import Optional, Tuple

from harness import ListNode, build_linked_list, linked_list_to_list


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """Reverse each aligned group of `k` nodes in place.

        Before any flip, a lookahead walks `k` nodes from `group_head` (the
        node before the group) to the group's last node; falling off the end
        first means the trailing remainder is shorter than `k` and the loop
        returns. Each round then flips exactly the `k` nodes after
        `group_head` and stitches the reversed group between its predecessor
        and the next group's head. `group_head` advances to the reversed
        group's tail, which is the node before the next group.

        Args:
            head: First node of the list, never None.
            k: Group size, 1 <= k <= list length.

        Returns:
            The head of the relinked list over the same nodes; only `next`
            pointers change, values stay put.

        Time:  O(n): the lookahead and the flip each touch a group's nodes a
               constant number of times, and groups partition the list.
        Space: O(1): the dummy node and a constant number of pointers.
        """

        def reverse_k(node: ListNode) -> Tuple[ListNode, ListNode]:
            """Reverse `k` nodes starting at `node`; return (new first, new last)."""
            previous = node
            current = node.next
            for _ in range(k - 1):
                following = current.next
                current.next = previous
                previous = current
                current = following
            return previous, node

        dummy = ListNode(next=head)
        group_head = dummy
        while True:
            group_last = group_head
            for _ in range(k):
                group_last = group_last.next
                if group_last is None:
                    return dummy.next
            next_group = group_last.next
            new_first, new_last = reverse_k(group_head.next)
            group_head.next = new_first
            new_last.next = next_group
            group_head = new_last


if __name__ == "__main__":
    # Debug playground: set a breakpoint in reverseKGroup above, then run this
    # file. cases.json is empty (multi-method starter), so a literal example
    # stands in.
    values = [1, 2, 3, 4, 5, 6]
    k = 3
    result = Solution().reverseKGroup(build_linked_list(values), k)
    print(f"args = head = {values}, k = {k}")
    print(f"expected: [3, 2, 1, 6, 5, 4]")
    print(f"got:      {linked_list_to_list(result)}")
