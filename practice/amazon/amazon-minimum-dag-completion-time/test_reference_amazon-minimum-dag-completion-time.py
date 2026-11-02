"""Reference-parametrized gauntlet for Minimum Completion Time for DAG Dependencies.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Topological Longest-Path Dynamic Programming reference against
cases_full.json. Every expectation in cases_full.json is oracle-derived,
never hand-computed and never recorded from this reference: the oracle
is the fixed-point edge relaxation below, which walks the dependency
list repeatedly until no finish time moves. It has no queue, no
indegree counters, and no topological order, so it shares no mechanism
with the reference's Kahn pass. Per the D3 ruling this oracle stays
alive: every run re-derives each expectation and cross-checks the
reference against it. The output is a deterministic integer, so the
comparison is plain `==` with no canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's three examples, a single task, two parallel tasks, a
three-task chain, a duplicated dependency edge, five independent unit
tasks, a ten-leaf fan-in, an eight-leaf fan-out, a diamond, a double
diamond, durations at the 10^9 bound, a chain that beats one longer
task, two disconnected components, a chain whose edges are listed back
to front, a late long tail, uneven parallel paths, a chain of ten
increasing durations, a twelve-task mixed graph, a hub joining two
fans, an edge repeated three times, and a sources-plus-sink graph.
Scale corners live here as constructed cases per the Testing Strategy
rule that length corners are constructible or synthesized, never
serialized bulk; all four build their graphs in this module at sizes
the alive oracle affords, and each asserts the reference and the oracle
agree:

- test_constructed_chain_of_one_thousand_unit_tasks: a 1000-task chain
  forces one task per topological layer; the answer is the duration
  sum, 1000.
- test_constructed_fan_in_of_two_thousand_leaves: 2000 unit leaves all
  feeding one hub of duration 2; the hub starts at 1 and finishes at 3.
- test_constructed_fan_out_of_one_thousand_five_hundred_leaves: a hub
  of duration 4 feeding 1500 unit leaves; the last leaf finishes at 5.
- test_constructed_chain_of_five_hundred_bound_durations: 500 tasks of
  10^9 chained end to end; the answer is 5 * 10^11, above 32-bit range.
- test_synthesized_random_forward_graph: one seeded 40-task instance
  with forward-only edges, recomputed live by the oracle.

Discrimination record, naming the mutant classes the serialized and
constructed cases catch, every claim verified by applying the mutant
rendering to the reference and running it against all 28 cases
(23 frozen plus five constructed or synthesized). Reading the answer as
`sum(durations)` instead of the largest finish (serial scheduling) is
caught by example_1, example_2, two_in_parallel,
all_unit_five_independent, fan_in_ten_leaves, fan_out_hub, diamond,
double_diamond, chain_beats_single_long, disconnected_chain_and_pair,
uneven_parallel_paths, twelve_task_mixed, hub_between_two_fans,
duplicate_edges_three_times, sources_and_sink_only,
constructed_fan_in_2000, constructed_fan_out_1500, and
synthesized_random_forward_graph; pure chains and single tasks are not
caught because serial and parallel time coincide there. Registering
each edge reversed survives all 28 cases: the answer is the longest
path in the DAG, and the longest path read from either end accumulates
the same total, so reversal never moves the maximum (an honest blind
spot of this gauntlet). Dropping the popped task's own duration
(`finish[task] += 0`) is caught by every non-empty case except none:
all 27 non-empty cases catch it; only the empty example_3 cannot.
Reading the answer from the last dequeued task instead of the maximum
finish is caught by example_2 (whose seven-unit task dequeues early)
and example_3 (which never dequeues, so the read raises); in every
other authored case the topologically last task is also the latest
finisher. Overwriting a successor's start instead of taking the max
(`finish[next_task] = finish[task]`) is caught by example_1 (the later
root's larger start is clobbered by the earlier root's smaller one) and
twelve_task_mixed. Double-decrementing the indegree (`-= 2`, tasks
whose indegree is odd never reaching the queue) is caught by
simple_chain, fan_out_hub, diamond, double_diamond,
big_durations_at_bound, chain_beats_single_long,
disconnected_chain_and_pair, reversed_edge_listing, late_long_tail,
uneven_parallel_paths, chain_of_ten_increasing, twelve_task_mixed,
hub_between_two_fans, constructed_chain_1000, constructed_fan_out_1500,
constructed_chain_500_bound, and synthesized_random_forward_graph;
cases escape only when every undercounted task is redundant for the
maximum (even indegrees like example_1's hub or duplicated_edge's
target enqueue anyway, and example_2's dropped tasks are not the
latest finishers).
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


class FixedPointRelaxation:
    """The oracle: edge relaxation repeated until no finish time moves.

    Each task's finish starts at its own duration (no dependency credit)
    and every `[before, after]` edge raises `finish[after]` toward
    `finish[before] + durations[after]`; passes repeat until a full pass
    changes nothing. On a DAG this converges to the exact forced finish
    times regardless of edge order, with no queue and no topological
    sort.
    """

    @classmethod
    def minimum_completion_time(cls, durations, dependencies):
        finish = list(durations)
        changed = True
        while changed:
            changed = False
            for before, after in dependencies:
                relaxed = finish[before] + durations[after]
                if relaxed > finish[after]:
                    finish[after] = relaxed
                    changed = True
        return max(finish, default=0)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().minimumCompletionTime, case)


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_oracle_agrees_with_frozen_expectation(case):
    assert FixedPointRelaxation.minimum_completion_time(*case["args"]) == case["expected"]


def test_constructed_chain_of_one_thousand_unit_tasks():
    count = 1000
    durations = [1] * count
    dependencies = [[task, task + 1] for task in range(count - 1)]
    expected = count
    assert reference.Solution().minimumCompletionTime(durations, dependencies) == expected
    assert FixedPointRelaxation.minimum_completion_time(durations, dependencies) == expected


def test_constructed_fan_in_of_two_thousand_leaves():
    leaves = 2000
    durations = [1] * leaves + [2]
    dependencies = [[leaf, leaves] for leaf in range(leaves)]
    expected = 3
    assert reference.Solution().minimumCompletionTime(durations, dependencies) == expected
    assert FixedPointRelaxation.minimum_completion_time(durations, dependencies) == expected


def test_constructed_fan_out_of_one_thousand_five_hundred_leaves():
    leaves = 1500
    durations = [4] + [1] * leaves
    dependencies = [[0, leaf] for leaf in range(1, leaves + 1)]
    expected = 5
    assert reference.Solution().minimumCompletionTime(durations, dependencies) == expected
    assert FixedPointRelaxation.minimum_completion_time(durations, dependencies) == expected


def test_constructed_chain_of_five_hundred_bound_durations():
    count = 500
    durations = [10**9] * count
    dependencies = [[task, task + 1] for task in range(count - 1)]
    expected = count * 10**9
    assert reference.Solution().minimumCompletionTime(durations, dependencies) == expected
    assert FixedPointRelaxation.minimum_completion_time(durations, dependencies) == expected


def test_synthesized_random_forward_graph():
    import random

    random.seed(20261101)
    count = 40
    durations = [random.randint(1, 20) for _ in range(count)]
    dependencies = [
        [task, other]
        for task in range(count)
        for other in random.sample(range(task + 1, count), random.randint(0, min(3, count - 1 - task)))
    ]
    expected = FixedPointRelaxation.minimum_completion_time(durations, dependencies)
    assert expected > 0
    assert reference.Solution().minimumCompletionTime(durations, dependencies) == expected
