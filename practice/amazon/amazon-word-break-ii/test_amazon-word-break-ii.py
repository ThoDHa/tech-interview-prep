"""Tests for Word Break II — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-word-break-ii.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'catsanddog',
            [
                'cat',
                'cats',
                'and',
                'sand',
                'dog',
            ],
        ],
        "expected": [
            'cat sand dog',
            'cats and dog',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            'pineapplepenapple',
            [
                'apple',
                'pen',
                'applepen',
                'pine',
                'pineapple',
            ],
        ],
        "expected": [
            'pine apple pen apple',
            'pine applepen apple',
            'pineapple pen apple',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            'catsandog',
            [
                'cats',
                'dog',
                'sand',
                'and',
                'cat',
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
        _check(solution.Solution().wordBreak, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
