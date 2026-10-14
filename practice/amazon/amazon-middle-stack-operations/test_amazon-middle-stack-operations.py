"""Tests for Stack with Constant-Time Middle Queries — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-middle-stack-operations.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = []

if len(CASES) == 0:
    pytest.skip("design-operation example for amazon-middle-stack-operations is not `==`-assertable", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().processMiddleStack, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
