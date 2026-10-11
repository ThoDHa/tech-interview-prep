# [Word Break](https://www.fastprep.io/problems/amazon-word-break)

**Medium** | **NN minutes** | **Array, Hash Table, String, Dynamic Programming**

Given a string s and an array of distinct dictionary words wordDict, return true if s can be split into a sequence of one or more dictionary words.

A dictionary word may be reused any number of times.

## Examples

### Example 1

**Input:** `s = "leetcode"`, `wordDict = ["leet","code"]`

**Output:** `true`

**Explanation:** The string splits as leet + code.

### Example 2

**Input:** `s = "applepenapple"`, `wordDict = ["apple","pen"]`

**Output:** `true`

**Explanation:** The word apple is reused in apple + pen + apple.

### Example 3

**Input:** `s = "catsandog"`, `wordDict = ["cats","dog","sand","and","cat"]`

**Output:** `false`

**Explanation:** No sequence of dictionary words covers the entire string.

## Constraints

- `1 <= s.length <= 300.`
- `1 <= wordDict.length <= 1000.`
- `1 <= wordDict[i].length <= 20.`
- `s and every dictionary word contain only lowercase English letters.`
- `All dictionary words are distinct.`

## Solutions

### Brute Force Recursion

#### Derivation

The literal reading: a valid segmentation must start with some dictionary word, and after removing that word the rest of the string poses the same question. That is a [recursive](https://en.wikipedia.org/wiki/Recursion_(computer_science)) structure: try every word that could begin at the current position, recurse on what remains, and succeed the moment the whole string is consumed.

1. Put the words in `word_set` for constant-time membership tests.
2. From the current `start_index`, try every word boundary `end_index` and
   slice `current_word = s[start_index:end_index]`.
3. When `current_word` is a dictionary word, recurse on the remaining suffix
   via `segmentable(end_index)`.
4. Return `True` as soon as any branch reaches the end of the string
   (`start_index == n`); return `False` when no boundary works.

#### Walkthrough

Example 1: `s = "leetcode"`, `wordDict = ["leet","code"]`, so `n = 8` and `word_set = {"leet", "code"}`. Each call scans `end_index` from `start_index + 1` upward, slicing `current_word` and recursing only when the slice is a dictionary word:

```text
segmentable(0)            s[0:] = "leetcode"
  "l", "le", "lee" fail; "leet" matches at end_index = 4: recurse
  └─ segmentable(4)       s[4:] = "code"
       "c", "co", "cod" fail; "code" matches at end_index = 8: recurse
       └─ segmentable(8)  start_index == n: return True   (base case)
     returns True
  returns True
```

The deepest call hits the base case because `start_index` reached `n = 8`, meaning the whole string was consumed exactly, and that `True` flows straight back up the chain: `segmentable(4)` returns `True` on its `"code"` branch and `segmentable(0)` returns `True` on its `"leet"` branch. The final value is `True`, matching the expected Output for Example 1.

#### Solution

The code is the call tree from the walkthrough: one loop over `end_index`, one recursive call per matching word.

```python
from typing import List


class Solution:
    def solve(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        n = len(s)

        def segmentable(start_index: int) -> bool:
            if start_index == n:
                return True
            for end_index in range(start_index + 1, n + 1):
                current_word = s[start_index:end_index]
                if current_word in word_set and segmentable(end_index):
                    return True
            return False

        return segmentable(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

Nothing remembers which suffixes have already been explored, so the same suffix is re-searched along every prefix that reaches it; in the worst case the recursion explores exponentially many partial segmentations.

##### Space Complexity: `O(n)`

The recursion stack, which can reach one frame per character before a branch either succeeds or dies.

#### Key Insights

- Every prefix that matches a dictionary word spawns an independent subproblem on the remaining suffix, which is the recursive structure every faster approach exploits.
- The exponential blowup has one source: overlapping subproblems, the same suffix searched again and again along different prefixes.
- This formulation is worth writing down even when it is too slow, because it defines the subproblem ("can the suffix from here be segmented?") that the memoized and tabular versions optimize.

### Top-Down Memoization

#### Derivation

The brute force re-explores a suffix because nothing records the answer already computed for it. That answer depends on `start_index` alone, not on how the search got there, so there are only `n + 1` genuinely distinct subproblems behind the exponentially many paths. [Memoization](https://en.wikipedia.org/wiki/Memoization) keeps the recursion exactly as the brute force wrote it and adds a `memo` dictionary keyed on `start_index`: look the answer up on entry, store it before returning.

1. Define `dp(start_index)` as "can `s[start_index:]` be segmented?".
2. Return `memo[start_index]` immediately when the position was computed
   before.
3. Try each `end_index` whose `current_word = s[start_index:end_index]` is in
   `word_set`, recursing via `dp(end_index)`.
4. Store the outcome in `memo[start_index]` on both the success and failure
   paths before returning it.

#### Walkthrough

Example 1 succeeds on its first path, so no index is ever revisited there and the memo never fires. Example 3 exercises it: `s = "catsandog"`, `wordDict = ["cats","dog","sand","and","cat"]`, expected Output `false`. The trace indents one level per recursive call:

```text
dp(0)  s[0:] = "catsandog"   "cat" matches -> recurse
  dp(3)  s[3:] = "sandog"    "sand" matches -> recurse
    dp(7)  s[7:] = "og"      no word starts here
    dp(7) -> False, memo[7] = False
  dp(3) -> False, memo[3] = False
dp(0)  continues              "cats" matches -> recurse
  dp(4)  s[4:] = "andog"     "and" matches -> recurse
    dp(7)  memo hit: return False without scanning anything
  dp(4) -> False, memo[4] = False
dp(0) -> False, memo[0] = False
```

Position 7 is reached twice, once through `"cat" + "sand"` and once through `"cats" + "and"`. The first visit scans `"o"` and `"og"`, finds no word, and stores `memo[7] = False`; the second visit returns that stored answer before slicing anything. Without the memo the whole suffix search from 7 would run again for every prefix landing there. With no boundary working anywhere, `dp(0)` returns `False`, matching the expected Output for Example 3.

#### Solution

The code is the brute force recursion with the `memo` lookup and store wrapped around the boundary loop.

```python
from typing import List


class Solution:
    def solve(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        memo = {}

        def dp(start_index: int) -> bool:
            if start_index == n:
                return True
            if start_index in memo:
                return memo[start_index]
            for end_index in range(start_index + 1, n + 1):
                current_word = s[start_index:end_index]
                if current_word in word_set and dp(end_index):
                    memo[start_index] = True
                    return True
            memo[start_index] = False
            return False

        n = len(s)
        return dp(0)
```

Wait, that code has a bug: `n` is read inside `dp` before it is defined. Let me fix the ordering: `n = len(s)` must come before `dp` is called (Python closures resolve at call time, so defining `n` after `dp` but before `dp(0)` is legal). Hmm, actually it IS legal: `dp`'s body evaluates `n` at call time, and `n = len(s)` runs before `return dp(0)`. It works but reads badly. Let me restructure to define `n` first. 

Corrected version to write in the file:

```python
from typing import List


class Solution:
    def solve(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        n = len(s)
        memo = {}

        def dp(start_index: int) -> bool:
            if start_index == n:
                return True
            if start_index in memo:
                return memo[start_index]
            for end_index in range(start_index + 1, n + 1):
                current_word = s[start_index:end_index]
                if current_word in word_set and dp(end_index):
                    memo[start_index] = True
                    return True
            memo[start_index] = False
            return False

        return dp(0)
```

I need to replace the block I just wrote with this corrected one. Doing that now before moving on.
