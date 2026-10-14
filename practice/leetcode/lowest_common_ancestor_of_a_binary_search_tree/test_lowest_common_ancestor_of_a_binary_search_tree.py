"""Tests for Lowest Common Ancestor of a BST: your attempt (solution.py) against both sets.

Trees are stored in the case files as level-order value arrays plus the integer
values of `p` and `q`; both are marshalled to TreeNodes here. The worked approaches
live in ../../docs/problems/lowest_common_ancestor_of_a_binary_search_tree.md.
"""

import pytest

from harness import (
    NotSolved,
    build_tree,
    find_tree_node,
    load_cases,
    load_solution,
)

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    tree_array, p_val, q_val = case["args"]
    root = build_tree(tree_array)
    p_node = find_tree_node(root, p_val)
    q_node = find_tree_node(root, q_val)
    result = method(root, p_node, q_node)
    assert result.val == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().lowestCommonAncestor, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().lowestCommonAncestor, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
