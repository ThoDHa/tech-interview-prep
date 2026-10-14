"""Tests for Loyal Customers Across Two Days — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-loyal-customers.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    '09:00',
                    'alice',
                    'home',
                ],
                [
                    '09:05',
                    'alice',
                    'search',
                ],
                [
                    '09:10',
                    'alice',
                    'checkout',
                ],
                [
                    '10:00',
                    'bob',
                    'home',
                ],
                [
                    '10:05',
                    'bob',
                    'search',
                ],
                [
                    '10:10',
                    'bob',
                    'checkout',
                ],
                [
                    '11:00',
                    'cara',
                    'home',
                ],
                [
                    '11:05',
                    'cara',
                    'search',
                ],
                [
                    '11:10',
                    'cara',
                    'checkout',
                ],
            ],
            [
                [
                    '09:00',
                    'alice',
                    'home',
                ],
                [
                    '09:05',
                    'alice',
                    'offers',
                ],
                [
                    '09:10',
                    'alice',
                    'checkout',
                ],
                [
                    '10:00',
                    'bob',
                    'home',
                ],
                [
                    '10:05',
                    'bob',
                    'search',
                ],
                [
                    '12:00',
                    'dan',
                    'home',
                ],
                [
                    '12:05',
                    'dan',
                    'search',
                ],
                [
                    '12:10',
                    'dan',
                    'checkout',
                ],
            ],
        ],
        "expected": [
            'alice',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    '1',
                    'cust-b',
                    'p1',
                ],
                [
                    '2',
                    'cust-b',
                    'p2',
                ],
                [
                    '3',
                    'cust-b',
                    'p3',
                ],
                [
                    '4',
                    'cust-a',
                    'p1',
                ],
                [
                    '5',
                    'cust-a',
                    'p2',
                ],
                [
                    '6',
                    'cust-a',
                    'p3',
                ],
            ],
            [
                [
                    '7',
                    'cust-a',
                    'p4',
                ],
                [
                    '8',
                    'cust-a',
                    'p5',
                ],
                [
                    '9',
                    'cust-a',
                    'p6',
                ],
                [
                    '10',
                    'cust-b',
                    'p4',
                ],
                [
                    '11',
                    'cust-b',
                    'p5',
                ],
                [
                    '12',
                    'cust-b',
                    'p6',
                ],
            ],
        ],
        "expected": [
            'cust-a',
            'cust-b',
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
        _check(solution.Solution().findLoyalCustomers, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
