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
statement and example name: the granted empty array (the statement's
expected 0), single element, one run spanning the whole array,
all-distinct (every run length 1), runs at the start, middle,
and end, ties for the maximum, non-adjacent repeats of one value across
separate runs, signed extreme magnitudes, and randomized arrays, all at
eye-auditable sizes. The output is a deterministic integer, so the
comparison is plain `==`.

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

Discrimination record for the wrong-neighbor compare mutants, each
rendering applied to every case in the module: the randomized item alone
discriminates none of them, all three renderings return the frozen 2 on
that draw, and the serialized cases carry the discrimination instead,
with the constructed all-equal corner joining against the look-ahead
rendering. example_1 catches the back-lagged compare
`nums[index] == nums[index - 2]`: comparing two back misses the first
extension of every run, so the interior [2, 2, 2] run scores 2 and the
mutant answers 2 against the frozen 3. two_equal and the all-equal
corners catch the look-ahead compare `nums[index] == nums[index + 1]`
with the out-of-bounds final index dropped from the loop: a two-element
array never enters the loop (mutant 1 against the frozen 2) and a
whole-array run loses its final extension (9 vs 10 serialized, 99999 vs
100000 constructed). run_at_end catches the lagged-pair compare
`nums[index - 1] == nums[index - 2]`: the condition reads the two
elements before the current one, so a run's first extension never fires
(mutant 2 against the frozen 3; the same shape catches it in
negatives_and_large_values).
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
