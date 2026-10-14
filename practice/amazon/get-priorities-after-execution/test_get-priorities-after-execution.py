"""Tests for Get Priorities After Execution — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/get-priorities-after-execution.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                6,
                6,
                6,
                1,
                2,
                2,
            ],
        ],
        "expected": [
            3,
            6,
            0,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                4,
                4,
                2,
                1,
            ],
        ],
        "expected": [
            0,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                2,
                1,
                5,
                10,
                10,
                1,
            ],
        ],
        "expected": [
            0,
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
        _check(solution.Solution().getPrioritiesAfterExecution, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
