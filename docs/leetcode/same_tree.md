# [Same Tree](https://leetcode.com/problems/same-tree/)

**Easy** | **15 minutes** | **Tree, Depth-First Search, Breadth-First Search, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/same_tree/solution.py`](../../practice/same_tree/solution.py)

Given the roots of two binary trees `p` and `q`, return `true` if the trees are **equivalent**, otherwise return `false`.

Two binary trees are considered **equivalent** if they share the exact same structure and the nodes have the same values.

## Examples

### Example 1

**Input:** `p = [1,2,3], q = [1,2,3]`

**Output:** `true`

### Example 2

**Input:** `p = [4,7], q = [4,null,7]`

**Output:** `false`

### Example 3

**Input:** `p = [1,2,3], q = [1,3,2]`

**Output:** `false`

## Constraints

- `0 <= The number of nodes in both trees <= 100`.
- `-100 <= Node.val <= 100`

## Deriving the Solution

Equivalence is defined node by node: two trees are the same exactly when their roots hold equal values, their left subtrees are the same, and their right subtrees are the same. That self-similar definition is the whole solution family; every variant walks a worklist of node pairs and differs only in how the worklist is managed.

1. **Start literal.** Translate the definition straight into recursion: compare
   the two roots, recurse on both child pairs, and let a missing child on
   either side give an immediate verdict: see [Recursive DFS](#recursive-dfs).
2. **Make the worklist explicit.** The recursion is just a stack of node
   pairs; managing the stack by hand removes the call-depth limit while
   keeping the depth-first order: see [Iterative DFS](#iterative-dfs).
3. **Swap the stack for a queue.** Consuming the same pairs from the other
   end turns the walk into a level-order sweep with identical pair logic:
   see [Iterative BFS](#iterative-bfs).

## Solutions

### Recursive DFS

#### Derivation

The problem statement's definition of equivalence is already recursive, so the most direct reading turns it into code one clause at a time:

1. Both nodes `None`: both subtrees are empty, so they are equivalent.
2. Exactly one of `p`, `q` is `None`: one subtree exists where the other has
   nothing, so the structures differ.
3. `p.val != q.val`: the values at this position differ.
4. Otherwise both nodes exist with equal values: the trees are the same
   exactly when the left pair and the right pair are the same, so recurse on
   both and combine with `and`.

The order matters: the `None` cases must be tested before reading `.val`, and the one-sided `None` check must come before the value check, because a missing node has no value to compare.

#### Walkthrough

Trace the recursion on Example 3: `p = [1,2,3]`, `q = [1,3,2]`:

```text
p:   1         q:   1
    / \            / \
   2   3          3   2

pair (1, 1):   both exist, values equal -> recurse on both child pairs
  pair (2, 3): both exist, values differ -> False
verdict: left pair is False, `and` short-circuits, right pair never runs
```

The roots match, so the verdict is delegated to the child pairs. The left children hold `2` and `3`, and the value mismatch returns `False` immediately, matching the expected Output for Example 3. The structure-only failure is Example 2 (`p = [4,7]`, `q = [4,null,7]`): the root pair `4, 4` passes, and the child pairs `(7, None)` and `(None, 7)` each hit the one-sided `None` check, returning `False` even though the two `7` values are equal, matching the expected Output for Example 2.

#### Solution

The code is the definition's four clauses written down, in order.

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
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None and q is None:
            return True
        if p is None or q is None:
            return False
        if p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(min(n, m))`

One recursive call runs per aligned node pair, and the traversal stops the moment one side runs out or a mismatch appears, so the work is bounded by the smaller tree's size `min(n, m)`.

##### Space Complexity: `O(min(n, m))`

The recursion depth is bounded by the smaller tree's height: `O(log n)` for a balanced pair of trees, `O(n)` for two identical skewed chains.

#### Key Insights

- The two `None` checks encode the entire structural comparison: both empty
  means equal, exactly one empty means different, and anything else is
  decided by values and recursion.
- Testing `p.val != q.val` after the `None` guards is what makes reading
  `.val` safe; reordering those checks is the classic crash in this problem.
- The `and` short-circuits, so the first failing child pair spares the
  sibling subtree entirely.

### Iterative DFS

#### Derivation

The recursive version leans on the call stack, which caps how deep a tree it can process. The recursion's only state is the set of pending node pairs, and Python's list is already a stack: pop the newest pair, apply the same three checks, and push the children of any surviving pair. The verdict becomes the loop's exit value instead of a return value:

1. Seed a stack with the root pair `(p, q)`.
2. Pop a pair `(a, b)`. Both `None`: this position matches, continue.
3. Exactly one `None`, or values differ: return `False`.
4. Otherwise push `(a.left, b.left)` and `(a.right, b.right)`.
5. An emptied stack means every aligned pair matched: return `True`.

#### Walkthrough

Trace the stack on Example 2: `p = [4,7]`, `q = [4,null,7]`, where `p`'s `7` hangs left and `q`'s `7` hangs right:

```text
pop (4, 4):     both exist, values equal
                push (p.left, q.left)  = (7, None)
                push (p.right, q.right) = (None, 7)
pop (None, 7):  exactly one side is None -> return False
```

The list pops from the end, so the last-pushed pair `(None, 7)` is examined first. That pair fails the one-sided `None` check even though both trees hold a `7`: the values are equal but the positions are not, which is exactly the structural difference Example 2 encodes, matching the expected Output for Example 2.

#### Solution

The code is the pair stack: seed, pop, check, push children, and `True` when the stack empties.

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
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        stack = [(p, q)]
        while stack:
            a, b = stack.pop()
            if a is None and b is None:
                continue
            if a is None or b is None or a.val != b.val:
                return False
            stack.append((a.left, b.left))
            stack.append((a.right, b.right))
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(min(n, m))`

Each aligned node pair is pushed and popped at most once before a mismatch or exhaustion ends the walk.

##### Space Complexity: `O(min(n, m))`

The stack holds pending pairs along one root-to-leaf frontier, bounded by the smaller tree's height.

#### Key Insights

- The recursion's implicit stack becomes a literal list of pairs; nothing
  else about the algorithm changes.
- `continue` on the both-`None` pair is what lets the walk pass through
  matched leaf positions instead of treating them as mismatches.
- A deep skewed chain no longer risks the recursion limit: the explicit
  stack simply grows.

### Iterative BFS

#### Derivation

The explicit worklist raises one question: must it be a stack? Swapping the list for a `deque` consumed from the other end keeps every pair check identical but visits the pairs level by level instead of diving depth first. For this problem the visit order is irrelevant to the verdict, so the variant is a free choice of traversal shape:

1. Seed a queue with the root pair `(p, q)`.
2. Dequeue a pair `(a, b)` and apply the same three checks as the stack
   version.
3. On a match, enqueue `(a.left, b.left)` and `(a.right, b.right)`.
4. An emptied queue means every aligned pair matched: return `True`.

#### Walkthrough

Trace the queue on Example 3: `p = [1,2,3]`, `q = [1,3,2]`:

```text
dequeue (1, 1): both exist, values equal
                enqueue (2, 3), (3, 2)
dequeue (2, 3): values differ -> return False
```

The first level's pair passes and enqueues the second level's two pairs. The dequeued `(2, 3)` mismatches before the `(3, 2)` pair is ever examined, matching the expected Output for Example 3.

#### Solution

The code is the stack version with the pop exchanged for a `popleft`.

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
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        queue = deque([(p, q)])
        while queue:
            a, b = queue.popleft()
            if a is None and b is None:
                continue
            if a is None or b is None or a.val != b.val:
                return False
            queue.append((a.left, b.left))
            queue.append((a.right, b.right))
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(min(n, m))`

Each aligned node pair enters and leaves the queue at most once.

##### Space Complexity: `O(min(n, m))`

The queue's peak size is the smaller tree's maximum level width, which is worst-case half its nodes.

#### Key Insights

- The verdict cannot depend on the visit order, so stack and queue are
  interchangeable here; that freedom is the proof this is a pure traversal
  problem.
- The queue's frontier is width-bounded while the stack's is height-bounded:
  the BFS peak can exceed the DFS peak on wide trees.
- Every pair check is byte-for-byte the stack version's; only the container
  and its access end changed.

## Comparison of Solutions

### Time Complexity

- **Recursive DFS**: `O(min(n, m))` - one call per aligned pair until a mismatch.
- **Iterative DFS**: `O(min(n, m))` - one push and pop per aligned pair.
- **Iterative BFS**: `O(min(n, m))` - one enqueue and dequeue per aligned pair.

### Space Complexity

- **Recursive DFS**: `O(min(n, m))` - call stack bounded by the smaller tree's height.
- **Iterative DFS**: `O(min(n, m))` - explicit stack bounded by the same height.
- **Iterative BFS**: `O(min(n, m))` - queue bounded by the smaller tree's widest level.

### Trade-offs

- All three examine the same aligned pairs and differ only in worklist
  management, so asymptotic costs match across the board.
- The recursive version is the shortest and mirrors the definition, but its
  depth is capped by Python's recursion limit.
- The iterative DFS removes the depth cap at the cost of manual stack
  bookkeeping; the BFS adds a `deque` import and a wider worst-case frontier
  while buying level-order visiting that this problem does not need.

### When to Use Each

- **Recursive DFS**: The default answer; the code is the definition
  (recommended here).
- **Iterative DFS**: When tree depth could approach the recursion limit or
  the interviewer asks to de-recursion the solution.
- **Iterative BFS**: When the surrounding code already processes trees level
  by level and this check can ride along.

### Optimization Notes

- The guards fire before any `.val` read, so neither a missing child nor an
  early mismatch can crash or waste work.
- `min(n, m)` bounds all three: the first exhausted branch terminates its
  whole subtree comparison, so uneven tree sizes are never punished.
- Short-circuit evaluation makes the first mismatched pair prune its sibling
  subtree in all three variants.
