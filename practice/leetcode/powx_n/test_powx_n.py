"""Tests for Pow(x, n) — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/powx_n.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            2.0,
            5,
        ],
        "expected": 32.0,
    },
    {
        "id": 'example_2',
        "args": [
            1.1,
            10,
        ],
        "expected": 2.59374,
    },
    {
        "id": 'example_3',
        "args": [
            2.0,
            -3,
        ],
        "expected": 0.125,
    },
]

if len(CASES) == 0:
    pytest.skip("no cases parsed", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().myPow, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
