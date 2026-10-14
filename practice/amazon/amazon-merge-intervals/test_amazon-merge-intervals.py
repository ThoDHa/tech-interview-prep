"""Tests for Merge Intervals — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-merge-intervals.md.
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
                    3,
                ],
                [
                    2,
                    6,
                ],
                [
                    8,
                    10,
                ],
                [
                    15,
                    18,
                ],
            ],
        ],
        "expected": [
            [
                1,
                6,
            ],
            [
                8,
                10,
            ],
            [
                15,
                18,
            ],
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    1,
                    4,
                ],
                [
                    4,
                    5,
                ],
            ],
        ],
        "expected": [
            [
                1,
                5,
            ],
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                [
                    8,
                    10,
                ],
                [
                    1,
                    4,
                ],
                [
                    2,
                    3,
                ],
                [
                    15,
                    18,
                ],
                [
                    6,
                    9,
                ],
                [
                    3,
                    7,
                ],
                [
                    17,
                    20,
                ],
                [
                    12,
                    12,
                ],
            ],
        ],
        "expected": [
            [
                1,
                10,
            ],
            [
                12,
                12,
            ],
            [
                15,
                20,
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
        _check(solution.Solution().merge, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
