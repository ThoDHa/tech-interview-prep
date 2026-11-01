# [Binary Tree Spiral Level Order](https://www.fastprep.io/problems/amazon-binary-tree-spiral-level-order)

**Medium** | **NN minutes** | **Tree, Breadth First Search, Depth First Search**

Return the values of a binary tree one level at a time in alternating directions.

For this exercise, assume the root level is traversed left to right, the next level right to left, and directions alternate thereafter. Group values by their distance from the root and omit missing children. Preserve node positions even when values repeat. An empty tree returns an empty list.

## Examples

### Example 1

**Input:** `root = [3,9,20,null,null,15,7]`

**Output:** `[[3],[20,9],[15,7]]`

**Explanation:** The root is left-to-right, the second level is right-to-left, and the third returns to left-to-right.

### Example 2

**Input:** `root = [1,2,3,4,null,null,5]`

**Output:** `[[1],[3,2],[4,5]]`

**Explanation:** Null links are skipped; the second level is [3,2] and the third is [4,5].

### Example 3

**Input:** `root = []`

**Output:** `[]`

**Explanation:** An empty tree has no levels.

## Constraints

- `For this exercise, assume a finite acyclic binary tree with 0 through 500 nodes.`
- `-10^6 <= node.val <= 10^6.`

## Deriving the Solution

Every approach must recover the same two facts from the tree: which level a node sits on, and in which direction that level is read. Both facts come from the same observation: the root is at depth 0, and every child sits one level deeper than its parent, so a traversal that carries the depth alongside the node can group values without measuring positions.

1. **Start literal.** Walk the tree depth-first, carrying each node's depth, and append every value into a per-depth bucket. Reverse the buckets of odd depth and the buckets are the answer: see [Depth-Bucketed DFS](#depth-bucketed-dfs).
2. **Drop the bookkeeping.** The DFS still threads a depth argument through every call just to learn what a level-order traversal hands you for free: a queue drains the tree exactly one level per round, so the grouping is implicit in the queue's own state: see [Level-Size BFS](#level-size-bfs).

## Solutions

### Depth-Bucketed DFS

#### Derivation

The most literal reading of the statement is to classify every node by its distance from the root. A depth-first traversal computes that distance on the way down: the root is at depth 0, and recursing into a child adds one. Collecting values into one bucket per depth therefore groups the levels directly, and the visit order within a bucket is left to right as long as the recursion always enters the left subtree before the right one. Reversing every odd-depth bucket then flips the direction on exactly the levels the statement reads right to left:

1. Keep a list of buckets; the first bucket visited at a new depth grows the list by one, so `len(levels)` is the current deepest depth.
2. Recurse with an explicit stack of `(node, depth)` pairs, pushing the right child first so the left child is processed first.
3. Append `node.val` to `levels[depth]`, creating the bucket when `depth == len(levels)`.
4. Return the buckets with every odd-indexed bucket reversed.

#### Walkthrough

Example 1, `root = [3,9,20,null,null,15,7]`. The stack is drawn with its top on the left, and each line shows the bucket a value lands in:

```text
visit (3, 0)   levels = [[3]]
visit (9, 1)   levels = [[3], [9]]
visit (15, 2)  levels = [[3], [9], [15]]
visit (7, 2)   levels = [[3], [9], [15, 7]]
visit (20, 1)  levels = [[3], [9, 20], [15, 7]]
reverse odd    levels = [[3], [20, 9], [15, 7]]
```

The buckets fill left to right while the traversal runs, and reversing the middle bucket turns it into `[20, 9]`, matching the expected Output.

#### Solution

```python
from typing import List, Optional


class Solution:
    def zigzagLevels(self, root: Optional[TreeNode]) -> List[List[int]]:
        levels: List[List[int]] = []
        stack = [(root, 0)] if root is not None else []

        while stack:
            node, depth = stack.pop()
            if depth == len(levels):
                levels.append([])
            levels[depth].append(node.val)
            if node.right is not None:
                stack.append((node.right, depth + 1))
            if node.left is not None:
                stack.append((node.left, depth + 1))

        return [bucket[::-1] if index % 2 else bucket for index, bucket in enumerate(levels)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is pushed once, popped once, and appended to one bucket; the final pass reverses each bucket at most once, touching every value a constant number of times.

##### Space Complexity: `O(n)`

The buckets hold all `n` values and the stack holds at most one root-to-leaf path, which is `O(h)` for height `h` and `O(n)` on a skewed tree.

#### Key Insights

- A DFS learns a node's level for free by carrying `depth` down the recursion, so grouping by level needs no queue and no per-level snapshots.
- The left-first visit order is what makes each bucket left-to-right; pushing the right child onto the stack first guarantees the left child pops first.
- The depth compare `depth == len(levels)` doubles as the bucket creator, so no dictionary and no preallocated table is needed.

### Level-Size BFS

#### Derivation

The DFS carries a `depth` argument per node solely to recover information a queue produces on its own: a breadth-first queue drains exactly one level per round, because a node's children can only enter the queue after every node of the current level. Snapshot the queue before the level drains, and the snapshot is the level read left to right, no depth tracking required. Reversing alternate snapshots then alternates the reading direction exactly as the statement asks. The explicit queue also removes the recursion limit a very deep input would impose on the DFS variant:

1. Seed the queue with `root` unless the tree is empty.
2. While the queue is non-empty, snapshot `level_values` as the values of the nodes currently queued, in queue order.
3. Append `level_values` reversed when `len(levels)` is odd, as-is when even.
4. Drain exactly `len(frontier)` nodes, enqueueing each node's children left before right.

#### Walkthrough

Example 2, `root = [1,2,3,4,null,null,5]`. Each row is one round: the snapshot, the direction decision, and the children that enqueue (left before right):

```text
round 0  frontier = [1]        snapshot [1]     even, keep      enqueue 2, 3
round 1  frontier = [2, 3]     snapshot [2, 3]  odd, reverse    enqueue 4 (of 2), 5 (of 3)
round 2  frontier = [4, 5]     snapshot [4, 5]  even, keep      no children

levels = [[1], [3, 2], [4, 5]]
```

Round 1's snapshot `[2, 3]` reverses to `[3, 2]`, and round 2 returns to left-to-right `[4, 5]`, matching the expected Output.

#### Solution

The code is the walkthrough's round structure: snapshot the queue, choose the direction, drain the level, enqueue the children.

```python
from collections import deque
from typing import List, Optional


class Solution:
    def zigzagLevels(self, root: Optional[TreeNode]) -> List[List[int]]:
        levels: List[List[int]] = []
        frontier = deque([root] if root is not None else [])

        while frontier:
            level_values = [node.val for node in frontier]
            levels.append(level_values[::-1] if len(levels) % 2 else level_values)
            for _ in range(len(frontier)):
                node = frontier.popleft()
                if node.left is not None:
                    frontier.append(node.left)
                if node.right is not None:
                    frontier.append(node.right)

        return levels
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is enqueued once, dequeued once, and its value copied into exactly one snapshot; reversing odd snapshots touches each of those values at most once more.

##### Space Complexity: `O(n)`

The output holds all `n` values and the queue holds at most one full level, which is `O(n)` wide on a complete tree.

#### Key Insights

- A level-size BFS needs no depth argument: the queue's length before a round is the level's width, and the queue's order inside a round is the level's left-to-right order.
- Reversing the snapshot instead of enqueueing children in alternating order keeps the child enqueueing uniform, which is where most zigzag implementations go wrong.
- Building `level_values` from the queue before draining any node is safe because a list comprehension over a `deque` iterates without consuming; the drain loop then pops exactly the snapshotted nodes.

## Comparison of Solutions

### Time Complexity

- **Depth-Bucketed DFS**: `O(n)` - each node is visited once and appended once.
- **Level-Size BFS**: `O(n)` - each node is enqueued, snapshotted, and dequeued once.

### Space Complexity

- **Depth-Bucketed DFS**: `O(n)` - value buckets plus a stack bounded by the tree height.
- **Level-Size BFS**: `O(n)` - value buckets plus a queue bounded by the widest level.

### Trade-offs

- **Depth-Bucketed DFS**: the shortest path from the statement to code, and the stack never exceeds one root-to-leaf path; the price is threading a `depth` argument and a second pass to reverse odd buckets.
- **Level-Size BFS**: the grouping is implicit in the queue and each level is finished in one round; the price is the snapshot discipline (snapshot before draining) and queue memory that can hold a full wide level.

### When to Use Each

- **Depth-Bucketed DFS**: when the input arrives as a recursive structure and the traversal is naturally written depth-first, or when memory must stay bounded by tree height rather than level width.
- **Level-Size BFS (Recommended)**: the answer to give in an interview: the queue mirrors the level-by-level output directly, the direction flip is one conditional, and no argument threading is needed.

### Optimization Notes

- Reversing the snapshot (`level_values[::-1]`) instead of enqueueing children right-to-left on odd levels keeps one enqueue order for every round; the alternative mixes two orderings and is a common source of subtle bugs.
- The `500`-node bound keeps a left-skewed input well inside Python's default recursion limit, so the recursive variant of the DFS is also safe here; the explicit-stack form shown above is the habit that generalizes to unbounded inputs.
- Both approaches touch each value a constant number of times, so the choice between them is about traversal style, not asymptotics.
