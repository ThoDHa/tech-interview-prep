"""Tests for E-commerce Notification Router — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-ecommerce-notification-router.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                'EMAIL',
                'SMS',
                'PUSH',
            ],
            [
                'NORMAL',
                'URGENT',
                'NORMAL',
            ],
        ],
        "expected": [
            [
                'EMAIL',
            ],
            [
                'EMAIL',
                'SMS',
                'PUSH',
            ],
            [
                'PUSH',
            ],
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                'PUSH',
            ],
            [
                'URGENT',
            ],
        ],
        "expected": [
            [
                'EMAIL',
                'SMS',
                'PUSH',
            ],
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                'SMS',
                'EMAIL',
            ],
            [
                'NORMAL',
                'NORMAL',
            ],
        ],
        "expected": [
            [
                'SMS',
            ],
            [
                'EMAIL',
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
        _check(solution.Solution().routeNotifications, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
