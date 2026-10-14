"""Tests for Word Break — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-word-break.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'leetcode',
            [
                'leet',
                'code',
            ],
        ],
        "expected": True,
    },
    {
        "id": 'example_2',
        "args": [
            'applepenapple',
            [
                'apple',
                'pen',
            ],
        ],
        "expected": True,
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
        "expected": False,
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
