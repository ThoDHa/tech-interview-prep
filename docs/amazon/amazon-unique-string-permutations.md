# [Unique String Permutations](https://www.fastprep.io/problems/amazon-unique-string-permutations)

**Medium** | **NN minutes** | **String, Sorting, Backtracking, Combinatorics**

Given a lowercase string s, return every distinct permutation of its characters exactly once.

Return the permutations in ascending lexicographic order. Equal characters from different input positions must not create duplicate strings.

## Examples

### Example 1

**Input:** `s = "aab"`

**Output:** `["aab","aba","baa"]`

**Explanation:** There are three distinct arrangements after duplicate swaps of the two a characters are removed.

### Example 2

**Input:** `s = "xxyy"`

**Output:** `["xxyy","xyxy","xyyx","yxxy","yxyx","yyxx"]`

**Explanation:** The four positions have six unique arrangements because each character appears twice.

### Example 3

**Input:** `s = "z"`

**Output:** `["z"]`

**Explanation:** A one-character string has one permutation.

## Constraints

- `1 <= s.length <= 8.`
- `s contains only lowercase English letters.`

## Solutions

### Backtracking with Set Deduplication

#### Derivation

The classic permutation template fills positions one at a time: keep a partial permutation and a used flag per input position, and at each level try every unused position. The statement adds two requirements the distinct-input template does not handle: equal characters at different positions must not produce duplicate output strings, and the results must come back in ascending lexicographic order. The most direct reading generates every ordering with the plain template and repairs both requirements after the fact, with a set absorbing duplicates and a sort imposing order:

1. Keep `current`, the partial permutation, and `used`, a boolean array parallel to the positions of `s`.
2. When `current` reaches the length of `s`, join it into a string and add it to `permutations_set`.
3. Otherwise scan every `position` of `s`; skip used ones, then mark the position used, append its character, recurse, and undo both.
4. Return `sorted(permutations_set)` to satisfy the order requirement.

#### Walkthrough

Example 1, `s = "aab"`. The two `a` characters sit at positions 0 and 1, so the used-position tree builds all `3! = 6` orderings and the set collapses the repeats:

```text
positions chosen    string    permutations_set after the insert
(0, 1, 2)           "aab"     {"aab"}
(0, 2, 1)           "aab"     {"aab"}                 duplicate, absorbed
(1, 0, 2)           "aba"     {"aab", "aba"}
(1, 2, 0)           "aba"     {"aab", "aba"}          duplicate, absorbed
(2, 0, 1)           "baa"     {"aab", "aba", "baa"}
(2, 1, 0)           "baa"     {"aab", "aba", "baa"}   duplicate, absorbed
```

Sorting the set yields `["aab", "aba", "baa"]`, the expected Output for Example 1. Half the tree was wasted work: six orderings were built and three were thrown away.

#### Solution

The code is the classic used-position backtracking with the set and the sort bolted on:

```python
from typing import List, Set


class Solution:
    def uniquePermutations(self, s: str) -> List[str]:
        """Return every distinct permutation of s in ascending lexicographic order.

        Time:  O(n! * n): all n! position orderings are built and joined, then
               the unique strings are sorted.
        Space: O(n! * n): the set can hold all n! distinct strings of length n.
        """
        permutations_set: Set[str] = set()
        used = [False] * len(s)

        def backtrack(current: List[str]) -> None:
            if len(current) == len(s):
                permutations_set.add("".join(current))
                return
            for position in range(len(s)):
                if used[position]:
                    continue
                used[position] = True
                current.append(s[position])
                backtrack(current)
                current.pop()
                used[position] = False

        backtrack([])
        return sorted(permutations_set)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

The tree always has `n!` leaves because it never reacts to duplicates: each leaf joins `n` characters, and the final sort of at most `n!` strings of length `n` is bounded by the same term.

##### Space Complexity: `O(n! × n)`

The set holds one string per distinct permutation, which is `n!` strings of length `n` when every character is distinct; the recursion and `current` add `O(n)`.

#### Key Insights

- Deduplicating after generation is correct but pays full price for the duplicates: Example 2's `"xxyy"` builds `4! = 24` orderings to produce `6` strings.
- The set shrinks the output, never the tree: pruning has to happen at the choice level, which is what the next approach does.
- Sorting at the end is the tax for not controlling the generation order.

### Backtracking with Character Counts

#### Derivation

The set in the previous approach exists because sibling branches choose equal characters from different positions and grow into identical strings. Removing duplicates at the source changes what a branch chooses: characters, not positions. Sort the characters once, keep one count per letter, and at each position try each letter whose count is still positive. Two branches at the same node now always pick different letters, so no two leaves can spell the same string and the set disappears. Scanning the letters in ascending order at every node makes the output emerge already in lexicographic order, so the final sort disappears too:

1. Tally `counts`, a 26-entry table indexed by `ord(character) - ord("a")`.
2. When `current` reaches the length of `s`, join it and append it to `result`.
3. Otherwise scan `letter_index` from `0` to `25` in order; skip letters whose count is `0`.
4. Decrement `counts[letter_index]`, append `chr(ord("a") + letter_index)`, recurse, then restore the count and pop `current`.

#### Walkthrough

Example 2, `s = "xxyy"`, starts from `counts = x:2, y:2`. The trace is an indented call tree: each `take` line shows the counts and `current` after the choice, and indentation marks depth:

```text
backtrack()                          counts x:2 y:2   current ""
├─ take x  (x:1 y:2)                 current "x"
│  ├─ take x  (x:0 y:2)              current "xx"
│  │  └─ take y  (x:0 y:1)           current "xxy"
│  │     └─ take y  (x:0 y:0)        current "xxyy"  -> append "xxyy"
│  └─ take y  (x:1 y:1)              current "xy"
│     ├─ take x  (x:0 y:1)           current "xyx"
│     │  └─ take y  (x:0 y:0)        current "xyxy"  -> append "xyxy"
│     └─ take y  (x:1 y:0)           current "xyy"
│        └─ take x  (x:0 y:0)        current "xyyx"  -> append "xyyx"
└─ take y  (x:2 y:1)                 current "y"
   ├─ take x  (x:1 y:1)              current "yx"
   │  ├─ take x  (x:0 y:1)           current "yxx"
   │  │  └─ take y  (x:0 y:0)        current "yxxy"  -> append "yxxy"
   │  └─ take y  (x:1 y:0)           current "yxy"
   │     └─ take x  (x:0 y:0)        current "yxyx"  -> append "yxyx"
   └─ take y  (x:2 y:0)              current "yy"
      └─ take x  (x:1 y:0)           current "yyx"
         └─ take x  (x:0 y:0)        current "yyxx"  -> append "yyxx"
```

Every node offers each distinct letter at most once, so no leaf repeats another and nothing is generated just to be discarded. The appends land in ascending order: `["xxyy", "xyxy", "xyyx", "yxxy", "yxyx", "yyxx"]`, exactly the expected Output for Example 2.

#### Solution

The code is the counts table and the ascending letter scan from the walkthrough:

```python
from typing import List


class Solution:
    def uniquePermutations(self, s: str) -> List[str]:
        """Return every distinct permutation of s in ascending lexicographic order.

        Time:  O(u * n): u distinct permutations, each reached once and joined
               in O(n), with u the number of distinct permutations.
        Space: O(n): the recursion stack, the partial permutation, and a fixed
               26-entry count table.
        """
        counts = [0] * 26
        for character in s:
            counts[ord(character) - ord("a")] += 1

        result: List[str] = []
        current: List[str] = []
        length = len(s)

        def backtrack() -> None:
            if len(current) == length:
                result.append("".join(current))
                return
            for letter_index in range(26):
                if counts[letter_index] == 0:
                    continue
                counts[letter_index] -= 1
                current.append(chr(ord("a") + letter_index))
                backtrack()
                current.pop()
                counts[letter_index] += 1

        backtrack()
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(u × n)`

With `u` the number of distinct permutations (`u ≤ n!`): the tree has exactly one leaf per output string, each leaf costs `O(n)` to join, and the interior nodes are fewer than leaves times depth, so the whole tree is `O(u × n)`. The worst case remains `O(n! × n)` when all characters are distinct.

##### Space Complexity: `O(n)`

The recursion depth is at most `n`, `current` holds at most `n` characters, and `counts` is a fixed 26 entries. The output list is not counted as auxiliary space.

#### Key Insights

- Sorting the characters up front is what makes the ascending letter scan produce lexicographic order for free; the counts table alone would still need a final sort.
- The no-duplicates guarantee lives in the shape of the tree (distinct choices per node), not in a filter applied afterwards.
- With `n ≤ 8` the output holds at most `8! = 40320` strings, so an algorithm linear in the output size is comfortably fast; the duplicate-generating tree, by contrast, can build up to `n!` orderings regardless of how few are distinct.

### Built-in itertools.permutations

#### Derivation

When demonstrating the enumeration is not the point, the standard library generates orderings in C: [`itertools.permutations`](https://docs.python.org/3/library/itertools.html#itertools.permutations). This is the library version of [Backtracking with Set Deduplication](#backtracking-with-set-deduplication): the generation loop moves into the library while the set and the sort remain, because the library has no awareness that equal characters exist. Feeding it `sorted(s)` at least makes the orderings arrive in lexicographic order. It ranks last because it hides both the algorithm and the duplicate-handling insight the problem is really about:

1. Call `permutations(sorted(s))` so tuples arrive in lexicographic order.
2. Collect the tuples into a set to drop duplicates.
3. Sort the survivors and join each tuple into a string.

#### Walkthrough

The library is the technique, so the trace is of its documented behavior on Example 1, `s = "aab"`:

```text
sorted(s)                 -> "aab"
permutations("aab")       -> ("a","a","b") ("a","b","a") ("a","a","b")
                             ("a","b","a") ("b","a","a") ("b","a","a")
set(...)                  -> {("a","a","b"), ("a","b","a"), ("b","a","a")}
sorted(...), "".join each -> ["aab", "aba", "baa"]
```

Six tuples go in, three strings come out in ascending order, matching the expected Output for Example 1.

#### Solution

The code is one comprehension over the library's iterator:

```python
from itertools import permutations
from typing import List


class Solution:
    def uniquePermutations(self, s: str) -> List[str]:
        """Return every distinct permutation of s in ascending lexicographic order.

        Time:  O(n! * n): the library emits all n! orderings, duplicates
               included, then the unique strings are sorted.
        Space: O(n! * n): materializing the set holds up to n! tuples before
               deduplication is finished.
        """
        return ["".join(perm) for perm in sorted(set(permutations(sorted(s))))]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n! × n)`

The library produces all `n!` orderings of the `n` characters regardless of duplicates; each tuple is hashed and compared in `O(n)`, and the final sort is bounded by the same term.

##### Space Complexity: `O(n! × n)`

The set materializes one tuple per distinct ordering, and the iterator feeds it every one of the `n!` raw orderings before deduplication is finished.

#### Key Insights

- The standard library does the core work, so this is ranked last despite being the shortest.
- `itertools.permutations` enumerates by position, not by value: it cannot skip duplicates, so the set remains mandatory.
- Building `set(permutations(...))` holds all `n!` tuples at once; the hand-written versions stream each finished string into their collection instead.

## Comparison of Solutions

### Time Complexity

- **Backtracking with Set Deduplication**: `O(n! × n)` - builds all `n!` position orderings and sorts the survivors.
- **Backtracking with Character Counts**: `O(u × n)` - one tree node per distinct partial permutation, with `u` the number of distinct results.
- **Built-in itertools.permutations**: `O(n! × n)` - the library emits every ordering, duplicates included.

### Space Complexity

- **Backtracking with Set Deduplication**: `O(n! × n)` - the set holds one string per distinct permutation in the worst case.
- **Backtracking with Character Counts**: `O(n)` - recursion stack, partial permutation, and a fixed 26-entry count table, excluding the output.
- **Built-in itertools.permutations**: `O(n! × n)` - the materialized set holds every distinct ordering as a tuple.

### Trade-offs

- **Backtracking with Set Deduplication**: the least new material on top of the classic template, but it does full duplicate work and needs a final sort.
- **Backtracking with Character Counts**: does no wasted generation and emits results already ordered, at the cost of reasoning about counts instead of positions.
- **Built-in itertools.permutations**: one line, but it hides the algorithm and pays for every duplicate the input contains.

### When to Use Each

- **Backtracking with Character Counts (Recommended)**: the interview answer: it demonstrates backtracking, handles duplicates structurally, and produces sorted output with no extra pass.
- **Backtracking with Set Deduplication**: when extending the distinct-input permutation template quickly matters more than the duplicate work, and `n` is small.
- **Built-in itertools.permutations**: for production scripts where brevity beats demonstrating the technique.

### Optimization Notes

- The decisive optimization is structural, not micro: choosing letters with positive counts instead of unused positions is what removes duplicate branches.
- Sorting the characters once up front buys the lexicographic order for free; sorting the output afterwards costs up to `u log u` string comparisons.
- Appending `"".join(current)`, a fresh string, rather than the live `current` list is what keeps already-collected results safe from later mutation.
- For alphabets beyond lowercase letters, swap the 26-entry list for a `Counter`; the argument and the bounds are unchanged.
