"""Tests for All About Medians — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-medians.md.
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
            ],
            2,
        ],
        "expected": [
            2,
            1,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                56,
                21,
            ],
            1,
        ],
        "expected": [
            56,
            21,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                16,
                21,
                9,
                2,
                78,
            ],
            5,
        ],
        "expected": [
            16,
            16,
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
        _check(solution.Solution().medians, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
