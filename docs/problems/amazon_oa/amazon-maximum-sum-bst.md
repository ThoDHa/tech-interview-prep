# [Maximum Sum BST in a Binary Tree](https://www.fastprep.io/problems/amazon-maximum-sum-bst)

**Hard** | **NN minutes** | **Tree, Depth First Search, Dynamic Programming**

Given the root of a binary tree, find the maximum sum of node values among all subtrees that are valid binary search trees.

A valid BST has every left-subtree value strictly smaller than its root and every right-subtree value strictly larger. Return 0 when every valid non-empty BST subtree has a negative sum.

## Examples

### Example 1

**Input:** `root = [1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]`

**Output:** `20`

**Explanation:** The subtree rooted at 3 is a BST with sum 20.

### Example 2

**Input:** `root = [4,3,null,1,2]`

**Output:** `2`

**Explanation:** The leaf with value 2 is the best valid BST subtree.

### Example 3

**Input:** `root = [-4,-2,-5]`

**Output:** `0`

**Explanation:** All valid BST sums are negative, so zero is returned.

## Constraints

- `The tree contains between 0 and 5000 nodes.`
- `-10000 ≤ Node.val ≤ 10000.`

## Solutions

The solutions below assume the standard node definition and `from typing import Dict, Optional, Tuple`:

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

The most literal reading executes the problem's own sentence: for every node of the tree, ask whether the subtree rooted there is a valid BST, and if it is, add up that subtree's values. Two independent questions, two independent helpers: a validity check and a sum accumulation, each restarting from the candidate node's root.

The validity check is the classic top-down bounds test: a node must sit strictly between the tightest constraint imposed by its ancestors, and each descent narrows the window. A node in a left subtree must be smaller than its ancestor, so descending left tightens the upper bound; descending right tightens the lower bound. Treating the whole tree as unbounded at the start (`low = -inf`, `high = +inf`) makes the recursion uniform:

1. `is_valid_bst(node, low, high)` returns `True` for `None`, and otherwise requires
   `low < node.val < high` plus the same test on both children with the window
   narrowed to `(low, node.val)` and `(node.val, high)`.
2. `subtree_sum(node)` returns `0` for `None`, otherwise `node.val` plus both
   children's sums.
3. `visit` walks every node: when `is_valid_bst` holds for a node, fold
   `subtree_sum(node)` into `max_bst_sum`.
4. `max_bst_sum` starts at `0`, which directly encodes the rule that the answer
   is `0` when every valid BST subtree has a negative sum.
5. Return `max_bst_sum`.

#### Walkthrough

Example 3, `root = [-4,-2,-5]`, is small enough to show every visit, including the invalid root:

```text
      -4
     /  \
   -2    -5
```

```text
visit -4 (root)   is_valid_bst(-4, -inf, +inf):
                    -5 sits in -4's right subtree but -5 < -4 -> False
                    invalid, no candidate recorded
visit -2          leaf: valid -> subtree_sum(-2) = -2
                  max_bst_sum = max(0, -2) = 0
visit -5          leaf: valid -> subtree_sum(-5) = -5
                  max_bst_sum = max(0, -5) = 0
```

The root fails because a value smaller than it lives in its right subtree, and the only valid BST subtrees are the two negative leaves, so the folded maximum never rises above the initial `0`. The function returns `0`, matching the expected Output for Example 3. (On Example 1 the same process records the leaves, the subtree rooted at `5` with sum `15`, and the subtree rooted at `3` with sum `20`, and returns `20`.)

#### Solution

The code is the walkthrough's three helpers: bounds check, sum accumulation, and the visiting loop.

```python
from typing import Optional


class Solution:
    def solve(self, root: Optional[TreeNode]) -> int:
        """Return the maximum sum over all valid BST subtrees, 0 if none is positive.

        Time:  O(n^2): each of the n nodes starts a validation and a sum
            accumulation that may scan its entire subtree.
        Space: O(h) recursion stack, h the tree height.
        """
        max_bst_sum = 0

        def is_valid_bst(node: Optional[TreeNode], low: float, high: float) -> bool:
            if node is None:
                return True
            return (
                low < node.val < high
                and is_valid_bst(node.left, low, node.val)
                and is_valid_bst(node.right, node.val, high)
            )

        def subtree_sum(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            return node.val + subtree_sum(node.left) + subtree_sum(node.right)

        def visit(node: Optional[TreeNode]) -> None:
            nonlocal max_bst_sum
            if node is None:
                return
            if is_valid_bst(node, float("-inf"), float("inf")):
                max_bst_sum = max(max_bst_sum, subtree_sum(node))
            visit(node.left)
            visit(node.right)

        visit(root)
        return max_bst_sum
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` nodes starts both a validation and a sum accumulation, and either helper may traverse the node's entire subtree, so one candidate costs up to `O(n)` and the loop repeats that `n` times.

##### Space Complexity: `O(h)`

No auxiliary structure survives a visit; the recursion of the three helpers stacks at most one frame per tree level, which is `O(n)` for a fully skewed tree.

#### Key Insights

- Seeding `max_bst_sum` at `0` implements the "return 0 when all valid sums are negative" rule for free: negative candidates can never raise it.
- The bounds test must be strict on both sides (`low < node.val < high`), since a BST requires strictly smaller left values and strictly larger right values.
- The brute force re-walks each subtree from its own root, so a node deep in the tree has its values scanned once for every one of its ancestors: that repeated scanning is exactly what the next approach removes.

### Bottom-Up Validation with Precomputed Sums

#### Derivation

The brute force re-scans every subtree from its own root: validating node `v` re-walks the very nodes its children's validations already walked, and each restart costs another full pass. The repair is to build each fact from the facts of the children, once. A subtree is a valid BST exactly when both children's subtrees are valid BSTs and the children's value ranges leave room for the parent: `left_max < node.val < right_min`. So one post-order pass can hand every node a report `(is_valid, subtree_min, subtree_max)` computed in `O(1)` from its children's reports, and validity for all `n` subtrees costs one traversal.

The sums still need a home, and this approach keeps the two concerns in two separate traversals: a first post-order pass computes every subtree's sum into a dictionary keyed by node, and the validation pass consults the dictionary only where a subtree turns out valid. Plain Python objects hash by identity, so nodes work directly as dictionary keys:

1. `collect_sums` runs post-order, storing each node's subtree total in
   `subtree_sums[node]` and returning it upward.
2. `validate_subtree` runs post-order, returning `(is_valid, subtree_min,
   subtree_max)`; the `None` child reports `(True, +inf, -inf)`, the identity
   that makes `min`/`max` composition work for one-sided subtrees.
3. A node is valid when both children report valid and
   `left_max < node.val < right_min`; then `subtree_min` and `subtree_max`
   compose from the three involved values, and `subtree_sums[node]` becomes a
   candidate for `max_bst_sum`.
4. An invalid node reports `(False, 0, 0)`; parents test the validity flags
   first, so the placeholder bounds are never read.
5. Run both passes from the root and return `max_bst_sum`.

#### Walkthrough

Example 2, `root = [4,3,null,1,2]`:

```text
      4
     /
    3
   / \
  1   2
```

Pass 1 fills the sums bottom-up; pass 2 hands out the validity reports. Each report reads `(is_valid, subtree_min, subtree_max)`:

```text
pass 1  collect_sums
  node 1 (leaf)   subtree_sums[1] = 1
  node 2 (leaf)   subtree_sums[2] = 2
  node 3          subtree_sums[3] = 1 + 3 + 2 = 6
  node 4          subtree_sums[4] = 6 + 4 = 10

pass 2  validate_subtree
  node 1 (leaf)   children None -> (True, 1, 1)
                  valid: max_bst_sum = max(0, subtree_sums[1] = 1) = 1
  node 2 (leaf)   children None -> (True, 2, 2)
                  valid: max_bst_sum = max(1, subtree_sums[2] = 2) = 2
  node 3          left (True, 1, 1), right (True, 2, 2):
                  left_max = 1 < 3 holds, but 3 < right_min = 2 fails
                  -> (False, 0, 0), no candidate
  node 4          left child reports invalid -> (False, 0, 0), no candidate
```

The decisive beat is node `3`: its own value sits inside its ancestors' window, but its right child `2` is smaller than it, so the bottom-up check fails the subtree there and the sums `6` and `10` never become candidates. Only the two leaves were valid, and `max_bst_sum` settled at `2`, the expected Output for Example 2.

#### Solution

The code is the two passes from the walkthrough: one pass fills the sum dictionary, the other folds validity reports upward and records candidates.

```python
from typing import Dict, Optional, Tuple


class Solution:
    def solve(self, root: Optional[TreeNode]) -> int:
        """Return the maximum sum over all valid BST subtrees, 0 if none is positive.

        Time:  O(n): one post-order pass computes every subtree sum, and one
            bottom-up pass validates every subtree in O(1) from its children.
        Space: O(n): the sum dictionary holds one entry per node, on top of
            the O(h) recursion stack.
        """
        max_bst_sum = 0
        subtree_sums: Dict[TreeNode, int] = {}

        def collect_sums(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            total = node.val + collect_sums(node.left) + collect_sums(node.right)
            subtree_sums[node] = total
            return total

        def validate_subtree(node: Optional[TreeNode]) -> Tuple[bool, float, float]:
            nonlocal max_bst_sum
            if node is None:
                return (True, float("inf"), float("-inf"))
            left_valid, left_min, left_max = validate_subtree(node.left)
            right_valid, right_min, right_max = validate_subtree(node.right)
            if left_valid and right_valid and left_max < node.val < right_min:
                max_bst_sum = max(max_bst_sum, subtree_sums[node])
                subtree_min = min(left_min, node.val, right_min)
                subtree_max = max(left_max, node.val, right_max)
                return (True, subtree_min, subtree_max)
            return (False, 0.0, 0.0)

        collect_sums(root)
        validate_subtree(root)
        return max_bst_sum
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each pass visits every node exactly once, and both the sum combination and the validity report do constant work per node.

##### Space Complexity: `O(n)`

The `subtree_sums` dictionary holds one entry per node; the recursion stack adds `O(h)` on top.

#### Key Insights

- Bottom-up validation turns the `O(n)` per-candidate scan into an `O(1)` combination: `left_max < node.val < right_min` is the whole BST test, because the children's reports already vouch for everything below them.
- Splitting sums and validity into two passes keeps each function single-purpose, which is easier to test, at the price of a dictionary and a second traversal.
- Plain Python objects hash by identity, so `TreeNode` instances work as dictionary keys without any extra machinery; no `__eq__` override exists to complicate that.
- A top-down bounds check alone would be wrong here: it clears a node on ancestor constraints before knowing whether deeper violations exist, which is why the validity decision must travel bottom-up.

### One-Pass Post-Order DFS

#### Derivation

The previous approach computes two facts per node, its subtree sum and its validity trio, but sends them through the tree in two separate traversals and parks the sums in a dictionary between passes. Every node is visited by both passes, so the natural fold is to carry everything in one report: let the post-order recursion return `(is_valid, subtree_min, subtree_max, subtree_sum)` and the dictionary disappears along with the second traversal:

1. `postorder(None)` returns `(True, +inf, -inf, 0)`: an empty subtree is valid,
   contributes no values to the `min`/`max` composition, and sums to `0`.
2. Recurse into both children first, unpacking their four-part reports.
3. The node is valid when both children report valid and
   `left_max < node.val < right_min`; then compose `subtree_min`,
   `subtree_max`, and `subtree_sum` from the two reports plus `node.val`,
   fold the sum into `max_bst_sum`, and return the composed report.
4. Otherwise return `(False, 0, 0, 0)`, which any parent rejects via the
   validity flags before reading the placeholder fields.
5. Start at the root and return `max_bst_sum`.

#### Walkthrough

Example 1, `root = [1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]`:

```text
            1
          /   \
         4     3
        / \   / \
       2   4 2   5
                / \
               4   6
```

Post-order visits a node only after both children have reported. Each report reads `(is_valid, subtree_min, subtree_max, subtree_sum)`:

```text
postorder(1)
  postorder(4a)                       4a = the root's left child
    postorder(2)  -> (True, 2, 2, 2)      leaf
    postorder(4b) -> (True, 4, 4, 4)      leaf
    2 < 4 < 4 fails, right child equals parent
                  -> (False, 0, 0, 0)     no candidate
  postorder(3)
    postorder(2') -> (True, 2, 2, 2)      leaf
    postorder(5)
      postorder(4') -> (True, 4, 4, 4)    leaf
      postorder(6)  -> (True, 6, 6, 6)    leaf
      4 < 5 < 6 holds
                  -> (True, min(4,5,6)=4, max(4,5,6)=6, 4+5+6=15)
    2 < 3 < 4 holds
                  -> (True, min(2,3,4)=2, max(2,3,6)=6, 2+3+15=20)
                  max_bst_sum = 20
  left report is invalid -> the root is not a BST, no candidate
```

The subtree rooted at `3` composes the leaf `2` and the valid `5`-subtree into a valid BST holding every value from `2` to `6`, so its sum `20` becomes the best candidate, and the broken `4a` subtree stops the root from ever competing. The function returns `20`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's fold: two child reports in, one composed report out, with the candidate recorded on the valid branch.

```python
from typing import Optional, Tuple


class Solution:
    def solve(self, root: Optional[TreeNode]) -> int:
        """Return the maximum sum over all valid BST subtrees, 0 if none is positive.

        Time:  O(n): every node is visited once and combines its children's
            reports in O(1).
        Space: O(h) recursion stack; the report tuple replaces the sum
            dictionary of the two-pass version.
        """
        max_bst_sum = 0

        def postorder(node: Optional[TreeNode]) -> Tuple[bool, float, float, int]:
            nonlocal max_bst_sum
            if node is None:
                return (True, float("inf"), float("-inf"), 0)

            left_valid, left_min, left_max, left_sum = postorder(node.left)
            right_valid, right_min, right_max, right_sum = postorder(node.right)

            if left_valid and right_valid and left_max < node.val < right_min:
                subtree_min = min(left_min, node.val, right_min)
                subtree_max = max(left_max, node.val, right_max)
                subtree_sum = left_sum + node.val + right_sum
                max_bst_sum = max(max_bst_sum, subtree_sum)
                return (True, subtree_min, subtree_max, subtree_sum)

            return (False, 0.0, 0.0, 0)

        postorder(root)
        return max_bst_sum
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node enters `postorder` exactly once and does constant work combining its children's reports; the tree of `n` nodes costs a single linear sweep.

##### Space Complexity: `O(h)`

The only extra memory is the recursion stack, one frame per level, which reaches `O(n)` on a fully skewed tree; no dictionary or visited structure exists.

#### Key Insights

- The `None` report `(True, +inf, -inf, 0)` is the linchpin: `min` and `max` over the three involved values then compose correctly for leaves and one-sided subtrees with no special cases.
- Validity must be decided bottom-up: the parent-child range test plus the children's validity flags capture every BST violation, including ones far below the node being judged.
- This is optimal: any algorithm must inspect every node at least once, and this one touches each node exactly once with `O(1)` work.
- A skewed tree of 5,000 nodes would push the recursion past Python's default limit of 1,000 frames; the traversal translates mechanically to an explicit stack if the input shape demands it.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - each of the `n` nodes restarts a validation and a sum scan that may cover its whole subtree.
- **Bottom-Up Validation with Precomputed Sums**: `O(n)` - two linear passes, with `O(1)` validity combination per node.
- **One-Pass Post-Order DFS**: `O(n)` - one linear pass, the sum riding along in the validity report.

### Space Complexity

- **Brute Force**: `O(h)` - recursion only, nothing survives a visit.
- **Bottom-Up Validation with Precomputed Sums**: `O(n)` - the sum dictionary holds one entry per node.
- **One-Pass Post-Order DFS**: `O(h)` - recursion stack only; the report tuples live one level at a time.

### Trade-offs

- **Brute Force**: the direct transcription of the problem sentence, trivially correct and easy to trust, but quadratic time caps it at a few hundred nodes.
- **Bottom-Up Validation with Precomputed Sums**: keeps sums and validity as two independently readable passes, at the cost of a dictionary and a second traversal.
- **One-Pass Post-Order DFS**: optimal in both time and auxiliary space, but its four-part report packs more into a single function, so the fold deserves a careful first read.

### When to Use Each

- **Brute Force**: as the derivation baseline and a correctness oracle for checking the faster versions on small trees.
- **Bottom-Up Validation with Precomputed Sums**: when the two concerns stay separated naturally, for example when subtree sums are queried elsewhere and the dictionary earns its keep.
- **One-Pass Post-Order DFS (Recommended)**: the interview default: optimal, and the report tuple is a reusable pattern for any "is this subtree an X" problem that also aggregates.

### Optimization Notes

- The report-tuple pattern generalizes: any per-subtree question answerable from the children's answers (height balance, path sums, subtree size) folds into the same single traversal.
- Strict inequalities on both sides of `left_max < node.val < right_min` matter: equal values violate the BST definition, as Example 1's `4a` node with two children of values `2` and `4` shows.
- The `max_bst_sum` seed of `0` must not be replaced by `float("-inf")`: the problem redefines the answer as `0` when no valid BST subtree has a positive sum.
- For inputs near the 5,000-node cap with pathological skew, translate the recursion to an explicit stack; the report tuple moves into the stack frames unchanged.
