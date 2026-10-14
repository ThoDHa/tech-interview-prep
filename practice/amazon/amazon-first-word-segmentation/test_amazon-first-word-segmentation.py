"""Tests for First Valid Word Segmentation — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-first-word-segmentation.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'myhousehavecat',
            [
                'my',
                'house',
                'have',
                'cat',
            ],
        ],
        "expected": [
            'my',
            'house',
            'have',
            'cat',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            'aaaa',
            [
                'a',
                'aa',
            ],
        ],
        "expected": [
            'a',
            'a',
            'a',
            'a',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            'catsanddog',
            [
                'cats',
                'dog',
                'sand',
                'and',
                'cat',
            ],
        ],
        "expected": [
            'cat',
            'sand',
            'dog',
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
        _check(solution.Solution().segmentWords, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
