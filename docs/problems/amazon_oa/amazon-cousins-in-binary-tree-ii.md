# [Cousins in Binary Tree II](https://www.fastprep.io/problems/amazon-cousins-in-binary-tree-ii)

**Medium** | **NN minutes** | **Tree, Breadth First Search, Depth First Search**

You are given a non-empty binary tree serialized as a level-order string array levelOrder. Each non-null token is a decimal integer, and "null" denotes a missing child.

Replace every node's value with the sum of the original values of all its cousins. Two nodes are cousins when they are at the same depth and have different parents. If a node has no cousins, its replacement value is 0.

All replacements are conceptually simultaneous. Return the updated tree using the same level-order array shape, preserving every "null" marker from the input.

## Examples

### Example 1

**Input:** `levelOrder = ["5","4","9","1","10","null","7"]`

**Output:** `["0","0","0","7","7","null","11"]`

**Explanation:** At depth 2, nodes 1 and 10 are siblings, so their only cousin has value 7. Node 7 has cousins with original values 1 and 10, whose sum is 11.

### Example 2

**Input:** `levelOrder = ["3","1","2"]`

**Output:** `["0","0","0"]`

**Explanation:** The root has no cousins, and the two nodes at depth 1 are siblings, so every replacement is 0.

### Example 3

**Input:** `levelOrder = ["1","2","3","4","null","5","6"]`

**Output:** `["0","0","0","11","null","4","4"]`

**Explanation:** At depth 2, node 4 receives 5 + 6 = 11, while sibling nodes 5 and 6 each receive the cousin value 4.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-cousins-in-binary-tree-ii; fill them in. -->

## Solutions

The solutions below assume the standard node definition:

```python
from typing import Optional


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: "Optional[TreeNode]" = None,
        right: "Optional[TreeNode]" = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right
```

### BFS with Pairwise Cousin Scan

#### Derivation

The definition is the algorithm's first draft: a node's cousins are the nodes at its own depth with a different parent. So the most literal reading is: walk the tree level by level, and for every node of a level re-scan that level, summing the values of the nodes whose parent differs. The scan is wasteful but it is also obviously faithful to the statement, which makes it the right baseline to stand the faster solutions against:

1. Parse `levelOrder` into a `root` plus `nodes_by_slot`, the tree node (or
   `None`) that occupies each input token, so the output can reuse the exact
   input shape including every `"null"`.
2. Put `(root, None)` in a queue, where the second field is the parent node.
3. Drain the queue one level at a time: read `current_level` as a snapshot,
   then compute each node's replacement as the sum of `neighbor.val` over
   nodes in `current_level` with `neighbor_parent is not parent`; collect the
   sums in `replacements` and assign them only after the whole level is
   scanned, so every sum reads the original values the statement's
   simultaneous replacement implies.
4. Enqueue `(child, node)` for every child of every node of `current_level`.
5. When the queue empties, emit `str(node.val)` for every occupied slot and
   `"null"` for every null marker.

#### Walkthrough

Example 3, `levelOrder = ["1","2","3","4","null","5","6"]`, parses into root `1` with children `2` and `3`; node `2` has left child `4`; node `3` has children `5` and `6`. The queue processes two levels after the root:

```text
level 1:  current_level = [(2, parent 1), (3, parent 1)]
          node 2: scan -> 3 has parent 1 (same) -> no cousins -> 2.val = 0
          node 3: scan -> 2 has parent 1 (same) -> no cousins -> 3.val = 0
          enqueue (4, 2), (5, 3), (6, 3)
level 2:  current_level = [(4, parent 2), (5, parent 3), (6, parent 3)]
          node 4: scan -> 5 (parent 3) + 6 (parent 3) = 11 -> 4.val = 11
          node 5: scan -> 4 (parent 2, different) = 4 -> 5.val = 4
          node 6: scan -> 4 (parent 2, different) = 4 -> 6.val = 4
```

Node `4` meets two different-parent nodes and sums to `11`; nodes `5` and `6` are siblings, so each finds only node `4` on the other side of the parent test. Emitting the slots in input order gives `["0","0","0","11","null","4","4"]`, matching the expected Output.

#### Solution

The code is the level snapshot with the pairwise parent test from the walkthrough, wrapped in the parse and emit that keep the array shape.

```python
from collections import deque
from typing import List, Optional
class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: "Optional[TreeNode]" = None,
        right: "Optional[TreeNode]" = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def solve(self, levelOrder: List[str]) -> List[str]:
        nodes_by_slot: List[Optional[TreeNode]] = [None] * len(levelOrder)
        root = TreeNode(int(levelOrder[0]))
        nodes_by_slot[0] = root
        queue = deque([root])
        slot = 1
        while queue and slot < len(levelOrder):
            parent = queue.popleft()
            if levelOrder[slot] != "null":
                parent.left = TreeNode(int(levelOrder[slot]))
                nodes_by_slot[slot] = parent.left
                queue.append(parent.left)
            slot += 1
            if slot < len(levelOrder):
                if levelOrder[slot] != "null":
                    parent.right = TreeNode(int(levelOrder[slot]))
                    nodes_by_slot[slot] = parent.right
                    queue.append(parent.right)
                slot += 1

        root.val = 0
        level_queue = deque([(root, None)])
        while level_queue:
            current_level = list(level_queue)
            level_queue.clear()
            replacements = []
            for node_index, (node, parent) in enumerate(current_level):
                cousin_sum = 0
                for neighbor_index, (neighbor, neighbor_parent) in enumerate(current_level):
                    if neighbor_index != node_index and neighbor_parent is not parent:
                        cousin_sum += neighbor.val
                replacements.append((node, cousin_sum))
            for node, cousin_sum in replacements:
                node.val = cousin_sum
            for node, _ in current_level:
                for child in (node.left, node.right):
                    if child is not None:
                        level_queue.append((child, node))

        return [
            token if token == "null" else str(nodes_by_slot[position].val)
            for position, token in enumerate(levelOrder)
        ]

```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Parsing, emitting, and every queue operation are linear, but each level of width `w` runs a pairwise scan costing `O(w^2)`; a complete tree packs most of its `n` nodes into the last level, so the squared term reaches `O(n^2)`.

##### Space Complexity: `O(n)`

The parsed nodes, `nodes_by_slot`, and the queue, which holds one level at a time.

#### Key Insights

- The definition translates directly into a two-field queue entry `(node, parent)`: the parent reference is what turns "different parent" into an identity check `is not`.
- Siblings are excluded by the same test, since they share the parent object; no separate sibling logic is needed.
- The sums must be collected into `replacements` and assigned after the level scan: assigning during the scan would let node `7` of Example 1 read the already-overwritten `7, 7` and produce `14` instead of `11`.
- The quadratic blowup hides in the repeated rescans of one level: each node's answer recomputes information the level as a whole already contains.

### BFS with Level Sum and Sibling Groups

#### Derivation

The pairwise scan re-adds the same level total once per node. The repair is arithmetic, not a new traversal: every node of a level belongs to exactly one sibling group (the children of one parent), and each group's internal sum can be computed once. Then the identity `cousin_sum = level_sum - sibling_group_sum` follows because a level splits into disjoint sibling groups, and the groups other than your own are precisely your cousins. One pass computes the level sum, one subtraction replaces the scan:

1. Parse `levelOrder` and build `nodes_by_slot` as before; set `root.val = 0`.
2. Hold the current level as a plain list of nodes. Compute `next_level` as
   the list of all children, then `next_level_sum` as the sum of their values.
3. For each node of the current level, read its children's values (still
   original) into `sibling_sum`, then overwrite each child with
   `next_level_sum - sibling_sum`.
4. Advance `current_level = next_level` and repeat until it is empty.
5. Emit values through `nodes_by_slot`, preserving every `"null"` marker.

#### Walkthrough

Example 1, `levelOrder = ["5","4","9","1","10","null","7"]`, parses into root `5` (children `4`, `9`), where `4` has children `1` and `10` and `9` has children `"null"` and `7`. Root set to `0`, then two level rounds:

```text
round 1   current_level = [4, 9]
          next_level = [1, 10, 7]   next_level_sum = 18
          node 4: children 1 + 10 -> sibling_sum = 11 -> 1.val = 18 - 11 = 7
                                                 -> 10.val = 18 - 11 = 7
          node 9: children 0 + 7  -> sibling_sum = 7  -> 7.val = 18 - 7 = 11
round 2   current_level = [1, 10, 7]
          next_level = []           next_level_sum = 0
          no children to overwrite
```

Nodes `1` and `10` are siblings, so both receive the same cousin value `7` (the level sum `18` minus their shared group `11`); node `7` stands alone under parent `9` and receives `18 - 7 = 11`. The emit reads `["0","0","0","7","7","null","11"]`, matching the expected Output.

#### Solution

The code is the walkthrough's per-level bookkeeping: sum first, then overwrite through each parent's sibling group.

```python
from collections import deque
from typing import List, Optional
class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: "Optional[TreeNode]" = None,
        right: "Optional[TreeNode]" = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def solve(self, levelOrder: List[str]) -> List[str]:
        nodes_by_slot: List[Optional[TreeNode]] = [None] * len(levelOrder)
        root = TreeNode(int(levelOrder[0]))
        nodes_by_slot[0] = root
        queue = deque([root])
        slot = 1
        while queue and slot < len(levelOrder):
            parent = queue.popleft()
            if levelOrder[slot] != "null":
                parent.left = TreeNode(int(levelOrder[slot]))
                nodes_by_slot[slot] = parent.left
                queue.append(parent.left)
            slot += 1
            if slot < len(levelOrder):
                if levelOrder[slot] != "null":
                    parent.right = TreeNode(int(levelOrder[slot]))
                    nodes_by_slot[slot] = parent.right
                    queue.append(parent.right)
                slot += 1

        root.val = 0
        current_level = [root]
        while current_level:
            next_level = [
                child
                for node in current_level
                for child in (node.left, node.right)
                if child is not None
            ]
            next_level_sum = sum(child.val for child in next_level)
            for node in current_level:
                sibling_sum = (node.left.val if node.left else 0) + (
                    node.right.val if node.right else 0
                )
                if node.left:
                    node.left.val = next_level_sum - sibling_sum
                if node.right:
                    node.right.val = next_level_sum - sibling_sum
            current_level = next_level

        return [
            token if token == "null" else str(nodes_by_slot[position].val)
            for position, token in enumerate(levelOrder)
        ]

```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Parsing and emitting are linear; each round does constant work per node (each node enters `next_level` once, is summed once, and is overwritten once), so every node is touched a bounded number of times.

##### Space Complexity: `O(n)`

The parsed tree, `nodes_by_slot`, and the per-level lists, which never exceed `n` entries in total.

#### Key Insights

- `cousin_sum = level_sum - sibling_group_sum` restates the definition as arithmetic: the level is partitioned into sibling groups, and everything outside your group is your cousins.
- Reading each child's original value just before overwriting it is safe because a node's children are read and overwritten only by that node's own iteration; `next_level_sum` is summed before any write.
- The deepest level costs nothing: with an empty `next_level`, the round rewrites no children and the loop ends.

### DFS with Depth Sums

#### Derivation

The level rounds of the previous solution are one way to group by depth; a [depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) reaches the same grouping without building level lists. Run two passes. Pass one accumulates `depth_sums[depth]`, the total of the original values at each depth, in the order the DFS first reaches each depth. Pass two walks the tree again and applies the same identity as before, read from the parent's seat: the children of one node form one sibling group, so both children receive `depth_sums[depth + 1] - (left_val + right_val)`. Each child is read and overwritten by its own parent's visit, so the original values survive exactly long enough:

1. `collect(node, depth)` appends a new bucket when `depth == len(depth_sums)`
   and adds `node.val` to `depth_sums[depth]`, recursing to both children.
2. Set `root.val = 0`: depth `0` holds no nodes other than the root itself.
3. `replace(node, depth)` reads `left_val` and `right_val` (original, since
   only this visit writes them), assigns each existing child
   `depth_sums[depth + 1] - left_val - right_val`, then recurses into both
   children at `depth + 1`.
4. Emit through `nodes_by_slot` as in the earlier solutions.

#### Walkthrough

Example 1 again. Pass one builds `depth_sums` from the original values `[5, 4, 9, 1, 10, 7]`:

```text
collect: depth 0 <- 5      depth_sums = [5]
         depth 1 <- 4, 9   depth_sums = [5, 13]
         depth 2 <- 1, 10, 7   depth_sums = [5, 13, 18]
```

Pass two walks in the same order, reading children before overwriting them:

```text
root 5:    root.val = 0
replace(5, 0):  left_val 4, right_val 9 -> 4.val = 13 - 13 = 0
                                           9.val = 13 - 13 = 0
replace(4, 1):  left_val 1, right_val 10 -> 1.val  = 18 - 11 = 7
                                            10.val = 18 - 11 = 7
replace(9, 1):  left_val 0, right_val 7 -> 7.val  = 18 - 7 = 11
replace(1, 2) / (10, 2) / (7, 2):  leaves, no children to rewrite
```

The root's bucket `5` never enters the arithmetic because depth `0` has one node and no cousins, which is exactly the explicit `root.val = 0`. The depth-2 writes reproduce the BFS result: `1` and `10` share the sibling sum `11`, node `7` keeps the whole `18` minus its own `7`. The emit returns `["0","0","0","7","7","null","11"]`, matching the expected Output.

#### Solution

The code is the two walks from the trace: `collect` totals each depth, `replace` redistributes each depth through the parents.

```python
from collections import deque
from typing import List, Optional
class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: "Optional[TreeNode]" = None,
        right: "Optional[TreeNode]" = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def solve(self, levelOrder: List[str]) -> List[str]:
        nodes_by_slot: List[Optional[TreeNode]] = [None] * len(levelOrder)
        root = TreeNode(int(levelOrder[0]))
        nodes_by_slot[0] = root
        queue = deque([root])
        slot = 1
        while queue and slot < len(levelOrder):
            parent = queue.popleft()
            if levelOrder[slot] != "null":
                parent.left = TreeNode(int(levelOrder[slot]))
                nodes_by_slot[slot] = parent.left
                queue.append(parent.left)
            slot += 1
            if slot < len(levelOrder):
                if levelOrder[slot] != "null":
                    parent.right = TreeNode(int(levelOrder[slot]))
                    nodes_by_slot[slot] = parent.right
                    queue.append(parent.right)
                slot += 1

        depth_sums: List[int] = []

        def collect(node: Optional[TreeNode], depth: int) -> None:
            if node is None:
                return
            if depth == len(depth_sums):
                depth_sums.append(0)
            depth_sums[depth] += node.val
            collect(node.left, depth + 1)
            collect(node.right, depth + 1)

        def replace(node: Optional[TreeNode], depth: int) -> None:
            if node is None:
                return
            left_val = node.left.val if node.left else 0
            right_val = node.right.val if node.right else 0
            if node.left:
                node.left.val = depth_sums[depth + 1] - left_val - right_val
            if node.right:
                node.right.val = depth_sums[depth + 1] - left_val - right_val
            replace(node.left, depth + 1)
            replace(node.right, depth + 1)

        collect(root, 0)
        root.val = 0
        replace(root, 0)

        return [
            token if token == "null" else str(nodes_by_slot[position].val)
            for position, token in enumerate(levelOrder)
        ]

```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Both passes visit every node once with constant work per visit, on top of the linear parse and emit.

##### Space Complexity: `O(n)`

The parsed tree, `nodes_by_slot`, and `depth_sums`, which holds one entry per depth; the recursion stack adds the tree height, at most `n` on a degenerate chain.

#### Key Insights

- Depth totals replace level lists: `depth_sums` is all the level information the identity needs, collected in one pre-order sweep.
- Viewing the identity from the parent (`both children get the same replacement`) lets one subtraction serve a whole sibling group.
- A degenerate chain drives the recursion stack to `n` frames; BFS with Level Sum and Sibling Groups is the safer pick when the input tree can be a long chain.

## Comparison of Solutions

### Time Complexity

- **BFS with Pairwise Cousin Scan**: `O(n^2)` - each level of width `w` pays `O(w^2)` for the pairwise scan, quadratic on complete trees.
- **BFS with Level Sum and Sibling Groups**: `O(n)` - every node is enqueued, summed, and overwritten a constant number of times.
- **DFS with Depth Sums**: `O(n)` - two constant-work visits per node plus the linear parse and emit.

### Space Complexity

- **BFS with Pairwise Cousin Scan**: `O(n)` - parsed tree, slot map, and a queue holding at most one level.
- **BFS with Level Sum and Sibling Groups**: `O(n)` - parsed tree, slot map, and per-level lists.
- **DFS with Depth Sums**: `O(n)` - parsed tree, slot map, one bucket per depth, plus a recursion stack as tall as the tree.

### Trade-offs

- **BFS with Pairwise Cousin Scan**: the definition written as loops, with no identity to prove, but it rescans each level once per node and degrades quadratically exactly when the tree is bushiest.
- **BFS with Level Sum and Sibling Groups**: linear, iterative, and stack-safe, at the cost of ordering the writes so originals survive (`next_level_sum` first, per-parent reads before writes).
- **DFS with Depth Sums**: linear with the smallest working set per level (a running list of depth totals instead of level lists), but recursive and therefore height-sensitive.

### When to Use Each

- **BFS with Pairwise Cousin Scan**: as the baseline you quote from the definition and diff against; acceptable when levels are known to be narrow.
- **BFS with Level Sum and Sibling Groups (Recommended)**: the interview answer: linear, iterative, and the identity `cousin_sum = level_sum - sibling_group_sum` is easy to state and defend.
- **DFS with Depth Sums**: when the input arrives as a tree you already traverse recursively, or when you prefer accumulating depth totals to building level lists.

### Optimization Notes

- The parse maps every input slot to the node occupying it (`nodes_by_slot`), which makes the emit a single comprehension and preserves every `"null"` marker for free; serializing the tree back into level order by hand would re-derive the shape it must already match.
- A null token consumes its slot during parsing but enqueues nothing, so the slot counter must advance even when a child is missing.
- The root is set to `0` explicitly in every solution: no formula covers depth `0`, because the root's only potential "group" is itself.
- If the interviewer asks for the tree object instead of the array, all three solutions already maintain it; only the emit line changes.
