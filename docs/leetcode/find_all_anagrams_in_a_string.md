# [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/)

**Medium** | **20 minutes** | **String**

**Pattern:** [Sliding Window](../patterns/sliding_window/intuition.md)

**Algorithm:** [Sliding window](https://usaco.guide/gold/sliding-window)

**Practice:** [`practice/find_all_anagrams_in_a_string/solution.py`](../../practice/find_all_anagrams_in_a_string/solution.py)

Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`. You may return the answer in any order.

An **anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Examples

### Example 1

**Input:** `s = "cbaebabacd"`, `p = "abc"`

**Output:** `[0,6]`

**Explanation:** The substring with start index = 0 is `"cba"`, which is an anagram of `"abc"`. The substring with start index = 6 is `"bac"`, which is an anagram of `"abc"`.

### Example 2

**Input:** `s = "abab"`, `p = "ab"`

**Output:** `[0,1,2]`

**Explanation:** The substring with start index = 0 is `"ab"`, which is an anagram of `"ab"`. The substring with start index = 1 is `"ba"`, which is an anagram of `"ab"`. The substring with start index = 2 is `"ab"`, which is an anagram of `"ab"`.

## Constraints

- `1 <= s.length, p.length <= 3 * 10^4`
- `s` and `p` consist of lowercase English letters only.

## Deriving the Solution

A substring of `s` is an anagram of `p` exactly when it has length `k = len(p)` and the same letter counts: order never matters, only the frequency of each of the 26 lowercase letters. All three solutions compare letter counts; they differ in how much counting work each window position costs and in whether those counts are hand-rolled or borrowed from the standard library.

1. **Start literal.** Try every width-`k` window of `s`: for each start index,
   count its letters from scratch and compare against `p`'s counts. Correct, but each of the `n - k + 1` windows pays a full `O(k)` recount, quadratic when `k` is a large fraction of `n`: see [Brute Force](#brute-force).
2. **Spot the waste.** Adjacent windows overlap in all but two positions: one
   character leaves on the left and one enters on the right. Rebuilding the whole count throws away `k - 2` letters of work that did not change.
3. **Slide the count.** Keep one running `window` count and update only the
   entering and leaving slots, plus a `matches` counter recording how many of the 26 slots already agree with `need`, so the per-window comparison collapses to the single test `matches == 26`. Every character enters and leaves once, making the scan `O(n)`: see [Sliding Window with Fixed-Size Count Array](#sliding-window-with-fixed-size-count-array).
4. **Let the library hold the counts.** The slide itself does not care what
   stores the frequencies. Handing them to `Counter` deletes the `need` construction loop, the `ord` arithmetic, and the whole `matches` apparatus, leaving a plain `window == need` test: markedly cleaner code for a slightly larger constant factor, see [Sliding Window with Counter](#sliding-window-with-counter).

## Solutions

### Brute Force

#### Derivation

The first question is what "anagram" means operationally: a substring of `s` is an anagram of `p` exactly when it has length `k = len(p)` and the same multiset of characters, which two frequency counts can verify. The most direct strategy tries every possible window of width `k` and rebuilds its frequency count independently.

1. If `p` is longer than `s`, no anagram can exist, so return an empty list.
2. Build `need`, a fixed 26-slot array holding the frequency of each lowercase
   letter in `p`. Indexing by `ord(c) - ord('a')` maps `'a'..'z'` to `0..25`.
3. For each start index `i` from `0` to `n - k`, scan the `k` characters of the
   window `s[i:i+k]` and tally them into a fresh `window` array.
4. Compare `window` to `need`. Python compares the two 26-element lists slot by
   slot, so a match means the window is an anagram of `p`.
5. Append `i` on every match, then return the collected start indices.

This rebuilds the entire count for every window, doing no work-sharing between overlapping windows, which makes it simple but redundant.

#### Walkthrough

Let's watch the Brute Force run on Example 1: `s = "cbaebabacd"`, `p = "abc"`.

First we build `need`, the target count for `p`. Only three slots are nonzero: `a: 1`, `b: 1`, `c: 1` (all other 23 slots stay `0`). Here `n = 10` and `k = 3`, so the loop tries window starts `i` from `0` to `n - k = 7`.

For each `i` we rebuild `window` from scratch over `s[i:i+3]`, then check `window == need`. The "counts" column below lists only the nonzero slots:

| `i` | window `s[i:i+3]` | counts | `== need`? |
| --- | --- | --- | --- |
| `0` | `"cba"` | `a:1, b:1, c:1` | yes: append `0` |
| `1` | `"bae"` | `a:1, b:1, e:1` | no |
| `2` | `"aeb"` | `a:1, b:1, e:1` | no |
| `3` | `"eba"` | `a:1, b:1, e:1` | no |
| `4` | `"bab"` | `a:1, b:2` | no |
| `5` | `"aba"` | `a:2, b:1` | no |
| `6` | `"bac"` | `a:1, b:1, c:1` | yes: append `6` |
| `7` | `"acd"` | `a:1, c:1, d:1` | no |

At `i = 0` the window `"cba"` has exactly one `a`, one `b`, one `c`, matching `need`, so `0` is appended. The next windows each carry an `e`, a doubled letter, or a `d`, so none match until `i = 6`, where `"bac"` again has one of each needed letter and `6` is appended.

The loop ends and we return `result = [0, 6]`, which matches the expected Output `[0,6]`.

#### Solution

The code is the walkthrough's table: rebuild `window` for each start index and compare it to `need`.

```python
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n, k = len(s), len(p)
        if k > n:
            return []

        # Target frequency of p as a fixed 26-slot array (one per letter).
        need = [0] * 26
        for c in p:
            need[ord(c) - ord("a")] += 1

        result = []
        # Try every possible window start; the last valid start is n - k.
        for i in range(n - k + 1):
            window = [0] * 26
            # Count the characters of the window s[i:i+k] from scratch.
            for j in range(i, i + k):
                window[ord(s[j]) - ord("a")] += 1
            # A window is an anagram of p iff the two count arrays match.
            if window == need:
                result.append(i)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n - k + 1) * k)`

There are `n - k + 1` window positions, and each one fully recounts `k` characters before a constant 26-slot comparison. Counting both parts gives `O((n - k + 1) * (k + 26))`, and the recount dominates once `k` exceeds the alphabet size. In the worst case (`k ≈ n / 2`) this is quadratic in `n`.

##### Space Complexity: `O(1)`

Both `need` and the per-window `window` array are fixed at 26 slots regardless of input size. The `result` list is output, not auxiliary working space.

#### Key Insights

- Anagram detection reduces to comparing character frequency counts, since order
  does not matter.
- A fixed 26-slot array indexed by `ord(c) - ord('a')` compares in constant time
  and needs no hashing, though `Counter` expresses the same tally far more briefly.
- The inefficiency comes from discarding each window's count and rebuilding the
  next from scratch, ignoring that adjacent windows differ by only two characters.

### Sliding Window with Fixed-Size Count Array

#### Derivation

The brute force discards each window's count and rebuilds the next from scratch, even though adjacent windows overlap heavily: [sliding one step](https://usaco.guide/gold/sliding-window) removes a single character on the left and adds a single character on the right. Rather than recounting, we maintain the window's 26-slot count incrementally and track a running `matches` value, the number of letters whose window count already equals the needed count. In plain text the invariant below is `matches == number of letters c with window[c] == need[c]`, which is what makes the test `matches == 26` equivalent to comparing the two arrays outright.

1. If `p` is longer than `s`, return an empty list.
2. Build `need` and a zeroed `window`, both fixed 26-slot arrays, then initialize
   `matches` by comparing the two arrays slot by slot (initially the 26 zeros of `window` match every zero slot of `need`).
3. Walk `i` across `s`. For the entering character, adjust `matches` before and
   after incrementing its slot: a slot only counts as a match when the two values are equal, so we decrement `matches` if it was matching, bump the count, then increment `matches` if it now matches.
4. Once `i >= k`, the window has grown past width `k`, so apply the mirror update
   for the leaving character `s[i - k]`, keeping the window exactly `k` wide.
5. When the window is full width (`i >= k - 1`) and `matches == 26`, every letter
   agrees, so the window is an anagram; record its start index `i - k + 1`.

Each character's entry and exit touches a single slot and adjusts `matches` in constant time, so the whole scan is linear.

#### Invariant

Both `need` and `window` are 26-slot counts indexed by a letter \(c \in \{0, \ldots, 25\}\). The loop maintains one property about the integer `matches`:

$$ \textit{matches} = \bigl|\{\, c \ :\ \textit{window}[c] = \textit{need}[c] \,\}\bigr| $$

```text
matches = number of letters c in 0..25 with window[c] == need[c]
```

It counts how many of the 26 letters currently agree. Since that set can only be a subset of all 26 letters, the count saturates exactly when every slot agrees:

$$ \textit{matches} = 26 \iff \textit{window} = \textit{need} $$

```text
matches == 26  if and only if  window == need
```

This equivalence is the payoff: the brute force's slot-by-slot array comparison collapses into a single integer test. The price is that every write to `window` must keep `matches` honest, and that is what the decrement-bump-increment triple around each count change is for.

A write to `window[c]` can change the agreement status of slot `c` and of no other slot, so only that slot's contribution to the count needs revisiting. Subtract it before the write if it was agreeing, then add it back after the write if it now agrees. Both count changes follow that shape: the entering letter around `window[entering] += 1`, and the leaving letter around `window[leaving] -= 1`. Drop either half and `matches` keeps a stale verdict for that slot, so the invariant fails.

The invariant holds before the first iteration because `matches` is initialized by direct comparison: `window` is all zeros, so it counts exactly the zero slots of `need`.

At the test the eviction step has already run, so the window is `s[i-k+1 .. i]`, exactly `k` characters wide once `i >= k - 1`. Reading the invariant there, `matches == 26` says the window's letter counts equal `p`'s, so the window is an anagram of `p` and its start index `i - k + 1` is recorded.

#### Walkthrough

Let us run the scan on Example 2: `s = "abab"`, `p = "ab"`, so `n = 4` and `k = 2`. `need` holds `a: 1, b: 1`, and `window` starts all zeros, so the initial slot-by-slot comparison finds the 24 letters absent from both arrays agreeing while the `a` and `b` slots disagree: `matches = 24`.

Each line below shows one loop iteration after its updates: the entering character, the leaving character once `i >= k`, the nonzero slots of `window`, and `matches`:

```text
i=0  enter 'a'             window a:1        matches 25    window not yet k wide
i=1  enter 'b'             window a:1, b:1   matches 26    append 0
i=2  enter 'a', leave 'a'  window a:1, b:1   matches 26    append 1
i=3  enter 'b', leave 'b'  window a:1, b:1   matches 26    append 2
```

At `i = 0` the `a` slot reaches its needed count, lifting `matches` to `25`, but the window is not yet `k` wide, so nothing is recorded. At `i = 1` the `b` slot agrees too, `matches` saturates at `26`, and start index `0` is appended. At `i = 2` the entering `a` first pushes its slot to `2` (dropping `matches` to `25` mid-update), then the leaving `a` at `s[0]` restores the slot to `1` and `matches` to `26`: the window `"ba"` is an anagram, so `1` is appended. `i = 3` mirrors it with `b`, appending `2`. The final `result = [0, 1, 2]` matches the expected Output `[0,1,2]`.

#### Solution

The code is the walkthrough's per-character update: the decrement-bump-increment triple for the entering slot, its mirror for the leaving slot, and the `matches == 26` test.

```python
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n, k = len(s), len(p)
        if k > n:
            return []

        need = [0] * 26
        window = [0] * 26
        for c in p:
            need[ord(c) - ord("a")] += 1

        # matches = how many of the 26 letters currently agree between
        # window and need. When matches == 26 the window is an anagram.
        matches = sum(1 for i in range(26) if need[i] == window[i])

        result = []
        for i in range(n):
            entering = ord(s[i]) - ord("a")
            # Add the incoming character, updating its match status in O(1).
            if window[entering] == need[entering]:
                matches -= 1
            window[entering] += 1
            if window[entering] == need[entering]:
                matches += 1

            # Once the window exceeds width k, drop the leftmost character.
            if i >= k:
                leaving = ord(s[i - k]) - ord("a")
                if window[leaving] == need[leaving]:
                    matches -= 1
                window[leaving] -= 1
                if window[leaving] == need[leaving]:
                    matches += 1

            # A full-width window with all 26 letters matching is an anagram.
            if i >= k - 1 and matches == 26:
                result.append(i - k + 1)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` characters enters the window once and leaves at most once. Every entry and exit performs a constant number of array updates and `matches` adjustments. There is no per-window 26-slot comparison because `matches` is maintained incrementally, so the total work is linear in `n`.

##### Space Complexity: `O(1)`

The `need` and `window` arrays are fixed at 26 slots, and `matches` is a single integer, all independent of input size. The `result` list is output rather than auxiliary space.

#### Key Insights

- A fixed-size window fits perfectly because every anagram of `p` has exactly
  length `k`.
- Maintaining counts incrementally turns the brute force's repeated `O(k)`
  recount into `O(1)` per slide.
- The `matches` counter avoids re-comparing all 26 slots each step: only the one
  or two slots that actually change can flip a letter's match status.
- Indexing a 26-slot array by `ord(c) - ord('a')` keeps every count update
  constant time with no hashing, which is what makes the extra `matches` bookkeeping worth its lines.

### Sliding Window with Counter

#### Derivation

The two previous solutions tally letters by hand because doing so keeps every operation constant time. Reaching for [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) does not change the algorithm at all: the window still advances one character at a time, and each character still enters and leaves exactly once. What changes is the amount of machinery on the page. `Counter` builds a frequency map in a single call and compares two maps with `==`, so the `need` construction loop, the `ord(c) - ord('a')` arithmetic, and the entire `matches` apparatus all disappear, replaced by one dictionary comparison per window.

1. If `p` is longer than `s`, return an empty list.
2. Build `need = Counter(p)` and seed `window = Counter(s[:k])` from the first
   window, recording index `0` when those two already agree.
3. For each `i` from `k` to `n - 1`, increment the entering character `s[i]` and
   decrement the leaving character `s[i - k]`.
4. Delete any key whose count drops to zero. `Counter` equality is plain
   dictionary equality, so a lingering `c: 0` entry keeps `window` unequal to `need` even when the letters genuinely match.
5. Test `window == need` after each slide, appending the start index `i - k + 1`
   on a match.

Step 4 is the one trap this version introduces. The count array can leave a slot sitting at zero harmlessly, because it compares fixed positions; a `Counter` compares key sets, so a zeroed key must be pruned rather than left behind.

#### Walkthrough

Run it on Example 1: `s = "cbaebabacd"`, `p = "abc"`, so `n = 10` and `k = 3`. `need` is `{a: 1, b: 1, c: 1}`, and `window` is seeded from `s[:3] = "cba"`, which already equals `need`, so `0` is recorded before the loop starts.

Each row shows one iteration after both updates have been applied, noting the key deleted whenever a count reaches zero:

| `i` | enters | leaves | `window` after | `== need`? |
| --- | --- | --- | --- | --- |
| `3` | `e` | `c` (key deleted) | `a:1, b:1, e:1` | no |
| `4` | `b` | `b` | `a:1, b:1, e:1` | no |
| `5` | `a` | `a` | `a:1, b:1, e:1` | no |
| `6` | `b` | `e` (key deleted) | `a:1, b:2` | no |
| `7` | `a` | `b` | `a:2, b:1` | no |
| `8` | `c` | `a` | `a:1, b:1, c:1` | yes: append `6` |
| `9` | `d` | `b` (key deleted) | `a:1, c:1, d:1` | no |

At `i = 3` the leaving `c` takes its count to zero and the key is dropped; without that deletion `window` would read `a:1, b:1, c:0, e:1` and could never compare equal to `need` again, even once the letters lined up. At `i = 8` the window covers `s[6:9] = "bac"`, whose counts match `need` exactly, so the start index `8 - 3 + 1 = 6` is appended. The scan ends with `result = [0, 6]`, matching the expected Output `[0,6]`.

#### Solution

The same slide as before, with the counting delegated to the standard library.

```python
from collections import Counter
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n, k = len(s), len(p)
        if k > n:
            return []

        need = Counter(p)
        window = Counter(s[:k])

        result = [0] if window == need else []
        for i in range(k, n):
            window[s[i]] += 1
            leaving = s[i - k]
            window[leaving] -= 1
            # Counter equality is dict equality, so a zeroed key must not linger.
            if window[leaving] == 0:
                del window[leaving]
            if window == need:
                result.append(i - k + 1)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * 26)`

Every character still enters and leaves the window once, and each of those updates hashes a single character. The difference from the fixed-array version is the `window == need` test, which walks the keys of both counters instead of reading one integer. Since `s` and `p` hold only lowercase letters, that comparison spans at most 26 keys, so the bound is `O(n * 26)`. The alphabet is fixed, so this still reduces to `O(n)`, but with a visibly larger constant than the `matches == 26` test.

##### Space Complexity: `O(1)`

Each counter holds at most 26 keys no matter how long the input grows, so auxiliary space is bounded by the alphabet. The hash table carries more per-entry overhead than a plain 26-slot list, which does not affect the bound.

#### Key Insights

- The algorithm is untouched: only the container holding the frequencies differs,
  which shows the sliding window is independent of how counts are stored.
- Pruning zero-valued keys is a correctness requirement rather than tidiness,
  because `Counter` equality is dictionary equality and `c: 0` is not the same as an absent `c`.
- Dropping `matches` trades a single-integer test for a map comparison per
  window: identical complexity class, about a third fewer lines, a larger constant.
- This is the version worth writing first under interview pressure, with the
  fixed-array form as the natural answer when asked to shave the constant.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O((n - k + 1) * k)` because each of the
  `n - k + 1` windows is recounted from scratch over `k` characters.
- **Sliding Window with Fixed-Size Count Array**: `O(n)` because each character
  enters and leaves the window exactly once with constant-time updates.
- **Sliding Window with Counter**: `O(n * 26)`, the same linear scan carrying a
  26-key map comparison at every window instead of a single integer test.

### Space Complexity

- **Brute Force**: `O(1)`, using only fixed 26-slot arrays.
- **Sliding Window with Fixed-Size Count Array**: `O(1)`, also using fixed
  26-slot arrays plus a single integer counter.
- **Sliding Window with Counter**: `O(1)`, two counters bounded at 26 keys each,
  though a hash table costs more per entry than a plain list.

All three use constant auxiliary space; they differ in time and in code volume.

### Trade-offs

- The brute force is the easiest to reason about: build a count, compare, repeat.
  Its cost is the repeated work across overlapping windows, which becomes quadratic when `k` is a large fraction of `n`.
- The fixed-array sliding window adds the bookkeeping of incremental updates and
  a `matches` counter, trading a little extra logic for a linear runtime that scales to the largest allowed inputs.
- The `Counter` sliding window keeps that linear runtime while cutting about a
  third of the lines, paying for the brevity with hashing and a per-window map comparison. It also introduces the one hazard the array version cannot have: a zeroed key must be deleted or every later comparison fails.

### When to Use Each

- **Brute Force**: Suitable when `s` is short, `p` is tiny, or clarity matters
  more than speed, such as a first pass or a teaching example.
- **Sliding Window with Fixed-Size Count Array**: Preferred for any sizeable
  input and for the constraint ceiling of `3 * 10^4`, where the quadratic approach risks being too slow, and wherever the tightest constant matters.
- **Sliding Window with Counter**: The Pythonic default. Reach for it when
  readability outweighs a constant factor, and when writing the solution quickly and correctly matters more than squeezing the inner loop.

### Optimization Notes

- The key optimization is recognizing that consecutive windows share all but two
  characters, so the count can be updated rather than rebuilt.
- The `matches` counter is a second-level optimization: it replaces an `O(26)`
  full-array comparison per window with `O(1)` adjustments to a single integer.
- Mapping letters to a fixed 26-slot array (via `ord(c) - ord('a')`) removes both
  the hashing and the import, at the cost of the `ord` arithmetic and the extra `matches` bookkeeping that `Counter` hides.
