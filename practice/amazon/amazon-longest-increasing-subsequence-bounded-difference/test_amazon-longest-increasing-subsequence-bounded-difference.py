"""Tests for Longest Increasing Subsequence With Bounded Adjacent Difference — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-longest-increasing-subsequence-bounded-difference.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                7,
                1,
                4,
                5,
                8,
                8,
                10,
                6,
                7,
                7,
                7,
                8,
            ],
            4,
        ],
        "expected": 6,
    },
    {
        "id": 'example_2',
        "args": [
            [
                3,
                1,
                2,
                6,
                10,
                11,
                4,
                5,
            ],
            3,
        ],
        "expected": 4,
    },
    {
        "id": 'example_3',
        "args": [
            [
                5,
                4,
                3,
                2,
                1,
            ],
            2,
        ],
        "expected": 1,
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
        _check(solution.Solution().longestBoundedIncreasingSubsequence, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
