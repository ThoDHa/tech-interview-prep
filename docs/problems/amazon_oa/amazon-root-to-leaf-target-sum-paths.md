# [Root-to-Leaf Paths with a Target Sum](https://www.fastprep.io/problems/amazon-root-to-leaf-target-sum-paths)

**Medium** | **NN minutes** | **Tree, Depth First Search, Backtracking**

Given the root of a binary tree and an integer targetSum, return every root-to-leaf path whose node values add up to targetSum.

A leaf has no children. Return paths in left-to-right depth-first order, with each path listed from the root to its leaf.

## Examples

### Example 1

**Input:** `root = [5,4,8,11,null,13,4,7,2,null,null,5,1]`, `targetSum = 22`

**Output:** `[[5,4,11,2],[5,8,4,5]]`

**Explanation:** Both listed root-to-leaf paths sum to 22, and the left path is visited first.

### Example 2

**Input:** `root = [1,2,3]`, `targetSum = 5`

**Output:** `[]`

**Explanation:** Neither root-to-leaf path sums to 5.

### Example 3

**Input:** `root = []`, `targetSum = 0`

**Output:** `[]`

**Explanation:** An empty tree has no root-to-leaf path.

## Constraints

- `The tree contains between 0 and 500 nodes.`
- `-1000 ≤ Node.val ≤ 1000.`
- `-10^9 ≤ targetSum ≤ 10^9.`

## Solutions

The solutions below assume the standard node definition and `from typing import Iterator, List, Optional, Tuple`:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Copy-per-Node Recursion

#### Derivation

The most literal reading of the problem executes its own sentence: a path is a root-to-leaf chain whose values sum to `targetSum`, so walk every root-to-leaf chain and sum as you go. Each node contributes its value and hands its children a smaller target, the running total already spent. The literal version also builds each path the way the sentence reads it, from the root: a node receives the lists collected below it and prepends its own value to each:

1. A `None` node contributes no paths.
2. A leaf matches when its value equals the remaining target, and contributes exactly one single-value path.
3. An interior node subtracts its value from the target, collects the matching paths from each child, and prepends its own value to every one of them.
4. The root's collection is the answer, already in left-to-right depth-first order.

#### Walkthrough

Example 2, `root = [1,2,3]`, `targetSum = 5`, shows both the list building and the miss:

```text
node 1, remaining 5     interior: ask both children with remaining 5 - 1 = 4
  node 2, remaining 4   leaf: 2 != 4 -> no match, contributes []
  node 3, remaining 4   leaf: 3 != 4 -> no match, contributes []
node 1 prepends 1 to [] + [] -> []
```

Neither leaf's value equals the remaining `4`, so both children contribute empty lists and the function returns `[]`, matching the expected Output. Example 3, a `None` root, returns `[]` at the first step.

#### Solution

The code is the walkthrough's two leaf rules and the prepend:

```python
from typing import List, Optional


class Solution:
    def pathSum(self, root: Optional[TreeNode], target_sum: int) -> List[List[int]]:
        """Return every root-to-leaf path summing to target_sum.

        Time:  O(n) node visits plus, for each matching path, one list copy
            at every ancestor: O(sum of leaf depths) total, O(n^2) worst case.
        Space: O(h) recursion stack plus the returned lists.
        """
        if root is None:
            return []
        if root.left is None and root.right is None:
            if root.val == target_sum:
                return [[root.val]]
            return []

        remaining = target_sum - root.val
        matching: List[List[int]] = []
        for child in (root.left, root.right):
            if child is not None:
                for child_path in self.pathSum(child, remaining):
                    matching.append([root.val] + child_path)
        return matching
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(sum of leaf depths)`, `O(n^2)` worst case

Every node is visited once, but each matching path is rebuilt once per ancestor: a path of length `h` is copied `h` times in growing prefixes.

##### Space Complexity: `O(h)` auxiliary plus the output

The recursion stack holds one frame per level; the intermediate and returned lists hold the paths themselves.

#### Key Insights

- The recursion mirrors the sentence structure, which makes it easy to derive and easy to trust, and it produces left-to-right order for free.
- Prepending at every ancestor is the hidden cost: the same path fragments are copied over and over on the way up.
- Negative node values mean the running total can dip below zero and come back, so pruning on `remaining < 0` would be wrong.

### Backtracking with a Shared Path

#### Derivation

The copy-per-node version pays repeatedly for fragments it already holds. The fix is to carry one shared `path` list down the recursion and treat it as a stack of the current route: append a value when entering a node, pop it when leaving. Nothing is copied on the way down; the only copy happens once, at a leaf, when a complete matching path is recorded into the result. The running total becomes a plain integer `remaining` threaded through the calls:

1. Maintain `path`, the node values on the current root-to-node route, and `remaining`, `target_sum` minus their sum.
2. On entering a node, append its value and subtract it from `remaining`.
3. At a leaf, record `path.copy()` into `matching` when `remaining` hits `0`; the copy is the single moment a path is materialized.
4. On leaving a node, pop `path` so the sibling branch sees the correct route.
5. Left-to-right order falls out of recursing into the left child before the right.

#### Walkthrough

Example 1, `root = [5,4,8,11,null,13,4,7,2,null,null,5,1]`, `targetSum = 22`, drawn from Example 1's own numbers:

```text
        5
       / \
      4   8
     /   / \
    11  13  4
   /  \    / \
  7    2  5   1
```

Each line is one visit, listing `path` and `remaining` after the append and subtract; leaves show the verdict:

```text
visit 5    path=[5]          remaining=17
visit 4    path=[5,4]        remaining=13
visit 11   path=[5,4,11]     remaining=2
visit 7    path=[5,4,11,7]   remaining=-5   leaf, no match -> pop 7
visit 2    path=[5,4,11,2]   remaining=0    leaf, MATCH -> record copy, pop 2
                             (pop 11, pop 4)
visit 8    path=[5,8]        remaining=9
visit 13   path=[5,8,13]     remaining=-4   leaf, no match -> pop 13
visit 4    path=[5,8,4]      remaining=5
visit 5    path=[5,8,4,5]    remaining=0    leaf, MATCH -> record copy, pop 5
visit 1    path=[5,8,4,1]    remaining=4    leaf, no match -> pop 1
```

The two recorded copies are `[5, 4, 11, 2]` and `[5, 8, 4, 5]`, in that order, matching the expected Output `[[5,4,11,2],[5,8,4,5]]`. The visits at `7` and `13` also show why negative sums must not be pruned: `remaining = -5` at node `7` is a dead end here, but a deeper negative child could have brought it back to `0`.

#### Solution

The code is the walkthrough's append, test, and pop discipline:

```python
from typing import List, Optional


class Solution:
    def pathSum(self, root: Optional[TreeNode], target_sum: int) -> List[List[int]]:
        """Return every root-to-leaf path summing to target_sum.

        Time:  O(n + matches * h): every node is visited once, and each
            matching path is copied exactly once at its leaf.
        Space: O(h) for the shared path and recursion stack, plus the
            returned lists.
        """
        matching: List[List[int]] = []
        path: List[int] = []

        def dfs(node: Optional[TreeNode], remaining: int) -> None:
            if node is None:
                return
            path.append(node.val)
            remaining -= node.val
            if node.left is None and node.right is None:
                if remaining == 0:
                    matching.append(path.copy())
            else:
                dfs(node.left, remaining)
                dfs(node.right, remaining)
            path.pop()

        dfs(root, target_sum)
        return matching
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + matches × h)`

Every node is appended and popped exactly once; the only path copying is one `O(h)` copy per matching path at its leaf.

##### Space Complexity: `O(h)` auxiliary plus the output

The shared `path` list and the recursion stack each hold at most one entry per level; `matching` holds the answer itself.

#### Key Insights

- Backtracking turns the path from data rebuilt at every node into state maintained by two `O(1)` operations, append and pop.
- The single copy at the leaf is the entire space cost of recording an answer, so the traversal overhead drops from once-per-ancestor to once-per-answer.
- The leaf check must come before the child recursions here: a leaf's `None` children would otherwise append nothing and the match test would run twice with the same state.

### Iterative DFS with an Explicit Stack

#### Derivation

The backtracking version is optimal, but its memory is still the call stack. With at most 500 nodes the interpreter's recursion limit never bites, yet the same traversal is worth knowing in loop form for deeper trees, and the rewrite is mechanical: the call stack becomes an explicit list of frames, each holding a node, a remaining target, and an iterator over that node's children. The shared `path` list survives the translation, appended when a frame is pushed and popped when it is retired:

1. Push a frame for the root with `path = [root.val]`, `remaining = target_sum - root.val`, and a leaf flag (true when the node has no children).
2. Each loop round asks the top frame's child iterator for its next child.
3. A `None` child means the frame is exhausted: retire it, popping `path`. The frame records `path.copy()` only if it is a leaf frame with `remaining` equal to `0`; an interior node also exhausts its iterator, so leafness must be tested, not inferred from exhaustion.
4. A real child is pushed as a new frame, appending its value to `path`, subtracting it from `remaining`, and carrying its own leaf flag.
5. Children are yielded left before right, so paths still come out in left-to-right depth-first order.

#### Walkthrough

The same Example 1 tree, condensed to stack events; each push appends to `path`, each retire pops it. `rem` is the frame's remaining target and `leaf` the flag stored at push time:

```text
push 5  path=[5]           rem=17   leaf=no
push 4  path=[5,4]         rem=13   leaf=no
push 11 path=[5,4,11]      rem=2    leaf=no
push 7  path=[5,4,11,7]    rem=-5   leaf=yes
retire 7  leaf, rem!=0 -> no record, pop    path=[5,4,11]
push 2  path=[5,4,11,2]    rem=0    leaf=yes
retire 2  leaf, rem==0 -> record [5,4,11,2] path=[5,4,11]
retire 11 exhausted, not a leaf -> pop     path=[5,4]
retire 4  exhausted, not a leaf -> pop     path=[5]
push 8  path=[5,8]         rem=9    leaf=no
push 13 path=[5,8,13]      rem=-4   leaf=yes
retire 13 leaf, rem!=0 -> no record, pop   path=[5,8]
push 4  path=[5,8,4]       rem=5    leaf=no
push 5  path=[5,8,4,5]     rem=0    leaf=yes
retire 5  leaf, rem==0 -> record [5,8,4,5]  path=[5,8,4]
push 1  path=[5,8,4,1]     rem=4    leaf=yes
retire 1  leaf, rem!=0 -> no record, pop   path=[5,8,4]
retire 4, retire 8, retire 5 exhausted, not leaves -> pops
```

The records appear in the same order as the backtracking version: `[5, 4, 11, 2]` then `[5, 8, 4, 5]`, the expected Output.

#### Solution

The code is the walkthrough's push, ask-iterator, retire loop:

```python
from typing import Iterator, List, Optional, Tuple


class Solution:
    def pathSum(self, root: Optional[TreeNode], target_sum: int) -> List[List[int]]:
        """Return every root-to-leaf path summing to target_sum.

        Time:  O(n + matches * h): each node is pushed once, each child
            iterator is consumed once, and each match copies one path.
        Space: O(h) for the explicit stack and shared path, plus the
            returned lists.
        """
        matching: List[List[int]] = []
        if root is None:
            return matching

        def is_leaf(node: TreeNode) -> bool:
            return node.left is None and node.right is None

        path: List[int] = [root.val]
        stack: List[Tuple[TreeNode, Iterator[Optional[TreeNode]], int, bool]] = [
            (root, iter((root.left, root.right)), target_sum - root.val, is_leaf(root))
        ]
        while stack:
            node, children, remaining, leaf = stack[-1]
            child = next(children, None)
            if child is None:
                if leaf and remaining == 0:
                    matching.append(path.copy())
                stack.pop()
                path.pop()
            else:
                path.append(child.val)
                stack.append(
                    (
                        child,
                        iter((child.left, child.right)),
                        remaining - child.val,
                        is_leaf(child),
                    )
                )
        return matching
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + matches × h)`

Every node is pushed exactly once and every child-pair iterator is consumed exactly once; the per-match cost is the single leaf copy.

##### Space Complexity: `O(h)` auxiliary plus the output

The explicit stack and the shared `path` list each hold at most one entry per tree level.

#### Key Insights

- The `(node, child_iterator, remaining, leaf)` frame is the call stack made visible: suspending and resuming a node's work is exactly what an iterator models.
- Exhausting a child iterator means the node's work is done, not that the node is a leaf; every interior node exhausts too, so leafness is decided once at push time and carried in the frame.
- The same `path` append-and-pop discipline as the recursive version keeps the memory profile flat, so the rewrite changes no asymptotics, only who owns the stack.

## Comparison of Solutions

### Time Complexity

- **Copy-per-Node Recursion**: `O(sum of leaf depths)` rebuild work over `O(n)` visits, `O(n^2)` worst case: each matching path is copied once per ancestor.
- **Backtracking with a Shared Path**: `O(n + matches × h)`: one visit per node plus one copy per matching path.
- **Iterative DFS with an Explicit Stack**: `O(n + matches × h)`, the same work with the stack owned explicitly.

### Space Complexity

- **Copy-per-Node Recursion**: `O(h)` recursion stack plus the intermediate fragment lists on the way up.
- **Backtracking with a Shared Path**: `O(h)` for the shared path and recursion stack, plus the returned lists.
- **Iterative DFS with an Explicit Stack**: `O(h)` for the explicit stack and shared path, plus the returned lists.

### Trade-offs

- **Copy-per-Node Recursion**: the derivation reads directly off the problem statement and needs no bookkeeping, but it pays for the same fragments again at every ancestor.
- **Backtracking with a Shared Path**: optimal visits-to-copies ratio and the canonical backtracking pattern, but the append/pop pairing must stay balanced or sibling branches see corrupted routes.
- **Iterative DFS with an Explicit Stack**: immune to recursion limits on pathological depths, at the cost of frame plumbing that is harder to read.

### When to Use Each

- **Backtracking with a Shared Path (Recommended)**: the interview default: optimal, idiomatic, and it demonstrates the append/pop invariant explicitly.
- **Copy-per-Node Recursion**: as a first spoken step in an interview, to state the naive contract before optimizing it.
- **Iterative DFS with an Explicit Stack**: when tree depth can approach the interpreter's recursion limit; with this problem's 500-node cap it is optional.

### Optimization Notes

- Negative node values forbid the tempting `remaining < 0` prune; only the leaf check is sound.
- The single `path.copy()` per match is the difference between paying once per answer and once per ancestor; there is no way to avoid it, since each recorded path must be its own list.
- The iterative variant's child iterators preserve left-before-right order without sorting or reversing anything, so the output order contract is inherited rather than enforced.
