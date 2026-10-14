"""Tests for Meeting Room Scheduler — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-meeting-room-scheduler.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            2,
            [
                [
                    0,
                    10,
                ],
                [
                    5,
                    7,
                ],
                [
                    10,
                    12,
                ],
                [
                    10,
                    15,
                ],
            ],
        ],
        "expected": [
            0,
            1,
            0,
            1,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            1,
            [
                [
                    1,
                    4,
                ],
                [
                    2,
                    3,
                ],
                [
                    4,
                    5,
                ],
            ],
        ],
        "expected": [
            0,
            -1,
            0,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            2,
            [
                [
                    1,
                    2,
                ],
                [
                    1,
                    2,
                ],
                [
                    1,
                    2,
                ],
            ],
        ],
        "expected": [
            0,
            1,
            -1,
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
        _check(solution.Solution().scheduleMeetings, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
