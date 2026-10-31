"""Tests for Binary Tree Spiral Level Order — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-binary-tree-spiral-level-order.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = []

if len(CASES) == 0:
    pytest.skip("example input 'root' for amazon-binary-tree-spiral-level-order is not JSON-representable", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().zigzagLevels, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
