"""Tests for Word Search II — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-word-search-ii.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    'o',
                    'a',
                    'a',
                    'n',
                ],
                [
                    'e',
                    't',
                    'a',
                    'e',
                ],
                [
                    'i',
                    'h',
                    'k',
                    'r',
                ],
                [
                    'i',
                    'f',
                    'l',
                    'v',
                ],
            ],
            [
                'oath',
                'pea',
                'eat',
                'rain',
            ],
        ],
        "expected": [
            'oath',
            'eat',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    'a',
                    'b',
                ],
                [
                    'c',
                    'd',
                ],
            ],
            [
                'abcb',
                'abcd',
                'acdb',
            ],
        ],
        "expected": [
            'acdb',
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
        _check(solution.Solution().findWords, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
