"""Tests for Most Frequent Consecutive Website Pattern — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-consecutive-website-visit-pattern.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                'amy',
                'amy',
                'amy',
                'ben',
                'ben',
                'ben',
            ],
            [
                1,
                2,
                3,
                1,
                2,
                3,
            ],
            [
                'home',
                'cart',
                'pay',
                'home',
                'cart',
                'pay',
            ],
        ],
        "expected": [
            'home',
            'cart',
            'pay',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                'a',
                'a',
                'a',
                'b',
                'b',
                'b',
            ],
            [
                3,
                1,
                2,
                1,
                2,
                3,
            ],
            [
                'z',
                'a',
                'z',
                'a',
                'z',
                'z',
            ],
        ],
        "expected": [
            'a',
            'z',
            'z',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                'a',
                'a',
                'b',
            ],
            [
                1,
                2,
                1,
            ],
            [
                'x',
                'y',
                'z',
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
        _check(solution.Solution().mostFrequentConsecutivePattern, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
