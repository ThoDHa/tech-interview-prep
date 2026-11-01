"""Reference-parametrized gauntlet for Longest Equal-Value Run.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Single-Pass Run Counter reference against cases_full.json plus
constructed and synthesized full-size corners. Every expectation in
cases_full.json is oracle-derived, never hand-computed and never
recorded from this
reference: the oracle enumerates run boundaries (indices whose value
differs from their predecessor), takes the longest stretch between
consecutive boundaries and the array ends, and shares no mechanism with
the reference's rolling counter. The statement parses with no
constraints block, so the gauntlet covers the corner shapes its
statement and example name: single element, one run spanning the whole
array, all-distinct (every run length 1), runs at the start, middle,
and end, ties for the maximum, non-adjacent repeats of one value across
separate runs, signed extreme magnitudes, and randomized arrays, all at
eye-auditable sizes. Arrays are non-empty by assumption, and the output
is a deterministic integer, so the comparison is plain `==`.

The two serialized length corners were converted to constructed or
synthesized cases per the Testing Strategy rule that length corners are
constructible or synthesized, never serialized bulk:

- test_constructed_strictly_ascending_array_answers_one: 0..99999 is
  strictly ascending, so no two neighbors are equal, every run has
  length 1, and the answer follows from the construction as 1.
- test_constructed_all_equal_array_answers_full_length: one value
  repeated 100000 times is a single run spanning the whole array, so
  the answer is the array length itself.
- test_synthesized_randomized_array_matches_frozen_expectation: the
  review-sanctioned single seeded randomized representative at the
  100000-element scale; values are drawn with one random.Random(20261031)
  generator over the narrow 1250-value domain, since the signed 10^9
  domain almost surely draws no adjacent equal pair in 10^5 draws and
  its outcome would merely repeat the constructed strictly-ascending
  corner instead of exercising run boundaries. Only the frozen
  expectation is stored (2, frozen from the boundary-enumeration oracle
  and confirmed by the reference's rolling counter).
"""

import random

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference_module = load_solution(__file__, "reference.py")

CONSTRUCTED_LENGTH = 100000
RANDOMIZED_SEED = 20261031
RANDOMIZED_LENGTH = 100000
RANDOMIZED_VALUE_DOMAIN = 1250
RANDOMIZED_FROZEN_EXPECTATION = 2


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference_module.Solution().solve, case)


def test_constructed_strictly_ascending_array_answers_one():
    ascending = list(range(CONSTRUCTED_LENGTH))
    assert reference_module.Solution().solve(ascending) == 1


def test_constructed_all_equal_array_answers_full_length():
    all_equal = [5] * CONSTRUCTED_LENGTH
    assert reference_module.Solution().solve(all_equal) == CONSTRUCTED_LENGTH


def test_synthesized_randomized_array_matches_frozen_expectation():
    value_rng = random.Random(RANDOMIZED_SEED)
    randomized = [
        value_rng.randrange(0, RANDOMIZED_VALUE_DOMAIN) for _ in range(RANDOMIZED_LENGTH)
    ]
    assert reference_module.Solution().solve(randomized) == RANDOMIZED_FROZEN_EXPECTATION
