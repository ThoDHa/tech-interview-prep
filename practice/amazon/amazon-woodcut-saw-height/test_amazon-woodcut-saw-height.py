"""Tests for Maximum Saw Height for At Least M Cut Length — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-woodcut-saw-height.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                20,
                15,
                10,
                17,
            ],
            7,
        ],
        "expected": 15,
    },
    {
        "id": 'example_2',
        "args": [
            [
                4,
                42,
                40,
                26,
                46,
            ],
            20,
        ],
        "expected": 36,
    },
    {
        "id": 'example_3',
        "args": [
            [
                5,
            ],
            5,
        ],
        "expected": 0,
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
        _check(solution.Solution().maxSawHeight, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
