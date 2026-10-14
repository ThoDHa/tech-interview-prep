"""Tests for Dropped Requests — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-dropped-requests.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                1,
                1,
                1,
                1,
                2,
            ],
        ],
        "expected": 1,
    },
    {
        "id": 'example_2',
        "args": [
            [
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                3,
                3,
                3,
                4,
                4,
                4,
                5,
                5,
                5,
                6,
                6,
                6,
                7,
                7,
            ],
        ],
        "expected": 2,
    },
    {
        "id": 'example_3',
        "args": [
            [
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                3,
                3,
                3,
                4,
                4,
                4,
                5,
                5,
                5,
                6,
                6,
                6,
                7,
                7,
                7,
                7,
                11,
                11,
                11,
                11,
            ],
        ],
        "expected": 7,
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
        _check(solution.Solution().droppedRequests, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
