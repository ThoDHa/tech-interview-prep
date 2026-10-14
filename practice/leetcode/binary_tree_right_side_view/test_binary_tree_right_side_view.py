"""Tests for Binary Tree Right Side View: your attempt (solution.py) against both sets.

Trees are stored in the case files as LeetCode level-order arrays (null = missing)
and marshalled to TreeNode here. The worked approaches live in
../../docs/problems/binary_tree_right_side_view.md.
"""

import pytest

from harness import (
    NotSolved,
    build_tree,
    load_cases,
    load_solution,
)

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
        _check(solution.Solution().rightSideView, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().rightSideView, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
