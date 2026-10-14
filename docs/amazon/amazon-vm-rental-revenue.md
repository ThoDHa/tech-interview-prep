# [VM Rental Revenue](https://www.fastprep.io/problems/amazon-vm-rental-revenue)

**Medium** | **NN minutes** | **Heap, Greedy**

There are multiple VM types, each with an initial stock count. A sequence of customers rent one VM at a time.

Each customer always rents from the VM type with the highest remaining stock. The revenue from a rental equals the sum of the current highest stock and the current lowest non-zero stock across all VM types. After the rental, the chosen VM type loses one unit of stock.

Return the total revenue after serving customerRequests customers.

## Examples

### Example 1

**Input:** `vmStock = [1, 2, 4]`, `customerRequests = 4`

**Output:** `15`

**Explanation:** The rental costs are 5, 4, 3, and 3, for a total revenue of 15.

## Constraints

- `Stocks are non-negative integers.`
- `The number of requests may be as large as the total available stock.`

## Solutions

### Linear Scan Simulation

#### Derivation

The revenue rule is a procedure, so the first solution simply performs the procedure. Each rental asks for two values, the highest remaining stock and the lowest non-zero stock, and a full scan of `vm_stock` answers both. The rented type is whichever type holds that highest stock, and its decrement is one more write:

1. Copy `vm_stock` into `stock` so the input stays intact.
2. For each of the `customer_requests` rentals: read `highest = max(stock)`,
   read `lowest` as the minimum over the positive values of `stock`.
3. Add `highest + lowest` to `total_revenue`, then decrement one occurrence of
   `highest` in `stock`.

#### Walkthrough

Example 1, `vm_stock = [1, 2, 4]`, `customer_requests = 4`. Each line is one rental with the two scanned values:

```text
rental 1   highest 4 (type 2), lowest 1 (type 0)   charge 5   stock [1, 2, 3]
rental 2   highest 3 (type 2), lowest 1 (type 0)   charge 4   stock [1, 2, 2]
rental 3   highest 2 (types 1 and 2 tie), lowest 1 charge 3   stock [1, 1, 2]
rental 4   highest 2 (type 2), lowest 1 (type 0)   charge 3   stock [1, 1, 1]
```

The charges `5, 4, 3, 3` sum to `15`, the expected Output.

#### Solution

The code is the walkthrough's per-rental scan and decrement:

```python
from typing import List


class Solution:
    def solve(self, vm_stock: List[int], customer_requests: int) -> int:
        stock = list(vm_stock)
        total_revenue = 0
        for _ in range(customer_requests):
            highest = max(stock)
            lowest = min(value for value in stock if value > 0)
            total_revenue += highest + lowest
            stock[stock.index(highest)] -= 1
        return total_revenue
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(R × n)`

Each of the `R = customer_requests` rentals scans the `n` VM types a constant number of times. Since the guarantee caps requests at the total stock, this is `O(S x n)` in the worst case, where `S` is the total stock.

##### Space Complexity: `O(n)`

The working copy `stock`; everything else is scalars.

#### Key Insights

- The simulation is a direct transcription of the revenue rule, which makes it the reference implementation every faster approach is checked against.
- `lowest` must skip zero: an emptied type is out of the rental market, and folding `0` into the minimum corrupts every later charge.
- The scan repeats nearly identical work every rental: only one type changes per rental, yet all `n` types are re-read, which is exactly the waste the next approach removes.

### Two Lazy Heaps

#### Derivation

The scan re-reads every type to learn something only two types changed: the rental decrements a single stock value, so the maximum can drop only along the rented type, and a new minimum can appear only as the rented type's new value. Both orderings are therefore maintainable with [heaps](https://en.wikipedia.org/wiki/Heap_(data_structure)): a max-heap over stocks for `highest`, a min-heap for `lowest`. Python's `heapq` is a min-heap, so the max side stores negated stocks.

Each rental must leave both heaps answerable again, but rebuilding them would reintroduce the scan. The repair is lazy invalidation: entries may go stale, and each heap repairs its top on demand. The decrement requires exactly two repairs: the rented type's entry in the max heap goes stale unless the type fell out of the lead (the top is then already correct), and the type's new value enters the min heap as a push when it is still positive. Dead entries, types whose stock hit `0`, linger in both heaps and are dropped only when they surface at the top:

1. Build `high_heap` of `(-stock, vm_type)` and `low_heap` of
   `(stock, vm_type)` over the positive stocks.
2. Clean `high_heap`: while the top's recorded stock differs from its live
   stock, pop the entry when the live stock is `0`, otherwise rewrite the top
   with the live value.
3. Clean `low_heap` the same way with positive recorded values.
4. Read `highest` and `lowest` from the cleaned tops and add their sum to
   `total_revenue`.
5. Decrement the rented type in `current`; push its new value onto `low_heap`
   when the value is still positive.

#### Invariant

Correctness rests on what the cleanup loops establish rather than on any formula. Every heap entry `(recorded_stock, vm_type)` was the true stock of `vm_type` at the moment the entry was last written, every type with positive stock has exactly one live entry in each heap, and no entry is rewritten by anything except the cleanup, the initial build, or the rental's own decrement and push:

```text
before each rental:  clean_high and clean_low run until the top's recorded
                     stock equals the live stock
branch pop:          live stock is 0 -> the entry is dead, dropping it
                     restores "one live entry per positive type"
branch rewrite:      recorded value is stale -> the live value is entered,
                     which was true the instant it was written
branch return:       the top equals the live stock -> every other entry
                     records an older (hence not larger, not smaller) value,
                     so the top is the true maximum / minimum
after the rental:    the decrement stales at most the rented type's max
                     entry, and the push supplies the min side
```

The invariant is what makes the read step legal: after the cleanup loops return, the tops of `high_heap` and `low_heap` are the true highest stock and the true lowest non-zero stock, without a single full scan.

#### Walkthrough

Example 1, `vm_stock = [1, 2, 4]`, `customer_requests = 4`. Each line is one rental; the tops are read after both cleanup loops settle:

```text
rental 1   tops 4 (type 2), 1 (type 0)     charge 5   revenue 5
           type 2 drops to 3; low pushes (3, 2)
rental 2   high top stale: 4 vs live 3 -> rewrite
           tops 3, 1                       charge 4   revenue 9
           type 2 drops to 2; low pushes (2, 2)
rental 3   high top stale: 3 vs live 2 -> rewrite
           tops 2, 1                       charge 3   revenue 12
           tie (-2, 1) < (-2, 2): type 1 rents; low pushes (1, 1)
rental 4   high top stale: 2 vs live 1 -> rewrite
           tops 2, 1                       charge 3   revenue 15
           type 2 drops to 1; low pushes (1, 2)
```

The charges read `5, 4, 3, 3` and sum to `15`, the expected Output. The stale-rewrite at the top of rentals 2 through 4 is the max side healing itself one entry at a time; no rental ever looks at more than a constant number of heap entries.

#### Solution

The code is the invariant in operation: two cleanup loops make the tops readable, the rental charges and decrements, and the push keeps the min side informed.

```python
import heapq
from typing import List


class Solution:
    def solve(self, vm_stock: List[int], customer_requests: int) -> int:
        current = list(vm_stock)

        def clean_high() -> None:
            while -high_heap[0][0] != current[high_heap[0][1]]:
                recorded_stock, vm_type = high_heap[0]
                live_stock = current[vm_type]
                if live_stock == 0:
                    heapq.heappop(high_heap)
                else:
                    heapq.heapreplace(high_heap, (-live_stock, vm_type))

        def clean_low() -> None:
            while low_heap[0][0] != current[low_heap[0][1]]:
                recorded_stock, vm_type = low_heap[0]
                live_stock = current[vm_type]
                if live_stock == 0:
                    heapq.heappop(low_heap)
                else:
                    heapq.heapreplace(low_heap, (live_stock, vm_type))

        high_heap = [(-stock, vm_type) for vm_type, stock in enumerate(current)
                     if stock > 0]
        heapq.heapify(high_heap)
        low_heap = [(stock, vm_type) for vm_type, stock in enumerate(current)
                    if stock > 0]
        heapq.heapify(low_heap)

        total_revenue = 0
        for _ in range(customer_requests):
            clean_high()
            clean_low()
            highest = -high_heap[0][0]
            lowest = low_heap[0][0]
            total_revenue += highest + lowest
            rented_type = high_heap[0][1]
            current[rented_type] -= 1
            if current[rented_type] > 0:
                heapq.heappush(low_heap, (current[rented_type], rented_type))
        return total_revenue
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n + R) log n)`

Building the heaps is `O(n)`; each of the `R` rentals performs a constant number of heap operations at `O(log n)` each, because the lazy cleanup charges every stale rewrite to the decrement that caused it and each entry is repaired at most once per stock change.

##### Space Complexity: `O(n)`

The live-value array plus at most `n` entries in each heap.

#### Key Insights

- One decrement can disturb only two orderings, so two heaps plus lazy repair maintain both at logarithmic cost instead of the scan's linear cost per rental.
- Zero entries must be popped, not kept: the revenue rule prices the lowest non-zero stock, and a dead type sitting at the top of `low_heap` would poison every later charge.
- Storing `(stock, vm_type)` tuples makes the ties deterministic and lets each cleanup branch find the live value with one array read.
- The guarantee that requests never exceed total stock doubles as the termination argument: `high_heap` and `low_heap` cannot empty while rentals remain.

## Comparison of Solutions

### Time Complexity

- **Linear Scan Simulation**: `O(R × n)` - every rental rescans all `n` types for the maximum, the minimum, and the rented position.
- **Two Lazy Heaps**: `O((n + R) log n)` - one heap build plus a constant number of logarithmic heap operations per rental.

### Space Complexity

- **Linear Scan Simulation**: `O(n)` - the working copy of the stock list.
- **Two Lazy Heaps**: `O(n)` - the live-value array plus both heaps.

### Trade-offs

- **Linear Scan Simulation**: impossible to get wrong and trivially verifiable, but the per-rental rescan is quadratic in the worst case and dwarfs everything else on large inputs.
- **Two Lazy Heaps**: amortizes each rental to logarithmic work, at the price of lazy invalidation, whose correctness needs the written invariant rather than a glance.

### When to Use Each

- **Linear Scan Simulation**: small stock totals, or as the oracle that validates the heap version during testing.
- **Two Lazy Heaps (Recommended)**: the interview answer whenever `customer_requests` or the stock counts can be large, which the constraints announce they can.

### Optimization Notes

- The heaps are built once from the initial stocks and never rebuilt; every later inconsistency is repaired lazily at the top, which is what keeps the per-rental cost at `O(log n)` instead of `O(n log n)`.
- The `0` check inside each cleanup branch is the whole difference between a correct solution and a subtly wrong one: the max side treats an emptied type as absent (correct either way, since it can no longer be the maximum), while the min side must evict it explicitly.
- Tuple entries `(stock, vm_type)` break ties by type index; any deterministic tie-break preserves the revenue total, because tied maximums yield the same charge.
