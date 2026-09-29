# Sliding Window: Pattern Intuition Guide

**Reference:** [Sliding window](https://usaco.guide/gold/sliding-window)

> *"The window is a moving lens of attention: it forgets the past to focus on what matters now."*

---

## The Situation That Calls for a Window

Imagine you're walking through a long corridor, and you can only see through a rectangular frame you carry with you. As you move forward, new things enter your view on the right, and old things disappear on the left.

**This is the essence of Sliding Window.**

You encounter this pattern whenever:
- You're scanning through a sequence (string, array, stream)
- You care about a **contiguous portion** of that sequence
- The answer depends on properties of that portion
- Those properties can be **updated incrementally** as the portion shifts

The key insight: *You don't need to remember everything: only what's currently in view.*

---

## The Two Forces at Play

Every sliding window algorithm is a dance between two opposing forces:

### The Explorer (Right Boundary) $R$
- Always moves forward, never backward
- Discovers new territory
- Adds new elements to consideration
- Asks: *"What happens if I include this?"*

### The Gatekeeper (Left Boundary) $L$
- Follows behind, cleaning up
- Removes elements that no longer serve the goal
- Enforces the rules of what's allowed
- Asks: *"Must I let go of something to stay valid?"*

The Explorer is eager and expansive. The Gatekeeper is disciplined and selective. Together, they maintain a **window of validity** that slides through the sequence.

---

## The Invariant: The Window's Promise

At every moment, the window makes a promise: an **invariant** that must always be true:

| Problem Type | The Promise |
|--------------|-------------|
| Longest unique substring | *"Every character in my view appears exactly once"* |
| At most K distinct | *"I contain no more than K different characters"* |
| Minimum covering substring | *"I contain everything required"* |
| Sum at least target | *"My total meets or exceeds the goal"* |

**This promise is sacred.** The moment it's broken, the Gatekeeper must act, shrinking the window until the promise is restored.

---

## The Irreversible Truth

Here's what makes sliding window work: **the Explorer never retreats.**

Once the right boundary passes an element, that element has been "seen." We may include it or exclude it from our current window, but we never go back to re-examine it as a potential starting point... unless the Gatekeeper releases it.

This one-directional march is what gives us O(n) time complexity. Each element enters the window at most once and exits at most once. No element is visited more than twice across the entire algorithm.

The irreversibility creates efficiency: *past decisions don't haunt us.*

---

## The Two Modes of Seeking

Depending on what you're optimizing, the dance changes:

### Mode 1: Maximize the Window
*"How large can my view become while staying valid?"*

```
Process:
1. Explorer advances, adding new element
2. If promise breaks → Gatekeeper advances until promise restored
3. Record the current window size (this is a candidate answer)
4. Repeat

The window EXPANDS freely, CONTRACTS only when forced.
```

**Mental image**: Stretching a rubber band until it's about to snap, then easing off just enough.

#### Flowchart: Maximize Window

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Example: Longest Substring Without Repeating Characters                    │
│  Sequence: [ a  b  c  a  b ]    Promise: "All chars unique"                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────┐                                                                    │
│  │START│                                                                    │
│  └──┬──┘                                                                    │
│     ▼                                                                       │
│  ┌──────────────────────┐                                                   │
│  │  R < length?         │───No───► ┌─────────┐                              │
│  └──────┬───────────────┘          │  DONE   │                              │
│     Yes │                          └─────────┘                              │
│         ▼                                                                   │
│  ╔══════════════════════════════╗                                           │
│  ║  🟢 R advances (Explorer)    ║◄───────────────────────────────┐          │
│  ║     Add element to state     ║                                │          │
│  ╚═══════════════╤══════════════╝                                │          │
│                  ▼                                               │          │
│        ┌─────────────────────┐                                   │          │
│        │ Promise broken?     │                                   │          │
│        │ (duplicate found?)  │                                   │          │
│        └────────┬────────────┘                                   │          │
│           Yes   │   No                                           │          │
│      ┌──────────┴──────────┐                                     │          │
│      ▼                     ▼                                     │          │
│  ┌─────────────────┐  ┌────────────────────────────────┐         │          │
│  │ While promise   │  │ ✅ Update answer:              │         │          │
│  │ is broken:      │  │    ans = max(ans, R-L+1)       │         │          │
│  │                 │  └──────────────┬─────────────────┘         │          │
│  │ ╔═════════════╗ │                 │                           │          │
│  │ ║ 🔴 L++      ║ │                 │                           │          │
│  │ ║ Remove L-1  ║ │                 │                           │          │
│  │ ╚═════════════╝ │                 │                           │          │
│  └────────┬────────┘                 │                           │          │
│           │                          │                           │          │
│           └──────────────────────────┘                           │          │
│                     │                                            │          │
│                     │                                            │          │
│                     │                                            │          │
│                     └────────────────────────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


Visual Trace:
═══════════════════════════════════════════════════════════════════════════════

  Sequence:   a    b    c    a    b
             [0]  [1]  [2]  [3]  [4]

  Step 1:   🟢R→
            [ a ]                        max = 1
              L,R

  Step 2:         🟢R→
            [ a    b ]                   max = 2
              L        R

  Step 3:              🟢R→
            [ a    b    c ]              max = 3
              L              R

  Step 4:                   🟢R→
            [ a    b    c    a ]         ❌ 'a' duplicate!
              L                  R
                             │
                             ▼
            🔴L→ 🔴L
                 [ b    c    a ]         max = 3 (restored)
                   L             R

  Step 5:                        🟢R→
                 [ b    c    a    b ]    ❌ 'b' duplicate!
                   L                  R
                                  │
                                  ▼
                  🔴L→ 🔴L
                      [ c    a    b ]    max = 3 (final)
                        L             R

Legend: 🟢 = R expands (green)  🔴 = L contracts (red)  ❌ = promise broken
```

---

### Mode 2: Minimize the Window
*"How small can my view become while still being valid?"*

```
Process:
1. Explorer advances until promise becomes TRUE
2. While promise holds → Gatekeeper advances, shrinking window
3. Record the window size just before promise breaks
4. Repeat

The window EXPANDS until valid, then CONTRACTS aggressively.
```

**Mental image**: Tightening a noose around the minimal solution.

#### Flowchart: Minimize Window

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Example: Minimum Size Subarray Sum ≥ 7                                     │
│  Sequence: [ 2  3  1  2  4  3 ]    Promise: "Sum ≥ target"                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────┐                                                                    │
│  │START│                                                                    │
│  └──┬──┘                                                                    │
│     ▼                                                                       │
│  ╔══════════════════════════════╗                                           │
│  ║  🟢 R advances (Explorer)    ║  ◀────────────────────────┐              │
│  ║     Add to sum               ║                            │              │
│  ╚═══════════════╤══════════════╝                            │              │
│                  ▼                                           │              │
│        ┌─────────────────────┐                               │              │
│        │ Promise satisfied?  │                               │              │
│        │   (sum ≥ target?)   │                               │              │
│        └────────┬────────────┘                               │              │
│            No   │   Yes                                      │              │
│      ┌──────────┴──────────────────────┐                     │              │
│      │                                 ▼                     │              │
│      │  ┌────────────────────────────────────────────────┐   │              │
│      │  │  WHILE promise still holds:                    │   │              │
│      │  │  ┌──────────────────────────────────────────┐  │   │              │
│      │  │  │ ✅ Update answer: min(ans, R-L+1)        │  │   │              │
│      │  │  │ 🔴 L advances (Gatekeeper)               │  │   │              │
│      │  │  │    Subtract from sum                     │  │   │              │
│      │  │  └──────────────────────────────────────────┘  │   │              │
│      │  └────────────────────────────────────────────────┘   │              │
│      │                                 │                     │              │
│      │                                 ▼                     │              │
│      │         ┌──────────────────────────────┐              │              │
│      └────────►│  More elements?              │              │              │
│                └─────────────┬────────────────┘              │              │
│                        Yes   │    No                         │              │
│                    ┌─────────┴─────────┐                     │              │
│                    │                   ▼                     │              │
│                    │              ┌─────────┐                │              │
│                    │              │  DONE   │                │              │
│                    │              └─────────┘                │              │
│                    └─────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘

Visual Trace:
═══════════════════════════════════════════════════════════════════════════════

  Sequence:   2    3    1    2    4    3      target = 7
             [0]  [1]  [2]  [3]  [4]  [5]

  Step 1:    🟢R→
            [ 2 ]                sum=2 < 7   ans = ∞
              L,R                (keep expanding)

  Step 2:         🟢R→
            [ 2    3 ]           sum=5 < 7   ans = ∞
              L        R         (keep expanding)

  Step 3:              🟢R→
            [ 2    3    1 ]      sum=6 < 7   ans = ∞
              L              R   (keep expanding)

  Step 4:                   🟢R→
            [ 2    3    1    2 ] sum=8 ≥ 7  ✅ VALID!   ans = min(∞, 3 - 0 + 1) = 4
              L                  R
                             │
                             ▼
             🔴L→ 🔴L
                 [ 3    1    2 ] sum=8-2 < 7  (stop contracting)
                   L             R

  Step 5:                        🟢R→
                 [ 3    1    2    4 ]  sum=10 ≥ 7  ✅ VALID!   ans = min(4, 4) = 4
                   L                   R
                                  │
                                  ▼
                  🔴L→ 🔴L
                      [ 1    2    4 ]  sum=7 ≥ 7  ✅ VALID!   ans = min(4, 3) = 3
                        L              R
                                  │
                                  ▼
                       🔴L→ 🔴L
                           [ 2    4 ]  sum=6 < 7  (stop)
                             L         R

  Step 6:                             🟢R→
                           [ 2    4    3 ]  sum=9 ≥ 7  ✅ VALID!   ans = min(3, 3) = 3
                             L              R
                                       │
                                       ▼ 
                            🔴L→ 🔴L
                                [ 4    3 ]  sum=7 ≥ 7  ✅ VALID!   ans = min(3, 2) = 2
                                  L         R
                                       │
                                       ▼
                                 🔴L→ 🔴L
                                     [ 3 ]  sum=3 < 7  (stop)
                                       L,R

Legend: 🟢 = R expands  🔴 = L contracts  ✅ = promise satisfied
```

---

## Pattern Recognition: "Is This a Sliding Window Problem?"

Ask yourself these questions:

```
┌─────────────────────────────────────────────────────────────┐
│  1. Am I looking for a CONTIGUOUS subarray or substring?    │
│     └── No? → Not sliding window                            │
│                                                             │
│  2. Can I describe a PROPERTY that makes a window valid?    │
│     └── No? → Probably not sliding window                   │
│                                                             │
│  3. Can I UPDATE that property in O(1) when I add/remove    │
│     a single element?                                       │
│     └── No? → Sliding window won't give O(n)                │
│                                                             │
│  4. Is the answer about OPTIMIZING that window              │
│     (longest, shortest, exists)?                            │
│     └── Yes to all? → SLIDING WINDOW.                       │
└─────────────────────────────────────────────────────────────┘
```

---

## The Three Window Shapes

### Shape 1: Variable Window, Maximize
**Story**: *"I want the biggest room that still follows the rules."*

- Invariant: Some constraint must not be violated
- Strategy: Grow greedily, shrink reluctantly
- Answer: Largest valid window seen

**Classic problems**: Longest substring without repeating characters, longest with at most K distinct

### Shape 2: Variable Window, Minimize  
**Story**: *"I want the smallest container that still holds everything I need."*

- Invariant: Some requirement must be satisfied
- Strategy: Grow until valid, shrink aggressively
- Answer: Smallest valid window seen

**Classic problems**: Minimum window substring, minimum size subarray sum

### Shape 3: Fixed Window
**Story**: *"I'm looking through a frame of exact size: does it ever show what I'm looking for?"*

- Invariant: Window size exactly K
- Strategy: Add one, remove one, check condition
- Answer: Whether/where condition is met

**Classic problems**: Find all anagrams, check permutation inclusion

#### Fixed Window Example Trace (K=3)

```
Problem: Find maximum sum of any subarray of size K=3
Sequence: [ 1  4  2  10  2  3  1  0  20 ]

┌──────┬───────┬─────────┬──────────────────┬───────────────┬────────────────┐
│ Step │ R→    │ sum     │ L action         │ Window [L,R]  │ Max Sum        │
├──────┼───────┼─────────┼──────────────────┼───────────────┼────────────────┤
│  0   │ 1     │ 1       │ -                │ [1]           │ (building...)  │
│  1   │ 4     │ 5       │ -                │ [1,4]         │ (building...)  │
│  2   │ 2     │ 7       │ -                │ [1,4,2]       │ 7 ✨           │
│  3   │ 10    │ 7+10=17 │ 🔴 remove 1 → 16 │ [4,2,10]      │ 16             │
│  4   │ 2     │ 16+2=18 │ 🔴 remove 4 → 14 │ [2,10,2]      │ 16             │
│  5   │ 3     │ 14+3=17 │ 🔴 remove 2 → 15 │ [10,2,3]      │ 16             │
│  6   │ 1     │ 15+1=16 │ 🔴 remove 10→ 6  │ [2,3,1]       │ 16             │
│  7   │ 0     │ 6+0=6   │ 🔴 remove 2 → 4  │ [3,1,0]       │ 16             │
│  8   │ 20    │ 4+20=24 │ 🔴 remove 3 → 21 │ [1,0,20]      │ 21 ✨          │
└──────┴───────┴─────────┴──────────────────┴───────────────┴────────────────┘

Key insight: Once R reaches index 2 (K-1), every subsequent step:
  1. 🟢 R advances → add new element
  2. 🔴 L advances → remove oldest element (exactly K steps behind)
  3. Window size stays constant at K=3

Answer: Maximum sum = 21 (subarray [1, 0, 20])
```

---

## The State: What the Window Remembers

The window isn't just boundaries: it carries **state** about its contents:

| What You're Tracking | State Structure | Update Cost |
|---------------------|-----------------|-------------|
| Character uniqueness | Last-seen index map | O(1) |
| Character frequencies | Count map | O(1) |
| Distinct count | Map + size | O(1) |
| Running sum | Single integer | O(1) |
| Requirement satisfaction | "Have" vs "Need" counters | O(1) |

The magic of sliding window is that these states are **incrementally maintainable**. Adding an element updates the state. Removing an element reverses that update. No full recomputation needed.

---

## Visualizing the Dance

**Problem**: Longest substring without repeating characters  
**Input**: `"abcabcbb"`. Find the longest window where all characters are unique.

| Step | $R$ (char) | State: `last_seen` | $L$ move? | Window `[L, R]` | Max Length |
|:----:|:----------:|:-------------------|:---------:|:---------------:|:----------:|
| 0 | `a` | `{a:0}` | - | `[0,0]` = "a" | 1 |
| 1 | `b` | `{a:0, b:1}` | - | `[0,1]` = "ab" | 2 |
| 2 | `c` | `{a:0, b:1, c:2}` | - | `[0,2]` = "abc" | 3 |
| 3 | `a` | `{a:3, b:1, c:2}` | 🔴 `L→1` (skip past old 'a') | `[1,3]` = "bca" | 3 |
| 4 | `b` | `{a:3, b:4, c:2}` | 🔴 `L→2` (skip past old 'b') | `[2,4]` = "cab" | 3 |
| 5 | `c` | `{a:3, b:4, c:5}` | 🔴 `L→3` (skip past old 'c') | `[3,5]` = "abc" | 3 |
| 6 | `b` | `{a:3, b:6, c:5}` | 🔴 `L→5` (skip past old 'b') | `[5,6]` = "cb" | 3 |
| 7 | `b` | `{a:3, b:7, c:5}` | 🔴 `L→7` (skip past old 'b') | `[7,7]` = "b" | 3 |

**Answer**: 3 (substring `"abc"`)

**Key observations**:
- $R$ (Explorer) advances every single step: never skips, never retreats
- $L$ (Gatekeeper) only moves when a duplicate is found in the current window
- The jump optimization: $L$ jumps directly to `last_seen[char] + 1` instead of incrementing one by one
- Window length = `R - L + 1`

---

## The Moment of Recognition

You're reading a problem. You see phrases like:
- *"contiguous subarray"*
- *"substring"*  
- *"longest/shortest"*
- *"at most K"*
- *"containing all of"*

And you feel it: *This is about maintaining something over a moving portion.*

That's your cue. The Explorer and Gatekeeper are ready. The window wants to slide.

---

## From Intuition to Implementation

Only now (after the dance is clear) does code become useful.

The template is always the same skeleton:

```python
def sliding_window(sequence):
    state = initial_state()
    left = 0
    answer = initial_answer()
    
    ## 1. Explorer (R) always advances
    for right, element in enumerate(sequence):
        # Explorer: include new element
        update_state_add(state, element)
        
        ## 2. Gatekeeper (L) acts to restore invariant
        while promise_is_broken(state):
            update_state_remove(state, sequence[left])
            left += 1
        
        # Record: this window is valid
        answer = consider(answer, left, right)
    
    return answer
```

The variations come from:
1. **What is the promise?** (determines the while condition)
2. **What state do we track?** (determines the data structure)
3. **What are we optimizing?** (determines how we update the answer)

---

## Quick Reference: Problem → Pattern Mapping

| When You See... | Think... | Window Type |
|----------------|----------|-------------|
| "Longest substring with unique chars" | Uniqueness promise | Maximize |
| "Longest with at most K distinct" | Count limit promise | Maximize |
| "Minimum window containing all of T" | Coverage promise | Minimize |
| "Subarray sum ≥ target" | Threshold promise | Minimize |
| "Contains permutation" | Exact match promise | Fixed |
| "Find all anagrams" | Exact match, collect all | Fixed |

---

## Complete Implementations: From Intuition to Code

Now we translate intuition into production-ready code. Each solution demonstrates the Explorer-Gatekeeper dance with explicit state management and complexity guarantees.

---

### Problem 1: [Longest Substring Without Repeating Characters](../../problems/longest_substring_without_repeating_characters.md)

**The Promise**: *"Every character in my view appears exactly once."*

**Why This Problem Matters**: This is the canonical sliding window problem. Master it, and you understand the pattern.

```python
def length_of_longest_substring(s: str) -> int:
    """
    Find the length of the longest substring without repeating characters.
    
    Intuition:
        We maintain a window [left, right] where all characters are unique.
        The Explorer (right pointer) advances one character at a time.
        When a duplicate is detected, the Gatekeeper (left pointer) jumps
        directly past the previous occurrence: no incremental crawling needed.
    
    The Jump Optimization:
        Instead of shrinking one position at a time (while loop), we record
        each character's last-seen index. When we see a duplicate, we can
        teleport the left boundary to skip all characters up to and including
        the previous occurrence. This eliminates redundant comparisons.
    
    Time Complexity: O(n)
        - The right pointer visits each character exactly once: O(n)
        - The left pointer only moves forward (never backward): amortized O(n)
        - Dictionary operations (get, set): O(1) per operation
        - Total: O(n) where n = len(s)
    
    Space Complexity: O(min(n, σ))
        - σ = size of character set (26 for lowercase, 128 for ASCII, etc.)
        - In practice, O(1) for fixed alphabets, O(n) for arbitrary Unicode
    
    Args:
        s: Input string to search
        
    Returns:
        Length of the longest substring with all unique characters
        
    Examples:
        >>> length_of_longest_substring("abcabcbb")
        3  # "abc"
        >>> length_of_longest_substring("bbbbb")
        1  # "b"
        >>> length_of_longest_substring("pwwkew")
        3  # "wke"
    """
    # State: Maps each character to its most recent index
    # This enables O(1) duplicate detection and O(1) jump calculation
    last_seen_at: dict[str, int] = {}
    
    # Window boundaries: [left, right] inclusive
    left = 0
    max_length = 0
    
    # Explorer advances through every position
    for right, char in enumerate(s):
        # Duplicate detection: Is this char already in our current window?
        # Key insight: We only care if the previous occurrence is at or after 'left'
        # Characters before 'left' are outside our window: they don't count
        if char in last_seen_at and last_seen_at[char] >= left:
            # Gatekeeper acts: Jump past the previous occurrence
            # The +1 ensures we exclude the duplicate itself
            left = last_seen_at[char] + 1
        
        # Record this character's position for future duplicate detection
        last_seen_at[char] = right
        
        # The window [left, right] is now guaranteed unique
        # Update our answer if this window is the largest seen
        current_length = right - left + 1
        max_length = max(max_length, current_length)
    
    return max_length


# Verification
if __name__ == "__main__":
    test_cases = [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        ("au", 2),
        ("dvdf", 3),
    ]
    for s, expected in test_cases:
        result = length_of_longest_substring(s)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: {s!r:15} → {result} (expected {expected})")
```

**Complexity Deep Dive**:

| Operation | Count | Cost | Total |
|-----------|-------|------|-------|
| Right pointer advances | n | O(1) | O(n) |
| Left pointer advances | ≤ n (total) | O(1) | O(n) |
| Dictionary lookup/update | n | O(1) average | O(n) |
| **Total** | | | **O(n)** |

The left pointer never retreats. Each character index is visited by `left` at most once across the entire algorithm, giving us the O(n) guarantee.

---

### Problem 2: Longest Substring with At Most K Distinct Characters (LeetCode 340)

**The Promise**: *"I contain no more than K different characters."*

**The Difference from Problem 1**: We can't jump: we must shrink incrementally because removing one character might still leave us with too many distinct characters.

```python
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    """
    Find the length of the longest substring with at most K distinct characters.
    
    Intuition:
        The window [left, right] maintains at most K distinct characters.
        When adding a character causes distinct count to exceed K, we shrink
        from the left until we're back to K or fewer distinct characters.
    
    Why We Can't Jump:
        Unlike the unique-character problem, removing one character doesn't
        guarantee we restore validity. We might need to remove several
        characters before the distinct count drops. Hence, we use a while-loop.
    
    State Design:
        We use a frequency map rather than a last-seen-index map because:
        1. We need to know when a character's count drops to zero (to decrement distinct count)
        2. The len(frequency_map) tells us the distinct count directly
    
    Time Complexity: O(n)
        - Right pointer: n iterations, O(1) per iteration
        - Left pointer: moves at most n times total (amortized)
        - Each character enters and exits the window at most once
    
    Space Complexity: O(K)
        - The frequency map contains at most K+1 entries at any time
        - Before we shrink, we might briefly have K+1 entries
    
    Args:
        s: Input string
        k: Maximum number of distinct characters allowed
        
    Returns:
        Length of the longest valid substring
        
    Examples:
        >>> length_of_longest_substring_k_distinct("eceba", 2)
        3  # "ece"
        >>> length_of_longest_substring_k_distinct("aa", 1)
        2  # "aa"
    """
    if k == 0:
        return 0
    
    # State: Frequency count of each character in current window
    # The length of this dict = number of distinct characters
    char_count: dict[str, int] = {}
    
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # Explorer adds new character to window
        char_count[char] = char_count.get(char, 0) + 1
        
        # Gatekeeper shrinks window while we have too many distinct characters
        # This is a while-loop, not an if: we may need multiple shrinks
        while len(char_count) > k:
            left_char = s[left]
            char_count[left_char] -= 1
            
            # Critical: Remove from dict when count reaches zero
            # This keeps len(char_count) accurate for distinct count
            if char_count[left_char] == 0:
                del char_count[left_char]
            
            left += 1
        
        # Window is now valid: at most K distinct characters
        max_length = max(max_length, right - left + 1)
    
    return max_length


# Verification
if __name__ == "__main__":
    test_cases = [
        (("eceba", 2), 3),
        (("aa", 1), 2),
        (("a", 0), 0),
        (("aabbcc", 2), 4),
    ]
    for (s, k), expected in test_cases:
        result = length_of_longest_substring_k_distinct(s, k)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: {s!r}, k={k} → {result} (expected {expected})")
```

**Engineering Note**: The deletion `del char_count[left_char]` is essential. Without it, `len(char_count)` would count characters with zero frequency, breaking our invariant check.

---

### Problem 3: [Minimum Window Substring](../../problems/minimum_window_substring.md)

**The Promise**: *"I contain all required characters with sufficient frequency."*

**The Paradigm Shift**: Now we're *minimizing*, not maximizing. We expand until valid, then shrink aggressively while staying valid.

```python
def min_window(s: str, t: str) -> str:
    """
    Find the minimum window in s that contains all characters of t.
    
    Intuition:
        Phase 1 (Expand): Explorer advances until window contains all of t.
        Phase 2 (Contract): Gatekeeper shrinks window while it remains valid.
        Record the smallest valid window, then continue exploring.
    
    The Satisfied Counter Optimization:
        Naively checking "do we have all characters?" requires O(|t|) per step.
        Instead, we track how many unique characters have met their quota.
        When `chars_satisfied == chars_required`, the window is valid.
        This reduces per-step cost from O(|t|) to O(1).
    
    Time Complexity: O(|s| + |t|)
        - Building need_count: O(|t|)
        - Main loop: O(|s|), each character enters and exits once
        - All dictionary operations: O(1) each
    
    Space Complexity: O(unique(s) + unique(t)), i.e. O(|s| + |t|) worst case
        - need_count: O(unique chars in t)
        - have_count: O(unique chars in s), every char entering the window
          is counted, not just the needed ones
    
    Args:
        s: Source string to search in
        t: Target string containing required characters
        
    Returns:
        Minimum window substring, or "" if no valid window exists
        
    Examples:
        >>> min_window("ADOBECODEBANC", "ABC")
        "BANC"
        >>> min_window("a", "a")
        "a"
        >>> min_window("a", "aa")
        ""
    """
    if not t or not s:
        return ""
    
    # Build the requirement: what characters do we need, and how many of each?
    need_count: dict[str, int] = {}
    for char in t:
        need_count[char] = need_count.get(char, 0) + 1
    
    # State: what characters do we have in current window?
    have_count: dict[str, int] = {}
    
    # Optimization: Track satisfaction at character level
    # chars_satisfied = count of unique characters meeting their quota
    chars_satisfied = 0
    chars_required = len(need_count)  # number of unique characters in t
    
    # Answer tracking
    min_length = float('inf')
    result_start = 0
    
    left = 0
    
    for right, char in enumerate(s):
        # Explorer: Add character to window
        have_count[char] = have_count.get(char, 0) + 1
        
        # Did adding this character satisfy a requirement?
        # We check for exact equality to avoid double-counting
        if char in need_count and have_count[char] == need_count[char]:
            chars_satisfied += 1
        
        # Gatekeeper: Try to shrink while window remains valid
        while chars_satisfied == chars_required:
            # Current window is valid: record if it's the smallest
            window_length = right - left + 1
            if window_length < min_length:
                min_length = window_length
                result_start = left
            
            # Remove leftmost character
            left_char = s[left]
            have_count[left_char] -= 1
            
            # Did removing break a requirement?
            if left_char in need_count and have_count[left_char] < need_count[left_char]:
                chars_satisfied -= 1
            
            left += 1
    
    if min_length == float('inf'):
        return ""
    return s[result_start : result_start + min_length]


# Verification
if __name__ == "__main__":
    test_cases = [
        (("ADOBECODEBANC", "ABC"), "BANC"),
        (("a", "a"), "a"),
        (("a", "aa"), ""),
        (("aa", "aa"), "aa"),
    ]
    for (s, t), expected in test_cases:
        result = min_window(s, t)
        status = "✓" if result == expected else "✗"
        print(f"{status} s={s!r}, t={t!r} → {result!r} (expected {expected!r})")
```

**Complexity Breakdown**:

| Phase | Operations | Complexity |
|-------|------------|------------|
| Build `need_count` | Iterate over t | O(\|t\|) |
| Expand (right pointer) | Each char enters once | O(\|s\|) |
| Contract (left pointer) | Each char exits at most once | O(\|s\|) |
| **Total** | | **O(\|s\| + \|t\|)** |

---

### Problem 4: [Find All Anagrams in a String](../../problems/find_all_anagrams_in_a_string.md)

**The Promise**: *"I contain exactly the same character frequencies as the pattern."*

**Fixed Window Property**: Since anagrams have the same length, we maintain a window of exactly `len(p)`.

```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find all starting indices of p's anagrams in s.
    
    Intuition:
        An anagram has the exact same character frequencies as the pattern.
        Since length must match, we use a fixed-size window of len(p).
        At each position, check if window frequencies match pattern frequencies.
    
    The Match Counter Optimization:
        Instead of comparing two frequency maps (O(26) for lowercase),
        we track how many characters have matching frequencies.
        When all match, we've found an anagram.
    
    Careful State Transitions:
        When adding a character:
          - If it now matches the pattern frequency: matches++
          - If it just exceeded the pattern frequency: matches--
        When removing a character:
          - If it was matching and now isn't: matches--
          - If it was exceeding and now matches: matches++
    
    Time Complexity: O(|s| + |p|)
        - Build pattern frequency: O(|p|)
        - Slide window over s: O(|s|) with O(1) per step
    
    Space Complexity: O(1)
        - Two frequency maps bounded by alphabet size (26 for lowercase)
    
    Args:
        s: Source string to search in
        p: Pattern string (looking for its anagrams)
        
    Returns:
        List of starting indices where anagrams of p begin
        
    Examples:
        >>> find_anagrams("cbaebabacd", "abc")
        [0, 6]
        >>> find_anagrams("abab", "ab")
        [0, 1, 2]
    """
    result: list[int] = []
    
    pattern_len = len(p)
    source_len = len(s)
    
    if pattern_len > source_len:
        return result
    
    # Build pattern frequency map
    pattern_freq: dict[str, int] = {}
    for char in p:
        pattern_freq[char] = pattern_freq.get(char, 0) + 1
    
    # Window frequency map
    window_freq: dict[str, int] = {}
    
    # Track how many characters have matching frequencies
    chars_matched = 0
    chars_to_match = len(pattern_freq)
    
    for right in range(source_len):
        # Add character at right edge
        right_char = s[right]
        window_freq[right_char] = window_freq.get(right_char, 0) + 1
        
        # Update match count for added character
        if right_char in pattern_freq:
            if window_freq[right_char] == pattern_freq[right_char]:
                chars_matched += 1
            elif window_freq[right_char] == pattern_freq[right_char] + 1:
                # We just went from matching to exceeding
                chars_matched -= 1
        
        # Remove character at left edge when window exceeds pattern length
        left = right - pattern_len
        if left >= 0:
            left_char = s[left]
            
            # Update match count for removed character BEFORE decrementing
            if left_char in pattern_freq:
                if window_freq[left_char] == pattern_freq[left_char]:
                    # We're about to break this match
                    chars_matched -= 1
                elif window_freq[left_char] == pattern_freq[left_char] + 1:
                    # Removing brings us from exceeding to matching
                    chars_matched += 1
            
            window_freq[left_char] -= 1
            if window_freq[left_char] == 0:
                del window_freq[left_char]
        
        # Check for anagram when window size equals pattern size
        if right >= pattern_len - 1 and chars_matched == chars_to_match:
            result.append(right - pattern_len + 1)
    
    return result


# Verification
if __name__ == "__main__":
    test_cases = [
        (("cbaebabacd", "abc"), [0, 6]),
        (("abab", "ab"), [0, 1, 2]),
        (("aaaaaaaaaa", "aaaaaaaaaaaaa"), []),
    ]
    for (s, p), expected in test_cases:
        result = find_anagrams(s, p)
        status = "✓" if result == expected else "✗"
        print(f"{status} s={s!r}, p={p!r} → {result} (expected {expected})")
```

---

### Problem 5: Minimum Size Subarray Sum (LeetCode 209)

**The Promise**: *"My sum is at least the target."*

**Numeric Sliding Window**: Instead of tracking character frequencies, we track a running sum. The principle remains identical.

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    """
    Find the minimal length of a subarray whose sum is >= target.
    
    Intuition:
        This is the numeric equivalent of minimum window substring.
        Expand until sum >= target, then shrink while sum stays >= target.
        Track the smallest window that ever achieves the target.
    
    Why Positive Numbers Matter:
        This algorithm works because all elements are positive.
        Adding an element always increases the sum.
        Removing an element always decreases the sum.
        This monotonicity is what makes sliding window viable.
    
    Caution for Interviews:
        If the array can contain negatives, sliding window doesn't work!
        You'd need a different approach (prefix sums + monotonic deque).
    
    Time Complexity: O(n)
        - Right pointer: visits each element once
        - Left pointer: moves forward only, at most n times total
        - Each element enters and exits the window at most once
    
    Space Complexity: O(1)
        - Only a few integer variables (sum, pointers, min_length)
    
    Args:
        target: The minimum sum we need to achieve
        nums: Array of positive integers
        
    Returns:
        Minimum length of valid subarray, or 0 if impossible
        
    Examples:
        >>> min_subarray_len(7, [2, 3, 1, 2, 4, 3])
        2  # [4, 3]
        >>> min_subarray_len(11, [1, 1, 1, 1, 1, 1, 1, 1])
        0  # Impossible
    """
    n = len(nums)
    if n == 0:
        return 0
    
    # State: Running sum of current window [left, right]
    window_sum = 0
    
    left = 0
    min_length = float('inf')
    
    for right, num in enumerate(nums):
        # Explorer: Expand window by including nums[right]
        window_sum += num
        
        # Gatekeeper: Shrink while sum meets target
        # We want the SMALLEST valid window, so shrink aggressively
        while window_sum >= target:
            # Current window is valid: record its size
            current_length = right - left + 1
            min_length = min(min_length, current_length)
            
            # Remove leftmost element
            window_sum -= nums[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0


# Verification
if __name__ == "__main__":
    test_cases = [
        ((7, [2, 3, 1, 2, 4, 3]), 2),
        ((4, [1, 4, 4]), 1),
        ((11, [1, 1, 1, 1, 1, 1, 1, 1]), 0),
        ((15, [1, 2, 3, 4, 5]), 5),
    ]
    for (target, nums), expected in test_cases:
        result = min_subarray_len(target, nums)
        status = "✓" if result == expected else "✗"
        print(f"{status} target={target}, nums={nums} → {result} (expected {expected})")
```

**The O(n) Guarantee Visualized**:

```
Element:     [2]  [3]  [1]  [2]  [4]  [3]
              ↓    ↓    ↓    ↓    ↓    ↓
Right visits: ✓    ✓    ✓    ✓    ✓    ✓   = 6 times
Left visits:  ✓    ✓    ✓    ✓    ✓    ✓   = 6 times (at most)
                                           ─────────
Total operations:                          ≤ 2n = O(n)
```

---

## Time Complexity: The Definitive Analysis

Every sliding window algorithm achieves O(n) through the **two-pointer invariant**:

```
Both pointers only move forward → Each element enters the window once, exits once
```

| Algorithm | Per-Element Cost | Total Visits | Complexity |
|-----------|------------------|--------------|------------|
| Right pointer advance | O(1) | n | O(n) |
| Left pointer advance | O(1) | ≤ n | O(n) |
| State update (add/remove) | O(1) | 2n | O(n) |
| **Combined** | | | **O(n)** |

**The Amortized Argument**: While the inner `while` loop might run multiple times for a single `right` advance, the total number of `left` advances across the *entire* algorithm is bounded by n. This is because `left` starts at 0 and can only increase, never decrease, and can never exceed n.

---

## Corner Cases

- Empty sequence: no window forms; return the empty answer
- Single element: one window of size 1; the loop must still record it
- Fixed window longer than the sequence (pattern longer than the string): answer is "never", not an index error
- k of 0 in at-most-K problems: the window can never grow; the answer is 0
- All elements identical: every advance triggers a shrink; the Gatekeeper works at full speed
- Sum or coverage never reached anywhere: return the "no answer" sentinel (0 or empty string), not a partial window
- Negative numbers in the array: sum windows lose monotonicity; the pattern does not apply

---

## The Pattern in One Sentence

> *Sliding Window is the art of maintaining a valid contiguous view by advancing eagerly and retreating only when necessary.*

When you see a problem about optimizing over contiguous sequences with incrementally checkable properties, you've found your window.

Let it slide.

---

