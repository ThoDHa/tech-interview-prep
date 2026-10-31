"""Tests for Binary Tree Cameras — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-binary-tree-cameras.md.
"""

import pytest

from harness import NotSolved, build_tree, load_cases, load_solution

CASES = load_cases(__file__, "cases.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(build_tree(case["args"][0])) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().minCameraCover, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
