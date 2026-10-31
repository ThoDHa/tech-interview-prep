"""Tests for 0/1 Knapsack — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-zero-one-knapsack.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                1,
                3,
                4,
                5,
            ],
            [
                1,
                4,
                5,
                7,
            ],
            7,
        ],
        "expected": 9,
    },
    {
        "id": 'example_2',
        "args": [
            [
                2,
                2,
                3,
            ],
            [
                6,
                10,
                12,
            ],
            5,
        ],
        "expected": 22,
    },
    {
        "id": 'example_3',
        "args": [
            [
                4,
                5,
            ],
            [
                8,
                9,
            ],
            3,
        ],
        "expected": 0,
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
        _check(solution.Solution().maximumKnapsackValue, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
