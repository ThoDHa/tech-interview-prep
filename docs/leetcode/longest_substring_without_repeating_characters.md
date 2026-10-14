# [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

**Medium** | **25 minutes** | **Hash Table, String, Sliding Window**

**Pattern:** [Sliding Window](../patterns/sliding_window/intuition.md)

**Algorithm:** [Sliding window](https://usaco.guide/gold/sliding-window) · [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/longest_substring_without_repeating_characters/solution.py`](../../practice/longest_substring_without_repeating_characters/solution.py)

Given a string `s`, find the length of the longest substring without repeating characters.

## Examples

### Example 1

**Input:** `s = "abcabcbb"`

**Output:** `3`

**Explanation:** The answer is "abc", with the length of 3.

### Example 2

**Input:** `s = "bbbbb"`

**Output:** `1`

**Explanation:** The answer is "b", with the length of 1.

### Example 3

**Input:** `s = "pwwkew"`

**Output:** `3`

**Explanation:** The answer is "wke", with the length of 3. Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

### Example 4

**Input:** `s = ""`

**Output:** `0`

## Constraints

- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols and spaces.

## Deriving the Solution

The answer is the widest window of consecutive characters containing no duplicate. Every solution below examines such windows; they differ in how much of an examined window survives when a duplicate appears.

1. **Start literal.** Anchor a start index, grow the substring rightward while
   collecting its characters into a set, and stop at the first repeat; try every anchor. Each anchor rescans up to `n` characters, costing `O(n^2)`: see [Brute Force](#brute-force).
2. **Stop restarting.** When a repeat appears, the brute force throws the whole
   window away and rebuilds most of it from the next anchor, yet only the prefix up to the duplicate is invalid. Keep the window and shrink it from the left just past the duplicate: each character then enters and leaves the window at most once, giving `O(2n)`: see [Sliding Window with Set](#sliding-window-with-set).
3. **Jump instead of shuffle.** The set version shrinks one character at a time
   because a set records only presence, not position. Recording each character's last-seen index lets `left` jump directly past the duplicate in a single assignment, touching each character exactly once: see [Sliding Window with Last-Seen Index](#sliding-window-with-last-seen-index).

## Solutions

### Brute Force

#### Derivation

The most direct idea is to consider every substring and keep the longest one that has no repeated character. Rather than re-scanning each substring from scratch, we anchor a `start` index and grow the substring one character at a time, collecting the characters into a `seen` set. The moment the next character is already in the set, this substring cannot grow any further, so we stop and move the anchor forward.

1. Initialize `longest = 0`.
2. For each `start` index, begin an empty `seen` set.
3. Extend `end` from `start` to the end of the string.
4. If `s[end]` is already in `seen`, the substring would repeat a character, so
   break out of the inner loop.
5. Otherwise add `s[end]` to `seen` and update `longest` with the current
   substring length `end - start + 1`.
6. Return `longest`.

#### Walkthrough

Let us watch the brute force run on Example 1: `s = "abcabcbb"` (indices `0` through `7`). The outer loop fixes each `start`; the inner loop grows `end` and fills a fresh `seen` set until a repeat forces a `break`. We track `longest` across the whole run.

The first anchor, `start = 0`, does the heavy lifting:

| `start` | `end` | `s[end]` | action | `seen` after | window length | `longest` |
|---------|-------|----------|--------|--------------|---------------|-----------|
| 0 | 0 | `a` | add | `{a}` | 1 | 1 |
| 0 | 1 | `b` | add | `{a, b}` | 2 | 2 |
| 0 | 2 | `c` | add | `{a, b, c}` | 3 | 3 |
| 0 | 3 | `a` | already in `seen`: `break` | - | - | 3 |

The substring `"abc"` reaches length `3`, then `s[3] = 'a'` repeats `s[0]`, so the inner loop breaks and the anchor moves on. Notice the restart: the next `start` throws away the `{a, b, c}` we just built and rediscovers it from scratch.

Every later anchor follows the same shape but never beats `3`:

| `start` | grows to | breaks at `s[end]` | best window length |
|---------|----------|--------------------|--------------------|
| 1 | `"bca"` | `b` (index 4) | 3 |
| 2 | `"cab"` | `c` (index 5) | 3 |
| 3 | `"abc"` | `b` (index 6) | 3 |
| 4 | `"bc"` | `b` (index 6) | 2 |
| 5 | `"cb"` | `b` (index 7) | 2 |
| 6 | `"b"` | `b` (index 7) | 1 |
| 7 | `"b"` | end of string | 1 |

No anchor produces a window longer than `3`, so `longest` stays at `3`. The function returns `3`, which matches the expected Output for Example 1.

#### Solution

The code is the walkthrough's anchor-and-grow loop written down.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        longest = 0

        # Try every possible starting index
        for start in range(len(s)):
            seen = set()
            # Extend the substring to the right until a repeat appears
            for end in range(start, len(s)):
                if s[end] in seen:
                    break
                seen.add(s[end])
                longest = max(longest, end - start + 1)

        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` starting positions, the inner loop extends until it hits a repeat, scanning up to `n` characters. Each membership test on the set is `O(1)` on average, so the total work is quadratic.

##### Space Complexity: `O(min(n, charset))`

The `seen` set holds at most one entry per distinct character in the current substring, bounded by both the string length and the size of the character set.

#### Key Insights

- Trying every substring is the most literal reading of the problem; no special
  pattern is required to derive it.
- Growing a substring with a running `seen` set avoids re-checking each candidate
  from scratch, dropping the naive `O(n^3)` to `O(n^2)`.
- The wasted work is the restart: when the inner loop breaks, everything learned
  about the prefix is discarded and recomputed from the next `start`. Removing that waste is exactly what the sliding window does.

### Sliding Window with Set

#### Derivation

The brute force's restart is the waste to remove: after a break, everything between the old anchor and the duplicate is duplicate-free and will be verified again anyway. Keep it. We maintain a [sliding window](https://usaco.guide/gold/sliding-window) `[left, right]` whose characters are kept in a set, guaranteeing the window never holds a duplicate. The `right` pointer expands the window one character at a time. Whenever the incoming character already lives in the window, we advance `left` one step at a time, removing each evicted character from the set, until the duplicate has been dropped.

1. Initialize an empty `seen` set, `longest = 0`, and `left = 0`.
2. Move `right` across each character of `s`.
3. While the character at `right` is already in `seen`, remove `s[left]` from the
   set and advance `left`.
4. Add the character at `right` to `seen`.
5. The window length `right - left + 1` is a candidate for `longest`.
6. Return `longest`.

#### Walkthrough

Let us slide the window across Example 1: `s = "abcabcbb"` (indices `0` through `7`). Each event is either an expansion (`right` moves and the character joins `seen`) or a shrink step (`s[left]` leaves `seen` and `left` advances), forced by an incoming duplicate:

```text
right=0  'a' not in seen -> add    window [0,0] "a"    seen={a}      longest=1
right=1  'b' not in seen -> add    window [0,1] "ab"   seen={a,b}    longest=2
right=2  'c' not in seen -> add    window [0,2] "abc"  seen={a,b,c}  longest=3
right=3  'a' in seen: remove s[0]='a', left=1
         add 'a'                   window [1,3] "bca"  seen={b,c,a}  longest=3
right=4  'b' in seen: remove s[1]='b', left=2
         add 'b'                   window [2,4] "cab"  seen={c,a,b}  longest=3
right=5  'c' in seen: remove s[2]='c', left=3
         add 'c'                   window [3,5] "abc"  seen={a,b,c}  longest=3
right=6  'b' in seen: remove s[3]='a', left=4
             still in: remove s[4]='b', left=5
         add 'b'                   window [5,6] "cb"   seen={c,b}    longest=3
right=7  'b' in seen: remove s[5]='c', left=6
             still in: remove s[6]='b', left=7
         add 'b'                   window [7,7] "b"    seen={b}      longest=3
```

The step at `right = 6` shows the shrink loop running twice: evicting `'a'` does not remove the duplicate `'b'`, so `left` keeps advancing until it does. Unlike the brute force, the characters between the duplicates are never rediscovered: they simply stay in the window. The widest window seen had length `3` (first reached by `"abc"`), so the function returns `3`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's expand-and-shrink loop: the inner `while` is the shrink steps.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Tracks the characters currently inside the window
        seen = set()
        longest = 0
        left = 0

        for right in range(len(s)):
            # If the new character duplicates one in the window, shrink from the
            # left one step at a time until that duplicate is removed
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            longest = max(longest, right - left + 1)

        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2n)`

Each character is added to the set once by `right` and removed at most once by `left`. In the worst case the pointers together traverse the string twice, which is linear, written here as `O(2n)` to make the double traversal explicit.

##### Space Complexity: `O(min(n, charset))`

The set holds at most one entry per distinct character in the window, bounded by both the string length and the size of the character set.

#### Key Insights

- A set gives `O(1)` average membership tests, which is exactly what the
  duplicate check needs.
- The `left` pointer only ever moves forward, so although there is a nested
  `while`, the total movement is bounded and the pass stays linear.
- This is the most fundamental form of the sliding window: it shrinks one
  character at a time rather than jumping.

### Sliding Window with Last-Seen Index

#### Derivation

The set version shrinks one character at a time because a set records only that a character is present, not where it is. Knowing *where* the duplicate sits would let `left` leap past it in a single move. So we keep the sliding window `[left, right]` that always holds a substring with no repeated characters, but replace the set with a [hash map](https://en.wikipedia.org/wiki/Hash_table) `last_seen` that records the most recent index of each character. When the current character has been seen at an index that falls inside the current window, the window must shrink from the left past that occurrence, and the stored index says exactly where that is.

1. Initialize an empty `last_seen` map, `longest = 0`, and `left = 0`.
2. Iterate `right` over each character `char` in `s`.
3. If `char` is in `last_seen` and its stored index is at or after `left`, it
   lies inside the window, so set `left = last_seen[char] + 1`.
4. Update `last_seen[char]` to the current index `right`.
5. The current window length is `right - left + 1`; update `longest` with it.
6. Return `longest`.

The guard `last_seen[char] >= left` is essential: a character may exist in the map from a position that has already been passed by `left`, and that stale entry must not drag `left` backward. The Invariant below is the formal statement of why, resting on `no duplicate in s[left..right]` plus `left never decreases`.

#### Invariant

The loop maintains two properties. The first is the window property, true at the end of every iteration:

$$ \forall\, i \ne j \in [\,\textit{left},\ \textit{right}\,]\ :\quad s[i] \ne s[j] $$

```text
for all i != j with left <= i <= right and left <= j <= right:  s[i] != s[j]
```

No character repeats inside `[left, right]`, so `right - left + 1` is always the length of a valid substring and taking a running maximum over it is sound.

The second says what `last_seen` holds, and it is deliberately *not* window-scoped:

$$ \textit{last\_seen}[c] = \max \{\, i \le \textit{right} \ :\ s[i] = c \,\} $$

```text
last_seen[c] = max { i <= right : s[i] == c }
               for every c in s[0..right]
```

That is the last occurrence anywhere in the prefix, which may sit far to the left of `left`.

Expansion is the only step that can break the first property, and only `char = s[right]` can break it, since the rest of the window was already duplicate-free. The previous occurrence of `char` sits at `last_seen[char]`, and it lies inside the window exactly when `last_seen[char] >= left`. The jump `left = last_seen[char] + 1` evicts it and nothing beyond it, restoring the property with the smallest possible move. When `last_seen[char] < left` the entry is stale, no duplicate is entering, and `left` must hold still.

That stale case is why the conjunct cannot be dropped. Testing only `char in last_seen` would assign `left = last_seen[char] + 1` from an index already passed, a value that can be *smaller* than the current `left`. On `"abba"` at `right = 3`, `last_seen['a'] == 0` while `left == 2`, so the window would rewind to `[1, 3]` and swallow both `b` characters.

The conjunct therefore also gives monotonicity: `left` is reassigned only when `last_seen[char] >= left`, so it never decreases. Both pointers advance at most `n` times, and at exit `longest` is the maximum width over all valid windows.

#### Walkthrough

The official Examples exercise the forward jump but never leave a stale map entry, so the `>= left` guard's rejecting branch would not appear in any of them. To see both behaviors we use the small tailored input `s = "abba"`, whose final character carries a last-seen index that lies behind the window:

```text
right=0  'a' new                                 left=0  window [0,0] "a"   longest=1
         last_seen = {a: 0}
right=1  'b' new                                 left=0  window [0,1] "ab"  longest=2
         last_seen = {a: 0, b: 1}
right=2  'b' seen at 1, and 1 >= left=0 -> jump  left=2  window [2,2] "b"   longest=2
         last_seen = {a: 0, b: 2}
right=3  'a' seen at 0, but 0 >= left=2 is False -> stale, left holds
                                                 left=2  window [2,3] "ba"  longest=2
         last_seen = {a: 3, b: 2}
```

At `right = 2` the duplicate `'b'` sits inside the window, so `left` jumps straight to `last_seen['b'] + 1 = 2` in a single assignment: no step-by-step eviction. At `right = 3` the map still remembers `'a'` at index `0`, but that occurrence lies behind `left = 2`: the entry is stale, the guard rejects it, and `left` correctly holds still. Dropping the guard would rewind `left` to `1` and count the invalid window `"bba"`. The widest valid window had length `2` (`"ab"`, later tied by `"ba"`), so the function returns `2`.

#### Solution

The code is the walkthrough's jump rule: one guarded assignment replaces the shrink loop.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Maps each character to the index where it was last seen
        last_seen = {}
        longest = 0
        left = 0

        for right, char in enumerate(s):
            # If we have seen char inside the current window, jump the left
            # edge just past its previous occurrence
            if char in last_seen and last_seen[char] >= left:
                left = last_seen[char] + 1
            last_seen[char] = right
            longest = max(longest, right - left + 1)

        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is visited once by `right`, and `left` only ever moves forward. Every hash map lookup and update is `O(1)` on average, so the total work is linear in the length of `s`.

##### Space Complexity: `O(min(n, m))`

The map stores at most one entry per distinct character. Its size is bounded by both the length `n` and the size `m` of the character set (English letters, digits, symbols, and spaces), giving `O(min(n, m))`.

#### Key Insights

- A "without repeating characters" constraint maps directly onto a sliding
  window that never contains a duplicate.
- Storing the last-seen index lets `left` jump in one step instead of shrinking
  the window one character at a time, which keeps the pass linear.
- The `>= left` check prevents stale indices outside the window from incorrectly
  rewinding `left`.
- Both pointers move only forward, so despite the nested feel there is no
  quadratic blowup.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - Every starting index grows a substring until a repeat, scanning up to `n` characters each time
- **Sliding Window with Set**: `O(2n)` - Each character is added once and removed at most once as the window shrinks step by step
- **Sliding Window with Last-Seen Index**: `O(n)` - `left` jumps directly past duplicates, so each character is touched a single time

### Space Complexity

- **Brute Force**: `O(min(n, charset))` - The `seen` set holds at most one entry per distinct character in the current substring
- **Sliding Window with Set**: `O(min(n, charset))` - The set holds at most one entry per distinct character in the window
- **Sliding Window with Last-Seen Index**: `O(min(n, m))` - The map holds at most one entry per distinct character

### Trade-offs

- The brute force is the easiest to derive: it literally tries every substring, but it discards everything it learns each time the inner loop breaks and restarts from the next index
- The set version keeps that discarded work by never restarting: it shrinks the window one character at a time until it is valid again, which is easy to reason about
- The last-seen-index version trades a slightly more subtle invariant (the `>= left` guard) for the ability to skip `left` forward in one move, halving the constant factor

### When to Use Each

- **Brute Force**: When first reasoning about the problem, or to establish a correct baseline before optimizing
- **Sliding Window with Set**: When clarity matters most, or when first learning the sliding-window pattern
- **Sliding Window with Last-Seen Index**: For the tightest single-pass solution, especially in interviews where the index jump is a desirable optimization to demonstrate

### Optimization Notes

- The two sliding-window solutions are linear; the difference between them is purely in the constant factor, since the set version may revisit characters as `left` advances
- Both improve on the brute force by reusing the window instead of recomputing each substring from scratch, turning the `O(n^2)` of repeated restarts into a single linear pass
- The last-seen-index map subsumes the set: it stores positions rather than mere presence, which is exactly what enables the forward jump
- The crucial correctness detail in the index version is the `last_seen[char] >= left` guard, which prevents a stale index from dragging `left` backward
