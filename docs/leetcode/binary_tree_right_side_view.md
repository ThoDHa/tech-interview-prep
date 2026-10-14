# [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/)

**Medium** | **20 minutes** | **Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)

**Practice:** [`practice/binary_tree_right_side_view/solution.py`](../../practice/binary_tree_right_side_view/solution.py)

Given the `root` of a binary tree, imagine yourself standing on the **right side** of it, return the values of the nodes you can see ordered from top to bottom.

## Examples

### Example 1

![Binary Tree Right Side View Example1](assets/binary_tree_right_side_view_example1.jpg)

**Input:** `root = [1,2,3,null,5,null,4]`

**Output:** `[1,3,4]`

### Example 2

![Binary Tree Right Side View Example 2](assets/binary_tree_right_side_view_example2.png)

**Input:** `root = [1,null,3]`

**Output:** `[1,3]`

### Example 3

**Input:** `root = []`

**Output:** `[]`

## Constraints

- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

## Deriving the Solution

Standing on the right, the node visible at each level is the rightmost one, so the answer is the last node of every level when the level is read left to right. Every solution below works from that reformulation; they differ only in how much of each level they keep around to find its last node.

1. **Start literal.** Bucket every node's value by depth, then read the last entry of each bucket. One traversal plus one final pass, but it stores entire levels when only a single value per level matters: see [Brute Force](#brute-force).
2. **Keep only the winner.** The rightmost node of a level is the *first* one a traversal reaches if it always descends the right child before the left, so a right-first DFS can record exactly one node per depth and skip the buckets entirely: see [Recursive DFS](#recursive-dfs).
3. **Read it off level by level.** A queue drained one level at a time hands over each level in left-to-right order, so the last node dequeued per level is the answer directly, with no ordering argument needed: see [Iterative BFS](#iterative-bfs).

## Solutions

### Brute Force

#### Derivation

The most direct reading of the problem is literal: group every node by its level, then the rightmost node of each level is simply the last one written when we walk left to right. This needs no clever ordering trick, just an honest bucket-per-depth collection:

1. Walk the tree with a plain [depth-first traversal](https://en.wikipedia.org/wiki/Depth-first_search), carrying the current `depth`.
2. The first time a `depth` is reached, append a fresh empty list so `levels[depth]` exists.
3. Append the current node's value to its depth's bucket, then recurse left child before right child so each bucket fills left to right.
4. After the walk, take the last value of every bucket: that is the node visible from the right.

#### Walkthrough

Let us trace the Brute Force on Example 1, `root = [1,2,3,null,5,null,4]`, whose tree looks like this:

```text
        1          depth 0
       / \
      2   3        depth 1
       \   \
        5   4      depth 2
```

`collect` recurses left child before right child, carrying `depth`. Each call appends the node's value to `levels[depth]`, creating a fresh bucket the first time a depth is reached. The order of calls is therefore `1` (depth 0), then `2` and its right child `5` (depths 1 and 2), then back up to `3` and its right child `4`:

| Step | Node visited (`depth`) | New bucket? | `levels` after the call |
| --- | --- | --- | --- |
| 1 | `1` (0) | yes, `levels[0]` | `[[1]]` |
| 2 | `2` (1) | yes, `levels[1]` | `[[1], [2]]` |
| 3 | `5` (2) | yes, `levels[2]` | `[[1], [2], [5]]` |
| 4 | `3` (1) | no | `[[1], [2, 3], [5]]` |
| 5 | `4` (2) | no | `[[1], [2, 3], [5, 4]]` |

Notice that node `2` has no left child, so after visiting `5` the recursion unwinds back to the root and descends into `3`. Because the walk fills each bucket left to right, `3` lands after `2` in `levels[1]`, and `4` lands after `5` in `levels[2]`.

The final pass takes the last value of every bucket: `levels[0][-1] = 1`, `levels[1][-1] = 3`, `levels[2][-1] = 4`. The function returns `[1, 3, 4]`, which matches the expected Output.

#### Solution

The code is the walkthrough's collection pass followed by the last-of-each-bucket read.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        levels = []

        def collect(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return
            # Grow the list of levels until it has a slot for this depth
            if depth == len(levels):
                levels.append([])
            levels[depth].append(node.val)
            collect(node.left, depth + 1)
            collect(node.right, depth + 1)

        collect(root, 0)
        # The viewer on the right sees the last value recorded at each level
        return [level[-1] for level in levels]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is visited once with constant work, and the final pass reads each bucket's last element across all `n` nodes, so the total stays linear.

##### Space Complexity: `O(n)`

The `levels` structure stores every node's value, so it grows to `O(n)` overall, on top of the `O(h)` recursion stack.

#### Key Insights

- Mirrors the problem statement directly: bucket nodes by level, then read the rightmost of each.
- Requires no ordering trick, which makes it the easiest version to derive but the most wasteful in space.
- Storing whole levels is redundant when only the last node of each is needed, which the next approaches eliminate.

### Recursive DFS

#### Derivation

The Brute Force stores every value on every level, then throws away all but one per bucket. The repair comes from asking which single node per level to keep, and how to recognize it without seeing the whole level. The answer: if a [depth-first traversal](https://en.wikipedia.org/wiki/Depth-first_search) always explores the right subtree before the left, then the first node it reaches at any depth is the rightmost node on that level, so recording only the first arrival per depth suffices:

1. Track the current `depth`, starting at `0` for the root.
2. When `depth == len(result)`, no node has been recorded for this level yet, so the current node is the first (and therefore rightmost) one seen there. Append its value.
3. Recurse into the right child first, then the left child, both at `depth + 1`.

Because the right branch is always visited before the left, deeper-right nodes are recorded ahead of any left node at the same depth. The `depth == len(result)` guard ensures only that first node per level is captured, which is exactly the right side view.

#### Walkthrough

Let us run the right-first traversal on Example 1, `root = [1,2,3,null,5,null,4]`. Each line shows one `visit` call in the order the recursion makes them, whether the guard fires, and `result` afterward:

```text
        1          depth 0
       / \
      2   3        depth 1
       \   \
        5   4      depth 2

visit(1, depth=0)    depth 0 == len(result) = 0 -> record 1    result = [1]
visit(3, depth=1)    depth 1 == len(result) = 1 -> record 3    result = [1, 3]
visit(4, depth=2)    depth 2 == len(result) = 2 -> record 4    result = [1, 3, 4]
visit(2, depth=1)    depth 1 < len(result) = 3 -> skip         result = [1, 3, 4]
visit(5, depth=2)    depth 2 < len(result) = 3 -> skip         result = [1, 3, 4]
```

From the root, the traversal dives right first: `1`, then `3`, then `3`'s right child `4`. Each arrives at a brand-new depth, so all three are recorded. Only then does the recursion unwind and descend the left side: `2` and its right child `5` reach depths `1` and `2` after those levels were already claimed by `3` and `4`, so the guard skips them. The traversal ends with `result = [1, 3, 4]`, matching the expected Output.

#### Solution

The code is the right-first walk from the trace, with the `depth == len(result)` guard doing the recording.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        result = []

        def visit(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return
            # First node reached at this depth is the rightmost, because
            # we always descend the right child before the left
            if depth == len(result):
                result.append(node.val)
            visit(node.right, depth + 1)
            visit(node.left, depth + 1)

        visit(root, 0)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is visited once with constant work, so the traversal is linear in the number of nodes.

##### Space Complexity: `O(h)`

No queue is used; the only auxiliary space is the recursion stack, which reaches the tree height `h`. This is `O(n)` for a skewed tree and `O(log n)` when balanced.

#### Key Insights

- Visiting right before left makes "first node at a depth" equivalent to "rightmost node at that level."
- The `depth == len(result)` check records exactly one node per level, with no need to track level sizes.
- Auxiliary space is `O(h)` rather than the brute force's `O(n)` storage, trimming the per-level buckets down to a single value each.
- The mirror version (visit left before right with the same guard) yields the left side view.

### Iterative BFS

#### Derivation

The right-first DFS rests on a subtle ordering argument. Asking instead for a traversal in which "last node of each level" is directly visible leads to [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search): process the tree one level at a time, and the node a viewer on the right sees is simply the final one dequeued on each level:

1. Return an empty list immediately when the tree is empty.
2. Seed a queue with `root` and process the tree level by level.
3. Before draining a level, record its size (`level_size`) so we know how many nodes belong to the current level.
4. Dequeue exactly `level_size` nodes; the final one (index `level_size - 1`) is the rightmost node visible from the right.
5. Enqueue each node's left child then right child so the next level stays ordered left to right.

Because children are enqueued left before right, the last node dequeued on every level is guaranteed to be the rightmost, which is precisely the node a viewer on the right would see.

#### Walkthrough

Let us run the queue on Example 1, `root = [1,2,3,null,5,null,4]`. Each round snapshots `level_size`, dequeues that many nodes, and records only the one at index `level_size - 1`:

```text
        1          level 0
       / \
      2   3        level 1
       \   \
        5   4      level 2

queue = [1]                                                 seeded with root
level_size = 1   i=0  pop 1   last index -> record 1    push 2, 3    result = [1]
                 queue = [2, 3]
level_size = 2   i=0  pop 2                             push 5
                 i=1  pop 3   last index -> record 3    push 4       result = [1, 3]
                 queue = [5, 4]
level_size = 2   i=0  pop 5
                 i=1  pop 4   last index -> record 4                 result = [1, 3, 4]
queue empty -> loop ends
```

On the middle level, `2` is dequeued first and passed over; only `3`, sitting at index `level_size - 1 = 1`, is recorded. Its child `4` is enqueued after `5`, so on the bottom level `4` is again the last one out. The loop ends with `result = [1, 3, 4]`, matching the expected Output.

#### Solution

The code is the walkthrough's loop written down: snapshot `level_size`, drain the level, and keep the value at index `level_size - 1`.

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
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            for i in range(level_size):
                node = queue.popleft()
                # The last node dequeued at this level is the rightmost
                if i == level_size - 1:
                    result.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` nodes is enqueued and dequeued exactly once, and the work per node is constant.

##### Space Complexity: `O(n)`

The queue holds at most one full level at a time. In the worst case (a complete tree), the widest level contains up to `n/2` nodes, so the queue grows to `O(n)`.

#### Key Insights

- The right side view question reduces to "last node of each level," which BFS surfaces naturally.
- Capturing `level_size` before the inner loop cleanly separates levels without extra marker nodes.
- Enqueuing left before right keeps each level in left-to-right order, so the rightmost node is always last.
- A right-first DFS that records the first node seen at each new depth solves it too, but BFS maps more directly to the level-by-level framing.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - Each node is visited once, then each level's last value is read
- **Recursive DFS**: `O(n)` - Each node is visited once
- **Iterative BFS**: `O(n)` - Each node is enqueued and dequeued once

### Space Complexity

- **Brute Force**: `O(n)` - Buckets every node's value by level, plus the `O(h)` recursion stack
- **Recursive DFS**: `O(h)` - Recursion stack equal to the tree height
- **Iterative BFS**: `O(n)` - Queue holds up to one full level, which can be `O(n)` wide

### Trade-offs

- Brute Force reads straight off the problem statement (group by level, take the rightmost) but stores entire levels it never needs.
- Recursive DFS uses no queue and only `O(h)` stack space, which is cheaper for tall, narrow trees but can overflow on extreme depth.
- BFS reads directly as "last node of each level," matching how the problem is usually framed, and peaks at the widest level while DFS peaks at the tallest path.

### When to Use Each

- **Brute Force**: When deriving a first correct solution and clarity matters more than space.
- **Recursive DFS**: When a concise recursive solution is preferred and the tree depth is bounded.
- **Iterative BFS**: When the level-by-level reading is clearest, or when the tree is deep enough to risk recursion limits.

### Optimization Notes

- All three approaches are `O(n)` time, so the decision hinges on auxiliary space and tree shape.
- Brute Force keeps full per-level buckets; the right-first DFS trims each bucket down to a single recorded value, reaching `O(h)` space.
- The right-first visit order is the key idea that lets DFS capture exactly the rightmost node per level.
- The DFS `O(h)` space is strictly better than the BFS `O(n)` width for skewed trees.
