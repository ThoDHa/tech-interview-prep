"""Tests for Get Active Requests Count — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-get-active-requests-count.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            6,
            [
                5,
                2,
                2,
                4,
                7,
                1,
            ],
        ],
        "expected": [
            6,
            4,
            2,
            2,
            1,
            0,
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
        _check(solution.Solution().getActiveRequestsCount, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
