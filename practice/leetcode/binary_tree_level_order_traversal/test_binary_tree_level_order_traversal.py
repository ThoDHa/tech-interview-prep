"""Tests for Binary Tree Level Order Traversal: your attempt (solution.py).

Trees are stored in the case files as LeetCode level-order arrays (null = missing
node) and marshalled to TreeNode here. cases.json (marker `simple`) is the "Run"
set; cases_full.json (marker `full`) is the "Submit" gauntlet. The worked
approaches live in ../../docs/problems/binary_tree_level_order_traversal.md.
"""

import pytest

from harness import NotSolved, build_tree, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    root = build_tree(case["args"][0])
    result = method(root)
    assert result == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().levelOrder, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().levelOrder, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
