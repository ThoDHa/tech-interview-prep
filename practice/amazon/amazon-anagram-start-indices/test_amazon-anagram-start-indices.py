"""Tests for All Anagram Start Indices — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-anagram-start-indices.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'acbadabcaa',
            'aabc',
        ],
        "expected": [
            0,
            5,
            6,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            'cbaebabacd',
            'abc',
        ],
        "expected": [
            0,
            6,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            'abab',
            'ab',
        ],
        "expected": [
            0,
            1,
            2,
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
        _check(solution.Solution().findAnagrams, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
