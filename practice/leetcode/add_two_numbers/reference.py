"""Add Two Numbers — https://leetcode.com/problems/add-two-numbers/

Write-up & approaches: ../../docs/problems/add_two_numbers.md

Canonical reference implementation: the write-up's Digit-wise Addition
solution (streaming schoolbook addition with a carry). Your own attempt
lives in solution.py.

You are given two non-empty linked lists, `l1` and `l2`, where each represents a non-negative integer with digits stored in reverse order. Each node contains a single digit. Return the sum of the two numbers as a linked list.

  uv run python add_two_numbers/reference.py   # debug one case (see below)
  uv run pytest add_two_numbers/               # run the test sets
"""

from typing import Optional

from harness import ListNode, build_linked_list, linked_list_to_list


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """Sum two reversed-digit lists into a new list, digit by digit.

        Walks both lists together reading `0` past either list's end, so
        unequal lengths need no padding. Each round emits
        `(digit1 + digit2 + carry) % 10` and promotes `// 10`; the loop
        keeps running while any list has nodes or a carry is owed, which
        is what appends the final carry node with no special case.

        Args:
            l1: Digits of the first number, least significant first.
            l2: Digits of the second number, least significant first.

        Returns:
            Fresh nodes holding the sum, least significant digit first;
            the input lists are untouched.

        Time:  O(max(n, m)): one iteration per output digit.
        Space: O(max(n, m)): the output list; auxiliary state is O(1).
        """
        dummy = ListNode()
        current = dummy
        carry = 0
        n1, n2 = l1, l2
        while n1 is not None or n2 is not None or carry != 0:
            digit1 = n1.val if n1 is not None else 0
            digit2 = n2.val if n2 is not None else 0
            total = digit1 + digit2 + carry
            current.next = ListNode(total % 10)
            current = current.next
            carry = total // 10
            if n1 is not None:
                n1 = n1.next
            if n2 is not None:
                n2 = n2.next
        return dummy.next


if __name__ == "__main__":
    # Debug playground: set a breakpoint in addTwoNumbers above, then run this
    # file. cases.json is empty (multi-method starter), so a literal example
    # stands in.
    values1 = [1, 2, 3]
    values2 = [4, 5, 6]
    result = Solution().addTwoNumbers(
        build_linked_list(values1), build_linked_list(values2)
    )
    print(f"args = {values1}, {values2}")
    print(f"expected: [5, 7, 9]")
    print(f"got:      {linked_list_to_list(result)}")
