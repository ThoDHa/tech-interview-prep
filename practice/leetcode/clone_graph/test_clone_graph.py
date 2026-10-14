"""Tests for Clone Graph: your attempt (solution.py) against both case sets.

Graphs are stored in the case files as LeetCode adjacency lists (1-indexed) and
marshalled to GraphNode here. The cloned graph is serialized back to an adjacency
list for comparison. The worked approaches live in ../../docs/problems/clone_graph.md.
"""

import pytest

from harness import (
    NotSolved,
    build_graph,
    graph_to_adjacency,
    load_cases,
    load_solution,
)

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    adj = case["args"][0]
    result = method(build_graph(adj))
    assert graph_to_adjacency(result) == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().cloneGraph, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().cloneGraph, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
