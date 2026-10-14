"""Tests for Currency Conversion Rate — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-currency-conversion-rate.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    'USD',
                    'JPY',
                    '110',
                ],
                [
                    'USD',
                    'AUD',
                    '1.45',
                ],
                [
                    'JPY',
                    'GBP',
                    '0.0070',
                ],
            ],
            [
                'GBP',
                'AUD',
            ],
        ],
        "expected": '1.88',
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    'USD',
                    'CAD',
                    '1.30',
                ],
                [
                    'CAD',
                    'EUR',
                    '0.70',
                ],
            ],
            [
                'USD',
                'EUR',
            ],
        ],
        "expected": '0.91',
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
        _check(solution.Solution().findConversionRate, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
