"""Reference-parametrized gauntlet for 0/1 Knapsack.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Bottom-Up Space-Optimized DP reference against cases_full.json. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a naive
definition-model enumeration of every subset via itertools.combinations,
keeping the subsets whose total weight fits the capacity and taking the
maximum total value, which shares no mechanism with the reference's
single-row DP sweep. The output is a deterministic integer, so the
comparison is plain `==` with no canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's three examples, the empty item list at capacity zero
and at a positive capacity, a single item that fits, misses, or lands
exactly on the capacity and weight bounds, capacity zero, the greedy
value-to-weight trap where the best ratio loses, identical items, zero
values, values at the 1000000 bound, a capacity exceeding the total
weight, an exact-fill pairing, two subsets tying on the optimum, ten
items against a tiny capacity, a dominant item that must be left
behind, same-weight items, a skip-to-optimize instance, and a sixteen-
item mixed instance at the oracle's practical size limit. Scale corners
live here as constructed cases per the Testing Strategy rule that
length corners are constructible or synthesized, never serialized bulk;
all three build their item lists in this module and derive every
expected outcome from the construction:

- test_constructed_two_hundred_unit_items_all_fit: 200 items of weight 1
  and value 1 at the statement's item-count bound, capacity 10000 at the
  capacity bound: everything fits, so the answer is 200.
- test_constructed_hundred_weight_items_exact_fill: 200 items of weight
  100 and value 1, capacity 10000: exactly 100 items fill the capacity,
  so the answer is 100.
- test_constructed_awkward_weight_leaves_one_slot_idle: 200 items of
  weight 101 and value 2, capacity 10000: 99 items fit (9999) and one
  more would not, so the answer is 198, pinning that the sweep takes as
  many items as the capacity truly allows rather than a round count.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

ITEM_COUNT_BOUND = 200
CAPACITY_BOUND = 10000


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().maximumKnapsackValue, case)


def test_constructed_two_hundred_unit_items_all_fit():
    weights = [1] * ITEM_COUNT_BOUND
    values = [1] * ITEM_COUNT_BOUND
    assert reference.Solution().maximumKnapsackValue(weights, values, CAPACITY_BOUND) == 200


def test_constructed_hundred_weight_items_exact_fill():
    weights = [100] * ITEM_COUNT_BOUND
    values = [1] * ITEM_COUNT_BOUND
    assert reference.Solution().maximumKnapsackValue(weights, values, CAPACITY_BOUND) == 100


def test_constructed_awkward_weight_leaves_one_slot_idle():
    weights = [101] * ITEM_COUNT_BOUND
    values = [2] * ITEM_COUNT_BOUND
    assert reference.Solution().maximumKnapsackValue(weights, values, CAPACITY_BOUND) == 198
