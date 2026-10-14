"""Tests for Domain Weight Calculation — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-domain-weight-calculation.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                'com 20',
                'domain.com 10',
                'mail.domain.com 5',
                'test.com 10',
                'user.test.com 30',
                'contact.user.test.com -5',
            ],
        ],
        "expected": [
            'contact.user.test.com=55',
            'mail.domain.com=35',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                'com 5',
                'a.com 2',
                'b.com 3',
            ],
        ],
        "expected": [
            'a.com=7',
            'b.com=8',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                'api.shop.com 4',
                'shop.com -2',
                'com 1',
                'cdn.shop.com 7',
                'img.cdn.shop.com 3',
            ],
        ],
        "expected": [
            'api.shop.com=3',
            'img.cdn.shop.com=9',
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
        _check(solution.Solution().calculateDomainScores, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
