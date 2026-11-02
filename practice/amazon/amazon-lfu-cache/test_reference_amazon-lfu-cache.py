"""Reference-parametrized gauntlet for LFU Cache.

The generator-emitted test module carries a module-level skip (the
design-operation starter is not a single `==`-assertable call), so the
sanctioned design class lives in reference.py and this module replays
it via run_operations; the generated module stays byte-identical. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a naive
definition-model simulation keeping plain `key -> (value, frequency,
stamp)` records and answering eviction by a full linear scan for the
minimum `(frequency, stamp)`, which shares no mechanism with the
reference's frequency buckets and doubly linked lists. The constructor
and mutators expect None; every get expects one integer, so
run_operations compares the whole expected list per sequence and no
canonicalization applies.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's two examples, the single-get minimum, capacity one
(eviction on every fresh insert), an updating put that must not evict
and must bump frequency, an updating put landing on a full cache that
must keep both keys, the frequency tie broken by recency, a miss get
touching nothing, a promotion saving a key, a re-inserted evicted key
starting fresh, negative and int32-extreme keys and values, a stored -1
colliding with the miss sentinel in output only, the min-frequency
pointer advancing before a fresh key refills its emptied bucket, a
large capacity (3000) with few keys, and a small interleaved churn. Two scale corners
live here as constructed cases per the Testing Strategy rule that
length corners are constructible or synthesized, never serialized bulk;
both build their operation sequences in this module and derive every
expected outcome from the construction:

- test_constructed_capacity_fill_evicts_the_lru_head: 3000 fresh keys
  fill the cache to the statement's capacity upper bound; all sit at
  frequency 1, so inserting one more key evicts the head of the minimum
  bucket, which is the first-inserted key; that key's get then misses
  while two untouched survivors still hit.
- test_constructed_twenty_thousand_op_churn_matches_pattern_derived_outcomes:
  20000 operations, the statement's operations-length upper bound. Cycle
  0 puts key 0, gets it (hit), and gets key 1 (miss). Cycle c >= 1
  puts key c, gets key c (hit), and gets key c - 1. At cycle 1 the
  cache holds only key 0 (frequency 2), so the fresh key fits without
  eviction and get 0 still hits, raising key 0 to frequency 3; from
  cycle 2 on the cache holds key 0 (frequency 3, never touched again)
  beside key c - 1 (frequency 2 from its insertion-cycle get), so the
  fresh key evicts key c - 1 and that get misses. Every outcome follows
  from the cycle index, and the final get of key 0 still hits with its
  original value.

Discrimination record, naming the mutant classes the serialized cases
catch, each claim verified by running the mutant against every case:
an LRU-instead-of-LFU eviction is caught by frequent_but_older_key_survives,
repeated_update_single_key, and min_advances_before_bucket_refill; an
MRU-instead-of-LRU tie break by recency_tie_after_parallel_promotion
and five further cases; skipping the frequency bump on an updating put
by update_never_evicts; running the capacity check before the
membership check, which evicts on an updating put, by
update_on_full_keeps_both_keys, the one case where an updated key and
an untouched key then compete at different frequencies; failing to
advance min_frequency crashes on an empty eviction bucket in example_1,
update_on_full_keeps_both_keys, and seven further cases, every catcher
failing by crash and none reading a wrong victim
(min_advances_before_bucket_refill survives this mutant because a
fresh insert re-creates the emptied bucket and resets min_frequency
before the stale pointer is read, so it catches only the
LRU-instead-of-LFU eviction named above); advancing min_frequency
whenever any bucket empties is caught by lower_frequency_beats_recency
and min_freq_advances_on_empty_bucket.
"""

import pytest

from harness import load_cases, load_solution, run_operations

FULL = load_cases(__file__, "cases_full.json")

reference_module = load_solution(__file__, "reference.py")

CAPACITY_FILL = 3000
CHURN_CYCLE_COUNT = 6665
CHURN_FINAL_KEY = 0


def _ids(cases):
    return [case["id"] for case in cases]


def _check(design_class, case):
    result = run_operations(design_class, case["operations"], case["arguments"])
    assert result == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference_module.LFUCache, case)


def test_constructed_capacity_fill_evicts_the_lru_head():
    operations = ["LFUCache"]
    arguments = [[CAPACITY_FILL]]
    expected = [None]
    for key in range(CAPACITY_FILL):
        operations.append("put")
        arguments.append([key, key])
        expected.append(None)
    operations.extend(["put", "get", "get", "get"])
    arguments.extend([[CAPACITY_FILL, CAPACITY_FILL], [0], [1], [CAPACITY_FILL - 1]])
    expected.extend([None, -1, 1, CAPACITY_FILL - 1])
    assert len(operations) == CAPACITY_FILL + 5
    assert run_operations(reference_module.LFUCache, operations, arguments) == expected


def test_constructed_twenty_thousand_op_churn_matches_pattern_derived_outcomes():
    operations = ["LFUCache"]
    arguments = [[2]]
    expected = [None]
    operations.extend(["put", "get", "get"])
    arguments.extend([[0, 0], [0], [1]])
    expected.extend([None, 0, -1])
    for cycle in range(1, CHURN_CYCLE_COUNT + 1):
        operations.extend(["put", "get", "get"])
        arguments.extend([[cycle, cycle], [cycle], [cycle - 1]])
        expected.extend([None, cycle, cycle - 1 if cycle == 1 else -1])
    operations.append("get")
    arguments.append([CHURN_FINAL_KEY])
    expected.append(CHURN_FINAL_KEY)
    assert len(operations) == 1 + 3 * (CHURN_CYCLE_COUNT + 1) + 1
    assert len(operations) == 20000
    assert run_operations(reference_module.LFUCache, operations, arguments) == expected
