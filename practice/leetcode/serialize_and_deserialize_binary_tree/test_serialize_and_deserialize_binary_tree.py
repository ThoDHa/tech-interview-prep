"""Tests for Serialize and Deserialize Binary Tree: your attempt (solution.py).

Each case stores a binary tree as a level-order array. The contract is a
round-trip: serialize the tree to a string, deserialize it back, and confirm the
restored tree matches the original array. cases.json (marker `simple`) is the
"Run" set; cases_full.json (marker `full`) is the "Submit" gauntlet. The worked
approaches live in ../../docs/problems/serialize_and_deserialize_binary_tree.md.
"""

import pytest

from harness import (
    NotSolved,
    build_tree,
    load_cases,
    load_solution,
    tree_to_list,
)

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(cls, case):
    arr = case["args"][0]
    codec = cls()
    restored = codec.deserialize(codec.serialize(build_tree(arr)))
    assert tree_to_list(restored) == case["expected"]


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Codec, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Codec, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
