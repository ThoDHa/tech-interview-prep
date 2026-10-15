"""Merge k Sorted Lists — https://www.fastprep.io/problems/amazon-merge-k-sorted-lists

Write-up & approaches: ../../../docs/amazon/amazon-merge-k-sorted-lists.md

Canonical reference implementation: the write-up's Divide and Conquer
solution (log k rounds of pairwise two-list merges). Your own attempt
lives in solution.py.

You are given an array lists containing k linked-list heads. Every linked list is sorted in ascending order.

Merge all of the linked lists into one ascending linked list and return its head.

  uv run python amazon/amazon-merge-k-sorted-lists/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-merge-k-sorted-lists/                          # run the test sets
"""

from typing import List, Optional

from harness import ListNode, build_linked_list, linked_list_to_list


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """Merge k sorted lists into one ascending list.

        Pairwise merges are scheduled divide-and-conquer style: round
        after round, `pending` is walked two lists at a time and each
        pair is spliced by the classic two-list merge, so every merge
        stays between lists of similar length. Each node takes part in
        exactly one merge per round, and pairing halves the count, which
        is where the `log k` rounds come from. An odd tail merges
        against `None` and passes through unchanged; equal values keep
        their input order because the splice prefers `first` on ties.

        Args:
            lists: Heads of the k sorted lists; entries and the array
                itself may be empty.

        Returns:
            The head of the merged ascending list, or None when every
            input list is empty. The input nodes are relinked, not
            copied.

        Time:  O(total_nodes * log k): each round merges every node once
            and there are log k rounds.
        Space: O(k): the per-round list of up to ceil(k/2) merged heads;
            both loops are iterative, so no recursion stack grows.
        """
        if not lists:
            return None

        def merge_two_lists(
            first: Optional[ListNode], second: Optional[ListNode]
        ) -> Optional[ListNode]:
            dummy = ListNode()
            tail = dummy

            while first is not None and second is not None:
                if first.val <= second.val:
                    tail.next = first
                    first = first.next
                else:
                    tail.next = second
                    second = second.next
                tail = tail.next

            tail.next = first if first is not None else second
            return dummy.next

        pending = list(lists)
        while len(pending) > 1:
            merged_pairs: List[Optional[ListNode]] = []
            for pair_start in range(0, len(pending), 2):
                first = pending[pair_start]
                second = (
                    pending[pair_start + 1]
                    if pair_start + 1 < len(pending)
                    else None
                )
                merged_pairs.append(merge_two_lists(first, second))
            pending = merged_pairs

        return pending[0]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mergeKLists above, then run
    # this file. cases.json is empty (not JSON-representable input), so a
    # literal example stands in.
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    merged = Solution().mergeKLists([build_linked_list(values) for values in lists])
    print(f"args = lists = {lists}")
    print(f"expected: [1, 1, 2, 3, 4, 4, 5, 6]")
    print(f"got:      {linked_list_to_list(merged)}")
