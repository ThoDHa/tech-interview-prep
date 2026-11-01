# [Hierarchical Document Search](https://www.fastprep.io/problems/amazon-hierarchical-document-search)

**Medium** | **NN minutes** | **Tree, Depth First Search**

Source note: The report asks for an extensible folder search library with size and type filters. Tree serialization, matching conventions, and ordering are practice assumptions. Conservative editorial estimate of core-task match: about 85%.

Implement document search over a hierarchy of folders. Each folder contains documents or subfolders.

For this exercise, assume nodes have zero-based IDs and the aligned arrays describe one valid rooted tree. parents[i] is the parent of node i; exactly one parent is -1. In documentFlags[i], 0 means a folder and 1 means a document. Document size and type are in sizes and documentTypes; folder values are ignored.

Search the subtree rooted at folder root. Return document IDs whose size is strictly greater than minSize and whose type equals wantedType. An empty wantedType disables the type condition. Type comparison is case-sensitive. Combine enabled conditions using AND and return matching IDs in increasing order.

Keep the tree traversal separate from the filter rules, so you can add another document condition without rewriting the traversal. Explain how you would test nested folders, combined filters, and size boundaries.

## Examples

### Example 1

**Input:** `parents = [-1,0,0,1,1,2]`, `documentFlags = [0,0,0,1,1,1]`, `sizes = [0,0,0,10,30,40]`, `documentTypes = ["","","","pdf","txt","pdf"]`, `root = 0`, `minSize = 20`, `wantedType = "pdf"`

**Output:** `[5]`

**Explanation:** Only document 5 is both larger than 20 bytes and of type pdf.

### Example 2

**Input:** `parents = [-1,0,0,1,1,2]`, `documentFlags = [0,0,0,1,1,1]`, `sizes = [0,0,0,10,30,40]`, `documentTypes = ["","","","pdf","txt","pdf"]`, `root = 1`, `minSize = 10`, `wantedType = ""`

**Output:** `[4]`

**Explanation:** Search only folder 1. Document 3 equals the threshold, so only document 4 matches.

## Constraints

- `For this exercise, assume 1 <= parents.length <= 100000, with all node arrays of equal length.`
- `Parent IDs describe a valid tree; documents have no children, and each folder has either only document children or only folder children.`
- `root is a valid folder ID.`
- `Document sizes and minSize are between 0 and 10^9.`
- `Document types and wantedType have at most 30 ASCII letters; document types are nonempty.`

## Deriving the Solution

The page's statement is explicit that the serialization and the matching rules are practice assumptions, so the contract this write-up implements, and the gauntlet tests, is exactly the following restatement of it: the four node arrays are aligned and describe one valid rooted tree (`parents[i]` is the parent of node `i`, exactly one entry is `-1`); documents (flag `1`) have no children and every folder's children are homogeneous (all documents or all folders); a document matches when its size is strictly greater than `minSize` and, when `wantedType` is non-empty, its type equals `wantedType` case-sensitively; folder rows in `sizes` and `documentTypes` are ignored; enabled conditions combine with AND; matching IDs return in increasing order. Every approach below separates the two concerns the statement asks to keep separate: finding the subtree, and filtering its documents.

1. **Start literal.** The subtree of `root` is the set of nodes whose parent chain reaches `root`, and the parent array answers chain questions directly: walk each node's parents and keep the documents that pass the filters: see [Parent-Walk Membership](#parent-walk-membership).
2. **Invert the walks.** Repeating an `O(depth)` walk per node is the waste; building the children map once turns membership into a single traversal that visits the subtree exactly: see [Children-Map DFS](#children-map-dfs).

## Solutions

### Parent-Walk Membership

#### Derivation

The most literal reading of "search the subtree rooted at `root`" asks, of every node, whether `root` sits on its parent chain. The parent array answers that question with no preprocessing: follow `parents[node]` until it reaches `root` (a member) or `-1` (not in the subtree). Applying the size and type filters to the documents among the members and sorting the survivors completes the search. Rebuilding nothing and using only the given array is this approach's whole appeal, and its whole cost: every node pays a fresh walk:

1. For each node `node`, walk `node = parents[node]` until it equals `root` (in the subtree) or `-1` (not).
2. When it is in the subtree and `documentFlags[node] == 1`, test the filters: `sizes[node] > minSize`, and `wantedType == ""` or `documentTypes[node] == wantedType`.
3. Collect the passing IDs and return them sorted.

#### Walkthrough

Example 2, with `root = 1`, `minSize = 10`, `wantedType = ""`. Each node's walk is one row; the verdict decides whether the filters run:

```text
node 0  walk 0 -> -1            outside, skip
node 1  walk 1 == root          in subtree, folder, skip
node 2  walk 2 -> 0 -> -1       outside, skip
node 3  walk 3 -> 1 == root     document: size 10 > 10 is false
node 4  walk 4 -> 1 == root     document: size 30 > 10 and type test disabled
node 5  walk 5 -> 2 -> 0 -> -1  outside, skip

matches [4]
```

Only document `4` survives both the membership walks and the filter, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def searchDocuments(
        self,
        parents: List[int],
        documentFlags: List[int],
        sizes: List[int],
        documentTypes: List[str],
        root: int,
        minSize: int,
        wantedType: str,
    ) -> List[int]:
        matches: List[int] = []
        for node in range(len(parents)):
            walker, in_subtree = node, False
            while walker != -1:
                if walker == root:
                    in_subtree = True
                    break
                walker = parents[walker]
            if (
                in_subtree
                and documentFlags[node] == 1
                and sizes[node] > minSize
                and (wantedType == "" or documentTypes[node] == wantedType)
            ):
                matches.append(node)
        return sorted(matches)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * depth + d log d)`

Each of the `n` nodes pays one parent walk of up to `depth` steps, and the `d` matches sort at the end. On a `100000`-node chain this is `10^10` steps, far past usable.

##### Space Complexity: `O(n)`

The output and its sorted copy dominate; the walk itself keeps one label.

#### Key Insights

- The parent array is a complete oracle for subtree membership on its own; no children map is required to be correct.
- The filters stay inline here, which is exactly the coupling the statement warns about: adding a third condition means editing the walk.
- Per-node walks re-traverse the same ancestor chains quadratically often in depth, which is the redundancy the next approach removes.

### Children-Map DFS

#### Derivation

The Parent-Walk's repeated work is re-deriving one relation per node: who is in the subtree. Inverting the parent array once answers it for the whole tree: a node's subtree is exactly the node plus the subtrees of its children, so a single traversal from `root` visits the search space with no membership tests at all. Building that children map is one linear pass, and the traversal is a stack loop, immune to the recursion depth a `100000`-node chain would produce. The statement's extensibility demand is met by keeping the filter as its own predicate that the traversal never sees:

1. Build `children`: one pass over `parents`, appending each node under its parent.
2. Walk the subtree with a stack seeded at `root`, collecting every visited node.
3. Keep the nodes where the filter predicate holds: document flag `1`, `sizes[node] > minSize`, and the case-sensitive type test unless `wantedType` is empty.
4. Return the survivors sorted.

#### Walkthrough

Example 1, with `root = 0`, `minSize = 20`, `wantedType = "pdf"`. Each row shows the stack at the top of the loop with the next node to pop rightmost; the filter column runs only on documents:

```text
stack [0]      visit 0          folder, skip
stack [1, 2]   visit 2          folder, skip
stack [1, 5]   visit 5          document: size 40 > 20 true, type pdf == pdf
stack [1]      visit 1          folder, skip
stack [3, 4]   visit 4          document: size 30 > 20 true, type txt != pdf
stack [3]      visit 3          document: size 10 > 20 false

matches [5]
```

The traversal visited the whole subtree once and the filter kept exactly document `5`, matching the expected Output.

#### Solution

The code is the walkthrough's two loops plus the filter predicate: a linear pass builds `children`, a stack loop visits the subtree, and `_is_matching_document` holds the only filter logic.

```python
from typing import DefaultDict, List


class Solution:
    def searchDocuments(
        self,
        parents: List[int],
        documentFlags: List[int],
        sizes: List[int],
        documentTypes: List[str],
        root: int,
        minSize: int,
        wantedType: str,
    ) -> List[int]:
        children: DefaultDict[int, List[int]] = DefaultDict(list)
        for node, parent in enumerate(parents):
            if parent != -1:
                children[parent].append(node)

        matches: List[int] = []
        stack = [root]
        while stack:
            node = stack.pop()
            if self._is_matching_document(node, documentFlags, sizes, documentTypes, minSize, wantedType):
                matches.append(node)
            stack.extend(children.get(node, []))
        return sorted(matches)

    @staticmethod
    def _is_matching_document(
        node: int,
        documentFlags: List[int],
        sizes: List[int],
        documentTypes: List[str],
        minSize: int,
        wantedType: str,
    ) -> bool:
        if documentFlags[node] != 1:
            return False
        if sizes[node] <= minSize:
            return False
        return wantedType == "" or documentTypes[node] == wantedType
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + d log d)`

One linear pass builds the child map, the traversal visits each subtree node once, and the `d` matches sort.

##### Space Complexity: `O(n)`

The child map holds one entry per non-root node and the stack at most the subtree's frontier.

#### Key Insights

- Inverting the parent array once (`children`) replaces n membership walks with one traversal; that inversion is the whole complexity win.
- The filter predicate takes node indices only and never asks about the tree, so a new document condition is one new clause in one function, which is the extensibility the statement asks to explain.
- The explicit stack matters at this problem's scale: a recursive DFS on a `100000`-node folder chain would hit Python's recursion limit before visiting half the tree.

## Comparison of Solutions

### Time Complexity

- **Parent-Walk Membership**: `O(n * depth + d log d)` - one ancestor walk per node.
- **Children-Map DFS**: `O(n + d log d)` - one map build plus one traversal.

### Space Complexity

- **Parent-Walk Membership**: `O(n)` - the output; the walk keeps one label.
- **Children-Map DFS**: `O(n)` - the child map plus the traversal stack.

### Trade-offs

- **Parent-Walk Membership**: zero preprocessing and a direct transcription of subtree membership, at the price of quadratic-in-depth total work and filters tangled into the walk.
- **Children-Map DFS**: one preprocessing pass buys a minimal traversal and a filter isolated in a predicate; the price is the child map's memory.

### When to Use Each

- **Parent-Walk Membership**: for a one-off query on a shallow hierarchy, or when the input is strictly the parent array and building auxiliary maps is disallowed.
- **Children-Map DFS (Recommended)**: the answer to give in an interview: linear in the input, comfortably inside the `100000`-node bound, and structured so the filter rules can grow without touching the traversal.

### Optimization Notes

- Memoizing the parent walks (resolve each node's membership once and fill its chain) turns the brute force into an `O(n)` algorithm that never builds the child map; the gauntlet's independent oracle uses exactly that shape to cross-check the reference.
- If the same hierarchy faces many searches with different roots, preprocessing depth numbers or an Euler tour answers membership in `O(1)` per query after one `O(n)` pass.
- The sort at the end is the only super-linear step; collecting matches into a boolean seen-array and sweeping once would trade the `d log d` for `O(n)` extra space and is not worth it at these sizes.
