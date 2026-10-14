"""Tests for Cinema Shows — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-cinema-shows.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                10,
                5,
                15,
                18,
                30,
            ],
            [
                20,
                12,
                20,
                35,
                35,
            ],
            [
                50,
                51,
                20,
                25,
                10,
            ],
        ],
        "expected": 76,
    },
    {
        "id": 'example_2',
        "args": [
            [
                1,
                2,
                4,
            ],
            [
                2,
                2,
                1,
            ],
            [
                1,
                2,
                3,
            ],
        ],
        "expected": 4,
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
        _check(solution.Solution().cinemaShows, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
