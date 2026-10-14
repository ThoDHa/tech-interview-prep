"""Tests for Minimum S3 Storage Cost — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-minimum-s3-storage-cost.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            2,
            2,
            1,
            [
                1,
                3,
            ],
        ],
        "expected": 6,
    },
    {
        "id": 'example_2',
        "args": [
            3,
            2,
            1,
            [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
            ],
        ],
        "expected": 16,
    },
    {
        "id": 'example_3',
        "args": [
            3,
            2,
            1,
            [
                7,
                1,
            ],
        ],
        "expected": 8,
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
        _check(solution.Solution().minStorageCost, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
