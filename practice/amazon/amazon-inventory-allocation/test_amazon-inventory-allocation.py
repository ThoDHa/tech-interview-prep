"""Tests for Inventory Allocation — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-inventory-allocation.md.
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
                    5,
                    5,
                    0,
                ],
                [
                    2,
                    7,
                    8,
                    1,
                ],
                [
                    3,
                    7,
                    5,
                    1,
                ],
                [
                    4,
                    10,
                    3,
                    3,
                ],
            ],
            18,
        ],
        "expected": [
            4,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    1,
                    2,
                    10,
                    0,
                ],
                [
                    2,
                    3,
                    10,
                    1,
                ],
                [
                    3,
                    1,
                    5,
                    0,
                ],
            ],
            3,
        ],
        "expected": [
            3,
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
        _check(solution.Solution().getUnfulfilledCustomers, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
