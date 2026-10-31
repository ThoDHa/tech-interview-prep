"""Tests for Construct a Tree from Level-Order and Inorder Traversals — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-construct-tree-level-inorder.md.
"""

import pytest

from harness import NotSolved, tree_to_list, load_cases, load_solution

CASES = load_cases(__file__, "cases.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert tree_to_list(method(list(case["args"][0]), list(case["args"][1]))) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().buildTree, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
