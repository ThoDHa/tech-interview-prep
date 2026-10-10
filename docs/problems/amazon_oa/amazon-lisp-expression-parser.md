# [Lisp Expression Parser](https://www.fastprep.io/problems/amazon-lisp-expression-parser)

**Medium** | **NN minutes** | **String, Stack, Parsing**

Source note: The reported task identifies this algorithmic exercise. The executable interface, bounds, deterministic tie rules, and examples are the documented practice contract.

Parse expression as one Lisp-style expression and return the canonical JSON serialization of its syntax tree as a string.

An atom is a nonempty maximal sequence of ASCII letters, digits, underscore, plus, minus, asterisk or slash. Preserve its exact characters and case, including leading zeros and signs.A list consists of an opening parenthesis, zero or more expressions, and a closing parenthesis. Lists may nest.ASCII space, tab, line feed and carriage return separate tokens and may occur before or after the root. Parentheses are standalone tokens even when adjacent to atoms or other parentheses.The input is valid and contains exactly one root expression. Adjacent atoms must be separated by whitespace; parentheses already provide token boundaries.Serialize every atom as a JSON string and every list as a JSON array of its children, preserving their order and nesting. Use commas between children and no whitespace outside quoted atom strings. The allowed atom characters never contain a quote or backslash. An empty list becomes [].

Do not evaluate operators, resolve names, change numeric-looking atoms into numbers, or flatten nested lists. For example, the atom 001 remains the JSON string "001". The function returns the serialized text, not a native nested array.

## Examples

### Example 1

**Input:** `expression = " (add 1 (mul 2 3)) "`

**Output:** `"[\"add\",\"1\",[\"mul\",\"2\",\"3\"]]"`

**Explanation:** The outer list has three children. Its last child is another list. Operator names and numbers are all strings; no multiplication or addition is performed.

### Example 2

**Input:** `expression = "(a (b) ())"`

**Output:** `"[\"a\",[\"b\"],[]]"`

**Explanation:** The nested one-element list and the empty list remain distinct child arrays. Whitespace outside atoms is not part of the canonical output.

## Constraints

- `1 <= expression.length <= 5000.`
- `There are at most 2000 tokens, counting each parenthesis and each atom once.`
- `At most 100 lists are open at the same time.`
- `The expression follows the stated grammar and contains exactly one root.`

## Solutions

### Brute Force

#### Derivation

The most direct reading mirrors the problem's own definition: a list is a parenthesis pair around zero or more expressions, so keep collapsing innermost lists until only the root remains. Validity alone grants the key fact that makes this work without any parsing structure: with balanced parentheses and exactly one root, the last `(` in the token stream always opens an innermost group, so the next `)` after it is its match. Tokenize once, then repeatedly lift that innermost group out and splice its finished child list back into the token stream as a single object:

1. Run `tokenize`, which skips the four whitespace characters and emits every
   remaining chunk: `(`, `)`, or one atom preserved character for character.
2. While the token list still contains `(`, find the last `(` (its matching
   `)` is the first one after it), collect the tokens between them into
   `children`, and replace the whole `(...)` span in the list with the single
   element `children` (a Python list nested inside the token list).
3. Spliced lists are atomic objects, never re-scanned, so when no `(` remains
   the list holds exactly one element: the root, an atom string or a nested
   list.
4. Run `serialize`, which wraps an atom string in quotes and renders a list as
   `[` + children joined by commas + `]`, recursing depth first.

Each collapse rescans the token list to find the last `(` and rebuilds the list when splicing, and there can be as many collapses as there are lists, so the same span is re-walked once per enclosing group. That repeated walking is the waste the next approach removes.

#### Walkthrough

Let us run the collapse loop by hand on Example 1: `expression = " (add 1 (mul 2 3)) "`, expected output `["add","1",["mul","2","3"]]`. Tokenizing skips the two leading and trailing spaces and produces nine tokens; nested list objects are shown in Python list notation inside the token row:

```text
start        ['(', 'add', '1', '(', 'mul', '2', '3', ')', ')']
collapse 1   open_position = 3 (last '('), close_position = 7
             children = ['mul', '2', '3']  (innermost: no '(' between them)
             tokens  -> ['(', 'add', '1', ['mul', '2', '3'], ')']
collapse 2   open_position = 0, close_position = 4
             children = ['add', '1', ['mul', '2', '3']]
             tokens  -> [['add', '1', ['mul', '2', '3']]]
no '(' left  root = ['add', '1', ['mul', '2', '3']]
```

Collapse 2 sees the spliced inner list as one indivisible element: it sits between `open_position = 0` and `close_position = 4` without being reopened. `serialize` then renders the root depth first, wrapping `add`, `1`, `mul`, `2`, `3` in quotes and joining the two levels with commas, which produces `["add","1",["mul","2","3"]]`, matching the expected Output.

#### Solution

The code is the tokenize, collapse, serialize loop from the walkthrough.

```python
from typing import List, Union

SyntaxNode = Union[str, List["SyntaxNode"]]

ATOM_CHARACTERS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_+-*/"
)
WHITESPACE = " \t\n\r"


def tokenize(expression: str) -> List[str]:
    tokens: List[str] = []
    position = 0
    length = len(expression)
    while position < length:
        char = expression[position]
        if char in WHITESPACE:
            position += 1
        elif char in "()":
            tokens.append(char)
            position += 1
        elif char in ATOM_CHARACTERS:
            start = position
            while position < length and expression[position] in ATOM_CHARACTERS:
                position += 1
            tokens.append(expression[start:position])
        else:
            raise ValueError(f"unexpected character {char!r} at position {position}")
    return tokens


def serialize(node: SyntaxNode) -> str:
    if isinstance(node, str):
        return f'"{node}"'
    return "[" + ",".join(serialize(child) for child in node) + "]"


class Solution:
    def parseLispExpression(self, expression: str) -> str:
        tokens: List[str] = tokenize(expression)
        while "(" in tokens:
            open_position = max(
                position for position, token in enumerate(tokens) if token == "("
            )
            close_position = tokens.index(")", open_position)
            children: List[SyntaxNode] = tokens[open_position + 1 : close_position]
            tokens[open_position : close_position + 1] = [children]
        return serialize(tokens[0])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

With `n` the input length, tokenizing is `O(n)`, but each of up to `O(n)` collapse steps rescans the token list to locate the last `(` and rebuilds it with slicing, both linear passes, so the collapses dominate at `O(n^2)`. At the constraint cap of 5000 characters and 2000 tokens this still finishes in well under a second, but the quadratic slope is the obvious target for improvement.

##### Space Complexity: `O(n)`

The token list, the nested child lists it comes to hold, and the output string are all proportional to the input plus one quote per atom and one bracket pair per list, which stays linear.

#### Key Insights

- The last `(` always opens an innermost group, so match pairs are found without any stack or depth counting: the first `)` after the last `(` is always its partner.
- Splicing a finished Python list object back into the token stream (rather than flattened text) is what lets the loop terminate: the object is opaque to every later scan.
- Correct but quadratic: each enclosing group pays a fresh scan of everything inside it, which the single-pass approaches refuse to do.

### Single-Pass Stack

#### Derivation

The Brute Force re-walks the token list once per enclosing group, yet the tokens arrive in order anyway: a scan that is standing at a `)` already holds, somewhere in its working memory, the list that just closed. The repair is to keep that memory organized as a [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) of open lists. A `(` opens a new list, appends it to the innermost open list, and pushes it; an atom joins the innermost open list; a `)` pops, because the innermost open list has just received all of its children. Every token is touched exactly once and no group is ever re-walked:

1. Start `frames` as a one-element stack holding `root`, an empty list, and
   consume `tokens[1:]`: the first token is the root list's opening
   parenthesis, and seeding the frame from it makes `root` itself the
   outermost list. The single-token input (a bare atom as the whole root
   expression) is peeled off before the loop, since it never opens a frame.
2. For each remaining token: on `(`, create `opened`, append it to
   `frames[-1]`, and push it; on `)`, pop `frames`; otherwise append the atom
   to `frames[-1]`.
3. The last token is the root list's closing parenthesis, so it pops `root`
   and empties the stack: the statement's exactly-one-root guarantee turned
   into an end-state check.
4. Return `serialize(root)`.

Pushing the new list at open time (not at close time) is what makes every `)` a pure pop: the closing parenthesis contributes no children of its own, it only ends the innermost list, and an empty list is the degenerate case where the pop happens with nothing ever appended.

#### Walkthrough

Let us push Example 1 through the frames: `expression = " (add 1 (mul 2 3)) "`, expected output `["add","1",["mul","2","3"]]`. Tokenizing skips the two leading and trailing spaces; the root list's opening parenthesis seeds `frames` outside the loop, so the first line below records that seeding and each further line shows one of the remaining tokens, the innermost open list after it is handled, and the stack; `A` is the one non-root list the run creates:

```text
token        innermost open list after   frames after
'('          root = []                   [root]        root list opens, frame seeded
'add'        root = ['add']              [root]
'1'          root = ['add', '1']         [root]
'('          A = []                      [root, A]     root = ['add', '1', A]
'mul'        A = ['mul']                 [root, A]
'2'          A = ['mul', '2']            [root, A]
'3'          A = ['mul', '2', '3']       [root, A]
')'          pop A                       [root]        root = ['add', '1', ['mul', '2', '3']]
')'          pop root                    []            tree complete
```

Each `)` pops the frame its matching `(` pushed, and the last one pops `root` itself, leaving the stack empty: the one-root guarantee visible as an end state. `serialize(root)` renders `["add","1",["mul","2","3"]]`, matching the expected Output for Example 1.

#### Solution

The code is the frames discipline from the walkthrough: the root's opening parenthesis seeds the frame stack, inner `(` tokens append and push, `)` pops, atoms land on the top frame.

```python
from typing import List, Union

SyntaxNode = Union[str, List["SyntaxNode"]]

ATOM_CHARACTERS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_+-*/"
)
WHITESPACE = " \t\n\r"


def tokenize(expression: str) -> List[str]:
    tokens: List[str] = []
    position = 0
    length = len(expression)
    while position < length:
        char = expression[position]
        if char in WHITESPACE:
            position += 1
        elif char in "()":
            tokens.append(char)
            position += 1
        elif char in ATOM_CHARACTERS:
            start = position
            while position < length and expression[position] in ATOM_CHARACTERS:
                position += 1
            tokens.append(expression[start:position])
        else:
            raise ValueError(f"unexpected character {char!r} at position {position}")
    return tokens


def serialize(node: SyntaxNode) -> str:
    if isinstance(node, str):
        return f'"{node}"'
    return "[" + ",".join(serialize(child) for child in node) + "]"


class Solution:
    def parseLispExpression(self, expression: str) -> str:
        tokens: List[str] = tokenize(expression)
        if len(tokens) == 1:
            return serialize(tokens[0])

        root: List[SyntaxNode] = []
        frames: List[List[SyntaxNode]] = [root]
        for token in tokens[1:]:
            if token == "(":
                opened: List[SyntaxNode] = []
                frames[-1].append(opened)
                frames.append(opened)
            elif token == ")":
                frames.pop()
            else:
                frames[-1].append(token)
        return serialize(root)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Tokenizing visits each character once, and the tree build visits each token exactly once with constant work: one append, one pop, or one frame push. Serialization is linear in the output length, which is the input length plus one quote pair per atom, one bracket pair per list, and one comma per child boundary.

##### Space Complexity: `O(n)`

The token list, the tree, the frame stack (at most the maximum nesting depth, capped at 100 by the constraints), and the output string are all linear.

#### Key Insights

- The frame stack holds exactly the lists whose closing parenthesis has not been read, so `frames[-1]` is always the list the next atom belongs to.
- An empty list `()` is the same mechanism with nothing in between: `(` pushes a fresh frame and `)` immediately pops it, which is why Example 2's third child needs no special case.
- Appending the new list to its parent before pushing it is what wires the tree together without any back-pointers: the parent's reference to the child exists from the moment the child opens.

### Recursive Descent

#### Derivation

The [Single-Pass Stack](#single-pass-stack) hand-implements what the grammar says out loud: an expression is either an atom or a parenthesis pair around a sequence of expressions. When the structure is written as a grammar, the natural executor is [recursive descent](https://en.wikipedia.org/wiki/Recursive_descent_parser): one `parse` function that reads one expression and calls itself for each expression it finds nested inside. A shared token list and a `position` carried through return values let every character be consumed exactly once, while the call stack replaces the explicit frame stack:

1. `parse(tokens, position)` inspects the token at `position`.
2. Any token other than `(` is an atom: return it and `position + 1`.
3. On `(`, advance and collect children: loop calling `parse` on the shared
   token list until the token at `position` is `)`, then return the children
   list and `position + 1` to skip the closing parenthesis.
4. The top-level call starts at position `0`; the statement's exactly-one-root
   guarantee means its return value is the whole tree.
5. Return `serialize(root)`.

A bare atom as the entire root expression needs no guard here, unlike the stack build: the top-level `parse` simply takes branch 2 and returns the atom string, which `serialize` quotes.

#### Walkthrough

Let us run the recursion on Example 2: `expression = "(a (b) ())"`, expected output `["a",["b"],[]]`, the case that exercises the empty list. The trace indents one level per `parse` call and annotates the empty-list call, where `parse` meets `)` with no children collected:

```text
parse()                    root group, tokens ['(', 'a', '(', 'b', ')', '(', ')', ')']
  '(' -> open, collect children
  parse() -> 'a'           atom branch, position advances past 'a'
  parse()                  group
    '(' -> open, collect children
    parse() -> 'b'
    ')' -> return ['b']    one child collected
  parse()                  group
    '(' -> open
    ')' -> return []       empty list: closing parenthesis arrives immediately
  ')' -> return ['a', ['b'], []]
```

The third inner call returns `[]` because the loop body never runs: the token right after its `(` is already `)`. The root call assembles its three children in order and returns `['a', ['b'], []]`, which `serialize` renders as `["a",["b"],[]]`, matching the expected Output for Example 2. The whitespace between `)` and `(` never reaches the recursion because tokenization absorbed it.

#### Solution

The code is the call tree from the walkthrough: one `parse` function, the grammar's two branches, with the position threaded through return values.

```python
from typing import List, Tuple, Union

SyntaxNode = Union[str, List["SyntaxNode"]]

ATOM_CHARACTERS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_+-*/"
)
WHITESPACE = " \t\n\r"


def tokenize(expression: str) -> List[str]:
    tokens: List[str] = []
    position = 0
    length = len(expression)
    while position < length:
        char = expression[position]
        if char in WHITESPACE:
            position += 1
        elif char in "()":
            tokens.append(char)
            position += 1
        elif char in ATOM_CHARACTERS:
            start = position
            while position < length and expression[position] in ATOM_CHARACTERS:
                position += 1
            tokens.append(expression[start:position])
        else:
            raise ValueError(f"unexpected character {char!r} at position {position}")
    return tokens


def serialize(node: SyntaxNode) -> str:
    if isinstance(node, str):
        return f'"{node}"'
    return "[" + ",".join(serialize(child) for child in node) + "]"


def parse(tokens: List[str], position: int) -> Tuple[SyntaxNode, int]:
    token = tokens[position]
    if token != "(":
        return token, position + 1

    position += 1
    children: List[SyntaxNode] = []
    while tokens[position] != ")":
        child, position = parse(tokens, position)
        children.append(child)
    return children, position + 1


class Solution:
    def parseLispExpression(self, expression: str) -> str:
        tokens: List[str] = tokenize(expression)
        root, _ = parse(tokens, 0)
        return serialize(root)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Tokenizing is linear, and `parse` consumes exactly one token per call frame entered or loop iteration, since `position` only ever moves forward and is returned by every call; serialization stays linear in the output length.

##### Space Complexity: `O(n)`

The token list, the tree, and the output are linear; the call stack reaches the maximum nesting depth, capped at 100 by the constraints.

#### Key Insights

- The grammar `expression := atom | '(' expression* ')'` maps one branch per line of `parse`, which is why this version reads as a transcription of the statement's definition.
- Threading `position` through return values instead of mutating shared state makes every call self-contained and lets the empty list fall out of the natural loop shape.
- The call stack replaces the explicit frame stack one-to-one: each pending `(` is a pending call, so the two versions build identical trees and differ only in who remembers the open frames.

### Recursive Descent with json.dumps

#### Derivation

The [Recursive Descent](#recursive-descent) solution stacks two separate concerns: building the tree, and rendering it. The statement asks for the canonical JSON serialization, which is precisely what [`json.dumps`](https://docs.python.org/3/library/json.html) produces: strings quoted, lists bracketed, children joined by commas, nested structures recursed depth first. Only the separators need pinning, because `json.dumps` defaults to a space after each comma and the canonical form has none. The rendering is pure bookkeeping, so the standard library takes it over while the parser stays untouched:

1. Keep `tokenize` and `parse` verbatim from Recursive Descent.
2. Delete the hand-rolled `serialize`.
3. Return `json.dumps(root, separators=(",", ":"))`: the compact separators
   remove the default post-comma space, and nothing else needs configuring.
4. The atom alphabet is what makes the substitution exact: it never contains a
   quote or a backslash, so every atom serializes as itself in quotes, with no
   escape sequences to disagree about.

`json.dumps` also accepts the bare-atom root for free: handed the string `"a"`, it returns `"\"a\""`, matching what the deleted `serialize` produced.

#### Walkthrough

No new mechanism is traced here; the run is Recursive Descent's Example 2 trace ending in a library call. The tree built for `expression = "(a (b) ())"` is `['a', ['b'], []]`, and the serializer swap changes only the last step:

```text
root = ['a', ['b'], []]
json.dumps(root, separators=(",", ":"))
  -> '[' + '"a"' + ',' + '[' + '"b"' + ']' + ',' + '[' + ']' + ']'
  -> ["a",["b"],[]]
```

The rendered text is `["a",["b"],[]]`, matching the expected Output for Example 2, byte for byte what the hand-rolled `serialize` returned on the same tree.

#### Solution

The Recursive Descent code with the serializer deleted and one library call in its place.

```python
import json
from typing import List, Tuple, Union

SyntaxNode = Union[str, List["SyntaxNode"]]

ATOM_CHARACTERS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_+-*/"
)
WHITESPACE = " \t\n\r"


def tokenize(expression: str) -> List[str]:
    tokens: List[str] = []
    position = 0
    length = len(expression)
    while position < length:
        char = expression[position]
        if char in WHITESPACE:
            position += 1
        elif char in "()":
            tokens.append(char)
            position += 1
        elif char in ATOM_CHARACTERS:
            start = position
            while position < length and expression[position] in ATOM_CHARACTERS:
                position += 1
            tokens.append(expression[start:position])
        else:
            raise ValueError(f"unexpected character {char!r} at position {position}")
    return tokens


def parse(tokens: List[str], position: int) -> Tuple[SyntaxNode, int]:
    token = tokens[position]
    if token != "(":
        return token, position + 1

    position += 1
    children: List[SyntaxNode] = []
    while tokens[position] != ")":
        child, position = parse(tokens, position)
        children.append(child)
    return children, position + 1


class Solution:
    def parseLispExpression(self, expression: str) -> str:
        tokens: List[str] = tokenize(expression)
        root, _ = parse(tokens, 0)
        return json.dumps(root, separators=(",", ":"))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The parser is unchanged, and `json.dumps` walks the finished tree once, visiting each node and each output character a constant number of times.

##### Space Complexity: `O(n)`

The token list, the tree, the output string, and a recursion depth bounded by the nesting limit.

#### Key Insights

- `separators=(",", ":")` is the whole configuration surface: the default `(", ", ": ")` separators would inject a space after every comma and break the canonical form.
- The substitution is exact, not approximate, because the atom alphabet excludes quotes and backslashes, so JSON escaping can never change an atom's characters.
- Hand-rolling the serializer once (Recursive Descent) and then delegating it (this section) shows precisely which work the library absorbs: the recursion over the tree, not the parse.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - each collapse rescans and reslices the token list, once per list in the input.
- **Single-Pass Stack**: `O(n)` - one tokenize pass, one build pass over the tokens, one serialization pass.
- **Recursive Descent**: `O(n)` - the forward-only position reads each token exactly once across all calls.
- **Recursive Descent with json.dumps**: `O(n)` - identical parse, library walk over the finished tree.

### Space Complexity

- **Brute Force**: `O(n)` - token list, nested child lists, and output, all linear.
- **Single-Pass Stack**: `O(n)` - token list, tree, and output; the frame stack is bounded by the nesting depth.
- **Recursive Descent**: `O(n)` - token list, tree, and output; the call stack is bounded by the nesting depth.
- **Recursive Descent with json.dumps**: `O(n)` - same as Recursive Descent, plus the library's own output buffer.

### Trade-offs

- The Brute Force restates the problem's own recursive definition as a loop and needs no stack discipline, but it re-walks every enclosing group's tokens once per collapse, paying quadratic time for that simplicity.
- The Single-Pass Stack is the most literal repair: it keeps the open lists on a stack so each token is handled once. It handles the bare-atom root with an explicit guard.
- The Recursive Descent makes the grammar executable and handles the bare-atom root without a guard, at the cost of delegating frame memory to the call stack.
- The json.dumps tidy-up deletes the serializer in favor of the standard library, keeping the parser identical; it is the same algorithm with the rendering handed over.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle on small inputs.
- **Single-Pass Stack** (recommended): the default interview answer; one pass, no recursion-depth exposure, and the frame discipline is easy to narrate.
- **Recursive Descent**: when the grammar may grow (operators, quoted atoms with escapes), where a parser per production pays off.
- **Recursive Descent with json.dumps**: the Pythonic form in production code, once the tree-shape contract is settled.

### Optimization Notes

- Tokenizing before parsing is the load-bearing separation: the atom alphabet overlaps the parenthesis characters not at all, but folding the two into one character loop would blur every branch and buy nothing.
- The output is longer than the input (one quote pair per atom, one bracket pair per list, one comma per child boundary), so a bound stated purely in input length understates the serialization cost only by a constant factor, never asymptotically.
- The frame stack and the call stack are the same data under two names; the iterative version is preferred at the constraint cap only because Python's recursion limit is a fixed 1000 while the nesting here is capped at 100, leaving both far inside their limits.
- If quoted atoms ever enter the grammar, `json.dumps` stops being a drop-in (the parser must track escape states), which is the concrete condition that would retire the tidy-up in favor of the hand-rolled serializer.
