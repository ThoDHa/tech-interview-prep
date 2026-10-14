# [Maximum System Memory Capacity](https://www.fastprep.io/problems/amazon-maximum-capacity)

**Easy** | **NN minutes** | **Sorting, Greedy**

Amazon is optimizing the capacity of a cloud system with n servers. The memory capacity of the i-th server is memory[i].

A system uses an even number of servers. If it uses 2x servers, exactly x are primary servers and the other x are backup servers. For every primary server P, it must be paired with a distinct backup server B whose memory capacity is at least that of P.

The system memory capacity is the sum of the memory capacities of all primary servers. You may leave servers unused. Given memory, return the maximum system memory capacity that can be formed.

Complete maximumCapacity, which receives the integer array memory and returns the maximum capacity as a long.

## Examples

### Example 1

**Input:** `memory = [1, 2, 1, 2]`

**Output:** `3`

**Explanation:** Here, we have 4 servers [serverA, serverB, serverC, serverD] having memory sizes as [1, 2, 1, 2].

We can choose serverA and serverB as primary servers, and serverC and serverD as their respective backup.
The conditions hold true since memory[serverC] ≥ memory[serverA] and memory[serverD] ≥ memory[serverB].
Hence, the maximum system memory capacity is 3.

### Example 2

**Input:** `memory = [1, 2, 1]`

**Output:** `1`

**Explanation:** Here, we have 3 servers [serverA, serverB, serverC] having memory sizes as [1, 2, 1].

We can choose serverA as a primary server, and serverB as its respective backup server.
The conditions hold true since memory[serverB] ≥ memory[serverA].
Hence, the maximum system memory capacity is 1.

### Example 3

**Input:** `memory = [2, 4, 3, 1, 2]`

**Output:** `5`

**Explanation:** $23

## Constraints

- `2 ≤ n ≤ 2 * 10^5`
- `1 ≤ size[i] ≤ 10^9`

## Solutions

### Brute Force over Subsets

#### Derivation

The most literal reading enumerates systems directly. Every even-size subset of servers is a candidate system; for each candidate, decide whether its servers can be split into primary-backup pairs, and if so compute the primary sum. The subset-and-split with the largest sum is the answer. The feasibility check must respect the one freedom the statement grants: a chosen set is legal if *some* assignment of its servers into primaries and backups works, so the split itself has to be enumerated, not assumed:

1. For every `pair_count` from `1` to `server_count // 2`, enumerate every
   `chosen` subset of `2 * pair_count` servers with
   `itertools.combinations`.
2. For every way to pick the `pair_count` primaries from `chosen`
   (`primary_set`), derive the backups as the multiset difference
   `backup_counts = Counter(chosen) - Counter(primary_set)`.
3. The assignment exists exactly when the backups can be matched against
   the primaries one to one: sort both descending and require every
   aligned `backup >= primary`; one primary with no big-enough backup
   dooms the assignment.
4. When the assignment exists, add the primary sum to the running
   `best_capacity`.
5. Return `best_capacity`.

#### Walkthrough

Trace the enumeration on Example 3: `memory = [2, 4, 3, 1, 2]`, `server_count = 5`, so `pair_count` runs over `1` and `2`. For `pair_count = 1` the best legal single pair is primary `3` backed by the `4`, capacity `3` (a primary of `4` itself has no bigger backup). For `pair_count = 2`, the promising size-4 subsets and their best splits are:

```text
chosen [4,3,2,2]   primaries [4,3] backups [2,2] -> 2 >= 4 fails
                   primaries [4,2] backups [3,2] -> 3 >= 4 fails
                   primaries [3,2] backups [4,2] -> 4 >= 3, 2 >= 2  capacity 3+2 = 5
                   primaries [2,2] backups [4,3] -> 4 >= 2, 3 >= 2  capacity 2+2 = 4
chosen [4,3,2,1]   best split primaries [3,1] backups [4,2] -> capacity 3+1 = 4
chosen [4,2,2,1]   best split capacity 2+1 = 3
chosen [3,2,2,1]   best split capacity 2+1 = 3
```

The winning line is `chosen = [4, 3, 2, 2]` with primaries `{3, 2}` backed up by `{4, 2}`: capacity `5`. No other subset or split beats it, so `best_capacity = 5`, matching the expected Output for Example 3. On Example 1, `memory = [1, 2, 1, 2]`, the split primaries `{2, 1}` backups `{2, 1}` gives capacity `3`; on Example 2, `memory = [1, 2, 1]`, only single pairs fit (odd server count) and the best is primary `1` backed by `2`, capacity `1`.

#### Solution

The code is the enumeration with the multiset-difference split and the aligned descending check.

```python
from collections import Counter
from itertools import combinations
from typing import List


class Solution:
    def maximumCapacity(self, memory: List[int]) -> int:
        server_count = len(memory)
        best_capacity = 0

        for pair_count in range(1, server_count // 2 + 1):
            for chosen in combinations(memory, 2 * pair_count):
                for primary_set in combinations(chosen, pair_count):
                    backup_counts = Counter(chosen) - Counter(primary_set)
                    primaries = sorted(primary_set, reverse=True)
                    backups_descending = sorted(
                        backup_counts.elements(), reverse=True
                    )
                    if all(
                        backup >= primary
                        for backup, primary in zip(backups_descending, primaries)
                    ):
                        best_capacity = max(best_capacity, sum(primaries))

        return best_capacity
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(5^n × n log n)`

Every subset is combined with every split of itself; summed over subset sizes, the number of such pairs grows like `5^n` (choosing `k` of `n` servers and then `k` primaries among the `2k` chosen peaks near `k = n/5`), and each pair is sorted and checked in `O(n log n)`.

##### Space Complexity: `O(n)`

The sorted primary and backup lists of the current candidate hold at most `n` servers.

#### Key Insights

- Feasibility is a property of the chosen set, not of one pairing: the correct check enumerates which servers become primaries, then asks whether the remaining backups cover them in aligned descending order.
- The aligned descending check is the same greedy insight the optimal solution automates: the strongest backup should cover the strongest primary.
- Correct but explosive: with `n` up to `2 * 10^5`, the exponential count of subset-and-split pairs (about `5^n` at the worst subset size) is unthinkable, which is what motivates the polynomial solutions below.

### Bottom-Up Balance DP

#### Derivation

The brute force re-decides the same subproblems: which servers were chosen so far, and how many of them are primaries versus backups. Process the servers in descending order and those two facts collapse into one number. Strong servers make the best backups (they cover anything), so a descending scan faces, server by server, exactly three choices: skip the server, reserve it as a backup, or take it as a primary and immediately collect its size into the capacity. The only state the future needs is how many more reservations than collections have been made; call it the `balance`. A final state is a system when the balance is exactly zero and every reservation was matched by a collection:

1. Sort `memory` descending into `sorted_sizes`.
2. Let `best_sum[balance]` be the maximum primary sum achievable using a
   prefix of `sorted_sizes` that leaves `balance` unmatched backups, with
   negative infinity where the balance is unreachable. Start with
   `best_sum[0] = 0`.
3. For each `size` in `sorted_sizes`, copy `best_sum` (the skip choice)
   and then, from every reachable `balance`, either reserve the server as
   a backup (`balance + 1`, sum unchanged) or pair it as a primary with a
   previously reserved backup (`balance - 1`, sum increased by `size`).
4. The answer is the largest finite value in `best_sum` after the last
   server (balance `0` is among them and is where the full system lands).

The descending order is what makes the three choices safe: a server is compared only against already-reserved backups, which are all at least its size, so a primary taken now is always covered.

#### Walkthrough

Trace the table over Example 3: `memory = [2, 4, 3, 1, 2]`, sorted descending to `sorted_sizes = [4, 3, 2, 2, 1]`. Each row shows the finite entries of `best_sum` after the server named on the left:

```text
start      best_sum[0] = 0
after 4    b0 = 0                     b1 = 0          (reserve 4)
after 3    b0 = 3                     b1 = 0          (pair 3 with the 4)
after 2    b0 = 3                     b1 = 3,  b2 = 0 (reserve 2)
after 2    b0 = 5                     b1 = 3,  b2 = 3 (pair second 2: 3+2)
after 1    b0 = 5    b1 = 5,  b2 = 3,  b3 = 3   (skip 1; reserve 1 -> 5)
```

Read the winning path at balance `0`: `4` reserved as backup, `3` taken as primary (`3`), first `2` reserved as backup, second `2` taken as primary (`3 + 2 = 5`), final `1` skipped. The largest entry in the final row is `5`, matching the expected Output for Example 3. On Example 1, `memory = [1, 2, 1, 2]`, the same table walks `2, 2, 1, 1` and reaches `3` (reserve the first `2`, collect the second, reserve the first `1`, collect the second, `2 + 1 = 3`); on Example 2, `memory = [1, 2, 1]`, the walk reaches `1` (reserve the `2`, collect one `1`, the second `1` only deepens the balance).

#### Solution

The code is the descending scan with the three-way choice per server.

```python
from typing import List


class Solution:
    def maximumCapacity(self, memory: List[int]) -> int:
        sorted_sizes = sorted(memory, reverse=True)
        positions = len(sorted_sizes)

        # best_sum[balance]: best primary sum over a descending prefix that
        # holds `balance` more backup reservations than collected primaries.
        # Any leftover reservation is worthless, so the final answer is the
        # maximum over all balances.
        unmatched = float("-inf")
        best_sum = [unmatched] * (positions + 1)
        best_sum[0] = 0

        for size in sorted_sizes:
            updated = best_sum[:]
            for balance in range(positions + 1):
                current_sum = best_sum[balance]
                if current_sum == unmatched:
                    continue
                if current_sum > updated[balance + 1]:
                    updated[balance + 1] = current_sum
                if balance >= 1 and current_sum + size > updated[balance - 1]:
                    updated[balance - 1] = current_sum + size
            best_sum = updated

        return int(max(best_sum))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

One table pass per server, each sweeping every balance from `0` to `n`.

##### Space Complexity: `O(n)`

The `best_sum` row holds one entry per balance, plus the copied row during each update.

#### Key Insights

- The descending order collapses subset choice and assignment into one scan: every reserved backup is at least as large as every primary collected later, so the coverage condition holds by construction.
- The balance is the only history the future needs; the capacity rides alongside the state instead of being part of it.
- A server left unmatched at the end (odd leftovers, skipped servers) is simply never collected; the answer reads the maximum over all final balances because unmatched reservations carry no capacity, so some balance-`0` state always matches any partial state's sum.

### Adjacent Pairing on Descending Sort

#### Derivation

The balance DP still sweeps `O(n)` balances. Sort descending and read the structure of the optimum instead. Two rules about a chosen set of `2x` servers do the work. First, the pairing rule from the brute force check: matching the strongest backups against the strongest primaries in order is the most generous assignment, so the set is feasible exactly when its `x`-th largest server (the weakest primary in that assignment) is covered by its `(x+1)`-th largest server (the strongest backup). In particular the adjacent pairing (position 1 backing position 2, position 3 backing position 4, and so on) is legal on any chosen set, because each odd position is at least the even position after it. Second, the value rule: in any legal pair the primary is the pair's minimum (the backup is at least the primary), so the capacity of a chosen set is the sum of its `x` pair minima, and the pairing that maximizes that sum is the adjacent one: for four sorted values `a ≥ b ≥ c ≥ d`, the crossed pairs `(a, c), (b, d)` have minima `c + d` while the adjacent pairs `(a, b), (c, d)` have minima `b + d ≥ c + d`, so uncrossing steps transform any pairing into the adjacent one without losing capacity (the set `[4, 3, 2, 2]` shows the shape: primaries `{3, 2}` against backups `{4, 2}` reach `5`, while pushing the primaries all the way down to `{2, 2}` reaches only `4`). Together the two rules turn the answer into a scan over the sorted list: the capacity of the best system using `2x` servers is the sum of the second, fourth, ..., `2x`-th largest servers of the whole array, because

1. the `k`-th largest minimum over all pairings of any server multiset is
   at most the `2k`-th largest server overall (every pairing has a `k`-th
   pair minimum, and no `k` pair minima can all exceed the `2k`-th
   largest value), and
2. the adjacent pairing (positions `1-2`, `3-4`, ... of the descending
   list) achieves that bound for every `k` at once.

So every even-position value belongs to some optimal system, and no legal system exceeds their sum. The key inequality: the sum of the even positions among any `2x` chosen servers is at most the sum of the `2x` largest servers' even positions, and that in turn cannot beat the stride sum over the whole sorted array:

1. Sort `memory` descending into `sorted_sizes`.
2. Walk `pair_start` over the odd positions `1, 3, 5, ...` (zero-indexed)
   and add `sorted_sizes[pair_start]` to `best_capacity`.
3. Return `best_capacity`.

#### Walkthrough

Trace the stride on Example 1: `memory = [1, 2, 1, 2]`, sorted descending to `sorted_sizes = [2, 2, 1, 1]`:

```text
pair_start 1   sorted_sizes[1] = 2   best_capacity = 2
pair_start 3   sorted_sizes[3] = 1   best_capacity = 3
```

The pairs are `(2, 2)` and `(1, 1)`, each backup at least its primary, and the capacity `3` matches the expected Output for Example 1. On Example 2, `memory = [1, 2, 1]` sorts to `[2, 1, 1]`: the only odd position below the length is `1`, `best_capacity = 1`, and the leftover third server stays unused. On Example 3, `memory = [2, 4, 3, 1, 2]` sorts to `[4, 3, 2, 2, 1]`: the stride collects `sorted_sizes[1] = 3` and `sorted_sizes[3] = 2`, capacity `5`, matching the expected Output for Example 3.

#### Solution

The code is the descending sort and the stride over odd positions.

```python
from typing import List


class Solution:
    def maximumCapacity(self, memory: List[int]) -> int:
        sorted_sizes = sorted(memory, reverse=True)

        best_capacity = 0
        for pair_start in range(1, len(sorted_sizes), 2):
            best_capacity += sorted_sizes[pair_start]
        return best_capacity
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

One sort dominates; the stride is a single pass over half the positions.

##### Space Complexity: `O(n)`

The descending copy of the memory array.

#### Key Insights

- The capacity of the best system is the sum of the even positions (1-indexed) of the descending sort: each even position is the minimum of its adjacent pair, and the adjacent pairing maximizes every pair minimum simultaneously, which is what maximizes the sum of the minima.
- No stopping rule is needed: adding the next even position never lowers the capacity (sizes are positive), and it stays legal because adjacent pairing keeps backups ahead of primaries all the way down.
- Compare with the failed greedy of pairing neighbors with a feasibility break: the stride shows the break was never needed, because in the descending order every adjacent pair is automatically feasible.

## Comparison of Solutions

### Time Complexity

- **Brute Force over Subsets**: `O(5^n × n log n)` - every subset combined with every split of itself, each sorted and checked.
- **Bottom-Up Balance DP**: `O(n^2)` - one balance sweep per server.
- **Adjacent Pairing on Descending Sort**: `O(n log n)` - one sort plus a stride over half the positions.

### Space Complexity

- **Brute Force over Subsets**: `O(n)` - the sorted primary and backup lists of the current candidate.
- **Bottom-Up Balance DP**: `O(n)` - one table row of balances.
- **Adjacent Pairing on Descending Sort**: `O(n)` - the descending copy of the memory array.

### Trade-offs

- The subset enumeration is the ground truth: it defines the optimum by trying every subset and every split, and it is the oracle the faster solutions were checked against on small inputs.
- The balance DP keeps the DP honest about the assignment freedom (primaries and backups interleave as reservations and collections) at a quadratic price, and it generalizes to variants where the pairing rule changes.
- The descending sort reads the whole optimum off one ordering, but its correctness rests on the two structural facts (strongest-backup-first matching, the even-position stride), which are the part an interviewer will probe.

### When to Use Each

- **Brute Force over Subsets**: for tiny inputs and as the correctness oracle for the other two.
- **Bottom-Up Balance DP**: when the pairing rule is non-standard (for example backups strictly larger than primaries) and the sorted-order shortcut no longer applies.
- **Adjacent Pairing on Descending Sort** (Recommended): always, in interviews and in the OA: linearithmic time, two lines of logic, and the pairing argument is one sentence.

### Optimization Notes

- The stride needs the descending order: ascending would sum the larger half of each pair instead of the smaller one, overcounting the capacity.
- In fixed-width languages the return is a `long` (the statement says so): with `n` up to `2 * 10^5` and sizes up to `10^9`, the capacity exceeds 32 bits; Python integers do not overflow.
- The sum of even positions equals the sum of all values minus the sum of odd positions, so an equivalent implementation accumulates the discarded half and subtracts; the direct stride is clearer and avoids the subtraction.
