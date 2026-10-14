"""Tests for About Mortgage — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-maximum-number-of-days-to-survive.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                4,
                6,
                1,
                8,
            ],
            [
                7,
                10,
                3,
                9,
            ],
        ],
        "expected": 3,
    },
    {
        "id": 'example_2',
        "args": [
            [
                2,
                1,
                5,
            ],
            [
                2,
                2,
                5,
            ],
        ],
        "expected": 3,
    },
    {
        "id": 'example_3',
        "args": [
            [
                1,
                1,
                1,
                2,
            ],
            [
                2,
                2,
                2,
                3,
            ],
        ],
        "expected": 2,
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
        _check(solution.Solution().maximumNumberOfDaysToSurvive, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
