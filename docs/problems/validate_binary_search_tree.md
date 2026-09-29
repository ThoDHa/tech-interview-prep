# [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/)

**Medium** | **30 minutes** | **Tree, Depth-First Search, Binary Search Tree, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) · [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal)

**Practice:** [`practice/validate_binary_search_tree/solution.py`](../../practice/validate_binary_search_tree/solution.py)

Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).

A **valid BST** is defined as follows:

- The left subtree of a node contains only nodes with keys **less than** the node's key.
- The right subtree of a node contains only nodes with keys **greater than** the node's key.
- Both the left and right subtrees must also be binary search trees.

## Examples

### Example 1

![BST](assets/validate_binary_search_tree_example1.jpg)

**Input:** `root = [2,1,3]`

**Output:** `true`

### Example 2

![Invalid BST](assets/validate_binary_search_tree_example2.jpg)

**Input:** `root = [5,1,4,null,null,3,6]`

**Output:** `false`

**Explanation:** The root node's value is 5 but its right child's value is 4.

## Constraints

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

## Deriving the Solution

The BST definition constrains every node against all of its ancestors, not just its parent: "the left subtree contains only smaller keys" reaches down to the deepest descendant. Every solution below is a different way of enforcing that global constraint; they differ in how much work each node repeats.

1. **Start literal.** Apply the definition word for word: at every node, scan
   its entire left subtree for values below `node.val`, scan its entire right subtree for values above it, then recurse into both children. Correct, but each descendant is rescanned once per ancestor, `O(n^2)` on a skewed tree: see [Brute Force](#brute-force).
2. **Spot the waste.** By the time the traversal reaches a node, its ancestors
   have already dictated everything it must satisfy: stay above the last ancestor it descended right from, stay below the last ancestor it descended left from. Two numbers summarize every ancestor constraint, so the repeated subtree scans re-derive information the path down already carried.
3. **Carry the bounds down.** Pass an open interval `(low, high)` into each
   recursive call, tightening one side per descent, and check each node once against its interval. One `O(n)` pass: see [Recursive Bounds](#recursive-bounds).
4. **Use the sorted-order property.** An inorder traversal of a valid BST
   visits values in strictly increasing order, and the converse holds too. Checking that each visited value exceeds the previous one validates the tree in one pass while tracking a single number: see [Inorder Traversal](#inorder-traversal).

## Solutions

### Brute Force

#### Derivation

The [BST definition](https://en.wikipedia.org/wiki/Binary_search_tree) reads almost like an algorithm: every value in a node's left subtree is strictly smaller, every value in its right subtree is strictly larger, and both subtrees are themselves BSTs. The most direct implementation simply enforces that definition word for word at every node, scanning the full subtrees each time:

1. For each node, scan its entire left subtree and confirm every value is strictly less than `node.val`.
2. Scan its entire right subtree and confirm every value is strictly greater than `node.val`.
3. Recurse into both children, applying the same full check at each.
4. An empty subtree is trivially valid.

This rescans descendants repeatedly, but it needs no insight beyond restating the definition, which makes it the natural first attempt.

#### Walkthrough

Trace the Brute Force solution on Example 1: `root = [2,1,3]`, the tree with `2` at the root, `1` as its left child, and `3` as its right child. The expected output is `true`.

The outer call is `valid(2)`. It runs two subtree scans, then recurses into its children:

- `valid(2)`: node `2` is not empty, so apply the BST definition here.
  - `all_less(node.left=1, limit=2)`: scan the left subtree, every value must be strictly below `2`. Node `1` has no children, so it checks `1 < 2`, which is `True`. The scan returns `True`.
  - `all_greater(node.right=3, limit=2)`: scan the right subtree, every value must be strictly above `2`. Node `3` has no children, so it checks `3 > 2`, which is `True`. The scan returns `True`.
  - Neither check failed, so recurse into both children:
    - `valid(node.left=1)`: node `1` has no children, so both subtree scans run on empty subtrees and return `True` immediately. With no children to recurse into, this returns `True`.
    - `valid(node.right=3)`: node `3` likewise has no children, so it returns `True`.
  - Both recursive calls returned `True`, so `valid(2)` returns `True`.

The order of calls, with each node's checks and what it returns:

| Call | Subtree checks | Returns |
| --- | --- | --- |
| `valid(2)` | `all_less(1, 2)` is `True`, `all_greater(3, 2)` is `True` | `True` (after children) |
| `valid(1)` | both scans on empty subtrees, `True` | `True` |
| `valid(3)` | both scans on empty subtrees, `True` | `True` |

The top-level `valid(root)` returns `True`, which matches the example's expected Output of `true`.

#### Solution

The code is the walkthrough's three helpers written down: the two subtree scans and the recursive `valid` that applies them at every node.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def all_less(node: Optional[TreeNode], limit: int) -> bool:
            # Every value in this subtree must be strictly below limit
            if not node:
                return True
            return (node.val < limit and
                    all_less(node.left, limit) and
                    all_less(node.right, limit))

        def all_greater(node: Optional[TreeNode], limit: int) -> bool:
            # Every value in this subtree must be strictly above limit
            if not node:
                return True
            return (node.val > limit and
                    all_greater(node.left, limit) and
                    all_greater(node.right, limit))

        def valid(node: Optional[TreeNode]) -> bool:
            if not node:
                return True
            # Apply the BST definition literally at this node
            if not all_less(node.left, node.val):
                return False
            if not all_greater(node.right, node.val):
                return False
            return valid(node.left) and valid(node.right)

        return valid(root)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each node triggers a full scan of its subtrees, and in a skewed tree those scans cover up to `O(n)` nodes per call across `O(n)` nodes, giving quadratic work in the worst case.

##### Space Complexity: `O(h)`

The recursion stack reaches the tree's height `h`: `O(log n)` for a balanced tree and `O(n)` for a skewed one. The subtree scans add no extra storage beyond their own stack frames.

#### Key Insights

- Translates the BST definition directly, so it is the easiest version to derive and trust.
- The strict `<` and `>` comparisons reject duplicate values, as the definition requires.
- It re-examines the same descendants once per ancestor, which is the redundancy the bounds and inorder approaches eliminate.

### Recursive Bounds

#### Derivation

The Brute Force rescans every descendant once per ancestor: `all_less` and `all_greater` re-derive, at each node, facts the path down has already passed through. The tempting shortcut, comparing a node only against its two immediate children, checks too little: a value can satisfy its parent yet still violate an ancestor higher up. The right compression sits in between. By the time the recursion reaches a node, everything its ancestors demand collapses into two numbers: the largest value it must stay above (`low`) and the smallest it must stay below (`high`). Checking each node once against that `(low, high)` interval, and tightening one side per descent, enforces the full definition in a single pass:

1. Start at the root with the widest possible bounds, `(-inf, +inf)`.
2. For each node, verify `low < node.val < high` using a strict comparison so duplicates are rejected.
3. [Recurse](https://en.wikipedia.org/wiki/Depth-first_search) left, tightening the upper bound to the current node's value: everything in the left subtree must be smaller.
4. Recurse right, tightening the lower bound to the current node's value: everything in the right subtree must be larger.
5. An empty subtree is trivially valid.

Passing the bounds downward propagates every ancestor's constraint to the deepest descendants, which is exactly what the BST definition demands. The Invariant below states that property formally: `low < v < high` holds for every value `v` in the subtree, not merely for the node being checked.

#### Invariant

Each call carries an open interval and guarantees it for the whole subtree, not just for the node at hand:

$$ \forall\, v \in \text{subtree}(\textit{node}):\quad \textit{low} < v < \textit{high} $$

```text
for all v in subtree(node):  low < v < high
    root call: low = -infinity, high = +infinity
```

Here `low` is the largest ancestor value the subtree must stay above and `high` the smallest it must stay below, so the interval is the intersection of every constraint the ancestors impose. The root starts at \((-\infty,\ +\infty)\), which constrains nothing.

Both recursive calls preserve it. Descending left, every value below `node` must also be smaller than `node.val`, so the upper bound tightens while `low` is inherited unchanged; descending right is the mirror image:

$$ (\textit{low},\ \textit{node.val}) \quad\text{left},\qquad (\textit{node.val},\ \textit{high}) \quad\text{right} $$

```text
left  child inherits (low,      node.val)
right child inherits (node.val, high)
```

Passing the node's own value as the *other* side's bound is what carries a constraint past the immediate child: a bound is never dropped on the way down, only intersected with tighter ones. The comparison `low < node.val < high` is strict, so equal values fail as the definition requires.

This is precisely what defeats the common wrong answer of comparing a node only against its two children, which asserts one edge at a time and says nothing about a grandchild. Take `[5,1,6,null,null,3,7]`: node `3` is the left child of `6` and `3 < 6` passes the child-only test, yet `3` sits in the root's right subtree and must exceed `5`. The bounds version reaches that call with `low = 5` inherited from the root, so `5 < 3` fails and the tree is correctly rejected.

#### Walkthrough

Example 2 fails at the root's own right child (`5 < 4 < +inf` is false on the very first check below the root), a violation even the flawed child-only comparison would catch. The mechanism worth seeing is a bound carried past the immediate parent, so we trace the tailored tree from the Invariant discussion instead: `root = [5,1,6,null,null,3,7]`, built so the violation sits at a grandchild:

```text
        5
       / \
      1   6
         / \
        3   7
```

Each call checks its node against its inherited `(low, high)` interval, then descends with one side tightened:

```text
validate(5, -inf, +inf)    -inf < 5 < +inf   ok; children get (-inf, 5) and (5, +inf)
  validate(1, -inf, 5)     -inf < 1 < 5      ok; leaf
    validate(None, -inf, 1)                  empty -> True
    validate(None, 1, 5)                     empty -> True
  validate(6, 5, +inf)     5 < 6 < +inf      ok; children get (5, 6) and (6, +inf)
    validate(3, 5, 6)      5 < 3   fails     -> False
```

Node `3` passes the local test its parent would run (`3 < 6`), but its interval `(5, 6)` remembers the root: descending right at `5` set `low = 5`, and descending left at `6` tightened only `high`, inheriting `low` unchanged. The check `5 < 3 < 6` fails on its left side, so the call returns `False`, the `and` in `validate(6, ...)` short-circuits without ever visiting node `7`, and `False` propagates up to the root call. The function returns `False`: the tree is not a valid BST.

#### Solution

The code is the interval check from the walkthrough, with each recursive call tightening one side of the bounds.

```python
from typing import Optional


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node: Optional[TreeNode], low: float, high: float) -> bool:
            if not node:
                return True
            # Every node must lie strictly within the open interval (low, high)
            if not (low < node.val < high):
                return False
            return (validate(node.left, low, node.val) and
                    validate(node.right, node.val, high))

        return validate(root, float("-inf"), float("inf"))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited once with constant work per visit.

##### Space Complexity: `O(h)`

The recursion stack reaches the tree's height `h`: `O(log n)` for a balanced tree and `O(n)` for a skewed one.

#### Key Insights

- Comparing against ancestor-derived bounds, not just children, is the crux that defeats the common wrong answer.
- Using `float("-inf")` and `float("inf")` sidesteps the `-2^31` to `2^31 - 1` value range without special casing.
- Strict `<` comparisons enforce the "strictly less / strictly greater" rule, correctly rejecting duplicate values.
- Early return on the first violation prunes the rest of the traversal.

### Inorder Traversal

#### Derivation

The bounds solution threads two numbers through every call. A different property of BSTs removes even that: an [inorder traversal](https://en.wikipedia.org/wiki/Tree_traversal) (left, node, right) of a valid BST visits values in strictly increasing order, and the converse holds as well. So validating a BST is equivalent to confirming the inorder sequence never decreases or repeats, which needs only the single previously visited value:

1. Traverse in inorder (left, node, right).
2. Track the previously visited value in `previous`.
3. At each node, fail if `node.val <= previous`, since a valid BST must strictly increase.
4. Update `previous` and continue into the right subtree.

This avoids threading bounds through the recursion; instead it leans on the structural property that inorder linearizes a BST into sorted order.

#### Walkthrough

Trace the traversal on Example 2: `root = [5,1,4,null,null,3,6]`, expected output `false`:

```text
        5
       / \
      1   4
         / \
        3   6
```

Inorder visits each node between its left and right subtrees, so a valid BST would emit its values in ascending order. The trace below indents one level per recursive call; "visit" marks the moment a node's value is compared against `previous` after its left subtree returns:

```text
inorder(5)                       descend left first
  inorder(1)                     descend left first
    inorder(None) -> True        empty left subtree
    visit 1    previous=None     first value, no check; previous = 1
    inorder(None) -> True        empty right subtree
  visit 5      previous=1        5 > 1, still increasing; previous = 5
  inorder(4)                     descend left first
    inorder(3)                   descend left first
      inorder(None) -> True      empty left subtree
      visit 3    previous=5      3 <= 5 -> return False
    inorder(4) left call False   -> False, node 4 never visited
inorder(5) right call False      -> False
```

The visited sequence begins `1, 5, 3`: the moment `3` follows `5`, the strictly increasing order breaks, and the `node.val <= previous` test fires. `False` propagates straight up without visiting nodes `4` or `6`, and the function returns `False`, matching the expected Output for Example 2.

#### Solution

The code is the inorder visit from the walkthrough, with `previous` as the only carried state.

```python
from typing import Optional


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        previous = None

        def inorder(node: Optional[TreeNode]) -> bool:
            nonlocal previous
            if not node:
                return True
            if not inorder(node.left):
                return False
            # Inorder of a valid BST is strictly increasing
            if previous is not None and node.val <= previous:
                return False
            previous = node.val
            return inorder(node.right)

        return inorder(root)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited once during the traversal.

##### Space Complexity: `O(h)`

The recursion stack is bounded by the tree height `h`, ranging from `O(log n)` to `O(n)`.

#### Key Insights

- Inorder traversal of a valid BST yields a strictly ascending sequence: a clean equivalence to exploit.
- Only the single previous value needs tracking, so no full array of values is required.
- The strict `<=` rejection again handles duplicates correctly.
- Comparing adjacent values means an early exit the moment monotonicity breaks.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - each node rescans its full subtrees, quadratic on a skewed tree.
- **Recursive Bounds**: `O(n)` - each node checked once against propagated bounds.
- **Inorder Traversal**: `O(n)` - each node visited once in sorted-order traversal.

### Space Complexity

- **All three solutions**: `O(h)` - dominated by the recursion stack, `O(log n)` balanced to `O(n)` skewed.

### Trade-offs

- **Brute Force** is the most direct restatement of the BST definition but wastes time rescanning descendants once per ancestor.
- **Recursive Bounds** makes the BST invariant explicit by carrying bounds, which generalizes naturally to range-style problems.
- **Inorder Traversal** is conceptually elegant, relying on the sorted-order property, and stores only one prior value.

### When to Use Each

- **Brute Force**: As a teaching baseline or first attempt when correctness matters more than speed.
- **Recursive Bounds**: When you want the validity constraint stated directly, or need to adapt it to subtree range queries.
- **Inorder Traversal**: When you prefer leaning on the BST's sorted-order property, or plan to reuse the inorder sequence for other checks.

### Optimization Notes

- All three approaches short-circuit on the first violation, avoiding unnecessary traversal.
- Recursive Bounds and Inorder Traversal both collapse the brute force's repeated subtree scans into a single pass by propagating constraints instead of re-deriving them.
- The Inorder Traversal can be rewritten with an explicit stack to remove recursion depth limits on extremely skewed trees.
- None of the approaches needs to materialize the full value list, keeping auxiliary space at `O(h)` rather than `O(n)`.
