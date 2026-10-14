"""Tests for Maximum Profit in Job Scheduling — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-maximum-profit-job-scheduling.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                1,
                2,
                3,
                3,
            ],
            [
                3,
                4,
                5,
                6,
            ],
            [
                50,
                10,
                40,
                70,
            ],
        ],
        "expected": 120,
    },
    {
        "id": 'example_2',
        "args": [
            [
                1,
                2,
                3,
                4,
                6,
            ],
            [
                3,
                5,
                10,
                6,
                9,
            ],
            [
                20,
                20,
                100,
                70,
                60,
            ],
        ],
        "expected": 150,
    },
    {
        "id": 'example_3',
        "args": [
            [
                1,
                1,
                1,
            ],
            [
                2,
                3,
                4,
            ],
            [
                5,
                6,
                4,
            ],
        ],
        "expected": 6,
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
        _check(solution.Solution().jobScheduling, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
