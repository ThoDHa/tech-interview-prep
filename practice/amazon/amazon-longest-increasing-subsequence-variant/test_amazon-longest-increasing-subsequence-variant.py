"""Tests for Longest Increasing Subsequence — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-longest-increasing-subsequence-variant.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                10,
                9,
                2,
                5,
                3,
                7,
                101,
                18,
            ],
        ],
        "expected": 4,
    },
    {
        "id": 'example_2',
        "args": [
            [
                0,
                1,
                0,
                3,
                2,
                3,
            ],
        ],
        "expected": 4,
    },
    {
        "id": 'example_3',
        "args": [
            [
                7,
                7,
                7,
                7,
                7,
                7,
                7,
            ],
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
        _check(solution.Solution().lengthOfLIS, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
