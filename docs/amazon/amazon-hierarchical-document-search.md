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

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
