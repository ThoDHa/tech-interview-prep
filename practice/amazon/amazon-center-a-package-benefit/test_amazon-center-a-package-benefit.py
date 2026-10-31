"""Tests for Maximize Center A Package Benefit — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-center-a-package-benefit.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                8,
                3,
                7,
                4,
            ],
            [
                1,
                9,
                2,
                6,
            ],
            [
                [
                    0,
                    1,
                ],
            ],
        ],
        "expected": 12,
    },
    {
        "id": 'example_2',
        "args": [
            [
                5,
                2,
                9,
            ],
            [
                4,
                8,
                1,
            ],
            [],
        ],
        "expected": 7,
    },
    {
        "id": 'example_3',
        "args": [
            [
                10,
                4,
                6,
                12,
            ],
            [
                2,
                8,
                7,
                1,
            ],
            [
                [
                    0,
                    1,
                ],
                [
                    2,
                    3,
                ],
            ],
        ],
        "expected": 22,
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
        _check(solution.Solution().maximizeCenterABenefit, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
