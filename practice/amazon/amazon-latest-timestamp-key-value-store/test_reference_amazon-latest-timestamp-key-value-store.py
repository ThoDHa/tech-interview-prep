"""Reference-parametrized gauntlet for Latest-Timestamp Key-Value Store.

The generator-emitted test module carries a module-level skip (the
design-operation starter is not a single `==`-assertable call), so the
sanctioned design class lives in reference.py and this module replays
it via run_operations; the generated module stays byte-identical. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a naive
definition-model simulation keeping every set in a full history list
and answering each get by a linear scan that tracks the greatest
timestamp, preferring the later entry on ties, which shares no
mechanism with the reference's single-winner map. The constructor and
mutators expect None; every get expects one string, so run_operations
compares the whole expected list per sequence and no canonicalization
applies.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's two examples, the never-set get returning the empty
string, a later set with a smaller timestamp not replacing, greatest-
timestamp ties resolved to the latest set (including a chain of three
equal timestamps and ties at timestamp zero), a stored empty value
colliding with the never-set empty string in output only, independent
keys, out-of-order arrival, ascending and descending timestamp runs,
the timestamp bounds 0 and 1000000000, maximum-length keys and values,
repeated gets leaving state unchanged, sets after gets, and a many-key
interleave. One scale corner lives here as a constructed case per the
Testing Strategy rule that length corners are constructible or
synthesized, never serialized bulk; it builds its operation sequence in
this module and derives every expected outcome from the construction:

- test_constructed_two_hundred_operations_match_pattern_derived_outcomes:
  200 operations, the statement's sequence-length upper bound. Cycle c
  in 0..99 sets key k(c mod 10) at timestamp c with value v(c) and then
  gets the same key. The get immediately follows its own set, whose
  timestamp is the greatest that key has seen, so the expected value is
  v(c); reaching it requires the winner entry to survive the nine other
  keys' sets in between and to replace the key's previous winner from
  cycle c - 10, which the interleaved ordering exercises on every
  cycle.

The statement's rule that a get row's timestamp and value fields are
ignored lives in the judged array wrapper, not in the design class
whose get takes only the key; the write-up's Solution fences are
additionally executed against the page's statement examples in raw
array form, whose get rows carry nonzero timestamps and nonempty
values, which exercises that rule.
"""

import pytest

from harness import load_cases, load_solution, run_operations

FULL = load_cases(__file__, "cases_full.json")

reference_module = load_solution(__file__, "reference.py")

CHURN_CYCLE_COUNT = 100


def _ids(cases):
    return [case["id"] for case in cases]


def _check(design_class, case):
    result = run_operations(design_class, case["operations"], case["arguments"])
    assert result == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference_module.LatestTimestampStore, case)


def test_constructed_two_hundred_operations_match_pattern_derived_outcomes():
    operations = ["LatestTimestampStore"]
    arguments = [[]]
    expected = [None]
    for cycle in range(CHURN_CYCLE_COUNT):
        key = f"k{cycle % 10}"
        operations.extend(["set", "get"])
        arguments.extend([[cycle, key, f"v{cycle}"], [f"k{cycle % 10}"]])
        expected.extend([None, f"v{cycle}"])
    assert len(operations) == 1 + 2 * CHURN_CYCLE_COUNT
    assert len(operations) == 201
    assert run_operations(reference_module.LatestTimestampStore, operations, arguments) == expected
