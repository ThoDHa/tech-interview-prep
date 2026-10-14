# [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/)

**Easy** | **15 minutes** | **Tree, Depth-First Search, Breadth-First Search**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

**Practice:** [`practice/invert_binary_tree/solution.py`](../../practice/invert_binary_tree/solution.py)

Given the `root` of a binary tree, invert the tree, and return its root.

## Examples

### Example 1

![Invert Binary Tree Example 1](assets/invert_binary_tree_example1.jpg)

**Input:** `root = [4,2,7,1,3,6,9]`

**Output:** `[4,7,2,9,6,3,1]`

### Example 2

![Invert Binary Tree Example 2](assets/invert_binary_tree_example2.jpg)

**Input:** `root = [2,1,3]`

**Output:** `[2,3,1]`

### Example 3

**Input:** `root = []`

**Output:** `[]`

## Constraints

- The number of nodes in the tree is in the range `[0, 100]`
- `-100 <= Node.val <= 100`

## Deriving the Solution

The mirror image of a tree is the tree in which every node's two children have traded places. That makes inversion a purely local operation: swap the children at each node, and the whole tree is inverted once every node has been swapped. Since the swaps are independent of one another, any traversal that reaches every node exactly once solves the problem; the solutions differ only in how they enumerate the nodes.

1. **Start with the definition.** The inverted tree is the tree whose root has its children swapped and whose subtrees are themselves inverted. That self-similar statement is already an algorithm: swap, then recurse into both children. See [Recursive DFS](#recursive-dfs).
2. **Name the limit.** The recursion borrows the call stack, one frame per level, so a deep tree can hit the recursion limit. The fix is to manage the pending nodes ourselves: an explicit stack visits the same nodes in the same depth-first order without any recursion. See [Iterative DFS](#iterative-dfs).
3. **Vary the order.** Because the swap is local, the worklist does not have to be a stack at all. Replacing it with a queue turns the walk into a level-order traversal, trading the height-bounded `O(h)` stack for a width-bounded `O(n)` frontier. See [Iterative BFS](#iterative-bfs).

## Solutions

### Recursive DFS

#### Derivation

The question to ask is what "inverted" means for a single node. Inverting a binary tree is self-similar: the inverted tree is the one whose root children are swapped and whose two subtrees are themselves inverted. That [recursive](https://en.wikipedia.org/wiki/Recursion_(computer_science)) definition translates directly into code:

1. Base case: when `root` is `None`, there is nothing to invert, so return `None`.
2. Swap the current node's `left` and `right` children with a single tuple assignment.
3. Recursively invert what is now the left subtree and what is now the right subtree.
4. Return `root`, which is the root of the fully inverted tree.

The swap can happen before or after the recursive calls because each node's swap is independent of its descendants; this version swaps first (a pre-order shape), but a post-order swap produces the identical result.

#### Walkthrough

Let us watch the Recursive DFS solution run on Example 1: `root = [4,2,7,1,3,6,9]`. As a tree, that is `4` with left child `2` (children `1`, `3`) and right child `7` (children `6`, `9`).

Each call swaps the current node's two children, then recurses into the new left child and the new right child. The indentation below shows the call tree: a deeper indent is a nested recursive call, and we read each call top to bottom.

```text
invertTree(4): swap children -> 4.left=7, 4.right=2
  invertTree(7): swap children -> 7.left=9, 7.right=6
    invertTree(9): no children, swap does nothing, returns
    invertTree(6): no children, swap does nothing, returns
  invertTree(2): swap children -> 2.left=3, 2.right=1
    invertTree(3): no children, swap does nothing, returns
    invertTree(1): no children, swap does nothing, returns
```

Tracing the swaps in order:

- `invertTree(4)`: swap `2` and `7`, so node `4` now has left `7`, right `2`. Recurse into `7` first, then `2`.
- `invertTree(7)`: swap `6` and `9`, so node `7` now has left `9`, right `6`. Recurse into the leaves `9` and `6`, each of which has no children and returns immediately.
- `invertTree(2)`: swap `1` and `3`, so node `2` now has left `3`, right `1`. Recurse into the leaves `3` and `1`, which also return immediately.

After every node's children have been swapped, the original call `invertTree(4)` returns the same `root` node. Reading the inverted tree in level order gives `[4,7,2,9,6,3,1]`, which matches the example's expected Output.

#### Solution

The code is the recursive definition written down: swap, then invert each subtree.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is visited exactly once, and each visit does a constant-time swap, so the total work is linear in the number of nodes `n`.

##### Space Complexity: `O(h)`, where `h` is the height of the tree

The only extra space is the recursion stack, whose depth equals the height of the tree. A balanced tree gives `O(log n)`; a skewed tree degrades to `O(n)`.

#### Key Insights

- The inversion is defined recursively in terms of itself: swap the children, then invert both subtrees.
- Tuple assignment swaps the two children without an explicit temporary variable.
- Because each swap is local and independent, the relative order of the swap and the recursive calls does not change the outcome.
- Inverting an already inverted tree restores the original, so the operation is its own inverse.

### Iterative DFS

#### Derivation

The recursive version leans on the call stack, which caps how deep a tree it can handle. Because each node's swap is independent, the recursion can be made explicit by managing the pending nodes with a stack instead of the call stack. This keeps the same [depth-first](https://en.wikipedia.org/wiki/Depth-first_search) visit order:

1. Return `None` when the tree is empty.
2. Seed a stack with `root`.
3. While the stack is non-empty, pop a node and swap its `left` and `right` references.
4. Push both children so their subtrees are inverted in turn.
5. Return the original `root`.

This is the explicit-stack equivalent of the recursive version, useful when recursion depth is a concern but a depth-first order is still preferred over the wide frontier a queue can build.

#### Walkthrough

Let us run the explicit stack on Example 1: `root = [4,2,7,1,3,6,9]`, the tree

```text
    4
   / \
  2   7
 / \ / \
1  3 6  9
```

The `stack` starts as `[4]`. Each line pops one `node`, swaps its children, and pushes the (post-swap) left child then the right child:

```text
pop 4   swap -> 4.left=7, 4.right=2   push 7, push 2   stack = [7, 2]
pop 2   swap -> 2.left=3, 2.right=1   push 3, push 1   stack = [7, 3, 1]
pop 1   leaf, swap does nothing                        stack = [7, 3]
pop 3   leaf, swap does nothing                        stack = [7]
pop 7   swap -> 7.left=9, 7.right=6   push 9, push 6   stack = [9, 6]
pop 6   leaf, swap does nothing                        stack = [9]
pop 9   leaf, swap does nothing                        stack = []
```

Popping from the end of the list means the most recently pushed node is processed next, so the walk dives through `4`'s new right subtree (`2`, then its leaves) before returning to `7`: a depth-first order, just like the recursion, only driven by an explicit list. When the stack empties, every node has been swapped exactly once, and reading the tree in level order gives `[4,7,2,9,6,3,1]`, the expected Output.

#### Solution

The code is the walkthrough's loop: pop, swap, push both children until the stack is empty.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        stack = [root]
        while stack:
            node = stack.pop()
            node.left, node.right = node.right, node.left
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return root
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is pushed and popped exactly once and performs a constant-time swap, giving linear time.

##### Space Complexity: `O(h)`, where `h` is the height of the tree

A depth-first stack holds at most one root-to-leaf path plus pending siblings, so its size tracks the tree height rather than its width. This is `O(log n)` for a balanced tree and `O(n)` for a skewed one.

#### Key Insights

- Replacing the implicit call stack with an explicit stack reproduces the recursive version while avoiding recursion-depth limits.
- The swap is again local, so neither the data structure nor the visit order affects correctness.
- Tuple assignment swaps the two children without an explicit temporary variable.

### Iterative BFS

#### Derivation

The iterative DFS made the worklist explicit, which raises the question of whether it must be a stack at all. Swapping the stack for a queue turns the depth-first walk into a level-order ([breadth-first](https://en.wikipedia.org/wiki/Breadth-first_search)) one while keeping the logic identical:

1. Return `None` immediately when the tree is empty.
2. Seed a queue with `root`.
3. While the queue is non-empty, dequeue a node and swap its `left` and `right` references.
4. Enqueue both children (after the swap, either order is fine) so their subtrees are inverted in turn.
5. Return the original `root`, now the root of the fully inverted tree.

The only change from the iterative DFS version is which end of the pending collection is consumed next, which trades the height-bounded stack for a width-bounded frontier.

#### Walkthrough

Let us run the queue on the same Example 1 tree drawn in the Iterative DFS walkthrough: `root = [4,2,7,1,3,6,9]`. The `queue` starts as `[4]`. Each line takes `node` from the front with `popleft`, swaps its children, and appends the (post-swap) left child then the right child at the back:

```text
popleft 4   swap -> 4.left=7, 4.right=2   enqueue 7, 2   queue = [7, 2]
popleft 7   swap -> 7.left=9, 7.right=6   enqueue 9, 6   queue = [2, 9, 6]
popleft 2   swap -> 2.left=3, 2.right=1   enqueue 3, 1   queue = [9, 6, 3, 1]
popleft 9   leaf, swap does nothing                      queue = [6, 3, 1]
popleft 6   leaf, swap does nothing                      queue = [3, 1]
popleft 3   leaf, swap does nothing                      queue = [1]
popleft 1   leaf, swap does nothing                      queue = []
```

Consuming from the front means nodes are processed in the order they were discovered: the root, then the whole second level (`7`, `2`), then the whole third level (`9`, `6`, `3`, `1`). After the root's swap the queue momentarily holds one full level, `[7, 2]` and later `[9, 6, 3, 1]`, which is the width-bounded frontier the complexity analysis charges for. Every node is swapped exactly once, and the finished tree reads in level order as `[4,7,2,9,6,3,1]`, the expected Output.

#### Solution

The code is the walkthrough's loop with `deque` as the queue: dequeue from the front, swap, enqueue both children.

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
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        queue = deque([root])
        while queue:
            node = queue.popleft()
            node.left, node.right = node.right, node.left
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return root
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is enqueued and dequeued exactly once and performs a constant-time swap, giving linear time in the number of nodes.

##### Space Complexity: `O(n)`

The queue holds at most one full level at a time. For a complete tree the widest level is up to `n/2` nodes, so the auxiliary space is `O(n)`.

#### Key Insights

- A stack and a queue differ only in which pending node is processed next; both invert the whole tree.
- The inversion is purely local: swapping each node's children in any order inverts the whole tree.
- BFS is chosen here only to contrast with the depth-first versions; the wider frontier gives it `O(n)` space rather than the `O(h)` of a depth-first walk.

## Comparison of Solutions

### Time Complexity

- **Recursive DFS**: `O(n)` - Each node is visited once.
- **Iterative DFS**: `O(n)` - Each node is pushed and popped once.
- **Iterative BFS**: `O(n)` - Each node is enqueued and dequeued once.

### Space Complexity

- **Recursive DFS**: `O(h)` - Recursion stack equal to the tree height.
- **Iterative DFS**: `O(h)` - Explicit stack tracks a path, bounded by the tree height.
- **Iterative BFS**: `O(n)` - Queue holds up to one full level, which can be `O(n)` wide.

### Trade-offs

- The recursive version is the most concise and reads naturally as "swap, then invert each subtree."
- The iterative DFS version makes the call stack explicit, avoiding recursion limits yet keeping the smaller height-bounded space of a depth-first walk.
- The iterative BFS version swaps the stack for a queue, sidestepping the recursion-depth ceiling, but its frontier can grow to the widest level.

### When to Use Each

- **Recursive DFS**: When code clarity is valued and the tree depth is bounded.
- **Iterative DFS**: When the tree may be deep enough to risk a recursion-limit error and the smaller depth-first frontier is preferable to a queue.
- **Iterative BFS**: When a breadth-first order is wanted and the tree is not pathologically deep.

### Optimization Notes

- All three approaches are `O(n)` time, so the choice is driven by space and recursion-depth concerns.
- Because each node's swap is independent, any traversal order works; the data structure (recursion stack, queue, or explicit stack) only changes the visit order, not the result.
- For skewed trees the height-bounded `O(h)` stack of the depth-first approaches degrades to `O(n)`, matching the BFS queue; for balanced trees the depth-first space stays at `O(log n)` while the BFS frontier reaches `O(n)`.
