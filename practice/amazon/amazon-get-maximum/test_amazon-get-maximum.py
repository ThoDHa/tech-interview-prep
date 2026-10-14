"""Tests for Get Maximum — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-get-maximum.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                7,
                4,
                5,
                2,
                6,
                5,
            ],
        ],
        "expected": 12,
    },
    {
        "id": 'example_2',
        "args": [
            [
                2,
                9,
                4,
                7,
                5,
                2,
            ],
        ],
        "expected": 16,
    },
    {
        "id": 'example_3',
        "args": [
            [
                2,
                5,
                6,
                7,
            ],
        ],
        "expected": 20,
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
        _check(solution.Solution().getMaximum, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
