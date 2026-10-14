"""Same Tree — https://leetcode.com/problems/same-tree/

Write-up & approaches: ../../docs/problems/same_tree.md

Canonical reference implementation: the write-up's Recursive DFS solution
(the equivalence definition translated clause by clause). Your own attempt
lives in solution.py.

Given the roots of two binary trees `p` and `q`, return `true` if the trees are equivalent (same structure, same values), otherwise return `false`.

  uv run python same_tree/reference.py   # debug one case (see below)
  uv run pytest same_tree/               # run the test sets
"""

from typing import Optional

from harness import TreeNode, build_tree


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """Report whether two trees match in structure and values.

        Compares one aligned node pair per call. Both `None` means both
        subtrees are empty (equal); exactly one `None` means the structures
        diverge; differing values diverge too. Otherwise the verdict is the
        `and` of the two child-pair verdicts, and the first failing pair
        short-circuits its sibling.

        Args:
            p: Root of the first tree, or None.
            q: Root of the second tree, or None.

        Returns:
            True when the trees are equivalent, False otherwise.

        Time:  O(min(n, m)): one call per aligned pair until a mismatch or
               exhaustion, bounded by the smaller tree.
        Space: O(min(n, m)): call stack bounded by the smaller tree's height.
        """
        if p is None and q is None:
            return True
        if p is None or q is None:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in isSameTree above, then run this
    # file. cases.json is empty (multi-method starter), so literal examples
    # stand in.
    p_values = [1, 2, 3]
    q_values = [1, 2, 3]
    result = Solution().isSameTree(build_tree(p_values), build_tree(q_values))
    print(f"args = p = {p_values}, q = {q_values}")
    print(f"expected: True")
    print(f"got:      {result}")
