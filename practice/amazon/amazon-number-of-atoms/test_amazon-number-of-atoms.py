"""Tests for Number of Atoms — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-number-of-atoms.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'H2O',
        ],
        "expected": 'H2O',
    },
    {
        "id": 'example_2',
        "args": [
            'Mg(OH)2',
        ],
        "expected": 'H2MgO2',
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
        _check(solution.Solution().countOfAtoms, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
