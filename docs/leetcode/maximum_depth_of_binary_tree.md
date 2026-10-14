# [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/)

**Easy** | **15 minutes** | **Tree, Depth-First Search, Breadth-First Search, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal)

**Practice:** [`practice/maximum_depth_of_binary_tree/solution.py`](../../practice/maximum_depth_of_binary_tree/solution.py)

Given the `root` of a binary tree, return its maximum depth.

A binary tree's **maximum depth** is the number of nodes along the longest path from the root node down to the farthest leaf node.

## Examples

### Example 1

![Maximum Depth of Binary Tree Example 1](assets/maximum_depth_of_binary_tree_example1.jpg)

**Input:** `root = [3,9,20,null,null,15,7]`

**Output:** `3`

### Example 2

**Input:** `root = [1,null,2]`

**Output:** `2`

### Example 3

**Input:** `root = []`

**Output:** `0`

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-100 <= Node.val <= 100`

## Deriving the Solution

A tree's depth is defined by its subtrees: a node sits one level above the deeper of its two children, and an empty tree has depth `0`. Every solution below is a full `O(n)` traversal; they differ only in who keeps track of how deep each node sits.

1. **Start literal.** The definition is already a recurrence,
   `depth(node) = 1 + max(depth(left), depth(right))` with `depth(None) = 0`, so transcribe it as a post-order recursion and let the call stack carry the depth bookkeeping. Clean and short, at `O(h)` stack space: see [Recursive DFS](#recursive-dfs).
2. **Name the risk.** The call stack is borrowed from the language: on a
   degenerate chain of `10^4` nodes the recursion can exceed Python's default recursion limit. The remaining approaches keep the same traversal but manage the bookkeeping themselves.
3. **Count levels instead of paths.** Depth is also the number of levels, so
   walk the tree one level at a time with a queue and count how many levels drain. Recursion-free, but the queue holds an entire level, up to `O(w)` nodes on wide trees: see [Iterative BFS](#iterative-bfs).
4. **Keep depth-first, add an explicit stack.** Simulate the recursion with a
   stack of `(node, depth)` pairs and track the maximum depth popped. This removes the recursion limit while restoring the depth-first `O(h)` space profile: see [Iterative DFS with Stack](#iterative-dfs-with-stack).

## Solutions

### Recursive DFS

#### Derivation

Ask what the depth of a tree is in terms of its parts. The problem's own definition answers: the longest root-to-leaf path passes through whichever child subtree is deeper, so a node's depth is one more than the larger of its children's depths, and an empty subtree contributes `0`. A definition phrased in terms of smaller instances of itself is precisely what recursion executes, so a recursive [depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) transcribes it directly:

1. If `root` is `None`, the subtree is empty and its depth is `0`.
2. Otherwise, recursively compute `self.maxDepth(root.left)` and
   `self.maxDepth(root.right)`.
3. Return `1 + max(...)` of those two subtree depths, where the `1` counts the
   current node.

Because each node's result is combined only after both children return, this follows the post-order pattern: children are fully processed before the parent produces its answer.

#### Recurrence

Depth is defined on a node in terms of its children, which is exactly a recurrence:

$$ \text{depth}(v) = \begin{cases} 0, & v = \text{null} \\[4pt] 1 + \max\bigl(\text{depth}(v.\text{left}),\ \text{depth}(v.\text{right})\bigr), & \text{otherwise} \end{cases} $$

```text
maxDepth(None) = 0
maxDepth(root) = 1 + max(maxDepth(root.left), maxDepth(root.right))
                 for root != None
```

The empty tree contributing `0` is the base case, and the `+1` charges one level for the node itself. This is the smallest complete example of tree DP: the answer at a node needs nothing but the answers at its children, so a single post-order pass computes it. Swapping \(\max\) for \(\min\) gives minimum depth, and swapping it for \(+\) gives the node count: same traversal, different combiner.

#### Walkthrough

Let us watch the recursion run on Example 1: `root = [3,9,20,null,null,15,7]`. That tree looks like this:

```text
        3
       / \
      9   20
         /  \
        15   7
```

Each call computes `1 + max(left, right)`, so a parent cannot answer until both children return. The call tree below indents each recursive call, and the `->` shows the value handed back up:

```text
maxDepth(3): call left, then right
  maxDepth(9): call left, then right
    maxDepth(None) -> 0
    maxDepth(None) -> 0
  maxDepth(9): 1 + max(0, 0) -> 1
  maxDepth(20): call left, then right
    maxDepth(15): call left, then right
      maxDepth(None) -> 0
      maxDepth(None) -> 0
    maxDepth(15): 1 + max(0, 0) -> 1
    maxDepth(7): call left, then right
      maxDepth(None) -> 0
      maxDepth(None) -> 0
    maxDepth(7): 1 + max(0, 0) -> 1
  maxDepth(20): 1 + max(1, 1) -> 2
maxDepth(3): 1 + max(1, 2) -> 3
```

Reading it bottom-up: each `None` returns `0`, so the leaves `9`, `15`, and `7` each return `1`. Node `20` takes the larger of its two children (`1` and `1`) and adds itself to get `2`. Finally node `3` compares its left subtree (`1`) against its right subtree (`2`), keeps the larger, and adds `1` for itself: `1 + max(1, 2) = 3`.

The call returns `3`, which matches the expected Output of `3`.

#### Solution

The code is the recurrence from the walkthrough written down: one base case and one combining line.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node in the tree is visited exactly once, so the work is linear in the number of nodes `n`.

##### Space Complexity: `O(h)`

The space is the depth of the recursion stack, which equals the height of the tree `h`. In the worst case of a completely unbalanced tree this is `O(n)`; for a balanced tree it is `O(log n)`.

#### Key Insights

- The recurrence `depth(node) = 1 + max(depth(left), depth(right))` mirrors the recursive structure of the tree itself.
- Treating the empty subtree as depth `0` removes the need for any special leaf handling.
- It is the most concise and readable approach, though deep trees can risk exceeding the recursion limit.

### Iterative BFS

#### Derivation

The recursion above leans on the language's call stack, and a degenerate tree deep enough can exhaust it. To drop recursion entirely, change what is counted: depth is also the number of levels in the tree, and [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) visits the tree exactly one level at a time. If the traversal can tell where one level ends and the next begins, counting drained levels counts the depth. The boundary comes from a snapshot: the nodes in the queue at the top of an iteration are precisely one level, so dequeuing exactly that many processes the level while their children, enqueued behind them, form the next one:

1. If the root is `None`, return `0`.
2. Seed `queue` with the root and start a `depth` counter at `0`.
3. On each outer iteration, increment `depth`, record the current `len(queue)`,
   then dequeue exactly that many nodes with `popleft`, enqueuing each node's existing children.
4. When `queue` empties, `depth` equals the number of levels, which is the
   maximum depth; return it.

Snapshotting `len(queue)` before the inner loop is what isolates one level from the next, since children added during the loop belong to the following level.

#### Walkthrough

Let us drain Example 1 level by level: `root = [3,9,20,null,null,15,7]`, the tree

```text
        3
       / \
      9   20
         /  \
        15   7
```

Each outer iteration bumps `depth`, snapshots the queue length, and dequeues exactly that many nodes, appending their children behind:

```text
start      queue = [3]        depth = 0
level 1    snapshot len = 1: pop 3, enqueue 9 and 20
           queue = [9, 20]    depth = 1
level 2    snapshot len = 2: pop 9 (leaf), pop 20, enqueue 15 and 7
           queue = [15, 7]    depth = 2
level 3    snapshot len = 2: pop 15 (leaf), pop 7 (leaf)
           queue = []         depth = 3
```

After the third level drains, the queue is empty and the loop exits. Three levels were processed, so `depth = 3`, matching the expected Output of `3`.

#### Solution

The code is the level drain from the walkthrough: snapshot, dequeue that many, count the level.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
from typing import Optional


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        queue = deque([root])
        depth = 0

        while queue:
            depth += 1
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return depth
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is enqueued and dequeued exactly once, giving linear time.

##### Space Complexity: `O(w)`

The queue holds at most one full level at a time, so the space is bounded by the maximum width `w` of the tree. For a perfect binary tree the widest level holds about `n/2` nodes, which is `O(n)`.

#### Key Insights

- Iterating level by level lets depth be counted directly without tracking per-node depths.
- Capturing the level size before draining the queue cleanly separates one level from the next.
- BFS uses recursion-free control flow, avoiding stack-overflow risk on very deep trees.

### Iterative DFS with Stack

#### Derivation

BFS removed the recursion risk but pays for it in width: on a bushy tree the queue holds an entire level, up to half the nodes. The recursive traversal only ever held one root-to-leaf path. To keep that `O(h)` footprint without recursion, simulate the recursion with an explicit [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)). One thing the call stack provided for free must now be carried by hand: each frame knew its own depth, so the stack stores `(node, depth)` pairs, and the answer is the largest depth ever popped:

1. If the root is `None`, return `0`.
2. Push `(root, 1)` onto `stack` and initialize `max_depth` to `0`.
3. Pop a `(node, depth)` pair, update `max_depth` with `depth`, and push each
   existing child paired with `depth + 1`, right child before left so the left subtree is visited first.
4. Continue until `stack` is empty; `max_depth` then holds the deepest path
   length seen. Return it.

#### Walkthrough

Let us run the explicit stack on Example 1: `root = [3,9,20,null,null,15,7]`, the tree

```text
        3
       / \
      9   20
         /  \
        15   7
```

Each line pops one `(node, depth)` pair, folds its depth into `max_depth`, and pushes the children one level deeper (right first, left on top):

```text
start         stack = [(3, 1)]            max_depth = 0
pop (3, 1)    push (20, 2) then (9, 2)    max_depth = 1
              stack = [(20, 2), (9, 2)]
pop (9, 2)    leaf, nothing pushed        max_depth = 2
              stack = [(20, 2)]
pop (20, 2)   push (7, 3) then (15, 3)    max_depth = 2
              stack = [(7, 3), (15, 3)]
pop (15, 3)   leaf, nothing pushed        max_depth = 3
              stack = [(7, 3)]
pop (7, 3)    leaf, nothing pushed        max_depth = 3
              stack = []
```

The stack empties after five pops, one per node. The deepest pairs popped were `(15, 3)` and `(7, 3)`, so `max_depth = 3`, matching the expected Output of `3`.

#### Solution

The code is the pop-update-push loop from the walkthrough, with depths carried explicitly on the stack.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        stack = [(root, 1)]
        max_depth = 0

        while stack:
            node, depth = stack.pop()
            max_depth = max(max_depth, depth)
            if node.right:
                stack.append((node.right, depth + 1))
            if node.left:
                stack.append((node.left, depth + 1))

        return max_depth
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is pushed and popped exactly once, so the traversal is linear.

##### Space Complexity: `O(h)`

The stack mirrors a root-to-leaf path, so its size is bounded by the height `h`: `O(n)` for an unbalanced tree and `O(log n)` for a balanced one.

#### Key Insights

- Storing `(node, depth)` pairs replaces the implicit depth bookkeeping that recursion provides for free.
- An explicit stack removes recursion-depth limits while keeping the depth-first traversal order.
- Pushing the right child before the left makes the traversal visit the left subtree first, though the final maximum is unaffected by visit order.

## Comparison of Solutions

### Time Complexity

- **Recursive DFS**: `O(n)` - visits each node once.
- **Iterative BFS**: `O(n)` - visits each node once.
- **Iterative DFS with Stack**: `O(n)` - visits each node once.

### Space Complexity

- **Recursive DFS**: `O(h)` - bounded by the recursion depth, the tree height.
- **Iterative BFS**: `O(w)` - bounded by the widest level of the tree.
- **Iterative DFS with Stack**: `O(h)` - bounded by the stack holding one root-to-leaf path.

### Trade-offs

- Recursive DFS is the shortest and clearest, but very deep trees can exceed the recursion limit.
- Iterative BFS removes recursion risk and counts levels directly, at the cost of more memory on wide trees.
- Iterative DFS with Stack removes recursion risk while staying depth-first, at the cost of tracking depths explicitly.

### When to Use Each

- **Recursive DFS**: When readability matters most and the tree is not pathologically deep.
- **Iterative BFS**: When the tree may be deep and you want to avoid recursion, especially when level information is also useful.
- **Iterative DFS with Stack**: When you want recursion-free depth-first traversal and prefer `O(h)` space over BFS's `O(w)`.

### Optimization Notes

- All three approaches are `O(n)` in time, so the practical choice hinges on space and recursion-depth constraints rather than speed.
- For trees deep enough to threaten Python's default recursion limit, prefer either iterative approach over Recursive DFS.
- In interview settings the Recursive DFS solution is usually preferred first for its clarity, with an iterative approach offered as the follow-up that avoids stack overflow.
