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

### Explicit Tree with Post-Order Folding

#### Derivation

The statement names a tree, so the first solution builds exactly that object: parse the prefix sequence into nodes, simplify the tree bottom-up, then serialize whatever survived. Prefix order makes the parse mechanical: the next token is always the root of the next subtree, and an operator token owns the two subtrees that follow it.

1. Read the tokens through an iterator. `build_subtree` consumes one token per call:
   a leaf token returns immediately as a node, an operator token first fills
   `node.left` and `node.right` with two recursive calls and then returns.
2. `simplify` runs in post-order: a leaf returns as it is, an operator node first
   simplifies both children, then decides.
3. The decision mirrors the statement. When both children hold integer tokens,
   compute the arithmetic result and return one integer node. Otherwise test the six
   identities and return the surviving child when one fires. Otherwise keep the node.
4. `serialize` walks the simplified tree in prefix order, appending into one shared
   token list, and `" ".join` flattens it.

#### Walkthrough

Example 1, `preorder = ["+","*","x","1","0"]`, builds this tree, where the root's right child is the leaf `0`:

```text
       +          root: operator, then the left subtree "*", then the right leaf "0"
      / \
     *   0
    / \
   x   1
```

Post-order simplification visits the `*` node before the `+` node, and each decision consumes the final form of both children:

```text
visit *   children "x" and "1"   x * 1 = x applies -> replace with leaf "x"
visit +   children "x" and "0"   x + 0 = x applies -> replace with leaf "x"
serialize                        "x"
```

The first fold is what enables the second: the `+` node only sees a plain `x` child because the `*` subtree already collapsed. Serializing the surviving single node returns `"x"`, the expected Output.

#### Solution

The code is the walkthrough written down: build, simplify, serialize.

```python
from dataclasses import dataclass
from typing import Iterator, List, Optional

OPERATORS = {"+", "-", "*"}


@dataclass
class ExpressionNode:
    token: str
    left: Optional["ExpressionNode"] = None
    right: Optional["ExpressionNode"] = None


def is_integer_token(token: str) -> bool:
    if token in OPERATORS:
        return False
    digits = token[1:] if token.startswith("-") else token
    return digits.isdigit()


def build_subtree(token_stream: Iterator[str]) -> ExpressionNode:
    token = next(token_stream)
    node = ExpressionNode(token)
    if token in OPERATORS:
        node.left = build_subtree(token_stream)
        node.right = build_subtree(token_stream)
    return node


def simplify(node: ExpressionNode) -> ExpressionNode:
    if node.token not in OPERATORS:
        return node
    node.left = simplify(node.left)
    node.right = simplify(node.right)
    left_token, right_token = node.left.token, node.right.token
    if is_integer_token(left_token) and is_integer_token(right_token):
        left_value, right_value = int(left_token), int(right_token)
        if node.token == "+":
            return ExpressionNode(str(left_value + right_value))
        if node.token == "-":
            return ExpressionNode(str(left_value - right_value))
        return ExpressionNode(str(left_value * right_value))
    if node.token == "+" and right_token == "0":
        return node.left
    if node.token == "+" and left_token == "0":
        return node.right
    if node.token == "-" and right_token == "0":
        return node.left
    if node.token == "*" and left_token == "1":
        return node.right
    if node.token == "*" and right_token == "1":
        return node.left
    if node.token == "*" and right_token == "0":
        return ExpressionNode("0")
    return node


def serialize(node: ExpressionNode, tokens: List[str]) -> None:
    tokens.append(node.token)
    if node.token in OPERATORS:
        serialize(node.left, tokens)
        serialize(node.right, tokens)


class Solution:
    def solve(self, preorder: List[str]) -> str:
        tokens: List[str] = []
        serialize(simplify(build_subtree(iter(preorder))), tokens)
        return " ".join(tokens)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every token is read once while building, visited once while simplifying, and appended once while serializing.

##### Space Complexity: `O(n)`

One node per token, plus recursion along the tree height, which a left-deep expression drives to `O(n)`.

#### Key Insights

- Prefix order parses without lookahead: the next token is always the next subtree's root, so a recursive builder needs no index bookkeeping.
- Simplification must run post-order: an identity such as `x * 1 = x` can only fire after both children have reached their final form, and Example 1 shows one fold enabling the next.
- The identity list is applied verbatim, asymmetries included: `x - 0 = x` fires but `0 - x` does not, and `x * 0 = 0` fires but `0 * x` does not, because the statement lists exactly those six rewrites.
- After simplification an integer subtree is always a single token, so inspecting a child's `.token` is enough to classify it.

### Recursive Descent with Inline Folding

#### Derivation

The tree version spends one node object per token and two extra traversals on bookkeeping. The observation that removes both: a subtree's simplified form is fully determined the moment both of its subtrees have been read, so parsing and folding can share one traversal, and the fold's output can be the subtree's serialized token list instead of a node. Classifying a finished subtree is then immediate: it is an integer literal exactly when its list is one integer token.

1. `read_subtree` consumes one token. A leaf returns `[token]`.
2. An operator first reads its two subtrees, then calls `fold`.
3. `fold` computes the arithmetic result when both lists are single integer tokens,
   returns the surviving side when an identity fires, and otherwise concatenates
   `[operator] + left_tokens + right_tokens`.
4. `solve` returns the one remaining list joined with spaces.

#### Walkthrough

Example 2, `preorder = ["*","+","2","3","y"]`, shows the fold happening as the recursion unwinds:

```text
read "*"      operator, read the left subtree first
  read "+"    operator, read its left
    read "2"  leaf -> ["2"]
    read "3"  leaf -> ["3"]
    fold "+"  both integers -> ["5"]
  read "y"    leaf -> ["y"]
  fold "*"    ["5"] and ["y"]: both-integer fails, no identity fires
              -> ["*", "5", "y"]
```

The constant addition collapsed during the parse while the variable multiplication survived untouched, so joining the top-level list returns `"* 5 y"`, the expected Output.

#### Solution

The code is the recursion from the walkthrough, with `fold` carrying every rule from the statement.

```python
from typing import Iterator, List

OPERATORS = {"+", "-", "*"}


def is_integer_token(token: str) -> bool:
    if token in OPERATORS:
        return False
    digits = token[1:] if token.startswith("-") else token
    return digits.isdigit()


def fold(operator: str, left_tokens: List[str], right_tokens: List[str]) -> List[str]:
    left_is_integer = len(left_tokens) == 1 and is_integer_token(left_tokens[0])
    right_is_integer = len(right_tokens) == 1 and is_integer_token(right_tokens[0])
    if left_is_integer and right_is_integer:
        left_value, right_value = int(left_tokens[0]), int(right_tokens[0])
        if operator == "+":
            return [str(left_value + right_value)]
        if operator == "-":
            return [str(left_value - right_value)]
        return [str(left_value * right_value)]
    if operator == "+" and right_tokens == ["0"]:
        return left_tokens
    if operator == "+" and left_tokens == ["0"]:
        return right_tokens
    if operator == "-" and right_tokens == ["0"]:
        return left_tokens
    if operator == "*" and left_tokens == ["1"]:
        return right_tokens
    if operator == "*" and right_tokens == ["1"]:
        return left_tokens
    if operator == "*" and right_tokens == ["0"]:
        return ["0"]
    return [operator] + left_tokens + right_tokens


def read_subtree(token_stream: Iterator[str]) -> List[str]:
    token = next(token_stream)
    if token not in OPERATORS:
        return [token]
    left_tokens = read_subtree(token_stream)
    right_tokens = read_subtree(token_stream)
    return fold(token, left_tokens, right_tokens)


class Solution:
    def solve(self, preorder: List[str]) -> str:
        return " ".join(read_subtree(iter(preorder)))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Reading the tokens is one pass. The honest total is `O(n × h)` with `h` the tree height: every fold that keeps its operator concatenates the two child lists, so each token is copied once per unfolded ancestor, which is quadratic on a left-deep chain that never folds.

##### Space Complexity: `O(n)`

The live lists hold every token at most once across the stack of unfinished subtrees, plus the recursion itself.

#### Key Insights

- One traversal replaces three: parsing, simplifying, and serializing collapse into the recursion's unwind.
- Representing subtrees as token lists makes the fold rules read like the statement: a list of length one holding digits is an integer, otherwise it is an expression.
- The economy has a price: a fold that keeps its operator copies its children, so an unfoldable left-deep chain pays quadratic copying where the tree version pays none.
- `fold` never mutates its inputs, so returning a child's list when an identity fires shares it safely.

### Iterative Right-to-Left Stack Folding

#### Derivation

Both earlier versions recurse, and the recursion follows the tree height: with up to 10000 tokens, a left-deep chain bottoms out near 5000 frames, past Python's default recursion limit. The repair changes the reading direction. Read the tokens right to left and every subtree is complete before its operator arrives, so a completed subtree can be pushed as a finished value and folded on the spot, with an explicit list standing in for the call stack.

1. Walk `reversed(preorder)`. A leaf pushes its own one-token list.
2. An operator pops the top entry as its left subtree and the next entry as its
   right subtree, because the left subtree finished last in a right-to-left walk.
3. `fold` applies the same rules as before and the result is pushed back.
4. One entry remains; it is the simplified sequence in prefix order, ready for the join.

#### Walkthrough

Example 1, `preorder = ["+","*","x","1","0"]`, reads right to left as `0`, `1`, `x`, `*`, `+`:

```text
read "0"   push ["0"]                      stack = [["0"]]
read "1"   push ["1"]                      stack = [["0"], ["1"]]
read "x"   push ["x"]                      stack = [["0"], ["1"], ["x"]]
read "*"   pop left ["x"], pop right ["1"]
           x * 1 = x applies -> push ["x"]  stack = [["0"], ["x"]]
read "+"   pop left ["x"], pop right ["0"]
           x + 0 = x applies -> push ["x"]  stack = [["x"]]
```

Both folds fired inside the loop, so the single remaining entry joins directly to `"x"`, the expected Output. (Example 2 runs the same way and returns `"* 5 y"`.)

#### Solution

The code is the reversed walk from the walkthrough, sharing the same `fold`.

```python
from typing import List

OPERATORS = {"+", "-", "*"}


def is_integer_token(token: str) -> bool:
    if token in OPERATORS:
        return False
    digits = token[1:] if token.startswith("-") else token
    return digits.isdigit()


def fold(operator: str, left_tokens: List[str], right_tokens: List[str]) -> List[str]:
    left_is_integer = len(left_tokens) == 1 and is_integer_token(left_tokens[0])
    right_is_integer = len(right_tokens) == 1 and is_integer_token(right_tokens[0])
    if left_is_integer and right_is_integer:
        left_value, right_value = int(left_tokens[0]), int(right_tokens[0])
        if operator == "+":
            return [str(left_value + right_value)]
        if operator == "-":
            return [str(left_value - right_value)]
        return [str(left_value * right_value)]
    if operator == "+" and right_tokens == ["0"]:
        return left_tokens
    if operator == "+" and left_tokens == ["0"]:
        return right_tokens
    if operator == "-" and right_tokens == ["0"]:
        return left_tokens
    if operator == "*" and left_tokens == ["1"]:
        return right_tokens
    if operator == "*" and right_tokens == ["1"]:
        return left_tokens
    if operator == "*" and right_tokens == ["0"]:
        return ["0"]
    return [operator] + left_tokens + right_tokens


class Solution:
    def solve(self, preorder: List[str]) -> str:
        stack: List[List[str]] = []
        for token in reversed(preorder):
            if token not in OPERATORS:
                stack.append([token])
                continue
            left_tokens = stack.pop()
            right_tokens = stack.pop()
            stack.append(fold(token, left_tokens, right_tokens))
        return " ".join(stack.pop())
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Reading is one pass over the tokens. As in the recursive fold, a fold that keeps its operator copies its children, so the honest total is `O(n × h)` with `h` the tree height.

##### Space Complexity: `O(n)`

The stack holds each token in exactly one entry, and no call stack exists at all.

#### Key Insights

- Reading prefix right to left turns "operator waiting for operands" into "operands already on the stack", the same trick that makes postfix (RPN) evaluation a one-liner.
- Pop order matters: the left subtree finished last, so the first pop is the left child and the second is the right child; swapping them silently flips every subtraction.
- The explicit list removes the recursion-depth hazard that the constraint sizes make real, at no asymptotic cost.
- Entries are never mutated after being pushed, so `fold` returning a child's list when an identity fires is safe.

## Comparison of Solutions

### Time Complexity

- **Explicit Tree with Post-Order Folding**: `O(n)` - one read, one simplify visit, and one serialize append per token, with no copying.
- **Recursive Descent with Inline Folding**: `O(n × h)` - one pass to read, plus list concatenation that copies each token once per unfolded ancestor.
- **Iterative Right-to-Left Stack Folding**: `O(n × h)` - the same fold and the same copying bound, reached without recursion.

### Space Complexity

- **Explicit Tree with Post-Order Folding**: `O(n)` - one node per token plus recursion along the tree height.
- **Recursive Descent with Inline Folding**: `O(n)` - the unfinished subtrees hold each token at most once, plus the recursion.
- **Iterative Right-to-Left Stack Folding**: `O(n)` - the explicit stack holds each token once and no call stack exists.

### Trade-offs

- **Explicit Tree with Post-Order Folding**: the asymptotic leader and the closest mirror of the statement's own wording, but the most code and the same recursion-depth exposure as the inline version.
- **Recursive Descent with Inline Folding**: the shortest from-scratch expression of the idea, at the cost of list copying on unfoldable chains and a call stack that can overflow on deep trees.
- **Iterative Right-to-Left Stack Folding**: the only version with no recursion, which matters at the 10000-token cap, while keeping the copying bound of the inline fold.

### When to Use Each

- **Explicit Tree with Post-Order Folding (Recommended)**: the default interview answer: it demonstrates the parse, the fold, and the serialize as three legible steps.
- **Recursive Descent with Inline Folding**: when asked to minimize passes or object churn and the inputs are known to stay shallow.
- **Iterative Right-to-Left Stack Folding**: when the input size or shape makes recursion depth a real risk, or when the interviewer asks for the postfix-style evaluation.

### Optimization Notes

- Every version tests the both-children-integer fold before the identities, so `0 + 0` folds arithmetically instead of matching an identity first.
- The identity list is applied exactly as stated: `x * 0 = 0` is in it and `0 * x` is not, so `0 * y` survives as `0 * y`. Implementing unlisted symmetric identities changes the output on inputs the grader may include.
- `is_integer_token` inspects the digits directly rather than calling `int` in a `try` block, which keeps the operator `-` from being misread as a negative sign.
- The explicit tree serializes into one shared list via `serialize(node, tokens)`; concatenating child lists there instead would quietly add the same per-ancestor copying the folded variants carry.
