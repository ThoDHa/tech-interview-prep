"""Reference-parametrized gauntlet for Parking Garage Allocator.

The generator-emitted test module carries a module-level skip (the
design-operation starter is not a single `==`-assertable call), so the
sanctioned design class lives in reference.py and this module replays
it via run_operations; the generated module stays byte-identical. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a naive
definition-model simulation keeping one boolean per space and answering
each park by scanning candidate starts left to right for the first
all-free window, exactly as the statement's leftmost-fit rule reads. It
shares no mechanism with the reference's free-interval list. The
constructor and every leave expect None; every park expects one
integer, so run_operations compares the whole expected list per
sequence and no canonicalization applies.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's two examples, the one-space garage minimum, a
single-park operation minimum, a single-cell leave-and-refill cycle, an
exact fill that turns the next park away, a full garage rejecting every
size, free cells totalling two with no contiguous pair (fragmentation),
a short front gap the first fit must skip, two fitting gaps where the
leftmost wins, one-sided merges left and right, a merge of both sides
into one run, a boundary leave at the left edge followed by an exact
size-three fit, a boundary leave at the last cell, a partial leave that
frees exactly its stated size, a middle hole reclaimed leftmost, an
exact tail refit of a size-three run, an interleaved churn mixing parks
and leaves, and a one-operation sequence whose only park fails. Three
scale corners live here as constructed cases per the Testing Strategy
rule that length corners are constructible or synthesized, never
serialized bulk; all three build their operation sequences in this
module and derive every expected outcome from the construction:

- test_constructed_full_fill_of_hundred_thousand_spaces: 50000 parks of
  two fill the statement's 100000-space bound exactly, parking at every
  even index, and the next park fails.
- test_constructed_alternating_leave_park_churn_at_scale: the same full
  garage, then leave-and-park cycles that free the pair at `2 * cycle`
  and reclaim it immediately: the freed pair is the only gap, so every
  park returns the position just freed, and the sequence stays within
  the statement's 100000-operation bound.
- test_constructed_fragmentation_then_coalescence_at_scale: 49998
  filled pairs, every other pair freed: 24999 gaps of two separated by
  occupied pairs make the next park of three fail, freeing the rest
  coalesces the whole garage only if the leave merges its neighbors,
  and the final park of three returns 0.

Discrimination record, naming the mutant classes the serialized cases
catch, each claim verified by running the mutant against every case:
allocating at the rightmost fitting run instead of the leftmost is
caught by example_1 and fragmented_free_cells_reject_size_two;
placing at the chosen run's far end instead of its start by 14 of the
19, escaping exactly example_2, min_garage_single_park,
min_garage_leave_refill_cycle, full_garage_rejects_all_sizes, and
single_operation_oversize, whose parks all land where the run's start
is its own far end; skipping exact-fit runs with a strict comparison
by 17 of the 19, escaping exactly example_1 and
single_operation_oversize, whose parks never meet an exactly-fitting
run; dropping the left merge by merge_left_enables_size_three and
merge_both_sides_into_one_run; dropping the right merge by
merge_right_enables_size_three and leave_left_boundary_then_oversize;
dropping both merges by those four cases; freeing one cell past the
stated range by 10 of the 19, escaping exactly the five leave-free
sequences example_2, min_garage_single_park, exact_fill_then_fail,
full_garage_rejects_all_sizes, and single_operation_oversize plus
example_1, min_garage_leave_refill_cycle,
leave_left_boundary_then_oversize, and size_three_exact_tail_fit,
whose extra freed cell moves no later park; and keeping an
exactly-consumed run in the list (stale run, later double booking) by
9 of the 19, escaping exactly example_1, example_2,
min_garage_single_park, min_garage_leave_refill_cycle,
fragmented_free_cells_reject_size_two, first_fit_skips_short_front_gap,
leftmost_of_two_fitting_gaps, merge_right_enables_size_three,
merge_both_sides_into_one_run, and single_operation_oversize.
"""

import pytest

from harness import load_cases, load_solution, run_operations

FULL = load_cases(__file__, "cases_full.json")

reference_module = load_solution(__file__, "reference.py")

SPACE_COUNT_BOUND = 100000
OPERATION_COUNT_BOUND = 100000


def _ids(cases):
    return [case["id"] for case in cases]


def _check(design_class, case):
    result = run_operations(design_class, case["operations"], case["arguments"])
    assert result == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference_module.ParkingGarage, case)


def test_constructed_full_fill_of_hundred_thousand_spaces():
    operations = ["ParkingGarage"]
    arguments = [[SPACE_COUNT_BOUND]]
    expected = [None]
    for position in range(0, SPACE_COUNT_BOUND, 2):
        operations.append("park")
        arguments.append([2])
        expected.append(position)
    operations.append("park")
    arguments.append([2])
    expected.append(-1)
    assert len(operations) == SPACE_COUNT_BOUND // 2 + 2
    assert run_operations(reference_module.ParkingGarage, operations, arguments) == expected


def test_constructed_alternating_leave_park_churn_at_scale():
    operations = ["ParkingGarage"]
    arguments = [[SPACE_COUNT_BOUND]]
    expected = [None]
    for position in range(0, SPACE_COUNT_BOUND, 2):
        operations.append("park")
        arguments.append([2])
        expected.append(position)
    churn_cycles = (OPERATION_COUNT_BOUND - len(operations)) // 2
    for cycle in range(churn_cycles):
        freed_start = 2 * cycle
        operations.extend(["leave", "park"])
        arguments.extend([[freed_start, 2], [2]])
        expected.extend([None, freed_start])
    assert len(operations) <= OPERATION_COUNT_BOUND
    assert run_operations(reference_module.ParkingGarage, operations, arguments) == expected


def test_constructed_fragmentation_then_coalescence_at_scale():
    space_count = 99996
    pair_count = space_count // 2
    operations = ["ParkingGarage"]
    arguments = [[space_count]]
    expected = [None]
    for position in range(0, space_count, 2):
        operations.append("park")
        arguments.append([2])
        expected.append(position)
    for pair_index in range(0, pair_count, 2):
        operations.append("leave")
        arguments.append([2 * pair_index, 2])
        expected.append(None)
    operations.append("park")
    arguments.append([3])
    expected.append(-1)
    for pair_index in range(1, pair_count, 2):
        operations.append("leave")
        arguments.append([2 * pair_index, 2])
        expected.append(None)
    operations.append("park")
    arguments.append([3])
    expected.append(0)
    assert len(operations) == 99999
    assert run_operations(reference_module.ParkingGarage, operations, arguments) == expected
