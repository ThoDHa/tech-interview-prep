"""Tests for Longest Common Subsequence Length — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-longest-common-subsequence-length.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'abcde',
            'ace',
        ],
        "expected": 3,
    },
    {
        "id": 'example_2',
        "args": [
            'abc',
            'def',
        ],
        "expected": 0,
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
        _check(solution.Solution().longestCommonSubsequence, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
