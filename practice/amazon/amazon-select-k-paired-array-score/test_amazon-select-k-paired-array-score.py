"""Tests for Select K Paired Indices for Maximum Score — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-select-k-paired-array-score.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                1,
                3,
                3,
                2,
            ],
            [
                2,
                1,
                3,
                4,
            ],
            3,
        ],
        "expected": 12,
    },
    {
        "id": 'example_2',
        "args": [
            [
                4,
                2,
                3,
                1,
                1,
            ],
            [
                7,
                5,
                10,
                9,
                6,
            ],
            1,
        ],
        "expected": 30,
    },
    {
        "id": 'example_3',
        "args": [
            [
                2,
                1,
                14,
                12,
            ],
            [
                11,
                7,
                13,
                6,
            ],
            3,
        ],
        "expected": 168,
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
        _check(solution.Solution().maximumPairedScore, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
