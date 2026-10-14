# [Count Uni-Valued Subtrees](https://www.fastprep.io/problems/amazon-count-univalued-subtrees)

**Medium** | **NN minutes** | **Tree, Depth First Search, Recursion**

Given the root of a binary tree, return the number of subtrees whose nodes all have the same value.

Every node defines one subtree consisting of that node and all of its descendants. A leaf is therefore always a uni-valued subtree.

## Examples

### Example 1

**Input:** `root = [5,1,5,5,5,null,5]`

**Output:** `4`

**Explanation:** The three leaf fives and the right subtree rooted at five are uni-valued.

### Example 2

**Input:** `root = [1]`

**Output:** `1`

**Explanation:** A leaf is uni-valued.

### Example 3

**Input:** `root = []`

**Output:** `0`

**Explanation:** An empty tree contains no subtree.

## Constraints

- `The tree contains between 0 and 500 nodes.`
- `-1000 ≤ Node.val ≤ 1000.`

## Solutions

The solutions below assume the standard node definition and `from typing import Dict, List, Optional`:

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

The most literal reading executes the problem's own sentence: for every node of the tree, ask whether all nodes in the subtree rooted there share that node's value, and count it when they do. Two independent duties, two independent helpers: one walk that tests a candidate subtree against a fixed value, and one walk that offers every node as a candidate root. The subtree test is the simpler of the two, because "every node equals `value`" decomposes per node: the candidate node itself must equal `value`, and so must everything below it:

1. `is_univalued(node, value)` returns `True` for `None`, and otherwise requires
   `node.val == value` plus the same test on both children with the same
   `value`.
2. `visit(node)` walks the whole tree; at every node it runs
   `is_univalued(node, node.val)` and increments `unival_count` on `True`.
3. A leaf always passes the test (it has no children to disagree), which is
   exactly the statement's guarantee that every leaf is a uni-valued subtree.
4. Return `unival_count`.

#### Walkthrough

Example 1, `root = [5,1,5,5,5,null,5]`, shows a passing leaf, a failing interior node, and the passing right subtree in one trace:

```text
        5
       / \
      1   5
     / \    \
    5   5    5
```

```text
visit 5 (root)   is_univalued(root, 5): left subtree holds 1 -> False, no count
visit 1          is_univalued(1-node, 1): child holds 5 -> False, no count
visit 5 (leaf)   leaf, no children -> True, unival_count = 1
visit 5 (leaf)   leaf, no children -> True, unival_count = 2
visit 5 (right)  is_univalued: node 5 == 5, right child 5 == 5 -> True,
                 unival_count = 3
visit 5 (leaf)   leaf, no children -> True, unival_count = 4
```

The count reaches `4`: the three leaf fives and the subtree rooted at the right-hand five, matching the expected Output for Example 1. On Example 2 the single node `1` is a leaf and passes, returning `1`; on Example 3 the `visit` call returns immediately from a `None` root with `unival_count = 0`.

#### Solution

The code is the walkthrough's two helpers: the value test and the candidate loop.

```python
from typing import Optional


class Solution:
    def countUnivalSubtrees(self, root: Optional[TreeNode]) -> int:
        """Count the subtrees whose nodes all share one value.

        Time:  O(n^2): each of the n nodes starts a test that may scan its
            entire subtree.
        Space: O(h) recursion stack, h the tree height.
        """
        def is_univalued(node: Optional[TreeNode], value: int) -> bool:
            if node is None:
                return True
            return (
                node.val == value
                and is_univalued(node.left, value)
                and is_univalued(node.right, value)
            )

        unival_count = 0

        def visit(node: Optional[TreeNode]) -> None:
            nonlocal unival_count
            if node is None:
                return
            if is_univalued(node, node.val):
                unival_count += 1
            visit(node.left)
            visit(node.right)

        visit(root)
        return unival_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` nodes starts an `is_univalued` test that may scan every node of its subtree; a degenerate chain pays `1 + 2 + ... + n`.

##### Space Complexity: `O(h)`

The recursion stack of the candidate walk stacks on top of the test's stack, both bounded by the tree height.

#### Key Insights

- Testing a subtree "against `node.val`" rather than collecting the subtree's distinct values keeps the test allocation-free.
- The approach re-answers the same question for every descendant: a node's test re-verifies nodes its parent already verified, which is precisely the waste the single-pass version removes.
- Every leaf passes, so the count starts at the leaf total and can only grow as interiors qualify.

### Single-Pass Postorder

#### Derivation

The brute force re-tests whole subtrees from scratch at every level. The repair is the standard bottom-up contract: let the recursion answer for the children first, and let each node combine the two child reports instead of re-scanning. A subtree rooted at `node` is uni-valued exactly when both children's subtrees are uni-valued *and* each present child's root value equals `node.val`; one comparison per edge replaces the full re-scan. The recursion returns whether the subtree at `node` is uni-valued and counts qualifying nodes as a side effect. The `None` base case returns `True` (an empty tree satisfies any equality vacuously), which lets the parent treat a missing child as an agreeing one:

1. `report(node)` returns `True` for `None`.
2. Recurse first: collect `left_report` from the left child and `right_report`
   from the right child.
3. The node qualifies when `left_report` holds (or the left child is absent)
   with `node.left.val == node.val`, and the same on the right.
4. Increment `unival_count` when the node qualifies, and return the verdict so
   the parent can use it.

#### Walkthrough

Trace the reports on Example 1, `root = [5,1,5,5,5,null,5]`, with the recursion descending fully before any verdict forms:

```text
report(leaf 5, left of 1)      both children absent -> True    count = 1
report(leaf 5, right of 1)     both children absent -> True    count = 2
report(1)   left True but 5 != 1, right True but 5 != 1 -> False
report(leaf 5, right of right-5)  both children absent -> True count = 3
report(right 5)  left absent (True) and right True with 5 == 5 -> True
                                                            count = 4
report(root 5)  left False -> False, no count
```

Each line's verdict is computed from the two verdicts above it, never from a re-scan: node `1` fails on a single value comparison against each child, and the right-hand five qualifies on the strength of its child's report. The count finishes at `4`, matching the expected Output for Example 1. On Example 2 the lone node's two absent children report `True`, so the root qualifies and the function returns `1`; on Example 3 `report(None)` returns `True` without ever incrementing, and the function returns `0`.

#### Solution

The code is the walkthrough's report: children first, one comparison per edge, count on the way up.

```python
from typing import Optional


class Solution:
    def countUnivalSubtrees(self, root: Optional[TreeNode]) -> int:
        """Count the subtrees whose nodes all share one value.

        Time:  O(n): each node is visited once and combines its children's
            reports with two comparisons.
        Space: O(h) recursion stack, h the tree height.
        """
        unival_count = 0

        def report(node: Optional[TreeNode]) -> bool:
            nonlocal unival_count
            if node is None:
                return True
            left_report = report(node.left)
            right_report = report(node.right)
            left_agrees = node.left is None or (
                left_report and node.left.val == node.val
            )
            right_agrees = node.right is None or (
                right_report and node.right.val == node.val
            )
            if left_agrees and right_agrees:
                unival_count += 1
            return left_agrees and right_agrees

        report(root)
        return unival_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is visited exactly once, and each visit performs a constant number of comparisons against its children's reports.

##### Space Complexity: `O(h)`

The recursion stack holds one frame per level, `h` the tree height; no other structure grows with the input.

#### Key Insights

- The `None -> True` base case is what lets the parent write one uniform test per side instead of branching on child presence.
- The verdict a node returns must reflect its whole subtree, not just its own value: a univalued parent requires univalued children, which is why `left_report` appears inside `left_agrees`.
- This bottom-up report pattern is the tree analogue of a DP table filled from the leaves: the answer for a node is a function of the answers for its children.

### Iterative Postorder with Explicit Stack

#### Derivation

The single-pass version inherits the interpreter's recursion limit: a degenerate 500-node chain is 500 frames deep, uncomfortably close to Python's default limit of 1,000, and a non-Amazon variant without the node cap could exceed it. The call stack contributes nothing but an ordering guarantee, children before parent, so an explicit [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) can produce the same postorder sequence, and the combine step then runs as a plain loop over that sequence. Splitting the work into two phases keeps each phase simple: one pass collects nodes in postorder, one pass combines:

1. Seed `stack` with `(root, False)`, where the flag records whether the node's
   children still need to be stacked.
2. Pop a frame. Skip `None`; when the flag is `False`, re-push the node marked
   `True`, then push its right child and left child, so the left subtree is
   expanded and emitted first.
3. When the flag is `True`, append the node to `postorder`: children are now
   guaranteed to appear earlier in the list.
4. Sweep `postorder` in order, deciding `subtree_univalued[node]` from the
   already-recorded verdicts of its children, counting qualifiers, and storing
   each verdict for the parent to read.

#### Walkthrough

Trace both phases on Example 1, `root = [5,1,5,5,5,null,5]`, writing `5a` and `5b` for the two leaf fives under node `1`, and `5r` and `5rr` for the right-hand five and its right child. The expansion phase pushes the right child first and the left child last, so the left subtree pops and emits before the right:

```text
stack phase (pop order):
pop (root 5, False)  push (5,True), (5r,False), (1,False)
pop (1,False)        push (1,True), (5b,False), (5a,False)
pop (5a,False)       push (5a,True); its two None children pop and skip
pop (5a,True)        postorder [5a]
pop (5b,False)       push (5b,True); its two None children pop and skip
pop (5b,True)        postorder [5a, 5b]
pop (1,True)         postorder [5a, 5b, 1]
pop (5r,False)       push (5r,True), (5rr,False), (None)
pop (None)           skip
pop (5rr,False)      push (5rr,True); its two None children pop and skip
pop (5rr,True)       postorder [5a, 5b, 1, 5rr]
pop (5r,True)        postorder [5a, 5b, 1, 5rr, 5r]
pop (5,True)         postorder [5a, 5b, 1, 5rr, 5r, root 5]
```

The combine sweep then reads each node's children, whose verdicts the sweep recorded earlier in the list:

```text
5a   leaf: both children absent -> True      count = 1
5b   leaf: both children absent -> True      count = 2
1    children 5a, 5b True but 5 != 1 -> False
5rr  leaf: both children absent -> True      count = 3
5r   left absent (True), right child 5rr True and 5 == 5 -> True  count = 4
root left child 1 False -> False
```

The sweep counts the same four subtrees as the recursion, so the function returns `4`, matching the expected Output for Example 1. Example 2's single node is pushed, emitted, and qualifies in the sweep for `1`; on Example 3 the stack empties without emitting anything and the function returns `0`.

#### Solution

The code is the two phases: the flag-marked stack that emits postorder, then the combine sweep.

```python
from typing import Dict, List, Optional, Tuple


class Solution:
    def countUnivalSubtrees(self, root: Optional[TreeNode]) -> int:
        """Count the subtrees whose nodes all share one value.

        Time:  O(n): the stack phase emits each node once and the combine
            sweep reads each node once.
        Space: O(n) for the postorder list and verdict map, with the stack
            bounded by O(h).
        """
        postorder: List[TreeNode] = []
        stack: List[Tuple[Optional[TreeNode], bool]] = [(root, False)]
        while stack:
            node, children_stacked = stack.pop()
            if node is None:
                continue
            if children_stacked:
                postorder.append(node)
            else:
                stack.append((node, True))
                stack.append((node.right, False))
                stack.append((node.left, False))

        unival_count = 0
        subtree_univalued: Dict[TreeNode, bool] = {}
        for node in postorder:
            left_univalued = node.left is None or (
                subtree_univalued[node.left] and node.left.val == node.val
            )
            right_univalued = node.right is None or (
                subtree_univalued[node.right] and node.right.val == node.val
            )
            subtree_univalued[node] = left_univalued and right_univalued
            if subtree_univalued[node]:
                unival_count += 1
        return unival_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The stack phase pushes each node a constant number of times (once unexpanded, once expanded), and the combine sweep processes each node once.

##### Space Complexity: `O(n)`

The postorder list and the verdict map each hold every node; the explicit stack itself stays within `O(h)`.

#### Key Insights

- The `(node, children_stacked)` frame is the recursion's return address made visible: re-pushing the node marked `True` is exactly the "resume after the children" moment of a postorder call.
- Children land on the stack after the parent's re-push, so they pop first and are emitted first, which is what makes the combine sweep safe to run left-to-right over `postorder`.
- The verdict map replaces the recursion's return value; the trade for removing the recursion limit is `O(n)` extra space for the emitted list and the map.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - every node starts a test that may scan its entire subtree.
- **Single-Pass Postorder**: `O(n)` - one visit per node with constant work per visit.
- **Iterative Postorder with Explicit Stack**: `O(n)` - one emission per node plus one combine pass.

### Space Complexity

- **Brute Force**: `O(h)` - recursion stacks for the walk and the subtree test.
- **Single-Pass Postorder**: `O(h)` - recursion stack only.
- **Iterative Postorder with Explicit Stack**: `O(n)` - the postorder list and verdict map, with the stack at `O(h)`.

### Trade-offs

- **Brute Force**: the problem statement in code with no bookkeeping beyond two helpers, but it re-verifies descendants its ancestors already verified.
- **Single-Pass Postorder**: optimal time and minimal memory; the cost is trusting the bottom-up report contract instead of a direct reading of the sentence.
- **Iterative Postorder with Explicit Stack**: immune to recursion limits, at the cost of two-phase plumbing and a verdict map.

### When to Use Each

- **Brute Force**: as the spoken baseline in an interview, to state the naive contract before collapsing it.
- **Single-Pass Postorder** (Recommended): the interview default: optimal, short, and it demonstrates the bottom-up report pattern.
- **Iterative Postorder with Explicit Stack**: when tree depth can approach the interpreter's recursion limit; with this problem's 500-node cap it is optional.

### Optimization Notes

- The single comparison per edge is the entire improvement over the brute force: a child's report certifies its whole subtree, so the parent never looks below the child's root.
- Reject the tempting alternative of collecting each subtree's value set: a set per node costs `O(n)` per merge and `O(n^2)` overall, worse than both solutions here.
- The `None -> True` convention does the heavy lifting in every version: it makes leaves qualify without special-casing and lets absent children count as agreeing.
