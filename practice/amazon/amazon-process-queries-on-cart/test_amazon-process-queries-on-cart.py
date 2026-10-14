"""Tests for Process Queries On Cart — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-process-queries-on-cart.md.
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
                1,
                2,
                1,
            ],
            [
                -1,
                -1,
                3,
                4,
                -3,
            ],
        ],
        "expected": [
            2,
            2,
            1,
            4,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                5,
                1,
                2,
                2,
                4,
                6,
            ],
            [
                1,
                -2,
                -1,
                -1,
            ],
        ],
        "expected": [
            5,
            2,
            4,
            6,
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
        _check(solution.Solution().processQueriesOnCart, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
