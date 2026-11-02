# [Minimum Cost of Left and Right Propagation](https://www.fastprep.io/problems/amazon-minimum-left-right-propagation-cost)

**Medium** | **NN minutes** | **Array, Greedy**

You are given a positive integer array values. You may perform either propagation operation any number of times and in any order:

Choose index i and propagate left: replace every element before i with values[i]. This costs i * values[i].
Choose index i and propagate right: replace every element after i with values[i]. This costs (n - 1 - i) * values[i].

Return the minimum total cost needed to make every array element equal. You may perform zero operations when the array is already uniform.

## Examples

### Example 1

**Input:** `values = [5,2,4]`

**Output:** `4`

**Explanation:** Keep the middle value 2, propagate it left for cost 2, and propagate it right for another cost 2.

### Example 2

**Input:** `values = [1,1,2,1]`

**Output:** `2`

**Explanation:** Keep the first run of two 1s and propagate right from index 1 for cost 2.

### Example 3

**Input:** `values = [5,1,1,2,1,1]`

**Output:** `4`

**Explanation:** Keep the run of two 1s at indices 1 and 2. Propagate left from index 1 for cost 1, then right from index 2 for cost 3. The total is 4; no original equal-value run gives a lower cost.

## Constraints

- `1 <= values.length <= 100000`
- `1 <= values[i] <= 10^9`
- `The answer fits in a signed 64-bit integer.`

## Deriving the Solution

Every element the operations never touch must already equal the final common value, and the untouched positions always form one contiguous middle stretch: a left propagation flattens a prefix, a right propagation flattens a suffix, and whatever sits between them survives. So an optimal plan keeps one equal-value run and pays exactly to flatten what is left of it and what is right of it, which collapses the whole search to scanning the runs.

1. **Start literal.** Search operation sequences the statement allows: apply either propagation at any index in any order until the array is uniform, minimizing total cost. Correct but exponential in general; see [Operation-Sequence Search](#operation-sequence-search).
2. **Spot the structure.** Every reachable array is a constant prefix, a constant suffix, and an untouched middle slice of the original; only the last operation per direction matters, and any operation whose side is later re-covered was wasted, so an optimal sequence uses at most one left and one right propagation.
3. **Fix it.** Keep one maximal equal-value run `[left..right]`, propagate left from `left` and right from `right`, and pay `(left + n - 1 - right) * value`; scan all runs and take the minimum: see [Kept-Run Greedy](#kept-run-greedy).

## Solutions

### Operation-Sequence Search

#### Derivation

The statement's most literal reading: the answer is the cheapest path through operation space, so search it like one:

1. Start from the input array with cost `0`; the goal test is "all elements equal".
2. From any non-uniform array, expand every operation: for each index `i`, the left propagation (new prefix, cost `i * values[i]` at the current array) and the right propagation (new suffix, cost `(n - 1 - i) * values[i]`).
3. Because every operation only overwrites with a value already present and never lengthens the untouched middle forever, the reachable state space stays tiny; a priority queue ordered by cost returns the minimum cost at the first uniform state (edge costs are non-negative, so this is Dijkstra).
4. Return that minimum; the empty operation list already covers uniform inputs at cost `0`.

This search never reasons about runs: it applies the operations mechanically, which makes it the independent oracle the greedy is checked against.

#### Walkthrough

Example 1 (`values = [5,2,4]`), the cheapest expansions first:

```text
start            [5,2,4]  cost 0    not uniform
left  from 1     [2,2,4]  cost 2    not uniform
right from 1     [5,2,2]  cost 2    not uniform
right from 1 of [2,2,4]   cost 2+2  -> [2,2,2] uniform: total 4
```

No cheaper uniform state exists (cost `0` and `1` states are non-uniform or absent), matching the expected Output.

#### Solution

```python
import heapq
from typing import List


class Solution:
    def minimumPropagationCost(self, values: List[int]) -> int:
        start = tuple(values)
        best_cost = {start: 0}
        frontier = [(0, start)]
        while frontier:
            cost, state = heapq.heappop(frontier)
            if cost > best_cost[state]:
                continue
            if len(set(state)) == 1:
                return cost
            for index in range(len(state)):
                if index > 0:
                    left_state = (state[index],) * index + state[index:]
                    left_cost = cost + index * state[index]
                    if left_cost < best_cost.get(left_state, float("inf")):
                        best_cost[left_state] = left_cost
                        heapq.heappush(frontier, (left_cost, left_state))
                if index < len(state) - 1:
                    right_state = (
                        state[: index + 1]
                        + (state[index],) * (len(state) - 1 - index)
                    )
                    right_cost = cost + (len(state) - 1 - index) * state[index]
                    if right_cost < best_cost.get(right_state, float("inf")):
                        best_cost[right_state] = right_cost
                        heapq.heappush(frontier, (right_cost, right_state))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(S * n^2 * log S)`

Each expansion builds and hashes `2n` neighbor tuples of length `n`, the quadratic term, and up to `2n` improving neighbors each pay a heap push whose sift makes `O(log S)` length-`n` tuple comparisons, `O(n log S)` per push, so the heap term `O(n^2 log S)` dominates the expansion. `S`, the number of reachable states, is bounded by the constant-prefix, untouched-middle, constant-suffix shapes the operations can produce, which keeps the whole product tiny.

##### Space Complexity: `O(S * n)`

The cost table and frontier hold full array states.

#### Key Insights

- The search is the statement's quantifiers transcribed: any operation, any order, any number of times, cheapest total wins.
- Reachable states collapse fast: a prefix written by one left propagation and a suffix written by one right propagation bracket an untouched slice of the original array, so the space is polynomial even though the operation count is unbounded.
- Uniform inputs exit at cost `0` before any expansion, so zero-operation inputs need no special case.

### Kept-Run Greedy

#### Derivation

The search wastes its time re-deriving structure the array already shows. Two observations finish the problem:

1. An operation never changes the middle it brackets, so the positions no operation ever writes form a contiguous stretch, and all of them must already hold the final value. An optimal plan therefore keeps one equal-value run and flattens both outsides.
2. Extra operations cannot help: a second propagation in the same direction either covers a superset (its predecessor was wasted) or leaves a hole; propagations from inside the kept run change nothing. So the plan is exactly: left propagation from the run's first index `left`, right propagation from its last index `right`.

The kept run must be maximal for its value: extending a run strictly lowers `left`, lowers `n - 1 - right`, or both, and the value stays the same. Scanning the maximal runs and taking the cheapest flat cost is the whole algorithm.

#### Closed Form

For a maximal run of `value` spanning `[left..right]` in an array of length `n`:

$$ \text{cost}(\text{left}, \text{right}, \text{value}) = (\text{left} + n - 1 - \text{right}) \cdot \text{value} $$

and the answer is the minimum of this over all maximal runs. An already-uniform array's single run scores `0`, matching the zero-operation rule.

#### Walkthrough

Example 3 (`values = [5,1,1,2,1,1]`), every maximal run scored with `n = 6`:

```text
run [0..0] value 5:  (0 + 6 - 1 - 0) * 5 = 25
run [1..2] value 1:  (1 + 6 - 1 - 2) * 1 = 1 + 3 = 4
run [3..3] value 2:  (3 + 6 - 1 - 3) * 2 = 10
run [4..5] value 1:  (4 + 6 - 1 - 5) * 1 = 4
```

The minimum is `4`, matching the expected Output: propagate left from index 1 and right from index 2.

#### Solution

```python
from typing import List


class Solution:
    def minimumPropagationCost(self, values: List[int]) -> int:
        count = len(values)
        best = None
        left = 0
        while left < count:
            right = left
            while right + 1 < count and values[right + 1] == values[left]:
                right += 1
            cost = (left + count - 1 - right) * values[left]
            if best is None or cost < best:
                best = cost
            left = right + 1
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass splits the runs; each element is visited by the run scan exactly twice.

##### Space Complexity: `O(1)`

Only the running best and the two run pointers.

#### Key Insights

- "Make everything equal" decomposes into "choose what survives": the survivors are always one contiguous equal-value run, and the cost is the price of flattening the two sides.
- Maximality is free optimality: a longer run of the same value costs less from both ends, so scanning maximal runs alone is safe.
- Costs multiply the flattened width by the kept value, so a cheap value wins even from the middle, and a run touching an end is cheaper still; already-uniform arrays score `0` with no special case.
- The greedy matches the exhaustive search on every small input, and scales to `n = 100000` with `10^9` values because one integer pass cannot overflow a Python int.

## Comparison of Solutions

### Time Complexity

- **Operation-Sequence Search**: `O(S * n^2 * log S)` over reachable states `S` - exhaustive but tiny-state.
- **Kept-Run Greedy**: `O(n)` - one pass over the runs.

### Space Complexity

- **Operation-Sequence Search**: `O(S * n)` - every visited state stored.
- **Kept-Run Greedy**: `O(1)` - two pointers and a running minimum.

### Trade-offs

- **Operation-Sequence Search**: the definition executed literally and the independent checker for the greedy; unusable at the statement's `100000` scale.
- **Kept-Run Greedy (Recommended)**: the structural proof (at most one propagation per direction, kept run maximal) turns the search into one scan.

### When to Use Each

- **Operation-Sequence Search**: for tiny inputs in tests, and always as the oracle validating the greedy before publication.
- **Kept-Run Greedy (Recommended)**: the interview answer: derive the kept-run shape, then scan.

### Optimization Notes

- **Kept-Run Greedy** is the recommended choice: linear time, constant space, and no heap.
- The closed form needs no prefix or suffix arrays: the run boundaries carry everything.
- Watch the multiplication order in fixed-width languages: `(left + n - 1 - right)` reaches `100000` and `value` reaches `10^9`, so the product needs 64-bit arithmetic, exactly the constraint the statement calls out.
