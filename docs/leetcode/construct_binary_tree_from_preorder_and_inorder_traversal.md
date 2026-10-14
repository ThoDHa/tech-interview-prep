# [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

**Medium** | **25 minutes** | **Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Algorithm:** [Tree traversal](https://en.wikipedia.org/wiki/Tree_traversal) · [Recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science))

**Practice:** [`practice/construct_binary_tree_from_preorder_and_inorder_traversal/solution.py`](../../practice/construct_binary_tree_from_preorder_and_inorder_traversal/solution.py)

Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.

## Examples

### Example 1

![Binary Tree Example](./assets/construct_binary_tree_example1.jpg)

**Input:** `preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`

**Output:** `[3,9,20,null,null,15,7]`

### Example 2

**Input:** `preorder = [-1]`, `inorder = [-1]`

**Output:** `[-1]`

## Constraints

- `1 <= preorder.length <= 3000`
- `inorder.length == preorder.length`
- `-3000 <= preorder[i], inorder[i] <= 3000`
- `preorder` and `inorder` consist of unique values.
- Each value of `inorder` also appears in `preorder`.
- `preorder` is guaranteed to be the preorder traversal of the tree.
- `inorder` is guaranteed to be the inorder traversal of the tree.

## Deriving the Solution

The two traversals describe the same tree from complementary angles: preorder puts every subtree's root before that subtree's other values, and inorder puts everything left of a root before it and everything right of it after. Every solution below rests on the same observation: the head of preorder names the current root, that root's position in inorder splits the remaining values into the left and right subtrees, and each half is the same problem again on smaller arrays.

1. **Start literal.** Take `preorder[0]` as the root, search for it in
   `inorder`, physically cut both lists in two, and recurse on the halves. Correct, but every node pays a linear `index` scan plus slice copies, which is `O(n^2)` on a skewed tree: see [Recursive Slicing](#recursive-slicing).
2. **Spot the waste.** The per-node linear work has two sources: re-scanning
   `inorder` for each root, and copying sub-lists that are only ever read. Neither is necessary, since positions can be precomputed once and a sub-array can be described by its bounds.
3. **Fix both.** A hash map from value to inorder index makes every root lookup
   `O(1)`, and passing `[start, end)` index ranges instead of slices removes all copying. The build drops to `O(n)`: see [Hash Map with Index Bounds](#hash-map-with-index-bounds).
4. **Refine.** The four range indices are more state than needed. When the left
   subtree is always built before the right, preorder is consumed strictly left to right, so a single shared cursor into `preorder` can replace both preorder bounds: see [Hash Map with Shared Preorder Pointer](#hash-map-with-shared-preorder-pointer).

## Solutions

### Recursive Slicing

#### Derivation

The starting question is what each traversal, on its own, pins down. The two traversals encode the tree in complementary ways. [Preorder](https://en.wikipedia.org/wiki/Tree_traversal) visits the root before its subtrees, so the first preorder value is always the root of the current subtree. Inorder visits the left subtree, then the root, then the right subtree, so once we know the root we can split inorder into its left and right halves by locating the root's position. Each half is a smaller instance of the same problem, which dictates a recursion:

1. If `preorder` is empty, the subtree is empty, so return `None`.
2. Take `root_val = preorder[0]` and create the root node.
3. Find `mid = inorder.index(root_val)`. Everything in `inorder[:mid]` belongs to
   the left subtree and everything in `inorder[mid + 1:]` belongs to the right subtree.
4. The left subtree contains exactly `mid` nodes, so its preorder values are the
   next `mid` entries: `preorder[1 : mid + 1]`. The remaining preorder values, `preorder[mid + 1:]`, form the right subtree.
5. Recurse on each half and attach the results as `root.left` and `root.right`.

This is the most direct reading of the definitions, reaching for nothing beyond list slicing and `index`, and carrying no auxiliary structure at all. The price of that plainness is the repeated `index` scan and the fresh lists each level allocates, which the later approaches remove.

#### Walkthrough

Let us trace the Recursive Slicing solution on Example 1: `preorder = [3,9,20,15,7]` and `inorder = [9,3,15,20,7]`. Each call takes the head of its `preorder` slice as the root, finds that value in its `inorder` slice to get `mid`, and splits both slices into a left and a right half. The indentation below shows how deep the recursion is; a call returns once both of its children are built.

```text
build(pre=[3,9,20,15,7], in=[9,3,15,20,7])
  root = 3, mid = 1: left_in=[9], right_in=[15,20,7]
  left  -> build(pre=[9], in=[9])
            root = 9, mid = 0: left_in=[], right_in=[]
            left  -> build(pre=[], in=[])  -> None
            right -> build(pre=[], in=[])  -> None
          returns node(9)
  right -> build(pre=[20,15,7], in=[15,20,7])
            root = 20, mid = 1: left_in=[15], right_in=[7]
            left  -> build(pre=[15], in=[15])
                      root = 15, both halves empty -> node(15)
            right -> build(pre=[7], in=[7])
                      root = 7, both halves empty -> node(7)
          returns node(20)
returns node(3)
```

Reading the steps: the first call picks `3` as the root and locates it at `mid = 1` in inorder, so `[9]` is the left subtree and `[15,20,7]` is the right. The matching preorder slices are `preorder[1:2] = [9]` for the left and `preorder[2:] = [20,15,7]` for the right. The left call builds the single node `9`. The right call picks `20` as its root, splitting into left `[15]` and right `[7]`, each of which becomes a leaf.

Assembling the returned nodes top down gives the tree with `3` at the root, `9` as its left child, and `20` as its right child with children `15` and `7`. Read in level order that is `[3,9,20,null,null,15,7]`, which matches the expected Output.

#### Solution

The code is the walkthrough's split written down: take the head of `preorder`, cut both lists at `mid`, and recurse on the halves.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder:
            return None

        # The first preorder value is the root of the current subtree
        root_val = preorder[0]
        root = TreeNode(root_val)

        # The root's position in inorder splits the left and right subtrees
        mid = inorder.index(root_val)

        # Left subtree: inorder[:mid] with the matching preorder[1 : mid + 1]
        root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])
        # Right subtree: inorder[mid + 1:] with the remaining preorder
        root.right = self.buildTree(preorder[mid + 1 :], inorder[mid + 1 :])
        return root
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each call does an `O(n)` `inorder.index` search and builds `O(n)`-sized slices. For a balanced tree the recurrence is `T(n) = 2T(n/2) + O(n)`, giving `O(n log n)`, but a skewed tree degrades the search and slicing to `O(n)` work at every level over `n` levels, producing the `O(n^2)` worst case.

##### Space Complexity: `O(n^2)`

The slices created at each level copy `O(n)` elements, and a skewed tree creates `O(n)` levels of live slices, so the slice copies dominate at `O(n^2)` in the worst case. The recursion stack alone is `O(n)`.

#### Key Insights

- The head of preorder is the root; the position of that root in inorder splits
  the remaining values into the two subtrees.
- The left subtree's node count equals `mid`, which is exactly how many preorder
  values to peel off for the left recursion.
- It is the cleanest expression of the idea but pays for repeated `index` scans
  and slice copies.

### Hash Map with Index Bounds

#### Derivation

The slicing approach repeats two expensive operations: scanning inorder for the root and copying slices. Both disappear once we precompute root positions and pass array bounds instead of physical slices.

1. Build a [hash map](https://en.wikipedia.org/wiki/Hash_table) `inorder_index` from each value to its index in `inorder`.
   Because all values are unique, this gives `O(1)` root-position lookups.
2. Describe each subtree by two half-open ranges: `[pre_start, pre_end)` into
   `preorder` and `[in_start, in_end)` into `inorder`. A range with `pre_start >= pre_end` is empty and returns `None`.
3. The root is `preorder[pre_start]`. Look up `mid = inorder_index[root_val]` and
   compute `left_size = mid - in_start`, the number of nodes in the left subtree.
4. The left subtree occupies preorder `[pre_start + 1, pre_start + 1 + left_size)`
   and inorder `[in_start, mid)`. The right subtree occupies the rest of preorder `[pre_start + 1 + left_size, pre_end)` and inorder `[mid + 1, in_end)`.
5. Recurse on both ranges and attach the children.

#### Walkthrough

Let us rebuild Example 1 with ranges instead of slices: `preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`. The map built up front is `inorder_index = {9: 0, 3: 1, 15: 2, 20: 3, 7: 4}`. Each call receives the half-open ranges `[pre_start, pre_end)` and `[in_start, in_end)`, reads its root from `preorder[pre_start]`, looks up `mid`, and computes `left_size = mid - in_start`. The arrays are never touched beyond those two reads. The indentation shows recursion depth:

```text
build(0, 5, 0, 5)      root = preorder[0] = 3,  mid = 1, left_size = 1 - 0 = 1
  build(1, 2, 0, 1)    root = preorder[1] = 9,  mid = 0, left_size = 0 - 0 = 0
    build(2, 2, 0, 0)  pre_start >= pre_end -> None
    build(2, 2, 1, 1)  pre_start >= pre_end -> None
                       returns node(9)
  build(2, 5, 2, 5)    root = preorder[2] = 20, mid = 3, left_size = 3 - 2 = 1
    build(3, 4, 2, 3)  root = preorder[3] = 15, both child ranges empty -> node(15)
    build(4, 5, 4, 5)  root = preorder[4] = 7,  both child ranges empty -> node(7)
                       returns node(20)
returns node(3)
```

The splits are the same as in the slicing walkthrough, only expressed as index arithmetic: the top call's `left_size = 1` sends preorder range `[1, 2)` and inorder range `[0, 1)` to the left child, and the remainder, `[2, 5)` and `[3, 5)`, to the right. No list is ever copied and no scan is ever repeated. The assembled tree is again `3` with left child `9` and right child `20` over `15` and `7`, which reads in level order as `[3,9,20,null,null,15,7]`, the expected Output.

#### Solution

The code is the walkthrough's range bookkeeping: the same splits, expressed as four indices instead of new lists.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # Map each value to its index in inorder for O(1) root lookups
        inorder_index = {val: i for i, val in enumerate(inorder)}

        def build(pre_start: int, pre_end: int, in_start: int, in_end: int) -> Optional[TreeNode]:
            # Empty preorder range means an empty subtree
            if pre_start >= pre_end:
                return None

            # The first value in the preorder range is the root
            root_val = preorder[pre_start]
            root = TreeNode(root_val)

            # Split inorder at the root; left_size counts the left subtree's nodes
            mid = inorder_index[root_val]
            left_size = mid - in_start

            root.left = build(pre_start + 1, pre_start + 1 + left_size, in_start, mid)
            root.right = build(pre_start + 1 + left_size, pre_end, mid + 1, in_end)
            return root

        return build(0, len(preorder), 0, len(inorder))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We create each of the `n` nodes exactly once, and each recursive call does constant work thanks to the `O(1)` inorder-index map and the absence of slicing. Building the map is also `O(n)`.

##### Space Complexity: `O(n)`

The hash map stores all `n` values. The recursion stack adds `O(h)` where `h` is the tree height (`O(n)` for a skewed tree, `O(log n)` when balanced), which is dominated by the map.

#### Key Insights

- Passing index bounds instead of slices removes all copying, collapsing the
  space from `O(n^2)` to `O(n)`.
- The index map turns the repeated linear `index` search into a constant-time
  lookup, removing the other source of the `O(n^2)` time.
- `left_size = mid - in_start` is what keeps the two preorder ranges aligned with
  the inorder split.

### Hash Map with Shared Preorder Pointer

#### Derivation

The bounds approach still threads four indices through every call. We can shrink that to a single inorder range plus one shared preorder pointer by exploiting the order in which preorder lays nodes out: the entire left subtree appears before any right-subtree node.

1. Build the same `inorder_index` map for `O(1)` lookups.
2. Keep one moving pointer `pre_pos` into `preorder`, starting at `0`. Each node
   we create consumes exactly one preorder value and advances the pointer.
3. [Recurse](https://en.wikipedia.org/wiki/Recursion_(computer_science)) with the inclusive inorder bounds `[left, right]` for the current
   subtree. When `left > right` the subtree is empty, so return `None`.
4. Take the root from `preorder[pre_pos]`, advance the pointer, find its index
   `mid` in inorder, then build the left child from `[left, mid - 1]` and the right child from `[mid + 1, right]`.

Building the left subtree fully before the right subtree is essential: it keeps the preorder pointer synchronized, since preorder lays out the entire left subtree before any right-subtree node. The Invariant below states that formally: on entry to every call, `preorder[pre_pos]` is that subtree's root, which only stays true if the left subtree is fully consumed before the right one begins.

#### Invariant

Where the bounds version hands each subtree its own preorder range, this version keeps one mutable cursor for the whole build. The property that makes the two equivalent is:

$$ \text{on entry to } \textit{build}(\textit{left},\ \textit{right}):\quad \textit{preorder}[\textit{pre\_pos}] = \text{root of that subtree} $$

```text
on entry to build(left, right):  preorder[pre_pos] == root of that subtree
        (for every non-empty call, that is left <= right)
```

Here `[left, right]` are the inclusive inorder bounds of the subtree being built, and `pre_pos` is the number of nodes created so far.

It holds because preorder lays a subtree out as its root, then the entire left subtree, then the entire right subtree:

$$ \underbrace{\textit{root}}_{1 \text{ value}}\\
\underbrace{\cdots}_{\textit{left\_size} \text{ values}}\\
\underbrace{\cdots}_{\text{the rest}} $$

```text
preorder for one subtree:  root     then  left subtree      then  right subtree
                           1 value        left_size values        the rest
```

So the cursor must consume exactly one value for the root and then be advanced past precisely the left subtree before the right subtree's root is read. The code does the first with `self.pre_pos += 1` and the second by *finishing* `build(left, mid - 1)` before starting `build(mid + 1, right)`. By induction that left call creates one node per value it consumes and returns with the cursor on the next unconsumed value, which is exactly the right subtree's root.

Nothing verifies this at runtime. Swap the order of the two recursive calls so the right subtree is built first, and the right subtree reads its root from a position belonging to the left, so the cursor and the bounds stop agreeing about which subtree is being built. On the problem's own Example 1 that desynchronization compounds until the recursion walks off the end of `preorder` and raises `IndexError`. The outcome is strictly binary: the swap raises on every input containing a node with two children, and is a harmless no-op on every input without one, since there one of the two calls is empty and their order cannot matter. The inorder bounds constrain only the *shape* of each subtree; the cursor order is the sole thing pinning *which value* lands at each position.

#### Walkthrough

Let us rebuild Example 1 once more, watching the cursor: `preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`, with the same `inorder_index = {9: 0, 3: 1, 15: 2, 20: 3, 7: 4}`. Each call now carries only the inclusive inorder bounds `[left, right]`; the shared `pre_pos` starts at `0` and advances once per created node. Each line notes where `pre_pos` stands on entry, so the Invariant can be checked at every step:

```text
build(0, 4)      pre_pos=0: root = preorder[0] = 3, pre_pos -> 1, mid = 1
  build(0, 0)    pre_pos=1: root = preorder[1] = 9, pre_pos -> 2, mid = 0
    build(0, -1) left > right -> None
    build(1, 0)  left > right -> None
                 returns node(9); cursor now rests on preorder[2] = 20
  build(2, 4)    pre_pos=2: root = preorder[2] = 20, pre_pos -> 3, mid = 3
    build(2, 2)  pre_pos=3: root = preorder[3] = 15, pre_pos -> 4 -> node(15)
    build(4, 4)  pre_pos=4: root = preorder[4] = 7,  pre_pos -> 5 -> node(7)
                 returns node(20)
returns node(3)
```

The Invariant is visible in the middle of the trace: when the left call `build(0, 0)` finishes building node `9`, the cursor has advanced to `2`, and `preorder[2] = 20` is exactly the root of the right subtree that `build(2, 4)` is about to construct. No preorder bounds were ever passed; the left-before-right call order alone kept the cursor aligned. The finished tree is the same `3`, `9`, `20`, `15`, `7` structure, read in level order as `[3,9,20,null,null,15,7]`, the expected Output.

#### Solution

The code is the walkthrough's cursor discipline written down: one `pre_pos` advance per node, left subtree finished before the right begins.

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # Map each value to its index in inorder for O(1) root lookups
        inorder_index = {val: i for i, val in enumerate(inorder)}
        self.pre_pos = 0

        def build(left: int, right: int) -> Optional[TreeNode]:
            # No values remain for this subtree
            if left > right:
                return None

            # The next unconsumed preorder value is always this subtree's root
            root_val = preorder[self.pre_pos]
            self.pre_pos += 1
            root = TreeNode(root_val)

            # Inorder splits into left and right subtrees around the root
            mid = inorder_index[root_val]
            root.left = build(left, mid - 1)
            root.right = build(mid + 1, right)
            return root

        return build(0, len(inorder) - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We create each of the `n` nodes exactly once, and each recursive call does constant work thanks to the `O(1)` inorder-index map. Building that map is also `O(n)`.

##### Space Complexity: `O(n)`

The hash map stores all `n` values. The recursion stack adds `O(h)` where `h` is the tree height (`O(n)` for a skewed tree, `O(log n)` when balanced), which is dominated by the map.

#### Key Insights

- A single shared preorder pointer, advanced left-subtree-first, removes the need
  to track preorder ranges at all.
- The left-before-right recursion order is what makes the shared pointer correct:
  preorder finishes the whole left subtree before touching the right.
- Only the inorder bounds need to be passed, since preorder is consumed strictly
  in order.

## Comparison of Solutions

### Time Complexity

- **Recursive Slicing**: `O(n^2)` worst case - `index` searches and slice copies
  repeat linear work on skewed trees.
- **Hash Map with Index Bounds**: `O(n)` - constant-time lookups, no slicing.
- **Hash Map with Shared Preorder Pointer**: `O(n)` - constant-time lookups, no
  slicing.

### Space Complexity

- **Recursive Slicing**: `O(n^2)` - layered slice copies dominate the `O(n)` stack.
- **Hash Map with Index Bounds**: `O(n)` - index map plus `O(h)` recursion stack.
- **Hash Map with Shared Preorder Pointer**: `O(n)` - index map plus `O(h)`
  recursion stack.

### Trade-offs

- **Recursive Slicing** is the easiest to read and derive but allocates new lists
  and rescans inorder at every node.
- **Hash Map with Index Bounds** keeps each subtree self-contained through four
  indices, which is explicit but verbose.
- **Hash Map with Shared Preorder Pointer** is the most compact optimal form but
  relies on mutable shared state and a strict left-to-right traversal order.

### When to Use Each

- **Recursive Slicing**: When clarity matters more than performance, or `n` is
  small and the inputs are not adversarially skewed.
- **Hash Map with Index Bounds**: When you want optimal performance with purely
  local state and no reliance on traversal-order side effects (Recommended).
- **Hash Map with Shared Preorder Pointer**: When you want the tightest optimal
  code and are comfortable reasoning about the shared pointer's invariant.

### Optimization Notes

- The `inorder_index` map is the single change that removes the `O(n)` root search;
  it is well defined precisely because all values are unique.
- Passing index bounds instead of slices is what cuts both time and space from
  `O(n^2)` to `O(n)`; the same trick applies to building a tree from postorder and inorder.
- All three solutions recurse once per node, so a fully skewed input near the
  `3000`-node limit needs roughly `3000` stack frames, which exceeds CPython's default recursion limit of `1000`. For such inputs, raise the limit with `sys.setrecursionlimit` or rewrite the construction iteratively with an explicit stack.
- The hash map itself can be eliminated: advance a shared pointer through both
  arrays and pass each subtree a *stop value* instead of index bounds. Build left children from consecutive preorder values until the current inorder value equals the subtree's stop value (the subtree root's value for a left child, the inherited stop value for a right child), consuming one inorder position each time a subtree closes. This keeps `O(n)` time with no auxiliary map, at the cost of a distinctly subtler invariant than either hash map version.
