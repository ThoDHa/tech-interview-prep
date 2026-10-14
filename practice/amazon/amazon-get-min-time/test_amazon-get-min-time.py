"""Tests for Get Min Time — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-get-min-time.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            8,
            [
                2,
                6,
                8,
            ],
        ],
        "expected": 4,
    },
    {
        "id": 'example_2',
        "args": [
            5,
            [
                1,
                5,
            ],
        ],
        "expected": 1,
    },
    {
        "id": 'example_3',
        "args": [
            10,
            [
                4,
                6,
                2,
                9,
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
        _check(solution.Solution().getMinTime, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
