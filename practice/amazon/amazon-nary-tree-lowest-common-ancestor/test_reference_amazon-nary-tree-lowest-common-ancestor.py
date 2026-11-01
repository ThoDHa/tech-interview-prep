"""Reference-parametrized gauntlet for N-ary Tree Lowest Common Ancestor.

Every expectation in cases_full.json is oracle-derived, never
hand-computed and never recorded from this reference: the oracle
rebuilds children adjacency from the parent array, walks an explicit
DFS from the root recording the full path to each query node, and
returns the last shared path entry, which shares no mechanism with the
reference's leaf-up climbs. The output is a single deterministic label,
so the comparison is plain `==` with no canonicalization. A node counts
as its own ancestor, so the band includes equal queries and
ancestor-of-query cases alongside siblings, cousins, wide fan-outs,
unbalanced branches, deep chains, and a seeded random band of 30
shuffled-label trees; every serialized parent array stays within the
eye-auditable bound. The statement's 200000-node length corner stays
out of the JSON and is constructed here, where its expectation follows
from the construction:

- test_constructed_chain_of_200000_nodes_meets_at_the_higher_spine_node:
  a pure chain parent[i] = i - 1 rooted at 0. Every node's ancestor
  chain is its label's prefix, so the deepest shared prefix of two
  labels is their minimum; the test queries both extremes and a
  near-tip pair against that derivation.
- test_constructed_comb_of_200000_nodes_meets_on_the_shared_spine: a
  100000-node spine (labels 0..99999) with one leaf per spine node
  (label 100000 + spine index). Every leaf's ancestor chain is its
  spine index's chain plus itself, so any pair's lowest common ancestor
  is the spine node labelled min of the two underlying spine indices;
  the test queries leaf-leaf, leaf-spine, and spine-spine pairs against
  that derivation.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

CHAIN_NODE_COUNT = 200_000
COMB_SPINE_LENGTH = 100_000


def _ids(cases):
    return [case["id"] for case in cases]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().lowestCommonAncestor, case)


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


def test_constructed_chain_of_200000_nodes_meets_at_the_higher_spine_node():
    parent = [-1] + list(range(CHAIN_NODE_COUNT - 1))
    solve = reference.Solution().lowestCommonAncestor
    assert solve(parent, 0, CHAIN_NODE_COUNT - 1) == 0
    assert solve(parent, CHAIN_NODE_COUNT // 2, CHAIN_NODE_COUNT - 1) == CHAIN_NODE_COUNT // 2
    assert solve(parent, CHAIN_NODE_COUNT - 2, CHAIN_NODE_COUNT - 1) == CHAIN_NODE_COUNT - 2
    assert solve(parent, CHAIN_NODE_COUNT - 1, CHAIN_NODE_COUNT - 1) == CHAIN_NODE_COUNT - 1


def test_constructed_comb_of_200000_nodes_meets_on_the_shared_spine():
    parent = [-1] + list(range(COMB_SPINE_LENGTH - 1))
    parent += [spine_index for spine_index in range(COMB_SPINE_LENGTH)]
    solve = reference.Solution().lowestCommonAncestor
    leaf = COMB_SPINE_LENGTH

    assert solve(parent, leaf + 7, leaf + 12) == 7
    assert solve(parent, leaf + 12, leaf + 7) == 7
    assert solve(parent, leaf + 7, 12) == 7
    assert solve(parent, 12, leaf + 7) == 7
    assert solve(parent, 7, 12) == 7
    assert solve(parent, leaf + COMB_SPINE_LENGTH - 1, 0) == 0
