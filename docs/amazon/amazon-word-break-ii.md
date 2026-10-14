# [Word Break II](https://www.fastprep.io/problems/amazon-word-break-ii)

**Hard** | **NN minutes** | **Array, Hash Table, String, Dynamic Programming, Backtracking, Trie**

Given a string s and an array of unique dictionary words wordDict, insert spaces into s so that every resulting token is a dictionary word.

Return every valid sentence in lexicographic order. A dictionary word may be reused any number of times.

## Examples

### Example 1

**Input:** `s = "catsanddog"`, `wordDict = ["cat","cats","and","sand","dog"]`

**Output:** `["cat sand dog","cats and dog"]`

**Explanation:** The string can be segmented as cat sand dog or cats and dog. The two sentences are returned in lexicographic order.

### Example 2

**Input:** `s = "pineapplepenapple"`, `wordDict = ["apple","pen","applepen","pine","pineapple"]`

**Output:** `["pine apple pen apple","pine applepen apple","pineapple pen apple"]`

**Explanation:** All three sentences concatenate to pineapplepenapple, and dictionary words such as apple may be reused.

### Example 3

**Input:** `s = "catsandog"`, `wordDict = ["cats","dog","sand","and","cat"]`

**Output:** `[]`

**Explanation:** No sequence of dictionary words concatenates to the entire string.

## Constraints

- `1 <= s.length <= 20`
- `1 <= wordDict.length <= 1000`
- `1 <= wordDict[i].length <= 10`
- `s and every wordDict[i] contain only lowercase English letters.`
- `All strings in wordDict are unique.`
- `The total length of all valid output sentences does not exceed 10^5.`

## Solutions

### Brute Force Recursion

#### Derivation

The literal reading: every valid sentence begins with some dictionary word, and after peeling that word off the front, the rest of the string poses the same question again. That recursive structure is [backtracking](https://en.wikipedia.org/wiki/Backtracking): try every word that could start at the current position, recurse on what remains, and record a sentence every time the whole string is consumed.

1. Put the words in `word_set` for constant-time membership tests.
2. From `start_index`, try every word boundary `end_index` and slice
   `current_word = s[start_index:end_index]`.
3. When `current_word` is a dictionary word, append it to `words_used`, recurse
   via `collect_sentences(end_index, words_used)`, then pop it again so the trail stays one shared list.
4. When `start_index == n`, the whole string is consumed: join `words_used`
   with single spaces and append the sentence to `sentences`.
5. Return `sorted(sentences)`, since the statement demands lexicographic order
   and the search itself makes no ordering promise.

#### Walkthrough

Example 1: `s = "catsanddog"`, `wordDict = ["cat","cats","and","sand","dog"]`, so `n = 10`. The boundary loop scans `end_index` left to right, which is why `"cat"` is tried before `"cats"` at position 0:

```text
collect_sentences(0)   s[0:] = "catsanddog"
  "cat"  -> collect_sentences(3)   s[3:] = "sanddog"
    "sand" -> collect_sentences(7)   s[7:] = "dog"
      "dog" -> collect_sentences(10)   start_index == n: append "cat sand dog"
    no other boundary at 3 works: "s", "sa", "sandd", ..., "sanddog" all fail
  "cats" -> collect_sentences(4)   s[4:] = "anddog"
    "and" -> collect_sentences(7)   s[7:] = "dog"
      "dog" -> collect_sentences(10): append "cats and dog"
    no other boundary at 4 works: "a", "an", "andd", ..., "anddog" all fail
```

Both leaves reach `start_index == 10` and append one sentence each, so `sentences` holds `["cat sand dog", "cats and dog"]` before the sort, which matches the expected Output. Example 3 (`s = "catsandog"`) shows the failure mode: the branches through `"cat"` and `"cats"` both reach position 7, both discover that no word starts at `"og"`, and both die there, so `sentences` stays empty and the function returns `[]`.

#### Solution

The code is the search tree from the walkthrough: one loop over `end_index`, one recursive call per matching word, one append per complete path.

```python
from typing import List


class Solution:
    def solve(self, s: str, wordDict: List[str]) -> List[str]:
        word_set = set(wordDict)
        n = len(s)
        sentences: List[str] = []

        def collect_sentences(start_index: int, words_used: List[str]) -> None:
            if start_index == n:
                sentences.append(" ".join(words_used))
                return
            for end_index in range(start_index + 1, n + 1):
                current_word = s[start_index:end_index]
                if current_word not in word_set:
                    continue
                words_used.append(current_word)
                collect_sentences(end_index, words_used)
                words_used.pop()

        collect_sentences(0, [])
        return sorted(sentences)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n × n)`

The search re-explores the same suffix along every prefix that reaches it. When the dictionary offers words of many lengths (an all-`"a"` string with words `"a"`, `"aa"`, `"aaa"`, ...), the number of complete segmentations grows exponentially in `n`, and each complete path costs up to `O(n)` to join into a sentence, hence the extra factor.

##### Space Complexity: `O(n + L)`

The recursion nests at most `n` frames deep and `words_used` holds at most one word per boundary, while the output list stores all `L` characters of the returned sentences (the constraint bounds `L` by `10^5`).

#### Key Insights

- Every prefix that matches a word spawns an independent suffix search, and the exponential cost comes from re-searching the same suffix along many different prefixes; nothing remembers what a suffix can produce.
- `words_used` with the append/pop trail is the standard backtracking pattern: one shared list instead of copying a fresh list on every call.
- The final `sorted` call is what honors the lexicographic requirement. Discovery order follows the dictionary and the boundary scan, not sentence order.

### Backtracking with Reachability Pruning

#### Derivation

The brute force walks into subtrees that cannot possibly finish: on Example 3 it recurses to position 7 twice and each time re-discovers that `"og"` is hopeless. The repair is to answer the decision question "can the suffix starting here be segmented?" once per position, up front, with the same boolean table the [Word Break](amazon-word-break.md) decision problem uses: `can_reach_end[i]` is `True` exactly when `s[i:]` splits into dictionary words. The backtracking then refuses to step onto any position holding `False`, so every branch it explores still leads to at least one complete sentence and no work is spent on doomed subtrees:

1. Build `can_reach_end` right to left: `can_reach_end[n] = True` for the empty
   suffix, and position `start` becomes `True` when some slice `s[start:end]` is a dictionary word with `can_reach_end[end]` already `True`.
2. Cap `end` at `start + max_word_length` during the sweep: no slice longer than
   the longest dictionary word can match, so longer candidates are pure waste.
3. Run the brute force backtracking unchanged except for one extra guard: a
   candidate `end_index` must pass `can_reach_end[end_index]` before the recursion.
4. Collect the sentences and return them sorted.

#### Walkthrough

Example 1: `s = "catsanddog"`, `n = 10`, and the longest word is `"sand"` or `"cats"`, so `max_word_length = 4`. The sweep fills `can_reach_end` from right to left:

```text
can_reach_end[10] = True    (empty suffix, base case)
start 9   "g" no word                              -> False
start 8   "og" no word                             -> False
start 7   "dog" in word_set, can_reach_end[10]     -> True
start 6   "d", "dd", "ddo", "ddog" none match      -> False
start 5   "n", "nd", "ndd", "nddo" none match      -> False
start 4   "and" in word_set, can_reach_end[7]      -> True
start 3   "sand" in word_set, can_reach_end[7]     -> True
start 2   "t", "ts", "tsa", "tsan" none match      -> False
start 1   "a", "at", "ats", "atsa" none match      -> False
start 0   "cat" in word_set, can_reach_end[3]      -> True
```

The backtracking from position 0 now consults the table on every step. At `start_index = 0` the candidate `"cat"` survives because `can_reach_end[3]` is `True`, and the path `"cat" -> "sand" -> "dog"` lands on `can_reach_end[10]` to append `"cat sand dog"`; the path `"cats" -> "and" -> "dog"` appends `"cats and dog"` the same way. On Example 3 (`s = "catsandog"`) the sweep sets no entry to `True` except the base case: `can_reach_end[3]` and `can_reach_end[4]` both come out `False` because position 7 cannot finish. The backtracking then examines `"cat"` and `"cats"` at position 0, rejects both on the table without recursing once, and returns `[]`, matching the expected Output.

#### Solution

The code is the brute force search plus the `can_reach_end` gate on every step, with the sweep capped at the longest word.

```python
from typing import List


class Solution:
    def solve(self, s: str, wordDict: List[str]) -> List[str]:
        word_set = set(wordDict)
        max_word_length = max(len(word) for word in wordDict)
        n = len(s)

        can_reach_end = [False] * (n + 1)
        can_reach_end[n] = True
        for start in range(n - 1, -1, -1):
            for end in range(start + 1, min(start + max_word_length, n) + 1):
                if can_reach_end[end] and s[start:end] in word_set:
                    can_reach_end[start] = True
                    break

        sentences: List[str] = []

        def collect_sentences(start_index: int, words_used: List[str]) -> None:
            if start_index == n:
                sentences.append(" ".join(words_used))
                return
            for end_index in range(start_index + 1,
                                   min(start_index + max_word_length, n) + 1):
                if not can_reach_end[end_index]:
                    continue
                current_word = s[start_index:end_index]
                if current_word not in word_set:
                    continue
                words_used.append(current_word)
                collect_sentences(end_index, words_used)
                words_used.pop()

        collect_sentences(0, [])
        return sorted(sentences)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(S × n × k^2 + L)`

With `n = len(s)`, `k` the longest word, `S` the number of sentences, and `L` the total output length: the feasibility sweep tries up to `k` slice lengths per position and each slice-and-hash costs `O(k)`, so it adds `O(n × k^2)`. Every backtracking call stands at a position whose `can_reach_end` entry is `True`, and every such subtree contains at least one complete sentence, so the search performs at most `S × n` calls, each scanning up to `k` capped slices at `O(k)` per slice-and-hash. Joining the words of every sentence adds the `L` term.

##### Space Complexity: `O(n + L)`

The boolean table takes `O(n)`, the recursion and `words_used` hold at most one entry per boundary (`O(n)`), and the output list stores all `L` characters of the returned sentences.

#### Key Insights

- The decision DP and the enumeration DFS answer different questions ("can this suffix be segmented?" versus "list every segmentation"), and composing them keeps the enumeration from ever entering a subtree with no sentence in it.
- A position may be reachable through perfectly valid words and still be a dead end; the `can_reach_end` gate detects that before the recursion pays for it, which is exactly where the brute force used to waste its work.
- Capping the slice scan at `max_word_length` is a free win: no slice longer than the longest word can match, and the cap is what keeps both the sweep and each backtracking call at `O(k^2)` instead of degrading toward `O(n^2)` per position.

### Memoized Suffix Sentences

#### Derivation

The pruning version still re-derives what follows a shared position every time the search lands on it. Asking "what are all the sentences that cover the suffix starting here?" is a function of `start_index` alone, so its answers can be computed once and reused: that is [memoization](https://en.wikipedia.org/wiki/Memoization), and the answer itself is a list of sentences rather than a boolean. [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache) holds the cache: it consults its dictionary before the body runs and stores the returned list after, which is all the bookkeeping this formulation needs.

1. Define `sentences_from(start_index)` as every sentence covering
   `s[start_index:]`.
2. Base case: `sentences_from(n)` returns `[""]`, the single empty tail.
3. For every dictionary word `current_word` starting at `start_index`, join it
   to every tail in `sentences_from(end_index)`.
4. Decorate the function with `@cache` so each position computes its list once.
5. Return `sorted(sentences_from(0))`.

#### Recurrence

Let `sentences(i)` be the list of sentences covering the suffix `s[i:]`, and let `w ∥ t` denote the word `w` joined to the tail `t` with a single space (just `w` when `t` is empty):

$$ \text{sentences}(i) = \{\, w \mathbin{\|} t \;:\; w \in \text{wordDict},\ s[i : i + |w|] = w,\ t \in \text{sentences}(i + |w|) \,\}, \qquad \text{sentences}(n) = \{\, \epsilon \,\} $$

```text
sentences(n) = [""]      (epsilon: the empty tail)
sentences(i) = [join(word, tail)
                for each end_index with word = s[i:end_index] in word_set
                for tail in sentences(end_index)]
join(word, tail) = word + " " + tail   when tail is not empty
                 = word                when tail is empty
```

`sentences(n) = [""]` encodes "the empty suffix is covered by exactly one empty tail", which lets the innermost join produce a bare word instead of special-casing the last word. Every later position reads only strictly larger indices, so one downward pass (or the recursion, which visits the same order) fills the table, and `sentences(0)` is the answer.

#### Walkthrough

Example 1: `s = "catsanddog"`, `n = 10`. The recursion computes each suffix once, deepest position first, and the merge at position 0 joins `"cat"` and `"cats"` to the cached tails:

```text
sentences_from(10) -> [""]                          base case
sentences_from(7)  word "dog":  tails [""]          -> ["dog"]
sentences_from(3)  word "sand": tails ["dog"]       -> ["sand dog"]
sentences_from(4)  word "and":  tails ["dog"]       -> ["and dog"]
sentences_from(0)  word "cat":  tails ["sand dog"]  -> "cat sand dog"
                   word "cats": tails ["and dog"]   -> "cats and dog"
                   -> ["cat sand dog", "cats and dog"]
```

The `[""]` base case is what lets `sentences_from(7)` produce the bare word `"dog"` rather than `"dog "` with a trailing space. The final sort leaves the list unchanged here, and it matches the expected Output for Example 1. Example 2 (`"pineapplepenapple"`) shows the cache earning its keep: `sentences_from(9)` is computed while the `"pine"` branch expands, and when the `"pineapple"` branch later lands on position 9 the decorator returns the stored list without running the body again. On Example 3 the dead suffixes (`3`, `4`, and `7`) are each scanned once, cached as empty lists, and never scanned again.

#### Solution

The code is the recurrence read top to bottom: every word starting at `start_index` is joined to the cached tails of the suffix where it ends.

```python
from functools import cache
from typing import List


class Solution:
    def solve(self, s: str, wordDict: List[str]) -> List[str]:
        word_set = set(wordDict)
        max_word_length = max(len(word) for word in wordDict)
        n = len(s)

        @cache
        def sentences_from(start_index: int) -> List[str]:
            if start_index == n:
                return [""]
            collected: List[str] = []
            for end_index in range(start_index + 1,
                                   min(start_index + max_word_length, n) + 1):
                current_word = s[start_index:end_index]
                if current_word not in word_set:
                    continue
                for tail in sentences_from(end_index):
                    if tail:
                        collected.append(current_word + " " + tail)
                    else:
                        collected.append(current_word)
            return collected

        return sorted(sentences_from(0))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × k^2 + L)`

Each of the `n` suffix positions computes its list at most once, scanning up to `k` capped slice lengths at `O(k)` per slice-and-hash. Every string the merge builds is a sentence of some suffix, and all of those sentences together are bounded by the total output length `L`, so construction adds a linear-in-output term rather than an extra asymptotic factor.

##### Space Complexity: `O(L + n)`

The cache stores one list per computed suffix, and every stored sentence spells a distinct span of `s`, so the stored characters total `O(L)`; the recursion nests at most `n` frames before reaching the base case.

#### Key Insights

- Caching composes cleanly here because the subproblem answer is a reusable part: the sentences of a suffix are used verbatim as the tails of longer sentences, never re-derived.
- The state is a single integer, which is exactly why `@cache` works unadjusted: `s` and `word_set` stay captured by the closure, out of the hash key, and nesting the decorated function inside `solve` keeps the cache per call, so answers from one input can never leak into another.
- No deduplication is needed: two different boundaries at a position produce words of different lengths, hence different first tokens, and the same word always lands on the same suffix, so every (word, tail) pair is distinct.
- Dead suffixes are not free here, but they are cheap: a suffix with no segmentation is scanned once, its empty list is cached, and every later arrival is answered from the cache.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(2^n × n)` - exponentially many partial segmentations are explored, and each complete path pays `O(n)` to join.
- **Backtracking with Reachability Pruning**: `O(S × n × k^2 + L)` - the reachability table confines the search to subtrees that finish, so the work tracks the sentence count.
- **Memoized Suffix Sentences**: `O(n × k^2 + L)` - every suffix computes its sentence list once, and building the strings is bounded by the output.

### Space Complexity

- **Brute Force Recursion**: `O(n + L)` - recursion depth and the `words_used` trail are `O(n)`, plus the output.
- **Backtracking with Reachability Pruning**: `O(n + L)` - the boolean table, the recursion, and the trail are all `O(n)`, plus the output.
- **Memoized Suffix Sentences**: `O(L + n)` - the cache holds every computed suffix's sentences, which total `O(L)` characters, plus `O(n)` recursion depth.

### Trade-offs

- **Brute Force Recursion**: the shortest code and the clearest mirror of the statement, but exponential time makes it usable only on tiny inputs.
- **Backtracking with Reachability Pruning**: never enters a doomed subtree, and it holds only the current path in memory while it works, but it re-walks the tails of a shared suffix once per path that reaches it.
- **Memoized Suffix Sentences**: computes each suffix's tails exactly once, which shines when many paths converge on the same positions, at the cost of holding every suffix's sentences in the cache for the duration of the call.

### When to Use Each

- **Brute Force Recursion**: to establish correctness and the recursive shape of the problem, or when `n` is tiny and the dictionary is friendly.
- **Backtracking with Reachability Pruning (Recommended)**: the default interview answer: the feasibility sweep is five lines, memory stays proportional to one path plus the output, and the pruning story is easy to explain.
- **Memoized Suffix Sentences**: when many search paths converge on the same suffixes (highly repetitive strings), or when the memoized framing is the one that comes to mind and the input is small enough that the cache is irrelevant.

### Optimization Notes

- The reachability sweep and the backtracking loop both cap their boundary scan at `max_word_length`; dropping the cap costs a factor of `n` per position for no benefit.
- Both collecting solutions return `sorted(sentences)`, which is the honest way to meet the lexicographic requirement: the alternative, iterating candidate words alphabetically so the search emits sorted sentences directly, works only because a space sorts before every letter and is easy to get subtly wrong.
- `functools.cache` must wrap a function defined inside `solve`: the cached lists depend on this call's `s` and `word_set`, and a cache surviving across calls would return one input's sentences for another.
- In fixed-width languages the output bound (`10^5` characters) and the exponential path count make the brute force not just slow but unbounded in practice; the pruning or memoized forms are the only ones that scale with the actual output.
