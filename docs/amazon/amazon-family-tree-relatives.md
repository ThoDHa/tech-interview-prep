# [Are Two People Relatives in a Family Tree?](https://www.fastprep.io/problems/amazon-family-tree-relatives)

**Medium** | **NN minutes** | **Graph, Breadth First Search, Hash Table**

A family tree is given as a list of rows. Each row relations[i] = [parent, child] means that parent is a parent of child. A person can have up to two recorded parents, and some people have no recorded parents at all. Because a child can have two parents, the family is a graph, not a simple tree.

Two people are relatives when they share at least one ancestor. Each person counts as one of their own ancestors. So a person is a relative of every ancestor and every descendant they have, and a person is always a relative of themselves.

## Examples

### Example 1

**Input:** `relations = [["ann","bob"],["ann","cat"],["bob","dan"],["cat","eve"]]`, `first = "dan"`, `second = "eve"`

**Output:** `true`

**Explanation:** dan's ancestors are dan, bob, and ann. eve's ancestors are eve, cat, and ann. Both sets contain ann, so the two cousins are relatives.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-family-tree-relatives; fill them in. -->

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
