"""Reference-parametrized gauntlet for Connect N Ropes With Minimum Cost.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Min-Heap with heapq reference against cases_full.json plus
constructed and synthesized full-size corners. The statement defines
its procedure
literally, so the oracle was an independently coded implementation of
that same smallest-first greedy rather than a different algorithm: a
two-queue merge planner (original ropes sorted once, merged sums
drained from a second FIFO queue, two smallest fronts per round) that
shares no mechanism with the reference's heap. Before freezing, every
small and medium expectation was cross-checked against a second
independent implementation (a re-sorting simulation), so each frozen
value carries three agreeing implementations. The gauntlet covers the
statement's named corners: the single-rope zero cost, one merge for two
ropes, all-equal lengths, the ropes[i] boundaries 1 and 10^4,
adversarial descending order, and randomized shapes, all at
eye-auditable sizes. The output is a deterministic integer, so the
comparison is plain `==`.

The three serialized length corners were converted to constructed or
synthesized cases per the Testing Strategy rule that length corners are
constructible or synthesized, never serialized bulk:

- test_constructed_all_equal_ropes_match_depth_profile_closed_form at
  2000 ropes of length 7 and at the statement's 100000-rope and
  10^4-length bounds (the signed-64-bit total corner): for rope_count
  ropes of one common length, every merge tree costs that length times
  the sum of leaf depths, and the smallest-first greedy on equal
  weights repeatedly merges equal-sized subtrees, so its merge tree is
  the complete binary tree: with shallow_depth = floor(log2 rope_count),
  2 * (rope_count - 2**shallow_depth) leaves sit at depth
  shallow_depth + 1 and the rest at depth shallow_depth. The test
  asserts the reference against that closed form, which also agrees
  with the serialized all_equal case ([5] x 5 -> 60).
- test_synthesized_randomized_ropes_match_frozen_expectation: the
  review-sanctioned single seeded randomized representative at the
  100000-rope scale; lengths are drawn with one random.Random(20261031)
  generator over 1..10^4, and only the frozen expectation is stored
  (8169573966, frozen from the two-queue oracle and confirmed by the
  reference's heapq mechanism).
"""

import random

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference_module = load_solution(__file__, "reference.py")

RANDOMIZED_SEED = 20261031
RANDOMIZED_ROPE_COUNT = 100000
RANDOMIZED_FROZEN_EXPECTATION = 8169573966

CONSTRUCTED_SHAPES = [(2000, 7), (100000, 10000)]


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


def _equal_rope_closed_form(rope_count: int, rope_length: int) -> int:
    """Return the minimum connection cost of rope_count ropes of one
    common length via the complete-tree depth profile.

    The smallest-first greedy on equal weights builds the complete
    binary tree, so the cost is the length times the leaf-depth sum:
    leaves at depth floor(log2 rope_count) sit one level shallower than the rest.
    """
    shallow_depth = rope_count.bit_length() - 1
    deep_count = 2 * (rope_count - 2**shallow_depth)
    shallow_count = rope_count - deep_count
    return rope_length * (shallow_count * shallow_depth + deep_count * (shallow_depth + 1))


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference_module.Solution().minimumRopeConnectionCost, case)


@pytest.mark.parametrize(
    ("rope_count", "rope_length"),
    CONSTRUCTED_SHAPES,
    ids=["medium_scale", "statement_bounds"],
)
def test_constructed_all_equal_ropes_match_depth_profile_closed_form(rope_count, rope_length):
    ropes = [rope_length] * rope_count
    assert (
        reference_module.Solution().minimumRopeConnectionCost(ropes)
        == _equal_rope_closed_form(rope_count, rope_length)
    )


def test_synthesized_randomized_ropes_match_frozen_expectation():
    length_rng = random.Random(RANDOMIZED_SEED)
    lengths = [length_rng.randrange(1, 10**4 + 1) for _ in range(RANDOMIZED_ROPE_COUNT)]
    assert (
        reference_module.Solution().minimumRopeConnectionCost(lengths)
        == RANDOMIZED_FROZEN_EXPECTATION
    )
