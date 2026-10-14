# [Inventory Allocation](https://www.fastprep.io/problems/amazon-inventory-allocation)

**Medium** | **NN minutes** | **Simulation, Sorting, Heap**

You are given a list of inventory requests. Each request is represented as [customerId, quantity, bidAmount, timestamp].

Allocate totalInventory items using these rules:

Requests with a higher bidAmount are processed before lower bids.For requests with the same bidAmount, items are distributed in round-robin order by increasing timestamp.During each round, a customer can receive at most one item.A customer leaves the current round-robin group once their requested quantity is fulfilled.Lower bids are considered only after every higher bid has either been fulfilled or inventory is exhausted.Return the customer IDs of customers who receive no items, in the same order their requests appear in the input.

## Examples

### Example 1

**Input:** `requests = [[1,5,5,0],[2,7,8,1],[3,7,5,1],[4,10,3,3]]`, `totalInventory = 18`

**Output:** `[4]`

**Explanation:** Customer 2 is fully served first because bid 8 is highest. Customers 1 and 3 then share the remaining inventory at bid 5. No inventory remains for customer 4.

### Example 2

**Input:** `requests = [[1,2,10,0],[2,3,10,1],[3,1,5,0]]`, `totalInventory = 3`

**Output:** `[3]`

**Explanation:** The bid-10 group receives all 3 available items before the lower bid is considered, so customer 3 receives none.

## Constraints

- `1 <= requests.length <= 10^5`
- `requests[i].length = 4`
- `customer IDs are unique.`
- `0 <= timestamp <= 10^9`
- `0 <= totalInventory <= 10^9`

## Solutions

### One-Item Round-Robin Simulation

#### Derivation

The most literal reading of the rules is to run the allocation exactly as described, one item at a time. Sort the requests into bid groups, highest bid first, order each group by timestamp, and rotate through the group handing out single items until the group is fulfilled or the inventory runs out; a fulfilled customer simply stops being rotated back. The [queue rotation](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)) (pop the front customer, serve one item, re-append while they still want more) is the classic way to run a round-robin without index arithmetic:

1. Split `requests` into `grouped`, mapping each `bid_amount` to the input
   positions of its requests, skipping zero-quantity requests (they are
   fulfilled on arrival and can never receive an item).
2. Visit bids in descending order. For each group, build `waiting`, a deque of
   positions sorted by `timestamp`.
3. While inventory remains and `waiting` is non-empty, pop the front position,
   hand out one item (decrement `remaining_quantity[position]` and
   `remaining_inventory`, set `received[position] = True`), and re-append the
   position only while its remaining quantity is positive.
4. Return the customer IDs at positions whose `received` flag is still `False`,
   in input order.

Every handed-out item costs constant work, but the item count itself can be `totalInventory`, which reaches `10^9`.

#### Walkthrough

Example 2, `requests = [[1,2,10,0],[2,3,10,1],[3,1,5,0]]`, `totalInventory = 3`. The bid-10 group holds customer 1 (quantity 2) and customer 2 (quantity 3) in timestamp order; the bid-5 group holds customer 3. Each line is one pop from `waiting`:

```text
bid 10       waiting = [1, 2]        inventory = 3
pop 1        serve item, remaining[1] = 1, re-append   inventory = 2, waiting = [2, 1]
pop 2        serve item, remaining[2] = 2, re-append   inventory = 1, waiting = [1, 2]
pop 1        serve item, remaining[1] = 0, leave        inventory = 0, waiting = [2]
inventory 0  stop; bid 5 never starts, customer 3 receives nothing
```

`received` is `[True, True, False]`, so the function returns `[3]`, matching the expected Output. Customer 2 is left half-served mid-rotation, which the one-item view handles without any special casing.

#### Solution

The code is the walkthrough's rotation: pop, serve, re-append while more is wanted.

```python
from collections import deque
from typing import Dict, List


class Solution:
    def solve(self, requests: List[List[int]], total_inventory: int) -> List[int]:
        received = [False] * len(requests)
        remaining_quantity = [request[1] for request in requests]
        remaining_inventory = total_inventory

        grouped: Dict[int, List[int]] = {}
        for position, request in enumerate(requests):
            quantity, bid_amount = request[1], request[2]
            if quantity > 0:
                grouped.setdefault(bid_amount, []).append(position)

        for bid_amount in sorted(grouped, reverse=True):
            waiting = deque(sorted(grouped[bid_amount],
                                   key=lambda position: requests[position][3]))
            while remaining_inventory > 0 and waiting:
                position = waiting.popleft()
                remaining_quantity[position] -= 1
                remaining_inventory -= 1
                received[position] = True
                if remaining_quantity[position] > 0:
                    waiting.append(position)

        return [requests[position][0] for position, has_received in enumerate(received)
                if not has_received]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n + I)`

Sorting the groups costs `O(n log n)`, and the simulation hands out `I = min(total inventory, total requested quantity)` items one at a time at constant cost each. With `totalInventory` up to `10^9`, the `I` term dominates and the loop cannot finish in an online judge's budget.

##### Space Complexity: `O(n)`

The received and remaining-quantity arrays plus the per-group deques, all bounded by the request count.

#### Key Insights

- The queue rotation encodes both round-robin fairness and the leaving rule: a fulfilled customer is simply not re-appended, so no separate membership bookkeeping is needed.
- Zero-quantity requests are fulfilled on arrival and can never receive an item, so keeping them out of the groups up front lets the return statement treat "never rotated" and "never received" identically.
- The approach is correct but item-at-a-time: its running time is tied to `totalInventory` rather than to the request count, which is the flaw the next approach repairs.

### Bid-Group Pass

#### Derivation

The simulation pays per item, but the requested output never asks how many items anyone got, only who got none. That question is decided entirely in each group's first round: the first round serves one item to every group member in timestamp order, so every customer in a group receives at least one item if and only if the inventory is at least the group size at the moment the group starts. If the inventory is smaller, exactly the first `remaining_inventory` customers in timestamp order receive one item, the inventory hits zero, and everyone else, in this group and every lower bid, receives nothing. Everything after round one (fulfillment counts, later rounds, customers leaving) affects only arithmetic the output never reads:

1. Build `grouped` from `requests`, mapping each `bid_amount` to
   `[timestamp, position, quantity]` records, skipping zero-quantity requests.
2. Visit bids in descending order. Sort each `group` by timestamp.
3. When `remaining_inventory < len(group)`, mark the first
   `remaining_inventory` positions as having received an item and stop: the
   inventory is exhausted and every unmarked customer stays unmarked.
4. Otherwise mark every position in the group, subtract
   `min(remaining_inventory, the group's total quantity)` from
   `remaining_inventory`, and continue to the next bid.
5. Return the customer IDs at unmarked positions, in input order.

#### Walkthrough

Example 1, `requests = [[1,5,5,0],[2,7,8,1],[3,7,5,1],[4,10,3,3]]`, `totalInventory = 18`. The groups, ordered by bid, with each record shown as `(timestamp, customer, quantity)`:

```text
bid 8        group = [(1, 2, 7)]            size 1 <= 18
             mark 2; served = min(18, 7) = 7     remaining_inventory = 11
bid 5        group = [(0, 1, 5), (1, 3, 7)] size 2 <= 11
             mark 1 and 3; served = min(11, 12) = 11   remaining_inventory = 0
bid 3        group = [(3, 4, 10)]           size 1 > 0
             prefix is empty; stop
```

The bid-5 line is where the shortcut shows: customers 1 and 3 need 12 items between them but only 11 remain, so the one-item view would rotate eleven single serves; the group pass reads `min(11, 12)` and moves on, and both customers keep their first-round item either way. The marked set is `{2, 1, 3}` and customer 4 stays unmarked, so the function returns `[4]`, matching the expected Output.

#### Solution

The code is the group pass: mark per group, subtract the served total, stop at the first group the inventory cannot seat.

```python
from typing import Dict, List


class Solution:
    def solve(self, requests: List[List[int]], total_inventory: int) -> List[int]:
        received = [False] * len(requests)
        remaining_inventory = total_inventory

        grouped: Dict[int, List[List[int]]] = {}
        for position, request in enumerate(requests):
            quantity, bid_amount, timestamp = request[1], request[2], request[3]
            if quantity > 0:
                grouped.setdefault(bid_amount, []).append([timestamp, position, quantity])

        for bid_amount in sorted(grouped, reverse=True):
            group = sorted(grouped[bid_amount])
            if remaining_inventory < len(group):
                for timestamp, position, quantity in group[:remaining_inventory]:
                    received[position] = True
                break
            for timestamp, position, quantity in group:
                received[position] = True
            served_quantity = min(remaining_inventory,
                                  sum(quantity for _, _, quantity in group))
            remaining_inventory -= served_quantity

        return [requests[position][0] for position, has_received in enumerate(received)
                if not has_received]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting the `n` requests into groups and each group by timestamp dominates; the pass over groups and records is linear.

##### Space Complexity: `O(n)`

The grouped records and the received array both scale with the request count.

#### Key Insights

- Who-receives-nothing is a first-round property: a group seated while `remaining_inventory >= len(group)` gives every member an item, no matter how the later rounds divide the rest.
- The group's consumption is `min(remaining_inventory, total quantity)`, which keeps the running inventory correct without simulating any round.
- Sorting each group by `[timestamp, position]` breaks timestamp ties by input order, matching the rotation order the one-item simulation would use.
- The output order requirement (input order, not allocation order) is free here: the `received` array is indexed by input position and read left to right.

## Comparison of Solutions

### Time Complexity

- **One-Item Round-Robin Simulation**: `O(n log n + I)` - constant work per handed-out item, with `I = min(total inventory, total requested quantity)` potentially in the billions.
- **Bid-Group Pass**: `O(n log n)` - sorting dominates; the marking pass reads each request a constant number of times.

### Space Complexity

- **One-Item Round-Robin Simulation**: `O(n)` - received and remaining-quantity arrays plus per-group deques.
- **Bid-Group Pass**: `O(n)` - the grouped records and the received array.

### Trade-offs

- **One-Item Round-Robin Simulation**: mirrors the rules so directly that its correctness is immediate, but its running time is tied to `totalInventory`, not to the input size.
- **Bid-Group Pass**: runs in sorting time regardless of inventory size, but it must justify the first-round argument that collapses the whole round-robin into one membership question.

### When to Use Each

- **One-Item Round-Robin Simulation**: when inventories are small, when the problem asks for per-customer item counts, or as the reference oracle the fast version is checked against.
- **Bid-Group Pass (Recommended)**: the right answer at the stated constraints, where `totalInventory` reaches `10^9` and only the unfulfilled IDs are requested.

### Optimization Notes

- The decisive observation generalizes: when a simulation is asked for a coarser output than it computes, look for the first round or first pass that already decides that output.
- The `min(remaining_inventory, group total)` subtraction is the only arithmetic that survives the collapse; everything else about the round-robin (rounds, leaving, partial rounds) is dead weight for this output.
- A pitfall is returning unfulfilled customers instead of zero-item customers: customer 3 in Example 1 receives six of seven items and must not appear in the output, while a customer whose group is never seated must.
