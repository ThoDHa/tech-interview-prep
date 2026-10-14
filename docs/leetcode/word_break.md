# [Word Break](https://leetcode.com/problems/word-break/)

**Medium** | **30 minutes** | **Array, Hash Table, String, Dynamic Programming, Trie, Memoization**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md), [Trie](../patterns/trie/intuition.md)

**Algorithm:** [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) · [Trie](https://en.wikipedia.org/wiki/Trie)

**Practice:** [`practice/word_break/solution.py`](../../practice/word_break/solution.py)

Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

**Note** that the same word in the dictionary may be reused multiple times in the segmentation.

## Examples

### Example 1

**Input:** `s = "leetcode"`, `wordDict = ["leet","code"]`

**Output:** `true`

**Explanation:** Return true because `"leetcode"` can be segmented as `"leet code"`.

### Example 2

**Input:** `s = "applepenapple"`, `wordDict = ["apple","pen"]`

**Output:** `true`

**Explanation:** Return true because `"applepenapple"` can be segmented as `"apple pen apple"`. Note that you are allowed to reuse a dictionary word.

### Example 3

**Input:** `s = "catsandog"`, `wordDict = ["cats","dog","sand","and","cat"]`

**Output:** `false`

## Constraints

- `1 <= s.length <= 300`
- `1 <= wordDict.length <= 1000`
- `1 <= wordDict[i].length <= 20`
- `s` and `wordDict[i]` consist of only lowercase English letters.
- All the strings of `wordDict` are **unique**.

## Deriving the Solution

Every segmentation is a chain of word boundaries: positions `0` through `len(s)` act as nodes, and a dictionary word `s[i:j]` connects position `i` to position `j`. The question "can `s` be segmented?" becomes "is position `len(s)` reachable from position `0`?", and every solution below is a different way of exploring that reachability.

1. **Start literal.** From each position, try every word that could start
   there and recurse on the rest. Correct, but the same suffix is re-explored along many different prefixes, costing `O(2^n)`: see [Brute Force Recursion](#brute-force-recursion).
2. **Spot the waste.** Whether `s[start_index:]` can be segmented depends only
   on `start_index`, not on how the search reached it, so there are only `n + 1` genuinely distinct subproblems.
3. **Visit each position once.** Two dressings of the same repair: walk the
   reachability graph with a queue and a `visited` set, in [BFS](#bfs), or keep the recursion and cache each `start_index` answer, in [Top-Down Memoization](#top-down-memoization). Either way each position is processed at most once.
4. **Flip the direction.** Build prefix answers iteratively instead: `dp[i]`
   records whether `s[0:i]` splits cleanly, computed from smaller prefixes with no recursion at all: see [Bottom-Up DP](#bottom-up-dp).
5. **Sharpen the matching.** All of the above slice and hash a candidate
   substring per boundary pair. Walking a prefix tree character by character finds every word starting at a position in one descent and stops the moment no word can continue: see [Trie-Based DP](#trie-based-dp).
6. **Let the library hold the cache.** The memoized form in step 3 spends five
   lines declaring a dictionary, reading it on entry, and writing it on both exits. Decorating the recursion with `functools.cache` deletes all five while the boundary loop and the base case stay exactly as the brute force wrote them: see [Top-Down Memoization with functools.cache](#top-down-memoization-with-functoolscache).

## Solutions

### Brute Force Recursion

#### Derivation

The most direct reading: a segmentation must start with some dictionary word, and after removing that word the rest of the string poses the same question. That is a [recursive](https://en.wikipedia.org/wiki/Recursion_(computer_science)) structure: try every word that could begin at the current position, recurse on what remains, and succeed the moment the whole string is consumed.

1. Put the words in `word_set` for constant-time membership tests.
2. From the current `start_index`, try every possible word boundary
   `end_index`.
3. If `current_word = s[start_index:end_index]` is a dictionary word, recurse
   on the remaining suffix via `backtrack(end_index)`.
4. Return `True` as soon as any branch reaches the end of the string
   (`start_index == len(s)`); return `False` when no boundary works.

#### Walkthrough

Let us watch the Brute Force Recursion run on Example 1: `s = "leetcode"`, `wordDict = ["leet","code"]`. First, `word_set` becomes `{"leet", "code"}`, then we call `backtrack(0)`. Each call asks the question "can `s[start_index:]` be segmented?" and tries every word boundary from the current index.

The recursion forms a call tree. Each call scans `end_index` from `start_index + 1` upward, slicing `current_word = s[start_index:end_index]`, and only recurses when that slice is in `word_set`:

```text
backtrack(0)            s[0:] = "leetcode"
  end_index runs 1..8, slicing "l", "le", "lee", then "leet"
  "leet" is in word_set: recurse on the remaining suffix
  └─ backtrack(4)       s[4:] = "code"
       end_index runs 5..8, slicing "c", "co", "cod", then "code"
       "code" is in word_set: recurse on the remaining suffix
       └─ backtrack(8)  s[8:] = ""
            start_index == len(s), so return True   ← base case
       └─ returns True, so backtrack(4) returns True
  └─ returns True, so backtrack(0) returns True
```

Tracing how each call resolves and how the `True` propagates back up:

| Call | `s[start_index:]` | First valid word found | Recursive result | Returns |
| --- | --- | --- | --- | --- |
| `backtrack(0)` | `"leetcode"` | `"leet"` at `end_index = 4` | `backtrack(4)` is `True` | `True` |
| `backtrack(4)` | `"code"` | `"code"` at `end_index = 8` | `backtrack(8)` is `True` | `True` |
| `backtrack(8)` | `""` | (base case: `start_index == len(s)`) | none | `True` |

The deepest call hits the base case because `start_index` reached `len(s) = 8`, meaning the whole string was consumed exactly. That `True` flows back up: `backtrack(4)` returns `True` the moment its `"code"` branch succeeds, and `backtrack(0)` returns `True` the moment its `"leet"` branch succeeds. The final returned value is `True`, which matches the expected Output for Example 1.

#### Solution

The code is the call tree from the walkthrough: one loop over `end_index`, one recursive call per matching word.

```python
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)

        def backtrack(start_index: int) -> bool:
            # Base case: reached end of string
            if start_index == len(s):
                return True

            # Try all possible words starting from current index
            for end_index in range(start_index + 1, len(s) + 1):
                current_word = s[start_index:end_index]

                # If current word is valid and rest can be segmented
                if current_word in word_set and backtrack(end_index):
                    return True

            return False

        return backtrack(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

In the worst case, we might explore all possible ways to partition the string, leading to exponential time.

##### Space Complexity: `O(n)`

Space for the recursion stack, which can be up to n levels deep.

#### Key Insights

- Every prefix that matches a dictionary word spawns an independent subproblem on the remaining suffix.
- Without caching, the same suffix positions are re-explored along many different prefixes, which is the source of the exponential blowup.
- This formulation makes the recursive structure explicit, which is the foundation every faster approach optimizes.

### BFS

#### Derivation

The brute force re-explores the same suffix along many prefixes because nothing remembers which positions have already been examined. Making the graph explicit fixes that. Treat the problem as finding a path from index `0` to index `len(s)` in a graph where each valid starting position is a node and there is an edge from position `i` to position `j` when `s[i:j]` is in the dictionary. [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) explores all reachable positions level by level, and a `visited` set guarantees no position is ever expanded twice.

1. Start a `queue` holding only index `0` and an empty `visited` set.
2. Pop a `start_index`; skip it when already in `visited`, otherwise mark it.
3. For every `end_index` whose slice `s[start_index:end_index]` is in
   `word_set`, enqueue `end_index`; return `True` immediately when such a slice ends exactly at `len(s)`.
4. When the queue empties without reaching the end, return `False`.

#### Walkthrough

Let us run the BFS on Example 3: `s = "catsandog"`, `wordDict = ["cats","dog","sand","and","cat"]`, where the expected Output is `false`. Positions run from `0` to `9`, and `9` is the goal. Each line shows one queue pop and its effect:

```text
pop 0   words "cat" -> 3, "cats" -> 4    queue=[3, 4]    visited={0}
pop 3   word  "sand" -> 7                queue=[4, 7]    visited={0, 3}
pop 4   word  "and" -> 7                 queue=[7, 7]    visited={0, 3, 4}
pop 7   s[7:9]="og": no word starts      queue=[7]       visited={0, 3, 4, 7}
pop 7   already visited: skipped         queue=[]
```

Position `7` is reachable two ways (`"cat" + "sand"` and `"cats" + "and"`), so it is enqueued twice, but the `visited` set turns the second pop into a no-op instead of a re-expansion: that is the mechanism that keeps each position processed at most once. No word starts at position `7` (neither `"o"` nor `"og"` is in `word_set`), so no pop ever reaches position `9`. The queue drains and the function returns `False`, matching the expected Output.

#### Solution

The code is the pop-and-expand loop from the walkthrough, with the early `return True` firing when a word ends exactly at `len(s)`.

```python
from collections import deque
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        queue = deque([0])  # Start from index 0
        visited = set()     # Track visited indices to avoid cycles

        while queue:
            start_index = queue.popleft()

            # Skip if we've already processed this index
            if start_index in visited:
                continue
            visited.add(start_index)

            # Try all possible words starting from current index
            for end_index in range(start_index + 1, len(s) + 1):
                # If we reached the end of string, segmentation is possible
                if end_index == len(s) and s[start_index:end_index] in word_set:
                    return True

                # If current word is valid, add end_index to queue
                if s[start_index:end_index] in word_set:
                    queue.append(end_index)

        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n³ + m × k)`

Each index is visited once and up to `O(n)` word endings are tried from it, but every candidate `s[start_index:end_index]` is sliced and hashed, which costs up to `O(n)` per candidate since the code never caps the slice length at the longest dictionary word. Capping `end_index` at `start_index` plus the maximum word length is the standard optimization that would bring this to `O(n² × k)`.

##### Space Complexity: `O(n + m × k)`

Space for the queue, visited set, and word set.

#### Key Insights

- The visited set is essential: without it, the same index can be enqueued repeatedly and the search degenerates toward the exponential brute force.
- Reachability is all that matters here, so BFS and DFS are interchangeable for correctness; BFS naturally lends itself to recovering a shortest segmentation if one were needed.
- Each index is processed at most once, which bounds the work and mirrors the memoized formulations.

### Top-Down Memoization

#### Derivation

The BFS repairs the re-exploration by managing an explicit queue, but the recursive shape of the brute force can be kept instead. Its only flaw is recomputation: the answer to "can `s[start_index:]` be segmented?" depends solely on `start_index`, so once computed it can be stored and reused. That is [memoization](https://en.wikipedia.org/wiki/Memoization): the recursion is unchanged, but a `memo` dictionary keyed on `start_index` answers every revisit without recursing.

1. Define `dp(start_index)` as "can `s[start_index:]` be segmented?".
2. On entry, return `memo[start_index]` if this index was already computed.
3. Try each `end_index` whose `current_word = s[start_index:end_index]` is in
   `word_set`, and recurse on `dp(end_index)`.
4. Store the outcome in `memo[start_index]` before returning it.

#### Walkthrough

Example 1 succeeds on its first path, so no index is ever revisited and the memo never fires there. Example 3 does exercise it: `s = "catsandog"`, `wordDict = ["cats","dog","sand","and","cat"]`, expected Output `false`. The trace indents one level per recursive call:

```text
dp(0)  s[0:]="catsandog"       "cat" matches -> recurse
  dp(3)  s[3:]="sandog"        "sand" matches -> recurse
    dp(7)  s[7:]="og"          no word starts here
    dp(7) -> False, memo[7] = False
  dp(3) -> False, memo[3] = False
dp(0)  continues               "cats" matches -> recurse
  dp(4)  s[4:]="andog"         "and" matches -> recurse
    dp(7) -> False             ** memo hit, no recursion **
  dp(4) -> False, memo[4] = False
dp(0) -> False, memo[0] = False
```

Position `7` is reached twice: once through `"cat" + "sand"` and once through `"cats" + "and"`. The first visit scans `"o"` and `"og"`, finds no word, and stores `memo[7] = False`; the second visit returns that stored answer without scanning anything. The brute force would have redone the whole suffix search from `7` for every prefix landing there. With no boundary working anywhere, `dp(0)` returns `False`, matching the expected Output for Example 3.

#### Solution

The code is the brute force recursion with the `memo` lookup and store wrapped around the boundary loop.

```python
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        memo = {}

        def dp(start_index: int) -> bool:
            # Base case: reached end of string
            if start_index == len(s):
                return True

            # Check if result is already computed
            if start_index in memo:
                return memo[start_index]

            # Try all possible words starting from current index
            for end_index in range(start_index + 1, len(s) + 1):
                current_word = s[start_index:end_index]

                # If current word is in dictionary and rest can be segmented
                if current_word in word_set and dp(end_index):
                    memo[start_index] = True
                    return True

            # No valid segmentation found from this index
            memo[start_index] = False
            return False

        return dp(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n³ + m × k)`

Each unique starting index (n positions) is computed at most once, and each tries all possible ending positions (O(n)). Each candidate `s[start_index:end_index]` is sliced and hashed at a cost of up to O(n), because the slice length is not capped by the longest dictionary word, giving O(n³) for the DP portion. Capping the ending position at the maximum word length would tighten this to `O(n² × k)`.

##### Space Complexity: `O(n + m × k)`

O(n) for memoization cache and recursion stack, plus O(m × k) for the word set.

#### Key Insights

- Memoization converts the brute force's exponential tree into a linear set of distinct subproblems, one per starting index.
- It is the same recurrence as the bottom-up DP, only evaluated lazily and in suffix orientation rather than prefix orientation.
- The cache makes the overlapping-subproblems structure explicit, which is the defining property that makes dynamic programming applicable.

### Bottom-Up DP

#### Derivation

The memoized recursion still asks from the top: "can the suffix from here be segmented?". Turn the question around and build from the bottom instead: "can the prefix ending here be segmented?". Let `dp[i]` record whether `s[0:i]` can be segmented. A prefix `s[0:i]` splits cleanly exactly when some earlier boundary `j` has `dp[j]` true and the final piece `s[j:i]` is a dictionary word, so every `dp[i]` is computed from smaller prefixes with no recursion at all: the iterative [bottom-up DP](https://en.wikipedia.org/wiki/Dynamic_programming).

1. Initialize `dp[0] = True` because the empty prefix is trivially
   segmentable.
2. For each end position `i` from `1` to `n`, scan candidate split points
   `j < i` and check whether `dp[j]` holds and `s[j:i]` is in `word_set`.
3. Break on the first valid split (`dp[i]` is settled), and return `dp[n]` as
   the final answer.

#### Recurrence

Let `dp[i]` be true when the prefix `s[0:i]` splits cleanly into dictionary words. Splitting on where the *last* word starts gives a disjunction over every candidate boundary `j`:

$$ dp[i] = \bigvee_{j=0}^{i-1} \Bigl( dp[j] \ \wedge \ s[j{:}i] \in \text{wordDict} \Bigr), \qquad dp[0] = \text{true} $$

```text
dp[0] = True
dp[i] = OR over j = 0 .. i - 1 of (dp[j] and s[j:i] in word_set)
        for 1 <= i <= n
```

\(\bigvee\) is the "or" counterpart of \(\sum\): it runs over the same index range, but combines with logical **or** instead of addition, so `dp[i]` is true as soon as one boundary works. That is exactly what the inner loop's `break` exploits. The empty prefix is vacuously segmentable, which seeds `dp[0]`.

#### Walkthrough

Let us fill `dp` by hand on Example 1: `s = "leetcode"`, `wordDict = ["leet","code"]`, so `n = 8` and `dp` has nine entries with `dp[0] = True`. For each `i` the inner loop scans `j` from `0` upward, asking whether `dp[j]` is true and `s[j:i]` is a word:

```text
i=1   j=0: "l" not a word                            dp[1] = False
i=2   j=0: "le" not a word                           dp[2] = False
i=3   j=0: "lee" not a word                          dp[3] = False
i=4   j=0: dp[0] and s[0:4]="leet" in word_set       dp[4] = True
i=5   j=0: "leetc" no; j=4: "c" no                   dp[5] = False
i=6   j=0: "leetco" no; j=4: "co" no                 dp[6] = False
i=7   j=0: "leetcod" no; j=4: "cod" no               dp[7] = False
i=8   j=0: "leetcode" no; j=4: s[4:8]="code" yes     dp[8] = True
```

Only boundaries `j` with `dp[j]` already true can contribute, so the annotations list just those candidates: from `i = 5` onward they are `j = 0` and `j = 4`. The word `"leet"` ending at `4` sets `dp[4]`, and at `i = 8` the whole-string slice `"leetcode"` fails first before `"code"` continues from the `j = 4` boundary and sets `dp[8]`, where the `break` fires. The function returns `dp[8] = True`, matching the expected Output for Example 1.

#### Solution

The code is the double loop from the walkthrough, with the `break` firing as soon as `dp[i]` is settled.

```python
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # Convert to set for O(1) lookup
        word_set = set(wordDict)
        n = len(s)

        # dp[i] = True if s[0:i] can be segmented into dictionary words
        dp = [False] * (n + 1)
        dp[0] = True  # Base case: empty string can always be segmented

        # For each ending position i in string s
        for i in range(1, n + 1):
            # Try all possible starting positions j for the last word
            for j in range(i):
                # If s[0:j] can be segmented AND s[j:i] is in dictionary
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break  # Found valid segmentation, no need to check further

        return dp[n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n³ + m × k)`

Where n is the length of string s, m is the number of words in wordDict, and k is the maximum length of words. The nested loop runs O(n²) times, and each iteration slices and hashes `s[j:i]`, which can be up to O(n) characters since the code does not cap the slice length at the longest dictionary word. Converting wordDict to a set takes O(m × k). Bounding `i - j` by the maximum word length is the standard optimization that would give `O(n² × k)`.

##### Space Complexity: `O(n + m × k)`

O(n) for the DP array, plus O(m × k) for storing the word set.

#### Key Insights

- Iterating end positions in increasing order guarantees that every `dp[j]` the transition depends on is already finalized.
- The early `break` stops scanning split points as soon as `dp[i]` is established, since one valid segmentation is enough.
- The prefix-oriented state `dp[i]` (can `s[0:i]` be segmented) is the iterative mirror of the memoized suffix recurrence.

### Trie-Based DP

#### Derivation

The bottom-up DP checks each boundary pair `(j, i)` by slicing and hashing `s[j:i]`, paying up to `O(n)` per candidate and testing every length independently. A [Trie](https://en.wikipedia.org/wiki/Trie) (prefix tree) built from the dictionary repairs both costs: starting from a reachable position `i`, descend the Trie following `s[i], s[i+1], ...` one character at a time. Every node marked `is_word` along the descent reveals a word starting at `i`, so one walk discovers all of them at once, and the walk stops the moment the next character has no child, since no dictionary word can extend that span.

1. Build the Trie once: for each `word`, walk `node.children` down from
   `root`, creating nodes as needed, and set `is_word` on the final node.
2. For each position `i` with `dp[i]` true, descend the Trie along the suffix
   `s[i:]`.
3. Mark `dp[j + 1] = True` at every node that completes a word, and break as
   soon as `s[j]` is missing from `node.children`.
4. Return `dp[n]`.

#### Walkthrough

Let us run the Trie walk on Example 1: `s = "leetcode"`, `wordDict = ["leet","code"]`. The Trie holds two branches from `root`: `l-e-e-t` with `is_word` set on the final `t` node, and `c-o-d-e` with `is_word` set on the final `e` node. As before, `dp` starts as `[True, False, ..., False]`, and only positions with `dp[i]` true launch a walk:

```text
i=0     dp[0] True: walk 'l','e','e','t'   is_word at j=3 -> dp[4] = True
        next char s[4]='c' has no child under the 't' node -> break
i=1..3  dp[i] False: no walk
i=4     dp[4] True: walk 'c','o','d','e'   is_word at j=7 -> dp[8] = True
i=5..7  dp[i] False: no walk
```

The walk from `i = 0` finds `"leet"` in one descent and stops immediately after, because no dictionary word continues with `'c'` beyond `"leet"`. The walk from `i = 4` finds `"code"` and reaches the end of the string. No slice is ever taken: each step consumes one character and one child lookup. The function returns `dp[8] = True`, matching the expected Output for Example 1.

#### Solution

The code builds the Trie, then runs the walkthrough's descent from every reachable position `i`.

```python
from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # Build Trie from word dictionary
        root = TrieNode()
        for word in wordDict:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_word = True

        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(n):
            # Only expand from positions we already know are reachable
            if not dp[i]:
                continue

            # Walk the Trie forward over s[i:], marking every word end reachable
            node = root
            for j in range(i, n):
                if s[j] not in node.children:
                    break  # No dictionary word continues past this character

                node = node.children[s[j]]

                if node.is_word:
                    dp[j + 1] = True

        return dp[n]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² + m × k)`

Building the Trie takes O(m × k). The DP portion is O(n²) in the worst case, but the forward Trie walk terminates as soon as the current span stops being a dictionary prefix, which prunes work in practice.

##### Space Complexity: `O(m × k + n)`

The Trie stores all characters from all words, plus the O(n) DP array.

#### Key Insights

- The Trie must be walked forward over `s[i:]` so the descent direction matches the order in which dictionary words were inserted.
- A single forward walk from position `i` discovers every word that starts at `i` at once, instead of testing each candidate length independently.
- The early break on a missing child is the real win: once the current span is not a dictionary prefix, no longer span can be a word either.

### Top-Down Memoization with functools.cache

#### Derivation

The recursion is the algorithm, and none of it changes here: the same scan over every word boundary from `start_index`, the same recursive call on each match, the same base case at `start_index == len(s)`. Only the bookkeeping moves. [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) wraps a function in an unbounded dictionary keyed on its arguments, consulting that dictionary before the body runs and storing the return value after, which is what the explicit `memo` did with `start_index`.

The key is the one detail worth checking. `functools.cache` hashes the argument tuple, so every parameter must be hashable, and `wordDict` is a list. That is not a problem here because the state is a single integer position: `s` and `word_set` are fixed for the whole call and stay captured by the closure rather than passed down, so the cached function takes `start_index` alone. Rewriting the recursion to pass the remaining suffix or the dictionary as parameters would either enlarge the key needlessly or fail outright with `TypeError: unhashable type: 'list'`.

1. Build `word_set = set(wordDict)` for constant-time membership tests.
2. Decorate the inner `dp` with `@cache`, taking `start_index` as its only
   parameter.
3. Write the body as the brute force wrote it: return `True` at
   `start_index == len(s)`, otherwise scan `end_index` upward and recurse on `dp(end_index)` whenever `s[start_index:end_index]` is a dictionary word.
4. Call `dp(0)`. Each of the `n + 1` positions runs the body at most once, and
   every later arrival at a position is answered from the decorator's dictionary.

Five lines vanish: the `memo = {}` declaration, the two-line lookup, and the two stores on the success and failure paths. Defining `dp` inside `wordBreak` also keeps the cache per call, which matters more here than usual: the cached answers depend on `s` and `word_set`, so a cache surviving across calls would return another input's verdicts.

#### Walkthrough

Let us run the decorated recursion on Example 3: `s = "catsandog"`, `wordDict = ["cats","dog","sand","and","cat"]`, whose expected Output is `false`. The trace indents one level per call, noting whether the decorator ran the body or answered from its dictionary:

```text
dp(0)   s[0:]="catsandog"    miss: "cat" matches -> recurse
  dp(3)   s[3:]="sandog"     miss: "sand" matches -> recurse
    dp(7)   s[7:]="og"       miss: no word starts here
    dp(7) -> False
  dp(3) -> False
dp(0)   continues            "cats" matches -> recurse
  dp(4)   s[4:]="andog"      miss: "and" matches -> recurse
    dp(7) -> False           ** cache hit, the body never runs **
  dp(4) -> False
dp(0) -> False
```

Position `7` is reached twice, once through `"cat" + "sand"` and once through `"cats" + "and"`. The first arrival scans `"o"` and `"og"`, finds no word, and returns `False`, which the decorator stores on the way out; the second arrival never enters the body at all. Asking the decorator afterwards confirms the shape of the search: `dp.cache_info()` reports `hits=1, misses=4` with four entries, one for each distinct position the search reached (`0`, `3`, `4`, and `7`). No boundary works anywhere, so `dp(0)` returns `False`, matching the expected Output for Example 3.

#### Solution

The brute force recursion unchanged, with one decorator line above it doing what the memo lookup and the two stores did.

```python
from functools import cache
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)

        # start_index is an int, so @cache can hash it directly. s and
        # word_set stay captured by the closure, keeping them out of the key.
        @cache
        def dp(start_index: int) -> bool:
            # Base case: the whole string was consumed.
            if start_index == len(s):
                return True

            # Try all possible words starting from current index
            for end_index in range(start_index + 1, len(s) + 1):
                current_word = s[start_index:end_index]

                # If current word is in dictionary and rest can be segmented
                if current_word in word_set and dp(end_index):
                    return True

            return False

        return dp(0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n³ + m×k)`

The reachable states are unchanged: each of the `n` starting indices runs its body at most once, trying `O(n)` ending positions, and each candidate `s[start_index:end_index]` is sliced and hashed at a cost of up to `O(n)` because the slice length is not capped by the longest dictionary word, giving `O(n³)` for the search itself. Building `word_set` adds `O(m × k)`. The decorator's lookup hashes one small integer, which is `O(1)`, so it does not enter the bound. Capping the ending position at the maximum word length would tighten the search portion to `O(n² × k)` here exactly as it would for the hand-written memo.

##### Space Complexity: `O(n + m×k)`

The decorator's dictionary holds at most one entry per starting index, so `O(n)`, and the recursion stack reaches `O(n)` depth in the worst case. The word set contributes `O(m × k)`.

#### Key Insights

- Decorating the brute force recursion produces the memoized solution outright,
  which shows how little of memoization is algorithm: the subproblem structure was already there, and only the storage of answers was missing.
- The suffix question depends on `start_index` alone, and that is exactly why a
  cache keyed on the argument tuple works without adjustment: the subproblem state and the function signature already coincide.
- Hashability is the constraint to watch when reaching for `functools.cache`.
  Keeping `s` and `word_set` in the closure keeps the key to one integer, while a signature carrying `wordDict` would raise `TypeError` on the first call because lists are unhashable.
- Because the cached answers are only valid for one `s` and one dictionary, the
  decorated function must be nested inside `wordBreak`. Decorating `wordBreak` itself would also fail on the unhashable `wordDict`, and a module-level cached helper would answer later calls with an earlier input's verdicts.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(2^n)` - Without memoization, overlapping subproblems are re-solved, leading to exponential exploration of partitions.
- **BFS**: `O(n³ + m×k)` - Each index is visited once with O(n) endings, and each uncapped slice costs up to O(n), plus O(m×k) for the word set.
- **Top-Down Memoization**: `O(n³ + m×k)` - Each of n starting indices is computed once, trying O(n) endings whose slices cost up to O(n) each, plus O(m×k) to build the set.
- **Bottom-Up DP**: `O(n³ + m×k)` - The nested loop over positions is O(n²) and each uncapped substring slice costs up to O(n); building the word set takes O(m×k).
- **Trie-Based DP**: `O(n² + m×k)` - Building the Trie takes O(m×k); the DP walk advances one character at a time with no slicing, so each (i, j) pair costs O(1).
- **Top-Down Memoization with functools.cache**: `O(n³ + m×k)`, identical to the hand-written memo, since the decorator hashes one small integer per call and changes neither the state count nor the uncapped slicing.

### Space Complexity

- **Brute Force Recursion**: `O(n)` - Space for the recursion stack, up to n levels deep.
- **BFS**: `O(n + m×k)` - Space for the queue, visited set, and word set.
- **Top-Down Memoization**: `O(n + m×k)` - O(n) for the memo cache and recursion stack, plus O(m×k) for the word set.
- **Bottom-Up DP**: `O(n + m×k)` - O(n) for the DP array plus O(m×k) for the word set.
- **Trie-Based DP**: `O(m×k + n)` - The Trie stores all characters from all words, plus the O(n) DP array.
- **Top-Down Memoization with functools.cache**: `O(n + m×k)`, with O(n) for the decorator's dictionary and the recursion stack, plus O(m×k) for the word set.

### Trade-offs

- **Brute Force Recursion**: Simple to understand, but exponential time makes it impractical for real inputs.
- **BFS**: Offers an alternative graph perspective, but carries extra queue overhead.
- **Top-Down Memoization**: Intuitive recursion that only computes the states it needs, at the cost of recursion overhead.
- **Bottom-Up DP**: Iterative with clear logic, though its uncapped substring slices make it `O(n³)` strict as written.
- **Trie-Based DP**: Can provide early termination when the dictionary shares common prefixes, but has a more complex implementation.
- **Top-Down Memoization with functools.cache**: The same recursion with five lines of dictionary handling deleted, at the cost of losing direct access to the table and of a hashability requirement on the arguments, which forces `s` and `word_set` into the closure.

### When to Use Each

- **Brute Force Recursion**: Only for understanding the problem or very small inputs.
- **BFS**: When modeling as a graph problem or when you need to find the actual segmentation path.
- **Top-Down Memoization**: When recursive thinking feels more natural or for problems requiring path reconstruction.
- **Bottom-Up DP (Recommended)**: Best for interviews: clear iterative logic, easily tightened with the max-word-length cap.
- **Trie-Based DP**: For optimization when the dictionary is large and has many common prefixes.
- **Top-Down Memoization with functools.cache**: The Pythonic default whenever the recursive framing is the one you want. Prefer it over the hand-written memo unless the point is to demonstrate how caching works, or unless the stored answers must be inspected or reused after the call returns.

### Optimization Notes

- Bottom-Up DP is the recommended solution: straightforward iterative logic that is easy to reason about under interview pressure, running in `O(n³ + m×k)` as written.
- Converting `wordDict` to a set is the single most important optimization across every approach, turning O(m×k) list scans into O(k) average-case lookups.
- Capping the inner loop by the maximum dictionary word length (no slice longer than the longest word can ever match) tightens the slicing approaches from `O(n³)` to `O(n² × k)`; the code shown does not apply this cap, but it is the standard follow-up optimization.
- The bottom-up loop can break as soon as any valid split is found for position `i`, avoiding redundant work once `dp[i]` is established.
- Avoid the brute-force recursion without memoization: its `O(2^n)` blowup comes purely from re-solving overlapping subproblems, which both DP variants eliminate.
- `functools.cache` is the shortest route from the brute-force recursion to the memoized bound: it changes no states and no complexity, only which code performs the lookup and the store, so it costs nothing to prefer it over writing the dictionary out.
- The max-word-length cap applies to the decorated recursion exactly as it does to the other slicing approaches, since the decorator only removes bookkeeping and leaves the boundary loop available to tighten.
