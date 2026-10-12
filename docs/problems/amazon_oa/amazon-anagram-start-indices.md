# [All Anagram Start Indices](https://www.fastprep.io/problems/amazon-anagram-start-indices)

**Medium** | **NN minutes** | **String, Hash Table, Sliding Window**

Given lowercase strings s and p, return every starting index where a substring of s is an anagram of p.

Return indices in increasing order. Overlapping matches are included.

## Examples

### Example 1

**Input:** `s = "acbadabcaa"`, `p = "aabc"`

**Output:** `[0,5,6]`

**Explanation:** The length-four substrings at 0, 5, and 6 have exactly the pattern frequencies.

### Example 2

**Input:** `s = "cbaebabacd"`, `p = "abc"`

**Output:** `[0,6]`

**Explanation:** cba and bac are anagrams of abc.

### Example 3

**Input:** `s = "abab"`, `p = "ab"`

**Output:** `[0,1,2]`

**Explanation:** All three length-two windows match, including overlaps.

## Constraints

- `1 ≤ s.length, p.length ≤ 100000.`
- `s and p contain only lowercase English letters.`

## Solutions

### Brute Force

#### Derivation

The first question is what "anagram" means operationally: a substring of `s` is an anagram of `p` exactly when it has length `k = len(p)` and the same multiset of characters, which two frequency counts can verify. Order never matters, only the count of each of the 26 lowercase letters. The most direct strategy tries every possible window of width `k` and rebuilds its frequency count independently:

1. If `p` is longer than `s`, no anagram can exist, so return an empty list.
2. Build `need`, a fixed 26-slot array holding the frequency of each lowercase
   letter in `p`. Indexing by `ord(c) - ord("a")` maps `'a'..'z'` to `0..25`.
3. For each start index `start` from `0` to `n - k`, scan the `k` characters of
   the window `s[start:start + k]` and tally them into a fresh `window` array.
4. Compare `window` to `need`. Python compares the two 26-element lists slot by
   slot, so a match means the window is an anagram of `p`.
5. Append `start` on every match, then return the collected start indices.

This rebuilds the entire count for every window, sharing no work between overlapping windows, which makes it simple but redundant.

#### Walkthrough

Let us watch the Brute Force run on Example 1: `s = "acbadabcaa"`, `p = "aabc"`.

First build `need` for `p = "aabc"`. The nonzero slots are `a: 2`, `b: 1`, `c: 1`; here `n = 10` and `k = 4`, so the loop tries window starts `0` to `n - k = 6`. For each start the window is rebuilt from scratch over `s[start:start + 4]`; the "counts" column lists only the nonzero slots:

| `start` | window | counts | `== need`? |
| --- | --- | --- | --- |
| `0` | `"acba"` | `a:2, b:1, c:1` | yes: append `0` |
| `1` | `"cbad"` | `a:1, b:1, c:1, d:1` | no |
| `2` | `"bada"` | `a:2, b:1, d:1` | no |
| `3` | `"adab"` | `a:2, b:1, d:1` | no |
| `4` | `"daba"` | `a:2, b:1, d:1` | no |
| `5` | `"abca"` | `a:2, b:1, c:1` | yes: append `5` |
| `6` | `"bcaa"` | `a:2, b:1, c:1` | yes: append `6` |

At `start = 0` the window `"acba"` carries exactly two `a`s, one `b`, and one `c`, matching `need`, so `0` is appended. The middle windows each carry a `d` or lack a second `a`, so none match until `start = 5`, where `"abca"` and then `"bcaa"` line up again. The loop ends and the function returns `[0, 5, 6]`, matching the expected Output.

#### Solution

The code is the walkthrough's table: rebuild `window` for each start index and compare it to `need`.

```python
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        length_s, window_size = len(s), len(p)
        if window_size > length_s:
            return []

        need = [0] * 26
        for char in p:
            need[ord(char) - ord("a")] += 1

        matches: List[int] = []
        last_start = length_s - window_size
        for start in range(last_start + 1):
            window = [0] * 26
            for position in range(start, start + window_size):
                window[ord(s[position]) - ord("a")] += 1
            if window == need:
                matches.append(start)

        return matches
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n - k + 1) × k)`

There are `n - k + 1` window positions, and each one recounts `k` characters before a constant 26-slot comparison. The recount dominates once `k` exceeds the alphabet size, and in the worst case (`k` close to `n`) this is quadratic in `n`; at the constraint ceiling of `10^5` that is too slow.

##### Space Complexity: `O(1)`

Both `need` and the per-window `window` array are fixed at 26 slots regardless of input size; the `matches` list is output, not auxiliary working space.

#### Key Insights

- Anagram detection reduces to comparing character frequency counts, since order does not matter.
- A fixed 26-slot array indexed by `ord(c) - ord("a")` compares in constant time and needs no hashing.
- The inefficiency comes from discarding each window's count and rebuilding the next from scratch, ignoring that adjacent windows differ by only two characters.

### Sliding Window with Fixed-Size Count Array

#### Derivation

The brute force discards each window's count and rebuilds the next from scratch, even though adjacent windows overlap heavily: sliding one step removes a single character on the left and adds a single character on the right. Rather than recounting, we maintain the window's 26-slot count incrementally and track a running `matches` value, the number of letters whose window count already equals the needed count. In plain text the invariant is `matches == number of letters with window == need`, which is what makes the test `matches == 26` equivalent to comparing the two arrays outright:

1. If `p` is longer than `s`, return an empty list.
2. Build `need` and a zeroed `window`, both fixed 26-slot arrays, then initialize
   `matches` by comparing the two arrays slot by slot (initially the 26 zeros of
   `window` match every zero slot of `need`).
3. Walk `position` across `s`. For the entering character, adjust `matches`
   before and after incrementing its slot: a slot only counts as a match when
   the two values are equal, so decrement `matches` if it was matching, bump
   the count, then increment `matches` if it now matches.
4. Once `position >= window_size`, the window has grown past width `window_size`,
   so apply the mirror update for the leaving character `s[position -
   window_size]`, keeping the window exactly `window_size` wide.
5. When the window is full width (`position >= window_size - 1`) and
   `matches == 26`, every letter agrees, so the window is an anagram; record its
   start index `position - window_size + 1`.

Each character's entry and exit touches a single slot and adjusts `matches` in constant time, so the whole scan is linear.

#### Walkthrough

Let us run the scan on Example 3: `s = "abab"`, `p = "ab"`, so `n = 4` and `window_size = 2`. `need` holds `a: 1, b: 1`, and `window` starts all zeros, so the initial slot-by-slot comparison finds the 24 letters absent from both arrays agreeing while the `a` and `b` slots disagree: `matches = 24`.

Each line below shows one loop iteration after its updates: the entering character, the leaving character once `position >= window_size`, the nonzero slots of `window`, and `matches`:

```text
pos=0  enter 'a'             window a:1        matches 25    window not yet 2 wide
pos=1  enter 'b'             window a:1, b:1   matches 26    append 0
pos=2  enter 'a', leave 'a'  window a:1, b:1   matches 26    append 1
pos=3  enter 'b', leave 'b'  window a:1, b:1   matches 26    append 2
```

At `pos = 0` the `a` slot reaches its needed count, lifting `matches` to `25`, but the window is not yet `window_size` wide, so nothing is recorded. At `pos = 1` the `b` slot agrees too, `matches` saturates at `26`, and start index `0` is appended. At `pos = 2` the entering `a` first pushes its slot to `2` (dropping `matches` to `25` mid-update), then the leaving `a` at `s[0]` restores the slot to `1` and `matches` to `26`: the window `"ba"` is an anagram, so `1` is appended. `pos = 3` mirrors it with `b`, appending `2`. The final `matches_list = [0, 1, 2]` matches the expected Output `[0,1,2]`, including both overlapping windows.

#### Solution

The code is the walkthrough's per-character update: the decrement-bump-increment triple for the entering slot, its mirror for the leaving slot, and the `matches == 26` test.

```python
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        length_s, window_size = len(s), len(p)
        if window_size > length_s:
            return []

        need = [0] * 26
        window = [0] * 26
        for char in p:
            need[ord(char) - ord("a")] += 1

        matches = sum(
            1 for slot in range(26) if need[slot] == window[slot]
        )
        matches_list: List[int] = []

        for position in range(length_s):
            entering = s[position]
            if window[ord(entering) - ord("a")] == need[ord(entering) - ord("a")]:
                matches -= 1
            window[ord(entering) - ord("a")] += 1
            if window[ord(entering) - ord("a")] == need[ord(entering) - ord("a")]:
                matches += 1

            if position >= window_size:
                leaving = s[position - window_size]
                if window[ord(leaving) - ord("a")] == need[ord(leaving) - ord("a")]:
                    matches -= 1
                window[ord(leaving) - ord("a")] -= 1
                if window[ord(leaving) - ord("a")] == need[ord(leaving) - ord("a")]:
                    matches += 1

            if position >= window_size - 1 and matches == 26:
                matches_list.append(position - window_size + 1)

        return matches_list
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` characters enters the window once and leaves at most once, and every entry and exit performs a constant number of array updates and `matches` adjustments. There is no per-window 26-slot comparison because `matches` is maintained incrementally, so the total work is linear in `n`, which is what makes the `10^5` constraint ceiling comfortable.

##### Space Complexity: `O(1)`

The `need` and `window` arrays are fixed at 26 slots and `matches` is a single integer, all independent of input size; the output list is not auxiliary space.

#### Key Insights

- A fixed-size window fits perfectly because every anagram of `p` has exactly length `len(p)`.
- Maintaining counts incrementally turns the brute force's repeated `O(k)` recount into `O(1)` per slide.
- The `matches` counter avoids re-comparing all 26 slots each step: only the one or two slots that actually change can flip a letter's match status.
- The decrement-bump-increment triple around each count write is what keeps `matches` honest: skipping either half leaves a stale verdict for that slot.

### Sliding Window with Counter

#### Derivation

The two previous solutions tally letters by hand because doing so keeps every operation constant time. Reaching for [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) does not change the algorithm at all: the window still advances one character at a time, and each character still enters and leaves exactly once. What changes is the amount of machinery on the page. `Counter` builds a frequency map in a single call and compares two maps with `==`, so the `need` construction loop, the `ord` arithmetic, and the entire `matches` apparatus all disappear, replaced by one dictionary comparison per window:

1. If `p` is longer than `s`, return an empty list.
2. Build `need = Counter(p)` and seed `window = Counter(s[:window_size])` from
   the first window, recording index `0` when those two already agree.
3. For each `position` from `window_size` to `n - 1`, increment the entering
   character `s[position]` and decrement the leaving character
   `s[position - window_size]`.
4. Delete any key whose count drops to zero. `Counter` equality is plain
   dictionary equality, so a lingering `c: 0` entry keeps `window` unequal to
   `need` even when the letters genuinely match.
5. Test `window == need` after each slide, appending the start index
   `position - window_size + 1` on a match.

Step 4 is the one trap this version introduces. The count array can leave a slot sitting at zero harmlessly, because it compares fixed positions; a `Counter` compares key sets, so a zeroed key must be pruned rather than left behind.

#### Walkthrough

Run it on Example 1: `s = "acbadabcaa"`, `p = "aabc"`, so `n = 10` and `window_size = 4`. `need` is `{a: 2, b: 1, c: 1}`, and `window` is seeded from `s[:4] = "acba"`, which already equals `need`, so `0` is recorded before the loop starts.

Each row shows one iteration after both updates have been applied, noting the key deleted whenever a count reaches zero:

| `position` | enters | leaves | `window` after | `== need`? |
| --- | --- | --- | --- | --- |
| `4` | `d` | `a` | `a:1, b:1, c:1, d:1` | no |
| `5` | `a` | `c` (key deleted) | `a:2, b:1, d:1` | no |
| `6` | `b` | `b` | `a:2, b:1, d:1` | no |
| `7` | `c` | `a` | `a:1, b:1, c:1, d:1` | no |
| `8` | `a` | `d` (key deleted) | `a:2, b:1, c:1` | yes: append `5` |
| `9` | `a` | `a` | `a:2, b:1, c:1` | yes: append `6` |

At `position = 5` the leaving `c` drops to zero and its key is deleted; without that deletion `window` would read `a:2, b:1, c:0, d:1` and could never compare equal to `need` again, even once the letters lined up. At `position = 8` the entering `a` restores the second `a` just as the leaving `d` is pruned, and the window's counts match `need` exactly, so the start index `8 - 4 + 1 = 5` is appended; `position = 9` slides onto another match and appends `6`. The scan ends with `[0, 5, 6]`, matching the expected Output `[0,5,6]`.

#### Solution

The same slide as before, with the counting delegated to the standard library.

```python
from collections import Counter
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        length_s, window_size = len(s), len(p)
        if window_size > length_s:
            return []

        need = Counter(p)
        window = Counter(s[:window_size])

        matches: List[int] = [0] if window == need else []
        for position in range(window_size, length_s):
            window[s[position]] += 1
            leaving = s[position - window_size]
            window[leaving] -= 1
            if window[leaving] == 0:
                del window[leaving]
            if window == need:
                matches.append(position - window_size + 1)

        return matches
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × 26)`

Every character still enters and leaves the window once, and each of those updates hashes a single character. The difference from the fixed-array version is the `window == need` test, which walks the keys of both counters instead of reading one integer; since `s` and `p` hold only lowercase letters, that comparison spans at most 26 keys, so the bound is `O(n × 26)`. The alphabet is fixed, so this still reduces to `O(n)`, but with a visibly larger constant than the `matches == 26` test.

##### Space Complexity: `O(1)`

Each counter holds at most 26 keys no matter how long the input grows, so auxiliary space is bounded by the alphabet; the hash table carries more per-entry overhead than a plain 26-slot list, which does not affect the bound.

#### Key Insights

- The algorithm is untouched: only the container holding the frequencies differs, which shows the sliding window is independent of how counts are stored.
- Pruning zero-valued keys is a correctness requirement rather than tidiness, because `Counter` equality is dictionary equality and `c: 0` is not the same as an absent `c`.
- Dropping `matches` trades a single-integer test for a map comparison per window: identical complexity class, about a third fewer lines, a larger constant.
- This is the version worth writing first under interview pressure, with the fixed-array form as the natural answer when asked to shave the constant.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O((n - k + 1) × k)` - each of the `n - k + 1` windows is recounted from scratch over `k` characters.
- **Sliding Window with Fixed-Size Count Array**: `O(n)` - each character enters and leaves the window exactly once with constant-time updates.
- **Sliding Window with Counter**: `O(n × 26)` - the same linear scan carrying a 26-key map comparison at every window instead of a single integer test.

### Space Complexity

- **Brute Force**: `O(1)` - only fixed 26-slot arrays.
- **Sliding Window with Fixed-Size Count Array**: `O(1)` - fixed 26-slot arrays plus a single integer counter.
- **Sliding Window with Counter**: `O(1)` - two counters bounded at 26 keys each, though a hash table costs more per entry than a plain list.

All three use constant auxiliary space; they differ in time and in code volume.

### Trade-offs

- The brute force is the easiest to reason about: build a count, compare, repeat. Its cost is the repeated work across overlapping windows, which becomes quadratic when `k` is a large fraction of `n`.
- The fixed-array sliding window adds the bookkeeping of incremental updates and a `matches` counter, trading a little extra logic for a linear runtime that scales to the largest allowed inputs.
- The `Counter` sliding window keeps that linear runtime while cutting about a third of the lines, paying for the brevity with hashing and a per-window map comparison. It also introduces the one hazard the array version cannot have: a zeroed key must be deleted or every later comparison fails.

### When to Use Each

- **Brute Force**: suitable when `s` is short, `p` is tiny, or clarity matters more than speed, such as a first pass or a teaching example.
- **Sliding Window with Fixed-Size Count Array** (Recommended): for any sizeable input and for the constraint ceiling of `10^5`, where the quadratic approach is too slow, and wherever the tightest constant matters.
- **Sliding Window with Counter**: the Pythonic default; reach for it when readability outweighs a constant factor and writing the solution quickly and correctly matters most.

### Optimization Notes

- The key optimization is recognizing that consecutive windows share all but two characters, so the count can be updated rather than rebuilt.
- The `matches` counter is a second-level optimization: it replaces an `O(26)` full-array comparison per window with `O(1)` adjustments to a single integer.
- Mapping letters to a fixed 26-slot array (via `ord(c) - ord("a")`) removes both the hashing and the import, at the cost of the `ord` arithmetic and the extra `matches` bookkeeping that `Counter` hides.
- Overlapping matches need no special handling in any approach: every window position is tested independently, so adjacent hits like Example 3's `[0, 1, 2]` fall out naturally.
