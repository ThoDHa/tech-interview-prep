"""Tests for Grouped-Query Attention with a KV Cache — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-grouped-query-attention-with-kv-cache.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    1,
                ],
            ],
            [],
            [],
            [
                [
                    0,
                ],
                [
                    1,
                ],
            ],
            [
                [
                    10,
                ],
                [
                    20,
                ],
            ],
            1,
            1,
        ],
        "expected": [
            '17.310586',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [
                    1,
                    0,
                ],
            ],
            [
                [
                    1,
                ],
            ],
            [
                [
                    4,
                ],
            ],
            [
                [
                    0,
                ],
            ],
            [
                [
                    8,
                ],
            ],
            2,
            1,
        ],
        "expected": [
            '5.075766,6.000000',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            [
                [
                    1,
                    0,
                ],
                [
                    0,
                    1,
                ],
            ],
            [
                [
                    1,
                    0,
                ],
            ],
            [
                [
                    10,
                    20,
                ],
            ],
            [
                [
                    0,
                    1,
                ],
            ],
            [
                [
                    30,
                    40,
                ],
            ],
            2,
            2,
        ],
        "expected": [
            '15.378828,30.000000',
            '20.000000,34.621172',
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
        _check(solution.Solution().groupedQueryAttentionWithCache, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
