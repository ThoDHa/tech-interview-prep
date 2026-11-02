"""Reference-parametrized gauntlet for Dijkstra Shortest Paths in a Weighted Undirected Graph.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Dijkstra with a Min-Heap reference against cases_full.json. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is the fixed-point
Bellman-Ford relaxation (sweep every edge in both orientations until a
full pass changes nothing), which has no heap, no settlement order, and
no adjacency lists, so it shares no mechanism with the reference. Per
the Testing Strategy rule for non-outlier problems, the oracle script
was scratch and was deleted after freezing; the comparison is a
deterministic integer list, so plain `==` with no canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's three examples, self-loops on the source and
elsewhere, duplicated self-loops, zero-weight chains and shortcuts, a
disconnected vertex, an isolated vertex next to an edgeless graph, the
source at the last index, an edge back into the source, two disjoint
components, a star out of the source, a chain, a cycle closed cheaply,
a parallel edge discovered late, weights at the 10^9 bound, a bound
weight versus two hops, and a twelve-vertex mix. Scale corners live
here as constructed cases per the Testing Strategy rule that length
corners are constructible or synthesized, never serialized bulk; the
three constructed tests build their graphs in this module at sizes the
closed form affords, and the synthesized instance's construction is
replayed here with its expectation frozen from the oracle:

- test_constructed_path_of_one_thousand_unit_edges: a 1000-vertex path
  with unit weights; distance equals the vertex index.
- test_constructed_star_of_two_thousand_leaves: 2000 leaves joined to
  the source by weight 2; every leaf sits at distance 2.
- test_constructed_bound_weight_path_of_five_hundred: a 500-vertex path
  of 10^9 edges; the far end reaches 499 * 10^9, past 32 bits.
- a seeded synthesized 60-vertex instance (spanning path plus random
  extra edges) frozen as synthesized_random_connected in
  cases_full.json, its expectation recorded from the oracle with only
  the construction replayed here.

Discrimination record, naming the mutant classes the serialized and
constructed cases catch, every claim verified by applying the mutant
rendering to the reference and running it against all 22 cases
(21 frozen authored corners plus the synthesized instance; the three
large constructed corners are exercised below and were battery-checked
separately). Registering each edge in one
direction only (dropping the reverse append) is caught by
edge_back_into_source, cycle_cheap_to_close, late_cheaper_parallel,
twelve_vertex_mix, and synthesized_random_connected: exactly the cases
whose shortest routes need an edge travelled against its listing
order; graphs whose edges already point forward from the source
escape. Seeding every distance to 0 instead of the unreached sentinel
is caught by 23 of 25 cases (all but example_2 and zero_weight_chain,
whose every vertex sits at distance zero anyway, so the all-zero
table is accidentally right). Counting hops (`arrival = distance +
1`) instead of adding weights is caught by 19 cases;
unit-weight graphs (cycle_cheap_to_close,
path_of_one_thousand_unit_edges) and the all-zero zero_weight_chain
agree by the luck of their weights, and zero_weight_shortcut is
caught through its weight-5 edge. Leaking the unreached sentinel
(computing with `inf` and never translating to -1) is caught by
example_1, self_loop_on_source, duplicate_self_loops,
disconnected_single, isolated_second_vertex, and two_components: the
cases with at least one unreachable vertex. Never seeding the source
distance is caught by all 25 cases, example_2 included, since the
heap then pops a sentinel-keyed entry and the answer table never
becomes real.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

PATH_VERTEX_COUNT = 1000
STAR_LEAF_COUNT = 2000
BOUND_WEIGHT_PATH_LENGTH = 500


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().shortestUndirectedDistances, case)


def test_constructed_path_of_one_thousand_unit_edges():
    vertex_count = PATH_VERTEX_COUNT
    edges = [[vertex, vertex + 1, 1] for vertex in range(vertex_count - 1)]
    expected = list(range(vertex_count))
    assert reference.Solution().shortestUndirectedDistances(vertex_count, edges, 0) == expected


def test_constructed_star_of_two_thousand_leaves():
    vertex_count = STAR_LEAF_COUNT + 1
    edges = [[0, leaf, 2] for leaf in range(1, vertex_count)]
    expected = [0] + [2] * STAR_LEAF_COUNT
    assert reference.Solution().shortestUndirectedDistances(vertex_count, edges, 0) == expected


def test_constructed_bound_weight_path_of_five_hundred():
    vertex_count = BOUND_WEIGHT_PATH_LENGTH
    edges = [[v, v + 1, 10**9] for v in range(vertex_count - 1)]
    expected = [distance * 10**9 for distance in range(vertex_count)]
    assert reference.Solution().shortestUndirectedDistances(vertex_count, edges, 0) == expected
