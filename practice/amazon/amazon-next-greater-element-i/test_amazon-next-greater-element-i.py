"""Tests for Next Greater Element I — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-next-greater-element-i.md.
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
                2,
            ],
            [
                1,
                3,
                4,
                2,
            ],
        ],
        "expected": [
            -1,
            3,
            -1,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                2,
                4,
            ],
            [
                1,
                2,
                3,
                4,
            ],
        ],
        "expected": [
            3,
            -1,
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
        _check(solution.Solution().nextGreaterElement, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
