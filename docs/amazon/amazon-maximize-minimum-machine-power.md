# [Maximize Minimum Machine Power](https://www.fastprep.io/problems/amazon-maximize-minimum-machine-power)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given an integer array sources, where sources[i] is the amount of power available from the i-th power source, and an integer n representing the number of machines.

Each machine must receive power from exactly one source. A source may power multiple machines, but the total power assigned from that source cannot exceed its capacity.

Return the maximum possible value of the minimum power assigned to any machine.

## Examples

### Example 1

**Input:** `sources = [5, 8, 6]`, `n = 4`

**Output:** `4`

**Explanation:** A minimum assignment of 4 is possible: the sources can support 1 + 2 + 1 = 4 machines with at least 4 power each. A minimum of 5 would support only 1 + 1 + 1 = 3 machines.

### Example 2

**Input:** `sources = [10, 10]`, `n = 3`

**Output:** `5`

**Explanation:** Each source can power two machines with 5 power each, so three machines can be powered. A minimum of 6 would allow only two machines total.

## Constraints

- `1 <= sources.length`
- `1 <= n`
- `sources[i] is a non-negative integer power capacity.`

## Solutions

### Linear Scan on the Candidate Minimum

#### Derivation

The most literal reading turns the question around: instead of assigning machines to sources directly, pick a candidate minimum power `target` and ask whether every one of the `n` machines can receive at least that much. With `target` fixed, a source of capacity `power` can serve exactly `power // target` machines at `target` power each (and leftover power below `target` is waste), so the sources as a whole can support `sum(power // target for power in sources)` machines. If that count reaches `n`, the target is achievable, because machines are interchangeable and can be dealt out to any source with remaining capacity. No machine can receive more than the largest capacity, so the candidates worth trying run from `max(sources)` down to `1`:

1. Loop `target` over `range(max(sources), 0, -1)`, from the largest capacity down to 1.
2. For each `target`, compute `supported = sum(power // target for power in sources)`.
3. Return `target` the first time `supported >= n`.
4. If the loop exhausts, even one power per machine is impossible, so return `0`.

#### Walkthrough

Example 1: `sources = [5, 8, 6]`, `n = 4`. Each line is one candidate tested with the capacity arithmetic `power // target`:

```text
target = 6   supported = 5//6 + 8//6 + 6//6 = 0 + 1 + 1 = 2   < 4, keep scanning
target = 5   supported = 5//5 + 8//5 + 6//5 = 1 + 1 + 1 = 3   < 4, keep scanning
target = 4   supported = 5//4 + 8//4 + 6//4 = 1 + 2 + 1 = 4   >= 4, return 4
```

The scan stops at the first candidate that supports all four machines, which is the expected Output `4`. (Example 2 runs the same check down to `target = 5`, where `10//5 + 10//5 = 4 >= 3`.)

#### Solution

The code is the walkthrough's downward scan with the capacity arithmetic inline:

```python
from typing import List


class Solution:
    def solve(self, sources: List[int], n: int) -> int:
        for target in range(max(sources), 0, -1):
            supported = sum(power // target for power in sources)
            if supported >= n:
                return target
        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × P)`

Where `m` is the number of sources and `P = max(sources)`: up to `P` candidate targets are each checked with one pass over the `m` sources.

##### Space Complexity: `O(1)`

Only the running `supported` count is stored.

#### Key Insights

- Reformulating "assign machines" as "test a minimum" replaces a combinatorial assignment problem with an arithmetic count, `power // target` machines per source.
- `target = 0` needs no test: every machine trivially receives at least zero, so `0` is the fallback answer whenever every positive candidate fails.
- The approach repeats enormous work: lowering the target by one rarely changes most `power // target` quotients, which is exactly the waste the next approach removes.

### Binary Search on the Answer

#### Derivation

The linear scan tests every integer between `1` and `max(sources)`, but the feasibility predicate is monotone: lowering `target` never lowers any quotient, because `power // target` is non-increasing in `target`, so the number of supported machines only grows. That means the candidates split into a feasible tail (every small target) and an infeasible head (every large target), and the answer is the boundary between them. A boundary in a monotone predicate is what [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) finds in logarithmic probes:

1. Keep the same feasibility question as a helper: `machines_supported(target)` returns `sum(power // target for power in sources)`.
2. Binary search `low = 1` to `high = max(sources)` on the largest feasible `target`.
3. When `machines_supported(mid) >= n`, `mid` works and larger candidates may too:
   record `best = mid` and move `low = mid + 1`.
4. Otherwise `mid` is too ambitious: move `high = mid - 1`.
5. When the window empties, `best` holds the largest feasible target, or the
   initial `0` when no positive target supports all `n` machines.

#### Walkthrough

Example 1: `sources = [5, 8, 6]`, `n = 4`. The window starts at `low = 1, high = 8`; each line is one probe with `mid = (low + high) // 2`:

```text
low = 1, high = 8, best = 0
mid = 4   supported = 1 + 2 + 1 = 4   >= 4   best = 4, low = 5
mid = 6   supported = 0 + 1 + 1 = 2   < 4    high = 5
mid = 5   supported = 1 + 1 + 1 = 3   < 4    high = 4
low (5) > high (4)   loop ends, return best = 4
```

Three probes replace the full scan and land on the same boundary: `4` is feasible while `5` is not, so the return value is `4`, the expected Output.

#### Solution

The code is the monotone probe from the walkthrough, with the feasibility count factored into `machines_supported`:

```python
from typing import List


class Solution:
    def solve(self, sources: List[int], n: int) -> int:
        def machines_supported(target: int) -> int:
            return sum(power // target for power in sources)

        best = 0
        low, high = 1, max(sources)
        while low <= high:
            mid = (low + high) // 2
            if machines_supported(mid) >= n:
                best = mid
                low = mid + 1
            else:
                high = mid - 1
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × log P)`

Where `P = max(sources)`: the window halves each round, and each of the `O(log P)` rounds makes one `O(m)` pass over the sources.

##### Space Complexity: `O(1)`

Only `low`, `high`, `mid`, and `best` are stored.

#### Key Insights

- Monotonicity is the whole argument: `power // target` never increases as `target` grows, so feasibility flips exactly once and binary search applies to a non-sorted value domain.
- Seeding `best = 0` and `low = 1` folds the fallback into the search: when even `target = 1` fails (total power below the machine count), the loop never records anything and `0` is returned.
- `max(sources)` is a tight upper bound because any `target` above it gives every quotient zero.
- The helper returns the full count, but it could stop early once the running total reaches `n`; on inputs where `n` is small that shaves the constant, not the asymptotics.

## Comparison of Solutions

### Time Complexity

- **Linear Scan on the Candidate Minimum**: `O(m × P)` - every candidate from `max(sources)` down to `1` is tested with one pass over the sources.
- **Binary Search on the Answer**: `O(m × log P)` - the candidate window halves each round, so only `O(log P)` passes are made.

### Space Complexity

- **Linear Scan on the Candidate Minimum**: `O(1)` - a single running count.
- **Binary Search on the Answer**: `O(1)` - the search window bounds plus the recorded best.

### Trade-offs

- **Linear Scan on the Candidate Minimum**: impossible to get wrong and trivial to debug, but its cost scales with the magnitude of the capacities, so large power values (say `10^9`) make it unusable.
- **Binary Search on the Answer**: logarithmic in the capacity range regardless of magnitude, at the price of arguing monotonicity before writing a line of code.

### When to Use Each

- **Linear Scan on the Candidate Minimum**: tiny capacity ranges or a first pass to generate expected outputs for testing.
- **Binary Search on the Answer**: the interview answer, and the only one that survives the constraint sizes typical of the "maximize the minimum" family.

### Optimization Notes

- This page is the standard template for every "maximize the minimum / minimize the maximum" problem: guess the answer, write an `O(m)` feasibility check, then binary search the guess.
- The feasibility helper counts all sources every time; an early exit once the running total reaches `n` is a cheap constant-factor win.
- Watch the boundary contract in the loop: recording `best` before moving `low = mid + 1` (and never returning `mid` directly) is what keeps the largest feasible value across the final iteration.
