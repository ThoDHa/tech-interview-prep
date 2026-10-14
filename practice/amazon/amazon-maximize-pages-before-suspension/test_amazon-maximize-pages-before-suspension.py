"""Tests for Maximize Pages Before Suspension — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-maximize-pages-before-suspension.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                4,
                1,
                5,
                2,
                3,
            ],
            [
                3,
                3,
                2,
                3,
                3,
            ],
        ],
        "expected": 14,
    },
    {
        "id": 'example_2',
        "args": [
            [
                2,
                4,
                4,
                4,
                5,
                3,
            ],
            [
                1,
                3,
                1,
                3,
                3,
                2,
            ],
        ],
        "expected": 20,
    },
    {
        "id": 'example_3',
        "args": [
            [
                2,
                6,
                10,
                13,
            ],
            [
                2,
                1,
                1,
                1,
            ],
        ],
        "expected": 15,
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
        _check(solution.Solution().getMaxPages, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
