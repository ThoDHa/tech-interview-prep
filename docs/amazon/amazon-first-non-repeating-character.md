# [First Non-Repeating Character](https://www.fastprep.io/problems/amazon-first-non-repeating-character)

**Easy** | **NN minutes** | **String, Hash Table**

Given a non-empty string s, return the first character whose total frequency in the string is exactly one.

If no such character exists, return the empty string. Character comparisons are case-sensitive.

## Examples

### Example 1

**Input:** `s = "swiss"`

**Output:** `"w"`

**Explanation:** The first s repeats, while w occurs once.

### Example 2

**Input:** `s = "aabbc"`

**Output:** `"c"`

**Explanation:** Only c has frequency one.

### Example 3

**Input:** `s = "aabb"`

**Output:** `""`

**Explanation:** Every character repeats, so the result is empty.

## Constraints

- `1 ≤ s.length ≤ 100000.`
- `s contains printable ASCII characters.`

## Solutions

### Brute Force Scan

#### Derivation

The most literal reading of the problem is a direct translation into two nested questions: for each character of `s`, in order, does it appear exactly once in the whole string? The first character that answers yes is the answer. Counting "appears in the whole string" is itself a scan, so the literal version counts with `s.count`:

1. Scan `s` left to right with `position` and `character`.
2. For each `character`, ask `s.count(character) == 1`.
3. Return `character` on the first yes; return `""` after the scan finishes.

#### Walkthrough

Example 1, `s = "swiss"`:

```text
position 0  's'  count('s') = 3  not 1 -> continue
position 1  'w'  count('w') = 1  exactly one -> return "w"
```

The scan returns `"w"`, matching the expected Output. For Example 3, `s = "aabb"`, every position's count is `2`, the loop ends without returning, and the function returns `""`.

#### Solution

The code is the walkthrough's per-position count:

```python
class Solution:
    def firstNonRepeating(self, s: str) -> str:
        """Return the first character with total frequency one, else "".

        Time:  O(n^2): each of the n positions triggers a full-string count.
        Space: O(1): only the scan position and the candidate character.
        """
        for character in s:
            if s.count(character) == 1:
                return character
        return ""
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` positions calls `s.count`, which itself scans up to `n` characters.

##### Space Complexity: `O(1)`

Only the loop's current character is held; no auxiliary structure grows with the input.

#### Key Insights

- The brute force is correct and needs no extra memory, which makes it a reasonable first spoken answer.
- Its cost is re-answering the same question: every occurrence of a repeated character triggers another full count of that same character.

### Two-Pass Frequency Table

#### Derivation

The brute force re-counts each character once per occurrence. The repair is to answer "how often does each character appear?" exactly once: walk the string a first time and tally every character into a table, then walk it a second time and return the first character whose tally is `1`. A plain list of 128 counters covers printable ASCII, indexed by `ord(character)`, and the second pass reads the table instead of rescanning the string:

1. Allocate `counts`, a list of 128 zeros.
2. First pass: for each `character`, increment `counts[ord(character)]`.
3. Second pass: for each `character` in order, return it when `counts[ord(character)] == 1`.
4. Return `""` when the second pass finds no unique character.

#### Walkthrough

Example 1, `s = "swiss"`, showing the tally after the first pass and the second pass verdicts:

```text
first pass:  s -> 3, w -> 1, i -> 1
second pass:
position 0  's'  counts[ord('s')] = 3  not 1
position 1  'w'  counts[ord('w')] = 1  exactly one -> return "w"
```

The second pass returns `"w"`, matching the expected Output. For Example 2, `s = "aabbc"`, the tally is `a -> 2, b -> 2, c -> 1`, so the second pass walks past `a` and `b` and returns `"c"`. For Example 3, `s = "aabb"`, every tally is `2` and the function returns `""`.

#### Solution

The code is the two passes over one shared tally:

```python
class Solution:
    def firstNonRepeating(self, s: str) -> str:
        """Return the first character with total frequency one, else "".

        Time:  O(n): two passes over the string with O(1) table work each.
        Space: O(1): the tally has a fixed 128 entries for printable ASCII.
        """
        counts = [0] * 128
        for character in s:
            counts[ord(character)] += 1
        for character in s:
            if counts[ord(character)] == 1:
                return character
        return ""
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two linear passes; each position does one table read or write, both constant time.

##### Space Complexity: `O(1)`

The tally is a fixed 128 integers, independent of `n`.

#### Key Insights

- Counting once and querying many times is the general pattern: the frequency table amortizes the brute force's repeated scans into one.
- The second pass must walk the string, not the table: table order is by character code, while the answer needs first occurrence in `s`.
- A fixed-size array over a bounded alphabet beats a hash map on constants; the 128-entry list is `O(1)` space and avoids hashing entirely.

### Hash Map Tally via Counter

#### Derivation

The 128-entry table hard-codes an alphabet assumption. The same two-pass shape works for any character set if the tally is a dictionary keyed by the character itself, and the standard library already provides the counting loop as [Counter](https://docs.python.org/3/library/collections.html#collections.Counter). The algorithm is unchanged; only the bookkeeping moves to the library. The second pass stays a manual scan because the "first in string order" rule is the core of the problem, not bookkeeping:

1. Build `frequencies = Counter(s)` in one library call.
2. Scan `s` in order; return the first `character` with `frequencies[character] == 1`.
3. Return `""` after the scan.

#### Walkthrough

Example 1, `s = "swiss"`, with the Counter contents made explicit:

```text
frequencies = Counter({'s': 3, 'w': 1})
position 0  's'  frequencies['s'] = 3  not 1
position 1  'w'  frequencies['w'] = 1  exactly one -> return "w"
```

The scan returns `"w"`, matching the expected Output. Example 2's `frequencies` is `Counter({'a': 2, 'b': 2, 'c': 1})`, so the scan returns `"c"`; Example 3's is `Counter({'a': 2, 'b': 2})` and the scan returns `""`.

#### Solution

The code is the same two-pass shape with the tally delegated:

```python
from collections import Counter


class Solution:
    def firstNonRepeating(self, s: str) -> str:
        """Return the first character with total frequency one, else "".

        Time:  O(n): one counting pass and one scanning pass.
        Space: O(k) for the counter, k the number of distinct characters.
        """
        frequencies = Counter(s)
        for character in s:
            if frequencies[character] == 1:
                return character
        return ""
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`Counter` makes one pass; the answer scan makes a second, both linear.

##### Space Complexity: `O(k)`

The counter holds one entry per distinct character; `k` is at most the alphabet size, so it is constant for ASCII input.

#### Key Insights

- `Counter` replaces only the tally loop; deciding "first with count one" remains an explicit string scan, which keeps the algorithm visible.
- Dictionary keys accept any character, so the solution survives alphabets the fixed table does not.
- Reading a missing key from a `Counter` returns `0` rather than raising, though here every key read was written during counting.

### One-Pass Order Map

#### Derivation

Both two-pass versions walk the string twice. A single pass can capture everything needed: for each character, record its first occurrence position when it is new, or mark it repeated when it has been seen before. After the pass, the answer is the minimum first-occurrence position among characters never marked repeated. A dictionary mapping each character to either its first index or a repeated marker carries both facts, and the final minimum is over at most the distinct characters:

1. Allocate `first_position`, an empty dictionary.
2. One pass with `position` over `s`: a character seen for the first time is stored as `position`; a character already present is rewritten to the marker `-1`.
3. Collect every value in `first_position` that is not the marker and take the minimum.
4. Return `s` at that minimum position, or `""` when no entry survives.

#### Walkthrough

Example 1, `s = "swiss"`, one entry per event:

```text
's' new   first_position = {'s': 0}
'w' new   first_position = {'s': 0, 'w': 1}
'i' new   first_position = {'s': 0, 'w': 1, 'i': 2}
's' seen  first_position = {'s': -1, 'w': 1, 'i': 2}
's' seen  first_position = {'s': -1, 'w': 1, 'i': 2}
```

The surviving entries are `w -> 1` and `i -> 2`; the minimum position is `1`, so the function returns `s[1] = "w"`, matching the expected Output. For Example 2, `s = "aabbc"`, the surviving entries are `c -> 4` alone and the return is `"c"`. For Example 3, `s = "aabb"`, every entry is the marker, no minimum exists, and the function returns `""`.

#### Solution

The code is the walkthrough's mark-or-record loop and final minimum:

```python
class Solution:
    def firstNonRepeating(self, s: str) -> str:
        """Return the first character with total frequency one, else "".

        Time:  O(n) for the pass plus O(k) for the minimum over distinct
            characters.
        Space: O(k) for the first-occurrence map.
        """
        REPEATED = -1
        first_position = {}
        for position, character in enumerate(s):
            if character in first_position:
                first_position[character] = REPEATED
            else:
                first_position[character] = position

        unique_positions = [
            position for position in first_position.values() if position != REPEATED
        ]
        if not unique_positions:
            return ""
        return s[min(unique_positions)]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass over the string with constant-time dictionary operations, then a minimum over at most `k` distinct-character entries.

##### Space Complexity: `O(k)`

The map holds one entry per distinct character.

#### Key Insights

- The input string itself is the order index, so remembering first-occurrence positions is enough; there is no need to preserve full frequency counts.
- Rewriting a repeated character's entry to a marker fuses "seen" and "how many" into one cell: only the first occurrence's position survives for unique characters.
- The one-pass property helps when the string arrives as a stream, since a second scan of the input is not required.

### One-Liner with next and a Generator

#### Derivation

After the `Counter` tally exists, the second pass is just "the first element of `s` satisfying a predicate", which is exactly what [next](https://docs.python.org/3/library/functions.html#next) over a generator expression expresses. The algorithm is the Counter variant verbatim; the explicit loop collapses into one expression with a default for the no-match case:

1. Build `Counter(s)`.
2. Ask `next` for the first character of `s` whose count is `1`, defaulting to `""`.

#### Walkthrough

Example 1, `s = "swiss"`: `Counter(s)` is `{'s': 3, 'w': 1}`. The generator offers `s`, `w`, `i`, `s`, `s` in order; `next` takes the first one whose count is `1`, which is `"w"` at position 1, matching the expected Output. Example 3, `s = "aabb"`: no character passes the predicate, the generator is exhausted, and `next` returns its default `""`.

#### Solution

```python
from collections import Counter


class Solution:
    def firstNonRepeating(self, s: str) -> str:
        """Return the first character with total frequency one, else "".

        Time:  O(n): one counting pass and one short-circuiting scan.
        Space: O(k) for the counter.
        """
        frequencies = Counter(s)
        return next((character for character in s if frequencies[character] == 1), "")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The counting pass is linear; `next` scans at most the whole string and stops at the first match.

##### Space Complexity: `O(k)`

The counter is the only structure that grows with the input.

#### Key Insights

- `next` with a default encodes "first match or fallback" without any result bookkeeping.
- The generator is lazy, so the scan short-circuits at the answer exactly like the explicit loop.
- What the one-liner buys in brevity it spends in opacity: the two-pass idea is easier to explain with the loop visible, which is why it ranks last.

## Comparison of Solutions

### Time Complexity

- **Brute Force Scan**: `O(n^2)`: a full-string count per position.
- **Two-Pass Frequency Table**: `O(n)`: two linear passes over a fixed-size tally.
- **Hash Map Tally via Counter**: `O(n)`: one counting pass plus one scanning pass.
- **One-Pass Order Map**: `O(n)`: one string pass plus a minimum over distinct characters.
- **One-Liner with next and a Generator**: `O(n)`: identical work to the Counter variant.

### Space Complexity

- **Brute Force Scan**: `O(1)`: nothing stored.
- **Two-Pass Frequency Table**: `O(1)`: a fixed 128-entry array for printable ASCII.
- **Hash Map Tally via Counter**: `O(k)`: one counter entry per distinct character.
- **One-Pass Order Map**: `O(k)`: one map entry per distinct character.
- **One-Liner with next and a Generator**: `O(k)`: the counter only.

### Trade-offs

- **Brute Force Scan**: zero auxiliary memory and trivially correct, but quadratic time rules it out at the `10^5` constraint.
- **Two-Pass Frequency Table**: the fastest constants and `O(1)` space, but the 128-entry array assumes a bounded alphabet.
- **Hash Map Tally via Counter**: alphabet-independent and idiomatic, at the cost of hashing per character.
- **One-Pass Order Map**: reads the string once, which matters for streams, but the marker convention is subtler than a count.
- **One-Liner with next and a Generator**: the shortest expression of the idea and the least instructive.

### When to Use Each

- **Two-Pass Frequency Table (Recommended)**: the interview default here: linear, `O(1)` space over a stated alphabet, and easy to explain in two sentences.
- **Hash Map Tally via Counter**: when the alphabet is unknown or unbounded, or the interviewer expects idiomatic library use.
- **One-Pass Order Map**: when the input arrives as a stream and a second pass is impossible or expensive.
- **Brute Force Scan**: as the spoken baseline before improving it; also fine for tiny inputs.
- **One-Liner with next and a Generator**: production code where the Counter version is already understood and brevity wins.

### Optimization Notes

- The decisive move from `O(n^2)` to `O(n)` is answering "how many?" once per character instead of once per occurrence; say that sentence in an interview before writing code.
- For this problem's stated alphabet (printable ASCII) the fixed array beats `Counter` on constants; neither changes the asymptotics.
- A common pitfall is scanning the frequency table instead of the string in the second pass: table order is by character code and returns the smallest code, not the first occurring character.
