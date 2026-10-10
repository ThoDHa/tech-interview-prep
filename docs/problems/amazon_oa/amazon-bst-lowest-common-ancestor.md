# [Lowest Common Ancestor in an Inserted BST](https://www.fastprep.io/problems/amazon-bst-lowest-common-ancestor)

**Easy** | **NN minutes** | **Tree, Binary Search**

Build a binary search tree by inserting the distinct values of insertionOrder from left to right. For each insertion, values smaller than the current node go left and larger values go right.

Return the value of the lowest common ancestor of the nodes containing p and q. A node may be an ancestor of itself.

## Examples

### Example 1

**Input:** `insertionOrder = [6,2,8,0,4,7,9,3,5]`, `p = 2`, `q = 8`

**Output:** `6`

**Explanation:** The two nodes lie on opposite sides of the root, so 6 is their lowest common ancestor.

### Example 2

**Input:** `insertionOrder = [6,2,8,0,4,7,9,3,5]`, `p = 2`, `q = 4`

**Output:** `2`

**Explanation:** The node containing 2 is an ancestor of the node containing 4.

### Example 3

**Input:** `insertionOrder = [5]`, `p = 5`, `q = 5`

**Output:** `5`

**Explanation:** A node is its own lowest common ancestor.

## Constraints

- `1 <= insertionOrder.length <= 100000.`
- `All values in insertionOrder are distinct integers.`
- `p and q both appear in insertionOrder.`

## Solutions

### Build Then Walk Ancestor Sets

#### Derivation

The most literal route materializes what the words describe: insert every value into a binary search tree, then find the lowest common ancestor by set membership. Record each node's parent while inserting. The ancestors of `p` (the chain from `p`'s node up to the root) form a set; walking from `q`'s node upward, the first node in that set is the lowest common ancestor:

1. Insert values left to right, keeping a `parent` map.
2. Collect the ancestor chain of `p` into a set.
3. Walk from `q` upward until a node appears in the set; return its value.

#### Walkthrough

Example 1, `insertionOrder = [6,2,8,0,4,7,9,3,5]`, `p = 2`, `q = 8`: the chain above 2 is `2 -> 6`. Walking up from 8 reaches `8 -> 6`; the first shared node is `6`, the expected output. Example 2, `p = 2`, `q = 4`: the chain above 4 is `4 -> 2 -> 6`, which already contains `2`, so the walk from `q = 4` finds `2` at its second step, matching the expected `2`. Example 3, the single-node tree `[5]` with `p = q = 5`: the ancestor set of 5 contains 5 itself, so the answer is `5`, confirming a node may be its own ancestor.

#### Solution

```python
from typing import Dict, List


class Solution:
    def solve(self, insertionOrder: List[int], p: int, q: int) -> int:
        """Return the lowest common ancestor value in the inserted BST.

        Time:  O(h) per ancestor walk after O(n * h) construction, with
            h the tree height (n log n when values arrive randomly).
        Space: O(n) for the node and parent maps.
        """
        if not insertionOrder:
            raise ValueError("insertionOrder must be nonempty")

        children: Dict[int, List] = {}
        for value in insertionOrder:
            if value in children:
                continue
            children[value] = [None, None]
        parent: Dict[int, int] = {}
        for value in insertionOrder:
            node = insertionOrder[0]
            while node != value:
                side = 0 if value < node else 1
                nxt = children[node][side]
                if nxt is None:
                    children[node][side] = value
                    parent[value] = node
                    break
                node = nxt
        p_ancestors = {p}
        current = p
        while current in parent:
            current = parent[current]
            p_ancestors.add(current)
        current = q
        while current not in p_ancestors:
            current = parent[current]
        return current
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * h)` for construction plus `O(h)` for the walks

Each insertion descends one root-to-leaf path of height `h`; `h` is `O(log n)` for random orders and `O(n)` for sorted ones.

##### Space Complexity: `O(n)`

The children map, the parent map, and the ancestor set.

#### Key Insights

- Parent pointers invert the tree into two upward chains, and the lowest common ancestor is exactly their first intersection.
- A node is its own ancestor: `p`'s chain includes `p` itself, so `p = q` or direct ancestor queries fall out without special cases.

### Descend From the Root

#### Derivation

The BST property gives a direct characterization: at a node with value `node_value`, if both `p` and `q` are smaller the common ancestor lies in the left subtree; if both are larger it lies in the right subtree; the moment they sit on opposite sides (or one equals `node_value`) that node is the lowest common ancestor. So after building the tree, start at the root and branch on the comparison; no ancestor sets are needed. Building can also skip the children map: each query only needs the walk structure, and for repeated queries the tree could be kept, but a single query is served by building and walking once:

1. Insert all values as before (the same `O(n * h)` construction).
2. From the root, while both targets are below the current node on the same side, step that way.
3. Stop and return the current value at the first split.

#### Walkthrough

Example 1, tree root `6`, `p = 2 < 6`, `q = 8 > 6`: opposite sides at the root, so the walk stops immediately and returns `6`. Example 2, `p = 2`, `q = 4`: both are below `6` on the left, step to `2`; now `p` equals the node value, a split, so return `2`. Example 3, the one-node tree: `p = q = 5` equals the root, return `5`.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, insertionOrder: List[int], p: int, q: int) -> int:
        """Return the lowest common ancestor value in the inserted BST.

        Time:  O(n * h) to build (h is the tree height), O(h) to descend.
        Space: O(n) for the tree maps.
        """
        children = {}
        root_value = insertionOrder[0]
        for value in insertionOrder:
            if value in children:
                continue
            if value != root_value:
                node = root_value
                while True:
                    side = 0 if value < node else 1
                    nxt = children.get(node, [None, None])[side]
                    if nxt is None:
                        children.setdefault(node, [None, None])[side] = value
                        break
                    node = nxt
            children[value] = children.get(value, [None, None])
        node = root_value
        while True:
            if p < node and q < node:
                node = children[node][0]
            elif p > node and q > node:
                node = children[node][1]
            else:
                return node
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * h)` construction plus `O(h)` descent

Same insertion cost as the baseline; the ancestor walk is replaced by a single root-down branch.

##### Space Complexity: `O(n)`

The children map only; no parent map or ancestor set.

#### Key Insights

- The BST ordering replaces set bookkeeping with three comparisons per step: both-left, both-right, or split.
- The split condition covers equality: when `p` equals the current value, the pair cannot lie strictly on one side, so the current node is the answer.

## Comparison of Solutions

### Time Complexity

- **Build Then Walk Ancestor Sets**: `O(n * h)` build, `O(h)` walk with an `O(h)` set.
- **Descend From the Root**: `O(n * h)` build, `O(h)` descent, no set.

### Space Complexity

- **Build Then Walk Ancestor Sets**: `O(n)` maps plus `O(h)` ancestor set.
- **Descend From the Root**: `O(n)` map only.

### Trade-offs

- The ancestor-set version generalizes to any tree with parent pointers, BST or not.
- The root-descent version needs the BST property but carries less state and answers repeated queries without rebuilding chains.

### When to Use Each

- **Build Then Walk Ancestor Sets**: when parent pointers already exist or the tree is not ordered.
- **Descend From the Root**: the interview default for BSTs; shorter code, less memory, same asymptotics.

### Optimization Notes

- Construction dominates both rungs; a balanced insertion order (or an AVL/redo-black tree) would cap `h` at `O(log n)`, but the problem fixes the insertion order, so worst-case `h = n` stands.
- With `insertionOrder.length <= 100000`, sorted input makes the quadratic construction the real constraint to name in an interview.
