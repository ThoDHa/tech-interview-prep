"""Tests for Nearby Fulfillment Centers with Inventory — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-nearby-fulfillment-centers.md.
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
                    1,
                    3,
                ],
                [
                    2,
                    4,
                ],
                [
                    3,
                    4,
                ],
                [
                    4,
                    5,
                ],
            ],
            4,
            1,
            [
                [
                    1,
                    2,
                ],
                [
                    2,
                    0,
                ],
                [
                    3,
                    5,
                ],
                [
                    4,
                    3,
                ],
                [
                    5,
                    6,
                ],
            ],
        ],
        "expected": [
            3,
            5,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    10,
                    20,
                ],
                [
                    20,
                    30,
                ],
                [
                    30,
                    40,
                ],
            ],
            20,
            2,
            [
                [
                    10,
                    1,
                ],
                [
                    20,
                    9,
                ],
                [
                    30,
                    0,
                ],
                [
                    40,
                    4,
                ],
                [
                    50,
                    8,
                ],
            ],
        ],
        "expected": [
            10,
            40,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                [
                    1,
                    2,
                ],
                [
                    2,
                    3,
                ],
            ],
            2,
            0,
            [
                [
                    1,
                    7,
                ],
                [
                    2,
                    5,
                ],
                [
                    3,
                    9,
                ],
            ],
        ],
        "expected": [],
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
        _check(solution.Solution().findFulfillmentCenters, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
