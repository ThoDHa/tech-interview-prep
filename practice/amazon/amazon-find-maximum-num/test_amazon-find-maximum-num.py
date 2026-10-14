"""Tests for Find Max Num — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-find-maximum-num.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                24,
                27,
                0,
            ],
            [
                51,
                52,
                100,
            ],
            100,
        ],
        "expected": 2,
    },
    {
        "id": 'example_2',
        "args": [
            [
                24,
                27,
                0,
            ],
            [
                51,
                52,
                100,
            ],
            200,
        ],
        "expected": 3,
    },
    {
        "id": 'example_3',
        "args": [
            [
                2,
                4,
            ],
            [
                4,
                5,
            ],
            1,
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
        _check(solution.Solution().findMaximumNum, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
