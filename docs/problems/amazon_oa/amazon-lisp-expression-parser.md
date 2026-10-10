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

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
