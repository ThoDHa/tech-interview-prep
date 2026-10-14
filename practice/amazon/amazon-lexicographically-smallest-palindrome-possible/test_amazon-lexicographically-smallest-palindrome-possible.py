"""Tests for Lexicographically Smallest Palindrome Possible — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-lexicographically-smallest-palindrome-possible.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'a?rt???',
        ],
        "expected": 'aartraa',
    },
    {
        "id": 'example_2',
        "args": [
            'bx??tm',
        ],
        "expected": '-1',
    },
    {
        "id": 'example_3',
        "args": [
            'ai?a??u',
        ],
        "expected": 'aaiuiaa',
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
        _check(solution.Solution().getSmallestPalindrome, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
