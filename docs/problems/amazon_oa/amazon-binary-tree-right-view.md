# [Binary Tree Right View](https://www.fastprep.io/problems/amazon-binary-tree-right-view)

**Medium** | **NN minutes** | **Tree, Breadth First Search, Depth First Search**

Given the root of a binary tree, imagine viewing the tree from its right side.

Return the value of the visible node at each depth, ordered from the root level downward. For an empty tree, return an empty array.

## Examples

### Example 1

**Input:** `root = [1,2,3,null,5,null,4]`

**Output:** `[1,3,4]`

**Explanation:** The rightmost visible values at successive levels are 1, 3, and 4.

### Example 2

**Input:** `root = [1,null,3]`

**Output:** `[1,3]`

**Explanation:** The right child is visible below the root.

### Example 3

**Input:** `root = []`

**Output:** `[]`

**Explanation:** An empty tree has no visible levels.

## Constraints

- `The tree contains between 0 and 10000 nodes.`
- `-10^9 <= Node.val <= 10^9.`

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

### Brute Force

#### Derivation

The most direct reading of the problem is literal: group every node's value by
its depth, then the node visible from the right at each depth is simply the
last one written when the walk fills the group left to right. No ordering
trick is needed, just an honest bucket per depth:

1. Walk the tree with a plain [depth-first traversal](https://en.wikipedia.org/wiki/Depth-first_search),
   carrying the current `depth`, starting at `0` for the root.
2. The first time a `depth` is reached, append a fresh empty list so
   `levels[depth]` exists.
3. Append the node's value to its depth's bucket, recursing into the left
   child before the right child so each bucket fills left to right.
4. After the walk, take the last value of every bucket: that is the view from
   the right. An empty tree produces no buckets and returns `[]`.

#### Walkthrough

Example 1, `root = [1,2,3,null,5,null,4]`, has two left-side nodes whose
placement exercises the bucket order:

```text
        1          depth 0
       / \
      2   3        depth 1
       \   \
        5   4      depth 2
```

`collect` recurses left child before right child, carrying `depth`, and each
call appends to `levels[depth]`, creating the bucket on first arrival:

| Step | Node visited (`depth`) | New bucket? | `levels` after the call |
| --- | --- | --- | --- |
| 1 | `1` (0) | yes, `levels[0]` | `[[1]]` |
| 2 | `2` (1) | yes, `levels[1]` | `[[1], [2]]` |
| 3 | `5` (2) | yes, `levels[2]` | `[[1], [2], [5]]` |
| 4 | `3` (1) | no | `[[1], [2, 3], [5]]` |
| 5 | `4` (2) | no | `[[1], [2, 3], [5, 4]]` |

Because the walk fills each bucket left to right, `3` lands after `2` and `4`
lands after `5`. The final pass takes the last value of every bucket:
`levels[0][-1] = 1`, `levels[1][-1] = 3`, `levels[2][-1] = 4`, so the function
returns `[1, 3, 4]`, matching the expected Output for Example 1. On Example 2
the buckets are `[[1], [3]]` and the return is `[1, 3]`; on Example 3 the
`collect` call returns immediately from a `None` root, leaving `levels` empty
and the return `[]`.

#### Solution

The code is the walkthrough's collection pass followed by the last-of-each-
bucket read.

```python
from typing import List, Optional


class Solution:
    def solve(self, root: Optional[TreeNode]) -> List[int]:
        levels: List[List[int]] = []

        def collect(node: Optional[TreeNode], depth: int) -> None:
            if node is None:
                return
            if depth == len(levels):
                levels.append([])
            levels[depth].append(node.val)
            collect(node.left, depth + 1)
            collect(node.right, depth + 1)

        collect(root, 0)
        return [level[-1] for level in levels]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node of the tree's `n` nodes is visited once with constant work, and the
final pass reads one value per bucket.

##### Space Complexity: `O(n)`

The `levels` structure stores every node's value, on top of the `O(h)`
recursion stack with `h` the tree height.

#### Key Insights

- Mirrors the problem statement directly: bucket nodes by level, then read the
  rightmost of each.
- Requires no ordering argument, which makes it the easiest version to derive
  but the most wasteful in space.
- Storing whole levels is redundant when only the last node of each is needed,
  which the next approaches eliminate.

### Recursive DFS

#### Derivation

The Brute Force stores every value on every level, then throws away all but
one per bucket. The repair comes from asking which single node per level to
keep, and how to recognize it without seeing the whole level. If a
[depth-first traversal](https://en.wikipedia.org/wiki/Depth-first_search)
always explores the right subtree before the left, then the first node it
reaches at any depth is the rightmost node on that level, so recording only
the first arrival per depth suffices:

1. Track the current `depth`, starting at `0` for the root.
2. When `depth == len(visible)`, no node has been recorded for this level yet,
   so the current node is the first (and therefore rightmost) one seen there.
   Append its value to `visible`.
3. Recurse into the right child first, then the left child, both at
   `depth + 1`.
4. An empty tree never enters the recording branch, so `visible` stays `[]`.

#### Walkthrough

Let us run the right-first traversal on Example 1, `root = [1,2,3,null,5,null,4]`.
Each line shows one `visit` call in the order the recursion makes them, whether
the guard fires, and `visible` afterward:

```text
visit(1, depth=0)    depth 0 == len(visible) = 0 -> record 1    visible = [1]
visit(3, depth=1)    depth 1 == len(visible) = 1 -> record 3    visible = [1, 3]
visit(4, depth=2)    depth 2 == len(visible) = 2 -> record 4    visible = [1, 3, 4]
visit(2, depth=1)    depth 1 < len(visible) = 3 -> skip         visible = [1, 3, 4]
visit(5, depth=2)    depth 2 < len(visible) = 3 -> skip         visible = [1, 3, 4]
```

From the root, the traversal dives right first: `1`, then `3`, then `3`'s
right child `4`. Each arrives at a brand-new depth, so all three are recorded.
Only then does the recursion unwind and descend the left side: `2` and its
right child `5` reach depths `1` and `2` after those levels were already
claimed by `3` and `4`, so the guard skips them. The traversal ends with
`visible = [1, 3, 4]`, matching the expected Output. On Example 2 the dive
records `1` then the right child `3` and returns `[1, 3]`; on Example 3 the
single `visit(None)` returns immediately and `visible` stays `[]`.

#### Solution

The code is the right-first walk from the trace, with the
`depth == len(visible)` guard doing the recording.

```python
from typing import List, Optional


class Solution:
    def solve(self, root: Optional[TreeNode]) -> List[int]:
        visible: List[int] = []

        def visit(node: Optional[TreeNode], depth: int) -> None:
            if node is None:
                return
            if depth == len(visible):
                visible.append(node.val)
            visit(node.right, depth + 1)
            visit(node.left, depth + 1)

        visit(root, 0)
        return visible
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is visited once with constant work, so the traversal is linear in
the number of nodes.

##### Space Complexity: `O(h)`

No queue is used; the only auxiliary space is the recursion stack, which
reaches the tree height `h`. This is `O(n)` for a skewed tree and `O(log n)`
when balanced.

#### Key Insights

- Visiting right before left makes "first node at a depth" equivalent to
  "rightmost node at that level."
- The `depth == len(visible)` check records exactly one node per level, with no
  need to track level sizes.
- The mirror version (visit left before right with the same guard) yields the
  left side view.

### Iterative BFS

#### Derivation

The right-first DFS rests on a subtle ordering argument, and its recursion
depth equals the tree height, which this problem's node cap permits to reach
10,000 on a skewed tree, well past Python's default recursion limit of 1,000.
Asking instead for a traversal in which "last node of each level" is directly
visible, with no recursion at all, leads to [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search):
process the tree one level at a time, and the node a viewer on the right sees
is the final one dequeued on each level:

1. Return `[]` immediately when `root` is `None`.
2. Seed a `queue` with `root` and process the tree level by level.
3. Before draining a level, record its size (`level_size`) so the loop knows
   how many nodes belong to the current level.
4. Dequeue exactly `level_size` nodes; the final one (index
   `level_size - 1`) is the rightmost node visible from the right.
5. Enqueue each node's left child then right child so the next level stays
   ordered left to right.

Because children are enqueued left before right, the last node dequeued on
every level is guaranteed to be the rightmost, which is precisely the node a
viewer on the right would see.

#### Walkthrough

Let us run the queue on Example 1, `root = [1,2,3,null,5,null,4]`. Each round
snapshots `level_size`, dequeues that many nodes, and records only the one at
index `level_size - 1`:

```text
queue = [1]                                                 seeded with root
level_size = 1   position 0  pop 1   last index -> record 1  push 2, 3
                 visible = [1]          queue = [2, 3]
level_size = 2   position 0  pop 2                           push 5
                 position 1  pop 3   last index -> record 3  push 4
                 visible = [1, 3]       queue = [5, 4]
level_size = 2   position 0  pop 5
                 position 1  pop 4   last index -> record 4
                 visible = [1, 3, 4]    queue = [] -> loop ends
```

On the middle level, `2` is dequeued first and passed over; only `3`, sitting
at index `level_size - 1 = 1`, is recorded. Its child `4` is enqueued after
`5`, so on the bottom level `4` is again the last one out. The loop ends with
`visible = [1, 3, 4]`, matching the expected Output. On Example 2 the rounds
record `1` and then `3`; on Example 3 the `None` root returns `[]` before the
queue is ever seeded.

#### Solution

The code is the walkthrough's loop written down: snapshot `level_size`, drain
the level, and keep the value at index `level_size - 1`.

```python
from collections import deque
from typing import List, Optional


class Solution:
    def solve(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []

        visible: List[int] = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            for position_in_level in range(level_size):
                node = queue.popleft()
                if position_in_level == level_size - 1:
                    visible.append(node.val)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
        return visible
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` nodes is enqueued and dequeued exactly once, and the work per
node is constant.

##### Space Complexity: `O(n)`

The queue holds at most one full level at a time. In the worst case (a
complete tree), the widest level contains up to `n / 2` nodes, so the queue
grows to `O(n)`.

#### Key Insights

- The right side view question reduces to "last node of each level," which BFS
  surfaces naturally.
- Capturing `level_size` before the inner loop cleanly separates levels
  without extra marker nodes.
- Enqueuing left before right keeps each level in left-to-right order, so the
  rightmost node is always last.
- With this problem's cap of 10,000 nodes, a skewed tree would drive the
  recursive solutions 10,000 frames deep, past Python's default recursion
  limit of 1,000; the iterative queue has no such ceiling.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - each node is visited once, then each level's last
  value is read.
- **Recursive DFS**: `O(n)` - each node is visited once.
- **Iterative BFS**: `O(n)` - each node is enqueued and dequeued once.

### Space Complexity

- **Brute Force**: `O(n)` - buckets every node's value by level, plus the
  `O(h)` recursion stack.
- **Recursive DFS**: `O(h)` - recursion stack equal to the tree height, `O(n)`
  on a skewed tree.
- **Iterative BFS**: `O(n)` - the queue holds up to one full level, which can
  be `O(n)` wide.

### Trade-offs

- **Brute Force** reads straight off the problem statement (group by level,
  take the rightmost) but stores entire levels it never needs.
- **Recursive DFS** keeps only one recorded value per level and no queue, the
  leanest memory on balanced trees, but its recursion depth is the tree
  height and this problem's node cap makes that a real hazard.
- **Iterative BFS** reads directly as "last node of each level" and cannot hit
  a recursion limit, at the cost of holding a full level in the queue.

### When to Use Each

- **Brute Force**: when deriving a first correct solution and clarity matters
  more than space.
- **Recursive DFS**: when a concise recursive solution is preferred and the
  tree is known to stay shallow.
- **Iterative BFS** (Recommended): the interview default under this problem's
  constraints: it is level-shaped by construction and immune to the recursion
  limit the 10,000-node cap permits a skewed tree to trigger.

### Optimization Notes

- All three approaches are `O(n)` time, so the decision hinges on auxiliary
  space and tree shape.
- Brute Force keeps full per-level buckets; the right-first DFS trims each
  bucket down to a single recorded value, reaching `O(h)` space on balanced
  trees.
- The DFS `O(h)` space beats the BFS `O(n)` width only while the height stays
  small; on this page the height may reach 10,000, which flips the
  recommendation toward the queue.
- The mirror version of the DFS (visit left before right with the same first-
  arrival guard) produces the left side view with one line changed.
