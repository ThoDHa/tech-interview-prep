"""Tests for Get Success Value — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/get-success-value.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                2,
                5,
                6,
                3,
                5,
            ],
            [
                2,
                3,
                5,
            ],
        ],
        "expected": [
            11,
            16,
            21,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                7,
                3,
                5,
                2,
            ],
            [
                1,
                4,
            ],
        ],
        "expected": [
            7,
            17,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                7,
                5,
                6,
            ],
            [
                1,
                2,
                3,
            ],
        ],
        "expected": [
            7,
            13,
            18,
        ],
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
        _check(solution.Solution().findSuccessValue, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
