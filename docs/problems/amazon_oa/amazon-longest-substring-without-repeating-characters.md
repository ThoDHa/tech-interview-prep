# [Longest Substring Without Repeating Characters](https://www.fastprep.io/problems/amazon-longest-substring-without-repeating-characters)

**Medium** | **NN minutes** | **String, Sliding Window, Hash Table**

Given a string s, return the length of the longest contiguous substring whose characters are all distinct.

## Examples

### Example 1

**Input:** `s = "abcabcbb"`

**Output:** `3`

**Explanation:** abc is a longest substring with no repeated character.

### Example 2

**Input:** `s = "bbbbb"`

**Output:** `1`

**Explanation:** Every distinct-character substring contains at most one b.

### Example 3

**Input:** `s = ""`

**Output:** `0`

**Explanation:** The empty string has no nonempty substring.

## Constraints

- `0 <= s.length <= 200000.`
- `s contains printable ASCII characters.`

## Solutions

### Brute Force

#### Derivation

The most literal reading of the problem: consider every substring and keep the longest one whose characters are all distinct. Rather than re-scanning each candidate substring from scratch, anchor a `start` index and grow the substring one character at a time, collecting its characters into a `seen` set. The moment the incoming character already sits in the set, no longer substring can start at this anchor, so the inner loop stops and the anchor moves one step right.

1. Initialize `longest = 0`.
2. For each `start` index of `s`, open a fresh empty `seen` set.
3. Extend `end` from `start` toward the end of the string.
4. When `s[end]` is already in `seen`, break: every longer substring anchored at
   `start` repeats a character.
5. Otherwise add `s[end]` to `seen` and update `longest` with the window length
   `end - start + 1`.
6. Return `longest`.

#### Walkthrough

Let the brute force run on Example 1, `s = "abcabcbb"` (indices `0` through `7`). The anchor `start = 0` does the heavy lifting:

| `start` | `end` | `s[end]` | action | `seen` after | window length | `longest` |
|---------|-------|----------|--------|--------------|---------------|-----------|
| 0 | 0 | `a` | add | `{a}` | 1 | 1 |
| 0 | 1 | `b` | add | `{a, b}` | 2 | 2 |
| 0 | 2 | `c` | add | `{a, b, c}` | 3 | 3 |
| 0 | 3 | `a` | already in `seen`: break | - | - | 3 |

The substring `"abc"` reaches length `3`, then `s[3] = 'a'` repeats `s[0]`. Notice the restart: the next anchor throws away the `{a, b, c}` just built and rediscovers it from scratch.

Every later anchor follows the same shape and never beats `3`:

| `start` | grows to | breaks at | best window length |
|---------|----------|-----------|--------------------|
| 1 | `"bca"` | `b` (index 4) | 3 |
| 2 | `"cab"` | `c` (index 5) | 3 |
| 3 | `"abc"` | `b` (index 6) | 3 |
| 4 | `"bc"` | `b` (index 6) | 2 |
| 5 | `"cb"` | `b` (index 7) | 2 |
| 6 | `"b"` | `b` (index 7) | 1 |
| 7 | `"b"` | end of string | 1 |

No anchor produces a window longer than `3`, so the function returns `3`, matching the expected Output for Example 1. (Example 2, `"bbbbb"`, breaks every anchor immediately after one character and returns `1`; Example 3, the empty string, never enters the loop and returns `0`.)

#### Solution

The code is the walkthrough's anchor-and-grow loop written down.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        longest = 0

        for start in range(len(s)):
            seen = set()
            for end in range(start, len(s)):
                if s[end] in seen:
                    break
                seen.add(s[end])
                longest = max(longest, end - start + 1)

        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` anchors grows a window until a repeat, scanning up to `n` characters, and every set operation is `O(1)` on average.

##### Space Complexity: `O(min(n, charset))`

The `seen` set holds at most one entry per distinct character in the current window, bounded by the string length and by the printable-ASCII alphabet.

#### Key Insights

- No pattern is needed to derive this version: it is the problem statement translated into loops, which makes it a reliable interview baseline.
- Growing the window with a running `seen` set keeps each candidate's duplicate check constant-time instead of re-scanning the substring.
- The waste is the restart: a break discards everything learned about the prefix, and at the constraint bound of 200,000 characters the quadratic cost is far outside practical limits. Removing that restart is exactly what the sliding window does.

### Sliding Window with Set

#### Derivation

The brute force's flaw is the restart. When a repeat appears at `end`, the substring between `left` and the duplicate is still duplicate-free and will be verified again by the next anchor anyway, so throwing it away is wasted work. Keep it: maintain a [sliding window](https://en.wikipedia.org/wiki/Sliding_window) `[left, right]` whose characters live in a `seen` set, so the window never holds a duplicate. `right` expands one character per step; whenever the incoming character already sits in the window, `left` advances one step at a time, evicting each character from the set, until the duplicate has left the window.

1. Initialize an empty `seen` set, `longest = 0`, and `left = 0`.
2. Move `right` across each character of `s`.
3. While `s[right]` is already in `seen`, remove `s[left]` from the set and
   advance `left`.
4. Add `s[right]` to `seen`.
5. Update `longest` with the window length `right - left + 1`.
6. Return `longest`.

#### Walkthrough

Slide the window across Example 1, `s = "abcabcbb"`. Each line is one expansion of `right`, preceded by the shrink steps its duplicate forces:

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

The step at `right = 6` shows the shrink loop running twice: evicting `'a'` does not remove the duplicate `'b'`, so `left` keeps advancing until it does. Unlike the brute force, the surviving characters are never rediscovered; they simply stay in the window. The widest window had length `3`, first reached by `"abc"`, so the function returns `3`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's expand-and-shrink loop: the inner `while` is the shrink steps.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        longest = 0
        left = 0

        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            longest = max(longest, right - left + 1)

        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2n)`

`right` adds each character to the set exactly once and `left` removes each character at most once, so the two pointers together traverse the string at most twice; written as `O(2n)` to make the double traversal explicit.

##### Space Complexity: `O(min(n, charset))`

The set holds at most one entry per distinct character in the window, bounded by the string length and by the printable-ASCII alphabet.

#### Key Insights

- The set gives `O(1)` average membership tests, which is all the duplicate check needs.
- `left` only ever moves forward, so the nested `while` cannot blow up to quadratic time despite looking nested.
- Shrinking one character at a time is easy to reason about but repeats evictions; recording *where* the duplicate sits would let the window jump instead of shuffle.

### Sliding Window with Last-Seen Index

#### Derivation

The set version shrinks step by step because a set records only that a character is present, not where it sits. Storing each character's most recent index turns the shrink loop into a single assignment: when the incoming character's previous occurrence lies inside the window, `left` jumps directly past it. Keep the window `[left, right]` that always holds a duplicate-free substring, and replace the set with a [hash map](https://en.wikipedia.org/wiki/Hash_table) `last_seen` from character to latest index:

1. Initialize an empty `last_seen` map, `longest = 0`, and `left = 0`.
2. Iterate `right` over each `char` of `s`.
3. When `char` is in `last_seen` and the stored index is at or after `left`, the
   previous occurrence is inside the window: set `left = last_seen[char] + 1`.
4. Update `last_seen[char]` to `right`.
5. Update `longest` with the window length `right - left + 1`.
6. Return `longest`.

The guard `last_seen[char] >= left` is essential. `last_seen` deliberately remembers occurrences from the whole prefix, not just the window, and a stale entry behind `left` must not drag the window backward: on `"abba"` at `right = 3`, `last_seen['a']` holds `0` while `left` already stands at `2`, so an unguarded assignment would rewind the window to the invalid `"bba"`.

#### Walkthrough

Run the jump rule on Example 1, `s = "abcabcbb"`:

```text
right=0  'a' new                                    window [0,0] "a"    longest=1
         last_seen = {a: 0}
right=1  'b' new                                    window [0,1] "ab"   longest=2
         last_seen = {a: 0, b: 1}
right=2  'c' new                                    window [0,2] "abc"  longest=3
         last_seen = {a: 0, b: 1, c: 2}
right=3  'a' seen at 0, and 0 >= left=0 -> jump     window [1,3] "bca"  longest=3
         left=1, last_seen = {a: 3, b: 1, c: 2}
right=4  'b' seen at 1, and 1 >= left=1 -> jump     window [2,4] "cab"  longest=3
         left=2, last_seen = {a: 3, b: 4, c: 2}
right=5  'c' seen at 2, and 2 >= left=2 -> jump     window [3,5] "abc"  longest=3
         left=3, last_seen = {a: 3, b: 4, c: 5}
right=6  'b' seen at 4, and 4 >= left=3 -> jump     window [5,6] "cb"   longest=3
         left=5, last_seen = {a: 3, b: 6, c: 5}
right=7  'b' seen at 6, and 6 >= left=5 -> jump     window [7,7] "b"    longest=3
         left=7, last_seen = {a: 3, b: 7, c: 5}
```

Each duplicate collapses a whole shrink sequence into one guarded assignment: at `right = 6` the window jumps from `[3, 5]` straight to `[5, 6]` where the set version needed two evictions. The widest window had length `3`, so the function returns `3`, matching the expected Output for Example 1.

The stale-entry branch never fires on the official examples, so a short tailored input shows it. On `s = "abba"`, the final character carries a last-seen index behind the window:

```text
right=3  'a' seen at 0, but 0 >= left=2 is False -> stale, left holds
                                                  window [2,3] "ba"   longest=2
```

The guard rejects the stale index, `left` holds still, and the window stays duplicate-free.

#### Solution

The code is the walkthrough's jump rule: one guarded assignment replaces the shrink loop.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        longest = 0
        left = 0

        for right, char in enumerate(s):
            if char in last_seen and last_seen[char] >= left:
                left = last_seen[char] + 1
            last_seen[char] = right
            longest = max(longest, right - left + 1)

        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`right` visits each character once, `left` only moves forward, and every hash map operation is `O(1)` on average, so the whole pass touches each character a single time.

##### Space Complexity: `O(min(n, charset))`

The map stores at most one entry per distinct character, bounded by the string length and by the printable-ASCII alphabet.

#### Key Insights

- Recording last-seen positions rather than mere presence is what enables the jump: the map subsumes the set, and the shrink loop disappears.
- The `last_seen[char] >= left` guard keeps stale prefix entries from rewinding `left`; this is the one correctness detail the set version never needs.
- With both pointers monotonic, the pass is strictly linear, which matters at the constraint bound of 200,000 characters where the quadratic baseline is hopeless.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - each anchor rescans up to `n` characters before a repeat stops it.
- **Sliding Window with Set**: `O(2n)` - each character is added once by `right` and removed at most once by `left`.
- **Sliding Window with Last-Seen Index**: `O(n)` - `left` jumps past duplicates in one assignment, touching each character once.

### Space Complexity

- **Brute Force**: `O(min(n, charset))` - the `seen` set holds the current substring's distinct characters.
- **Sliding Window with Set**: `O(min(n, charset))` - the set holds the window's distinct characters.
- **Sliding Window with Last-Seen Index**: `O(min(n, charset))` - the map holds one entry per distinct character.

### Trade-offs

- The brute force is the shortest path from statement to working code, but it re-verifies already-checked characters after every restart and cannot run within limits at large `n`.
- The set version eliminates the restart and is the easiest window to reason about, at the cost of stepping `left` forward one eviction at a time.
- The last-seen-index version adds one guard condition (`>= left`) in exchange for jumping straight past duplicates, roughly halving the pointer work.

### When to Use Each

- **Brute Force**: to establish a correct baseline, or when the string is known to be tiny.
- **Sliding Window with Set**: when clarity matters most, or when introducing the sliding-window pattern for the first time.
- **Sliding Window with Last-Seen Index (Recommended)**: the interview answer: a single pass that holds up at the 200,000-character constraint bound.

### Optimization Notes

- The two window versions are both linear; the difference is the constant factor, since the set version may re-visit characters while `left` inches forward.
- The last-seen map makes the set redundant: presence plus position answers the same membership question and more.
- Test the stale-entry case (`"abba"`) whenever writing the index version; the official examples never exercise it, and an unguarded jump silently produces wrong windows.
- Python's set and dict operations are average-case `O(1)`; the printable-ASCII bound (at most 100 distinct characters) also caps the window at a constant width in practice.
