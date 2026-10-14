# [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)

**Medium** | **20 minutes** | **Tree, BFS, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)

**Practice:** [`practice/binary_tree_level_order_traversal/solution.py`](../../practice/binary_tree_level_order_traversal/solution.py)

Given the `root` of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

## Examples

### Example 1

![Binary Tree Example](assets/binary_tree_level_order_traversal_example1.jpg)

**Input:** `root = [3,9,20,null,null,15,7]`

**Output:** `[[3],[9,20],[15,7]]`

### Example 2

**Input:** `root = [1]`

**Output:** `[[1]]`

### Example 3

**Input:** `root = []`

**Output:** `[]`

## Constraints

- The number of nodes in the tree is in the range `[0, 2000]`.
- `-1000 <= Node.val <= 1000`

## Deriving the Solution

The output is the tree's values grouped by depth, left to right within each group. Every solution below visits all `n` nodes exactly once; what separates them is *when* the grouping by depth happens: after the walk, during a depth-carrying walk, or by walking in level order to begin with.

1. **Start literal.** Treat visiting and grouping as two separate jobs: walk the tree recording each value together with its depth, then bucket the recorded pairs by depth afterward. Correct in `O(n)`, but it stores a full intermediate pairs list and scans it twice: see [Brute Force](#brute-force).
2. **Group as you go.** The depth is already in hand at the moment each node is visited, so the after-the-fact bucketing is redundant: append each value straight into `result[depth]` during the walk, creating each bucket the first time its depth is reached: see [Recursive DFS](#recursive-dfs).
3. **Match the traversal to the output.** The output shape is one finished list per level, so traverse in exactly that order: a queue drained one full level at a time produces each level as a complete list, with no depth counter at all: see [Iterative BFS](#iterative-bfs).

## Solutions

### Brute Force

#### Derivation

The problem hands us two jobs at once: visit every node, and group the values by level. The most direct plan refuses to interleave them, so it ignores any clever level-grouping trick: just walk the entire tree, remember the depth of every node as you pass it, then sort the values into level buckets afterward. Because we visit the left child before the right child, the values within each depth already arrive in left-to-right order:

1. Traverse the tree with `visit`, appending a `(depth, value)` pair for every node, starting the root at depth `0`.
2. Return an empty list immediately if no pairs were collected (the tree was empty).
3. Scan the pairs once to find the maximum depth, which is the number of levels minus one.
4. Allocate one empty bucket per level, then drop each value into `result[depth]`.

#### Walkthrough

Let us watch the Brute Force run on Example 1: `root = [3,9,20,null,null,15,7]`. That tree looks like this, with `3` at the root, `9` and `20` as its children, and `15` and `7` hanging under `20`:

```text
        3        (depth 0)
       / \
      9   20     (depth 1)
         /  \
        15   7   (depth 2)
```

**Phase 1: collect `(depth, value)` pairs.** `visit(root, 0)` recurses left-before-right, appending one pair per node. Each row shows the call and the pair it adds to `pairs`:

| Step | Call | Pair appended | `pairs` so far |
|------|------|---------------|----------------|
| 1 | `visit(3, 0)` | `(0, 3)` | `[(0,3)]` |
| 2 | `visit(9, 1)` | `(1, 9)` | `[(0,3),(1,9)]` |
| 3 | `visit(20, 1)` | `(1, 20)` | `[(0,3),(1,9),(1,20)]` |
| 4 | `visit(15, 2)` | `(2, 15)` | `[(0,3),(1,9),(1,20),(2,15)]` |
| 5 | `visit(7, 2)` | `(2, 7)` | `[(0,3),(1,9),(1,20),(2,15),(2,7)]` |

The `null` children of `9` and the absent children of `15` and `7` hit `if not node: return` and add nothing.

**Phase 2: find `max_depth`.** Scanning the pairs, the largest depth seen is `2`, so there are `max_depth + 1 = 3` levels.

**Phase 3: drop each value into its bucket.** Allocate `result = [[], [], []]`, then place every `val` into `result[depth]`:

| Pair | Goes into | `result` after |
|------|-----------|----------------|
| `(0, 3)` | `result[0]` | `[[3], [], []]` |
| `(1, 9)` | `result[1]` | `[[3], [9], []]` |
| `(1, 20)` | `result[1]` | `[[3], [9, 20], []]` |
| `(2, 15)` | `result[2]` | `[[3], [9, 20], [15]]` |
| `(2, 7)` | `result[2]` | `[[3], [9, 20], [15, 7]]` |

The function returns `[[3], [9, 20], [15, 7]]`, which matches the expected Output `[[3],[9,20],[15,7]]`. Notice that because step 4 (`15`) ran before step 5 (`7`), the bottom level lands in left-to-right order with no sorting needed.

#### Solution

The code is the walkthrough's three phases written down: collect the pairs, find `max_depth`, then bucket the values.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # Walk the whole tree, recording each value alongside its depth
        pairs = []

        def visit(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return
            pairs.append((depth, node.val))
            visit(node.left, depth + 1)
            visit(node.right, depth + 1)

        visit(root, 0)
        if not pairs:
            return []

        # Group the collected values by depth into per-level buckets
        max_depth = 0
        for depth, _ in pairs:
            if depth > max_depth:
                max_depth = depth
        result = [[] for _ in range(max_depth + 1)]
        for depth, val in pairs:
            result[depth].append(val)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The traversal touches each of the `n` nodes once, and the two follow-up scans over the collected pairs are each linear, so the total work is `O(n)`.

##### Space Complexity: `O(n)`

The intermediate `pairs` list holds one entry per node, the output holds all `n` values, and the recursion stack adds `O(h)` for height `h`, so the auxiliary space is `O(n)`.

#### Key Insights

- Separating collection from grouping makes the logic obvious at the cost of a full intermediate `pairs` list.
- Visiting left before right is what keeps each level's values in the correct order without any extra sorting.
- It does redundant work: it stores every node's depth explicitly and walks the pairs twice, where the refined approaches group on the fly.

### Recursive DFS

#### Derivation

The Brute Force already knows each node's depth at the very moment it visits the node, yet it writes that depth into an intermediate `pairs` list only to read it back in a second pass. The repair is to do the grouping at visit time: a [depth-first traversal](https://en.wikipedia.org/wiki/Depth-first_search) that carries a `depth` parameter can append each value straight into the correct per-level bucket, and the buckets themselves can be created lazily the first time their depth is reached:

1. Maintain a `result` list whose index `depth` holds the values for that level.
2. Recurse with a `depth` parameter, starting at `0` for the root.
3. When `depth == len(result)`, this is the first node encountered at that depth, so append a new empty sublist to grow `result`.
4. Append the current node's value to `result[depth]`.
5. Recurse into the left child before the right child, both at `depth + 1`.

Visiting left before right in preorder guarantees that values land in each level's sublist in left-to-right order, matching the BFS output exactly even though the traversal itself is depth-first.

#### Walkthrough

Let us run the depth-carrying traversal on Example 1: `root = [3,9,20,null,null,15,7]`. Each line of the trace shows one `visit` call, whether it opens a new bucket, and `result` afterward:

```text
        3        (depth 0)
       / \
      9   20     (depth 1)
         /  \
        15   7   (depth 2)

visit(3, depth=0)     depth 0 == len(result) = 0 -> new bucket    result = [[3]]
visit(9, depth=1)     depth 1 == len(result) = 1 -> new bucket    result = [[3], [9]]
visit(20, depth=1)    bucket exists, append                       result = [[3], [9, 20]]
visit(15, depth=2)    depth 2 == len(result) = 2 -> new bucket    result = [[3], [9, 20], [15]]
visit(7, depth=2)     bucket exists, append                       result = [[3], [9, 20], [15, 7]]
```

The `null` children of `9`, `15`, and `7` hit the `if not node` guard and contribute nothing. Because `9` is visited before `20`, and `15` before `7`, every bucket fills left to right on its own. The traversal ends with `result = [[3], [9, 20], [15, 7]]`: exactly the expected Output, with no intermediate pairs list and no second pass.

#### Solution

The code is the trace's single walk: the `depth == len(result)` check opens each bucket on first contact.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        result = []

        def visit(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return
            # First time we reach this depth, start a fresh sublist for it
            if depth == len(result):
                result.append([])
            result[depth].append(node.val)
            visit(node.left, depth + 1)
            visit(node.right, depth + 1)

        visit(root, 0)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited once and performs constant work, so the traversal is linear in the number of nodes.

##### Space Complexity: `O(n)`

The output stores all `n` values. The recursion stack adds `O(h)` for the tree height `h`, which is `O(n)` for a skewed tree and `O(log n)` when balanced, so the output term dominates at `O(n)`.

#### Key Insights

- Indexing `result` by depth turns DFS into a level grouping without any queue.
- The `depth == len(result)` check is the lazy-allocation trick that creates each level's bucket exactly when first needed.
- Preorder left-before-right is what keeps every level ordered correctly.
- This approach is convenient when recursion is already natural for the surrounding code, trading queue space for recursion-stack space.

### Iterative BFS

#### Derivation

Both previous solutions simulate level order with a depth-first walk and a `depth` counter. But the output shape, one finished list per level, invites traversing in exactly that order instead. Level order traversal is a textbook [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search): a queue naturally holds nodes level by level, and the one trick needed to emit grouped output is measuring each level's size before draining it:

1. Return an empty list immediately when the tree is empty.
2. Seed a queue with `root`.
3. While the queue is non-empty, capture `level_size = len(queue)`: the exact count of nodes on the current level.
4. Dequeue that many nodes, collecting their values into a fresh `level` list and enqueuing each node's children (left then right).
5. Append the completed `level` to `result` and repeat for the next level.

Snapshotting `level_size` at the top of each iteration is what cleanly partitions the output into per-level sublists, since any children appended during the loop belong to the next level and are excluded from the current count.

#### Walkthrough

Let us run the queue on Example 1: `root = [3,9,20,null,null,15,7]`. Each round of the outer loop snapshots `level_size`, drains exactly that many nodes into `level`, and enqueues their children behind them:

```text
        3        level 0
       / \
      9   20     level 1
         /  \
        15   7   level 2

queue = [3]                                              seeded with root
level_size = 1   pop 3    level = [3]      push 9, 20    result = [[3]]
                 queue = [9, 20]
level_size = 2   pop 9    level = [9]      no children
                 pop 20   level = [9, 20]  push 15, 7    result = [[3], [9, 20]]
                 queue = [15, 7]
level_size = 2   pop 15   level = [15]     no children
                 pop 7    level = [15, 7]  no children   result = [[3], [9, 20], [15, 7]]
queue empty -> loop ends
```

In the second round, `15` and `7` are pushed while `level_size` is already fixed at `2`, so they wait in the queue for the next round instead of leaking into the current level. The loop ends with `result = [[3], [9, 20], [15, 7]]`, matching the expected Output.

#### Solution

The code is the walkthrough's outer loop written down: snapshot `level_size`, drain one level, enqueue the next.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            level = []
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is enqueued and dequeued exactly once, and each contributes constant work, giving linear time in the number of nodes.

##### Space Complexity: `O(n)`

The output stores all `n` node values. The queue independently holds at most one level, which is up to `n/2` nodes for a complete tree, so the auxiliary space is also `O(n)`.

#### Key Insights

- Recording `level_size` before the inner loop is the idiomatic way to separate BFS levels without sentinel markers.
- A `deque` gives `O(1)` `popleft`, unlike a plain list whose `pop(0)` is `O(n)`.
- Enqueuing left before right preserves the required left-to-right ordering within each level.
- Unlike the brute force, no intermediate `(depth, value)` list is needed: the queue groups levels directly, and the pattern generalizes to zigzag traversal, right side view, and per-level aggregates.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - One traversal plus two linear scans over the collected pairs
- **Recursive DFS**: `O(n)` - Each node is visited once
- **Iterative BFS**: `O(n)` - Each node is enqueued and dequeued once

### Space Complexity

- **Brute Force**: `O(n)` - Output plus a full intermediate `(depth, value)` list and an `O(h)` recursion stack
- **Recursive DFS**: `O(n)` - Output plus an `O(h)` recursion stack
- **Iterative BFS**: `O(n)` - Output plus a queue holding up to one full level

### Trade-offs

- Brute Force separates collection from grouping for maximum clarity, but pays for an intermediate pairs list and a second pass that the on-the-fly approaches avoid.
- Recursive DFS removes the explicit queue and groups levels during the walk by indexing `result` by depth, but introduces a recursion stack that can overflow on a very deep tree.
- Iterative BFS maps directly to the level-by-level framing, making the level grouping obvious from the queue mechanics, and avoids deep recursion entirely.
- BFS peaks at the widest level, while DFS peaks at the tallest path, so the cheaper auxiliary structure depends on tree shape.

### When to Use Each

- **Brute Force**: As a teaching baseline when separating the traversal from the grouping makes the logic clearest.
- **Recursive DFS**: When recursion is already idiomatic in the surrounding code and the tree depth is bounded.
- **Iterative BFS**: The recommended default; when the level-by-level reading is the clearest expression of the problem, or when the tree may be very deep.

### Optimization Notes

- All three approaches are `O(n)` time, so the choice is driven by which auxiliary structure better fits the expected tree shape.
- Both refinements drop the brute force's intermediate `(depth, value)` list by grouping levels as they go.
- For very deep trees, BFS avoids the recursion-depth ceiling that both recursive solutions can hit.
- Indexing the result list by depth lets DFS group levels without sentinel markers, mirroring how BFS uses `level_size`.
