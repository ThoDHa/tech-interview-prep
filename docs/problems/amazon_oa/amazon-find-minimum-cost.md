# [Find Minimum Cost](https://www.fastprep.io/problems/amazon-find-minimum-cost)

**Hard** | **NN minutes** | **Array, Prefix Sum, Greedy**

A warehouse has n identical containers arranged in a circle. Adjacent containers are one unit apart, and the goal is to make every container hold the same number of products.

Choose either clockwise or counterclockwise movement; all transfers must use that same direction.Products may be collected from containers with excess units and delivered to containers with deficits.Moving one product across one edge costs 1.Return the minimum total transfer cost. It is guaranteed that equal redistribution is possible.

## Examples

### Example 1

**Input:** `products = [3, 4, 6, 6, 6]`

**Output:** `7`

**Explanation:** $23

### Example 2

**Input:** `products = [1, 11, 1, 1, 1]`

**Output:** `20`

**Explanation:** The final average is 3. One container has 8 extra products. Moving in either fixed direction, send 2 products to each of the other four containers, for total cost 2*1 + 2*2 + 2*3 + 2*4 = 20.

## Constraints

- `1 <= products.length <= 2 * 10^50 <= products[i] <= 10^9The answer may exceed the 32-bit integer range.`

## Solutions

### Greedy Delivery Simulation

#### Derivation

The most literal reading of the problem: follow the products. Every container holding more than the average has a surplus to give, every container holding less has a deficit to fill, and moving one product across one edge costs 1. With a single fixed direction, the natural plan serves each deficit from the nearest surplus behind it and keeps walking forward around the circle:

1. Compute `average = sum(products) // container_count` (redistribution is guaranteed possible, so the division is exact) and build `surplus`, where `surplus[container] = products[container] - average`.
2. For each `source` in index order, while `surplus[source] > 0`, walk forward with a `step` counter until reaching a `target` whose `surplus[target] < 0`; deliver `moved = min(surplus[source], -surplus[target])` units at cost `moved * step`.
3. The statement lets us choose one direction for all transfers, and a plan and its mirror can cost different amounts, so run the same delivery routine once clockwise on `products` and once counterclockwise (by feeding it the reversed array) and return the smaller total.

#### Walkthrough

Example 2 has a single surplus container, so the deliveries are easy to read one by one: `products = [1, 11, 1, 1, 1]` gives `average = 3` and `surplus = [-2, 8, -2, -2, -2]`. The scan starts at container 0 (no surplus), then reaches container 1 with 8 units and serves the deficits in forward order:

| Delivery from container 1 | `target` | `step` | `moved` | Cost `moved * step` |
| --- | --- | --- | --- | --- |
| to container 2 | 2 | 1 | 2 | 2 |
| to container 3 | 3 | 2 | 2 | 4 |
| to container 4 | 4 | 3 | 2 | 6 |
| wraps to container 0 | 0 | 4 | 2 | 8 |

The clockwise total is 2 + 4 + 6 + 8 = 20, and `surplus` is now all zeros. The mirrored run on the reversed array walks the same four distances in the other direction and also totals 20 (single-source surplus is symmetric), so the function returns `min(20, 20) = 20`, matching the expected Output. Example 1 is less symmetric: the clockwise plan costs 7 there while the counterclockwise mirror costs 8, and the smaller value 7 is returned.

#### Solution

The code is the walkthrough's delivery loop, wrapped in a mirror run over the reversed array:

```python
from typing import List


class Solution:
    def solve(self, products: List[int]) -> int:
        container_count = len(products)
        average = sum(products) // container_count

        def direction_cost(ordered: List[int]) -> int:
            surplus = [amount - average for amount in ordered]
            transfer_cost = 0
            for source in range(container_count):
                while surplus[source] > 0:
                    step = 1
                    target = (source + step) % container_count
                    while surplus[target] >= 0:
                        step += 1
                        target = (source + step) % container_count
                    moved = min(surplus[source], -surplus[target])
                    transfer_cost += moved * step
                    surplus[source] -= moved
                    surplus[target] += moved
            return transfer_cost

        return min(direction_cost(products),
                   direction_cost(list(reversed(products))))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every delivery pairs one surplus container with one deficit, and locating the next deficit walks forward across the circle, so a worst case with many small deliveries performs `O(n)` scans of `O(n)` containers.

##### Space Complexity: `O(n)`

The `surplus` array copied by each direction run; the reversed view adds another `O(n)`.

#### Key Insights

- The answer is a cost, not a schedule: any collection of deliveries that moves enough units into every deficit is feasible, so a greedy nearest-deficit plan is safe to build and compare.
- The surplus array makes each delivery a constant-time bookkeeping update; the expense is only the forward search for the next deficit.
- Feeding the reversed array to the same routine evaluates the counterclockwise direction without writing a second delivery loop.
- The direction choice genuinely matters when several containers hold surplus (Example 1 differs by 1 between the two directions); a single-source instance like Example 2 is symmetric.

### Prefix-Sum Edge Flow

#### Derivation

The simulation's weakness is that it reasons about pairs of containers when the cost is charged to edges. Think per edge instead: a delivery of `moved` products across `step` edges contributes exactly `moved` crossings to each of those `step` edges, so the total cost is the sum over edges of the number of products crossing that edge. Which products cross is irrelevant; only the totals are. Cut the circle between container `i` and container `i + 1` and the net surplus that must leave the left side is fixed by arithmetic:

1. With `excess[container] = products[container] - average`, define the running
   excess `prefix[i] = excess[0] + ... + excess[i]`.
2. Any clockwise plan moves `clockwise_flow[i] = circulation + prefix[i]`
   products across edge `i` for some constant `circulation >= -min(prefix)`
   (products may make wasteful full laps, which is exactly what `circulation`
   counts). Cost `container_count * circulation + sum(prefix)` grows with
   `circulation`, so the best plan takes `circulation = -min(prefix)` and costs
   `sum(prefix) - container_count * min(prefix)`.
3. Counterclockwise movement flips the direction across each edge, and the
   conservation equation becomes `counter_flow[i] = circulation - prefix[i]`,
   giving the mirrored cost `container_count * max(prefix) - sum(prefix)`.
4. `sum(prefix)` is not zero in general, so the two bounds are different numbers (Example 1: 7 clockwise, 8 counterclockwise); return the smaller.

#### Formula

Let `prefix[i]` be the running excess after container `i`, with `prefix_total = sum(prefix)`, and let `n = container_count`:

$$ \text{cost}_{\text{cw}} = \text{prefix\_total} - n \cdot \min_i \text{prefix}[i], \qquad \text{cost}_{\text{ccw}} = n \cdot \max_i \text{prefix}[i] - \text{prefix\_total} $$

```text
prefix[i]      = excess[0] + ... + excess[i],   excess = products - average
prefix_total   = sum of all prefix values       (not zero in general)
clockwise_cost = prefix_total - n * min(prefix)
counter_cost   = n * max(prefix) - prefix_total
answer         = min(clockwise_cost, counter_cost)
```

The clockwise bound comes from the cheapest legal `circulation = -min(prefix)`; the counterclockwise bound mirrors it around `max(prefix)`. Both follow from charging one crossing per edge per product.

#### Walkthrough

Example 1, `products = [3, 4, 6, 6, 6]`: `average = 5`, `excess = [-2, -1, 1, 1, 1]`, and the running excess builds up one container at a time:

```text
container      excess   prefix[i]
0              -2       -2
1              -1       -3   (lowest_running)
2               1       -2
3               1       -1
4               1        0   (highest_running)
prefix_total = -2 - 3 - 2 - 1 + 0 = -8
```

The cut after container 1 carries the largest forced outflow, so `min(prefix) = -3` fixes the cheapest circulation at 3: the clockwise cost is `-8 - 5 * (-3) = 7`. Mirrored, `max(prefix) = 0` gives a counterclockwise cost of `5 * 0 - (-8) = 8`. The function returns `min(7, 8) = 7`, matching the expected Output. Reading the flows directly: all three surplus products move clockwise, crossing edge 4 three times, edge 3 twice, and edges 2 and 0 once each, for `3 + 2 + 1 + 1 + 0 = 7`. Concretely: container 2's surplus travels three edges to container 0, container 3's surplus travels three edges to container 1, and container 4's surplus travels one edge to container 0.

#### Solution

The code is the walkthrough in one pass: accumulate the running excess while tracking its total, minimum, and maximum, then evaluate the two direction bounds.

```python
from typing import List


class Solution:
    def solve(self, products: List[int]) -> int:
        container_count = len(products)
        average = sum(products) // container_count
        running_excess = 0
        prefix_total = 0
        lowest_running = 0
        highest_running = 0
        for amount in products:
            running_excess += amount - average
            prefix_total += running_excess
            lowest_running = min(lowest_running, running_excess)
            highest_running = max(highest_running, running_excess)
        clockwise_cost = prefix_total - container_count * lowest_running
        counter_cost = container_count * highest_running - prefix_total
        return min(clockwise_cost, counter_cost)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass over `products` to build the running excess statistics, plus constant work for the two bounds.

##### Space Complexity: `O(1)`

Five scalar accumulators; no array is kept because only the total, minimum, and maximum of `prefix` are ever read.

#### Key Insights

- Charging cost per edge instead of per delivery converts a matching problem into an arithmetic one: the cost is determined by the multiset of `prefix` values.
- The degree of freedom a circle adds over a line is the circulation, products that travel full laps and serve nobody; minimizing it means anchoring the flow at the cut with the largest forced deficit.
- The two directions are not mirrors of the same number because `sum(prefix) != 0` in general; evaluating both bounds costs nothing extra.
- Everything the formula needs (total, minimum, maximum of the running excess) fits in scalars, which is why this solution beats the simulation without simulating anything.

## Comparison of Solutions

### Time Complexity

- **Greedy Delivery Simulation**: `O(n^2)` - each surplus container scans forward to its next deficit, and there can be `O(n)` deliveries.
- **Prefix-Sum Edge Flow**: `O(n)` - a single pass computes the running excess total, minimum, and maximum.

### Space Complexity

- **Greedy Delivery Simulation**: `O(n)` - the `surplus` array per direction run, plus the reversed copy.
- **Prefix-Sum Edge Flow**: `O(1)` - five scalar accumulators regardless of the container count.

### Trade-offs

- **Greedy Delivery Simulation**: directly mirrors how a person ships products, so it is easy to trust and easy to adapt to extra rules (per-container transfer limits, direction changes), but it pays quadratic time and must be run twice for the two directions.
- **Prefix-Sum Edge Flow**: optimal in both time and space and direction-aware by construction, but the edge-flow reformulation is the kind of insight that must be derived rather than guessed, and the code no longer resembles the physical process.

### When to Use Each

- **Greedy Delivery Simulation (Recommended)**: for interviews: derive it in minutes, and it doubles as a checker for the closed formula on small inputs.
- **Prefix-Sum Edge Flow**: when `n` is large (the constraints allow answers beyond 32 bits and lengths up to millions) or when the answer must be produced in a single pass.

### Optimization Notes

- The greedy run stays correct if the inner deficit search restarts from `source + 1` each time; never resume a scan from a stale position, since filled deficits change the map.
- In the flow solution, initialize `lowest_running` and `highest_running` to `0` (not to the first prefix value) so the empty cut, where circulation must be 0, is always represented; this keeps the bound valid when all containers already hold the average.
- Both solutions need Python's arbitrary-precision integers only implicitly; summing up to `2 * 10^5` values of at most `10^9` stays far within safe ranges in other languages too, but the answer can exceed 32 bits, so use 64-bit accumulators when porting.
