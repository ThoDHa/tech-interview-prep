# [Feasible Indices After Reduction](https://www.fastprep.io/problems/amazon-feasible-indices-after-reduction)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given an integer array arr of size n. All elements of arr are distinct.

You may perform either of the following operations any number of times:

Choose a non-empty prefix of the current array and delete every element in that prefix except the minimum element of the prefix.Choose a non-empty suffix of the current array and delete every element in that suffix except the maximum element of the suffix.After each operation, the remaining elements are concatenated to form the new array.

An index i is called feasible if it is possible to reduce the array to the single element [arr[i]]. Return a binary string of length n where the i-th character is '1' if index i is feasible, and '0' otherwise.

## Examples

### Example 1

**Input:** `arr = [1, 3, 2, 5, 4]`

**Output:** `"10011"`

**Explanation:** The feasible values are 1, 5, and 4. They are the prefix minimum at index 0 or suffix maximums at indices 3 and 4.

### Example 2

**Input:** `arr = [4, 1, 3, 2]`

**Output:** `"1111"`

**Explanation:** All four indices are feasible. Values 4 and 1 are prefix minima, while values 3 and 2 are suffix maxima. For example, after reducing prefix [4,1] to 1, value 3 can survive a reduction of suffix [3,2] and then the whole array. The same first step followed by reducing the whole remaining suffix can leave 2.

## Constraints

- `1 <= n <= 10^5`
- `1 <= arr[i] <= 10^9`
- `All values in arr are distinct.`

## Solutions

### Reachable-State Search

#### Derivation

The most literal reading: an index is feasible when some sequence of the two operations transforms the full array into the one-element array `[arr[i]]`, so search every array the operations can reach and see which single-element arrays turn up. Each operation shrinks the array by at least one element, so the state graph is a finite [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) of depth at most `n` and a plain breadth-first enumeration terminates:

1. Seed `seen_states` with `tuple(arr)` and `frontier` with the same state.
2. For every state in the frontier, apply every prefix operation: for each
   `prefix_end`, rebuild the state as `(prefix_minimum,) + state[prefix_end + 1:]`.
3. Apply every suffix operation the same way:
   `state[:suffix_start] + (suffix_maximum,)`.
4. Collect unseen successors into `next_frontier` and repeat until it is empty.
5. Index `position` is feasible exactly when `(arr[position],)` is in
   `seen_states`; assemble the binary string.

#### Walkthrough

Example 2, `arr = [4, 1, 3, 2]`, is small enough to trace to all four singletons. Each line names the operation as `P(k)` (prefix `[0..k]`, keep the minimum) or `S(k)` (suffix `[k..3]`, keep the maximum):

```text
depth 1   from (4, 1, 3, 2):  P(1) keeps 1 -> (1, 3, 2)
                              P(2) keeps 1 -> (1, 2)
                              P(3) keeps 1 -> (1,)      value 1 confirmed
                              S(0) keeps 4 -> (4,)      value 4 confirmed
                              S(1) keeps 3 -> (4, 3)
                              S(2) keeps 3 -> (4, 1, 3)
depth 2   from (1, 3, 2):     S(0) keeps 3 -> (3,)      value 3 confirmed
          from (1, 2):        S(0) keeps 2 -> (2,)      value 2 confirmed
```

All four one-element arrays, `(1,)`, `(4,)`, `(3,)`, `(2,)`, are in `seen_states` by depth 2, so every index is feasible: the returned string is `"1111"`, the expected Output. (For Example 1 the same search finds `(1,)`, `(5,)`, and `(4,)` but never `(3,)` or `(2,)`, giving `"10011"`.)

#### Solution

The code is the frontier loop from the walkthrough, with tuples as hashable states.

```python
from typing import List


class Solution:
    def solve(self, arr: List[int]) -> str:
        start = tuple(arr)
        seen_states = {start}
        frontier = [start]
        while frontier:
            next_frontier = []
            for state in frontier:
                size = len(state)
                for prefix_end in range(size):
                    kept = min(state[:prefix_end + 1])
                    successor = (kept,) + state[prefix_end + 1:]
                    if successor not in seen_states:
                        seen_states.add(successor)
                        next_frontier.append(successor)
                for suffix_start in range(size):
                    kept = max(state[suffix_start:])
                    successor = state[:suffix_start] + (kept,)
                    if successor not in seen_states:
                        seen_states.add(successor)
                        next_frontier.append(successor)
            frontier = next_frontier

        return "".join(
            "1" if (arr[position],) in seen_states else "0"
            for position in range(len(arr))
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n^2)`

Every reachable state is a subsequence of `arr`, so there are at most `2^n` of them; expanding one state applies `2n` operations, each an `O(n)` min/max plus slice.

##### Space Complexity: `O(2^n × n)`

`seen_states` stores every reachable state, and each state holds up to `n` elements.

#### Key Insights

- The search is exhaustive, so its verdicts are correct by construction, which makes this version the oracle the faster approaches are checked against.
- Every operation strictly shortens the array, so the state graph cannot cycle and the loop terminates without a visited-depth cap.
- The exponential blowup is the price of not understanding the operations: nothing in this search exploits what prefix and suffix reductions do structurally.

### Greedy Route Simulation

#### Derivation

The search treats every operation sequence as equally worth trying. But a survivor of the final operation must be the kept element of that operation, which suggests committing to one of two routes per index instead of exploring all of them. To keep `value = arr[position]` alive, either a prefix operation keeps it (possible only when it is the minimum of its prefix), after which the tail still to its right must collapse, or a suffix operation keeps it (only when it is the maximum of its suffix), after which the head to its left must collapse. Each route is three operations with fixed choices:

1. Prefix route: apply the prefix operation over `[0..position]`. If the kept
   element is not `value`, the route dies. Collapse the tail with one suffix
   operation (the suffix starting right after `value`, whose maximum is kept),
   leaving `[value, tail_maximum]`.
2. Finish the route: `[value, tail_maximum]` keeps `value` under a prefix
   operation when `tail_maximum > value` (the minimum of the two is `value`),
   and under a suffix operation otherwise. One of the two always works.
3. Suffix route: mirror image. Apply the suffix operation over
   `[position..n - 1]`; on success collapse the head to `head_minimum`, then
   finish with the operation that keeps `value` in
   `[head_minimum, value]`.
4. `position` is feasible when either route ends at `[value]`.

#### Walkthrough

Example 2, `arr = [4, 1, 3, 2]`, exercises both routes. The trace below shows, per position, the route that succeeds:

```text
position 0  value 4  prefix route: P(0) -> [4, 1, 3, 2] (kept 4)
            S(1) collapses tail -> [4, 3];  tail_max 3 < 4 -> S(0) -> [4]  OK
position 1  value 1  prefix route: P(1) -> [1, 3, 2] (kept 1)
            S(1) collapses tail -> [1, 3];  tail_max 3 > 1 -> P(1) -> [1]  OK
position 2  value 3  prefix route: P(2) -> [1, 2] (kept 1)  kept != 3, route dies
            suffix route: S(2) -> [4, 1, 3] (kept 3)
            P(1) collapses head -> [1, 3];  head_min 1 < 3 -> S(0) -> [3]  OK
position 3  value 2  prefix route: P(3) -> [1] (kept 1)  kept != 2, route dies
            suffix route: S(3) -> [4, 1, 3, 2] (kept 2)
            P(2) collapses head -> [1, 2];  head_min 1 < 2 -> S(0) -> [2]  OK
```

Every position ends at `[value]`, so the result string is `"1111"`, the expected Output. Position 2 is the instructive one: the prefix route dies because reducing `[4, 1, 3]` keeps `1`, and only the suffix route rescues the index.

#### Solution

The code applies real operations to real lists, so each route's success check is executed, not assumed.

```python
from typing import List


class Solution:
    def solve(self, arr: List[int]) -> str:
        def apply_prefix_op(values: List[int], prefix_end: int) -> List[int]:
            kept = min(values[:prefix_end + 1])
            return [kept] + values[prefix_end + 1:]

        def apply_suffix_op(values: List[int], suffix_start: int) -> List[int]:
            kept = max(values[suffix_start:])
            return values[:suffix_start] + [kept]

        def can_reduce_to(position: int) -> bool:
            value = arr[position]

            working = apply_prefix_op(arr, position)
            if working[0] == value:
                if len(working) == 1:
                    return True
                working = apply_suffix_op(working, 1)
                if working[1] > value:
                    working = apply_prefix_op(working, 1)
                else:
                    working = apply_suffix_op(working, 0)
                if working == [value]:
                    return True

            working = apply_suffix_op(arr, position)
            if working[-1] == value:
                if len(working) == 1:
                    return True
                working = apply_prefix_op(working, len(working) - 2)
                if working[0] > value:
                    working = apply_prefix_op(working, 1)
                else:
                    working = apply_suffix_op(working, 0)
                if working == [value]:
                    return True

            return False

        return "".join(
            "1" if can_reduce_to(position) else "0"
            for position in range(len(arr))
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` positions runs one route of a constant number of list operations, each an `O(n)` min/max plus slice.

##### Space Complexity: `O(n)`

The `working` copies of the array, one per operation application.

#### Key Insights

- The finishing step can never fail: in `[value, u]` one of the two operations always keeps `value` (the prefix operation when `u > value`, the suffix operation when `u < value`), so a route that survives its first step always succeeds.
- Committing to three fixed operations per route replaces the exponential operation tree with two candidate routes per index.
- The simulation is constructive: for a feasible index it doubles as a witness sequence of operations, which the exhaustive search does not provide.

### Prefix Minimum and Suffix Maximum Scan

#### Derivation

The simulation needed both routes because it asked the wrong question: not "which route keeps `value`" but "which indices can any route keep". Strip the simulation to its skeleton and one fact falls out: the first operation of the prefix route keeps `value` exactly when `value` is the minimum of `arr[0..position]` (a prefix minimum), and the first operation of the suffix route keeps it exactly when `value` is the maximum of `arr[position..n - 1]` (a suffix maximum). The [Greedy Route Simulation](#greedy-route-simulation) walkthrough showed that a route passing its first step always finishes. So prefix minima and suffix maxima are all feasible. The converse needs an impossibility argument, and it rests on an invariant: an index that has both a smaller element somewhere to its left and a bigger element somewhere to its right can never shake off both witnesses.

#### Invariant

Let `A` state that some element left of `arr[i]` is smaller than `arr[i]`, and `D` state that some element right of `arr[i]` is bigger than `arr[i]`. For every array reachable while `arr[i]` is still present:

$$ A_0 \land D_0 \implies A_t \land D_t \quad \text{for every reachable array that still contains } arr[i] $$

```text
A: some element left  of arr[i] is smaller than arr[i]
D: some element right of arr[i] is bigger  than arr[i]

A and D hold before any operation that leaves arr[i] alive:
  prefix operation left of arr[i]    the left part collapses to its minimum,
                                     still smaller than arr[i]: A and D unchanged
  prefix operation covering arr[i]   every A-element lies in the prefix, so the
                                     kept minimum is smaller: arr[i] is deleted
  suffix operation right of arr[i]   the right part collapses to its maximum,
                                     still bigger than arr[i]: A and D unchanged
  suffix operation covering arr[i]   every D-element lies in the suffix, so the
                                     kept maximum is bigger: arr[i] is deleted
A and D hold after every operation that leaves arr[i] alive
```

A prefix covering `arr[i]` reaches every position left of it, so an `A`-element inside the prefix makes the kept minimum smaller than `arr[i]`; symmetrically for suffixes and `D`-elements. The singleton `[arr[i]]` satisfies neither `A` nor `D`, so an index with both witnesses is unreachable.

#### Walkthrough

Example 1, `arr = [1, 3, 2, 5, 4]`, in two sweeps plus the combination:

```text
prefix-minimum sweep   running_minimum   is_prefix_minimum
  position 0  value 1  1                 True
  position 1  value 3  1                 False
  position 2  value 2  1                 False
  position 3  value 5  1                 False
  position 4  value 4  1                 False

suffix-maximum sweep   running_maximum   is_suffix_maximum
  position 4  value 4  4                 True
  position 3  value 5  5                 True
  position 2  value 2  5                 False
  position 1  value 3  5                 False
  position 0  value 1  5                 False
```

Combining the two boolean arrays gives `"10011"`, the expected Output. Values `3` and `2` carry both witnesses (`1` is smaller to their left, `5` is bigger to their right), and the invariant forbids exactly those.

#### Solution

The code is the two sweeps from the walkthrough, OR-ed into the result string.

```python
from typing import List


class Solution:
    def solve(self, arr: List[int]) -> str:
        size = len(arr)
        is_prefix_minimum = [False] * size
        running_minimum = None
        for position in range(size):
            if running_minimum is None or arr[position] < running_minimum:
                running_minimum = arr[position]
                is_prefix_minimum[position] = True

        is_suffix_maximum = [False] * size
        running_maximum = None
        for position in range(size - 1, -1, -1):
            if running_maximum is None or arr[position] > running_maximum:
                running_maximum = arr[position]
                is_suffix_maximum[position] = True

        return "".join(
            "1" if is_prefix_minimum[position] or is_suffix_maximum[position] else "0"
            for position in range(size)
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two sweeps over the array plus one pass to assemble the output string.

##### Space Complexity: `O(n)`

The two boolean arrays; the output string adds another `O(n)`.

#### Key Insights

- An index survives to the end only by being kept by some operation, and the first operation of each route is a membership test for prefix minimum or suffix maximum, which makes the characterization exact rather than heuristic.
- The invariant is the whole proof that nothing else is feasible: witnesses smaller-left and bigger-right cannot both be destroyed while `arr[i]` lives, because the only operation able to destroy each of them also destroys `arr[i]`.
- Distinctness matters: with repeated values a "smaller" or "bigger" witness could be a tie, and both the operations' kept elements and the invariant's strict comparisons would need re-derivation.

## Comparison of Solutions

### Time Complexity

- **Reachable-State Search**: `O(2^n × n^2)` - up to `2^n` reachable states, each expanded by `2n` linear-time operations.
- **Greedy Route Simulation**: `O(n^2)` - two constant-length routes of list operations per index.
- **Prefix Minimum and Suffix Maximum Scan**: `O(n)` - two sweeps and one output pass.

### Space Complexity

- **Reachable-State Search**: `O(2^n × n)` - the set of all reachable states.
- **Greedy Route Simulation**: `O(n)` - one working copy per operation application.
- **Prefix Minimum and Suffix Maximum Scan**: `O(n)` - two boolean arrays plus the output.

### Trade-offs

- **Reachable-State Search**: correct by exhaustiveness and reusable for any operation set, but unusable beyond trivial `n` and it proves nothing about why the answers are what they are.
- **Greedy Route Simulation**: fast enough for the stated constraints and constructive (it yields a witness operation sequence per feasible index), but its correctness rides on the finishing-step argument, which is easy to miss.
- **Prefix Minimum and Suffix Maximum Scan**: linear, a one-look implementation, and backed by the invariant proof; it answers feasibility only and provides no operation sequence.

### When to Use Each

- **Reachable-State Search**: prototyping and cross-checking the fast approaches on small inputs, or a variant problem whose operations are too intricate to analyze.
- **Greedy Route Simulation (Recommended)**: the interview sweet spot: it demonstrates the routing insight, produces witnesses, and runs in quadratic time with a modest constant.
- **Prefix Minimum and Suffix Maximum Scan**: the final answer for the stated constraints (`n` up to `10^5`), where the linear scan and its invariant are the things an interviewer wants to hear.

### Optimization Notes

- The two routes in the simulation share their finishing logic by symmetry: both reduce to "one of the two operations keeps `value` in a two-element array", which is why a route that passes its first operation never fails.
- The scan never materializes intermediate arrays; keeping only the running minimum or maximum is what drops the space from per-route copies to two boolean arrays.
- All values being distinct lets the comparisons stay strict; with duplicates, both the kept element of an operation and the invariant's witness definitions would need tie-breaking rules spelled out.
