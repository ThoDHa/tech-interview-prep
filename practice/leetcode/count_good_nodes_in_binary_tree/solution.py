"""Count Good Nodes In Binary Tree — https://leetcode.com/problems/count-good-nodes-in-binary-tree/

Write-up & approaches: ../../docs/problems/count_good_nodes_in_binary_tree.md

Within a binary tree, a node `x` is considered **good** if the path from the root of the tree to the node `x` contains no nodes with a value greater than the value of node `x` Given the root of a bina

  uv run python count_good_nodes_in_binary_tree/solution.py   # debug one case (see CASE below)
  uv run pytest count_good_nodes_in_binary_tree/              # run the test sets
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
