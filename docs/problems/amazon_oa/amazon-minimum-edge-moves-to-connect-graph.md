# [Minimum Edge Moves to Connect a Network](https://www.fastprep.io/problems/amazon-minimum-edge-moves-to-connect-graph)

**Medium** | **NN minutes** | **Graph, Union Find**

You manage an undirected network with nodes 0 through n - 1. In one move, you may remove one existing cable and reconnect that cable between any two nodes.

Return the minimum number of cable moves needed to make every node connected. Return -1 when the network does not contain enough cables to connect all nodes.

## Examples

### Example 1

**Input:** `n = 4`, `edges = [[0,1],[0,2],[1,2]]`

**Output:** `1`

**Explanation:** One cycle edge can be moved to attach the isolated node.

### Example 2

**Input:** `n = 6`, `edges = [[0,1],[0,2],[0,3],[1,2]]`

**Output:** `-1`

**Explanation:** Four cables cannot connect six nodes.

## Constraints

- `1 <= n <= 100000.`
- `Every edge has two valid node IDs.`
- `Self-loops and parallel edges are allowed and still count as available cables.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
