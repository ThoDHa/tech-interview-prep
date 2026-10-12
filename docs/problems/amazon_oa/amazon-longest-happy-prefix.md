# [Longest Happy Prefix](https://www.fastprep.io/problems/amazon-longest-happy-prefix)

**Hard** | **NN minutes** | **String**

A string is a happy prefix of s when it is a non-empty proper prefix of s and is also a suffix of s.

Return the longest happy prefix. If none exists, return the empty string.

## Examples

### Example 1

**Input:** `s = "level"`

**Output:** `"l"`

**Explanation:** The prefix l is also the suffix, and no longer proper prefix matches.

### Example 2

**Input:** `s = "ababab"`

**Output:** `"abab"`

**Explanation:** The first four characters equal the last four characters.

### Example 3

**Input:** `s = "a"`

**Output:** `""`

**Explanation:** A one-character string has no non-empty proper prefix.

## Constraints

- `1 <= s.length <= 100000.`
- `s contains only lowercase English letters.`

## Solutions

### Brute Force

#### Derivation

The most literal reading of "prefix equals suffix" tries every candidate length from longest to shortest. A length `length` is a happy prefix exactly when the first `length` characters of `s` equal the last `length` characters of `s`, and `length` must stay below `len(s)` because the prefix has to be proper. Checking from the longest length down means the first hit is the answer, and reaching length `1` without a hit proves the empty string is the answer:

1. Sweep `length` from `len(s) - 1` down to `1`.
2. Compare the window `prefix = s[:length]` with the window `suffix = s[len(s) - length:]`.
3. On the first equal pair, return `prefix`.
4. After the sweep exhausts, return `""`.

#### Walkthrough

Example 1: `s = "level"`. Each candidate length compares one prefix window with one suffix window:

```text
length 5: prefix "level"  suffix "level"  whole string, not proper -> skip
length 4: prefix "leve"   suffix "evel"   differ
length 3: prefix "lev"    suffix "vel"    differ
length 2: prefix "le"     suffix "el"     differ
length 1: prefix "l"      suffix "l"      equal -> return "l"
```

The only window pair that agrees is the single character `l`, so the function returns `"l"`, matching the expected Output for Example 1. On Example 2 (`"ababab"`) the descent stops immediately at `length 4` with `"abab"`; on Example 3 (`"a"`) the sweep range is empty and the function returns `""`.

#### Solution

The code is the longest-first window sweep from the walkthrough.

```python
class Solution:
    def solve(self, s: str) -> str:
        size = len(s)
        for length in range(size - 1, 0, -1):
            prefix = s[:length]
            suffix = s[size - length:]
            if prefix == suffix:
                return prefix
        return ""
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Up to `n - 1` candidate lengths, and each iteration compares windows of up to `n` characters; near palindromes such as `"aaa...ab"` force the full sweep.

##### Space Complexity: `O(n)`

The two window slices `prefix` and `suffix`, of up to `n - 1` characters each.

#### Key Insights

- The definition transcribes directly into code: one comparison per candidate length, longest first.
- Slicing and comparing are single C-speed operations in Python, so the quadratic bound hides a small constant; the approach is still the only one here that fails the `100000`-character constraint on adversarial inputs.
- Correct with no subtlety, which makes it the reference oracle for checking the two linear approaches.

### Rolling Hash

#### Derivation

The brute force re-compares almost the same windows at every length. The observation that removes that work: extending the prefix window by one character and extending the suffix window by one character are both single-step updates if windows are represented by a polynomial rolling hash, a technique from [Rabin-Karp](https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm) string search. With `hash(w) = w[0]·b^(L-1) + w[1]·b^(L-2) + ... + w[L-1]` under a fixed base `b` and a prime modulus, appending a character multiplies the old hash by `b` and adds it, and prepending a character multiplies the character by `b^(L-1)` and adds it. Comparing two integers then stands in for comparing two strings, at one window update per length.

The catch is that two different windows can share a hash (a collision), so a match is a claim about probability, not proof. Equal windows always hash equal, so a genuine border is never missed; the risk runs the other way, an unequal pair hashing equal, which would endorse a prefix that is not actually a border. A modulus of `2^61 - 1` keeps that per-comparison risk near `length / 2^61` for inputs not engineered against the fixed base, negligible over a `100000`-character string.

1. Fix `hash_base = 31` and `hash_modulus = 2^61 - 1`.
2. Grow `length` from `1` to `len(s) - 1`. Update `prefix_hash` by appending
   `s[length - 1]`; update `suffix_hash` by prepending `s[len(s) - length]`,
   scaled by `power = hash_base^(length - 1)`.
3. When the two hashes match, record `best_length = length` (records may
   bounce back down, but each hash agreement is a genuine border unless a
   collision occurs).
4. Return `s[:best_length]`.

#### Invariant and Bound

The comparison is only as trustworthy as the hashes, so the correctness rests on the following property of the loop rather than on a formula:

```text
invariant:  at every length, prefix_hash = hash(s[:length])
            and suffix_hash = hash(s[size - length:])
bound:      unequal windows collide with probability <= length / 2^61
            per comparison (heuristic for a fixed base: inputs not
            engineered against hash_base); the union bound over all
            n - 1 comparisons stays below 10^-8
guarantee:  the returned s[:best_length] equals its opposite window
            unless a collision fired; a longer border can never be
            missed because equal windows always hash equal
```

The invariant holds because each iteration extends the prefix window by exactly one character and prepends exactly one character to the suffix window, and the `power` multiplier equals `hash_base^(length - 1)` at the moment of the prepend. What the loop buys with the probabilistic gap is a single pass in constant memory.

#### Walkthrough

Example 2: `s = "ababab"`, with `hash_base = 31`. The prefix window grows off the left end while the suffix window grows off the right end; each line shows the actual window strings and their hashes:

```text
length 1: prefix "a"    hash 97         suffix "b"    hash 98         differ
length 2: prefix "ab"   hash 3105       suffix "ab"   hash 3105       equal -> best_length = 2
length 3: prefix "aba"  hash 96352      suffix "bab"  hash 97283      differ
length 4: prefix "abab" hash 2987010    suffix "abab" hash 2987010    equal -> best_length = 4
length 5: prefix "ababa" hash 92597407  suffix "babab" hash 93492068  differ
return s[:4] = "abab"
```

The hash agreements at lengths `2` and `4` are genuine borders, and `best_length` ends at `4`, so the function returns `"abab"`, matching the expected Output for Example 2. On Example 1 (`"level"`) only the length-1 pair `'l'`/`'l'` agrees and the return is `"l"`; on Example 3 (`"a"`) the loop body never runs and `s[:0]` returns `""`.

#### Solution

The code is the two window updates and the compare from the walkthrough, one iteration per candidate length.

```python
class Solution:
    def solve(self, s: str) -> str:
        size = len(s)
        hash_base = 31
        hash_modulus = (1 << 61) - 1
        prefix_hash = 0
        suffix_hash = 0
        power = 1
        best_length = 0
        for length in range(1, size):
            prefix_hash = (prefix_hash * hash_base + ord(s[length - 1])) % hash_modulus
            suffix_hash = (ord(s[size - length]) * power + suffix_hash) % hash_modulus
            if prefix_hash == suffix_hash:
                best_length = length
            power = (power * hash_base) % hash_modulus
        return s[:best_length]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One constant-time hash update, one scaling, and one integer compare per candidate length, with no string comparisons at all.

##### Space Complexity: `O(1)`

Five integers regardless of the input size; the returned slice is output, not working memory.

#### Key Insights

- Growing both windows one character at a time converts the per-length string comparison into one integer update on each side; this is the Rabin-Karp trick applied to a prefix/suffix sweep instead of a pattern search.
- The base and modulus are tunable risk knobs: `2^61 - 1` pushes the collision probability so low that a birthday-style failure needs astronomically many trials.
- The probabilistic gap is the price of the linear pass: KMP below answers the same question with a proof instead of a probability, at the cost of a table.

### KMP Failure Function

#### Derivation

Both earlier approaches compare windows against each other. The named-algorithm route observes that the question is a classical quantity in disguise: the longest happy prefix of `s` is the longest [border](https://en.wikipedia.org/wiki/Prefix,_Proper_suffix,_Prefix_function) of `s`, meaning the longest string that is both a proper prefix and a suffix, which is exactly what the failure function of the [Knuth-Morris-Pratt](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm) algorithm computes for every prefix in one pass. The table stores, for each position, the longest border of the prefix ending there, and its last entry answers the whole problem:

1. Allocate `border_lengths` with one slot per position of `s`, all `0`.
2. Sweep `position` from `1` to `len(s) - 1` with `matched` holding the
   previous position's border length.
3. While `matched > 0` and `s[position] != s[matched]`, drop `matched` to
   `border_lengths[matched - 1]`: a character that breaks the current border
   may still extend the border of that border.
4. When `s[position] == s[matched]`, extend with `matched += 1`; store
   `border_lengths[position] = matched`.
5. Return `s[:border_lengths[-1]]`.

#### Walkthrough

Example 2: `s = "ababab"`. Each position either extends the running border or drops `matched` down the border chain first:

```text
position 1: 'b' vs s[0]='a'  matched 0 -> nothing to drop, stays 0
            border_lengths[1] = 0
position 2: 'a' vs s[0]='a'  extend -> matched = 1
            border_lengths[2] = 1
position 3: 'b' vs s[1]='b'  extend -> matched = 2
            border_lengths[3] = 2
position 4: 'a' vs s[2]='a'  extend -> matched = 3
            border_lengths[4] = 3
position 5: 'b' vs s[3]='b'  extend -> matched = 4
            border_lengths[5] = 4
return s[:4] = "abab"
```

The drop branch of the while loop never fires on this input because every position extends the previous border; on a string such as `"aabaa"` it does the real work: at the final `'a'` the matched count `2` (from border `"aa"`) is kept, giving `border_lengths[4] = 2` and the answer `"aa"`. Here the last entry is `4`, so the function returns `"abab"`, matching the expected Output for Example 2. Example 1 (`"level"`) fills `border_lengths = [0, 0, 0, 0, 1]` and returns `"l"`; Example 3 (`"a"`) fills `[0]` and returns `""`.

#### Solution

The code is the border sweep from the walkthrough; the last table entry is the answer.

```python
class Solution:
    def solve(self, s: str) -> str:
        size = len(s)
        border_lengths = [0] * size
        matched = 0
        for position in range(1, size):
            while matched > 0 and s[position] != s[matched]:
                matched = border_lengths[matched - 1]
            if s[position] == s[matched]:
                matched += 1
            border_lengths[position] = matched
        return s[:border_lengths[-1]]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The `matched` counter increases at most once per position, and every while-loop drop strictly decreases it, so the total number of drops across the whole sweep is bounded by `n - 1`: one pass with amortized constant work per character.

##### Space Complexity: `O(n)`

The `border_lengths` table, one integer per position.

#### Key Insights

- Reframing the problem as "find the longest border" connects it to KMP, whose failure function computes exactly this quantity for every prefix in a single pass.
- The while-loop drop is the whole difficulty: after a mismatch, the next candidate border is the longest border of the current border, and following that chain is what keeps the algorithm linear.
- Unlike the rolling hash, the answer carries no probabilistic caveat: the comparison is over actual characters, and `O(n)` holds for every input, not just on average.
- The table is reusable beyond this question: it is the same preprocessing KMP uses to search for a pattern inside a text.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - up to `n - 1` window comparisons, each over up to `n` characters.
- **Rolling Hash**: `O(n)` - one hash update and one integer compare per candidate length.
- **KMP Failure Function**: `O(n)` - one pass with amortized constant work per character.

### Space Complexity

- **Brute Force**: `O(n)` - the prefix and suffix window slices.
- **Rolling Hash**: `O(1)` - a fixed set of integers.
- **KMP Failure Function**: `O(n)` - the border table, one entry per position.

### Trade-offs

- **Brute Force**: zero subtlety and trivially correct, but quadratic time makes it unusable at the stated constraint of `100000` characters in the worst case.
- **Rolling Hash**: linear time in constant space, but its correctness argument is probabilistic; a collision would silently endorse a prefix that is not a border, while genuine borders are never missed.
- **KMP Failure Function**: linear time with a proof for every input, at the cost of the extra border table and the least self-evident loop of the three.

### When to Use Each

- **Brute Force**: as the correctness oracle while developing or testing; acceptable when the string is known to be short.
- **Rolling Hash**: when constant memory matters or when the surrounding problem already uses hashing; the standard choice in competitive settings where `2^61 - 1`-style hashes are house style.
- **KMP Failure Function (Recommended)**: the interview answer: optimal worst-case time, a deterministic correctness argument, and a named algorithm worth being able to derive on a whiteboard.

### Optimization Notes

- The brute force returns from inside the loop on the first hit; its worst case is a string with no happy prefix at all or a border only at the shortest lengths, so random inputs almost always exit early.
- In the rolling hash, the `power` multiplier tracks `hash_base^(length - 1)` and is itself reduced modulo `hash_modulus` each step; letting it grow unbounded works in Python but slows the big-integer arithmetic.
- In the failure function, the drop chain `matched = border_lengths[matched - 1]` is safe exactly because `border_lengths[matched - 1] < matched`; replacing it with `matched - 1` is the classic bug that quietly degrades the algorithm to quadratic.
- All three implementations return `""` naturally for a one-character string, since the sweep ranges are empty or the final border is `0`; no special case is needed.
