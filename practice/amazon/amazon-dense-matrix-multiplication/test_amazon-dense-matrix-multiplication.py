"""Tests for Dense Matrix Multiplication — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-dense-matrix-multiplication.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    1,
                    2,
                ],
                [
                    3,
                    4,
                ],
            ],
            [
                [
                    5,
                    6,
                ],
                [
                    7,
                    8,
                ],
            ],
        ],
        "expected": [
            [
                19,
                22,
            ],
            [
                43,
                50,
            ],
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    2,
                ],
                [
                    3,
                ],
            ],
            [
                [
                    4,
                    5,
                    6,
                ],
            ],
        ],
        "expected": [
            [
                8,
                10,
                12,
            ],
            [
                12,
                15,
                18,
            ],
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                [
                    1,
                    0,
                    -2,
                ],
            ],
            [
                [
                    3,
                ],
                [
                    4,
                ],
                [
                    5,
                ],
            ],
        ],
        "expected": [
            [
                -7,
            ],
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
        _check(solution.Solution().multiplyMatrices, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
