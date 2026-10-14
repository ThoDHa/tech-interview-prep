# [Longest Palindrome](https://leetcode.com/problems/longest-palindrome/)

**Easy** | **15 minutes** | **String, Hash Table, Greedy**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm)

**Practice:** [`practice/longest_palindrome/solution.py`](../../practice/longest_palindrome/solution.py)

Given a string `s` which consists of lowercase or uppercase letters, return the length of the longest palindrome that can be built with those letters.

Letters are case sensitive, for example, "Aa" is not considered a palindrome here.

## Examples

### Example 1

**Input:** `s = "abccccdd"`

**Output:** `7`

**Explanation:** One longest palindrome that can be built is "dccaccd", whose length is 7.

### Example 2

**Input:** `s = "a"`

**Output:** `1`

### Example 3

**Input:** `s = "bb"`

**Output:** `2`

## Constraints

- `1 <= s.length <= 2000`
- `s` consists of lowercase and/or uppercase English letters only.

## Deriving the Solution

A palindrome mirrors around its center, so its characters occur in pairs, with at most one unpaired character sitting in the exact middle. Every solution below computes the same quantity, the number of characters that can pair up plus one center character when any letter is left over, and they differ only in how the pairing is counted.

1. **Count, then pair.** Tally each character's frequency in a dictionary, keep
   the largest even part of every count, and add `1` if any count is odd. Two simple passes answer the question in `O(n)`: see [Brute Force](#brute-force).
2. **Pair as you read.** The counts are only ever used to extract pairs, so the
   pairs can be collected on the fly instead: a set holds characters still waiting for a partner, and each arrival either completes a pair or joins the waiting set. One pass, no per-count arithmetic: see [Set-based Pair Matching](#set-based-pair-matching).
3. **Subtract instead of add.** Summing even parts count by count is more work
   than needed: every discarded character comes from an odd count, and exactly one leftover may stay as the center. Start from `len(s)`, subtract one per odd count, and credit one back: see [Character Frequency Counting with Odd Character Tracking](#character-frequency-counting-with-odd-character-tracking).
4. **Let the library count.** The counting pass in step 1 is exactly what
   `collections.Counter` provides, so delegating it leaves only the pair arithmetic: see [Counter Frequency Tally](#counter-frequency-tally).

## Solutions

### Brute Force

#### Derivation

The most direct idea follows straight from how a palindrome is built: characters mirror around the center, so each character can contribute only in pairs, except for a single character allowed in the middle. That observation turns the question into pure counting, how many of each character are available and how many complete pairs they yield, without ever constructing a palindrome.

1. Count the frequency of every character with a plain [dictionary](https://en.wikipedia.org/wiki/Hash_table) `counts`.
2. For each frequency, add its largest even part `(count // 2) * 2` to the running `length`, because only complete pairs can mirror across the palindrome.
3. Record in `has_odd` whether any frequency is odd, since an odd frequency leaves one unpaired character.
4. If any odd frequency was seen, add `1` for a single center character.

#### Walkthrough

Let us trace the Brute Force solution on Example 1: `s = "abccccdd"`, expected Output `7`.

First pass: count each character with the dictionary. We read the string left to right, bumping `counts[c]` by one each time:

| Step | Char read | `counts` after |
|------|-----------|----------------|
| 1 | `a` | `{a: 1}` |
| 2 | `b` | `{a: 1, b: 1}` |
| 3 | `c` | `{a: 1, b: 1, c: 1}` |
| 4 | `c` | `{a: 1, b: 1, c: 2}` |
| 5 | `c` | `{a: 1, b: 1, c: 3}` |
| 6 | `c` | `{a: 1, b: 1, c: 4}` |
| 7 | `d` | `{a: 1, b: 1, c: 4, d: 1}` |
| 8 | `d` | `{a: 1, b: 1, c: 4, d: 2}` |

So the final counts are `a: 1`, `b: 1`, `c: 4`, `d: 2`.

Second pass: walk the counts, adding the even part `(count // 2) * 2` to `length` and flipping `has_odd` whenever a count is odd. Both `length` and `has_odd` start at `0` and `False`:

| Char | `count` | `(count // 2) * 2` added | `length` | `count % 2 == 1`? | `has_odd` |
|------|---------|--------------------------|----------|-------------------|-----------|
| `a` | 1 | 0 | 0 | yes | True |
| `b` | 1 | 0 | 0 | yes | True |
| `c` | 4 | 4 | 4 | no | True |
| `d` | 2 | 2 | 6 | no | True |

After the loop `length` is `6` and `has_odd` is `True`. Because `has_odd` is `True`, one leftover character (here `a` or `b`) can sit in the center, so we add `1`: `length` becomes `7`.

The function returns `7`, which matches the example's expected Output.

#### Solution

The code is the walkthrough's two passes written down: count every character, then take the even part of each count.

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:
        # Count each character by hand with a plain dictionary
        counts = {}
        for c in s:
            counts[c] = counts.get(c, 0) + 1

        length = 0
        has_odd = False
        for count in counts.values():
            # Every full pair contributes two characters to the palindrome
            length += (count // 2) * 2
            # A leftover single character means this count is odd
            if count % 2 == 1:
                has_odd = True

        # One leftover character can sit in the center
        if has_odd:
            length += 1
        return length
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Counting every character is one `O(n)` pass over the string of length `n`.
- Iterating the frequency values is `O(k)` where `k` is the number of distinct characters, bounded by the constant alphabet size.
- The total work is therefore linear in the input.

##### Space Complexity: `O(1)`

- The dictionary holds at most `52` entries (`26` lowercase + `26` uppercase English letters).
- This bound is constant regardless of input size, so the auxiliary space is constant.

#### Key Insights

- A palindrome mirrors around its center, so each character contributes only in pairs.
- Exactly one odd-frequency character can be placed in the center, which is why a single `+1` covers all the leftovers.
- Computing the answer from counts alone avoids ever building the palindrome string.
- Taking `(count // 2) * 2` cleanly drops any single unpaired character from each group.

### Set-based Pair Matching

#### Derivation

The Brute Force spends one pass counting and a second pass pairing, yet the counts themselves are never needed: only the pairs are. Can the pairs be collected while reading the string? A [set](https://en.wikipedia.org/wiki/Hash_table) `chars` of characters still waiting for a partner does exactly that: each incoming character either completes a pair with its waiting twin or becomes a waiter itself.

1. For each character in the string:
    - If it's already in the set, we've found a pair. Remove it from the set and increase `count` by 2.
    - If it's not in the set, add it to the set as a potential future pair.
2. After processing all characters, if the set is not empty (meaning we have unpaired characters), we can use one character as the center of the palindrome and add `1` to `count`.

#### Walkthrough

Let us run the pairing set on Example 1: `s = "abccccdd"`. Each line shows the character read, whether it found its partner waiting in `chars`, and the state afterward:

```text
c = a   not in chars -> add     chars = {a}          count = 0
c = b   not in chars -> add     chars = {a, b}       count = 0
c = c   not in chars -> add     chars = {a, b, c}    count = 0
c = c   in chars -> pair        chars = {a, b}       count = 2
c = c   not in chars -> add     chars = {a, b, c}    count = 2
c = c   in chars -> pair        chars = {a, b}       count = 4
c = d   not in chars -> add     chars = {a, b, d}    count = 4
c = d   in chars -> pair        chars = {a, b}       count = 6
```

Three pairs formed (`cc`, `cc`, `dd`), contributing `6`. The set still holds `{a, b}`: two characters never found a partner, and one of them may sit in the center, so `count` becomes `7`. The function returns `7`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's pairing loop, followed by the center check on the leftover set.

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:
        chars = set()
        count = 0

        for c in s:
            if c in chars:
                chars.remove(c)
                count += 2
            else:
                chars.add(c)

        # If we have any characters left, one can be used as center
        if chars:
            count += 1

        return count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- We iterate through the string once, performing `O(1)` operations (set insertion, lookup, removal) for each character.
- Since set operations are generally `O(1)`, the overall time complexity is `O(n)`.

##### Space Complexity: `O(1)`

- The set stores at most one of each unique character, which is bounded by the size of the character set (`52` letters).
- Since this upper bound is constant regardless of input size, the space complexity is `O(1)`.

#### Key Insights

- This approach elegantly tracks character pairs without explicit counting.
- The set effectively serves as a "pairing station": characters wait there until their pair arrives.
- The final check for a non-empty set determines if we can place one character at the center.
- This solution is particularly intuitive for understanding the palindrome construction process.

### Character Frequency Counting with Odd Character Tracking

#### Derivation

Both approaches so far build the answer upward by adding pairs, doing a little arithmetic for every distinct count. Work backward from `len(s)` instead: every character would be usable if nothing were unpaired, and only odd frequencies leave an unpaired character behind. Each odd frequency forces exactly one discard, except that one leftover may stay as the center, so counting the odd frequencies is all the arithmetic needed:

1. Create a [hash map](https://en.wikipedia.org/wiki/Hash_table) (dictionary) `counter` to store the count of each character.
2. Initialize the odd-frequency counter `odd_count` at `-1`, which pre-credits one odd character as the allowed center.
3. After counting characters, iterate through the values to count how many have an odd frequency.
4. Calculate the palindrome length:
    - If `odd_count > 0`: subtract that many characters from the total length, having already kept one odd character for the center.
    - If `odd_count = 0`: all characters pair up and the whole string is usable.

#### Closed Form

A palindrome uses each character in mirrored pairs, with at most one unpaired character allowed in the exact middle. So with \(c_x\) the frequency of character `x`, the answer is a direct formula rather than a search:

$$ \text{answer} = \sum_{x} 2\left\lfloor \frac{c_x}{2} \right\rfloor \ + \ \bigl[\, \exists\, x : c_x \text{ is odd} \,\bigr] $$

```text
answer = sum over x of 2 * (counter[x] // 2)
         + 1 if counter[x] is odd for some x, else + 0
```

The floor-halve-and-double term keeps the largest even portion of each frequency; the bracket adds `1` if any character has a leftover, since exactly one leftover may occupy the center.

This solution evaluates the same quantity from the other direction. Writing \(k\) for the number of characters with odd frequency:

$$ \sum_{x} 2\left\lfloor \frac{c_x}{2} \right\rfloor = |s| - k \qquad\Longrightarrow\qquad \text{answer} = \begin{cases}
|s|, & k = 0 \\[4pt]
|s| - k + 1, & k \ge 1
\end{cases} $$

```text
sum over x of 2 * (counter[x] // 2) = len(s) - k
    therefore
answer = len(s)          for k = 0
answer = len(s) - k + 1  for k >= 1
         where k = number of characters x with counter[x] odd
```

because each odd-frequency character contributes exactly one discarded unit. That is why the code initializes its counter at `-1`: pre-crediting the one character allowed in the center folds the `+1` into the subtraction, collapsing both cases into `len(s) - odd_count`.

#### Walkthrough

Let us trace on Example 1: `s = "abccccdd"`, so `len(s) = 8`. The counting pass fills `counter` exactly as in the Brute Force walkthrough, one increment per character, ending at `{a: 1, b: 1, c: 4, d: 2}`. The second pass tallies odd frequencies, starting from the pre-credit `odd_count = -1`:

```text
start          odd_count = -1    pre-credit: one odd character may be the center
a: 1   odd     odd_count = 0
b: 1   odd     odd_count = 1
c: 4   even    odd_count = 1
d: 2   even    odd_count = 1
```

Two characters (`a` and `b`) have odd counts; the pre-credit absorbs the first, leaving `odd_count = 1` genuine discard. Since `odd_count > 0`, the answer is `len(s) - odd_count = 8 - 1 = 7`, matching the expected Output for Example 1.

#### Solution

The code is the count-then-subtract pass from the walkthrough, with the center credit folded into the `-1` initialization.

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:
        counter = {}
        odd_count = -1
        # Count frequency of each character
        for c in s:
            counter[c] = counter.get(c, 0) + 1

        # Count characters with odd frequencies
        for count in counter.values():
            if count % 2 != 0:
                odd_count += 1

        # Calculate palindrome length
        if odd_count > 0:
            return len(s) - odd_count
        else:
            return len(s)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Counting the frequency of each character requires `O(n)` time where `n` is the length of the string.
- Iterating through the counter values is `O(k)` where `k` is the number of unique characters, which is bounded by the constant size of the character set.
- Since `k ≤ n`, the overall time complexity is `O(n)`.

##### Space Complexity: `O(1)`

- The counter dictionary stores at most `52` key-value pairs (`26` lowercase + `26` uppercase English letters).
- Since the size of the counter is bounded by a constant regardless of input size, the space complexity is `O(1)`.

#### Key Insights

- In a palindrome, most characters must appear in pairs (one on each side).
- At most one character can appear an odd number of times (placed in the center).
- The `odd = -1` initialization is a clever way to account for the fact that one odd-frequency character can be fully utilized.
- This approach efficiently handles the palindrome construction without explicitly building the string.

### Counter Frequency Tally

#### Derivation

The manual counting loop that opens every approach above is boilerplate the standard library already provides: [`collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) performs the same frequency tally in one call. What remains is the pair arithmetic, tightened with a bitwise touch: `freq & 1` is `1` when `freq` is odd and `0` when even, so it both detects odd counts and trims the unpaired character off each odd group in a single expression.

1. Build a `Counter` over `s`, mapping each character to its frequency.
2. For each frequency, add its largest even part (`freq - (freq & 1)`) to the running `length`, since pairs of characters always contribute to a palindrome.
3. Track whether any character has an odd frequency with `has_odd`.
4. If at least one odd frequency exists, a single leftover character can sit at the center, so add `1` to the result.

#### Walkthrough

Let us trace on Example 1: `s = "abccccdd"`. `Counter(s)` is the library's version of the counting pass and yields `counts = {a: 1, b: 1, c: 4, d: 2}`. The loop then processes each frequency, starting from `length = 0` and `has_odd = False`:

```text
freq = 1  (a)   freq & 1 = 1   length += 1 - 1 = 0 -> 0    has_odd = True
freq = 1  (b)   freq & 1 = 1   length += 1 - 1 = 0 -> 0    has_odd = True
freq = 4  (c)   freq & 1 = 0   length += 4 - 0 = 4 -> 4    has_odd stays True
freq = 2  (d)   freq & 1 = 0   length += 2 - 0 = 2 -> 6    has_odd stays True
```

The even parts contribute `6`, and because `has_odd` is `True` one leftover character may occupy the center: the function returns `6 + 1 = 7`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's loop with `Counter` supplying the counts.

```python
from collections import Counter


class Solution:
    def longestPalindrome(self, s: str) -> int:
        counts = Counter(s)
        length = 0
        has_odd = False
        for freq in counts.values():
            length += freq - (freq & 1)
            if freq & 1:
                has_odd = True
        return length + 1 if has_odd else length
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Building the `Counter` is a single `O(n)` pass over the string.
- Iterating the frequency values is `O(k)` where `k` is the number of distinct characters, bounded by the constant alphabet size.
- The overall time complexity is therefore `O(n)`.

##### Space Complexity: `O(1)`

- The `Counter` holds at most `52` entries (`26` lowercase + `26` uppercase letters).
- This bound is constant regardless of input size, so the space complexity is `O(1)`.

#### Key Insights

- `Counter` removes the manual frequency-counting boilerplate while preserving the same underlying logic.
- The even part of any count contributes fully to the palindrome; only the odd remainder is at risk.
- A single center slot is available whenever any character has an odd count, captured cleanly by the `has_odd` flag.
- `freq & 1` doubles as both an odd-parity test and the amount to subtract, keeping the loop body compact.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - One pass to count characters, one pass over the bounded set of distinct counts
- **Set-based Pair Matching**: `O(n)` - Single-pass approach with constant-time set operations
- **Character Frequency Counting with Odd Character Tracking**: `O(n)` - One pass to count characters and another to process counts
- **Counter Frequency Tally**: `O(n)` - One pass to build the `Counter`, one pass over the bounded set of distinct counts

### Space Complexity

- **Brute Force**: `O(1)` - Uses a dictionary bounded by the character set size
- **Set-based Pair Matching**: `O(1)` - Uses a set bounded by the character set size
- **Character Frequency Counting with Odd Character Tracking**: `O(1)` - Uses a dictionary bounded by the character set size
- **Counter Frequency Tally**: `O(1)` - Uses a `Counter` bounded by the character set size

### Trade-offs

- Brute Force is fully library-free and spells out the pair arithmetic directly, making it the clearest derivation of the answer.
- Set-based Pair Matching has a cleaner single-pass implementation and may be easier to understand conceptually, tracking pairs as they form.
- Character Frequency Counting trims the arithmetic by working backward from `len(s)`, using the `odd = -1` pre-credit to handle the center character implicitly.
- Counter Frequency Tally is the most concise, delegating the counting step to `collections.Counter` while keeping the palindrome arithmetic identical to the manual version.
- All four solutions handle the core requirement efficiently: determining the maximum palindrome length without building the actual palindrome.

### When to Use Each

- **Brute Force**: Preferred as the most direct, library-free derivation, or when the explicit pair-and-center logic aids understanding.
- **Set-based Pair Matching**: Preferred for readability and when solution simplicity is valued over minor optimizations.
- **Character Frequency Counting with Odd Character Tracking**: Preferred when you want a library-free solution and like deriving the answer by subtracting odd leftovers from the full length.
- **Counter Frequency Tally**: Preferred in production Python where `collections.Counter` is available and brevity is valued (Recommended for idiomatic code).

### Optimization Notes

- All four solutions are already optimal in terms of time and space complexity.
- The odd counter initialization in Character Frequency Counting is a clever way to absorb the center character without an extra conditional.
- Set-based Pair Matching demonstrates how using appropriate data structures can lead to elegant algorithmic solutions.
- Counter Frequency Tally uses `freq & 1` to fuse the odd-parity test with the unpaired-character subtraction, trimming the loop body to a single arithmetic step.
- In practice, all four solutions perform similarly for the constraints given.
