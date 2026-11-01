"""Lowest Common Ancestor in an N-ary Tree — https://www.fastprep.io/problems/amazon-nary-tree-lowest-common-ancestor

Write-up & approaches: ../../../docs/amazon/amazon-nary-tree-lowest-common-ancestor.md

Reference implementation of the write-up's recommended Ancestor-Set
Climb solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-nary-tree-lowest-common-ancestor/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-nary-tree-lowest-common-ancestor/              # run the test sets
"""

from typing import List, Set

from harness import pick_case


class Solution:
    def lowestCommonAncestor(self, parent: List[int], p: int, q: int) -> int:
        """Return the deepest node that is an ancestor of both p and q.

        Climbing from a node to the root visits exactly that node's
        ancestors, deepest first. The climb from `p` records every node
        it passes (p included, since a node is an ancestor of itself)
        into `ancestors_of_p`; the climb from `q` then walks up until it
        steps onto the first node the first climb already visited. That
        first shared node is the lowest shared ancestor: any deeper
        shared ancestor would have been visited by the q-climb earlier,
        and every node the q-climb passes is an ancestor of q.

        Args:
            parent: The tree encoding; parent[root] is -1, every other
                entry is the node's direct parent.
            p: First query node, 0 <= p < len(parent).
            q: Second query node, 0 <= q < len(parent).

        Returns:
            The label of the lowest common ancestor of p and q.

        Time:  O(depth_p + depth_q): two climbs that each stop at the
            root or at the first shared node.
        Space: O(depth_p): the set holds the ancestor chain of p.
        """
        ancestors_of_p: Set[int] = set()
        node = p
        while node != -1:
            ancestors_of_p.add(node)
            node = parent[node]

        node = q
        while node not in ancestors_of_p:
            node = parent[node]
        return node


if __name__ == "__main__":
    # Debug playground: set a breakpoint in lowestCommonAncestor above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().lowestCommonAncestor(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
