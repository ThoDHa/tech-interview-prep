"""Tests for Page Referrer Reachability — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-page-referrer-reachability.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    '/catalog',
                    '/home',
                ],
                [
                    '/item/7',
                    '/catalog',
                ],
                [
                    '/cart',
                    '/item/7',
                ],
            ],
            [
                '/home',
                '/cart',
            ],
        ],
        "expected": True,
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    '/pricing',
                    '/home',
                ],
                [
                    '/signup',
                    '/pricing',
                ],
            ],
            [
                '/pricing',
                '/home',
            ],
        ],
        "expected": False,
    },
    {
        "id": 'example_3',
        "args": [
            [
                [
                    '/landing',
                    '',
                ],
                [
                    '/account',
                    '/landing',
                ],
            ],
            [
                '/account',
                '/account',
            ],
        ],
        "expected": True,
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
        _check(solution.Solution().canReachPage, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
