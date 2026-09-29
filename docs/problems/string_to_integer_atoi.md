# [String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/)

**Medium** | **30 minutes** | **String**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine)

**Practice:** [`practice/string_to_integer_atoi/solution.py`](../../practice/string_to_integer_atoi/solution.py)

Implement the `myAtoi(string s)` function, which converts a string to a 32-bit signed integer (similar to C/C++'s `atoi` function).

The algorithm for `myAtoi(string s)` is as follows:

1. Read in and ignore any leading whitespace.
2. Check if the next character (if not already at the end of the string) is `'-'` or `'+'`. Read this character in if it is either. This determines if the final result is negative or positive respectively. Assume the result is positive if neither is present.
3. Read in next the characters until the next non-digit character or the end of the input is reached. The rest of the string is ignored.
4. Convert these digits into an integer (i.e. "123" -> 123, "0032" -> 32). If no digits were read, then the integer is 0. Change the sign as necessary (from step 2).
5. If the integer is out of the 32-bit signed integer range `[-2^31, 2^31 - 1]`, then clamp the integer so that it remains in the range. Specifically, integers less than `-2^31` should be clamped to `-2^31`, and integers greater than `2^31 - 1` should be clamped to `2^31 - 1`.
6. Return the integer as the final result.

**Note:**
- Only the space character `' '` is considered a whitespace character.
- Do not ignore any characters other than the leading whitespace or the rest of the string after the digits.

## Examples

### Example 1

**Input:** `s = "42"`

**Output:** `42`

**Explanation:** The underlined characters are what is read in, the caret is the current reader position.

```text
Step 1: "42" (no characters read because there is no leading whitespace)
         ^
Step 2: "42" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "42" (characters "42" are read in)
           ^
```

The parsed integer is 42. Since 42 is in the range `[-2^31, 2^31 - 1]`, the final result is 42.

### Example 2

**Input:** `s = "   -42"`

**Output:** `-42`

**Explanation:**

```text
Step 1: "   -42" (leading whitespace is read and ignored)
            ^
Step 2: "   -42" ('-' is read, so the result should be negative)
             ^
Step 3: "   -42" (characters "42" are read in)
               ^
```

The parsed integer is -42. Since -42 is in the range `[-2^31, 2^31 - 1]`, the final result is -42.

### Example 3

**Input:** `s = "4193 with words"`

**Output:** `4193`

**Explanation:**

```text
Step 1: "4193 with words" (no characters read because there is no leading whitespace)
         ^
Step 2: "4193 with words" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "4193 with words" (characters "4193" are read in; reading stops because the next character is a non-digit)
             ^
```

The parsed integer is 4193. Since 4193 is in the range `[-2^31, 2^31 - 1]`, the final result is 4193.

## Constraints

- `0 <= s.length <= 200`
- `s` consists of English letters (lower-case and upper-case), digits (0-9), `' '`, `'+'`, `'-'`, and `'.'`.

## Deriving the Solution

This is a simulation problem: the six specification steps (skip spaces, read one optional sign, read digits, convert, clamp, return) are the algorithm, and every solution is a different way of organizing the same left-to-right scan.

1. **Start literal.** Implement the steps as four separate phases with the
   simplest possible code: skip spaces, record the sign, collect the digit run into a string, then fold that string into a number by hand with a clamp. Clear, but it buffers an `O(n)` digit substring: see [Brute Force](#brute-force).
2. **Spot the waste.** The digits are collected only to be walked again.
   Folding each digit into `result` the moment it is read removes the buffer, provided overflow is tested before each multiply. That yields the `O(1)` space hand parser: see [Single Pass](#single-pass).
3. **Make the phases explicit.** The phase order lives implicitly in the
   sequence of loops, so every corner case depends on conditionals being ordered correctly. Reformulating the parse as a finite automaton moves the whole grammar into a transition table whose entries can be verified one by one: see [State Machine (DFA)](#state-machine-dfa).
4. **Delegate to the library.** Python can do the conversion itself: keep the
   phases but hand the digit string to `int()`, in [Strip and Parse](#strip-and-parse), or let a regular expression match the whole grammar at once, in [Regular Expression](#regular-expression). Both clamp once at the end instead of guarding every multiply.

## Solutions

### Brute Force

#### Derivation

The most literal way to solve this is to follow the six specification steps as four separate phases, doing each one with the simplest possible code and no library help. Whitespace, sign, and digit collection are handled in order, then the collected digit characters are converted into a number by hand.

1. Skip leading spaces by advancing `i` while the current character is `' '`.
2. Read a single optional `'+'` or `'-'`, recording `sign` and moving past
   it.
3. Walk forward collecting every consecutive digit character into a `digits`
   string, stopping at the first non-digit or the end of input.
4. Fold `digits` into an integer left to right with
   `result * 10 + (ord(ch) - ord('0'))`, clamping to `INT_MAX` or `INT_MIN` the moment the running value leaves the 32-bit range.

#### Walkthrough

Let us watch the Brute Force code run on Example 1: `s = "42"`, so `n = 2`. The expected Output is `42`.

**Phase 1, skip leading spaces:** `i` starts at `0`. `s[0]` is `'4'`, not a space, so the `while` loop never runs. `i` stays `0`.

**Phase 2, read an optional sign:** `s[0]` is `'4'`, which is neither `'+'` nor `'-'`, so the `if` is skipped. `sign` stays `1` and `i` stays `0`.

**Phase 3, collect the digit run:** the `while` loop appends one character per step. This is the heart of the parse, so trace it index by index:

| Step | `i` before | `s[i]` | digit? | `digits` after | `i` after |
|------|-----------|--------|--------|----------------|-----------|
| 1 | `0` | `'4'` | yes | `'4'` | `1` |
| 2 | `1` | `'2'` | yes | `'42'` | `2` |
| 3 | `2` | (end, `i == n`) | loop stops | `'42'` | `2` |

**Phase 4, fold the digits into a number:** `result` starts at `0`, then each character is folded with `result = result * 10 + (ord(ch) - ord('0'))`:

| `ch` | `result` before | `result * 10 + digit` | `result` after |
|------|-----------------|------------------------|----------------|
| `'4'` | `0` | `0 * 10 + 4` | `4` |
| `'2'` | `4` | `4 * 10 + 2` | `42` |

Neither value leaves the 32-bit range, so no clamp fires. The function returns `sign * result`, which is `1 * 42 = 42`. This matches the expected Output `42`.

#### Solution

The code is the four phases from the walkthrough, executed in order.

```python
class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31
        n = len(s)

        # Phase 1: skip leading spaces
        i = 0
        while i < n and s[i] == ' ':
            i += 1

        # Phase 2: read an optional sign
        sign = 1
        if i < n and (s[i] == '+' or s[i] == '-'):
            if s[i] == '-':
                sign = -1
            i += 1

        # Phase 3: collect the run of digit characters
        digits = ''
        while i < n and '0' <= s[i] <= '9':
            digits += s[i]
            i += 1

        # Phase 4: fold the digit characters into a number by hand
        result = 0
        for ch in digits:
            result = result * 10 + (ord(ch) - ord('0'))
            if sign == 1 and result > INT_MAX:
                return INT_MAX
            if sign == -1 and -result < INT_MIN:
                return INT_MIN

        return sign * result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each phase scans forward without ever revisiting a character, so the three scans plus the final fold touch every character a constant number of times.

##### Space Complexity: `O(n)`

The `digits` substring can grow to the length of the input in the worst case, so this version trades constant space for the clarity of separating collection from conversion.

#### Key Insights

- Each phase is mechanically simple in isolation: this mirrors the six numbered steps directly and is the easiest version to derive from the specification.
- The character-to-digit conversion `ord(ch) - ord('0')` is written out by hand, with no `int()` or `isdigit()` doing the work.
- Clamping inside the fold (rather than after) keeps every intermediate value inside the 32-bit range, even for inputs far larger than `2^31`.

### Single Pass

#### Derivation

The brute force's one waste is the intermediate `digits` substring: characters are collected only to be walked a second time. Fuse collection and conversion into one loop, folding each digit into `result` the moment it is read, and the buffer disappears. The price is that overflow can now happen mid-scan, so the test must run *before* each multiply: in plain text the dangerous condition is `result * 10 + digit > INT_MAX`, restated below as a pre-multiply comparison the code can evaluate safely.

1. Skip leading spaces, then read the optional sign exactly as before,
   tracking the position in `index`.
2. For each digit, check overflow before the multiply by comparing `result`
   against `INT_MAX // 10` and the incoming `digit` against `INT_MAX % 10`; clamp to `INT_MAX` or `INT_MIN` by `sign` the instant the guard fires.
3. Otherwise accumulate `result = result * 10 + digit` and advance `index`.
4. Return `sign * result` when the digit run ends.

#### Overflow Condition

Write \(q\) for `INT_MAX // 10` and \(r\) for `INT_MAX % 10`, so that \(\textit{INT\_MAX} = 10q + r\). For \(\textit{INT\_MAX} = 2^{31} - 1\) that is \(q = 214748364\) and \(r = 7\). Appending `digit` to `result` overflows exactly when:

$$ 10 \cdot \textit{result} + \textit{digit} > \textit{INT\_MAX} \iff \textit{result} > q \ \ \text{or} \\
\bigl(\textit{result} = q \ \text{and} \ \textit{digit} > r\bigr) $$

```text
10 * result + digit > INT_MAX
    <=>  result > INT_MAX // 10
         or (result == INT_MAX // 10 and digit > INT_MAX % 10)
    given 0 <= digit <= 9
```

The equivalence uses only \(0 \le \textit{digit} \le 9\). If \(\textit{result} \ge q + 1\) then \(10\,\textit{result} + \textit{digit} \ge 10q + 10 > 10q + r\). If \(\textit{result} \le q - 1\) then \(10\,\textit{result} + \textit{digit} \le 10q - 1 < 10q + r\). Only \(\textit{result} = q\) is left undecided by `result` alone, and there the comparison reduces to `digit` against `r`.

The right-hand side is what the code evaluates, and it must be evaluated *before* the multiply. In a fixed-width 32-bit type the product `result * 10 + digit` is the very value that overflows, so it wraps and a test performed afterwards would be reading a corrupted number. The pre-multiply form compares only `result` (already known to be in range) against a constant and one digit against another, so nothing intermediate can leave the range. Passing the guard establishes \(10\,\textit{result} + \textit{digit} \le \textit{INT\_MAX}\), which carries the invariant \(0 \le \textit{result} \le \textit{INT\_MAX}\) into the next iteration.

Testing against `INT_MAX` stays correct under a negative sign even though the true range \([-2^{31},\ 2^{31} - 1]\) is asymmetric. The guard measures magnitude, so it calls the magnitude \(2^{31}\) an overflow where a negative parse would accept it exactly. The returned verdict is unaffected: the clamp yields `INT_MIN`, and \(-2^{31}\) is precisely the value the exact parse would have produced. Every larger magnitude genuinely exceeds the range and clamps to `INT_MIN` regardless, so a single boundary serves both signs.

#### Walkthrough

None of the official Examples overflows, so the guard never fires on them. To see the clamp we use a tailored input one below the 32-bit floor: `s = "-2147483649"`, which must clamp to `INT_MIN = -2147483648`.

There are no spaces to skip; `s[0]` is `'-'`, so `sign = -1` and `index` moves to `1`. The digit loop then folds one digit per step, checking the guard (`q = INT_MAX // 10 = 214748364`, `r = INT_MAX % 10 = 7`) before each multiply:

```text
digit=2   result 0 -> 2
digit=1   result 2 -> 21
digit=4   result 21 -> 214
digit=7   result 214 -> 2147
digit=4   result 2147 -> 21474
digit=8   result 21474 -> 214748
digit=3   result 214748 -> 2147483
digit=6   result 2147483 -> 21474836
digit=4   result 21474836 -> 214748364    result now equals q
digit=9   result == q and digit 9 > r=7   guard fires -> return INT_MIN
```

The first nine digits pass the guard comfortably (`result < q` before each of them, or exactly `q` only after the ninth fold). The tenth digit lands on the boundary case: `result == q`, so the digit decides, and `9 > 7` means `10 * result + 9` would exceed `INT_MAX`. Since `sign == -1`, the function returns `INT_MIN = -2147483648`, the correct clamp for `-2147483649`.

#### Solution

The code is the fold from the walkthrough with the guard placed before the multiply.

```python
class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        index = 0
        sign = 1
        result = 0

        # Skip leading spaces
        while index < len(s) and s[index] == ' ':
            index += 1

        if index >= len(s):
            return 0

        # Read an optional sign
        if s[index] == '+':
            sign = 1
            index += 1
        elif s[index] == '-':
            sign = -1
            index += 1

        # Accumulate digits, guarding overflow before each multiply
        while index < len(s) and s[index].isdigit():
            digit = ord(s[index]) - ord('0')

            if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > INT_MAX % 10):
                return INT_MAX if sign == 1 else INT_MIN

            result = result * 10 + digit
            index += 1

        return sign * result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is visited at most once across the whitespace, sign, and digit phases.

##### Space Complexity: `O(1)`

The running integer, sign, and index are the only state; no per-digit buffer is built.

#### Key Insights

- Splitting the overflow test into `result > INT_MAX // 10` and the boundary case `result == INT_MAX // 10 and digit > INT_MAX % 10` mirrors how a fixed-width integer would overflow, while keeping every intermediate value inside Python ints that never actually overflow.
- The single shared clamp `INT_MAX if sign == 1 else INT_MIN` works because `2^31 - 1` and `-2^31` are the only two saturation targets, selected purely by the sign captured earlier.
- Folding collection into the accumulation loop removes the brute force's `O(n)` digit substring, the one piece of waste it carried.

### State Machine (DFA)

#### Derivation

The Single Pass is correct, but its phase structure is implicit: skipping, sign reading, and digit accumulation live in the order of its loops, and every corner case rests on conditionals being placed exactly right. This solution reformulates the parse as a **[deterministic finite automaton](https://en.wikipedia.org/wiki/Deterministic_finite_automaton)** (the classic LeetCode editorial framing). Every character of the input belongs to exactly one of four input classes: `space` (the literal `' '`), `sign` (`'+'` or `'-'`), `digit` (`'0'` through `'9'`), or `other` (anything else). The parser itself is always in exactly one of four states, and a fixed transition table maps each (state, input class) pair to the next state:

| State | `space` | `sign` | `digit` | `other` |
|-------|---------|--------|---------|---------|
| `start` | `start` | `sign` | `number` | `end` |
| `sign` | `end` | `end` | `number` | `end` |
| `number` | `end` | `end` | `number` | `end` |
| `end` | `end` | `end` | `end` | `end` |

In words: the automaton begins in `start` and stays there while consuming leading spaces; a sign character moves it to `sign`, a digit moves it to `number`, and anything else moves it to the absorbing `end` state. From `sign` only a digit continues the parse; from `number` only further digits do. Once `end` is reached, nothing can leave it, so the loop simply breaks.

The payoff is that the messy corner cases stop being code at all. A lone sign (`"+"`), a sign after spaces (`"   -"`), a second sign (`"+-12"`), leading letters (`"abc42"`), and trailing junk (`"42abc"`) are not handled by if-chains: each one is just a row-column lookup in the table that happens to land in `end`. The correctness argument shrinks from "did I order my conditionals correctly?" to "is this 16-entry table right?", which can be checked cell by cell against the specification. The same formulation generalizes directly to other parsing problems (Valid Number is the canonical example): define the input classes, draw the states, fill in the table, and the control flow writes itself.

1. Declare the `TRANSITIONS` table above and a `classify` helper mapping each
   character to its input class.
2. For each `ch` in `s`, step with
   `state = TRANSITIONS[state][classify(ch)]`.
3. Attach one action to each state landed in: entering `sign` records the
   sign, entering `number` folds the digit into `result` with the same before-the-multiply overflow guard as the Single Pass (compare against `INT_MAX // 10` and the boundary digit `INT_MAX % 10`, then clamp by sign), and entering `end` breaks the scan.
4. Return `sign * result`.

#### Walkthrough

Let us watch the State Machine code run on the tricky input `s = "   -42abc"`. The expected result is `-42`.

The automaton starts in `state = 'start'` with `sign = 1` and `result = 0`. Each character is classified, the table picks the next state, and the state's action fires:

| Step | `ch` | Input class | State before | State after | Action |
|------|------|-------------|--------------|-------------|--------|
| 1 | `' '` | `space` | `start` | `start` | none (still skipping spaces) |
| 2 | `' '` | `space` | `start` | `start` | none |
| 3 | `' '` | `space` | `start` | `start` | none |
| 4 | `'-'` | `sign` | `start` | `sign` | `sign = -1` |
| 5 | `'4'` | `digit` | `sign` | `number` | `result = 0 * 10 + 4 = 4` |
| 6 | `'2'` | `digit` | `number` | `number` | `result = 4 * 10 + 2 = 42` |
| 7 | `'a'` | `other` | `number` | `end` | `break` |

The `'a'` at step 7 drives the automaton into the absorbing `end` state, so `"bc"` is never examined. No overflow guard fires along the way (`4` and `42` are far below `INT_MAX // 10`). The function returns `sign * result = -1 * 42 = -42`, matching the expected result. Note how the three leading spaces, the sign, and the trailing junk were all handled by the same table lookup that handled the digits: no phase of the input needed its own code path.

#### Solution

The code is the table plus the per-state actions; the loop body never changes across characters.

```python
class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        # Transition table: state -> input class -> next state
        TRANSITIONS = {
            'start':  {'space': 'start', 'sign': 'sign', 'digit': 'number', 'other': 'end'},
            'sign':   {'space': 'end',   'sign': 'end',  'digit': 'number', 'other': 'end'},
            'number': {'space': 'end',   'sign': 'end',  'digit': 'number', 'other': 'end'},
            'end':    {'space': 'end',   'sign': 'end',  'digit': 'end',    'other': 'end'},
        }

        def classify(ch: str) -> str:
            if ch == ' ':
                return 'space'
            if ch == '+' or ch == '-':
                return 'sign'
            if '0' <= ch <= '9':
                return 'digit'
            return 'other'

        state = 'start'
        sign = 1
        result = 0

        for ch in s:
            state = TRANSITIONS[state][classify(ch)]
            if state == 'sign':
                sign = -1 if ch == '-' else 1
            elif state == 'number':
                digit = ord(ch) - ord('0')
                if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > INT_MAX % 10):
                    return INT_MAX if sign == 1 else INT_MIN
                result = result * 10 + digit
            elif state == 'end':
                break

        return sign * result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The loop visits each character exactly once, and each visit does one classification, one table lookup, and one constant-time action.

##### Space Complexity: `O(1)`

The transition table has a fixed 4 x 4 shape regardless of input length, and the only other state is the current state name, the sign, and the running integer.

#### Key Insights

- Table-driven parsing replaces ad hoc conditionals with data: the grammar lives in a 16-entry table you can verify cell by cell, while the loop body stays identical for every character. Adding a new rule means editing the table, not re-threading nested `if` logic.
- The DFA is computationally equivalent to the Single Pass solution: both make one forward scan with `O(1)` state and identical clamping. The difference is purely organizational, with the phase structure made explicit as named states instead of being implicit in the order of loops.
- The absorbing `end` state is what makes trailing junk free: once any invalid character is seen, every subsequent character maps back to `end`, so "ignore the rest of the string" requires no dedicated code path beyond the early `break`.
- Interviewers often like the DFA framing because it demonstrates a transferable technique: the same states-and-table recipe cleanly handles harder parsing problems (Valid Number, tokenizers, protocol decoders) where if-chains become unmanageable.

### Strip and Parse

#### Derivation

Every solution so far converts the digits by hand, but Python's `int()` already parses a digit string, and its arbitrary-precision integers cannot overflow. Keep the explicit phase structure of the manual parser and offload only the final numeric conversion: `lstrip(' ')` drops leading spaces (only the space character, matching the specification), a manual scan reads the sign and collects the digit run, and `int()` plus a single `max`/`min` clamp replace the per-digit overflow arithmetic.

1. Strip leading spaces with `s.lstrip(' ')`; if the string empties, return
   `0`.
2. Read an optional sign at `s[0]`, setting `sign` and the start position
   `position`.
3. Collect consecutive digit characters into `digits`; if none were read,
   return `0`.
4. Convert with `result = sign * int(digits)` and clamp once with
   `max(INT_MIN, min(INT_MAX, result))`.

#### Walkthrough

Let us run Strip and Parse on Example 2: `s = "   -42"`, expected Output `-42`. Each line shows one phase acting:

```text
lstrip(' ')     s = "-42"                 the three leading spaces vanish
s[0] = '-'      sign = -1, position = 1
position=1  '4'      digits = "4",  position = 2
position=2  '2'      digits = "42", position = 3    position == len(s): scan stops
int("42")       result = -1 * 42 = -42
clamp           max(INT_MIN, min(INT_MAX, -42)) = -42
```

The digit scan is the same character walk as the brute force's Phase 3; only the final fold is delegated to `int()`. `-42` sits inside the 32-bit range, so the clamp passes it through unchanged, and the function returns `-42`, matching the expected Output.

#### Solution

The code is the phase list from the walkthrough, with `int()` performing the final fold.

```python
class Solution:
    def myAtoi(self, s: str) -> int:
        """
        Strip leading spaces, scan the sign and digits, then convert
        """
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        s = s.lstrip(' ')
        if not s:
            return 0

        sign = 1
        position = 0
        if s[0] == '-':
            sign = -1
            position = 1
        elif s[0] == '+':
            position = 1

        digits = ''
        while position < len(s) and s[position].isdigit():
            digits += s[position]
            position += 1

        if not digits:
            return 0

        result = sign * int(digits)
        return max(INT_MIN, min(INT_MAX, result))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`lstrip` and the digit scan each run linearly in the string length, and `int()` is linear in the number of digits collected.

##### Space Complexity: `O(n)`

The accumulated `digits` substring can grow to the length of the input in the worst case, unlike the running-integer approaches that use constant space.

#### Key Insights

- Restricting the strip to the literal space character (`lstrip(' ')`) is essential: `str.strip()` with no argument would also remove tabs and newlines, which the specification forbids.
- Building the digit substring lets Python's arbitrary-precision `int()` parse any length safely, so the only overflow handling needed is a final `max`/`min` clamp.
- Returning early when `digits` is empty covers the "sign only" and "leading non-digit" cases without special-casing them.

### Regular Expression

#### Derivation

Strip and Parse still writes the sign and digit scan by hand. The whole grammar (leading whitespace, optional sign, digit run) is regular, so a [regular expression](https://docs.python.org/3/library/re.html) can match it in one step: `^\s*([+-]?\d+)` anchors at the start of the string, consumes whitespace, and captures the signed digit run. `int()` then converts the captured token and a final clamp bounds it.

1. Match with `re.match(r'^\s*([+-]?\d+)', s)`; when there is no match
   (empty string, sign with no digits, leading letters), return `0`.
2. Extract the token `num_str = match.group(1)` and convert with
   `int(num_str)`.
3. Clamp once with `max(INT_MIN, min(INT_MAX, result))`.

#### Walkthrough

Let us run the pattern on Example 3: `s = "4193 with words"`, expected Output `4193`. The regex engine walks the pattern against the string from position `0`:

```text
^          anchors at position 0
\s*        matches zero spaces               position stays 0
[+-]?      matches zero sign characters      position stays 0
\d+        matches '4','1','9','3'           position moves to 4
           ' ' is not a digit: the match ends here
group(1) = "4193"
```

The capture group holds exactly the token the hand parsers would have collected, and `" with words"` is left unmatched, which implements "ignore the rest of the string" for free. `int("4193")` gives `4193`, inside the 32-bit range, so the clamp leaves it unchanged and the function returns `4193`, matching the expected Output.

#### Solution

The code is one match, one conversion, one clamp.

```python
import re

class Solution:
    def myAtoi(self, s: str) -> int:
        """
        Regular expression approach for pattern matching
        """
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        # Regular expression to match the atoi pattern
        # ^ - start of string, \s* - zero or more whitespaces
        # [+-]? - optional sign, \d+ - one or more digits
        match = re.match(r'^\s*([+-]?\d+)', s)

        if not match:
            return 0

        # Extract the matched number string
        num_str = match.group(1)
        result = int(num_str)

        # Clamp to 32-bit signed integer range
        return max(INT_MIN, min(INT_MAX, result))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Regular expression matching is linear in string length, and `int()` conversion is also linear.

##### Space Complexity: `O(1)`

Uses constant extra space (the regex compilation is cached by Python).

#### Key Insights

- The pattern `^\s*([+-]?\d+)` encodes the entire parsing grammar (leading whitespace, optional sign, digit run) in one expression, so `int()` only ever receives a well-formed token.
- A missing match (empty string, sign with no digits, leading letters) returns `None`, which maps directly to the required `0` result.
- One caveat: `\s` matches all whitespace, not just the space character; this is acceptable only because the constraints restrict whitespace in `s` to the space character. A hand-written parser does not depend on that assumption.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - three forward scans plus a digit fold, each linear.
- **Single Pass**: `O(n)` - one pass with explicit overflow handling.
- **State Machine (DFA)**: `O(n)` - one pass with a constant-time table lookup per character.
- **Strip and Parse**: `O(n)` - linear strip and digit scan plus `int()` conversion.
- **Regular Expression**: `O(n)` - pattern matching plus conversion.

### Space Complexity

- **Brute Force**: `O(n)` - accumulates the digit substring before converting it.
- **Single Pass**: `O(1)` - builds the running integer directly with no buffer.
- **State Machine (DFA)**: `O(1)` - the transition table is fixed-size; only the current state and running integer vary.
- **Strip and Parse**: `O(n)` - accumulates the digit substring before conversion.
- **Regular Expression**: `O(1)` - constant space (regex cached).

### Trade-offs

- **Brute Force**: The most directly derivable version, separating the four phases for clarity, and fully library-free (`ord` conversion, no `int()`). It pays `O(n)` space for the intermediate digit substring.
- **Single Pass**: Trims the brute force's digit substring by folding collection into accumulation, reaching `O(1)` space while staying library-free. It is the recommended hand-written form.
- **State Machine (DFA)**: Matches the Single Pass on cost (`O(n)` time, `O(1)` space, library-free) but moves the control flow into a transition table. It is slightly longer to write, and in exchange the corner cases become table entries you can verify individually rather than conditional branches you must order correctly.
- **Strip and Parse**: Keeps explicit phases but leans on `int()` for the conversion and uses `O(n)` space for the digit substring, avoiding manual overflow arithmetic in favor of a final clamp.
- **Regular Expression**: The most concise but the most library-driven: `re` encodes the parsing grammar and `int()` does the conversion, so corner case handling is implicit and it depends on the `re` module.

### When to Use Each

- **Brute Force**: Best for learning the specification step by step with no library help.
- **Single Pass**: The recommended default: `O(1)` space, no dependencies, every parsing state handled explicitly.
- **State Machine (DFA)**: When you want to demonstrate the table-driven formulation, or when the interviewer steers toward generalizable parsing technique (it is the standard editorial answer and scales to problems like Valid Number).
- **Strip and Parse**: When you want explicit phases but prefer to delegate the numeric conversion and overflow clamping to the language.
- **Regular Expression**: When code brevity is prioritized over showing the parsing mechanics.

### Optimization Notes

- The **Single Pass** solution is the recommended choice: it runs in `O(n)` time and `O(1)` space, requires no external dependencies, and handles every parsing state (whitespace, sign, digits, overflow) explicitly.
- Key implementation detail: check for overflow *before* performing the multiplication `result * 10 + digit`. Comparing against `INT_MAX // 10` and `INT_MAX % 10` prevents the intermediate value from exceeding the 32-bit range, then clamp to `INT_MAX` or `INT_MIN` based on the sign.
- The **State Machine (DFA)** solution is not an optimization over the Single Pass (same time, same space, same clamping) but a restructuring: the transition table centralizes the corner case logic, which pays off when the grammar grows more complex than atoi's four states.
- The **Strip and Parse** and **Regular Expression** approaches offload the numeric conversion (and, for the regex, the corner case handling) to Python's `int()`. They are concise but hide the parsing mechanics and depend on the language for overflow-free arithmetic before the final clamp.
- Common pitfall: the many corner cases (empty string, only whitespace, only a sign, non-digit interruptions, and overflow) make this problem tricky; the task tests faithful implementation of an exact specification rather than algorithmic creativity, so each step must follow the stated order precisely.
