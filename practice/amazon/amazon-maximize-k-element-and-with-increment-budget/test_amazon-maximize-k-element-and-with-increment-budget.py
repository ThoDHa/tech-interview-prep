"""Tests for Maximize K-Element AND with an Increment Budget — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-maximize-k-element-and-with-increment-budget.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                5,
                4,
                1,
                7,
                2,
            ],
            3,
            3,
        ],
        "expected": 6,
    },
    {
        "id": 'example_2',
        "args": [
            [
                1,
                2,
                3,
            ],
            2,
            0,
        ],
        "expected": 2,
    },
    {
        "id": 'example_3',
        "args": [
            [
                0,
                0,
            ],
            2,
            2,
        ],
        "expected": 1,
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
        _check(solution.Solution().maximizeAnd, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
