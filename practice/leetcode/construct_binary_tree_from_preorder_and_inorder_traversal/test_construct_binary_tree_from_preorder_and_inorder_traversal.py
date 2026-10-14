"""Tests for Construct Binary Tree from Preorder and Inorder Traversal: your
attempt (solution.py) against both case sets.

Trees are stored in the case files as preorder/inorder value arrays (inputs) and a
LeetCode level-order array (expected output), marshalled with tree_to_list here.
The worked approaches live in
../../docs/problems/construct_binary_tree_from_preorder_and_inorder_traversal.md.
"""

import pytest

from harness import (
    NotSolved,
    load_cases,
    load_solution,
    tree_to_list,
)

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    preorder, inorder = case["args"]
    result = method(preorder, inorder)
    assert tree_to_list(result) == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().buildTree, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().buildTree, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
