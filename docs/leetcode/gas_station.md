# [Gas Station](https://leetcode.com/problems/gas-station/)

**Medium** | **25 minutes** | **Array, Greedy**

**Pattern:** [Greedy](../patterns/greedy_core/intuition.md)

**Algorithm:** [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm) · [Prefix sum](https://en.wikipedia.org/wiki/Prefix_sum) · [Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer)

**Practice:** [`practice/gas_station/solution.py`](../../practice/gas_station/solution.py)

There are `n` gas stations along a circular route. You are given two integer arrays `gas` and `cost` where:

* `gas[i]` is the amount of gas at the `ith` station.
* `cost[i]` is the amount of gas needed to travel from the `ith` station to the `(i + 1)th` station. (The last station is connected to the first station)

You have a car that can store an unlimited amount of gas, but you begin the journey with an empty tank at one of the gas stations.

Return the starting gas station's index such that you can travel around the circuit once in the clockwise direction. If it's impossible, then return `-1`.

It's guaranteed that at most one solution exists.

## Examples

### Example 1

**Input:** `gas = [1,2,3,4], cost = [2,2,4,1]`

**Output:** `3`

**Explanation:** Start at station 3 and fill up with `gas[3] = 4`, so tank = 4.
Travel from station 3 to station 0, spending `cost[3] = 1`, then fill `gas[0] = 1`, so tank = 4 - 1 + 1 = 4.
Travel from station 0 to station 1, spending `cost[0] = 2`, then fill `gas[1] = 2`, so tank = 4 - 2 + 2 = 4.
Travel from station 1 to station 2, spending `cost[1] = 2`, then fill `gas[2] = 3`, so tank = 4 - 2 + 3 = 5.
Travel from station 2 back to station 3, spending `cost[2] = 4`, so tank = 5 - 4 = 1.
The circuit is complete, so return 3.

### Example 2

**Input:** `gas = [1,2,3], cost = [2,3,2]`

**Output:** `-1`

**Explanation:** You cannot start at station 0 or 1 because neither has enough gas to travel to the next station.
If you start at station 2, fill `gas[2] = 3`, so tank = 3.
Travel from station 2 to station 0, spending `cost[2] = 2`, then fill `gas[0] = 1`, so tank = 3 - 2 + 1 = 2.
Travel from station 0 to station 1, spending `cost[0] = 2`, then fill `gas[1] = 2`, so tank = 2 - 2 + 2 = 2.
To travel from station 1 to station 2, you need `cost[1] = 3` gas, but the tank only has 2.
So no starting station can complete the circuit, and the answer is -1.

## Constraints

- `1 <= gas.length == cost.length <= 100000`
- `0 <= gas[i], cost[i] <= 1000`

## Deriving the Solution

Every leg of the route has a net gain `gas[i] - cost[i]`, so the journey is a circular walk over those gains that must never let the running total dip below zero. Every solution below searches for a rotation of the gain sequence whose partial sums all stay non-negative; they differ in how many rotations they actually examine.

1. **Start literal.** Try every start and simulate the full lap, resetting the
   tank per start. The guarantee that at most one start works even makes the
   search stop at the first success. Correct, at `O(n^2)`: see
   [Brute Force](#brute-force).
2. **Stop re-walking failed starts.** When a walk from `start` dies at station
   `k`, the skip argument retires `start` through `k` in one stroke: none of
   them can pass `k` either. The candidate walks never overlap, so the whole
   search is amortized `O(n)`: see
   [Early-Exit Simulation](#early-exit-simulation).
3. **Run one lap, not many.** The Greedy keeps one tank, resets it on every
   deficit, and banks the total in parallel: if the total is non-negative the
   surviving candidate is the answer, otherwise no start works. One pass,
   `O(1)` space: see [Greedy](#greedy).
4. **Name the start by the shape of the sums.** Prefix sums turn "the tank
   never dips" into a statement about the deepest point of the cumulative
   curve: the rotation beginning just after the deepest prefix is the only
   candidate, and it works exactly when the total is non-negative: see
   [Prefix Sum](#prefix-sum).

## Solutions

### Brute Force

#### Derivation

The most literal reading tries every candidate start and simulates a full lap: fill up at the start, drive leg by leg around the circle, and fail the candidate the moment the tank would go negative. Since a lap visits every station exactly once, the tank walk is `n` additions per candidate:

1. For each `start` in `0 .. n - 1`:
2. Walk `offset` from `0` to `n - 1`, reading station
   `(start + offset) % n`, and add `gas[i] - cost[i]` to `tank`.
3. If `tank` ever drops below `0`, abandon this start.
4. If the walk survives all `n` legs, return `start`.
5. If every start fails, return `-1`.

#### Walkthrough

Trace every start on Example 2: `gas = [1, 2, 3]`, `cost = [2, 3, 2]`, whose net gains are `[-1, -1, 1]`. Each line shows the running `tank` after each leg, indexed by the station just visited:

```text
net    = [-1, -1, 1]
start = 0    tank walk: 0: -1    negative at 0 -> abandon
start = 1    tank walk: 1: -1    negative at 1 -> abandon
start = 2    tank walk: 2: 1;  0: 0;  1: -1    negative at 1 -> abandon
-> -1
```

Start `2` gets furthest: it wraps through `0` at tank `0` and dies entering `1`, the station whose `cost` exceeds everything the circle can supply. No start survives, so the function returns `-1`, matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's candidate loop: simulate a lap per start, abandon on the first negative tank.

```python
from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        n = len(gas)
        for start in range(n):
            tank = 0
            ok = True
            for offset in range(n):
                i = (start + offset) % n
                tank += gas[i] - cost[i]
                if tank < 0:
                    ok = False
                    break
            if ok:
                return start
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` candidates walks up to `n` legs; a failing candidate stops at its first deficit, but the worst case (a solution far into the array, or none at all with late failures) still walks most of the circle per candidate.

##### Space Complexity: `O(1)`

One `tank` integer and the loop counters, regardless of input length.

#### Key Insights

- The modulo read `(start + offset) % n` is the whole circular machinery; no
  array duplication or rotation is needed.
- A leg's identity is what matters, not the fuel amounts themselves: only
  `gas[i] - cost[i]` ever enters the tank arithmetic.
- The waste is overlap: candidate walks replay legs their failed predecessors
  already priced, which the next solution refuses to do.

### Early-Exit Simulation

#### Derivation

The Brute Force's candidate walks overlap heavily, and the overlap has structure. When a walk from `start` survives stations `start, start + 1, ..., k - 1` and dies entering `k` (the first negative tank), no station in `start + 1, ..., k` can complete the circuit either: any of them, call it `s`, would reach `k` with tank `sum(net[s..k])`, which equals `sum(net[start..k]) - sum(net[start..s-1])`, a negative total minus a non-negative prefix, hence negative. So one failed walk retires an entire range, and the next candidate is `k + 1`. The walks issued this way never overlap, and together they cover the circle at most once:

1. Keep `start = 0` as the current candidate.
2. Simulate the walk from `start` exactly as the Brute Force does.
3. If the walk completes, return `start`.
4. If the walk dies entering station `k` without wrapping, every station from
   `start` through `k` is disqualified: set `start = k + 1`.
5. If the walk wraps past the array end and still fails, the disqualified
   range covers the entire circle: return `-1`.

#### Walkthrough

Trace the skip chain on Example 2: `gas = [1, 2, 3]`, `cost = [2, 3, 2]`, net gains `[-1, -1, 1]`:

```text
net    = [-1, -1, 1]
start = 0    tank walk: 0: -1    dies at 0, stations 0..0 all fail -> next start = 1
start = 1    tank walk: 1: -1    dies at 1, stations 1..1 all fail -> next start = 2
start = 2    tank walk: 2: 1;  0: 0;  1: -1    dies at 1 after wrapping: every station disqualified -> return -1
```

Each failed walk retires its whole dying prefix, so the three candidates partition the circle instead of replaying it. The last walk wraps (station `2` through `0` to `1`) and still fails, which means every station is retired at once, and the function returns `-1`, matching the expected Output for Example 2.

#### Solution

The code is the Brute Force's walk with the skip rule replacing the `+1` candidate advance.

```python
from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        n = len(gas)
        start = 0
        while start < n:
            tank = 0
            offset = 0
            while offset < n:
                i = (start + offset) % n
                tank += gas[i] - cost[i]
                if tank < 0:
                    break
                offset += 1
            if offset == n:
                return start
            fail_at = start + offset
            if fail_at >= n:
                # The walk wrapped past the array end and still failed: every
                # station from `start` around to `fail_at` is disqualified,
                # which covers the whole circle.
                return -1
            start = fail_at + 1
        return -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Successful segments of failed walks never overlap: each failed walk retires `offset + 1` stations and every station is retired at most once across the whole search, so the total walk length is `O(n)` in aggregate.

##### Space Complexity: `O(1)`

One `tank`, one `offset`, and the candidate index.

#### Key Insights

- The skip argument is a partial-sum statement in disguise: negative total
  minus non-negative prefix is negative, which is why the dying prefix dies
  for every member.
- Detecting the wrap (`fail_at >= n` before folding) is what keeps the search
  from cycling forever on unsolvable inputs: a wrapped failure disqualifies
  the entire circle at once.
- This is the Greedy below with the total bookkeeping stripped out; the two
  reach the same candidate sequence by different bookkeeping.

### Greedy

#### Derivation

The Early-Exit walk keeps restarting its tank at each new candidate. The Greedy observes that the restarts can be fused into one lap: walk the circle once, keep a local `tank` that resets at every deficit, and accumulate `total` in parallel without ever resetting it. The reset rule is the Early-Exit skip in motion: when the tank dips below `0` at station `i`, the skip argument retires everything up to `i`, so the only viable candidates start later, at `i + 1`. One subtlety carries the correctness: the fused pass only certifies candidates against the suffix it walks *after* the last reset, so a full-lap certification needs the classic theorem, that a solution exists exactly when `total >= 0`, and when it exists it is the survivor of the resets:

1. Sweep `i` from `0` to `n - 1`, adding `gas[i] - cost[i]` to both `tank`
   and `total`.
2. When `tank < 0`, set `start = i + 1` and reset `tank = 0`.
3. After the sweep, return `start` when `total >= 0`, otherwise `-1`.

#### Invariant

After processing station `i`, the current `start` is the only candidate for a circuit beginning in `0..i + 1`, and `tank` holds the sum of net gains over `start..i`:

$$ \text{tank} = \sum_{k=\text{start}}^{i} net[k] \;\ge 0, \qquad \text{all stations } j \le i \text{ with } j \ne \text{start} \text{ are disqualified} $$

```text
tank    = sum of net gains from start through the current station i
tank    >= 0 at every step (reset otherwise)
start   = the only station in 0..i+1 not yet disqualified
```

Each branch preserves it. The accumulate branch keeps `tank` non-negative, so `start` still walks a viable prefix. The reset branch applies the skip argument: `tank < 0` at `i` means every station from the old `start` through `i` fails, so `i + 1` becomes the only live candidate and the empty `tank` matches its fresh prefix. At loop exit the disqualification covers everything except `start`; if `total >= 0`, the classic theorem certifies `start` completes the circuit, and if `total < 0` no rotation can have all non-negative partial sums because every rotation's partial sums add up to `total`.

#### Walkthrough

Trace Example 1: `gas = [1, 2, 3, 4]`, `cost = [2, 2, 4, 1]`, net gains `[-1, 0, -1, 3]`:

```text
net    = [-1, 0, -1, 3]
start   start = 0, total = 0, tank = 0
i = 0    gain = -1    tank = -1 < 0 -> start = 1, tank = 0    total = -1
i = 1    gain = +0    tank = 0    total = -1
i = 2    gain = -1    tank = -1 < 0 -> start = 3, tank = 0    total = -2
i = 3    gain = +3    tank = 3    total = 1
-> total = 1 >= 0: return start = 3
```

Station `0` dies immediately and is reset past; station `2`'s deficit retires `1` and `2` together; the survivor is `start = 3`, and the banked total `1 >= 0` certifies it. The function returns `3`, matching the expected Output for Example 1. On Example 2 the same sweep ends with `total = -1 < 0` and reports `-1`.

#### Solution

The code is the walkthrough's single lap: accumulate, reset on deficit, certify by the total.

```python
from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        n = len(gas)
        total = 0
        tank = 0
        start = 0
        for i in range(n):
            gain = gas[i] - cost[i]
            total += gain
            tank += gain
            if tank < 0:
                start = i + 1
                tank = 0
        return start if total >= 0 else -1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass over the stations with constant work per station: two additions and one comparison.

##### Space Complexity: `O(1)`

Three integers (`total`, `tank`, `start`), regardless of input length.

#### Key Insights

- The two totals answer two different questions: `total` decides whether any
  solution exists, `tank` decides which candidate survives. Conflating them
  is the classic wrong answer (the tank alone reads `0` at the end of every
  complete lap).
- The reset is not a heuristic: it is the Early-Exit skip argument applied
  online, retiring a whole dying prefix per deficit.
- `start = i + 1` can equal `n` when the last station resets; that value
  only survives to the return when `total < 0` made the answer `-1` anyway,
  so no wrap-around check is needed.

### Prefix Sum

#### Derivation

Write `net[i] = gas[i] - cost[i]` and let `prefix[i]` be the running sum of `net[0..i]`. A rotation beginning at station `s` keeps its tank non-negative exactly when every `prefix[j] - prefix[s - 1]` (with `prefix[-1] = 0`, wrapping modulo the total) is non-negative, which is a statement about the distance from `prefix[s - 1]` to the deepest point of the curve. The classical [prefix sum](https://en.wikipedia.org/wiki/Prefix_sum) facts do the rest: if `total >= 0`, starting just after the deepest prefix is a valid start (the wrapping rotation lifts every partial sum by exactly the deficit it needs), and if `total < 0`, every partial sum of every rotation sums to a negative number, so no rotation can stay non-negative throughout:

1. Compute `net` and its `total`; return `-1` immediately when `total < 0`.
2. Sweep once tracking `prefix` and its running minimum `min_prefix`.
3. Record `worst = i + 1` each time the prefix sinks to a new low.
4. Return `worst`: the station after the deepest prefix is the answer.

#### Walkthrough

Trace the prefix walk on Example 1: `gas = [1, 2, 3, 4]`, `cost = [2, 2, 4, 1]`, net gains `[-1, 0, -1, 3]`:

```text
net    = [-1, 0, -1, 3]
total = 1 >= 0, a solution exists
i = 0    prefix = -1    min so far = -1   new low -> worst start = 1
i = 1    prefix = -1    min so far = -1
i = 2    prefix = -2    min so far = -2   new low -> worst start = 3
i = 3    prefix = 1    min so far = -2
-> deepest prefix after index 2: start = 3
```

The curve bottoms out at `prefix[2] = -2`, and station `3` sits right after the trough: its rotation rides the final climb of `3` and wraps while the curve is recovering, so no partial sum dips. The sweep returns `3`, matching the expected Output for Example 1 and the Greedy's verdict on the same input.

#### Solution

The code is the walkthrough's single sweep: track the running prefix, remember the station after each new low.

```python
from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        n = len(gas)
        net = [gas[i] - cost[i] for i in range(n)]
        if sum(net) < 0:
            return -1
        prefix = 0
        min_prefix = 0
        worst = 0
        for i in range(n):
            prefix += net[i]
            if prefix < min_prefix:
                min_prefix = prefix
                worst = i + 1
        return worst
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass builds `net` and the sweep reads it once, constant work per station.

##### Space Complexity: `O(n)`

The `net` array holds one entry per station; dropping it (folding the gain computation into the sweep) brings the space back to `O(1)` at the cost of a slightly denser loop.

#### Key Insights

- The deepest prefix is the whole argument: starting after it gives every
  wrapped partial sum the largest possible head start, which is exactly what
  "never negative" demands.
- The feasibility half (`total < 0` means `-1`) is unavoidable in this frame:
  the prefix facts say nothing about which start to pick when none works.
- The `worst = 0` seed covers inputs where the prefix never dips: no low is
  deeper than the empty prefix, and station `0` is then a valid start.

## Comparison of Solutions

The practice harness's `practice/gas_station/reference.py` implements the **Greedy** solution.

### Time Complexity

- **Brute Force**: `O(n^2)` - a full tank walk per candidate start.
- **Early-Exit Simulation**: `O(n)` - failed walks retire disjoint ranges, so each leg is priced once.
- **Greedy**: `O(n)` - one pass, constant work per station.
- **Prefix Sum**: `O(n)` - one pass for the total, one for the deepest prefix.

### Space Complexity

- **Brute Force**: `O(1)` - tank and counters.
- **Early-Exit Simulation**: `O(1)` - tank, offset, candidate index.
- **Greedy**: `O(1)` - `total`, `tank`, and `start`.
- **Prefix Sum**: `O(n)` - the `net` array (collapsible to `O(1)`).

### Trade-offs

- The Brute Force is the direct transcription of the rules and the easiest
  version to trust, but it is the only one here that misses the constraint
  budget at `n = 100000`.
- The Early-Exit Simulation keeps the simulation's shape and gains linearity
  through the skip argument; the Greedy reaches the same candidate sequence
  with less code but more trust in the reset rule.
- The Prefix Sum buys a different kind of insight, the deepest-prefix
  characterization, which generalizes to rotation-sum problems beyond this
  one, at the price of an `O(n)` scratch array as written.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for
  checking the faster versions on tiny inputs.
- **Early-Exit Simulation**: when you want linear time while keeping the
  simulation's shape; the skip argument is the whole proof.
- **Greedy** (recommended): the default; one pass, `O(1)` space, and the
  standard interview answer for this problem.
- **Prefix Sum**: when the rotation-sum framing is the one being taught, or
  as the bridge to problems about circular partial sums.

### Optimization Notes

- The feasibility theorem is the load-bearing fact across all linear
  solutions: a completing start exists exactly when `sum(gas) >= sum(cost)`.
  Uniqueness of that start is a different kind of fact: not derived but
  assumed, LeetCode's own input restriction that at most one solution
  exists. On general inputs several starts can complete the circuit
  (`net = [1, 0]` lets station `0` and station `1` both finish the lap), so
  the restriction is what keeps the answer well defined.
- The Greedy and the Prefix Sum agree station by station: the reset points of
  the one are the new-low points of the other, and both hand back the same
  survivor. Choosing between them is a choice of explanation, not of
  computation.
- Watch the wrap: both the Early-Exit skip and any hand-rolled circular walk
  must decide what a failure after wrapping means. Forgetting it loops
  forever on unsolvable inputs, the exact bug the `fail_at >= n` branch
  exists to prevent.
- What the prefix picture certifies is existence and a witness, not
  uniqueness: the sweep returns the station after the first occurrence of
  the deepest prefix, and that station is a valid completing start whenever
  `total >= 0`. When several starts complete (`net = [1, 0]` again), the
  return value is one valid completing start among them, not the only one;
  the problem's input restriction (at most one solution exists) is what
  upgrades "a completing start" to "the answer".
