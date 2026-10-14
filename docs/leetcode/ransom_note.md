# [Ransom Note](https://leetcode.com/problems/ransom-note/)

**Easy** | **15 minutes** | **Hash Table, String, Counting**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/ransom_note/solution.py`](../../practice/ransom_note/solution.py)

Given two strings `ransomNote` and `magazine`, return `true` if `ransomNote` can be constructed from `magazine` and `false` otherwise.

Each letter in `magazine` can only be used once in `ransomNote`.

## Examples

### Example 1

**Input:** `ransomNote = "a"`, `magazine = "b"`

**Output:** `false`

### Example 2

**Input:** `ransomNote = "aa"`, `magazine = "ab"`

**Output:** `false`

### Example 3

**Input:** `ransomNote = "aa"`, `magazine = "aab"`

**Output:** `true`

## Constraints

- `1 <= ransomNote.length, magazine.length <= 10^5`
- `ransomNote` and `magazine` consist of lowercase English letters.

## Deriving the Solution

The note can be built exactly when, for every letter, the magazine contains at least as many copies as the note needs. Every solution below enforces that supply-and-demand rule; they differ in whether the supply is rescanned, counted by hand, or counted by the library.

1. **Start literal.** Simulate cutting letters out: for each note character,
   scan the remaining magazine letters for a copy and remove it. Every character triggers a fresh scan of the pool, costing `O(m * n)`: see [Brute Force](#brute-force).
2. **Count instead of rescanning.** The scans keep re-answering "how many of
   this letter are left?", a question a tally answers in `O(1)`. Count the magazine once into a dictionary, then spend counts per note character, for `O(m + n)`: see [Hash Map](#hash-map).
3. **Exploit the alphabet.** The inputs are lowercase English letters only, so
   the dictionary can shrink to a fixed 26-slot array indexed by letter, trading hashing for direct indexing: see [Array Counter](#array-counter).
4. **Let the library count.** Python's `Counter` builds both tallies in a line
   apiece; it goes last because the standard library is doing the core work: see [Counter](#counter).

## Solutions

### Brute Force

#### Derivation

The most direct idea mirrors the physical act the problem describes: cut each letter out of the magazine. For every character the ransom note needs, scan the remaining magazine letters for a matching copy and remove it so it cannot be reused. No counting structure is involved at all, just repeated [linear search](https://en.wikipedia.org/wiki/Linear_search) over a shrinking pool:

1. Copy the magazine into a list `available` that acts as a pool of usable
   letters.
2. For each character `char` in the ransom note, scan the pool left to right
   for that character.
3. When a match is found, remove it from the pool (`available.pop(i)`) and
   move on to the next ransom-note character.
4. If any character is never found in the remaining pool, the note cannot be
   built, so return `False`.

#### Walkthrough

Let us trace the Brute Force on Example 1: `ransomNote = "a"`, `magazine = "b"`, expected Output `false`.

First we copy the magazine into the pool of available letters: `available = ['b']`.

Now we loop over each character in `ransomNote`. There is only one, `'a'`, so we scan the pool looking for it.

| Outer step | `char` needed | Scan of `available` | Match? | `available` after | Result so far |
| --- | --- | --- | --- | --- | --- |
| 1 | `'a'` | `available[0]` is `'b'`, and `'b' != 'a'` | no | `['b']` (unchanged) | `found` stays `False` |

The inner scan reaches the end of the pool without ever setting `found = True`. Because `not found` is true after the scan, the code immediately runs `return False`.

The returned value is `false`, which matches the example's expected Output. The note needs an `'a'`, the magazine offers only a `'b'`, so the note cannot be constructed.

#### Solution

The code is the scan-and-consume loop from the walkthrough.

```python
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        # Treat the magazine as a pool of letters we can consume one at a time
        available = list(magazine)

        for char in ransomNote:
            found = False
            # Scan the remaining pool for one copy of the needed letter
            for i in range(len(available)):
                if available[i] == char:
                    # Consume it so it can't be reused for another letter
                    available.pop(i)
                    found = True
                    break
            if not found:
                return False

        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

For each of the `n` characters in the ransom note we scan up to `m` magazine letters, and each `pop` shifts the remaining elements. This nested work makes the approach quadratic in the worst case.

##### Space Complexity: `O(m)`

We materialize the magazine as a list of `m` letters that shrinks as we consume them.

#### Key Insights

- This is the literal simulation of cutting letters out of a magazine, so it is the easiest approach to derive without any prior counting trick.
- Consuming each matched letter is what enforces the "each letter used once" rule.
- Its weakness is repeated rescanning: the same pool is swept again for every character, which the frequency-based approaches eliminate.

### Hash Map

#### Derivation

The brute force wastes its time rescanning: every note character sweeps the pool again to answer a question that never needed the pool's order, only its counts. So count once. A [hash map](https://en.wikipedia.org/wiki/Hash_table) tally of the magazine answers "how many of this letter remain?" in `O(1)`, and spending from the tally enforces the use-each-letter-once rule. A length check comes first, since a note longer than the magazine is impossible outright:

1. If `len(ransomNote) > len(magazine)`, return `False` immediately.
2. Build `counter`, mapping each magazine character to its frequency.
3. Iterate through the ransom note; when `counter.get(c, 0) == 0` the needed
   letter is out of stock, so return `False`.
4. Otherwise decrement `counter[c]` to consume one copy, and return `True`
   once every character is paid for.

#### Walkthrough

Let us run Example 3: `ransomNote = "aa"`, `magazine = "aab"`. The length check passes (`2 <= 3`), and the first loop tallies the magazine:

```text
build 'a'   counter = {'a': 1}
build 'a'   counter = {'a': 2}
build 'b'   counter = {'a': 2, 'b': 1}
```

The second loop spends from the tally, one note character at a time:

```text
need 'a'    counter['a'] is 2, not 0 -> spend one   counter = {'a': 1, 'b': 1}
need 'a'    counter['a'] is 1, not 0 -> spend one   counter = {'a': 0, 'b': 1}
```

The loop ends with every character paid for, so the function returns `True`, matching Example 3's expected Output. On Example 2 (`"aa"` from `"ab"`) the tally starts as `{'a': 1, 'b': 1}`: the first `'a'` spends the count down to `0`, the second finds `counter.get('a', 0) == 0`, and the function returns `False`, matching that example as well.

#### Solution

The code is the build-then-spend loop pair from the walkthrough.

```python
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False
        counter = {}

        for c in magazine:
            counter[c] = counter.get(c, 0) + 1

        for c in ransomNote:
            if counter.get(c, 0) == 0:
                return False
            counter[c] -= 1
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

We iterate through the magazine string once (of length m) to build our counter dictionary, and then through the ransom note once (of length n) to check if it can be constructed. All operations inside the loop (dictionary lookups and updates) are `O(1)`.

##### Space Complexity: `O(k)`

Where `k` is the number of unique characters in the magazine. In the worst case, this would be 26 (for lowercase English letters), which is a constant. So effectively, the space complexity is `O(1)`.

#### Key Insights

- The early length check (`len(ransomNote) > len(magazine)`) is a key optimization that avoids unnecessary processing.
- Using a hash map/dictionary provides efficient lookups and updates for character counts.
- The solution efficiently handles arbitrary characters, not just lowercase letters.
- We only need a single pass through each string, making this solution optimal in terms of time complexity.

### Array Counter

#### Derivation

The hash map is more machinery than the constraints require. Every character is a lowercase English letter, so there are only 26 possible keys, and `ord(char) - ord('a')` maps each letter to a slot in a plain 26-element array. That replaces hashing with direct indexing while keeping the same count-then-spend logic:

1. If `len(ransomNote) > len(magazine)`, return `False` immediately.
2. Create `counts`, a fixed array of 26 zeros, and count each magazine
   character with `counts[ord(char) - ord('a')] += 1`.
3. For each ransom-note character, compute its `index`; when
   `counts[index] <= 0` the letter is out of stock, so return `False`.
4. Otherwise decrement `counts[index]`, and return `True` once the note is
   exhausted.

#### Walkthrough

Let us rerun Example 3, `ransomNote = "aa"`, `magazine = "aab"`, on the array. `'a'` maps to index `0` and `'b'` to index `1`; slots `2` through `25` stay at `0` throughout, so the snapshots show only the first three:

```text
build 'a'   counts[0] += 1              counts = [1, 0, 0, ...]
build 'a'   counts[0] += 1              counts = [2, 0, 0, ...]
build 'b'   counts[1] += 1              counts = [2, 1, 0, ...]
spend 'a'   index 0, count 2 > 0        counts = [1, 1, 0, ...]
spend 'a'   index 0, count 1 > 0        counts = [0, 1, 0, ...]
```

Both `'a'`s are paid for and the loop ends, so the function returns `True`, matching Example 3's expected Output. The `'b'` count is never touched: the note did not ask for it.

#### Solution

The code is the same build-then-spend pass over a 26-slot array instead of a dictionary.

```python
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False

        # Array of size 26 for lowercase letters
        counts = [0] * 26

        # Count character occurrences in magazine
        for char in magazine:
            counts[ord(char) - ord('a')] += 1

        # Check if we can construct the ransom note
        for char in ransomNote:
            index = ord(char) - ord('a')
            if counts[index] <= 0:
                return False
            counts[index] -= 1

        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

We make one pass through the magazine string (of length m) to populate our counts array, and one pass through the ransom note (of length n) to check if it can be constructed. Array indexing and updates are `O(1)` operations.

##### Space Complexity: `O(1)`

The solution uses a fixed-size array of 26 elements, regardless of the input size. This is constant space complexity.

#### Key Insights

- Using an array is most memory-efficient when the character set is known and limited.
- Array indexing with `ord(char) - ord('a')` provides a direct mapping from characters to indices.
- This approach avoids hash computation overhead that would be present in dictionary-based solutions.
- For very large inputs, this solution may have better cache locality due to the contiguous memory of arrays.

### Counter

#### Derivation

The hand-rolled tallies are exactly what Python's built-in [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) class produces in one call, so the final step is to let the library count. Instead of spending counts down, this version tallies both strings and compares demand against supply directly:

1. If `len(ransomNote) > len(magazine)`, return `False` immediately.
2. Build `magazine_counts = Counter(magazine)` and
   `ransom_counts = Counter(ransomNote)`.
3. For each `(char, count)` pair the note demands, return `False` when
   `magazine_counts[char] < count`.
4. If no letter falls short, return `True`.

#### Walkthrough

Here `Counter` itself is the technique, so the trace picks up where the library leaves off: on Example 3 (`ransomNote = "aa"`, `magazine = "aab"`) the two constructor calls yield the finished tallies, and the loop compares demand against supply per unique character:

```text
magazine_counts = {'a': 2, 'b': 1}      supply
ransom_counts   = {'a': 2}              demand
char 'a', count 2:   magazine_counts['a'] = 2, and 2 < 2 is False -> covered
```

The only demanded letter is covered, so the loop ends and the function returns `True`, matching Example 3's expected Output. A letter the magazine lacks never raises an error: `Counter` returns `0` for absent keys, so the demand simply fails the `<` test naturally.

#### Solution

The code is the two tallies and the comparison loop from the walkthrough.

```python
from collections import Counter

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False

        magazine_counts = Counter(magazine)
        ransom_counts = Counter(ransomNote)

        for char, count in ransom_counts.items():
            if magazine_counts[char] < count:
                return False

        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

Creating the Counter objects requires one pass through each string (magazine of length m and ransom note of length n). The comparison loop iterates through unique characters in the ransom note, which is at most n iterations.

##### Space Complexity: `O(k)`

We store two Counter objects, each with at most k unique characters (where k ≤ 26 for lowercase English letters). This is effectively `O(1)` space.

#### Key Insights

- Python's Counter class streamlines the process of counting and comparing character frequencies.
- Creating two counters and then comparing them allows for a cleaner, more readable implementation.
- This approach is more declarative than imperative, focusing on what we want (compare frequencies) rather than how to do it.
- Counter objects handle missing keys gracefully, eliminating the need for explicit default value handling.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(m * n)`. Each ransom-note character triggers a fresh scan of the shrinking magazine pool.
- **Hash Map**: `O(m + n)`. One pass through magazine and one through ransom note.
- **Array Counter**: `O(m + n)`. One pass through each string with direct array indexing.
- **Counter**: `O(m + n)`. Same complexity as the hash map approach.

### Space Complexity

- **Brute Force**: `O(m)`. Materializes the magazine as a consumable list of letters.
- **Hash Map**: `O(k)`, where `k` is the number of unique characters (at most 26), effectively `O(1)`.
- **Array Counter**: `O(1)`. Fixed-size array of 26 elements regardless of input size.
- **Counter**: `O(k)`, same as the hash map approach, effectively `O(1)`.

### Trade-offs

- The brute force needs no counting structure and reads as a literal simulation, but its repeated rescanning makes it quadratic.
- The hash map solution works with any character set but carries slight hash table overhead.
- The array solution has the best memory efficiency but is limited to lowercase letters only.
- The Counter solution is most concise and leverages Python's built-in optimizations.

### When to Use Each

- **Brute Force**: When first reasoning about the problem, or when input sizes are tiny and clarity outweighs speed.
- **Hash Map**: When dealing with arbitrary character sets or in languages without specialized counter structures.
- **Array Counter**: When memory optimization is critical and the character set is limited to lowercase letters.
- **Counter**: When working in Python and prioritizing code readability and conciseness.

### Optimization Notes

- The early length check (`len(ransomNote) > len(magazine)`) provides a quick fail path in the frequency-based solutions.
- Counting each letter once, rather than rescanning per character, is what drops the brute force's `O(m * n)` down to `O(m + n)`.
- For very large inputs with a limited character set, the array-based approach may have better cache locality.
- Using direct array indexing avoids hash computation overhead for small, fixed character sets.
