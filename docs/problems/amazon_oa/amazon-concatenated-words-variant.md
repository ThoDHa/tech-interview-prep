# [Concatenated Words](https://www.fastprep.io/problems/amazon-concatenated-words-variant)

**Hard** | **NN minutes** | **String, Dynamic Programming, Trie**

Return every word in words that can be formed by concatenating at least two shorter words from the same input.

## Examples

### Example 1

**Input:** `words = ["cat","cats","dog","catsdog","dogcat","rat"]`

**Output:** `["catsdog","dogcat"]`

**Explanation:** catsdog and dogcat each combine two shorter input words.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-concatenated-words-variant; fill them in. -->

## Solutions

### Brute Force

#### Derivation

The most literal reading tests each word on its own: a word is concatenated when it can be cut into consecutive pieces, at least two of them, with every piece an input word. That is a recursive split search. Put the words in `word_set` for constant-time membership tests, then for each word walk a `position` through the word, cutting candidate pieces as you go:

1. Define `can_split(word, position, pieces)` as whether the remaining suffix
   `word[position:]` can be consumed by input words, given that `pieces`
   pieces were already cut.
2. Base case: `position == len(word)` means the whole word was consumed;
   return `pieces >= 2`, which is the "at least two shorter words" rule.
3. Otherwise try every `end_index` from `position + 1` through `len(word)`;
   whenever `word[position:end_index]` is in `word_set`, recurse with
   `can_split(word, end_index, pieces + 1)`.
4. The word qualifies when `can_split(word, 0, 0)` holds; collect qualifying
   words in input order.

Every choice of cut points is a separate branch, so a word of length `L` spawns up to `2^L` distinct split patterns before the answer settles.

#### Walkthrough

Let us run the split search on the qualifying word from Example 1, `catsdog`, with `words = ["cat","cats","dog","catsdog","dogcat","rat"]`. Each indented line is one recursion level; every tried slice is shown with its verdict:

```text
can_split(catsdog, 0, 0)
  "c" no   "ca" no   "cat" yes -> can_split(3, 1)
     "s" no   "sd" no   "sdo" no   "sdog" no           -> False
  "cats" yes -> can_split(4, 1)
     "d" no   "do" no   "dog" yes -> can_split(7, 2)
        position == 7 == len(catsdog): pieces >= 2     -> True
```

The first branch dies because after `"cat"` the remainder `sdog` is not an input word. The second branch cuts `"cats"` and then `"dog"`, lands on `position = 7` with `pieces = 2`, and returns `True`: `catsdog` is `"cats" + "dog"`. The same search finds `dogcat = "dog" + "cat"`, while `cat`, `cats`, `dog`, and `rat` can only ever be consumed as a single piece (`pieces = 1`), so the collected list is `["catsdog", "dogcat"]`, matching the expected Output.

#### Solution

The code is the walkthrough's cut-and-recurse loop wrapped in a per-word check.

```python
from typing import List


class Solution:
    def solve(self, words: List[str]) -> List[str]:
        word_set = set(words)

        def can_split(word: str, position: int, pieces: int) -> bool:
            if position == len(word):
                return pieces >= 2
            for end_index in range(position + 1, len(word) + 1):
                if word[position:end_index] in word_set:
                    if can_split(word, end_index, pieces + 1):
                        return True
            return False

        concatenated = []
        for word in words:
            if can_split(word, 0, 0):
                concatenated.append(word)
        return concatenated
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^L × L)` per word

With `L` the length of the longest word, each word's search enumerates up to `2^L` cut-point sets, and every tried slice hashes up to `L` characters.

##### Space Complexity: `O(L)`

The recursion stack holds one frame per cut, at most `L` deep; the shared `word_set` stores every input character.

#### Key Insights

- The base case `pieces >= 2` is the whole problem statement in one
  comparison: a word consumed as a single piece (pieces = 1) is just a word,
  not a concatenation.
- Reuse is allowed and free: `"a" + "a"` legitimately builds `"aa"`, because
  each piece only needs to be a shorter input word, not a distinct one.
- Correct but exponential: the same suffix is re-split along many different
  prefix pieces, which is exactly the waste the next approach removes.

### Bottom-Up Word Break DP

#### Derivation

The brute force re-splits the same suffix once for every route that reaches it. Whether the suffix `word[start:]` can be consumed depends only on `start`, so a word of length `L` poses only `L` genuinely distinct questions. Answer each once, left to right: let `dp[i]` record whether the prefix `word[0:i]` splits into input words. Then the word is concatenated exactly when some internal boundary `start_index` (from `1` through `len(word) - 1`) sits on a splittable prefix and the final piece `word[start_index:]` is itself an input word, which guarantees at least two pieces:

1. Build `word_set` once and iterate over each `word`.
2. Seed `dp[0] = True` (the empty prefix needs no pieces) and fill `dp[i]`
   for `1 <= i <= len(word) - 1`: `dp[i]` is true when some `j < i` has
   `dp[j]` true and `word[j:i]` in `word_set`.
3. Scan `start_index` from `1` through `len(word) - 1`; at the first one with
   `dp[start_index]` true and `word[start_index:len(word)]` in `word_set`,
   append `word` and move on.
4. The table stops one position short of the word's end, and the final scan
   demands one more dictionary piece after a reachable boundary; together
   those two choices keep every used piece strictly shorter than `word`.

#### Recurrence

Let `dp[i]` be true when the prefix `word[0:i]` splits into input words. Splitting on where the last piece starts gives a disjunction over every candidate boundary `j`:

$$ dp[i] = \bigvee_{j=0}^{i-1} \Bigl( dp[j] \ \wedge \ word[j{:}i] \in \text{word\_set} \Bigr), \qquad dp[0] = \text{true} $$

```text
dp[0] = True
dp[i] = OR over j = 0 .. i - 1 of (dp[j] and word[j:i] in word_set)
        for 1 <= i <= len(word) - 1
concatenated when some start_index in 1 .. len(word) - 1 has
        dp[start_index] and word[start_index:len(word)] in word_set
```

The base case is the empty prefix, which needs no pieces. The table never holds the full-word position, and the answer requires one extra dictionary piece after a reachable boundary, which is what enforces the two-piece minimum.

#### Walkthrough

Let us fill the table for `catsdog` from Example 1 (`len = 7`, table positions `0` through `6`):

```text
dp = [T, F, F, F, F, F, F]     dp[0] = True: the empty prefix
i=3  j=0: word[0:3] = "cat" in word_set           dp[3] = T
i=4  j=0: word[0:4] = "cats" in word_set          dp[4] = T
i=5  j=0: "catsd" no   j=3: dp[3] and "sd" no     dp[5] = F
i=6  j=0: "catsdo" no  j=3: "sdo" no  j=4: "do" no  dp[6] = F
final scan:
  start_index=3: dp[3] T, word[3:7] = "sdog" not a word
  start_index=4: dp[4] T, word[4:7] = "dog" in word_set  -> concatenated
```

Rows whose every candidate `j` sits on a false `dp[j]` (`i = 1`, `i = 2`) are omitted. Boundary `4` is reachable because `"cats"` alone fills `dp[4]`, and the suffix from it is the word `"dog"`, so `catsdog` is reported as `"cats" + "dog"`. The same fill on `dogcat` reaches `dp[3]` through `"dog"` and ends on the suffix `"cat"`, while `cat`, `cats`, `dog`, and `rat` never gain a reachable internal boundary with a word suffix, so the result is `["catsdog", "dogcat"]`, matching the expected Output.

#### Solution

The code is the walkthrough's table fill followed by the boundary scan.

```python
from typing import List


class Solution:
    def solve(self, words: List[str]) -> List[str]:
        word_set = set(words)
        concatenated = []
        for word in words:
            length = len(word)
            dp = [False] * length
            dp[0] = True
            for i in range(1, length):
                for j in range(i):
                    if dp[j] and word[j:i] in word_set:
                        dp[i] = True
                        break
            for start_index in range(1, length):
                if dp[start_index] and word[start_index:length] in word_set:
                    concatenated.append(word)
                    break
        return concatenated
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L³)` per word

With `L` the longest word's length, each word pairs every boundary with every earlier boundary, `O(L²)` pairs, and each pair slices and hashes a piece of up to `L` characters.

##### Space Complexity: `O(L)` per word

The table holds one entry per position of the current word; the shared `word_set` stores every input character.

#### Key Insights

- Anchoring each subproblem at a boundary instead of a route is what removes
  the brute force's re-splitting: `L` questions, each answered exactly once.
- The table deliberately excludes the full-word position and the final scan
  asks for one more word after a reachable boundary; that pair of choices is
  what turns plain word break into "at least two pieces".
- The early `break` in both loops stops at the first working boundary,
  because one valid split is all the problem asks for.

### Trie-Based Word Break DP

#### Derivation

The bottom-up DP pays `O(L)` for every boundary pair, slicing and hashing `word[j:i]` per pair. A [trie](https://en.wikipedia.org/wiki/Trie) (prefix tree) over the dictionary replaces that with one child lookup per character: from a reachable boundary, walk the trie along the word's own characters, and every node marked `is_word` on the way marks another reachable boundary. The walk dies the moment the next character has no child, since no input word continues that span, so one descent from a boundary discovers every piece starting there at once.

1. Build the trie once from all words, setting `is_word` on each word's final
   node.
2. Per word, fill the same boundary table: from every `start_index` with
   `dp[start_index]` true, descend the trie over `word[start_index:]` and
   mark `dp[position + 1] = True` at every `is_word` node, guarded by
   `position + 1 < len(word)` so the word never consumes itself whole.
3. For each internal boundary with `dp[start_index]` true, walk the trie over
   the suffix `word[start_index:]`; when that walk ends on an `is_word` node,
   the prefix splits and the suffix is a word, so append the word.
4. Collect results in input order.

#### Walkthrough

Let us walk the trie for `catsdog` from Example 1. The trie holds one path per input word, with `is_word` on the final node of `cat`, `cats`, `dog`, `catsdog`, `dogcat`, and `rat`:

```text
dp = [T, F, F, F, F, F, F]     dp[0] = True: the empty boundary
forward walk from 0:  c, a, t -> is_word, dp[3] = T
                      s       -> is_word, dp[4] = T
                      d, o, g -> is_word at position 6,
                                 6 + 1 = 7 = len: guarded, not marked
forward walk from 3:  s has no child under the root: walk dies
forward walk from 4:  d, o, g -> is_word at position 6: guarded
from 1, 2, 5: dp False, no walk
suffix walk from 3: 's' has no child under the root          -> no
suffix walk from 4: "dog" ends on an is_word node            -> concatenated
```

The walk from boundary `0` passes straight through the full word's node (`catsdog` is in the trie), and the guard is what refuses to mark it as a boundary: the word cannot be one of its own pieces. Boundary `4` stays the qualifying split, with prefix `"cats"` and suffix `"dog"`, so the function appends `catsdog`; `dogcat` behaves identically through `dp[3]`, and the result is `["catsdog", "dogcat"]`, matching the expected Output.

#### Solution

The code builds the trie, runs the guarded forward walks to fill `dp`, then scans internal boundaries with a suffix walk.

```python
from typing import Dict, List


class TrieNode:
    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_word = False


class Solution:
    def solve(self, words: List[str]) -> List[str]:
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_word = True

        def ends_at_word(text: str, start_index: int) -> bool:
            node = root
            for position in range(start_index, len(text)):
                if text[position] not in node.children:
                    return False
                node = node.children[text[position]]
            return node.is_word

        concatenated = []
        for word in words:
            length = len(word)
            dp = [False] * length
            dp[0] = True
            for start_index in range(length):
                if not dp[start_index]:
                    continue
                node = root
                for position in range(start_index, length):
                    if word[position] not in node.children:
                        break
                    node = node.children[word[position]]
                    # The word itself must not count as one of its own pieces
                    if node.is_word and position + 1 < length:
                        dp[position + 1] = True
            for start_index in range(1, length):
                if dp[start_index] and ends_at_word(word, start_index):
                    concatenated.append(word)
                    break
        return concatenated
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L²)` per word

Building the trie costs one step per input character, shared across all words; each word then runs at most `L` forward walks and `L` suffix walks of `O(L)` character steps each, one child lookup per step with no slicing or hashing.

##### Space Complexity: `O(L)` per word

The table holds one entry per position of the current word; the trie stores every input character once, shared across words.

#### Key Insights

- One forward walk from a boundary finds every piece starting there in a
  single descent, replacing the DP's per-length slice-and-hash with child
  lookups.
- The guard `position + 1 < length` is the "at least two pieces" rule in
  trie form: the walk from boundary `0` may pass through the whole word's
  node but may never mark the word's own end as a reachable boundary.
- The early death of a forward walk (a character with no child) is the real
  win over slicing: no input word continues that span, so no longer piece
  can exist either.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(2^L × L)` per word - enumerates cut-point sets and slices every candidate piece.
- **Bottom-Up Word Break DP**: `O(L³)` per word - `O(L²)` boundary pairs, each slicing and hashing up to `L` characters.
- **Trie-Based Word Break DP**: `O(L²)` per word - `O(L)` character steps per boundary at one child lookup each, after an `O(total characters)` trie build.

### Space Complexity

- **Brute Force**: `O(L)` - recursion depth bounded by the word's length.
- **Bottom-Up Word Break DP**: `O(L)` - one table entry per position of the current word.
- **Trie-Based Word Break DP**: `O(L)` - one table entry per position, plus the shared trie.

### Trade-offs

- The Brute Force is the problem statement transcribed directly and needs no structure beyond the word set, but exponential re-splitting confines it to short words.
- The Bottom-Up Word Break DP is the straightforward repair: each boundary answered once, at the price of `O(L)` slicing and hashing per boundary pair.
- The Trie-Based Word Break DP removes the per-pair slicing cost and abandons dead spans early, at the price of building and carrying a prefix tree.

### When to Use Each

- **Brute Force**: as the correctness oracle on tiny inputs and the clearest statement of the two-piece minimum.
- **Bottom-Up Word Break DP** (recommended): the default interview answer; the boundary table is easy to reason about and to adapt when the problem is extended.
- **Trie-Based Word Break DP**: when the dictionary is large with shared prefixes, or when a follow-up streams characters instead of slicing substrings.

### Optimization Notes

- Both table versions break out of their loops at the first working boundary; on inputs where most words do not qualify, the break in the fill loop is the bigger saver because it prunes per-position work.
- Bucketing words by length lets every version skip spans longer than the longest dictionary word; the trie version gets this for free through the walk's early death.
- The suffix walk can be folded into the forward walks (a boundary qualifies when some walk continues from it to an `is_word` node at the word's end), saving a pass per word at some cost in clarity.
- Words are independent of one another, so the outer loop parallelizes trivially if a follow-up scales the word count.
