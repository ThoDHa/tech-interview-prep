"""Tests for Get Total Requests — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-get-total-requests.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                20,
                10,
            ],
            [
                10,
                20,
            ],
            [
                20,
                1,
            ],
        ],
        "expected": [
            40,
            2,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                3,
                3,
            ],
            [
                3,
                1,
            ],
            [
                1,
                5,
            ],
        ],
        "expected": [
            2,
            10,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                2,
                5,
                2,
            ],
            [
                2,
                5,
                3,
            ],
            [
                3,
                1,
                5,
            ],
        ],
        "expected": [
            11,
            7,
            11,
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
        _check(solution.Solution().getTotalRequests, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
