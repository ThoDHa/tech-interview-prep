# [Count Good Nodes In Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/)

**Medium** | **25 minutes** | **Tree, Depth-First Search, Breadth-First Search, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/count_good_nodes_in_binary_tree/solution.py`](../../practice/count_good_nodes_in_binary_tree/solution.py)

Within a binary tree, a node `x` is considered **good** if the path from the root of the tree to the node `x` contains no nodes with a value greater than the value of node `x`

Given the root of a binary tree `root`, return the number of **good** nodes within the tree.

## Examples

### Example 1

**Input:** `root = [2,1,1,3,null,1,5]`

**Output:** `3`

### Example 2

**Input:** `root = [1,2,-1,3,4]`

**Output:** `4`

## Constraints

- `1 <= number of nodes in the tree <= 100,000`
- `-100 <= Node.val <= 100`

## Deriving the Solution

"Good" is a property of the root-to-node path, so no node can be judged until the walk reaches it carrying the maximum value seen so far. Every solution is therefore a traversal that threads that running maximum alongside each node; they differ only in what carries the pair.

1. **Start literal.** A recursive depth-first walk with `max_so_far` as a
   second argument: the node decides its own goodness, updates the maximum,
   and sums both children's verdicts: see [Recursive DFS](#recursive-dfs).
2. **Make the stack explicit.** The pair `(node, max_so_far)` is exactly
   what the call stack holds, so a hand-managed stack of pairs survives any
   tree depth: see [Iterative DFS](#iterative-dfs).
3. **Consume the pairs level by level.** The same pair logic read from the
   other end of the worklist gives a breadth-first sweep, at the price of a
   width-bounded frontier: see [Iterative BFS](#iterative-bfs).

## Solutions

### Recursive DFS

#### Derivation

The definition of good is local given one piece of context: a node is good exactly when no ancestor's value is greater than its own, which the walk can test as `node.val >= max_so_far`, the running maximum over the ancestors (the root is good automatically, since nothing precedes it). Making that context a parameter turns the definition into a recursion:

1. A `None` node contributes no good nodes: return `0`.
2. At `node`, count `1` when `node.val >= max_so_far`, else `0`.
3. The maximum the children see is `max(max_so_far, node.val)`, whether or
   not `node` was itself good.
4. Return the node's count plus both recursive results.

The comparison is `>=`, not `>`: the definition forbids only ancestors that are *strictly greater*, so a node equal to the path maximum is still good.

#### Walkthrough

Trace the recursion on Example 1: `root = [2,1,1,3,null,1,5]`:

```text
        2
       / \
      1   1
     /   / \
    3   1   5

dfs(2, 2): 2 >= 2 good -> 1; max for children stays 2
  dfs(1, 2): 1 < 2 not good; max stays 2
    dfs(3, 2): 3 >= 2 good -> 1; leaves contribute 0   -> 1
    -> 0 + 1 + 0 = 1
  dfs(1, 2): 1 < 2 not good; max stays 2
    dfs(1, 2): 1 < 2 not good                          -> 0
    dfs(5, 2): 5 >= 2 good -> 1                        -> 1
    -> 0 + 0 + 1 = 1
  -> 1 + 1 + 1 = 3
```

Only `2`, `3`, and `5` meet or exceed the maximum on their path; every `1` is buried under the `2`, so it is never good regardless of which subtree it sits in. The total `3` matches the expected Output for Example 1. Example 2 (`[1,2,-1,3,4]`) exercises rising maxima: `dfs(1, 1)` is good, `dfs(2, 1)` is good and raises the maximum to `2`, both of its children (`3` and `4`) beat that new maximum, and the lone `-1` does not, giving `4`, matching the expected Output for Example 2.

#### Solution

The code is the recursion above, seeded with the root's own value.

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


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node: Optional[TreeNode], max_so_far: int) -> int:
            if node is None:
                return 0
            good = 1 if node.val >= max_so_far else 0
            next_max = max(max_so_far, node.val)
            return good + dfs(node.left, next_max) + dfs(node.right, next_max)

        return dfs(root, root.val)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` nodes is visited once and does a constant-time comparison and maximum update.

##### Space Complexity: `O(h)`

The recursion depth is the tree's height: `O(log n)` for a balanced tree, `O(n)` for a skewed one. With `n` up to `100,000`, a degenerate chain approaches Python's recursion limit.

#### Key Insights

- `max_so_far` as a parameter is the path context made explicit: no visited
  set, no per-path bookkeeping, because the call order *is* the path.
- The `>=` comparison encodes the definition's "no node greater" wording:
  equals is good, only strictly greater ancestors disqualify.
- The child maximum is updated unconditionally; computing it only for good
  nodes is the classic wrong turn here, since a bad node still raises the
  bar for its own descendants.

### Iterative DFS

#### Derivation

The recursion's only per-frame state is the pair `(node, max_so_far)`, so the call stack is reproducible by a list of pairs. Popping from the end reproduces the depth-first order, and the counter moves from return values to an accumulator the loop owns:

1. Seed a stack with `(root, root.val)`.
2. Pop `(node, max_so_far)`.
3. Count `node` when `node.val >= max_so_far`, and compute
   `next_max = max(max_so_far, node.val)`.
4. Push `(node.left, next_max)` and `(node.right, next_max)` for every
   existing child.
5. An emptied stack has visited every node: return the accumulated count.

#### Walkthrough

Trace the stack on Example 2: `root = [1,2,-1,3,4]`. The list pops from the end, so a right child pushed last is processed first:

```text
pop (1, 1):   1 >= 1 good, count = 1; next_max = 1
              push (2, 1), (-1, 1)          stack: [(2, 1), (-1, 1)]
pop (-1, 1):  -1 < 1 not good, count = 1;  stack: [(2, 1)]
pop (2, 1):   2 >= 1 good, count = 2; next_max = 2
              push (3, 2), (4, 2)           stack: [(3, 2), (4, 2)]
pop (4, 2):   4 >= 2 good, count = 3         stack: [(3, 2)]
pop (3, 2):   3 >= 2 good, count = 4         stack: []
stack empty -> return 4
```

The `-1` is examined before the `2`'s subtree, but the accumulator is order-independent, so the early visit costs nothing. All four good nodes register, matching the expected Output for Example 2.

#### Solution

The code is the pair stack with the accumulator.

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


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        count = 0
        stack = [(root, root.val)]
        while stack:
            node, max_so_far = stack.pop()
            if node.val >= max_so_far:
                count += 1
            next_max = max(max_so_far, node.val)
            if node.left is not None:
                stack.append((node.left, next_max))
            if node.right is not None:
                stack.append((node.right, next_max))
        return count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is pushed and popped exactly once with constant work per visit.

##### Space Complexity: `O(h)`

The stack holds at most one root-to-leaf frontier of pairs, bounded by the tree's height.

#### Key Insights

- The pair `(node, max_so_far)` is the recursion frame written down; each
  child must get the *updated* maximum, which is why `next_max` is computed
  once per pop and threaded into both pushes.
- Children are pushed only when they exist, so no `None` placeholder pairs
  clutter the stack and the loop never needs a null guard.
- No recursion limit exists: a fully skewed `100,000`-node chain becomes a
  `100,000`-entry list, which Python handles without complaint.

### Iterative BFS

#### Derivation

The stack's discipline raises the same question the stack version answered for recursion: must the worklist be consumed from the newest end? A `deque` read from the front keeps every pair computation identical while visiting nodes level by level. The verdict is again an order-independent accumulator, so the traversal shape is a free choice, and breadth-first bounds the frontier by the widest level instead of the deepest path:

1. Seed a queue with `(root, root.val)`.
2. Dequeue `(node, max_so_far)` from the front.
3. Apply the same goodness test and `next_max` computation as the stack
   version.
4. Enqueue existing children with `next_max`.
5. An emptied queue means every node is counted: return the count.

#### Walkthrough

Trace the queue on Example 1: `root = [2,1,1,3,null,1,5]`:

```text
        2
       / \
      1   1
     /   / \
    3   1   5

dequeue (2, 2): good, count = 1; enqueue (1, 2), (1, 2)
                queue: [(1, 2), (1, 2)]
dequeue (1, 2): not good; enqueue (3, 2)          [left 1's child]
                queue: [(1, 2), (3, 2)]
dequeue (1, 2): not good; enqueue (1, 2), (5, 2)  [right 1's children]
                queue: [(3, 2), (1, 2), (5, 2)]
dequeue (3, 2): good, count = 2
dequeue (1, 2): not good
dequeue (5, 2): good, count = 3
queue empty -> return 3
```

The level sweep ends with the third level's `3`, `1`, and `5` in queue order: `3` and `5` beat the path maximum `2`, the middle `1` does not. The total `3` matches the expected Output for Example 1.

#### Solution

The code is the stack version with `pop` exchanged for `popleft`.

```python
from collections import deque
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


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        count = 0
        queue = deque([(root, root.val)])
        while queue:
            node, max_so_far = queue.popleft()
            if node.val >= max_so_far:
                count += 1
            next_max = max(max_so_far, node.val)
            if node.left is not None:
                queue.append((node.left, next_max))
            if node.right is not None:
                queue.append((node.right, next_max))
        return count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node enters and leaves the queue exactly once.

##### Space Complexity: `O(w)`

The queue's peak is the widest level `w`, worst-case `n / 2` nodes on a complete bottom level, which exceeds the depth-first frontier on broad trees.

#### Key Insights

- The pair threading is byte-for-byte the stack version's; only the
  container and its access end changed, which is the signature of a
  traversal-order choice rather than an algorithmic one.
- Level order carries the same `max_so_far` correctness: a parent's
  `next_max` is always enqueued with its children, so no node is judged
  before its path context exists.
- The width-bounded frontier is the trade: the queue wins on deep narrow
  trees and loses on wide shallow ones, so the DFS variants are preferred
  when height stays reasonable.

## Comparison of Solutions

### Time Complexity

- **Recursive DFS**: `O(n)` - one visit per node.
- **Iterative DFS**: `O(n)` - one push and pop per node.
- **Iterative BFS**: `O(n)` - one enqueue and dequeue per node.

### Space Complexity

- **Recursive DFS**: `O(h)` - call stack bounded by the height.
- **Iterative DFS**: `O(h)` - explicit pair stack bounded by the height.
- **Iterative BFS**: `O(w)` - queue bounded by the widest level.

### Trade-offs

- All three thread identical `(node, max_so_far)` state and count with the
  same `>=` rule, so time matches across the family.
- The recursive form is the clearest statement of the idea but inherits the
  interpreter's recursion limit, which this problem's `n <= 100,000` can
  actually reach on a skewed tree.
- The iterative DFS removes that ceiling; the BFS trades a height bound for
  a width bound and buys level order the problem does not use.

### When to Use Each

- **Recursive DFS**: The default when depth is known to be safe; the code
  reads exactly like the definition (recommended here).
- **Iterative DFS**: The same problem at scale or in a language/runtime
  where stack depth is a real constraint.
- **Iterative BFS**: When the surrounding system already works level by
  level, or in a breadth-first pipeline that can absorb the check for free.

### Optimization Notes

- Seeding with `root.val` (not `-infinity`) is available only because the
  root is trivially good; a sentinel also works but hides that fact.
- `next_max` is computed once per node and shared by both children; copying
  the max into each child branch separately duplicates the work.
- For a counting-only traversal the accumulator variants also skip the
  recombination the recursion performs on unwind, a constant-factor edge to
  the iterative forms.
