# [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)

**Medium** | **25 minutes** | **String, Dynamic Programming, Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md), [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Backtracking](https://en.wikipedia.org/wiki/Backtracking) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming)

**Practice:** [`practice/generate_parentheses/solution.py`](../../practice/generate_parentheses/solution.py)

You are given an integer `n`. Return all well-formed parentheses strings that you can generate with `n` pairs of parentheses.

## Examples

### Example 1

**Input:** `n = 1`

**Output:** `["()"]`

### Example 2

**Input:** `n = 3`

**Output:** `["((()))","(()())","(())()","()(())","()()()"]`

## Constraints

- `1 <= n <= 7`

## Deriving the Solution

Every approach shares one reformulation: a parentheses string is well-formed exactly when no prefix has more `)` than `(` and the whole string ends balanced. Read that condition while building the string character by character and it becomes a pair of local guards, not a finished-string test. Since the answer is exponential in size (Catalan(n) ~ 4^n / n^1.5 strings), the approaches differ only in how many doomed prefixes they build before discovering that.

1. **Start literal.** Every string of length `2 * n` over the two parentheses is
   a candidate: enumerate all `4^n` of them and validate each finished string
   with a running `balance` scan, costing `O(4^n * n)`: see
   [Brute Force](#brute-force).
2. **Spot the waste.** Almost every candidate is doomed long before its last
   character, but the validity scan only runs after the whole string exists: at
   the constraint cap the enumeration still builds every one of its `4^7`
   candidates, even the prefixes a single character already disproves.
3. **Prune during construction.** Track `open_count` and `close_count` while
   building: append `'('` only while `open_count < n`, append `')'` only while
   `close_count < open_count`. Every explored prefix stays extendable to a
   well-formed string, so the tree's leaves are exactly the Catalan(n) answers:
   see [Backtracking](#backtracking).
4. **Reuse overlapping subproblems.** Every well-formed string decomposes
   uniquely as `(a)b` with `a`, `b` well-formed and one fewer pair between them,
   so the answers for `k` pairs compose from the answers for fewer pairs. Build
   `dp[k]` bottom-up instead of searching each string separately: see
   [Bottom-Up DP](#bottom-up-dp).
5. **Let the library enumerate.** The brute force's enumeration loop is the
   [Cartesian product](https://en.wikipedia.org/wiki/Cartesian_product) of `2 * n`
   copies of the alphabet, a standard-library primitive: see
   [Built-in itertools.product](#built-in-itertoolsproduct).

## Solutions

### Brute Force

#### Derivation

The most literal reading of "well-formed": generate every candidate string of length `2 * n` over `('(', ')')`, then check each one with the balance definition. A string is well-formed exactly when a left-to-right scan never sees more `)` than `(` and ends with equal counts.

1. Extend a `prefix` recursively with one of `'('` or `')'` until it reaches
   length `2 * n`.
2. For each finished candidate, scan with `balance`: `+1` for `'('`, `-1` for
   `')'`.
3. Keep the candidate only if `balance` never drops below `0` and ends at `0`.
4. Return the kept list.

Nothing prunes, so the recursion tree has `4^n` leaves regardless of validity; the scan is what decides each one.

#### Walkthrough

Example 1 has `n = 1`, so candidates have length `2` and the product holds `4` strings. The scan is the whole story:

```text
candidate   balance trace   verdict
"(("        1, 2            ends at 2 != 0      -> reject
"()"        1, 0            never < 0, ends 0   -> keep
")("        -1              dropped below 0     -> reject
"))"        -1              dropped below 0     -> reject
```

Three of four candidates fail, and `result` is `["()"]`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's two layers: an enumeration that produces every candidate, and the balance scan that filters it.

```python
from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        def is_balanced(candidate: str) -> bool:
            balance = 0
            for char in candidate:
                balance += 1 if char == "(" else -1
                if balance < 0:
                    return False
            return balance == 0

        result: List[str] = []

        def enumerate_all(prefix: str) -> None:
            if len(prefix) == 2 * n:
                if is_balanced(prefix):
                    result.append(prefix)
                return
            for char in ("(", ")"):
                enumerate_all(prefix + char)

        enumerate_all("")
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(4^n * n)`

The candidate set is `2^(2n) = 4^n` strings, and each is validated by an `O(n)` balance scan. Nothing is rejected early, so every candidate pays the full scan.

##### Space Complexity: `O(4^n / sqrt(n))`

The result holds the Catalan(n) well-formed strings, `Catalan(n) ~ 4^n / n^1.5`; the recursion stack and the strings under construction reach depth `O(n)`.

#### Key Insights

- The balance definition is the problem's core fact: every later approach is a
  way of exploiting it earlier in the construction.
- The scan cannot start until a full string exists, which is where the approach
  wastes its work.
- Simple to derive and hard to get wrong, which is exactly what makes it a good
  baseline for correctness-checking the faster versions.

### Backtracking

#### Derivation

The brute force learns a prefix is doomed only after finishing it, but the balance definition already judges every prefix: well-formedness demands every prefix hold at least as many `'('` as `')'`, so one character can disprove a string no matter what follows. Two count guards turn that observation into a filter applied at construction time. Building depth-first along a single shared `path` buffer, with each append undone on the way back up, keeps only one partial string alive beside the finished results.

1. Carry `open_count` and `close_count` in the recursion and a shared `path`
   list of characters.
2. At `len(path) == 2 * n`, join the `path` and append it to `result`.
3. If `open_count < n`, append `'('`, recurse with `open_count + 1`, and pop.
4. If `close_count < open_count`, append `')'`, recurse with
   `close_count + 1`, and pop.
5. Start from `backtrack(0, 0)` and return `result`.

Both guards compare counts, never strings: `open_count < n` says every `'('` still has a future `')'` available, and `close_count < open_count` says no prefix ever leads with `')'`. Together they keep every explored prefix extendable to a well-formed string, so no branch is wasted and every leaf is an answer.

#### Walkthrough

Trace both guards and both pops on Example 1: `n = 1`. The full tree is small enough to show every event:

```text
backtrack(0, 0)   path = []
  open_count < 1        -> push '('    path = ['(']
  backtrack(1, 0)       path = ['(']
    open_count == 1           -> no '(' branch
    close_count < open_count  -> push ')'    path = ['(', ')']
    backtrack(1, 1)           -> len(path) == 2, record "()"
    pop ')'                   -> path = ['(']
  pop '('               -> path = []
  close_count < open_count is 0 < 0 -> no ')' branch
```

Each push is paired with a pop, so `path` returns to its prior state before the next branch is tried. At the root only the `'('` branch survives the guards, and inside it only the `')'` branch does; the single leaf records `"()"`, matching the expected Output for Example 1. On Example 2 the same tree keeps pruning every doomed prefix and `result` fills in the five well-formed strings in lexicographic order, since `'('` is always tried before `')'`.

#### Solution

The code is the walkthrough's two guards around one shared `path`, with each push undone by a pop.

```python
from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result: List[str] = []
        path: List[str] = []

        def backtrack(open_count: int, close_count: int) -> None:
            if len(path) == 2 * n:
                result.append("".join(path))
                return
            if open_count < n:
                path.append("(")
                backtrack(open_count + 1, close_count)
                path.pop()
            if close_count < open_count:
                path.append(")")
                backtrack(open_count, close_count + 1)
                path.pop()

        backtrack(0, 0)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(4^n / sqrt(n))`

The pruned tree has one leaf per well-formed string, `Catalan(n) ~ 4^n / n^1.5`, and each leaf is joined and copied in `O(n)`; the pruned internal nodes do constant work each and stay within the same bound.

##### Space Complexity: `O(4^n / sqrt(n))`

The result stores all Catalan(n) strings, plus `O(n)` for the recursion stack and the shared `path` buffer.

#### Key Insights

- The two guards are the entire algorithm: pruning with the balance condition
  during construction, not after, removes the `4^n`-leaf enumeration.
- The condition `close_count < open_count` is what keeps prefixes recoverable;
  guarding `')'` with `close_count < n` alone would still build doomed strings.
- Trying `'('` before `')'` emits the answer in lexicographic order for free.
- Accumulating characters in the shared `path` list and joining once at the
  leaf avoids building a fresh string per character.

### Bottom-Up DP

#### Derivation

Backtracking builds each of the Catalan(n) strings in isolation, but the family overlaps: every well-formed string decomposes uniquely as `'(' + a + ')' + b`, where `a` is what sits inside the first `'('` and its matching `')'`, and `b` is everything after. Both `a` and `b` are themselves well-formed, and they hold `k - 1` pairs between them. So the answers for `k` pairs are pure compositions of the answers for fewer pairs, which a bottom-up table computes without ever searching.

1. Let `dp[k]` be every well-formed string of `k` pairs, with `dp[0] = [""]`.
2. For each `k` from `1` to `n`, take each split `i` in `range(k)`.
3. For every `a` in `dp[i]` and every `b` in `dp[k - 1 - i]`, append the
   composition `f"({a}){b}"` to `dp[k]`.
4. Return `dp[n]`.

#### Recurrence

The split is unique because `a` is pinned to the first `'('` and its matching `')'`:

$$ dp[k] = \bigcup_{i=0}^{k-1} \bigl\{\, (\,a\,)\,b \;:\; a \in dp[i],\ b \in dp[k-1-i] \,\bigr\} $$

```text
dp[0] = [""]
dp[k] = every "(" + a + ")" + b
        for i in 0 .. k - 1, a in dp[i], b in dp[k - 1 - i]
```

Uniqueness of the decomposition matters twice over: no well-formed string is produced twice, so `dp[k]` needs no deduplication set, and every well-formed string is produced, since any string's own first parenthesis pair yields its split. The answer is read from `dp[n]`.

#### Walkthrough

The smallest input that shows a composition is `n = 2` (a tailored input; Example 1 collapses to one split and Example 2 lists five finished strings with no intermediate rows). Each `dp[k]` row composes from the rows above it:

```text
dp[0] = [""]
k = 1, i = 0:  a = ""  b = ""   -> "(" + "" + ")" + ""     = "()"
dp[1] = ["()"]
k = 2:
  i = 0:  a = ""    b in dp[1] = ["()"]  -> "()" + "()"  = "()()"
  i = 1:  a = "()"  b = ""               -> "(" + "()" + ")" = "(())"
dp[2] = ["()()", "(())"]
```

Both compositions are well-formed, and the unique split means no string appears twice; `dp[2]` is exactly the answer set for `n = 2`. Running the same table to `k = 3` produces the five strings of Example 2.

#### Solution

The code is the recurrence transcribed: one table pass, four nested loops, one composition.

```python
from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        dp: List[List[str]] = [[] for _ in range(n + 1)]
        dp[0] = [""]

        for k in range(1, n + 1):
            for i in range(k):
                for a in dp[i]:
                    for b in dp[k - 1 - i]:
                        dp[k].append(f"({a}){b}")

        return dp[n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(4^n / sqrt(n))`

Every pair `(a, b)` produces exactly one composition, so the work is one `O(k)` string build per element of each `dp[k]`; summing over the table reaches the same Catalan(n) bound as the backtracking tree with larger constants.

##### Space Complexity: `O(4^n / sqrt(n))`

The table keeps every `dp[k]` for `k <= n`; the character volume of all smaller rows is dominated by the final row's Catalan(n) strings of length `2n`.

#### Key Insights

- The closure decomposition `(a)b` with a unique split is what makes the DP
  correct: unique means complete without duplicates, so no dedup set is needed.
- This is the Dynamic Programming view of the same Catalan structure the
  backtracking tree walks, discovered from the counting side instead of the
  construction side.
- It computes every `dp[k]` up to `n` even though only `dp[n]` is asked, which
  costs constants against backtracking while keeping the same asymptotics.

### Built-in itertools.product

#### Derivation

The Brute Force's enumeration loop over `2 * n` alphabet choices is the [Cartesian product](https://en.wikipedia.org/wiki/Cartesian_product) of `2 * n` copies of `"()"`, which [`itertools.product`](https://docs.python.org/3/library/itertools.html#itertools.product) computes in one call. The balance scan keeps its filtering role; only the hand-written enumeration disappears.

1. Generate every candidate with `product("()", repeat=2 * n)`.
2. Join each tuple into a string.
3. Keep exactly the strings the balance scan accepts.

#### Walkthrough

Here the library call is the technique, so the trace shows what `product` yields for `n = 1` and how the scan filters it:

```text
product("()", repeat=2) yields:
    ('(', '(')   ('(', ')')   (')', '(')   (')', ')')
join    ->  "(("        "()"         ")("         "))"
balance ->  1, 2        1, 0         -1           -1
keep    ->  no          yes          no           no
result = ["()"]
```

`product` yields its tuples rightmost-factor-fastest, like an odometer. The scan keeps only `"()"`, matching the expected Output for Example 1.

#### Solution

The code is the one `product` call with the balance scan as the filter.

```python
from itertools import product
from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        def is_balanced(candidate: str) -> bool:
            balance = 0
            for char in candidate:
                balance += 1 if char == "(" else -1
                if balance < 0:
                    return False
            return balance == 0

        return [s for s in map("".join, product("()", repeat=2 * n)) if is_balanced(s)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(4^n * n)`

`product` enumerates all `4^n` candidates and each is joined and scanned in `O(n)`; the library changes the constant, not the class.

##### Space Complexity: `O(4^n / sqrt(n))`

The result holds the Catalan(n) well-formed strings; the generator holds one candidate at a time.

#### Key Insights

- The shortest expression of the brute force, leaning on the standard library
  for the combinatorial enumeration.
- Filtering with `is_balanced` keeps the correctness argument identical to the
  Brute Force's: only the enumeration mechanism changed.
- Reveals no algorithm; in an interview it serves best as a closing remark
  after the backtracking solution.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(4^n * n)` - enumerates all `4^n` candidates and scans
  each in `O(n)`.
- **Backtracking**: `O(4^n / sqrt(n))` - prunes to the Catalan(n) leaves,
  joining each in `O(n)`.
- **Bottom-Up DP**: `O(4^n / sqrt(n))` - one `O(n)` composition per
  well-formed string, with larger constants.
- **Built-in itertools.product**: `O(4^n * n)` - library-enumerated `4^n`
  candidates, each scanned in `O(n)`.

### Space Complexity

- **Brute Force**: `O(4^n / sqrt(n))` - the Catalan(n) kept strings plus `O(n)`
  construction depth.
- **Backtracking**: `O(4^n / sqrt(n))` - the result plus `O(n)` recursion stack
  and shared `path`.
- **Bottom-Up DP**: `O(4^n / sqrt(n))` - keeps every `dp[k]` row, not just the
  final one.
- **Built-in itertools.product**: `O(4^n / sqrt(n))` - the result; the product
  generator holds one candidate at a time.

### Trade-offs

- **Brute Force**: The clearest correctness argument (enumerate then filter),
  but it builds and scans every doomed candidate in full.
- **Backtracking**: Optimal asymptotics and no wasted prefixes; carries
  recursion and the choose/unchoose discipline.
- **Bottom-Up DP**: The counting-side view with a clean recurrence, but builds
  every smaller table row even when only `dp[n]` is needed.
- **Built-in itertools.product**: Minimal code with identical filtering logic,
  but hides the enumeration entirely.

### When to Use Each

- **Brute Force**: As the derivational baseline and a correctness oracle for
  testing the faster approaches.
- **Backtracking** (recommended): The interview answer; it demonstrates pruned
  construction, the pattern this problem exists to teach.
- **Bottom-Up DP**: When the Catalan recurrence itself is the subject, or when
  answers for every size up to `n` are needed.
- **Built-in itertools.product**: For production snippets where the candidate
  space is known small and brevity matters most.

### Optimization Notes

- Trying `'('` before `')'` in the backtracking tree makes the output come out
  in lexicographic order with no sorting step.
- A separate `close_count < n` guard would be dead code: whenever
  `close_count == n`, the closing appends that preceded it guarantee
  `open_count == n` too, so the length check has already fired; the code
  correctly omits it.
- Buffer-then-join beats per-character concatenation: each `path.append` is
  `O(1)`, and one `"".join(path)` per leaf replaces an `O(n)` string copy per
  character.
- All four approaches pay the output-size bound; no algorithm can beat
  producing Catalan(n) strings of length `2n`.
