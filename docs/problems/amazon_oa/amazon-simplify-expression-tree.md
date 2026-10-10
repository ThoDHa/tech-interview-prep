# [Simplify a Binary Expression Tree](https://www.fastprep.io/problems/amazon-simplify-expression-tree)

**Medium** | **NN minutes** | **Tree, Recursion, Parsing**

A valid binary expression tree is serialized in prefix order. Each token is +, -, *, a variable name, or a signed integer.

Simplify the tree bottom-up. Fold an operator when both children are integers. Also apply x + 0 = x, 0 + x = x, x - 0 = x, x * 1 = x, 1 * x = x, and x * 0 = 0. Return the simplified tree as one space-separated prefix expression.

## Examples

### Example 1

**Input:** `preorder = ["+","*","x","1","0"]`

**Output:** `"x"`

**Explanation:** Multiplication by one and addition of zero both disappear.

### Example 2

**Input:** `preorder = ["*","+","2","3","y"]`

**Output:** `"* 5 y"`

**Explanation:** The constant addition folds while the variable multiplication remains.

## Constraints

- `1 <= preorder.length <= 10000.`
- `The prefix sequence is a valid binary expression tree.`
- `Every folded result fits in a signed 64-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
