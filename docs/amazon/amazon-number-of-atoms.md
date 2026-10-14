# [Number of Atoms](https://www.fastprep.io/problems/amazon-number-of-atoms)

**Hard** | **NN minutes** | **String, Stack, Hash Table, Parsing, Sorting**

You are given a valid chemical formula string. Return the count of each atom as one canonical string.

An atom name starts with an uppercase letter and may be followed by lowercase letters. A number after an atom or a parenthesized group multiplies that atom or group. If no number follows, the multiplier is 1. Parentheses may be nested.

The output must list atom names in lexicographic order. For each atom, write the atom name followed by its count only when the count is greater than 1.

## Examples

### Example 1

**Input:** `formula = "H2O"`

**Output:** `"H2O"`

**Explanation:** There are two hydrogen atoms and one oxygen atom. The count for oxygen is omitted because it is 1.

### Example 2

**Input:** `formula = "Mg(OH)2"`

**Output:** `"H2MgO2"`

**Explanation:** The group (OH) is multiplied by 2, so the total counts are H:2, Mg:1, and O:2. Atom names are emitted in lexicographic order.

## Constraints

- `The formula is valid and contains atom names, positive integer multipliers, and parentheses.`
- `Parentheses may be nested.`

## Solutions

### Recursive Descent Parsing

#### Derivation

The formula is a nested structure by definition: a parenthesized group behaves like a single unit that happens to contain several atoms, and groups contain groups. The most literal reading is grammatical, so recursion mirrors the nesting one-to-one. A segment is a sequence of units; a unit is an atom with an optional count, or a parenthesized segment followed by an optional count:

1. `parse_segment(formula, position)` reads units until the string ends or a `)` appears, and returns the segment's `counts` together with the position it stopped at.
2. An atom: walk past the uppercase letter and any lowercase letters to get `atom_name`, then `read_number` returns the count (1 when no digits follow) and the updated `position`; add it into `counts`.
3. A group: recurse with `parse_segment(formula, position + 1)` to get `group_counts` and `close_position`, then `read_number` from `close_position + 1` yields the group's `multiplier`; merge every entry of `group_counts`, times `multiplier`, into `counts`.
4. `read_number` returns `1` when the run of digits is empty, which encodes the "no number means 1" rule in exactly one place.
5. After the top-level segment returns, `format_counts` walks `sorted(counts)` and appends each atom name, plus its count only when the count exceeds 1.

#### Walkthrough

Example 2, `formula = "Mg(OH)2"`, exercises the atom rule, the group rule, and the multiplier merge in seven characters:

```text
parse_segment(0)  'M' starts an atom: name "Mg", no digits -> counts = {Mg: 1}
parse_segment(2)  '(' -> recurse into the group at position 3
  inner segment   'O' -> {O: 1}, then 'H' -> {O: 1, H: 1}, stops at ')' (position 5)
  back in outer   close_position = 5, read_number from 6 -> multiplier 2
                  merge {O: 1, H: 1} times 2 -> counts = {H: 2, Mg: 1, O: 2}
parse_segment(0)  back at position 7 = end of string -> return {H: 2, Mg: 1, O: 2}
format_counts     sorted names H, Mg, O -> "H2" + "Mg" + "O2" = "H2MgO2"
```

The merged counter holds exactly the totals from the example's Explanation, and `format_counts` emits `"H2MgO2"`, the expected Output.

#### Solution

The code is the grammar from the derivation: one recursive segment reader plus two small helpers.

```python
from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple


class Solution:
    def solve(self, formula: str) -> str:
        counts, _ = self.parse_segment(formula, 0)
        return self.format_counts(counts)

    def parse_segment(self, formula: str, position: int) -> Tuple[DefaultDict[str, int], int]:
        counts: DefaultDict[str, int] = defaultdict(int)
        while position < len(formula) and formula[position] != ')':
            if formula[position] == '(':
                group_counts, close_position = self.parse_segment(formula, position + 1)
                multiplier, position = self.read_number(formula, close_position + 1)
                for atom_name, atom_count in group_counts.items():
                    counts[atom_name] += atom_count * multiplier
            else:
                name_end = position + 1
                while name_end < len(formula) and formula[name_end].islower():
                    name_end += 1
                atom_name = formula[position:name_end]
                atom_count, position = self.read_number(formula, name_end)
                counts[atom_name] += atom_count
        return counts, position

    def read_number(self, formula: str, position: int) -> Tuple[int, int]:
        digit_start = position
        while position < len(formula) and formula[position].isdigit():
            position += 1
        if position == digit_start:
            return 1, position
        return int(formula[digit_start:position]), position

    def format_counts(self, counts: Dict[str, int]) -> str:
        pieces: List[str] = []
        for atom_name in sorted(counts):
            pieces.append(atom_name)
            if counts[atom_name] > 1:
                pieces.append(str(counts[atom_name]))
        return ''.join(pieces)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × d + m log m)`

Reading consumes each character once. Each atom occurrence is re-merged once per enclosing group, so the merge work is bounded by the maximum nesting depth `d`; sorting the `m` distinct names for the output adds the logarithmic factor.

##### Space Complexity: `O(n)`

The counter dictionaries along one recursion path total at most `n` entries, and the recursion depth equals the nesting depth.

#### Key Insights

- Treating the formula as a grammar makes the recursion the stack: no explicit bookkeeping is needed to match parentheses.
- Folding "no number means 1" into `read_number` removes a conditional from both call sites.
- The output formatting rule (sort names, omit counts of 1) lives entirely in `format_counts`, so the parser never worries about presentation.

### Stack with Count Dictionaries

#### Derivation

The recursive parser inherits the interpreter's recursion limit: a formula nested hundreds of groups deep means hundreds of call frames. The observation that removes the dependency is that the recursion does only two things at a group boundary: park the outer counts while the inner segment is read, then merge the inner counts back under a multiplier. An explicit [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) of counter dictionaries performs both duties with a plain loop:

1. Start with `stack = [defaultdict(int)]`, the counter for the top level.
2. On `(`, push a fresh counter for the new group.
3. On an atom, parse `atom_name` and its count by hand and add them into `stack[-1]`.
4. On `)`, read the multiplier that follows, pop the group's counter, and merge each entry, times `multiplier`, into the counter now on top.
5. When the loop ends, `format_counts(stack[0])` produces the answer.

#### Walkthrough

Examples 1 and 2 never nest deeper than one level, so to see the stack work we use the tailored formula `formula = "K4(ON(SO3)2)2"` (a classic nested case whose canonical output is `"K4N2O14S4"`). Each line is one loop event; the counter an event writes into is `stack[-1]`:

```text
atom K4     stack[-1] = {K: 4}
(           push -> [{K: 4}, {}]
atom O      stack[-1] = {O: 1}
atom N      stack[-1] = {O: 1, N: 1}
(           push -> [{K: 4}, {O: 1, N: 1}, {}]
atom S      stack[-1] = {S: 1}
atom O3     stack[-1] = {S: 1, O: 3}
)2          pop {S: 1, O: 3}, merge times 2 -> {O: 1, N: 1} grows to {O: 7, N: 1, S: 2}
)2          pop {O: 7, N: 1, S: 2}, merge times 2 -> {K: 4} grows to {K: 4, N: 2, O: 14, S: 4}
```

`format_counts` reads K:4, N:2, O:14, S:4 as `"K4N2O14S4"`, as expected. (For Example 2, the same loop ends with `{H: 2, Mg: 1, O: 2}` and returns `"H2MgO2"`.)

#### Solution

The code is the event loop from the walkthrough: push on `(`, merge-and-pop on `)`, tally on atoms.

```python
from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple


class Solution:
    def solve(self, formula: str) -> str:
        stack: List[DefaultDict[str, int]] = [defaultdict(int)]
        position = 0
        while position < len(formula):
            char = formula[position]
            if char == '(':
                stack.append(defaultdict(int))
                position += 1
            elif char == ')':
                multiplier, position = self.read_number(formula, position + 1)
                group_counts = stack.pop()
                for atom_name, atom_count in group_counts.items():
                    stack[-1][atom_name] += atom_count * multiplier
            else:
                name_end = position + 1
                while name_end < len(formula) and formula[name_end].islower():
                    name_end += 1
                atom_name = formula[position:name_end]
                atom_count, position = self.read_number(formula, name_end)
                stack[-1][atom_name] += atom_count
        return self.format_counts(stack[0])

    def read_number(self, formula: str, position: int) -> Tuple[int, int]:
        digit_start = position
        while position < len(formula) and formula[position].isdigit():
            position += 1
        if position == digit_start:
            return 1, position
        return int(formula[digit_start:position]), position

    def format_counts(self, counts: Dict[str, int]) -> str:
        pieces: List[str] = []
        for atom_name in sorted(counts):
            pieces.append(atom_name)
            if counts[atom_name] > 1:
                pieces.append(str(counts[atom_name]))
        return ''.join(pieces)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × d + m log m)`

The same work as the recursive version, the same merges without call frames; each group close merges its popped counter once per entry.

##### Space Complexity: `O(n)`

One counter per open group sits on the stack, which is bounded by the nesting depth.

#### Key Insights

- The explicit stack holds exactly the state the recursion held: one counter per open group.
- Merging at pop time with the multiplier that trails the group computes each group's contribution once.
- A single `position` walking the string replaces the recursive descent's return-the-next-position plumbing.

### Stack Parsing with Regex Tokens

#### Derivation

Both versions so far hand-roll the same three-way tokenizer: recognize an uppercase-led name, scan the digits that trail it, and step over parentheses. That recognition is bookkeeping, and one [regular expression](https://docs.python.org/3/library/re.html) expresses it: `([A-Z][a-z]*)(\d*)|(\()|(\))(\d*)` matches an atom with its optional count, a `(`, or a `)` with its optional multiplier. `findall` turns the formula into a token stream and the stack loop from the previous solution consumes tokens instead of characters. The algorithm is unchanged; only the scanning moves into the library:

1. Iterate the five-group tuples that `TOKEN_PATTERN.findall(formula)` yields.
2. An `open_paren` token pushes a fresh counter.
3. A `close_paren` token pops the group's counter, multiplies by `close_digits` (1 when absent), and merges into the new top.
4. Any other token is an atom: add `int(atom_digits or '1')` under `atom_name` into `stack[-1]`.
5. `format_counts(stack[0])` finishes as before.

#### Walkthrough

The same tailored formula `formula = "K4(ON(SO3)2)2"` keeps the token trace comparable with the character trace above. `findall` yields, in order: `K4`, `(`, `O`, `N`, `(`, `S`, `O3`, `)2`, `)2`:

```text
token K4    atom_digits "4" -> stack[-1] = {K: 4}
token (     push -> [{K: 4}, {}]
token O     stack[-1] = {O: 1}
token N     stack[-1] = {O: 1, N: 1}
token (     push -> [{K: 4}, {O: 1, N: 1}, {}]
token S     stack[-1] = {S: 1}
token O3    stack[-1] = {S: 1, O: 3}
token )2    pop {S: 1, O: 3}, times 2 -> {O: 1, N: 1} grows to {O: 7, N: 1, S: 2}
token )2    pop {O: 7, N: 1, S: 2}, times 2 -> {K: 4} grows to {K: 4, N: 2, O: 14, S: 4}
```

Nine tokens, nine events, ending at the same counter and the same output `"K4N2O14S4"` as the character-level loop.

#### Solution

The code is the previous stack loop with the hand-rolled scanner replaced by `findall`.

```python
import re
from collections import defaultdict
from typing import DefaultDict, Dict, List

TOKEN_PATTERN = re.compile(r'([A-Z][a-z]*)(\d*)|(\()|(\))(\d*)')


class Solution:
    def solve(self, formula: str) -> str:
        stack: List[DefaultDict[str, int]] = [defaultdict(int)]
        for atom_name, atom_digits, open_paren, close_paren, close_digits in TOKEN_PATTERN.findall(formula):
            if open_paren:
                stack.append(defaultdict(int))
            elif close_paren:
                multiplier = int(close_digits or '1')
                group_counts = stack.pop()
                for merged_name, merged_count in group_counts.items():
                    stack[-1][merged_name] += merged_count * multiplier
            else:
                stack[-1][atom_name] += int(atom_digits or '1')
        return self.format_counts(stack[0])

    def format_counts(self, counts: Dict[str, int]) -> str:
        pieces: List[str] = []
        for atom_name in sorted(counts):
            pieces.append(atom_name)
            if counts[atom_name] > 1:
                pieces.append(str(counts[atom_name]))
        return ''.join(pieces)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × d + m log m)`

`findall` scans the string in one pass, and the merge and sort work matches the previous solution.

##### Space Complexity: `O(n)`

The materialized token list plus the same counter stack.

#### Key Insights

- The regex replaces only the tokenizer; the counter stack survives intact, the signature of a tidy-up rather than a new algorithm.
- `findall` returns empty strings for non-participating groups, so `int(atom_digits or '1')` handles missing atom counts and missing group multipliers uniformly.
- A module-level compiled pattern keeps the per-call cost to the scan itself and makes the token grammar visible in one line.

## Comparison of Solutions

### Time Complexity

- **Recursive Descent Parsing**: `O(n × d + m log m)` - one reading pass plus once-per-enclosing-group merging and the final sort of `m` distinct names.
- **Stack with Count Dictionaries**: `O(n × d + m log m)` - the same merges driven by an explicit loop instead of call frames.
- **Stack Parsing with Regex Tokens**: `O(n × d + m log m)` - `findall` scans once and the stack loop is unchanged.

### Space Complexity

- **Recursive Descent Parsing**: `O(n)` - counters along the recursion, whose depth tracks the nesting.
- **Stack with Count Dictionaries**: `O(n)` - one counter per open group plus the final counter.
- **Stack Parsing with Regex Tokens**: `O(n)` - the token list plus the same counters.

### Trade-offs

- **Recursive Descent Parsing**: the shortest expression of the grammar reading, but its memory lives on the interpreter call stack.
- **Stack with Count Dictionaries**: immune to the recursion limit and just as fast, at the cost of explicit stack bookkeeping.
- **Stack Parsing with Regex Tokens**: the least code and the most declarative tokenizer, but it asks the reader to trust a pattern instead of visible scanning and it materializes the token list.

### When to Use Each

- **Recursive Descent Parsing (Recommended)**: interviews where the grammar reading earns credit; chemical formulas never nest deep enough to reach the recursion limit.
- **Stack with Count Dictionaries**: when nesting may be pathological or the parser must interleave with other iterative logic.
- **Stack Parsing with Regex Tokens**: when the token grammar may grow (brackets, charges, hydrates) and a pattern absorbs the new shapes without touching the counting loop.

### Optimization Notes

- Every version pushes exactly one counter per group and pops it at the matching `)`, so the working set never exceeds the nesting depth plus the distinct atoms.
- `read_number` returning `1` on an empty digit run is what lets every call site skip its "was there a number?" branch.
- All three sort the distinct names once at the end rather than keeping a sorted structure during parsing; one sort of `m` names is cheaper than maintaining order incrementally.

