"""Tests for Evaluate Division — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-evaluate-division.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    'a',
                    'b',
                ],
                [
                    'b',
                    'c',
                ],
            ],
            [
                2.0,
                3.0,
            ],
            [
                [
                    'a',
                    'c',
                ],
                [
                    'b',
                    'a',
                ],
                [
                    'a',
                    'e',
                ],
                [
                    'a',
                    'a',
                ],
                [
                    'x',
                    'x',
                ],
            ],
        ],
        "expected": [
            6.0,
            0.5,
            -1.0,
            1.0,
            -1.0,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    'a',
                    'b',
                ],
                [
                    'b',
                    'c',
                ],
                [
                    'bc',
                    'cd',
                ],
            ],
            [
                1.5,
                2.5,
                5.0,
            ],
            [
                [
                    'a',
                    'c',
                ],
                [
                    'c',
                    'b',
                ],
                [
                    'bc',
                    'cd',
                ],
                [
                    'cd',
                    'bc',
                ],
            ],
        ],
        "expected": [
            3.75,
            0.4,
            5.0,
            0.2,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                [
                    'a',
                    'b',
                ],
            ],
            [
                0.5,
            ],
            [
                [
                    'a',
                    'b',
                ],
                [
                    'b',
                    'a',
                ],
                [
                    'a',
                    'c',
                ],
                [
                    'x',
                    'y',
                ],
            ],
        ],
        "expected": [
            0.5,
            2.0,
            -1.0,
            -1.0,
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
        _check(solution.Solution().calcEquation, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
