"""Tests for Implement Trie (Prefix Tree): your attempt (solution.py).

Each case is a LeetCode design-operation sequence: an `operations` list (first
entry is the constructor), an `arguments` list aligned with it, and the
`expected` results. `run_operations` drives the Trie class and the results are
compared against `expected`. The worked approaches live in
../../docs/problems/implement_trie_prefix_tree.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution, run_operations

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(cls, case):
    result = run_operations(cls, case["operations"], case["arguments"])
    assert result == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Trie, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Trie, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
