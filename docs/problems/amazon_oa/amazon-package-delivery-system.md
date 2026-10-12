# [Package Delivery System](https://www.fastprep.io/problems/amazon-package-delivery-system)

**Medium** | **NN minutes** | **Greedy, Sorting, Heap**

Each shipment scenario has a list of truck capacities and a list of package weights.

A truck may deliver any package whose weight does not exceed its current capacity. After a successful delivery, that truck's capacity becomes floor(capacity / 2). Determine whether every package in each scenario can be delivered using the available trucks.

Return an int[] where each entry is 1 if the corresponding scenario is feasible and 0 otherwise.

## Examples

### Example 1

**Input:** `truckCapacities = [[7]]`, `packageWeights = [[4, 3]]`

**Output:** `[1]`

**Explanation:** The single truck delivers package 4, its capacity drops to 3, and it can still deliver package 3. The scenario is feasible.

## Constraints

- `The number of scenarios and the lengths of the nested arrays can be large, so the solution should avoid brute-force backtracking over all assignments.`

## Solutions

### Descending Packages with Linear Truck Scans

#### Derivation

The most literal reading asks a feasibility question per scenario, and feasibility invites backtracking over all package-to-truck assignments, which the constraints explicitly warn against. Two observations shrink the search to nothing. First, the packages can be faced in descending weight order: a heavier package needs at least as much capacity as a lighter one, so if any delivery order works, the descending order works. Second, when facing the heaviest undelivered package, firing the fullest available truck is never worse than firing any other truck: halving is monotone, so the fullest truck's future capacities `c // 2, c // 4, ...` dominate every other truck's term by term. Together the observations collapse the search into one greedy pass:

1. For each scenario, copy the truck capacities into `remaining`.
2. Scan the packages in descending weight.
3. For each package, linearly find the fullest truck in `remaining`.
4. If that truck's capacity is below the package weight, the scenario is
   infeasible: no other truck could carry it either.
5. Otherwise deliver and halve that truck's capacity. A scenario that delivers
   every package contributes `1`, the rest `0`.

#### Walkthrough

Example 1, `truck_capacities = [[7]]`, `package_weights = [[4, 3]]`. The packages are faced in descending order, and each line shows the scan result:

```text
packages desc [4, 3]   remaining [7]
package 4   fullest truck 7   7 >= 4   deliver   remaining [3]
package 3   fullest truck 3   3 >= 3   deliver   remaining [1]
all delivered -> 1
```

The single truck delivers both packages, so the scenario contributes `1`, the expected Output.

#### Solution

The code is the walkthrough's descending pass with the fullest-truck scan inline:

```python
from typing import List


class Solution:
    def solve(self, truck_capacities: List[List[int]],
              package_weights: List[List[int]]) -> List[int]:
        results = []
        for capacities, weights in zip(truck_capacities, package_weights):
            remaining = list(capacities)
            feasible = True
            for weight in sorted(weights, reverse=True):
                fullest = 0
                for truck in range(1, len(remaining)):
                    if remaining[truck] > remaining[fullest]:
                        fullest = truck
                if remaining[fullest] < weight:
                    feasible = False
                    break
                remaining[fullest] //= 2
            results.append(1 if feasible else 0)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(P x (log P + m))` per scenario

Where `P` is the package count and `m` the truck count: sorting the packages costs `P log P`, and each of the `P` packages pays one linear scan over `m` trucks.

##### Space Complexity: `O(P + m)`

The sorted package order plus the `remaining` capacities copy.

#### Key Insights

- Descending package order is a free normalization: any feasible schedule can be reordered to face the heaviest package first, so testing only that order loses nothing.
- The abort is the greedy's whole infeasibility proof: when the fullest truck cannot carry the current package, no assignment can, because every other truck is weaker both now and after every future halving.
- The per-package rescan for the fullest truck repeats work the previous rental left behind, which is precisely what a heap eliminates.

### Descending Packages with a Capacity Heap

#### Derivation

The greedy is unchanged; only its bookkeeping improves. The scan re-finds the fullest truck every package even though at most one truck changed: the fired truck halved, and a halved capacity can never still be the maximum (a fired truck was at least `2` to deliver anything, so `c // 2 < c` and the field never grows). The fullest-truck query is therefore a dynamic maximum over a multiset with one removal and one insertion per package, which is exactly what a [max-heap](https://en.wikipedia.org/wiki/Heap_(data_structure)) maintains in logarithmic time. Python's `heapq` is a min-heap, so capacities enter negated. The greedy's correctness carries over untouched; per the argument above, facing packages heaviest first and always firing the current maximum capacity truck is safe:

1. Heapify the negated capacities into `available`.
2. Face the packages in descending weight.
3. Pop `biggest` (the negated top). When `biggest < weight`, mark the scenario
   infeasible; no remaining truck can carry the package.
4. Otherwise push `-(biggest // 2)` back.
5. Record `1` for a scenario whose packages all clear, `0` otherwise.

#### Walkthrough

Example 1 again, `truck_capacities = [[7]]`, `package_weights = [[4, 3]]`, now with the heap holding the fleet. Each line is one package:

```text
packages desc [4, 3]   available (max-heap) [7]
package 4   pop 7   7 >= 4   deliver, push 7 // 2 = 3   available [3]
package 3   pop 3   3 >= 3   deliver, push 3 // 2 = 1   available [1]
all delivered -> 1
```

Both packages clear, so the scenario contributes `1`, the expected Output. A tailored infeasible scenario shows the abort: with `truck_capacities = [[7]]`, `package_weights = [[4, 4]]`, the first package drops the truck to `3`, and the second package finds `3 < 4`, so the scenario contributes `0`.

#### Solution

The code is the same greedy with the linear scan replaced by heap operations:

```python
import heapq
from typing import List


class Solution:
    def solve(self, truck_capacities: List[List[int]],
              package_weights: List[List[int]]) -> List[int]:
        results = []
        for capacities, weights in zip(truck_capacities, package_weights):
            available = [-capacity for capacity in capacities]
            heapq.heapify(available)
            feasible = True
            for weight in sorted(weights, reverse=True):
                biggest = -heapq.heappop(available)
                if biggest < weight:
                    feasible = False
                    break
                heapq.heappush(available, -(biggest // 2))
            results.append(1 if feasible else 0)
        return results
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(P x (log P + log m) + m)` per scenario

Sorting the packages costs `P log P`, the heap build costs `m`, and each of the `P` packages performs one pop and at most one push at `O(log m)`.

##### Space Complexity: `O(P + m)`

The sorted package order plus the heap of negated capacities.

#### Key Insights

- A fired truck can never remain the maximum: it delivered a package, so its capacity was at least `2` and its halved value is strictly smaller. The heap top is therefore always fresh, and no lazy repair is needed.
- Negating capacities turns Python's min-heap into the max-heap the greedy needs; the pop-push cycle costs two logarithmic operations per package.
- The greedy's exchange argument does all the correctness work: monotone halving means the fullest truck dominates every alternative on every future step, so the locally best choice is globally safe.

## Comparison of Solutions

### Time Complexity

- **Descending Packages with Linear Truck Scans**: `O(P x (log P + m))` per scenario - the sort plus one full truck scan per package.
- **Descending Packages with a Capacity Heap**: `O(P x (log P + log m) + m)` per scenario - the sort plus logarithmic heap operations per package and one heap build.

### Space Complexity

- **Descending Packages with Linear Truck Scans**: `O(P + m)` - sorted packages plus the capacities copy.
- **Descending Packages with a Capacity Heap**: `O(P + m)` - sorted packages plus the negated-capacity heap.

### Trade-offs

- **Descending Packages with Linear Truck Scans**: the greedy in its plainest form, easy to reason about line by line, but the rescan makes dense fleets expensive.
- **Descending Packages with a Capacity Heap**: same decisions at heap speed, at the cost of trusting the negation idiom and the no-stale-top argument.

### When to Use Each

- **Descending Packages with Linear Truck Scans**: tiny scenarios or a first pass in an interview before the data structure question comes up.
- **Descending Packages with a Capacity Heap (Recommended)**: the interview answer whenever `P` or `m` grows, which the constraints say they do.

### Optimization Notes

- The greedy must face packages in descending weight: facing them in input order is not the same algorithm and fails (with trucks `[5, 3]` and packages `[3, 4]`, facing `3` first burns the `5` down to `2` and strands the `4`).
- Scenarios are independent, so the heaps and sorts never share state; a scenario's early abort skips straight to the next one.
- Capacities of `1` are legal deliverers and become `0` after one delivery; both versions handle that naturally, since a `0` capacity simply sits at the heap bottom and is never popped as a candidate that matters.
