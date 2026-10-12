# [Get Max Servers](https://www.fastprep.io/problems/amazon-find-maximum-number-of-servers)

**Medium** | **NN minutes** | **Array, Sorting, Greedy**

Source note: 2026-07-02 — This problem duplicates Server Selection. Sighting dates were merged into this fuller official-source version, which remains the recommended practice page.

A company that uses cloud servers is planning to scale up its application horizontally. It needs to buy a certain number of servers from a given set of n servers. To ensure that adjacent servers have similar load handling capacity, they want the computational power of two adjacent servers to have a difference of 1 or less.

Given the computational power of all the n servers as an array of integers powers, find the maximum number of servers that the client can buy such that the selected set of servers can be rearranged in a way that the absolute difference between the computational power of two adjacent servers is less than or equal to 1. The client wants to create a circular network, so the first and last servers in the sequence are also considered adjacent.

More formally, a sequence candidate[] of length m is classified as a candidate for selection by the client if it can be rearranged in a way such that abs(candidate[i] - candidate[i+1]) <= 1 for 0 <= i < m-1 and abs(candidate[m-1] - candidate[0]) <= 1.

Find the maximum number of servers the client can buy from the n available servers.

Note:

A subsequence is a sequence that can be derived from the given sequence by deleting zero or more elements without changing the order of the remaining elements.

## Examples

### Example 1

**Input:** `powers = [4, 3, 5, 1, 2, 2, 1]`

**Output:** `5`

**Explanation:** Source update (July 2, 2026) ᕙ( •̀ ᗜ •́ )ᕗ : I found an official source image that includes the example illustration.

Example source illustration











4











3











5












1










2










2










1




selected subsequence
Highlighted values form [3, 1, 2, 2, 1].






Consider powers = [4, 3, 5, 1, 2, 2, 1].

The subsequence [3, 1, 2, 2, 1] can be selected (5 servers) and rearranged to [2, 1, 1, 2, 3]. Checking circular adjacency: abs(2-1)=1, abs(1-1)=0, abs(1-2)=1, abs(2-3)=1, and (circular) abs(3-2)=1, all of which are <= 1.

No valid candidate of size greater than 5 exists, so the maximum number of servers the client can buy is 5.

## Constraints

- `1 <= n <= 2 * 10^5`
- `0 <= powers[i] <= 10^9`

## Solutions

Because the client may rearrange the selected servers however it likes, the order
the servers appear in `powers` is irrelevant: a selection is judged purely as a
multiset of computational powers. Every approach below asks the same question in
different clothes: which multisets pass the circular adjacency test, and which
passing multiset is largest?

### Bitmask Subset Enumeration

#### Derivation

The most literal reading of the objective: a selection is any subset of the `n`
servers, and the best selection is the largest subset whose powers can be laid
around a circle so every neighbor pair differs by at most 1. Enumerate every
subset, test every circular arrangement of it, and keep the largest subset that
passes:

1. For every non-empty bitmask over the `n` servers, collect the selected
   powers into `chosen`.
2. For every `order`, a permutation of `chosen`, check all `n` adjacent pairs
   around the circle, including the wrap pair
   `abs(order[n-1] - order[0]) <= 1`.
3. The first passing `order` marks `chosen` as selectable; raise `best_count`
   to `len(chosen)` when it is larger.
4. Return `best_count` after all bitmasks are processed.

#### Walkthrough

Example 1 has `n = 7`, so `2^7 - 1 = 127` subsets would fill the table; to keep
the trace readable we use a smaller tailored input with the same structure,
`powers = [2, 1, 2, 3]`. The masks are enumerated from 1 to 15; each row shows
the selected powers and the verdict of the arrangement search:

```text
mask   chosen      circular order tried      verdict
   1   (2)         (2)                       pass
   2   (1)         (1)                       pass
   3   (1, 2)      (1, 2)                    pass
   4   (2)         -                         pass
   5   (2, 2)      (2, 2)                    pass
   6   (1, 2)      -                         pass
   7   (1, 2, 2)   (1, 2, 2)                 pass
   8   (3)         -                         pass
   9   (2, 3)      (2, 3)                    pass
  10   (1, 3)      (1, 3)                    fail: wrap pair abs(3-1) = 2
  11   (1, 2, 3)   (1, 2, 3), (1, 3, 2),     fail: a circle of three values
                   (2, 1, 3), ...            always joins 1 and 3 somewhere,
                                                  and that difference is 2
  12   (2, 3)      -                         pass
  13   (2, 2, 3)   (2, 2, 3)                 pass
  14   (1, 2, 3)   -                         fail, as mask 11
  15   (1, 2, 2, 3) (2, 1, 2, 3)             pass: pairs 2-1, 1-2, 2-3,
                                                 wrap 3-2, all <= 1
```

Row mask 11 is the instructive failure: with three distinct values in a circle
of three positions, values 1 and 3 must stand adjacent somewhere (only value 2
sits between them), and that difference is 2. Row mask 15 shows the pass: the
duplicated 2 lets the circle climb 1 → 2 → 3 and come back down. The largest
passing subset has 4 powers. (For Example 1, the same enumeration examines 127
subsets; the largest passing one is {1, 1, 2, 2, 3} with the arrangement
[2, 1, 1, 2, 3] given in the statement, so it returns 5.)

#### Solution

```python
from itertools import permutations
from typing import List


class Solution:
    def solve(self, powers: List[int]) -> int:
        """Return the largest selectable multiset size for a circular network.

        Time:  O(2^n * n * n!): every non-empty subset is enumerated, and each
            is tested against up to n! circular orders at n adjacency checks
            per order.
        Space: O(n) for the current subset and the current candidate order.
        """
        server_count = len(powers)
        best_count = 0
        for mask in range(1, 1 << server_count):
            chosen = [
                powers[position]
                for position in range(server_count)
                if mask >> position & 1
            ]
            for order in permutations(chosen):
                if all(
                    abs(order[position] - order[(position + 1) % len(order)]) <= 1
                    for position in range(len(order))
                ):
                    best_count = max(best_count, len(chosen))
                    break
        return best_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n × n!)`

There are `2^n - 1` non-empty subsets; each costs up to `n!` circular orders
and each order costs `n` adjacency checks.

##### Space Complexity: `O(n)`

Only the current subset `chosen` and the current candidate `order` are held at
once.

#### Key Insights

- Because rearrangement is allowed, a subset's fate does not depend on which
  servers were picked, only on the multiset of powers, so enumerating bitmasks
  over servers is pure overhead the later approaches delete.
- The circular wrap pair is what makes duplicates matter: in a line, sorting
  the values would always suffice, but a circle must close from the largest
  value back to the smallest.
- The subset {1, 2, 3} failing while {1, 2, 2, 3} passes pinpoints the whole
  problem: interior values of the chosen range must be crossed twice.

### Sorted Window Enumeration

#### Derivation

The enumeration re-asks the same multiset question 2^n times and never uses
the structure the circular adjacency rule imposes. That structure has three
parts. First, a selectable multiset's distinct values form a contiguous
integer range: if values `v1 < v2 < v3` are present but `v2` is missing, the
circle must at some point join a neighbor ≤ `v1` to a neighbor ≥ `v3`, a
difference of at least 2, which is forbidden. Second, extra copies never hurt:
if a multiset is selectable, inserting one more copy of any value beside its
existing copy keeps every adjacent difference at 0 or 1, so some optimal
selection takes every copy of each value it contains. Third, a contiguous
range with full copy counts is selectable exactly when every interior value
has at least two copies: the circle must climb from values below `v` to values
above `v` and later come back down, each crossing must stand on a copy of `v`
because neighbors differ by at most 1, and a single copy leaves one of the two
crossings unguarded. (Conversely two copies suffice: lay one copy of each
value going up `low, low+1, ..., high`, then a second copy of the interior
values going back down, and tuck any remaining copies beside their own value.)

Together these say the only selections worth scoring are full-count chains of
consecutive values, so after run-length encoding the sorted array it is enough
to score every chain of runs with consecutive values:

1. Sort into `sorted_powers` and run-length encode it into `run_values` and
   `run_counts`.
2. Precompute `single_tally`, a prefix count of runs holding exactly one copy,
   and `run_totals`, a prefix count of servers, so each chain is judged in
   constant time.
3. For every `chain_start`, extend `chain_end` while values differ by exactly
   1; a chain is selectable when no interior run is a singleton
   (`single_tally[chain_end] - single_tally[chain_start + 1] == 0`).
4. Raise `best_count` to the chain's server total
   `run_totals[chain_end + 1] - run_totals[chain_start]` for each selectable
   chain, and return `best_count`.

#### Walkthrough

Example 1 sorts to `[1, 1, 2, 2, 3, 4, 5]`, which run-length encodes into
`run_values = [1, 2, 3, 4, 5]` and `run_counts = [2, 2, 1, 1, 1]`. The
enumeration scores every chain of consecutive values:

```text
chain            interior runs   singletons?   servers   best_count
[1]              -               -             2         2
[1, 2]           -               -             4         4
[1, 2, 3]        2 (two copies)  no            5         5
[1, 2, 3, 4]     2, 3            3 is single   -         5
[1, 2, 3, 4, 5]  2, 3, 4         singles       -         5
[2]              -               -             2         5
[2, 3]           -               -             3         5
[2, 3, 4]        3               single        -         5
[2, 3, 4, 5]     3, 4            singles       -         5
[3], [3, 4], [4], selectable, 1-2 servers                1-2       5
[4, 5], [5]
```

The winner is the chain [1, 2, 3] with all copies: two 1s, two 2s, one 3,
5 servers. The statement's own arrangement [2, 1, 1, 2, 3] is exactly the
construction from the derivation: climb 1, 2, 3 and come back down through
the second copies. Every chain that reaches value 4 dies because the value-3
run holds a single copy, and the circle would have to jump between 2 and 4.
The function returns 5, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, powers: List[int]) -> int:
        """Return the largest selectable multiset size for a circular network.

        Time:  O(n log n + R^2), for the sort plus every chain of runs, where
            R is the number of distinct values; each chain is judged in O(1)
            with the prefix tallies.
        Space: O(n) for the sorted copy, the run table, and the tallies.
        """
        sorted_powers = sorted(powers)
        run_values: List[int] = []
        run_counts: List[int] = []
        for value in sorted_powers:
            if run_values and run_values[-1] == value:
                run_counts[-1] += 1
            else:
                run_values.append(value)
                run_counts.append(1)

        total_runs = len(run_values)
        single_tally = [0] * (total_runs + 1)
        run_totals = [0] * (total_runs + 1)
        for run_position in range(total_runs):
            single_tally[run_position + 1] = single_tally[run_position] + (
                1 if run_counts[run_position] == 1 else 0
            )
            run_totals[run_position + 1] = (
                run_totals[run_position] + run_counts[run_position]
            )

        best_count = 1
        for chain_start in range(total_runs):
            for chain_end in range(chain_start, total_runs):
                if chain_end > chain_start and (
                    run_values[chain_end] - run_values[chain_end - 1] != 1
                ):
                    break
                interior_has_single = (
                    single_tally[chain_end] - single_tally[chain_start + 1] > 0
                )
                if not interior_has_single:
                    best_count = max(
                        best_count,
                        run_totals[chain_end + 1] - run_totals[chain_start],
                    )
        return best_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n + R^2)`

Sorting costs `O(n log n)`; the nested chain loops visit each viable chain of
runs once at constant time per chain, and there are at most `R(R+1)/2` such
chains for `R` distinct values.

##### Space Complexity: `O(n)`

The sorted copy, the run table, and the two prefix tallies are all linear in
the server count.

#### Key Insights

- The circular adjacency rule collapses to a counting rule: contiguous value
  range, full copy counts, every interior value at least twice.
- Extra copies of present values can always be inserted beside an existing
  copy, so "take everything in the range" is never wrong.
- The `break` when a value gap appears keeps the inner loop proportional to
  the chains actually examined, not to all run pairs.

### Sliding Window over Value Runs

#### Derivation

The chain enumeration still re-decides overlapping chains `O(R^2)` times, and
most of that work re-scans runs the previous chain already knew about. The
repair is the standard sliding window reduction: fix the run the window ends
on and ask how the feasible window starting point can change as the right end
advances by one run. When `window_end` advances to run `window_end`, exactly
three things can happen:

- the new run's value is more than 1 above the previous run's value: no chain
  crosses the gap, so every surviving window starts at `window_end` itself;
- the new run's value continues the chain, but the run it just made interior,
  `window_end - 1`, has only one copy: every surviving window must start above
  that starved run, and the cheapest repair is `window_start = window_end - 1`;
- otherwise the previous `window_start` still serves, because dropping runs
  from the left never fixes an interior singleton and only shrinks the count.

Each case needs only the previous window's start, so one left-to-right sweep
scores every window ending at each run:

1. Sort into `sorted_powers`, run-length encode into `run_values` and
   `run_counts`, and build the prefix total `run_totals`.
2. Sweep `window_end` over the runs, applying the three cases to maintain
   `window_start`.
3. After each step, raise `best_count` to
   `run_totals[window_end + 1] - run_totals[window_start]`.
4. Return `best_count` after the sweep.

#### Walkthrough

The run table of Example 1 is `run_values = [1, 2, 3, 4, 5]` with
`run_counts = [2, 2, 1, 1, 1]`. The sweep maintains the largest feasible
window ending at each run:

```text
window_end   run (value x count)   case                          window   servers  best_count
0            1 x2                  first run                     [1]      2        2
1            2 x2                  continues; run 0 has 2 copies [1..2]   4        4
2            3 x1                  continues; run 1 has 2 copies [1..3]   5        5
3            4 x1                  continues; run 2 has 1 copy   [3..4]   2        5
4            5 x1                  continues; run 3 has 1 copy   [4..5]   2        5
```

At `window_end = 3` the value 4 continues the chain, but the run newly interior
to the window (value 3, one copy) starves it, so the window restarts just
above that run. The best window seen anywhere in the sweep is [1..3] with 5
servers, which the function returns, matching the expected Output.

#### Solution

The code is the sweep from the walkthrough: one pass over the runs applying
the three window cases.

```python
from typing import List


class Solution:
    def solve(self, powers: List[int]) -> int:
        """Return the largest selectable multiset size for a circular network.

        Time:  O(n log n): the sort dominates; run-length encoding and the
            sweep each visit every run once.
        Space: O(n) for the sorted copy, the run table, and the prefix total.
        """
        sorted_powers = sorted(powers)
        run_values: List[int] = []
        run_counts: List[int] = []
        for value in sorted_powers:
            if run_values and run_values[-1] == value:
                run_counts[-1] += 1
            else:
                run_values.append(value)
                run_counts.append(1)

        total_runs = len(run_values)
        run_totals = [0] * (total_runs + 1)
        for run_position in range(total_runs):
            run_totals[run_position + 1] = (
                run_totals[run_position] + run_counts[run_position]
            )

        best_count = 1
        window_start = 0
        for window_end in range(total_runs):
            if window_end > 0 and (
                run_values[window_end] - run_values[window_end - 1] != 1
            ):
                window_start = window_end
            elif window_end > 0 and run_counts[window_end - 1] == 1:
                window_start = window_end - 1
            best_count = max(
                best_count, run_totals[window_end + 1] - run_totals[window_start]
            )
        return best_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates; run-length encoding and the sweep each touch every run a
constant number of times.

##### Space Complexity: `O(n)`

The sorted copy, the run table, and the prefix total are linear in the server
count; the window itself is just two indices.

#### Key Insights

- Fixing the window's right end turns "which chains are feasible" into a
  three-way case analysis on the run just appended, which is what removes the
  second loop.
- The restart `window_start = window_end - 1` (rather than erasing the whole
  window) is safe because a singleton run disqualifies only windows that
  contain it as interior, and windows ending at later runs are scored on
  their own sweep steps.
- The window start never moves right past the current end, so the sweep is
  linear even though the window jumps.

## Comparison of Solutions

### Time Complexity

- **Bitmask Subset Enumeration**: `O(2^n × n × n!)` - every subset is built and
  every circular order of it tested.
- **Sorted Window Enumeration**: `O(n log n + R^2)` - sorting plus every chain
  of runs at constant time per chain.
- **Sliding Window over Value Runs**: `O(n log n)` - sorting plus one linear
  sweep over the runs.

### Space Complexity

- **Bitmask Subset Enumeration**: `O(n)` - the current subset and order.
- **Sorted Window Enumeration**: `O(n)` - sorted copy, run table, two tallies.
- **Sliding Window over Value Runs**: `O(n)` - sorted copy, run table, one
  prefix total.

### Trade-offs

- **Bitmask Subset Enumeration**: derives directly from the statement and
  doubles as a correctness oracle, but its factorial layer caps it at roughly
  a dozen servers.
- **Sorted Window Enumeration**: rests the whole problem on one counting rule
  that is easy to re-derive and to argue about, at the cost of the nested
  chain loops.
- **Sliding Window over Value Runs**: optimal and a linear scan after the
  sort, but the three window cases are subtler to justify than the chain
  rule it abbreviates.

### When to Use Each

- **Bitmask Subset Enumeration**: for tiny inputs or while debugging, where
  its verdicts define the right answer.
- **Sorted Window Enumeration**: the recommended interview middle ground: the
  counting rule is the insight interviewers want stated, and the code stays
  short.
- **Sliding Window over Value Runs**: when the distinct-value count is large
  enough that the quadratic chain enumeration matters, which the constraint
  `n` up to `2 * 10^5` invites.

### Optimization Notes

- Sorting before any window or chain work is what turns "subset of servers"
  into "range of values"; skip it and every rule above becomes a contiguity
  test over arbitrary positions.
- The `n!` in the brute force is a multiset upper bound; inputs with many
  repeated powers permute far less, but never rely on that in the worst case.
- All three approaches return 1 for a single server: a circle of one node has
  only the wrap pair of the node with itself, a difference of 0.

