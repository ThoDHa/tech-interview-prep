"""Tests for Last Stone Weight — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/last_stone_weight.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                2,
                3,
                6,
                2,
                4,
            ],
        ],
        "expected": 1,
    },
    {
        "id": 'example_2',
        "args": [
            [
                1,
                2,
            ],
        ],
        "expected": 1,
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
        _check(solution.Solution().lastStoneWeight, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


FULL = CASES + load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().lastStoneWeight, case)
