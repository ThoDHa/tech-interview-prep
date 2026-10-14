"""Reverse Nodes In K Group — https://leetcode.com/problems/reverse-nodes-in-k-group/

Write-up & approaches: ../../docs/problems/reverse_nodes_in_k_group.md

You are given the head of a singly linked list `head` and a positive integer `k`. You must reverse the first `k` nodes in the linked list, and then reverse the next `k` nodes, and so on. If there are 

  uv run python reverse_nodes_in_k_group/solution.py   # debug one case (see CASE below)
  uv run pytest reverse_nodes_in_k_group/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, *args):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
