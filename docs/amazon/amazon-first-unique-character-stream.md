# [First Unique Character in a Stream](https://www.fastprep.io/problems/amazon-first-unique-character-stream)

**Medium** | **NN minutes** | **String, Hash Table, Queue**

Characters arrive in the order of the string stream. After each arrival, append the earliest character seen so far whose frequency in the processed prefix is exactly one.

If the current prefix has no unique character, append #. Return the concatenation of all per-arrival answers. Comparisons are case-sensitive.

Sibling variants: same core, different skinThese four problems are sibling variants of the same first-unique pattern. Their story wrappers and query timing differ, while the core rule keeps the earliest value whose frequency is exactly one.

Longest-Waiting Unique TaskDynamic Longest-Waiting Unique Task QueriesFirst User to Log In Exactly OnceFirst Unique Character in a Stream (current)

## Examples

### Example 1

**Input:** `stream = "aabc"`

**Output:** `"a#bb"`

**Explanation:** The first a is unique, then none is unique, and b remains first after c arrives.

### Example 2

**Input:** `stream = "zz"`

**Output:** `"z#"`

**Explanation:** The only character stops being unique after its second occurrence.

### Example 3

**Input:** `stream = "abc"`

**Output:** `"aaa"`

**Explanation:** The earliest a remains unique throughout all three prefixes.

## Constraints

- `1 ≤ stream.length ≤ 100000.`
- `stream contains only ASCII letters and digits.`
- `The sentinel # does not occur in stream.`

## Solutions

### Prefix Rescan with a Tally

#### Derivation

The most literal reading of the problem follows the sentence structure: after each arrival, look at everything received so far and answer "which character is unique?". Answering that question from scratch per arrival needs a frequency count of the prefix plus an in-order scan for the first character whose count is one. Python's `str.count` supplies the tally, so the literal version counts inside the scan:

1. Build `result_chars`, an empty list of one-character strings.
2. For each `end` in `range(1, len(stream) + 1)`, take `prefix = stream[:end]`.
3. Scan `prefix` in order; append the first `character` with
   `prefix.count(character) == 1`, or `"#"` when none qualifies.
4. Return `"".join(result_chars)`.

#### Walkthrough

Example 1, `stream = "aabc"`:

```text
prefix "a"     tally a -> 1      first count-1: 'a'  -> append "a"
prefix "aa"    tally a -> 2      no count-1          -> append "#"
prefix "aab"   a -> 2, b -> 1    'a' fails, 'b' passes -> append "b"
prefix "aabc"  a -> 2, b -> 1, c -> 1  'b' passes    -> append "b"
join -> "a#bb"
```

The join produces `"a#bb"`, matching the expected Output.

#### Solution

```python
class Solution:
    def solve(self, stream: str) -> str:
        """Return the per-arrival earliest unique character, # when none.

        Time:  O(n^2): each of the n arrivals recounts and rescans a
            prefix of up to n characters.
        Space: O(n): the result list plus the prefix slice.
        """
        result_chars: List[str] = []
        for end in range(1, len(stream) + 1):
            prefix = stream[:end]
            for character in prefix:
                if prefix.count(character) == 1:
                    result_chars.append(character)
                    break
            else:
                result_chars.append("#")
        return "".join(result_chars)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each of the `n` arrivals builds a prefix of up to `n` characters and scans it with `str.count`, which itself walks the prefix per candidate.

##### Space Complexity: `O(n)`

The result list holds `n` characters, and each prefix slice holds up to `n`.

#### Key Insights

- The brute force answers each arrival independently, which is exactly its flaw: earlier counts are recomputed for every later prefix.
- The `for`/`else` form captures the "#" fallback without a sentinel variable.

### Queue with Frequency Table

#### Derivation

The brute force re-tallies the whole prefix per arrival. The repair is incremental bookkeeping: keep a running `frequencies` table, updating one entry per arrival, and keep the candidate answer in arrival order. Arrival order is exactly a [queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)): every occurrence enters the queue when it arrives, and the front of the queue is the earliest character still pending. A character stops being unique as soon as its count passes one, so the maintenance rule is to pop the front while the front's count exceeds one. What remains at the front is the earliest character with count exactly one:

1. Allocate `frequencies`, a `defaultdict(int)`, and `candidates`, a `deque`.
2. For each `character` of `stream`: increment `frequencies[character]` and
   append `character` to `candidates`.
3. While `candidates` is non-empty and
   `frequencies[candidates[0]] > 1`, pop the front; each stale occurrence
   leaves the queue at most once.
4. Append the front's character, or `"#"` when the queue emptied.
5. Return the joined result.

#### Walkthrough

Example 1, `stream = "aabc"`, one line per arrival showing the tally update, the cleanup, and the read of the front:

```text
arrive 'a'   frequencies a -> 1   queue [a]     front 'a' unique   append "a"
arrive 'a'   frequencies a -> 2   queue [a, a]  pop 'a', pop 'a'   queue empty, append "#"
arrive 'b'   frequencies b -> 1   queue [b]     front 'b' unique   append "b"
arrive 'c'   frequencies c -> 1   queue [b, c]  front 'b' unique   append "b"
join -> "a#bb"
```

The join produces `"a#bb"`, matching the expected Output. The second arrival shows the cleanup doing all the work: both `a` occurrences were already in the queue, and their count passing one evicts both.

#### Solution

The code is the walkthrough's update, cleanup, and read:

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def solve(self, stream: str) -> str:
        """Return the per-arrival earliest unique character, # when none.

        Time:  O(n): each occurrence is enqueued once and popped at most
            once, so total queue work is linear.
        Space: O(n): the queue can hold every occurrence of the stream.
        """
        frequencies = defaultdict(int)
        candidates = deque()
        result_chars: List[str] = []

        for character in stream:
            frequencies[character] += 1
            candidates.append(character)

            while candidates and frequencies[candidates[0]] > 1:
                candidates.popleft()

            if candidates:
                result_chars.append(candidates[0])
            else:
                result_chars.append("#")

        return "".join(result_chars)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each occurrence is appended once and popped at most once over the whole run, so the cleanup adds amortized constant work per arrival; everything else is constant per arrival.

##### Space Complexity: `O(n)`

The queue may hold every occurrence of the stream: when a stale head never leaves, every later occurrence piles up behind it, so the occupancy is bounded by `n`, not by the alphabet.

#### Key Insights

- Counting incrementally turns the per-arrival tally from `O(prefix)` into `O(1)`.
- The queue order is arrival order, so "earliest still-unique character" is literally the front after stale entries are evicted.
- Stale occurrences are removed lazily: their counts, not positions, trigger the eviction, so no index bookkeeping is needed.
- The queue size is input-bounded, not alphabet-bounded; the next approach caps memory at the distinct-character count.

### Unique List with Position Removal

#### Derivation

The queue can hold the same character many times, yet only one copy of any character can ever be the answer: a character is a candidate exactly while its count is one. Tracking each character's single candidate position shrinks the structure to distinct characters. A [doubly linked list](https://en.wikipedia.org/wiki/Doubly_linked_list) holding the still-unique characters in arrival order supports both maintenance operations in worst-case constant time: append at the tail when a character is new, unlink in the middle when a character repeats. Reading the head after each arrival answers the query, and the head moves only forward:

1. Build `head` and `tail` sentinels around an empty list.
2. Allocate `nodes`, mapping each character to its list node or to `None`
   once the character has repeated.
3. Per arrival of `character`:
   - seen before with a node: unlink that node and set
     `nodes[character] = None`;
   - never seen: append a fresh node at the tail and record it.
4. Append the head's character, or `"#"` when the list is empty.
5. Return the joined result.

#### Walkthrough

Example 1, `stream = "aabc"`, showing the list between sentinels after each arrival:

```text
arrive 'a'   new      list [a]         head 'a'   append "a"
arrive 'a'   repeats  list []          empty      append "#"
arrive 'b'   new      list [b]         head 'b'   append "b"
arrive 'c'   new      list [b, c]      head 'b'   append "b"
join -> "a#bb"
```

The join produces `"a#bb"`, matching the expected Output. Example 2, `stream = "zz"`, runs `[z]` then `[]` and yields `"z#"`. Example 3, `stream = "abc"`, grows `[a]`, `[a, b]`, `[a, b, c]` with `a` at the head throughout, yielding `"aaa"`.

#### Solution

```python
from typing import Dict, List, Optional


class UniqueNode:
    def __init__(self, character: str) -> None:
        self.character = character
        self.previous: Optional[UniqueNode] = None
        self.next: Optional[UniqueNode] = None


class Solution:
    def solve(self, stream: str) -> str:
        """Return the per-arrival earliest unique character, # when none.

        Time:  O(n): each arrival does worst-case constant list work,
            with no amortization over late arrivals.
        Space: O(k) for the list, k the number of distinct characters.
        """
        head = UniqueNode("")
        tail = UniqueNode("")
        head.next = tail
        tail.previous = head
        nodes: Dict[str, Optional[UniqueNode]] = {}
        result_chars: List[str] = []

        for character in stream:
            if character in nodes:
                node = nodes[character]
                if node is not None:
                    node.previous.next = node.next
                    node.next.previous = node.previous
                    nodes[character] = None
            else:
                node = UniqueNode(character)
                node.previous = tail.previous
                node.next = tail
                tail.previous.next = node
                tail.previous = node
                nodes[character] = node

            first_unique = head.next
            if first_unique is tail:
                result_chars.append("#")
            else:
                result_chars.append(first_unique.character)

        return "".join(result_chars)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each arrival performs at most one append, one unlink, and one head read, all worst-case constant; unlike the queue, no work is deferred.

##### Space Complexity: `O(k)`

The list and the map hold one entry per distinct character, plus the output list.

#### Key Insights

- One position per character is enough: a character is a candidate only while its count is one, so duplicates can carry no information.
- Unlinking by stored node references removes the lazy-cleanup debt the queue carries: memory stays at the distinct-character count and each arrival costs a worst-case constant.
- Sentinels at both ends delete the empty-list and one-element edge cases from the code.

## Comparison of Solutions

### Time Complexity

- **Prefix Rescan with a Tally**: `O(n^2)` - a fresh count and scan of the whole prefix per arrival.
- **Queue with Frequency Table**: `O(n)` amortized - one enqueue and at most one dequeue per occurrence.
- **Unique List with Position Removal**: `O(n)` worst case - constant list work per arrival with nothing deferred.

### Space Complexity

- **Prefix Rescan with a Tally**: `O(n)` - the result list plus the prefix slice.
- **Queue with Frequency Table**: `O(n)` - the queue can pile up every occurrence behind a stale head.
- **Unique List with Position Removal**: `O(k)` - one node per distinct character, `k` the alphabet actually seen.

### Trade-offs

- **Prefix Rescan with a Tally**: trivial to write and obviously correct, but quadratic time rules it out at the `10^5` constraint.
- **Queue with Frequency Table**: the shortest linear solution and easy to explain, at the cost of input-sized memory and amortized (not worst-case) per-arrival bounds.
- **Unique List with Position Removal**: distinct-character memory and worst-case constant arrivals, at the cost of hand-managed list links.

### When to Use Each

- **Queue with Frequency Table (Recommended)**: the interview default: linear, a few lines, and the eviction rule is easy to state aloud.
- **Unique List with Position Removal**: when memory per arrival matters or the stream is long-lived, where input-sized queue occupancy is unacceptable.
- **Prefix Rescan with a Tally**: as the spoken baseline before improving it, or for tiny inputs.

### Optimization Notes

- The decisive observation: "earliest with count exactly one" changes only at arrivals of characters already present, so the answer structure needs distinct characters only.
- The queue version's cleanup is amortized because work is deferred; the list version pays immediately per arrival, which gives it the honest `O(1)` worst-case bound.
- A common pitfall is evicting a queue entry when it is appended rather than when its count passes one: counts change over time, so eviction decisions must be made lazily against the current tally.
- `defaultdict` reads return `0` for unseen characters, which is what lets the cleanup loop test `frequencies[candidates[0]]` without a membership check.
