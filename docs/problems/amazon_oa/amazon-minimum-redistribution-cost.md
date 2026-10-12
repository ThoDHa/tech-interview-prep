# [Minimum Redistribution Cost](https://www.fastprep.io/problems/amazon-minimum-redistribution-cost)

**Medium** | **NN minutes** | **Array, Prefix Sum, Greedy**

There are n warehouses arranged in a circle. Warehouse i initially stores products[i] items.

You may redistribute items around the circle, but all moved items must travel in one fixed direction: either clockwise or counter-clockwise. Moving one item across one edge costs 1.

Return the minimum total cost needed to make every warehouse contain the same number of products. You may choose the better of the two directions.

Function Description Complete getMinimumRedistributionCost.

int products[n]: product counts around the circleReturns long: the minimum redistribution cost.

## Examples

### Example 1

**Input:** `products = [1,11,1,1,1]`

**Output:** `20`

**Explanation:** The average is 3. The extra 8 products at the second warehouse must fill deficits of 2 at four other warehouses. In either direction, the total edge-crossing cost is 20.

### Example 2

**Input:** `products = [0,6,0]`

**Output:** `6`

**Explanation:** The average is 2. Four items move out of the middle warehouse: two cross one edge and two cross two edges.

## Constraints

- `1 <= products.length <= 10^5`
- `0 <= products[i] <= 10^9`
- `The total number of products is divisible by products.length.`

## Solutions

### Brute Force Zero-Edge Search

#### Derivation

The most literal reading asks: what does a legal plan even look like? Pick one direction; write `surplus[i] = products[i] - average` (negative means the warehouse needs items). Because every item moves the same way, the number of items crossing each edge is forced once one edge is fixed: walking warehouse to warehouse, the flow on the next edge equals the flow on the previous edge plus the current warehouse's surplus. A full loop returns to the starting flow automatically, since the surpluses sum to zero. One more constraint pins everything down: at the optimum some edge carries zero flow, because if every edge carried items, shifting the whole plan by one item less would still be legal and cheaper. So enumerate each edge as the zero edge and simulate:

1. Compute `average` and the `surplus` list.
2. For each direction, try every `zero_offset` from `0` to `warehouse_count - 1`: the plan
   starts with flow `0` entering warehouse `zero_offset`.
3. Walk `warehouse_count` warehouses in that direction. At each one, add its
   surplus to `flow`; a negative `flow` means items would move against the chosen
   direction, so the candidate is discarded.
4. Each unit of `flow` crosses the current edge, so add `flow` to `cost` at every step.
5. Return the minimum `cost` over all valid candidates in both directions.

#### Walkthrough

Example 2, `products = [0, 6, 0]`: the average is `2`, so `surplus = [-2, 4, -2]`. Clockwise, the three zero-edge candidates behave very differently:

```text
zero edge after warehouse 0: start at warehouse 1
  enter w1 flow 0 -> +4 -> edge w1->w2 carries 4, cost 4
  enter w2 flow 4 -> -2 -> edge w2->w0 carries 2, cost 6
  enter w0 flow 2 -> -2 -> edge w0->w1 carries 0, cost 6  (loop closes at 0: valid)
zero edge after warehouse 1: start at warehouse 2
  enter w2 flow 0 -> -2 -> flow -2  (items would move counter-clockwise: discard)
zero edge after warehouse 2: start at warehouse 0
  enter w0 flow 0 -> -2 -> flow -2  (discard)
```

Only the first candidate is a legal clockwise plan, costing `6`. The counter-clockwise walk mirrors it and also yields `6`, so the function returns `6`, the expected Output. (Example 1 works the same way: its best clockwise plan starts after warehouse 0 and costs `20`, the counter-clockwise best also costs `20`.)

#### Solution

The code is the enumeration from the derivation: one helper walks a direction from each candidate zero edge.

```python
from typing import List


class Solution:
    def solve(self, products: List[int]) -> int:
        warehouse_count = len(products)
        average = sum(products) // warehouse_count
        surplus = [count - average for count in products]

        def direction_cost(walk_surplus: List[int]) -> int:
            best_cost = None
            for zero_offset in range(warehouse_count):
                flow = 0
                cost = 0
                valid = True
                for offset in range(zero_offset, zero_offset + warehouse_count):
                    warehouse = offset % warehouse_count
                    flow += walk_surplus[warehouse]
                    if flow < 0:
                        valid = False
                        break
                    cost += flow
                if valid and (best_cost is None or cost < best_cost):
                    best_cost = cost
            return best_cost

        clockwise_cost = direction_cost(surplus)
        counter_clockwise_cost = direction_cost(surplus[::-1])
        return min(clockwise_cost, counter_clockwise_cost)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Two directions times `n` candidate zero edges, each simulated with an `O(n)` walk around the circle.

##### Space Complexity: `O(n)`

The `surplus` list plus its reversed copy for the second direction.

#### Key Insights

- Once the direction and one edge's flow are fixed, the entire plan is forced: the flows are running sums of the surpluses.
- Requiring a zero-flow edge is safe because a plan with all edges positive can shed one item per edge and stay legal, so the optimum always has one.
- Discarding negative-flow candidates is what enforces the single-direction rule; the surviving minimum is the true unidirectional cost.

### Running Prefix Sums

#### Derivation

The brute force re-walks the circle `n` times to find the best zero edge, but the walk only computes running sums. Writing `P[i]` for the prefix surplus through warehouse `i`, the flow on edge `i` in any legal plan is `C + P[i]` for one constant `C`, the plan's total cost is `n * C + sum(P)`, and legality (`C + P[i] >= 0` everywhere) pushes `C` down to `-min(P)`. The minimum cost in one direction therefore has a closed form, no search needed:

```text
cost(direction) = sum(P) - n * min(P)
```

Evaluate it once for each direction and return the smaller:

1. Compute `average` and `surplus`.
2. For one direction, sweep once keeping `prefix_sum`, `prefix_total` (the sum of
   all prefixes), and `prefix_min` (their minimum).
3. Return `prefix_total - warehouse_count * prefix_min` for that direction.
4. Repeat on the reversed surplus list and return the minimum of the two costs.

#### Walkthrough

Example 1, `products = [1, 11, 1, 1, 1]`: the average is `3`, so `surplus = [-2, 8, -2, -2, -2]`. Clockwise, the sweep tracks the running prefix `P`:

```text
warehouse 0   P = -2   prefix_total = -2   prefix_min = -2
warehouse 1   P =  6   prefix_total =  4   prefix_min = -2
warehouse 2   P =  4   prefix_total =  8   prefix_min = -2
warehouse 3   P =  2   prefix_total = 10   prefix_min = -2
warehouse 4   P =  0   prefix_total = 10   prefix_min = -2
cost = 10 - 5 * (-2) = 20
```

The counter-clockwise sweep on the reversed surplus `[-2, -2, -2, 8, -2]` produces prefixes `-2, -4, -6, 2, 0`, `prefix_total = -10`, `prefix_min = -6`, and cost `-10 - 5 * (-6) = 20`. Both directions cost `20`, exactly what the example's Explanation states, so the function returns `20`. (Example 2 gives `0 - 3 * (-2) = 6` in both directions.)

#### Solution

The code is the closed form evaluated twice: one sweep per direction.

```python
from typing import Iterable, List


class Solution:
    def solve(self, products: List[int]) -> int:
        warehouse_count = len(products)
        average = sum(products) // warehouse_count
        surplus = [count - average for count in products]
        clockwise_cost = self.direction_cost(surplus, warehouse_count)
        counter_clockwise_cost = self.direction_cost(reversed(surplus), warehouse_count)
        return min(clockwise_cost, counter_clockwise_cost)

    def direction_cost(self, walk_surplus: Iterable[int], warehouse_count: int) -> int:
        prefix_sum = 0
        prefix_total = 0
        prefix_min = 0
        for warehouse_surplus in walk_surplus:
            prefix_sum += warehouse_surplus
            prefix_total += prefix_sum
            prefix_min = min(prefix_min, prefix_sum)
        return prefix_total - warehouse_count * prefix_min
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One averaging pass plus two linear sweeps, a constant number of passes over the warehouses.

##### Space Complexity: `O(n)`

The `surplus` list dominates; each sweep itself carries only the three running numbers.

#### Key Insights

- The flows of a unidirectional plan are `C + P[i]`; cost is linear in `C`, so the best `C` is `-min(P)` and no enumeration is needed.
- The final prefix always equals `0` because the surpluses sum to zero, which is why initializing `prefix_min` to `0` is safe: the true minimum is never positive.
- The two directions are not mirror-symmetric in cost in general, so both closed-form evaluations are required even though one line separates them.

### Prefix Sums with accumulate

#### Derivation

The closed-form sweep carries three running numbers by hand, but its bookkeeping has a standard-library shape: `itertools.accumulate` produces the prefix list, and `sum` and `min` read the two statistics the formula needs. The algorithm is the previous one verbatim; only the loop moves into the library:

1. `prefix = list(accumulate(walk_surplus))` builds `P` for one direction.
2. The direction's cost is `sum(prefix) - warehouse_count * min(prefix)`.
3. Evaluate it for `surplus` and `reversed(surplus)`, return the smaller.

#### Walkthrough

Example 1's clockwise sweep again: `accumulate` over `[-2, 8, -2, -2, -2]` yields the prefix list directly:

```text
accumulate -> [-2,  6,  4,  2,  0]
sum(prefix)  = 10
min(prefix)  = -2
cost         = 10 - 5 * (-2) = 20
```

The counter-clockwise call accumulates `[-2, -2, -2, 8, -2]` into `[-2, -4, -6, 2, 0]`, giving `sum = -10`, `min = -6`, cost `20`, and the function returns `min(20, 20) = 20`.

#### Solution

The code is the closed form with `accumulate` holding the prefix list.

```python
from itertools import accumulate
from typing import Iterable, List


class Solution:
    def solve(self, products: List[int]) -> int:
        warehouse_count = len(products)
        average = sum(products) // warehouse_count
        surplus = [count - average for count in products]
        clockwise_cost = self.direction_cost(surplus, warehouse_count)
        counter_clockwise_cost = self.direction_cost(reversed(surplus), warehouse_count)
        return min(clockwise_cost, counter_clockwise_cost)

    def direction_cost(self, walk_surplus: Iterable[int], warehouse_count: int) -> int:
        prefix = list(accumulate(walk_surplus))
        return sum(prefix) - warehouse_count * min(prefix)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`accumulate`, `sum`, and `min` each make one linear pass per direction.

##### Space Complexity: `O(n)`

The `surplus` list plus the materialized prefix list, one per direction call.

#### Key Insights

- The swap is bookkeeping only: `accumulate` replaces the hand-rolled running-sum loop and the algorithm is unchanged.
- `list(accumulate(...))` accepts any iterable, so `reversed(surplus)` needs no special handling.
- Reading the formula off a materialized list (`sum`, `min`) trades the `O(1)` running variables of the previous solution for declarative statistics calls.

## Comparison of Solutions

### Time Complexity

- **Brute Force Zero-Edge Search**: `O(n^2)` - two directions times `n` zero-edge candidates, each simulated with a full walk.
- **Running Prefix Sums**: `O(n)` - two linear sweeps evaluate the closed form directly.
- **Prefix Sums with accumulate**: `O(n)` - the same sweeps with the running sum delegated to the library.

### Space Complexity

- **Brute Force Zero-Edge Search**: `O(n)` - the surplus list plus its reversed copy.
- **Running Prefix Sums**: `O(n)` - the surplus list; the sweeps hold three running numbers each.
- **Prefix Sums with accumulate**: `O(n)` - the surplus list plus one materialized prefix list per direction.

### Trade-offs

- **Brute Force Zero-Edge Search**: derives the structure from first principles and is easy to trust, but re-simulating every candidate is hopeless at `n = 10^5`.
- **Running Prefix Sums**: collapses the whole search into one formula per direction; the closed form needs the zero-edge argument to justify it.
- **Prefix Sums with accumulate**: the shortest expression of the formula, at the price of materializing prefix lists.

### When to Use Each

- **Brute Force Zero-Edge Search**: small inputs, or an interview warm-up whose simulation motivates the closed form.
- **Running Prefix Sums (Recommended)**: the interview answer: linear time, a fixed handful of running variables per sweep, and a formula you can state in one line.
- **Prefix Sums with accumulate**: production code where the prefix statistics may grow (percentiles, per-edge loads) and a materialized list earns its space.

### Optimization Notes

- The problem's divisibility guarantee makes `average` exact; `surplus` always sums to zero, which is what closes the flow loop and anchors `prefix_min`.
- Counts reach `10^5` warehouses times `10^9` items, so prefix totals exceed 32 bits; Python integers are unbounded, and the function's long return in the statement signals the same care in fixed-width languages.
- If only one direction were allowed, the answer would be the single `direction_cost` call; trying both directions and taking the minimum costs nothing extra.

