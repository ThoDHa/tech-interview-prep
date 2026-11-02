"""Reference-parametrized gauntlet for Lazy Merge of Sorted Event Streams.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Min-Heap of Stream Heads reference against cases_full.json. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a flat
concatenate-and-sort over all events, which shares no mechanism with
the reference's per-stream heap merge (the oracle is exactly the
O(N)-memory approach the statement's O(k) merge rule forbids, which is
why it judges only the output, not the memory). Expectations were
frozen from that oracle and the scratch script deleted; the output is
a deterministic sequence, so the comparison is plain `==` with no
canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's two examples, zero streams, all-empty rows, a single
empty row, a single stream, duplicates within and across rows,
negative timestamps, the signed 32-bit extremes, strict interleave,
one long stream beside a one-event stream, disjoint and reversed
range pairs, equal timestamps everywhere, empty rows first and last,
a three-way overlap, a zero flood, and a sign-spread triple. Scale
corners live here as constructed cases per the Testing Strategy rule
that length corners are constructible or synthesized, never serialized
bulk; all three build their streams in this module and derive every
expected outcome from the construction:

- test_constructed_ten_thousand_streams_round_robin: 10000 streams,
  the statement's stream-count bound, carrying the events 0..199999
  dealt round-robin, so every row is strictly ascending and the merge
  must return exactly the dealt sequence of 200000 events, the
  statement's total-event bound.
- test_constructed_single_stream_of_two_hundred_thousand: one stream
  holding 0..199999: the heap degenerates to a single head and the
  merge must return the row unchanged.
- test_constructed_half_empty_streams_round_robin: 5000 empty rows
  interleaved with 5000 rows carrying 0..199999 round-robin: empty
  rows never enter the heap and the merge returns the dealt sequence.

Discrimination record, naming the mutant classes the serialized cases
catch, each claim verified by running the mutant against every case:
returning the deduplicated sort (a set instead of a multiset) is
caught by example_1, example_2, single_stream, duplicates_within,
duplicates_across, int32_extremes, one_giant_one_tiny, all_equal, and
zero_flood; emitting the plain concatenation without sorting is
caught by example_1, example_2, negatives, int32_extremes,
interleaved, one_giant_one_tiny, disjoint_ranges, reversed_ranges,
three_way_overlap, zero_flood, and sign_spread; seeding the heap
without the nonempty guard crashes on example_1, example_2, all_empty,
single_empty, empty_first, and empty_last (IndexError on an empty
row's first head); advancing every stream whose head equals the
popped timestamp and dropping their heads unemitted is caught by
example_1, example_2, duplicates_across, int32_extremes,
one_giant_one_tiny, all_equal, and zero_flood; stopping once stream 0
exhausts is caught by example_1, duplicates_across, negatives,
int32_extremes, interleaved, all_equal, three_way_overlap, and
zero_flood, the cases where another stream still holds events after
stream 0's row is consumed; the stop is tested after the exhausting
event is emitted, where a pre-push or post-push placement behaves
identically, and every case with nothing pending at that moment
survives it, single_stream included, because stopping then is natural
termination (a pre-emit placement additionally drops stream 0's
exhausting event and catches the rest); and advancing the
winning stream's cursor by two (skipping an event) is caught by
example_1, example_2, single_stream, duplicates_within,
duplicates_across, negatives, int32_extremes, interleaved,
one_giant_one_tiny, disjoint_ranges, reversed_ranges, all_equal,
three_way_overlap, zero_flood, and sign_spread.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

STREAM_COUNT_BOUND = 10000
EVENT_TOTAL_BOUND = 200000


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().mergeEventStreams, case)


def test_constructed_ten_thousand_streams_round_robin():
    streams = [list(range(offset, EVENT_TOTAL_BOUND, STREAM_COUNT_BOUND)) for offset in range(STREAM_COUNT_BOUND)]
    expected = list(range(EVENT_TOTAL_BOUND))
    assert reference.Solution().mergeEventStreams(streams) == expected


def test_constructed_single_stream_of_two_hundred_thousand():
    streams = [list(range(EVENT_TOTAL_BOUND))]
    assert reference.Solution().mergeEventStreams(streams) == list(range(EVENT_TOTAL_BOUND))


def test_constructed_half_empty_streams_round_robin():
    half = STREAM_COUNT_BOUND // 2
    full_rows = [list(range(offset, EVENT_TOTAL_BOUND, half)) for offset in range(half)]
    streams = [row for pair in zip(full_rows, [[]] * half) for row in pair]
    expected = list(range(EVENT_TOTAL_BOUND))
    assert reference.Solution().mergeEventStreams(streams) == expected
