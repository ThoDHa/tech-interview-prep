# [Basic Calculator](https://leetcode.com/problems/basic-calculator/)

**Hard** | **40 minutes** | **Stack**

**Pattern:** [Stack](../patterns/stack/intuition.md)

**Algorithm:** [Stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) · [Recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science))

**Practice:** [`practice/basic_calculator/solution.py`](../../practice/basic_calculator/solution.py)

Given a string `s` representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.

**Note:** You are **not** allowed to use any built-in function which evaluates strings as mathematical expressions, such as `eval()`.

## Examples

### Example 1

**Input:** `s = "1 + 1"`

**Output:** `2`

### Example 2

**Input:** `s = " 2-1 + 2 "`

**Output:** `3`

### Example 3

**Input:** `s = "(1+(4+5+2)-3)+(6+8)"`

**Output:** `23`

## Constraints

- `1 <= s.length <= 3 * 10^5`
- `s` consists of digits, `'+'`, `'-'`, `'('`, `')'`, and `' '`.
- `s` represents a valid expression.
- `'+'` is **not** used as a unary operation (i.e., `"+1"` and `"+(2 + 3)"` is invalid).
- `'-'` could be used as a unary operation (i.e., `"-1"` and `"-(2 + 3)"` is valid).
- There will be no two consecutive operators in the input.
- Every number and running calculation will fit in a signed 32-bit integer.

## Deriving the Solution

The grammar has only `+`, `-`, digits, parentheses, and spaces: no `*` or `/`, so there is no operator precedence. A parenthesis-free expression therefore evaluates left to right with nothing but a running total and a pending sign, and the whole problem reduces to one question: what do we do when a `(...)` group interrupts that flat scan?

1. **Start literal.** Make the groups disappear: repeatedly evaluate an
   innermost `(...)`, splice its numeric value back into the string, and repeat until the expression is flat. Each splice rewrites the string, so `O(n)` groups cost `O(n^2)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Rewriting the string re-reads characters that were
   already parsed. A group does not need to be substituted back into the text; the outer computation only needs to be *suspended* while the group is evaluated and *resumed* afterward.
3. **Suspend and resume.** Scan once, left to right. On `(`, push the outer
   `result` and pending `sign` onto a stack and start fresh; on `)`, fold the group's value back into the popped context. One pass, `O(n)`: see [Stack](#stack).
4. **Shrink the saved state.** The outer partial sum never needs saving at
   all: if every term's sign is resolved eagerly (the group's sign multiplied into each local `+`/`-`), a single flat `result` can keep accumulating across parentheses, and the stack carries only one sign per level: see [Stack of Signs](#stack-of-signs).
5. **Let the call stack do it.** Suspend-and-resume is exactly what a function
   call does, so a `(` can instead trigger a recursive call that returns the group's value as if it were one parsed number. Same single pass, with the grammar made explicit: see [Recursive Descent](#recursive-descent).

## Solutions

### Brute Force

#### Derivation

The most direct idea ignores any clever sign bookkeeping: just keep evaluating the innermost parentheses by hand until none remain, then evaluate the leftover flat `+`/`-` expression. A flat expression with no parentheses is trivial to evaluate left to right, so the only real work is peeling parentheses off one group at a time.

The last `(` in the string always begins an innermost group: there can be no other `(` between it and its matching `)`, so its matching paren is simply the next `)` that follows. We evaluate that group's flat contents, substitute the number back into the string, and repeat.

1. Remove all spaces so positions are easy to reason about.
2. While the string still contains `(`, locate the last `(` and the first `)`
   after it; the substring between them is an innermost, paren-free group.
3. Evaluate that group with the flat helper and splice its value back into the
   string in place of the whole `(...)`.
4. When no parentheses remain, evaluate the final flat string and return it.

The flat helper folds digits into a running `number`. On each `+` or `-` it commits the previous term (only if a number was actually read), then folds the operator into the running `sign` by multiplication. Folding rather than overwriting is what keeps collapsed negatives correct: a group like `-(2)` rewrites the string to `1--2`, and the doubled `-` multiplies the sign back to positive, so `1 - (-2) = 3`. A leading unary `-` (such as a collapsed `-3`) works the same way, since no term is committed before the first digit.

#### Walkthrough

Example 1 (`"1 + 1"`) has no parentheses, so it skips the whole point of this approach. Trace Example 3 instead: `s = "(1+(4+5+2)-3)+(6+8)"`, expected output `23`.

After `s.replace(' ', '')` the string is already space-free: `"(1+(4+5+2)-3)+(6+8)"`. Now the `while '(' in s` loop collapses the innermost group (the one opened by the last `(`) one at a time. Each row shows the chosen group and the string after splicing its value back in:

| Step | `rfind('(')` | matching `)` | inner group | `_eval_flat` value | string after splice |
|------|--------------|--------------|-------------|--------------------|---------------------|
| 0 | `14` | `18` | `"6+8"` | `14` | `"(1+(4+5+2)-3)+14"` |
| 1 | `3` | `9` | `"4+5+2"` | `11` | `"(1+11-3)+14"` |
| 2 | `0` | `7` | `"1+11-3"` | `9` | `"9+14"` |

The string now contains no `(`, so the loop ends. One final `_eval_flat("9+14")` runs the sign-tracking scan: read `9` (`number = 9`), hit `+` so commit `result = 9` and reset, read `14` (`number = 14`), then flush at the end with `result + sign * number = 9 + 1 * 14 = 23`.

The returned value is `23`, which matches the expected Output.

#### Solution

The code is the collapse loop from the walkthrough plus the `_eval_flat` sign-tracking scan it calls on each group.

```python
class Solution:
    def calculate(self, s: str) -> int:
        # Strip spaces once so index math is simple
        s = s.replace(' ', '')

        # Repeatedly collapse the innermost parenthesized group into a number,
        # rewriting the string, until no parentheses are left.
        while '(' in s:
            # Find the last '(' (its matching ')' is the next ')' after it),
            # which is guaranteed to be an innermost group with no nesting.
            open_idx = s.rfind('(')
            close_idx = s.find(')', open_idx)
            inner = s[open_idx + 1:close_idx]
            value = self._eval_flat(inner)
            # Splice the computed value back in place of "(...)".
            s = s[:open_idx] + str(value) + s[close_idx + 1:]

        return self._eval_flat(s)

    def _eval_flat(self, expr: str) -> int:
        # Evaluate an expression of digits, '+', and '-'. A collapsed group can
        # leave a unary or doubled sign (e.g. "1-(-2)" rewrites to "1--2"), so
        # signs are folded by multiplication rather than overwritten.
        result = 0
        number = 0
        sign = 1
        have_number = False
        for char in expr:
            if char.isdigit():
                number = number * 10 + int(char)
                have_number = True
            else:  # char is '+' or '-'
                # Commit the previous term, if one was read, then start fresh.
                if have_number:
                    result += sign * number
                    number = 0
                    sign = 1
                    have_number = False
                # Fold this operator into the running sign.
                if char == '-':
                    sign = -sign
        # Flush the final term (an empty expr leaves result at 0)
        return result + sign * number
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each parenthesis-collapsing step rebuilds the string with slicing, which costs `O(n)`, and there can be `O(n)` groups, giving `O(n^2)` in the worst case. The repeated `rfind`/`find` scans add to the same quadratic bound.

##### Space Complexity: `O(n)`

Each rewrite allocates a fresh string of length up to `n`, and the flat helper uses only a constant number of scalars.

#### Key Insights

- The last `(` always opens an innermost group, so its match is just the next
  `)`: no stack is needed to find the pair.
- Collapsing `(...)` to a literal number reduces the problem to evaluating a flat
  expression, which any beginner can do with a single sign-tracking scan.
- Correct but wasteful: rewriting the whole string per group is the obvious cost
  the later single-pass approaches eliminate.

### Stack

#### Derivation

The Brute Force pays quadratic time only because it writes each group's value back into the string. The value does not need to go back into the text: when a `(` appears, the outer computation is merely *paused*, and everything it will need later is two values, its partial `result` and the `sign` that stood before the group. Save those on a [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)), evaluate the group as a fresh flat expression, and on `)` fold the group's value into the restored context. With no multiplication or division there is no precedence to respect, so this single left-to-right pass is all the machinery the problem needs.

We track three running values: `result` (the sum so far at the current level), `sign` (the `+1`/`-1` to apply to the next number), and `number` (the digits of the integer currently being read):

1. Scan each character of `s`.
2. For a digit, fold it into `number` with `number * 10 + int(char)`.
3. For `+` or `-`, commit the pending number with `result += sign * number`,
   reset `number`, and set `sign` to `+1` or `-1` for what comes next.
4. For `(`, push `result` and `sign` onto the stack, then reset them to `0` and
   `+1` to evaluate the inner expression independently.
5. For `)`, commit the pending number, multiply `result` by the saved `sign`
   (which may be `-1` for a unary-minus group), then add back the saved outer `result`.
6. Ignore spaces.
7. After the loop, commit the last pending number and return `result`.

Unary minus is handled naturally: `-(2 + 3)` reads `-` (setting `sign = -1`), then `(` pushes that `-1`. When `)` is hit, multiplying the inner result by the popped `-1` negates the whole group.

#### Walkthrough

Let us run the single pass by hand on Example 3: `s = "(1+(4+5+2)-3)+(6+8)"`, expected output `23`. Each line shows the state after one character is processed; `stack` holds the saved `(result, sign)` pairs, pushed as two entries:

```text
'('   result=0   sign=+1  number=0  stack=[0, 1]        push outer context, start fresh
'1'   result=0   sign=+1  number=1  stack=[0, 1]
'+'   result=1   sign=+1  number=0  stack=[0, 1]        commit 1
'('   result=0   sign=+1  number=0  stack=[0, 1, 1, 1]  push (result=1, sign=+1)
'4'   result=0   sign=+1  number=4  stack=[0, 1, 1, 1]
'+'   result=4   sign=+1  number=0  stack=[0, 1, 1, 1]  commit 4
'5'   result=4   sign=+1  number=5  stack=[0, 1, 1, 1]
'+'   result=9   sign=+1  number=0  stack=[0, 1, 1, 1]  commit 5
'2'   result=9   sign=+1  number=2  stack=[0, 1, 1, 1]
')'   result=12  sign=+1  number=0  stack=[0, 1]        commit 2 -> 11; *1, +1 -> 12
'-'   result=12  sign=-1  number=0  stack=[0, 1]        next term negated
'3'   result=12  sign=-1  number=3  stack=[0, 1]
')'   result=9   sign=-1  number=0  stack=[]            commit -3 -> 9; *1, +0 -> 9
'+'   result=9   sign=+1  number=0  stack=[]
'('   result=0   sign=+1  number=0  stack=[9, 1]        push (result=9, sign=+1)
'6'   result=0   sign=+1  number=6  stack=[9, 1]
'+'   result=6   sign=+1  number=0  stack=[9, 1]        commit 6
'8'   result=6   sign=+1  number=8  stack=[9, 1]
')'   result=23  sign=+1  number=0  stack=[]            commit 8 -> 14; *1, +9 -> 23
```

Each `)` performs three moves visible in its annotation: commit the pending number, multiply by the popped group sign, then add the popped outer `result`. After the last character the stack is empty and nothing is pending, so the final flush `result + sign * number = 23 + 1 * 0` returns `23`, matching the expected Output.

#### Solution

The code is the walkthrough's scan written down: one branch per character class, with `(` and `)` doing the push and the restore.

```python
class Solution:
    def calculate(self, s: str) -> int:
        result = 0       # Running total of the current parenthesis level
        sign = 1         # Sign to apply to the next number (+1 or -1)
        number = 0       # Digits accumulated for the number being parsed
        stack = []       # Saves (result, sign) when entering a sub-expression

        for char in s:
            if char.isdigit():
                # Build multi-digit numbers left to right
                number = number * 10 + int(char)
            elif char == '+':
                result += sign * number
                number = 0
                sign = 1
            elif char == '-':
                result += sign * number
                number = 0
                sign = -1
            elif char == '(':
                # Push the context and start the sub-expression fresh
                stack.append(result)
                stack.append(sign)
                result = 0
                sign = 1
            elif char == ')':
                # Finish the current number inside the parentheses
                result += sign * number
                number = 0
                # Apply the sign that preceded '(' to the whole group,
                # then add the result computed before '('
                result *= stack.pop()
                result += stack.pop()
            # Spaces are simply ignored

        # Flush the final number after the loop ends
        return result + sign * number
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is processed exactly once with constant work, where `n` is the length of `s`.

##### Space Complexity: `O(n)`

The stack grows with the depth of nested parentheses, which in the worst case (deeply nested expression) is `O(n)`.

#### Key Insights

- With no multiplication or division, the expression evaluates flatly left to
  right; the stack is needed only to suspend and resume across parentheses.
- Pushing `(result, sign)` and resetting captures exactly the state needed to
  resume the outer computation after the group closes.
- Multiplying the inner result by the saved sign is what makes unary minus on a
  parenthesized group fall out for free.
- Building numbers with `number * 10 + digit` cleanly handles multi-digit
  operands without slicing the string.

### Stack of Signs

#### Derivation

The Stack approach saves the outer partial sum on every `(` only to add it back on the matching `)`. That round trip is avoidable: instead of suspending the outer sum, distribute each group's sign down into the terms it contains. Every term then joins one single flat running `result` with its fully resolved sign, and nothing needs to be restored when a parenthesis closes.

The trick is the `signs` [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)), which holds the multiplier that applies to the current parenthesis level. When `(` is reached, the sign currently in front of the group is pushed; every operator inside then combines the group's sign with the local `+`/`-`. Because the sign is resolved eagerly, the expression never needs to remember an outer partial sum.

1. Keep `signs[-1]` as the sign that multiplies the current level (start at `+1`).
2. For a digit, fold it into `number`.
3. For `+`, commit the pending number, then set `sign` to `signs[-1]` so the next
   term carries the group's sign.
4. For `-`, commit the pending number, then set `sign` to `-signs[-1]` so the
   next term is negated relative to the group.
5. For `(`, push the current `sign` as the new level's multiplier.
6. For `)`, commit the pending number, pop the level, and restore `sign` to the
   parent's multiplier.
7. Ignore spaces; after the loop, commit the last number.

A leading `-` before a group sets `sign = -1`, which is pushed on `(`, so every term inside is negated relative to the parent: exactly the unary-minus behavior.

#### Walkthrough

No official Example places a `-` in front of a parenthesized group, which is precisely the mechanism this stack exists to handle, so we use a small tailored input: `s = "5-(2+(3-4))"`. By hand, `5 - (2 + (3 - 4)) = 5 - (2 - 1) = 4`. Each line shows the state after one character:

```text
'5'   result=0  sign=+1  number=5  signs=[1]
'-'   result=5  sign=-1  number=0  signs=[1]            commit 5; next term negated
'('   result=5  sign=-1  number=0  signs=[1, -1]        group inherits the -1
'2'   result=5  sign=-1  number=2  signs=[1, -1]
'+'   result=3  sign=-1  number=0  signs=[1, -1]        commit -2; '+' keeps level sign -1
'('   result=3  sign=-1  number=0  signs=[1, -1, -1]    inner group inherits -1
'3'   result=3  sign=-1  number=3  signs=[1, -1, -1]
'-'   result=0  sign=+1  number=0  signs=[1, -1, -1]    commit -3; '-' flips -1 to +1
'4'   result=0  sign=+1  number=4  signs=[1, -1, -1]
')'   result=4  sign=-1  number=0  signs=[1, -1]        commit +4; pop back to -1
')'   result=4  sign=+1  number=0  signs=[1]            nothing pending; pop to +1
```

The interesting beat is the `-` before `4`: the local minus combines with the level sign `-1` to give `sign = +1`, so the `4` inside two enclosing minuses enters `result` as `+4`. That is the distribution `-(3 - 4) = -3 + 4` happening term by term. The `)` characters only pop the level; no partial sum is ever restored. The final flush `result + sign * number = 4 + 1 * 0` returns `4`, matching the hand computation.

#### Solution

The code is the walkthrough's scan with the `signs` stack supplying the level multiplier that `+` and `-` fold into `sign`.

```python
class Solution:
    def calculate(self, s: str) -> int:
        result = 0       # Running total across the whole expression
        number = 0       # Digits accumulated for the number being parsed
        sign = 1         # Effective sign to apply to the next number
        signs = [1]      # Sign that multiplies the current parenthesis level

        for char in s:
            if char.isdigit():
                number = number * 10 + int(char)
            elif char == '+':
                result += sign * number
                number = 0
                sign = signs[-1]
            elif char == '-':
                result += sign * number
                number = 0
                sign = -signs[-1]
            elif char == '(':
                # The whole group inherits the sign in front of it
                signs.append(sign)
                sign = signs[-1]
            elif char == ')':
                result += sign * number
                number = 0
                signs.pop()
                sign = signs[-1]
            # Spaces are simply ignored

        return result + sign * number
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is processed once with constant work, where `n` is the length of `s`.

##### Space Complexity: `O(n)`

The `signs` stack grows with the nesting depth of parentheses, which is `O(n)` in the worst case.

#### Key Insights

- Pushing only a single integer (the level's sign) instead of `(result, sign)`
  keeps the running total flat and avoids reconstructing partial sums.
- Resolving each term's sign eagerly means the algorithm never has to "return"
  to an outer computation, only restore which sign currently applies.
- This is a clean reformulation: same `O(n)` cost, but the stack carries less
  state per frame.

### Recursive Descent

#### Derivation

The Stack approach hand-implements suspend-and-resume, but suspending one computation to run another is exactly what a function call already does. So let the grammar drive the structure: an expression is a sequence of signed terms, and a term is either a number or a parenthesized expression. A shared index `self.i` walks the string while `_parse` evaluates one parenthesis level and returns when it hits the matching `)` or the end of the string.

When `_parse` encounters `(`, it calls itself to evaluate the inner expression. The [recursive call](https://en.wikipedia.org/wiki/Recursion_(computer_science)) advances the shared index past the matching `)` and returns that group's value, which is treated exactly like a freshly parsed number and folded in with the current `sign`.

1. `calculate` stores the string, resets the index, and calls `_parse`.
2. `_parse` reads characters, building numbers and tracking `sign`, just like the
   flat scan.
3. On `(`, recurse into `_parse`; the returned value becomes the current
   `number`, picking up the pending `sign`.
4. On `)`, stop and return the level's `result` plus the trailing number.
5. The shared index guarantees each character is consumed exactly once across all
   recursive calls.

Unary minus works because a `-` before `(` sets `sign = -1`, and the recursive call's return value is then multiplied by that `sign` when committed.

#### Walkthrough

Let us run the recursion by hand on Example 3: `s = "(1+(4+5+2)-3)+(6+8)"`, expected output `23`. The trace below indents one level per `_parse` call; each call keeps its own `result`, `sign`, and `number` while `self.i` marches through the string exactly once:

```text
_parse()                              top level
  '(' -> recurse
  _parse()                            group "1+(4+5+2)-3"
    '1' number=1; '+' commit -> result=1, sign=+1
    '(' -> recurse
    _parse()                          group "4+5+2"
      '4'; '+' commit -> result=4
      '5'; '+' commit -> result=9
      '2' number=2
      ')' -> return 9 + 1*2 = 11
    number=11
    '-' commit -> result=1+11=12, sign=-1
    '3' number=3
    ')' -> return 12 + (-1)*3 = 9
  number=9
  '+' commit -> result=9, sign=+1
  '(' -> recurse
  _parse()                            group "6+8"
    '6'; '+' commit -> result=6
    '8' number=8
    ')' -> return 6 + 1*8 = 14
  number=14
  end of string -> return 9 + 1*14 = 23
```

Each recursive call returns its group's value (`11`, then `9`, then `14`), and the caller drops that value into `number` as if it had just been parsed from digits. The top-level call ends when the string runs out and returns `result + sign * number = 9 + 1 * 14 = 23`, matching the expected Output.

#### Solution

The code is the walkthrough's call tree written down: the flat scan, with `(` replaced by a recursive call whose return value becomes `number`.

```python
class Solution:
    def calculate(self, s: str) -> int:
        self.s = s
        self.i = 0
        return self._parse()

    def _parse(self) -> int:
        result = 0
        sign = 1
        number = 0
        while self.i < len(self.s):
            char = self.s[self.i]
            self.i += 1
            if char.isdigit():
                number = number * 10 + int(char)
            elif char == '+':
                result += sign * number
                number = 0
                sign = 1
            elif char == '-':
                result += sign * number
                number = 0
                sign = -1
            elif char == '(':
                # The parenthesized sub-expression evaluates to a single number
                number = self._parse()
            elif char == ')':
                break
            # Spaces are simply ignored
        return result + sign * number
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The shared index advances monotonically, so every character is read exactly once across all recursive calls.

##### Space Complexity: `O(n)`

Recursion depth equals the maximum parenthesis nesting, which is `O(n)` in the worst case; this consumes call-stack space rather than an explicit stack.

#### Key Insights

- A shared mutable index lets recursion replace the explicit stack while still
  touching each character once.
- Treating a parenthesized group's return value as just another number keeps the
  per-level logic identical to the flat left-to-right scan.
- The recursion structure makes the grammar explicit, which can be easier to
  extend if precedence (for example `*` and `/`) is added later.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - rewrites the whole string for each of up to `O(n)` parenthesized groups.
- **Stack**: `O(n)` - single pass, constant work per character.
- **Stack of Signs**: `O(n)` - single pass, constant work per character.
- **Recursive Descent**: `O(n)` - shared index reads each character once.

### Space Complexity

- **Brute Force**: `O(n)` - each rewrite allocates a fresh string up to length `n`.
- **Stack**: `O(n)` - pushes two values per nesting level.
- **Stack of Signs**: `O(n)` - pushes one sign per nesting level.
- **Recursive Descent**: `O(n)` - call-stack depth equals nesting depth.

### Trade-offs

- **Brute Force** is the most intuitive model (collapse innermost parentheses,
  then evaluate a flat expression) but rewrites the string per group, paying quadratic time for that simplicity.
- **Stack** stores a full snapshot `(result, sign)` per level, which is the most
  literal "save and restore the context" model and the easiest single-pass model to reason about first.
- **Stack of Signs** stores only a single integer per level by resolving each
  term's sign eagerly; it keeps the running total flat at the cost of a slightly less obvious sign bookkeeping.
- **Recursive Descent** trades the explicit stack for the call stack, making the
  grammar explicit and extensible but risking recursion-depth limits on pathologically nested input.

### When to Use Each

- **Brute Force**: As a first instinct or teaching baseline; avoid it on large
  inputs because the per-group string rewriting makes it quadratic.
- **Stack**: The default and clearest choice; reach for it first in an interview.
- **Stack of Signs**: When you want to minimize per-frame state or articulate the
  insight that only the group's sign needs preserving.
- **Recursive Descent**: When the parser may grow to handle operator precedence,
  where a grammar-driven structure pays off (Recommended for extensibility).

### Optimization Notes

- The three single-pass approaches are all optimal at `O(n)` time; the
  differences are in clarity and how much state each parenthesis level carries. The Brute Force trades that linear bound away for the simplest mental model.
- The iterative stack approaches avoid Python's recursion-depth ceiling, which
  matters because `s` can be up to `3 * 10^5` characters with deep nesting.
- Building numbers with `number * 10 + int(char)` avoids string slicing and keeps
  the scan allocation-free per character.
