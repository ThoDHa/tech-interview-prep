"""Tests for Get Redundant Substrings — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-get-redundant-substrings.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'abbacc',
            -1,
            2,
        ],
        "expected": 5,
    },
    {
        "id": 'example_2',
        "args": [
            'akljfs',
            -2,
            1,
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
        _check(solution.Solution().getRedundantSubstrings, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
