"""Reference-parametrized gauntlet for Bounded IPv4 Filter.

The generator-emitted test module carries a module-level skip (the
design-operation starter is not a single `==`-assertable call), so the
sanctioned design class lives in reference.py and this module replays
it via run_operations; the generated module stays byte-identical. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a naive
definition-model simulation keeping the pool as a plain list of
canonical address strings with linear-scan membership, add guarded by
the scan and the 128-entry limit, and remove deleting on a hit, which
shares no mechanism with the reference's packed-integer set. Mutators
and the constructor expect None; every check_ip expects one boolean, so
run_operations compares the whole expected list per sequence and no
canonicalization applies. The gauntlet covers the statement's named
corners: the page's three examples, the zero-operations input
(represented by the constructor-only sequence; the truly empty input is
a page-API shape covered by the write-up's fence gate, since
run_operations requires at least the constructor operation), empty-pool
checks, duplicate adds, absent removals, all-octet boundary addresses,
exact-match digit neighbors (10.0.0.1 versus 10.0.0.10 versus
1.0.0.10), and randomized add/remove/check interleavings, all at
eye-auditable sizes.

The two serialized length corners were converted to constructed cases
per the Testing Strategy rule that length corners are constructible or
synthesized, never serialized bulk; both build their operation
sequences in this module and derive every expected outcome from the
construction:

- test_constructed_cap_fill_ignores_overflow_add_and_accepts_retry_after_removal:
  128 distinct adds fill the pool to the statement's limit; the next
  add targets a fresh address and is ignored because the pool is full,
  so its check is false; the first filled address still checks true
  (the ignored add evicted nothing); removing it frees one slot and
  flips its check to false; the retried add is then accepted, so its
  check is true.
- test_constructed_churn_stream_matches_pattern_derived_outcomes: 2000
  cycles of five operations, 10000 operations plus the constructor,
  hitting the statement's operations-length upper bound. Cycle c adds
  a_c and checks it (true: the same cycle added it, and the pool holds
  at most three addresses, far below the limit), checks a_{c-1} for
  c >= 1 (true: a_{c-1} is removed only in cycle c + 1; cycle 0 probes
  a_1999, first added in the final cycle, so false), then removes
  a_{c-2} for c >= 2 and checks it (false: removed in the same cycle;
  cycles 0 and 1 instead remove a never-added probe address, an absent
  removal, which also checks false). After cycle c the pool holds
  exactly {a_{c-1}, a_c}.
"""

import pytest

from harness import load_cases, load_solution, run_operations

FULL = load_cases(__file__, "cases_full.json")

reference_module = load_solution(__file__, "reference.py")

POOL_FILL_COUNT = 128
CHURN_CYCLE_COUNT = 2000
CHURN_CYCLE_OPERATIONS = 5
CHURN_PROBE_ADDRESS = "255.255.255.255"


def _ids(cases):
    return [case["id"] for case in cases]


def _check(design_class, case):
    result = run_operations(design_class, case["operations"], case["arguments"])
    assert result == case["expected"]


def _churn_address(cycle_index: int) -> str:
    """Return the canonical churn address of one cycle, distinct per cycle."""
    return f"10.{cycle_index // 256}.{cycle_index % 256}.7"


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference_module.IPv4Pool, case)


def test_constructed_cap_fill_ignores_overflow_add_and_accepts_retry_after_removal():
    operations = ["IPv4Pool"]
    arguments = [[]]
    expected = [None]
    filled = [f"10.0.{position // 256}.{position % 256}" for position in range(POOL_FILL_COUNT)]
    for address in filled:
        operations.append("add_ip")
        arguments.append([address])
        expected.append(None)
    retried = "192.168.1.1"
    operations.extend(
        ["add_ip", "check_ip", "check_ip", "remove_ip", "check_ip", "add_ip", "check_ip"]
    )
    arguments.extend(
        [[retried], [retried], [filled[0]], [filled[0]], [filled[0]], [retried], [retried]]
    )
    expected.extend([None, False, True, None, False, None, True])
    assert run_operations(reference_module.IPv4Pool, operations, arguments) == expected


def test_constructed_churn_stream_matches_pattern_derived_outcomes():
    operations = ["IPv4Pool"]
    arguments = [[]]
    expected = [None]
    for cycle_index in range(CHURN_CYCLE_COUNT):
        address = _churn_address(cycle_index)
        predecessor = (
            _churn_address(cycle_index - 1)
            if cycle_index
            else _churn_address(CHURN_CYCLE_COUNT - 1)
        )
        target = _churn_address(cycle_index - 2) if cycle_index >= 2 else CHURN_PROBE_ADDRESS
        operations.extend(["add_ip", "check_ip", "check_ip", "remove_ip", "check_ip"])
        arguments.extend([[address], [address], [predecessor], [target], [target]])
        expected.extend([None, True, cycle_index > 0, None, False])
    assert len(operations) == 1 + CHURN_CYCLE_COUNT * CHURN_CYCLE_OPERATIONS
    assert run_operations(reference_module.IPv4Pool, operations, arguments) == expected
