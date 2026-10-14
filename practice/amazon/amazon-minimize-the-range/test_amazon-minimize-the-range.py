"""Tests for Fortune Telling — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-minimize-the-range.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            5,
            2,
            [
                1,
                2,
                17,
                16,
                9,
            ],
            [
                3,
                4,
                5,
                6,
                11,
            ],
        ],
        "expected": 8,
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
        _check(solution.Solution().minimizeTheRange, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
