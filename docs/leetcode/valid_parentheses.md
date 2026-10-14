# [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

**Easy** | **20 minutes** | **Stack, String**

**Pattern:** [Stack](../patterns/stack/intuition.md)

**Algorithm:** [Stack (abstract data type)](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) · [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/valid_parentheses/solution.py`](../../practice/valid_parentheses/solution.py)

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:

- Open brackets must be closed by the same type of brackets.
- Open brackets must be closed in the correct order.
- Every close bracket has a corresponding open bracket of the same type.

## Examples

### Example 1

**Input:** `s = "()"`

**Output:** `true`

### Example 2

**Input:** `s = "()[]{}"`

**Output:** `true`

### Example 3

**Input:** `s = "(]"`

**Output:** `false`

### Example 4

**Input:** `s = "([])"`

**Output:** `true`

## Constraints

- `1 <= s.length <= 10^4`
- `s` consists of parentheses only `'('`, `')'`, `'{'`, `'}'`, `'['`, `']'`.

## Deriving the Solution

The validity rules boil down to one ordering fact: a closing bracket must match the most recently opened bracket that is still unclosed. "Most recently opened, first closed" is Last-In-First-Out, and the data structure whose whole job is LIFO is the stack.

1. **Model the rule directly.** Push each opener as it appears; on each closer,
   the top of the stack must be its matching opener, popped on the spot. One pass, `O(n)`: see [Stack](#stack).
2. **Make the pairing data instead of code.** The first version spells out
   every closer-opener pair in an `if`/`elif` ladder. A small map from closer to opener replaces the ladder with one lookup, and membership in the map doubles as the open-versus-close test: see [Stack with Hash Map](#stack-with-hash-map).
3. **A different literal reading.** A valid string can also be dissolved from
   the inside out: repeatedly delete the innermost matched pairs `"()"`, `"[]"`, `"{}"` until nothing changes; valid strings vanish entirely. Short to write, but each round rescans the whole string (`O(n^2)`) and the core matching hides inside `str.replace`, so it ranks last: see [Iterative Replacement](#iterative-replacement).

## Solutions

### Stack

#### Derivation

Brackets must close in last-opened, first-closed order, which is exactly the behaviour of a [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)). The most direct idea is to push each opening bracket as it appears, then on a closing bracket check that the most recently opened bracket is its matching opener:

1. Walk the string one character at a time.
2. On an opening bracket, push that bracket onto the stack.
3. On a closing bracket, it is valid only if the stack is non-empty and its top is
   the matching opener. Pop and compare; on any mismatch (or an empty stack) the string is invalid, so return `False`.
4. After the loop, the string is valid only if the stack is empty, meaning every
   opening bracket was matched.

Each closing bracket spells out its own opener inline, so the logic stays explicit without any lookup table.

#### Walkthrough

Example 1 (`"()"`) is only two characters, so it barely exercises the stack. To see the Last-In-First-Out matching clearly, this trace uses Example 4, `s = "([])"`, whose nesting forces two pushes before any pop. `stack` starts empty as `[]`, and we read `s` one `char` at a time:

| Step | `char` | Branch taken | `stack` after |
|------|--------|--------------|---------------|
| 1 | `(` | opener: push `(` | `['(']` |
| 2 | `[` | opener: push `[` | `['(', '[']` |
| 3 | `]` | closer: top is `[`, matches, so pop | `['(']` |
| 4 | `)` | closer: top is `(`, matches, so pop | `[]` |

At step 3 the most recently opened bracket is `[`, exactly the opener that `]` must close, so `stack.pop()` returns `[` and the comparison passes. The same holds at step 4 for `(` and `)`. The loop ends with an empty `stack`, so `not stack` is `True`.

The function returns `True`, which matches the expected Output for Example 4.

#### Solution

The code is the walkthrough's push-and-match loop, with one `elif` arm per closing bracket.

```python
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []

        for char in s:
            if char == "(" or char == "[" or char == "{":
                stack.append(char)
            elif char == ")":
                if not stack or stack.pop() != "(":
                    return False
            elif char == "]":
                if not stack or stack.pop() != "[":
                    return False
            elif char == "}":
                if not stack or stack.pop() != "{":
                    return False

        return not stack
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is visited once, and the push, pop, and comparison operations are all `O(1)`, where `n` is the length of `s`.

##### Space Complexity: `O(n)`

In the worst case (a string of only opening brackets such as `"(((("`) every character is pushed, so the stack grows to size `n`.

#### Key Insights

- A stack models the Last-In-First-Out matching order brackets require.
- Storing the raw opener and comparing it on close handles the "right type" and
  "right order" rules together: the top of the stack is always the only opener that may legally be closed next.
- The final emptiness check catches unclosed openers like `"(("`, while the
  empty-stack guard inside the loop catches stray closers like `")"`.

### Stack with Hash Map

#### Derivation

The stack mechanics above are right, but the `if`/`elif` ladder repeats the same pop-and-compare three times with the pairing hard-coded into control flow. The pairing is data, so store it as data: a [hash map](https://en.wikipedia.org/wiki/Hash_table) from each closing bracket to its opening counterpart collapses the ladder into one lookup, and being a key in the map is itself the test for "is this a closer?":

1. Build a map `pairs` so that `pairs[")"] == "("` and so on.
2. Walk the string. If a character is a key in `pairs`, it is a closing bracket;
   otherwise it is an opening bracket.
3. For an opening bracket, push it onto the stack.
4. For a closing bracket, verify the stack is non-empty and its top equals the
   expected opener `pairs[char]`. If so, pop; otherwise return `False`.
5. Return `True` only when the stack is empty at the end.

Membership in `pairs` doubles as the open-versus-close test, so no separate set of opening brackets is needed.

#### Walkthrough

Let us run the lookup-driven loop on Example 2, `s = "()[]{}"`, which exercises all three bracket types and both branches of the `in pairs` test:

```text
char '('   not in pairs -> push          stack = ['(']
char ')'   in pairs, stack[-1] '(' == pairs[')'] -> pop   stack = []
char '['   not in pairs -> push          stack = ['[']
char ']'   in pairs, stack[-1] '[' == pairs[']'] -> pop   stack = []
char '{'   not in pairs -> push          stack = ['{']
char '}'   in pairs, stack[-1] '{' == pairs['}'] -> pop   stack = []
```

Three independent pairs open and close in sequence, and the stack never holds more than one element. The loop ends with `stack` empty, so the function returns `True`, matching the expected Output for Example 2. On Example 3 (`"(]"`), the second character hits the other outcome: `]` is in `pairs`, but `stack[-1]` is `'('` while `pairs["]"]` is `'['`, so the mismatch returns `False` immediately.

#### Solution

The code is the walkthrough's loop with the pairing table `pairs` standing in for the ladder of `elif` arms.

```python
class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []

        for char in s:
            if char in pairs:
                if not stack or stack[-1] != pairs[char]:
                    return False
                stack.pop()
            else:
                stack.append(char)

        return not stack
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every character drives one pass through the loop, and dictionary lookups, pushes, and pops are each `O(1)`.

##### Space Complexity: `O(n)`

The stack can hold up to `n` opening brackets. The `pairs` map is fixed-size, so it contributes only `O(1)`.

#### Key Insights

- Using the closing bracket as the dictionary key lets the `in pairs` check
  classify characters as opening or closing without a second collection.
- Inspecting `stack[-1]` before popping keeps the empty-stack case explicit.
- The logic is the textbook form most interviewers expect to see.

### Iterative Replacement

#### Derivation

Reading the rules another way: in a valid string there is always at least one innermost pair, two adjacent characters forming `"()"`, `"[]"`, or `"{}"`. Deleting it exposes the pair that surrounded it, so repeating the deletion peels the string from the inside out, and a valid string peels down to nothing:

1. While the string still contains `"()"`, `"[]"`, or `"{}"`, delete every
   occurrence of all three.
2. Each round removes the currently innermost pairs, exposing the pairs that
   surrounded them for the next round.
3. When no matched pair remains, the string is valid if and only if it is empty.

This leans on `str.replace` to do the core matching work, which is why it is listed after the from-scratch stack solutions despite its brevity.

#### Walkthrough

Let us peel Example 4 by hand: `s = "([])"`. Each round runs all three replacements and keeps only what survives:

```text
round 1   "([])"  contains "[]"  -> delete it   s = "()"
round 2   "()"    contains "()"  -> delete it   s = ""
loop ends: no pair remains in ""
```

Round 1 removes the innermost `"[]"`, which is exactly what exposes the outer `(` and `)` as an adjacent pair for round 2. The peeling leaves the empty string, so `s == ""` is `True`, matching the expected Output for Example 4. An invalid string stalls instead: `"(]"` contains none of the three patterns, so the loop never runs and `"(]" == ""` is `False`.

#### Solution

The code is the walkthrough's peeling loop, three deletions per round.

```python
class Solution:
    def isValid(self, s: str) -> bool:
        while "()" in s or "[]" in s or "{}" in s:
            s = s.replace("()", "").replace("[]", "").replace("{}", "")
        return s == ""
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each `replace` scan is `O(n)`, and a deeply nested string such as `"(((...)))"` removes only the innermost layer per round, requiring up to `O(n)` rounds.

##### Space Complexity: `O(n)`

Strings are immutable, so every `replace` builds a new string of size up to `n`.

#### Key Insights

- Deleting matched pairs is an intuitive restatement of the validity rules and is
  easy to reason about.
- It avoids an explicit stack but pays for it with repeated full-string rescans.
- Practical only for short inputs; the quadratic behaviour makes it unsuitable for
  the `10^4`-length upper bound.

## Comparison of Solutions

### Time Complexity

- **Stack**: `O(n)` - one pass with constant-time stack operations.
- **Stack with Hash Map**: `O(n)` - one pass with constant-time lookups.
- **Iterative Replacement**: `O(n^2)` - up to `O(n)` full-string scans.

### Space Complexity

- **Stack**: `O(n)` - the stack can hold every opening bracket.
- **Stack with Hash Map**: `O(n)` - same stack, plus an `O(1)` map.
- **Iterative Replacement**: `O(n)` - each rebuilt string is up to length `n`.

### Trade-offs

- **Stack** is the most direct single-pass solution and needs no auxiliary map, at
  the cost of an `if`/`elif` ladder that spells out each opener-closer pair inline.
- **Stack with Hash Map** trades that ladder for a readable lookup table, which
  scales naturally if more bracket types were ever added.
- **Iterative Replacement** is the shortest to write but the slowest, and it hides
  the matching logic inside `str.replace`.

### When to Use Each

- **Stack**: The default choice for an interview; fast, in-place, and explicit.
- **Stack with Hash Map**: When you want the clearest mapping between closers and
  openers, or anticipate more bracket types.
- **Iterative Replacement**: Only for tiny inputs or a quick sanity check where
  performance does not matter.

### Optimization Notes

- The **Stack** approach avoids a dictionary lookup per character by hard-coding
  each opener-closer pair in the `if`/`elif` ladder; a variant that pushes the expected closer instead of the opener would fuse the type and order checks into a single equality test.
- An optional early `return False` when `len(s)` is odd skips the whole scan for
  inputs that cannot possibly balance.
- Both stack solutions short-circuit on the first mismatch, so invalid strings are
  often rejected well before the end.
