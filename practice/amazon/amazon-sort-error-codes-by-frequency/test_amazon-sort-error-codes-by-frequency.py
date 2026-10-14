"""Tests for Sort Error Codes by Frequency — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-sort-error-codes-by-frequency.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                4,
                5,
                6,
                5,
                4,
                3,
            ],
        ],
        "expected": [
            3,
            6,
            4,
            4,
            5,
            5,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                2,
                2,
                1,
                1,
                1,
                3,
            ],
        ],
        "expected": [
            3,
            2,
            2,
            1,
            1,
            1,
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
        _check(solution.Solution().sortErrorCodesByFrequency, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
