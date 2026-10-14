"""Tests for Environment Variable Store and Substitution — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-environment-variable-substitution.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = []

if len(CASES) == 0:
    pytest.skip("design-operation example for amazon-environment-variable-substitution is not `==`-assertable", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().processEnvironment, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
