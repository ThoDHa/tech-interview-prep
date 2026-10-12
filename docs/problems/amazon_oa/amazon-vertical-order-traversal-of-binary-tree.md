# [Vertical Order Traversal of a Binary Tree](https://www.fastprep.io/problems/amazon-vertical-order-traversal-of-binary-tree)

**Medium** | **NN minutes** | **Tree, Breadth First Search, Hash Table, Sorting**

You are given a binary tree serialized as a level-order array levelOrder. Each non-null token is a signed decimal integer, and the token "null" denotes a missing child.

Place the root at row 0, column 0. For a node at row r, column c:

Its left child is at row r + 1, column c - 1.Its right child is at row r + 1, column c + 1.Return the node values grouped by column from the smallest column to the largest. Within one column, order nodes by increasing row. When multiple nodes share the same row and column, preserve their breadth-first left-to-right encounter order; do not sort them by value.

If the tree is empty, return an empty list.

## Examples

### Example 1

**Input:** `levelOrder = ["3","9","20","null","null","15","7"]`

**Output:** `[[9],[3,15],[20],[7]]`

**Explanation:** The columns from left to right are -1, 0, 1, and 2.

### Example 2

**Input:** `levelOrder = ["1","2","3","4","6","5","7"]`

**Output:** `[[4],[2],[1,6,5],[3],[7]]`

**Explanation:** Nodes 6 and 5 share row 2 and column 0. Breadth-first left-to-right encounter order places 6 before 5.

### Example 3

**Input:** `levelOrder = []`

**Output:** `[]`

**Explanation:** An empty tree has no columns.

## Constraints

- `0 <= non-null node count <= 10^5.`
- `Every non-null token represents a signed 32-bit integer.`
- `levelOrder is a valid level-order serialization using "null" markers.`

## Solutions

The solutions below rebuild the tree from the level-order tokens and assume the standard node definition:

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

### BFS with Sorted Records

#### Derivation

The input is a list of tokens, not a tree, so the first duty is deserialization, and the serialization format names the tool: a level-order encoding is itself a breadth-first recording, so a queue replays it. The first token builds the root, and every later non-null token attaches as the next free child slot in level order, left before right. A queue of parents awaiting children consumes the tokens two at a time: pop a parent, read its left token then its right token, enqueue each child that exists.

With the tree rebuilt, the coordinates come free during a second queue pass: the root sits at `(0, 0)`, and popping a node at `(row, col)` places its left child at `(row + 1, col - 1)` and its right child at `(row + 1, col + 1)`. Each visit writes one record `(col, row, encounter, value)`, where `encounter` is the visit's position in the queue. That tuple order is deliberate: sorting the records as plain tuples groups by column first, breaks row ties by row, and breaks row ties by the breadth-first encounter order the statement demands, all with one comparison sort and no custom key:

1. Guard the empty token list and return `[]`.
2. Build the root from token `0`; walk `parents` and `token_index` two tokens
   per parent, creating and enqueueing non-null children.
3. Run the coordinate BFS from `(root, 0, 0)`, appending
   `(col, row, len(records), node.val)` for every visit.
4. `records.sort()`.
5. Walk the sorted records, opening a new column list whenever `col` changes
   from the previous record, and append each `value` to the open column.

#### Walkthrough

Example 2 is the tie example, `levelOrder = ["1","2","3","4","6","5","7"]`:

```text
            1            row 0, col 0
           / \
          2   3          row 1, cols -1 and 1
         / \ / \
        4  6 5  7        row 2, cols -2, 0, 0, 2
```

The rebuild drains the token list two per parent, and the coordinate BFS writes one record `(col, row, encounter, value)` per visit:

```text
build    1 takes "2","3"    2 takes "4","6"    3 takes "5","7"   tokens end
visit    1 at (0, 0)   record ( 0, 0, 0, 1)
         2 at (1, -1)  record (-1, 1, 1, 2)
         3 at (1, 1)   record ( 1, 1, 2, 3)
         4 at (2, -2)  record (-2, 2, 3, 4)
         6 at (2, 0)   record ( 0, 2, 4, 6)
         5 at (2, 0)   record ( 0, 2, 5, 5)
         7 at (2, 2)   record ( 2, 2, 6, 7)
sort     (-2,2,3,4) (-1,1,1,2) (0,0,0,1) (0,2,4,6) (0,2,5,5) (1,1,2,3) (2,2,6,7)
group    col -2 [4]   col -1 [2]   col 0 [1, 6, 5]   col 1 [3]   col 2 [7]
```

The decisive records are the pair for nodes `6` and `5`: both sit at `(2, 0)`, and the encounter key orders the queue's left-to-right discovery (`6` under `2` before `5` under `3`), giving `[1, 6, 5]` exactly as the statement requires instead of the value-sorted `[1, 5, 6]`. The grouped output is `[[4],[2],[1,6,5],[3],[7]]`, matching the expected Output. On Example 1 the same process yields columns `-1` through `2` holding `[9], [3, 15], [20], [7]`; on Example 3 the guard returns `[]`.

#### Solution

The code is the walkthrough's two queue passes: replay the tokens into a tree, then record coordinates and sort.

```python
from collections import deque
from typing import List, Tuple


class Solution:
    def verticalOrder(self, levelOrder: List[str]) -> List[List[int]]:
        if not levelOrder:
            return []

        root = TreeNode(int(levelOrder[0]))
        parents = deque([root])
        token_index = 1
        while parents and token_index < len(levelOrder):
            parent = parents.popleft()
            left_token = (levelOrder[token_index]
                          if token_index < len(levelOrder) else "null")
            right_token = (levelOrder[token_index + 1]
                           if token_index + 1 < len(levelOrder) else "null")
            token_index += 2
            if left_token != "null":
                parent.left = TreeNode(int(left_token))
                parents.append(parent.left)
            if right_token != "null":
                parent.right = TreeNode(int(right_token))
                parents.append(parent.right)

        records: List[Tuple[int, int, int, int]] = []
        queue = deque([(root, 0, 0)])
        while queue:
            node, row, col = queue.popleft()
            records.append((col, row, len(records), node.val))
            if node.left:
                queue.append((node.left, row + 1, col - 1))
            if node.right:
                queue.append((node.right, row + 1, col + 1))

        records.sort()
        columns: List[List[int]] = []
        for position, record in enumerate(records):
            new_column = position == 0 or record[0] != records[position - 1][0]
            if new_column:
                columns.append([])
            columns[-1].append(record[3])
        return columns
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Both queue passes touch each of the `n` nodes once, and the sort over `n` records dominates.

##### Space Complexity: `O(n)`

The tree, the queue, and the record list each hold one entry per node.

#### Key Insights

- A level-order serialization replays through a queue of parents reading two tokens each; no index arithmetic over the array is needed.
- Packing the record as `(col, row, encounter, value)` makes one ascending tuple sort perform the entire ordering contract: columns left to right, rows top to bottom, ties in breadth-first encounter order.
- The encounter key, not the node value, breaks `(row, col)` ties; sorting ties by value is the classic wrong turn this problem is built to catch.

### DFS with Pre-Order Records

#### Derivation

The queue does two jobs above: rebuild the tree and fix the encounter order. The rebuild stands, but can the record collection run as a [depth-first traversal](https://en.wikipedia.org/wiki/Depth-first_search)? The worry is tie order: a pre-order walk visits whole subtrees before moving right, which interleaves rows and looks nothing like breadth-first order. The tie rule, however, only ever compares nodes sharing one row, and within a single row pre-order preserves breadth-first order exactly. The induction: row `r + 1` nodes appear in pre-order grouped by parent in the order those parents appear, because subtrees never interleave; the left child of a parent precedes the right child in both orders. Row `r` nodes already match by induction, so their children do too.

Each pre-order visit therefore keeps a monotonically rising counter (`len(records)`), and sorting records `(col, row, encounter, value)` produces the same column lists as the BFS version. The traversal itself trades the queue for the call stack, which costs memory on skewed trees but reads naturally in languages where recursion is the default shape:

1. Rebuild the tree exactly as in [BFS with Sorted Records](#bfs-with-sorted-records).
2. `visit(node, row, col)` appends `(col, row, len(records), node.val)`, then
   recurses left with `(row + 1, col - 1)` and right with `(row + 1, col + 1)`.
3. Sort the records and group them into columns as before.

#### Walkthrough

Example 2 again. The pre-order visit order differs from the BFS order (whole left subtree first), and the counters shift accordingly, yet the tie keeps its required order:

```text
visit 1 at (0, 0)    record ( 0, 0, 0, 1)
  visit 2 at (1, -1) record (-1, 1, 1, 2)
    visit 4 at (2, -2) record (-2, 2, 2, 4)
    visit 6 at (2, 0)  record ( 0, 2, 3, 6)
  visit 3 at (1, 1)  record ( 1, 1, 4, 3)
    visit 5 at (2, 0)  record ( 0, 2, 5, 5)
    visit 7 at (2, 2)  record ( 2, 2, 6, 7)
sort     (-2,2,2,4) (-1,1,1,2) (0,0,0,1) (0,2,3,6) (0,2,5,5) (1,1,4,3) (2,2,6,7)
group    col -2 [4]   col -1 [2]   col 0 [1, 6, 5]   col 1 [3]   col 2 [7]
```

The tie beat: node `6` holds encounter `3` here versus `4` under the BFS version, and node `5` holds `5` in both, but only the relative order inside one `(row, col)` group matters, and `3 < 5` keeps `6` before `5`. The grouped output is again `[[4],[2],[1,6,5],[3],[7]]`. Outside the tie the shifted counters are irrelevant: nodes `4` (encounter `2`) and `6` (encounter `3`) land in different columns, where the column key decides before the encounter is ever consulted.

#### Solution

The code swaps the coordinate queue for the recursive `visit`; rebuild, sort, and grouping are unchanged.

```python
from collections import deque
from typing import List, Optional, Tuple


class Solution:
    def verticalOrder(self, levelOrder: List[str]) -> List[List[int]]:
        if not levelOrder:
            return []

        root = TreeNode(int(levelOrder[0]))
        parents = deque([root])
        token_index = 1
        while parents and token_index < len(levelOrder):
            parent = parents.popleft()
            left_token = (levelOrder[token_index]
                          if token_index < len(levelOrder) else "null")
            right_token = (levelOrder[token_index + 1]
                           if token_index + 1 < len(levelOrder) else "null")
            token_index += 2
            if left_token != "null":
                parent.left = TreeNode(int(left_token))
                parents.append(parent.left)
            if right_token != "null":
                parent.right = TreeNode(int(right_token))
                parents.append(parent.right)

        records: List[Tuple[int, int, int, int]] = []

        def visit(node: Optional[TreeNode], row: int, col: int) -> None:
            if node is None:
                return
            records.append((col, row, len(records), node.val))
            visit(node.left, row + 1, col - 1)
            visit(node.right, row + 1, col + 1)

        visit(root, 0, 0)
        records.sort()
        columns: List[List[int]] = []
        for position, record in enumerate(records):
            new_column = position == 0 or record[0] != records[position - 1][0]
            if new_column:
                columns.append([])
            columns[-1].append(record[3])
        return columns
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The DFS visits each node once; the record sort still dominates.

##### Space Complexity: `O(n)`

The tree, records, and grouping lists hold one entry per node, plus a call stack that reaches `n` frames on a skewed tree.

#### Key Insights

- Within a single row, pre-order encounter order equals breadth-first order, so a DFS may feed the same `(col, row, encounter, value)` sort the BFS feeds it.
- The equivalence is row-local: pre-order does not reproduce BFS order across rows, which is harmless here because the row key in the tuple already dominates the encounter key.
- Recursion is the trade: no queue of pending nodes, but the interpreter's recursion limit becomes the real ceiling on skewed trees, the same hazard a queue removes.

### BFS with Column Buckets

#### Derivation

Both sorted-record versions pay `O(n log n)` for a sort whose outcome the traversal already knows. The BFS visits nodes row by row, left to right, so the first time a column is seen its entry is the topmost one, and every later append to that column arrives at a greater row or, on a tie, later in the encounter order. Appending values into a per-column bucket during the traversal therefore leaves every bucket sorted by row and then by encounter order with no comparison sort at all. The only remaining question is emission order of the buckets, and recording the smallest and largest column seen as the traversal runs turns that into a plain range walk:

1. Rebuild the tree as before.
2. BFS with `(node, col)` pairs, appending `node.val` to
   `columns.setdefault(col, [])` on each visit and widening `smallest_col` and
   `largest_col`.
3. Return `[columns[col] for col in range(smallest_col, largest_col + 1)]`.

#### Walkthrough

Example 2, with the bucket map shown after each visit:

```text
visit 1 col 0    smallest 0, largest 0    buckets: {0: [1]}
visit 2 col -1   smallest -1, largest 0   buckets: {-1: [2], 0: [1]}
visit 3 col 1    smallest -1, largest 1   buckets: {-1: [2], 0: [1], 1: [3]}
visit 4 col -2   smallest -2, largest 1   buckets: {-2: [4], -1: [2], 0: [1], 1: [3]}
visit 6 col 0    buckets: {-2: [4], -1: [2], 0: [1, 6], 1: [3]}
visit 5 col 0    buckets: {-2: [4], -1: [2], 0: [1, 6, 5], 1: [3]}
visit 7 col 2    smallest -2, largest 2   buckets: {-2: [4], -1: [2], 0: [1, 6, 5], 1: [3], 2: [7]}
emit     cols -2..2 -> [[4], [2], [1, 6, 5], [3], [7]]
```

The tie beat needs no key at all: the queue delivers `6` before `5` because their parents `2` and `3` were dequeued in that order, so the appends land in `bucket 0` as `[1, 6, 5]` directly. The emitted list matches the expected Output, and Example 1 emits `[[9],[3,15],[20],[7]]` the same way.

#### Solution

The code is the bucket-filling BFS with the range-walk emission; the rebuild block is shared with the earlier solutions.

```python
from collections import deque
from typing import Dict, List


class Solution:
    def verticalOrder(self, levelOrder: List[str]) -> List[List[int]]:
        if not levelOrder:
            return []

        root = TreeNode(int(levelOrder[0]))
        parents = deque([root])
        token_index = 1
        while parents and token_index < len(levelOrder):
            parent = parents.popleft()
            left_token = (levelOrder[token_index]
                          if token_index < len(levelOrder) else "null")
            right_token = (levelOrder[token_index + 1]
                           if token_index + 1 < len(levelOrder) else "null")
            token_index += 2
            if left_token != "null":
                parent.left = TreeNode(int(left_token))
                parents.append(parent.left)
            if right_token != "null":
                parent.right = TreeNode(int(right_token))
                parents.append(parent.right)

        columns: Dict[int, List[int]] = {}
        smallest_col = largest_col = 0
        queue = deque([(root, 0)])
        while queue:
            node, col = queue.popleft()
            columns.setdefault(col, []).append(node.val)
            smallest_col = min(smallest_col, col)
            largest_col = max(largest_col, col)
            if node.left:
                queue.append((node.left, col - 1))
            if node.right:
                queue.append((node.right, col + 1))

        return [columns[col] for col in range(smallest_col, largest_col + 1)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is rebuilt, visited, and appended once; the emission walks each column's bucket once, and no comparison sort runs.

##### Space Complexity: `O(n)`

The rebuilt tree and the buckets hold one entry per node, and the queue holds at most one wavefront.

#### Key Insights

- The BFS order is the column order: row-major, left-to-right traversal appends each value to its bucket already sorted by row and then by encounter order, which is exactly the statement's tie rule.
- Column indices are gap-free between the extremes: every child column is one away from its parent's, and the parent records its column before the child can record a wider one, so the range walk never misses a bucket.
- Sorting is optional whenever the traversal order already encodes the sort key; here the `O(n log n)` cost of the first two solutions buys nothing the queue did not already provide.

## Comparison of Solutions

### Time Complexity

- **BFS with Sorted Records**: `O(n log n)` - linear traversal plus a comparison sort over `n` records.
- **DFS with Pre-Order Records**: `O(n log n)` - linear traversal plus the same record sort.
- **BFS with Column Buckets**: `O(n)` - each node is appended to its bucket once and no sort runs.

### Space Complexity

- **BFS with Sorted Records**: `O(n)` - tree, queue, and record list.
- **DFS with Pre-Order Records**: `O(n)` - tree and records, plus a call stack up to `n` frames on a skewed tree.
- **BFS with Column Buckets**: `O(n)` - tree, buckets, and one traversal wavefront.

### Trade-offs

- The sorted-record versions state the whole ordering contract in one tuple and one `sort` call, which is short to write and easy to verify, at a logarithmic time cost.
- The DFS variant removes the traversal queue but reintroduces the recursion-depth hazard on skewed trees and leans on the row-local pre-order equivalence, an argument worth writing down before trusting.
- The bucket version is the fastest and needs the subtlest correctness argument: it relies on the traversal order itself, so nothing in the code shows the tie rule that makes it correct.

### When to Use Each

- **BFS with Sorted Records**: the interview opener: rebuild, record, sort, group is easy to state correctly under pressure, and `O(n log n)` usually passes.
- **DFS with Pre-Order Records**: when the rest of an interview solution is already recursive and the tree shape keeps depth moderate.
- **BFS with Column Buckets (Recommended)**: the answer to give for the stated `10^5` bound: linear time, no sort, and the tie rule handled by construction.

### Optimization Notes

- The explicit `encounter` key is technically redundant with a stable sort: Python's `sort` is stable, so `records.sort()` over `(col, row, value)` pairs would preserve insertion order on ties; keeping the key makes the tie rule visible in the code rather than in the language semantics.
- The rebuild loop can fuse with the coordinate pass by carrying `(row, col)` alongside each parent as children are created; the two-pass shape above is kept because it separates deserialization from the algorithm being taught.
- For repeated queries over one tree, the bucket version's `columns` dict can be kept and sorted keys cached once; the record versions would re-sort on every query.

