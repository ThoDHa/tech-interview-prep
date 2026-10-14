# [Nearby Fulfillment Centers with Inventory](https://www.fastprep.io/problems/amazon-nearby-fulfillment-centers)

**Medium** | **NN minutes** | **Graph, Breadth First Search, Shortest Path**

A delivery must be fulfilled near a destination center. The fulfillment network is an undirected graph whose edges are given by connections. Each row [u, v] connects centers u and v in both directions.

The array inventory represents a map from center ID to available quantity: each row is [centerId, quantity], and every center ID appears exactly once.

Return every center ID that satisfies all of these conditions:

the center is not destination;its inventory quantity is greater than 0;its shortest-path distance from destination is at most maxStep edges.Return the qualifying IDs in ascending numerical order. A center in a disconnected component does not qualify.

## Examples

### Example 1

**Input:** `connections = [[1,2],[1,3],[2,4],[3,4],[4,5]]`, `destination = 4`, `maxStep = 1`, `inventory = [[1,2],[2,0],[3,5],[4,3],[5,6]]`

**Output:** `[3,5]`

**Explanation:** Centers 2, 3, and 5 are one edge from destination 4. Center 2 has no inventory, while centers 3 and 5 have positive inventory. The destination itself is excluded.

### Example 2

**Input:** `connections = [[10,20],[20,30],[30,40]]`, `destination = 20`, `maxStep = 2`, `inventory = [[10,1],[20,9],[30,0],[40,4],[50,8]]`

**Output:** `[10,40]`

**Explanation:** Center 10 is one edge away and center 40 is two edges away. Center 30 has zero inventory, and center 50 is disconnected.

### Example 3

**Input:** `connections = [[1,2],[2,3]]`, `destination = 2`, `maxStep = 0`, `inventory = [[1,7],[2,5],[3,9]]`

**Output:** `[]`

**Explanation:** With maxStep = 0, only the destination is at an allowed distance, and the destination must be excluded.

## Constraints

- `1 <= inventory.length <= 2 * 10^5.`
- `Each inventory[i] is [centerId, quantity]; center IDs are distinct positive integers, and 0 <= quantity <= 10^9.`
- `destination appears exactly once in inventory.`
- `0 <= connections.length <= 2 * 10^5; each row contains two distinct center IDs that both appear in inventory.`
- `0 <= maxStep <= 2 * 10^5.`
- `The graph may be disconnected, and the answer is returned in ascending numerical order.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
