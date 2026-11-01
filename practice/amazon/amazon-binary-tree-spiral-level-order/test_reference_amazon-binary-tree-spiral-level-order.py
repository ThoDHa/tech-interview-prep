"""Reference-parametrized gauntlet for Binary Tree Spiral Level Order.

The generator-emitted test module carries a module-level skip (the
example input `root` is not JSON-representable), so cases_full.json
carries the level-array serialization in args form and this module
marshals each case through harness.build_tree before the plain `==`
comparison; the generated module stays byte-identical. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a depth-bucketed
DFS (explicit stack, left-first preorder, values appended per depth,
alternate buckets reversed), which shares no mechanism with the
reference's level-size BFS. The output direction is fixed by the
statement (root level left to right), so no canonicalization applies.

The gauntlet enumerates the statement's named corners in the JSON band:
the three authored examples (empty tree, skipped nulls, alternating
direction), single node, one-sided children, left/right/alternating
chains, complete trees, sparse null holes, duplicate values at and
across levels, all-negative values, and the +-10^6 value bounds, plus a
seeded random band of 100 trees drawn up to 40 nodes each (the frozen
band realizes 18 nodes at the maximum, median 6). Two further corners
stay out of the JSON because their serialized form exceeds the
eye-auditable bound; both are constructed here and their expectations
follow from the construction:

- test_constructed_perfect_tree_of_255_nodes_alternates_through_eight_levels:
  a perfect tree of eight levels (255 nodes, depths 0 through 7,
  within the 500-node bound) serialized as values 1..255 in level
  order. Level d of a perfect tree holds exactly the values 2^d
  through 2^(d+1) - 1 in left-to-right order, so the expected spiral
  alternates each ascending range with its reverse; the test
  double-asserts that expectation against the depth-bucketed
  traversal oracle defined below.
- test_constructed_caterpillar_of_500_nodes_turns_at_every_level:
  250 spine nodes (values 0..249) linked by left edges, each carrying a
  right-leaf (value 250 + spine index), 500 nodes in all. Levels 1
  through 249 hold [spine_depth, 249 + spine_depth] left to right,
  level 250 holds the last leaf alone, so the tree reaches the
  statement's node bound with the direction turning 250 times.
"""

from typing import List, Optional

import pytest

from harness import TreeNode, build_tree, load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

PERFECT_TREE_DEPTH = 7
CATERPILLAR_SPINE_LENGTH = 250


def _ids(cases):
    return [case["id"] for case in cases]


def _spiral_by_depth_bucketed_dfs(root: Optional[TreeNode]) -> List[List[int]]:
    """Independent oracle: depth-bucketed preorder, alternate depths reversed.

    An explicit stack walks a left-first preorder and appends each value
    to its depth bucket; preorder meets every level left to right, and
    reversing the odd buckets reproduces the statement's alternating
    direction. Shares no mechanism with the reference's level-size BFS.
    """
    buckets: List[List[int]] = []
    stack = [(root, 0)] if root is not None else []
    while stack:
        node, depth = stack.pop()
        if depth == len(buckets):
            buckets.append([])
        buckets[depth].append(node.val)
        if node.right is not None:
            stack.append((node.right, depth + 1))
        if node.left is not None:
            stack.append((node.left, depth + 1))
    return [bucket[::-1] if depth % 2 else bucket for depth, bucket in enumerate(buckets)]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    got = reference.Solution().zigzagLevels(build_tree(case["args"][0]))
    assert got == case["expected"]


def test_constructed_perfect_tree_of_255_nodes_alternates_through_eight_levels():
    values = list(range(1, 2 ** (PERFECT_TREE_DEPTH + 1)))
    expected = []
    for depth in range(PERFECT_TREE_DEPTH + 1):
        level = list(range(2**depth, 2 ** (depth + 1)))
        expected.append(level[::-1] if depth % 2 else level)
    tree = build_tree(values)
    got = reference.Solution().zigzagLevels(tree)
    assert got == expected
    assert _spiral_by_depth_bucketed_dfs(tree) == expected


def test_constructed_caterpillar_of_500_nodes_turns_at_every_level():
    spine = [TreeNode(spine_value) for spine_value in range(CATERPILLAR_SPINE_LENGTH)]
    for index, spine_node in enumerate(spine):
        spine_node.right = TreeNode(CATERPILLAR_SPINE_LENGTH + index)
        if index + 1 < CATERPILLAR_SPINE_LENGTH:
            spine_node.left = spine[index + 1]
    expected = [[0]]
    for depth in range(1, CATERPILLAR_SPINE_LENGTH):
        level = [depth, CATERPILLAR_SPINE_LENGTH - 1 + depth]
        expected.append(level[::-1] if depth % 2 else level)
    expected.append([2 * CATERPILLAR_SPINE_LENGTH - 1])
    got = reference.Solution().zigzagLevels(spine[0])
    assert got == expected
