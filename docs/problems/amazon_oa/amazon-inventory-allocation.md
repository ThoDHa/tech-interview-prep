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

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
