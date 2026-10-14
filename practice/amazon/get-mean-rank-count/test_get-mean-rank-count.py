"""Tests for Cet Mean Rank Count — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/get-mean-rank-count.md.
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
                4,
                5,
            ],
        ],
        "expected": [
            1,
            2,
            3,
            2,
            1,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                4,
                3,
                2,
                1,
            ],
        ],
        "expected": [
            1,
            2,
            2,
            1,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                4,
                7,
                3,
                6,
                5,
                2,
                1,
            ],
        ],
        "expected": [
            1,
            1,
            1,
            4,
            4,
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
        _check(solution.Solution().getMeanRankCount, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
