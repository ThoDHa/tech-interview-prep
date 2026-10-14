"""Distance Between Two Tree Nodes — https://www.fastprep.io/problems/amazon-distance-between-tree-nodes

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-distance-between-tree-nodes.md

You are given a rooted tree whose nodes are numbered from 1 through treeNodes. The arrays treeFrom and treeTo describe the undirected edges of the tree, and root identifies its root.

  uv run python amazon_oa/amazon-distance-between-tree-nodes/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-distance-between-tree-nodes/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def distanceBetweenNodes(self, treeNodes, treeFrom, treeTo, root, source, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in distanceBetweenNodes above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().distanceBetweenNodes(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
