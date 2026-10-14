"""Tests for Set Matrix Zeroes — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/set_matrix_zeroes.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = []

if len(CASES) == 0:
    pytest.skip("in-place mutation return is not `==`-assertable for set_matrix_zeroes", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().solve, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
