"""Reorder List — https://leetcode.com/problems/reorder-list/

Write-up & approaches: ../../docs/problems/reorder_list.md
Reference implementation of the write-up's Reverse-and-Merge solution.

Reorder the nodes of a singly linked list to alternate first, last, second,
second-to-last, and so on: `[0, 1, 2, 3, 4]` becomes `[0, 4, 1, 3, 2]`.

  uv run python reorder_list/reference.py   # debug one case (see CASE below)
  uv run pytest reorder_list/              # run the test sets
"""

from harness import build_linked_list, linked_list_to_list, pick_case


def reorder_list(head):
    """Rewire `head`'s nodes into the alternating first-last order in place.

    Args:
        head: First node of a singly linked list (None for an empty list).

    Returns:
        The same (rewired) head node.

    Time:  O(n): three linear passes (slow/fast split, reversal, merge).
    Space: O(1): pointer surgery only, no node allocation.
    """
    if head is None or head.next is None:
        return head

    second_half = split_second_half(head)
    second_half = reverse_list(second_half)
    merge_alternating(head, second_half)
    return head


def split_second_half(head):
    """Cut the list after its midpoint and return the second half's head.

    The slow pointer advances one node per step while the fast pointer
    advances two, so when `fast` runs off the end `slow` sits at the middle
    (on the last node of the first half for odd lengths).

    Args:
        head: Non-empty list with at least two nodes.

    Returns:
        The head of the second half, with the first half NUL-terminated.

    Time:  O(n). Space: O(1).
    """
    slow, fast = head, head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    second_half = slow.next
    slow.next = None
    return second_half


def reverse_list(head):
    """Reverse a linked list in place and return the new head.

    Args:
        head: First node of the segment to reverse, possibly None.

    Returns:
        The segment's former tail, now its head.

    Time:  O(n). Space: O(1).
    """
    previous = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous = current
        current = following
    return previous


def merge_alternating(first, second):
    """Interleave `second` into `first` by node, leaving both consumed.

    After the split the first half is never shorter than the second, so
    every round can splice one node of `second` after one node of `first`.

    Args:
        first: Head of the equal-or-longer half.
        second: Head of the reversed second half.

    Returns:
        None: the spliced result is reached through `first`.

    Time:  O(n). Space: O(1).
    """
    while second is not None:
        first_next = first.next
        second_next = second.next
        first.next = second
        second.next = first_next
        first = first_next
        second = second_next


if __name__ == "__main__":
    # Debug playground: set a breakpoint in reorder_list above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    head = build_linked_list(case["args"][0])
    result = reorder_list(head)
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {linked_list_to_list(result)}")
