# [Construct a Tree from Level-Order and Inorder Traversals](https://www.fastprep.io/problems/amazon-construct-tree-level-inorder)

**Hard** | **NN minutes** | **Array, Hash Table, Tree, Recursion, Stack**

Given the levelOrder and inorder traversals of the same binary tree, reconstruct and return its root.

All node values are distinct. Both arrays contain the same values, and together they describe exactly one valid binary tree.

## Examples

### Example 1

**Input:** `levelOrder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`

**Output:** `[3,9,20,null,null,15,7]`

**Explanation:** The root 3 appears first in level order; the inorder split places 9 left and the remaining nodes right.

### Example 2

**Input:** `levelOrder = [1]`, `inorder = [1]`

**Output:** `[1]`

**Explanation:** Both traversals describe a one-node tree.

### Example 3

**Input:** `levelOrder = [1,2,3,4,5]`, `inorder = [4,2,5,1,3]`

**Output:** `[1,2,3,4,5]`

**Explanation:** The traversals reconstruct the shown complete upper levels.

## Constraints

- `1 <= levelOrder.length == inorder.length <= 1200.`
- `-10^9 <= levelOrder[i], inorder[i] <= 10^9.`
- `Each traversal contains distinct values, and both contain the same set of values.`
- `The arrays are valid traversals of one binary tree.`

## Solutions

The solutions below assume the standard node definition:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Brute Force Partition

#### Derivation

The most literal reading exploits the one fact both traversals agree on: the first value of `levelOrder` is the root, and in `inorder` everything left of the root belongs to the left subtree while everything right belongs to the right subtree. Rebuilding recursively asks, for every subtree, which of the remaining level-order values go to each side. The honest way to answer it with no extra machinery is membership testing against the values the inorder split puts on the left:

1. `build(in_start, in_end, level)` rebuilds the subtree whose inorder slice is
   `inorder[in_start..in_end]` and whose level order is the list `level`; it
   returns `None` for an empty `level`.
2. Take `root_value = level[0]` and scan `inorder` from `in_start` until the scan
   lands on `root_value`; call that position `root_position`.
3. Collect `left_inorder_values`, the values in
   `inorder[in_start..root_position - 1]`, and split `level[1:]` by membership:
   values in the set go to `left_level`, the rest to `right_level`.
4. Recurse on `(in_start, root_position - 1, left_level)` for `root.left` and
   `(root_position + 1, in_end, right_level)` for `root.right`.

#### Walkthrough

Example 1, `levelOrder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`. The top call splits, and each child call splits again:

```text
build [3,9,20,15,7] / inorder [9,3,15,20,7]
  root 3 at inorder position 1
  left_inorder_values = {9}      -> left_level  = [9],   right_level = [20,15,7]
  build [9]  / inorder [9]
    root 9, left and right splits empty -> leaf
  build [20,15,7] / inorder [15,20,7]
    root 20 at inorder position 3
    left_inorder_values = {15}   -> left_level  = [15],  right_level = [7]
    build [15] -> leaf          build [7] -> leaf
```

Assembling the three pieces gives root `3` with left child `9` and right subtree `20(15, 7)`, exactly the structure of Example 1's Output. The membership scans are where the cost hides: finding `3` reads `inorder` from the start, and building `left_inorder_values` re-reads the slice at every level of the recursion.

#### Solution

The code is the walkthrough's split-and-recurse, with the inorder scan and the membership set spelled out:

```python
from typing import List, Optional


class Solution:
    def solve(self, levelOrder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """Rebuild the binary tree from its level-order and inorder traversals.

        Time:  O(n^2): each of the O(n) recursion nodes rescans its inorder
            window for the root and re-reads slices to build the membership
            set, for up to O(n) work per node.
        Space: O(n) for the level lists and membership sets handed down the
            recursion, plus O(h) recursion stack for a tree of height h.
        """

        def build(in_start: int, in_end: int, level: List[int]) -> Optional[TreeNode]:
            if not level:
                return None
            root_value = level[0]
            root = TreeNode(root_value)
            root_position = in_start
            while inorder[root_position] != root_value:
                root_position += 1
            left_inorder_values = {
                inorder[position] for position in range(in_start, root_position)
            }
            left_level: List[int] = []
            right_level: List[int] = []
            for value in level[1:]:
                if value in left_inorder_values:
                    left_level.append(value)
                else:
                    right_level.append(value)
            root.left = build(in_start, root_position - 1, left_level)
            root.right = build(root_position + 1, in_end, right_level)
            return root

        return build(0, len(inorder) - 1, levelOrder)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The recursion creates one call per tree node, and each call scans its inorder window for the root plus builds the membership set from slices, both `O(n)` at the top level.

##### Space Complexity: `O(n)`

Each recursion level hands down fresh `left_level` and `right_level` lists whose total length is the subtree size, and the stack itself grows to the tree height.

#### Key Insights

- The root's inorder position is the only structural fact the split needs; everything else is bookkeeping to route level-order values to the correct side.
- The membership test is correct because the two traversals share one value set: a level-order value is in the left subtree exactly when the inorder split placed it left of the root.
- The quadratic cost is duplicated scanning: the same inorder values are re-read and re-hashed at every ancestor, which is what the next approach removes.

### Hash Map Partition

#### Derivation

The brute force searches for the root in `inorder` by scanning and rebuilds the left-side membership set by re-reading a slice, at every recursion node. Both duties answer a position question, and positions never change: `inorder_position`, one dictionary from value to index built once, answers any root lookup in `O(1)`, and the left-side set is just the values whose positions fall in the window `[in_start, root_position)`. Building that set from positions is still slice-sized work, so the asymptotic gain lands on the lookups, not the split:

1. Build `inorder_position` once from the full `inorder` array.
2. In `build`, get `root_position = inorder_position[level[0]]` with no scan.
3. Collect `left_inorder_values` from `inorder[in_start..root_position - 1]`
   exactly as before, and split `level[1:]` by membership.
4. Recurse on the two windows as in the brute force.

#### Walkthrough

The dict changes the cost of each step, not the steps, so this walkthrough shows where the queue-split shortcut breaks and the membership split holds. The input is a tailored four-node tree (introduced as such, since no statement example exercises it) with `levelOrder = [1,2,5,3,4]` and `inorder = [4,3,2,1,5]`, a tree that leans left at every level:

```text
top: root 1 at position 3
  left_inorder_values = {4, 3, 2}    (positions 0..2)
  split [2,5,3,4]: 2 in set, 5 not, 3 in set, 4 in set
    left_level = [2, 3, 4]           right_level = [5]
```

A queue-split that fed `level[1:]` in order would take the first two values `[2, 5]` for a two-value left side and hand `[3, 4]` to the right: `5` would land in the right subtree although its inorder position `4` sits right of `1` but the left side already holds three values. The membership split routes `5` correctly, and the recursion completes as:

```text
build [2,3,4] / inorder [4,3,2]
  root 2 at position 2, left_inorder_values = {4, 3}
  split [3,4]: both in set -> left_level [3, 4], right_level []
  build [3,4] / inorder [4,3]: root 3, left [4], right []
    leaves 4 and (empty)            -> subtree 3(4, -)
build [5] -> leaf
```

The rebuilt tree is `1(2(3(4,-), -), 5)`, whose traversals reproduce both inputs. Example 1 rebuilds the same way, with each root lookup and each position test now `O(1)`.

#### Solution

The code is the brute force with the scan replaced by the dictionary and the split unchanged:

```python
from typing import Dict, List, Optional


class Solution:
    def solve(self, levelOrder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """Rebuild the binary tree from its level-order and inorder traversals.

        Time:  O(n^2) worst case: root lookups are O(1), but building the
            left-side membership set still reads an O(n) slice per
            recursion node on a skewed tree.
        Space: O(n) for the position dictionary, the per-call level lists
            and membership sets, plus O(h) recursion stack.
        """
        inorder_position: Dict[int, int] = {
            value: position for position, value in enumerate(inorder)
        }

        def build(in_start: int, in_end: int, level: List[int]) -> Optional[TreeNode]:
            if not level:
                return None
            root_value = level[0]
            root = TreeNode(root_value)
            root_position = inorder_position[root_value]
            left_inorder_values = {
                inorder[position] for position in range(in_start, root_position)
            }
            left_level: List[int] = []
            right_level: List[int] = []
            for value in level[1:]:
                if value in left_inorder_values:
                    left_level.append(value)
                else:
                    right_level.append(value)
            root.left = build(in_start, root_position - 1, left_level)
            root.right = build(root_position + 1, in_end, right_level)
            return root

        return build(0, len(inorder) - 1, levelOrder)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)` worst case

Root lookups drop to `O(1)`, but the membership set is rebuilt from an inorder slice at every recursion node; on a tree skewed so each left side holds most of the remaining values, that stays quadratic.

##### Space Complexity: `O(n)`

The position dictionary, the level lists descending the recursion, and the stack, which reaches the tree height.

#### Key Insights

- Replacing a scan with a dictionary speeds up constant factors but not the shape of the work: the split itself is still what costs.
- The queue-split shortcut is wrong on left-leaning trees: level-order values do not group by subtree position, so membership against the inorder window, not arrival order, must route each value.
- The approach is the natural interview middle ground: one dictionary, the same clear recursion, and correctness that is easy to argue, with the split cost left on the table for the next approach.

### Level-Synchronous Partition

#### Derivation

Both partition approaches pay for the split because they ask it per subtree, and the same inorder windows get rebuilt down the recursion. The repair is to answer every split at one depth in a single pass: the next `k` values of `levelOrder` after the ones already consumed fill the `k` child slots that exist at the current tree level, in slot order, and that order matches `levelOrder` exactly because both run left to right through the tree. So one sort positions each layer's values for `bisect`-style lookup, and each child claims its value by binary search on its own inorder window:

1. Build `inorder_position` once, and `root = TreeNode(levelOrder[0])` with the
   root's position from the map.
2. `pending` holds one `(node, in_start, root_position, in_end)` record per
   frontier node: its inorder window split by its own root position.
3. Loop while values remain: expand `pending` into `slots`, one
   `(node, in_start, in_end, attach_left)` per non-empty child window, left
   child first.
4. Sort `(inorder_position[value], value)` for the next `len(slots)` values of
   `levelOrder`, and assign slot `s` the value at sorted position `s`; binary
   search (`bisect_left` on the sorted pairs) finds the value whose position
   falls in the slot's window, which is unique because the windows partition the
   inorder line and the values are distinct.
5. Attach the child, record its `(child, in_start, child_position, in_end)` in
   the next `pending`, and advance the consumed count by `len(slots)`.

#### Walkthrough

Example 1, `levelOrder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`. The root consumes `3`; the frontier and slots then evolve one tree level at a time:

```text
consume 3 -> root 3, window (0, position 1, 4)
level 2: slots = [(3: window 0..0, left), (3: window 2..4, right)]
  sorted values (9,9), (15,15), (20,20), (7,7) -> positions 0,2,3,4
  slot 1 window 0..0 holds position 0 -> value 9   root 3.left = 9
  slot 2 window 2..4 holds position 2 -> value 20  root 3.right = 20
  pending = [(9, 0, 0, 0), (20, 2, 3, 4)]
level 3: slots = [(20: 2..2, left), (20: 4..4, right)]   leaf 9 has no windows
  slot 1 -> position 2 -> value 15   20.left = 15
  slot 2 -> position 4 -> value 7    20.right = 7
  consumed 5 of 5 -> stop
```

Each layer's values were assigned to the unique slot whose inorder window contains them, producing `3(9, 20(15, 7))`, the structure of Example 1's Output. No value was ever compared against a rebuilt set: the sorted positions answered every assignment.

#### Solution

The code is the layer loop from the walkthrough: expand slots, sort the layer's values by inorder position, and binary-search each slot's value.

```python
from bisect import bisect_left
from typing import List, Optional, Tuple


class Solution:
    def solve(self, levelOrder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """Rebuild the binary tree from its level-order and inorder traversals.

        Time:  O(n log n): the root lookups, window checks, and binary
            searches are O(log n) or O(1) per node, and the one sort of
            each layer's values is O(n log n) total.
        Space: O(n) for the position map, the sorted layer, and the
            frontier records.
        """
        total_values = len(levelOrder)
        inorder_position = {value: position for position, value in enumerate(inorder)}
        root_position = inorder_position[levelOrder[0]]
        root = TreeNode(levelOrder[0])
        pending: List[Tuple[TreeNode, int, int, int]] = [
            (root, 0, root_position, total_values - 1)
        ]
        consumed = 1

        while consumed < total_values and pending:
            slots: List[Tuple[TreeNode, int, int, bool]] = []
            for node, in_start, node_position, in_end in pending:
                if in_start <= node_position - 1:
                    slots.append((node, in_start, node_position - 1, True))
                if node_position + 1 <= in_end:
                    slots.append((node, node_position + 1, in_end, False))
            if not slots:
                break

            layer_values = levelOrder[consumed:consumed + len(slots)]
            sorted_pairs = sorted(
                (inorder_position[value], value) for value in layer_values
            )
            next_pending: List[Tuple[TreeNode, int, int, int]] = []
            for node, in_start, in_end, attach_left in slots:
                spot = bisect_left(sorted_pairs, (in_start, -10**18))
                child_value = sorted_pairs[spot][1]
                child = TreeNode(child_value)
                if attach_left:
                    node.left = child
                else:
                    node.right = child
                child_position = inorder_position[child_value]
                next_pending.append((child, in_start, child_position, in_end))

            consumed += len(slots)
            pending = next_pending

        return root
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Every node is created once and handled in exactly one layer; per node the work is an `O(log n)` binary search plus constant bookkeeping, and the per-layer sorts sum to `O(n log n)`.

##### Space Complexity: `O(n)`

The position dictionary, the current layer's sorted pairs, and the frontier records each hold `O(n)` entries at worst.

#### Key Insights

- Level order and the child-slot order traverse the tree in the same left-to-right sweep, so a whole depth of splits collapses into "match the next `k` values to the next `k` slots".
- The inorder windows of the slots at one level are disjoint and ordered, which is exactly the precondition binary search needs: the window containing a value's position is unique.
- The sentinel `bisect_left` key `(in_start, -10**18)` lands on the first pair whose position is at least the window start; the distinct values and the exact partition make the found position automatically within the window.
- The iterative frontier also removes the recursion of the earlier approaches, whose stack depth equals the tree height and strains Python's default recursion limit at `n` near 1200 on a skewed tree.

### Insert by Inorder Position

#### Derivation

Every approach so far maintains frontier bookkeeping to decide where each level-order value belongs. One structural fact shortens that to a per-value walk: in the inorder line, a node's left subtree occupies exactly the positions left of it and its right subtree the positions right of it. So attaching a new value `value` needs only one comparison per visited node, `inorder_position[value]` against `inorder_position[node.val]`: smaller descends left, otherwise right, and the first empty child along that path is the attach point. Processing `levelOrder` in order makes each insertion land at the position the true tree assigns it, because a value's true ancestors are exactly the previously inserted values whose windows still contain its position:

1. Build `inorder_position` once and create the root from `levelOrder[0]`.
2. For each value in `levelOrder[1:]`, start at the root and walk: when
   `inorder_position[value] < inorder_position[node.val]`, take the left child,
   otherwise the right child.
3. When the chosen child slot is empty, attach a new `TreeNode(value)` and stop
   the walk.
4. Return the root after every value is inserted.

#### Walkthrough

Example 1, `levelOrder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`, with positions `9 -> 0, 3 -> 1, 15 -> 2, 20 -> 3, 7 -> 4`. Each row is one insertion with its descent:

```text
insert 9  (position 0): 9 < 3's position 1 -> left of 3 empty     3.left  = 9
insert 20 (position 3): 3 > 1 -> right of 3 empty                 3.right = 20
insert 15 (position 2): 2 < 1? no  -> right of 3 is 20
                        2 < 20's position 3 -> left of 20 empty   20.left = 15
insert 7  (position 4): 4 < 1? no  -> right of 3 is 20
                        4 < 3? no -> right of 20 empty            20.right = 7
```

The walks reproduce the structure `3(9, 20(15, 7))` from Example 1's Output with no frontier at all: value `15` found its place because `3` and `20`, its two true ancestors, were already in the tree when it arrived.

#### Solution

The code is the per-value descent from the walkthrough:

```python
from typing import Dict, List, Optional


class Solution:
    def solve(self, levelOrder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """Rebuild the binary tree from its level-order and inorder traversals.

        Time:  O(n * h) where h is the tree height: each of the n
            insertions walks one root-to-attach path of at most h nodes.
        Space: O(n) for the position map and the tree itself; the walk
            uses no auxiliary structure.
        """
        inorder_position: Dict[int, int] = {
            value: position for position, value in enumerate(inorder)
        }
        root = TreeNode(levelOrder[0])
        for value in levelOrder[1:]:
            child = TreeNode(value)
            node = root
            while True:
                if inorder_position[value] < inorder_position[node.val]:
                    if node.left is None:
                        node.left = child
                        break
                    node = node.left
                else:
                    if node.right is None:
                        node.right = child
                        break
                    node = node.right
        return root
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × h)`

Each of the `n - 1` insertions descends one path whose length is at most the tree height `h`; a balanced tree gives `O(n log n)` and a skewed tree degrades to `O(n^2)`.

##### Space Complexity: `O(n)`

The position dictionary and the output tree; the insertion walk itself holds only the current node.

#### Key Insights

- The inorder position acts as a total order, so rebuilding becomes binary-search-tree insertion under that order; the result is the unique tree both traversals describe, not merely a BST.
- Insertion order does the work the frontier did: a value can only be claimed by ancestors inserted earlier, and earlier ancestors are exactly the nodes its descent visits.
- The approach has the shortest code of the four and no recursion, but the insertion path length, not `n`, is the cost driver, so adversarial inputs pay quadratically.
- A queue-based shortcut that walks children in level-order arrival order instead of comparing inorder positions builds wrong trees on left-leaning inputs, the same trap the Hash Map Partition walkthrough exposes.

## Comparison of Solutions

### Time Complexity

- **Brute Force Partition**: `O(n^2)` - each recursion node rescans its inorder window and rebuilds a membership set from slices.
- **Hash Map Partition**: `O(n^2)` worst case - `O(1)` root lookups, but the membership set still reads an `O(n)` slice per node on skewed inputs.
- **Level-Synchronous Partition**: `O(n log n)` - one sorted layer plus one binary search per node.
- **Insert by Inorder Position**: `O(n × h)` - one root-to-attach walk per value, `O(n log n)` balanced, `O(n^2)` skewed.

### Space Complexity

- **Brute Force Partition**: `O(n)` - per-call level lists and membership sets plus the recursion stack.
- **Hash Map Partition**: `O(n)` - position dictionary, level lists, membership sets, and the stack.
- **Level-Synchronous Partition**: `O(n)` - position dictionary, sorted layer, and frontier records, with no recursion.
- **Insert by Inorder Position**: `O(n)` - position dictionary and the output tree; the walk itself is `O(1)`.

### Trade-offs

- **Brute Force Partition**: the clearest transcription of the root-split fact, but duplicated scanning makes it the slowest on every input shape.
- **Hash Map Partition**: keeps the readable recursion and removes lookup cost, while the split remains the bottleneck.
- **Level-Synchronous Partition**: the best worst-case bound and an iterative frontier that cannot hit recursion limits, paid for with the most intricate bookkeeping.
- **Insert by Inorder Position**: the least code and no per-level machinery, but its runtime follows the tree height and degrades on skewed inputs.

### When to Use Each

- **Brute Force Partition**: to state the core idea in an interview before optimizing, or on tiny inputs where clarity is everything.
- **Hash Map Partition (Recommended as the first improvement)**: the default interview answer: one dictionary, one recursion, and a correctness argument that fits in a sentence.
- **Level-Synchronous Partition**: when the worst case matters, when the tree may be skewed near the full `n = 1200`, or when recursion depth is a hazard.
- **Insert by Inorder Position**: when code size matters more than worst-case guarantees, for example a quick reconstruction in tests or tooling.

### Optimization Notes

- The position dictionary is built once in every approach after the brute force; rebuilding it per call is the first thing to strike in a review.
- In the Level-Synchronous Partition, the sentinel key `(in_start, -10**18)` in `bisect_left` must be smaller than any real pair `(position, value)`; with values bounded by `10^9` in magnitude it never collides with a real entry.
- The Insert by Inorder Position walk never needs parent pointers or rebalancing: the true tree is unique, so plain descent lands on the exact node the original tree had.
- All four approaches rely on distinct values, which the constraints guarantee; with duplicates, inorder positions would be ambiguous and none of the partitions would be well defined.
