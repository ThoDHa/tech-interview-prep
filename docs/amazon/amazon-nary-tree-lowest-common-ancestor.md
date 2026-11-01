# [Lowest Common Ancestor in an N-ary Tree](https://www.fastprep.io/problems/amazon-nary-tree-lowest-common-ancestor)

**Medium** | **NN minutes** | **Tree, Hash Table**

A rooted N-ary tree has nodes labeled from 0 through n - 1. It is encoded by parent, where parent[root] = -1 and every other value gives the node's direct parent.

Given two valid node labels p and q, return their lowest common ancestor: the deepest node that is an ancestor of both. A node is an ancestor of itself.

## Examples

### Example 1

**Input:** `parent = [-1,0,0,1,1,2,2,3]`, `p = 7`, `q = 4`

**Output:** `1`

**Explanation:** Node 1 is the deepest shared ancestor of nodes 7 and 4.

### Example 2

**Input:** `parent = [-1,0,0,1,1,2,2]`, `p = 5`, `q = 6`

**Output:** `2`

**Explanation:** Both queried nodes are direct children of node 2.

## Constraints

- `1 <= parent.length <= 200000.`
- `Exactly one entry is -1; every other entry is a valid node label.`
- `The parent relationships form one connected acyclic rooted tree.`
- `0 <= p, q < parent.length.`

## Deriving the Solution

The encoding hands you upward travel for free: the answer to "who is node `x`'s parent?" is a single array read, so any walk from a node toward the root is a loop of array reads. Every approach below is built from those upward walks; they differ in what they remember along the way.

1. **Start literal.** Both query nodes know one thing the answer needs: how deep they are. Equalize the depths by lifting the deeper node, then move both up in lockstep until they meet: see [Depth-Equalized Climb](#depth-equalized-climb).
2. **Trade the counter for a memory.** The lockstep climb keeps both pointers in sync only by first measuring both depths; recording the first climb's visited nodes instead lets the second climb stop the moment it recognizes familiar ground: see [Ancestor-Set Climb](#ancestor-set-climb).

## Solutions

### Depth-Equalized Climb

#### Derivation

Two people on different branches of the same tree can only meet at the root unless one of them first climbs to the other's level. That is the whole idea: measure both depths by climbing to the root, send the deeper node up until both stand at the same depth, and only then advance them together. At equal depth the two climbers are either the same node or two nodes whose ancestors converge strictly above, so the first step where the two climbers agree is the deepest agreement there ever was:

1. Define `depth_of(node)`: climb `node` to the root counting steps.
2. Lift whichever of `p`, `q` is deeper by the depth difference, one parent read at a time.
3. While `p != q`, set `p = parent[p]` and `q = parent[q]`.
4. Return `p`, which the loop exits on as soon as the two climbers share a node.

#### Walkthrough

Example 1, `parent = [-1,0,0,1,1,2,2,3]`, `p = 7`, `q = 4`:

```text
depth_of(7)   7 -> 3 -> 1 -> 0          depth 3
depth_of(4)   4 -> 1 -> 0               depth 2
lift p by 1   7 -> 3                    both at depth 2
lockstep      p = 3, q = 4  differ
lockstep      p = parent[3] = 1, q = parent[4] = 1   agree

answer 1
```

The climbers meet at node `1`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def lowestCommonAncestor(self, parent: List[int], p: int, q: int) -> int:
        def depth_of(node: int) -> int:
            depth = 0
            while parent[node] != -1:
                node = parent[node]
                depth += 1
            return depth

        depth_p, depth_q = depth_of(p), depth_of(q)
        deeper, shallower = (p, q) if depth_p > depth_q else (q, p)
        for _ in range(abs(depth_p - depth_q)):
            deeper = parent[deeper]

        while deeper != shallower:
            deeper = parent[deeper]
            shallower = parent[shallower]
        return deeper
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(depth_p + depth_q)`

Each climb touches every node on one root path at most twice: once to measure, once to walk. With `n` nodes no root path exceeds `n - 1` reads.

##### Space Complexity: `O(1)`

Only the two travelling labels and two depth counters live beyond the input.

#### Key Insights

- Equalizing depths first is what makes the lockstep loop correct: from equal depth onward, the two climbers can only meet at a genuine common ancestor, and they meet at the deepest one.
- The array encoding needs no children adjacency for this approach; the root is found implicitly as the node whose parent is `-1`.
- `abs(depth_p - depth_q)` handles the equal-depth start where no lifting is needed, including `p == q`, which exits the lockstep loop immediately.

### Ancestor-Set Climb

#### Derivation

The Depth-Equalized Climb pays for its constant space with a synchronization contract: two counters, a lift loop, and a lockstep loop that must move in exact unison. A set removes the contract. A node's ancestor chain is fully determined by repeated parent reads, so the first climb can pour its entire chain into a set and finish; the second climb then walks its own chain and stops at the first label the set already holds. No deeper node can be the answer, because the second climb visits its ancestors deepest first, so the first membership hit is the lowest shared ancestor:

1. Define `ancestors_of_p` as an empty set and climb from `p` to the root, adding every visited label (`p` itself included, since a node is an ancestor of itself).
2. Climb from `q` while `q` is not in `ancestors_of_p`.
3. Return the label where that climb stopped.

#### Walkthrough

Example 1, `parent = [-1,0,0,1,1,2,2,3]`, `p = 7`, `q = 4`:

```text
climb from 7   visit 7    ancestors_of_p = {7}
               visit 3    ancestors_of_p = {7, 3}
               visit 1    ancestors_of_p = {7, 3, 1}
               visit 0    ancestors_of_p = {7, 3, 1, 0}
climb from 4   4 not in set   continue
               1 in set       stop

answer 1
```

The second climb's first hit in `ancestors_of_p` is node `1`, matching the expected Output.

#### Solution

The code is the walkthrough written down: one loop pours `p`'s chain into the set, the other walks `q`'s chain until it lands in that set.

```python
from typing import List, Set


class Solution:
    def lowestCommonAncestor(self, parent: List[int], p: int, q: int) -> int:
        ancestors_of_p: Set[int] = set()
        node = p
        while node != -1:
            ancestors_of_p.add(node)
            node = parent[node]

        node = q
        while node not in ancestors_of_p:
            node = parent[node]
        return node
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(depth_p + depth_q)`

The first climb stops at the root and the second at the first shared ancestor; every step is one array read plus one set operation.

##### Space Complexity: `O(depth_p)`

The set holds one entry per node on `p`'s root path.

#### Key Insights

- Recording the whole first chain lets the second climb carry no state but its current label; the set membership test replaces all depth bookkeeping.
- Adding `p` itself to the set is what makes the "a node is an ancestor of itself" rule work for free: an ancestor-descendant query pair stops on the ancestor label without a special case.
- The second climb cannot overshoot: it stops at the first, that is deepest, node of `q`'s chain that `p`'s chain also holds.

## Comparison of Solutions

### Time Complexity

- **Depth-Equalized Climb**: `O(depth_p + depth_q)` - two measuring climbs plus one lift and one lockstep walk.
- **Ancestor-Set Climb**: `O(depth_p + depth_q)` - two walks with constant work per step.

### Space Complexity

- **Depth-Equalized Climb**: `O(1)` - two labels and two counters.
- **Ancestor-Set Climb**: `O(depth_p)` - one set holding `p`'s root path.

### Trade-offs

- **Depth-Equalized Climb**: constant extra space and no auxiliary structures, at the price of a three-phase loop whose phases must stay synchronized.
- **Ancestor-Set Climb**: the shortest correct program, with the self-ancestor rule and the equal-query case absorbed by the set; the price is `O(depth_p)` set memory.

### When to Use Each

- **Depth-Equalized Climb**: when memory is the binding constraint, or the tree arrives as a parent array in a language where a hash set per query is too expensive.
- **Ancestor-Set Climb (Recommended)**: the answer to give in an interview: two plain loops, no arithmetic to get wrong, and the statement's self-ancestor rule handled by construction.

### Optimization Notes

- Both climbs touch each root path at most twice, so both are optimal up to constants; asymptotic improvement would need preorder numbering plus ancestor checks per query, which pays only across many queries on a static tree.
- The `200000`-node bound makes a left-skewed chain the worst case for both approaches: two full-depth climbs, which is still one linear pass over the array.
- If the same tree faces many queries, one `O(n)` preorder pass that records each node's depth and euler position reduces every later query to two array lookups; the single-query climbs above stay simpler.
