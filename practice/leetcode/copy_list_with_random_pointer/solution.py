"""Copy List With Random Pointer — https://leetcode.com/problems/copy-list-with-random-pointer/

Write-up & approaches: ../../docs/problems/copy_list_with_random_pointer.md

You are given the head of a linked list of length `n`. Unlike a singly linked list, each node contains an additional pointer `random`, which may point to any node in the list, or `null`. Create a **de

  uv run python copy_list_with_random_pointer/solution.py   # debug one case (see CASE below)
  uv run pytest copy_list_with_random_pointer/              # run the test sets
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
