# [Maximum Frequency Stack](https://leetcode.com/problems/maximum-frequency-stack/)

**Hard** | **35 minutes** | **Hash Table, Stack, Design**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md)

**Algorithm:** [Hash table](https://en.wikipedia.org/wiki/Hash_table) · [Stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) · [Priority queue](https://en.wikipedia.org/wiki/Priority_queue)

**Practice:** [`practice/maximum_frequency_stack/solution.py`](../../practice/maximum_frequency_stack/solution.py)

Design a stack-like data structure to push elements to the stack and pop the most frequent element from the stack.

Implement the `FreqStack` class:

- `FreqStack()` constructs an empty frequency stack.
- `void push(int val)` pushes an integer `val` onto the top of the stack.
- `int pop()` removes and returns the most frequent element in the stack.
    - If there is a tie for the most frequent element, the element closest to the stack's top is removed and returned.

## Examples

### Example 1

**Input:**

```text
["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"]
[[], [5], [7], [5], [7], [4], [5], [], [], [], []]
```

**Output:**

```text
[null, null, null, null, null, null, null, 5, 7, 5, 4]
```

**Explanation:**

```text
FreqStack freqStack = new FreqStack();
freqStack.push(5); // The stack is [5]
freqStack.push(7); // The stack is [5,7]
freqStack.push(5); // The stack is [5,7,5]
freqStack.push(7); // The stack is [5,7,5,7]
freqStack.push(4); // The stack is [5,7,5,7,4]
freqStack.push(5); // The stack is [5,7,5,7,4,5]
freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,5,7,4].
freqStack.pop();   // return 7, as 5 and 7 is the most frequent, but 7 is closest to the top. The stack becomes [5,7,5,4].
freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,4].
freqStack.pop();   // return 4, as 4, 5 and 7 is the most frequent, but 4 is closest to the top. The stack becomes [5,7].
```

## Constraints

- `0 <= val <= 10^9`
- At most `2 * 10^4` calls will be made to `push` and `pop`.
- It is guaranteed that there will be at least one element in the stack before calling `pop`.

## Deriving the Solution

Every `pop` must return the element with the highest current frequency, breaking ties toward the most recent push. All three designs below keep a live frequency map; they differ in how they locate that winner.

1. **Start literal.** Store exactly what the problem describes: the stack as one
   list in push order, plus a `freq_count` map. To pop, compute the maximum frequency and scan the list from the top for the first element carrying it. Correct, but each pop pays a linear scan and a linear mid-list removal: see [Brute Force](#brute-force).
2. **Spot the waste.** The pop rebuilds from scratch information that only
   changes incrementally: the maximum frequency moves by at most one per operation, and "closest to the top among the winners" can be maintained rather than searched for.
3. **Group by frequency.** Give every frequency level its own stack: an
   element's `k`-th copy lives in bucket `k`. The winner is always the top of the `max_freq` bucket, LIFO order inside each bucket resolves the recency tie for free, and `max_freq` moves in single steps. Both operations drop to `O(1)`: see [Stack of Stacks](#stack-of-stacks).
4. **Or reach for a priority queue.** "Highest frequency, then most recent" is
   a priority order, so a heap keyed `(-frequency, -timestamp)` surfaces the winner directly, at `O(log n)` per operation and with `heapq` carrying the core logic: see [Heap with Timestamps](#heap-with-timestamps).

## Solutions

### Brute Force

#### Derivation

The most direct model keeps exactly what the problem statement talks about: the stack itself, as one list in push order, plus a live `freq_count` map from each value to its current frequency. `push` maintains both in constant time. `pop` answers its two requirements literally: first find the highest frequency, then find the element closest to the top that carries it, by scanning the list from the top down. The steps:

1. `push(val)`: append `val` to `stack` and increment `freq_count[val]`.
2. `pop()`: compute `max_freq = max(self.freq_count.values())`.
3. Scan `stack` from the last index toward `0`; the first `val` whose
   `freq_count[val]` equals `max_freq` is the winner. Remove it with `stack.pop(i)`, decrement its count (deleting the entry when it reaches zero), and return it.

Scanning from the top is what enforces the tie-break: among all elements at the maximum frequency, the first one met is the one closest to the top.

#### Walkthrough

Let us run the **Brute Force** code on Example 1: push `5, 7, 5, 7, 4, 5`, then call `pop()` four times. Each `push` appends to `stack` and bumps that value's count in `freq_count`.

| Operation | `stack` after | `freq_count` after |
| --- | --- | --- |
| `push(5)` | `[5]` | `{5: 1}` |
| `push(7)` | `[5, 7]` | `{5: 1, 7: 1}` |
| `push(5)` | `[5, 7, 5]` | `{5: 2, 7: 1}` |
| `push(7)` | `[5, 7, 5, 7]` | `{5: 2, 7: 2}` |
| `push(4)` | `[5, 7, 5, 7, 4]` | `{5: 2, 7: 2, 4: 1}` |
| `push(5)` | `[5, 7, 5, 7, 4, 5]` | `{5: 3, 7: 2, 4: 1}` |

Now the pops. Each `pop()` first computes `max_freq = max(freq_count.values())`, then scans `stack` from the top down (`i` from the last index toward `0`) and removes the first value whose count equals `max_freq`:

- `pop()`: `max_freq` is `3`. Scanning from the top, the last `5` (index `5`) has count `3`, so it is removed and its count drops. `stack` becomes `[5, 7, 5, 7, 4]`, `freq_count` becomes `{5: 2, 7: 2, 4: 1}`. Returns `5`.
- `pop()`: `max_freq` is `2`. Scanning from the top, `4` (count `1`) is skipped, then `7` (count `2`) matches and is removed. `stack` becomes `[5, 7, 5, 4]`, `freq_count` becomes `{5: 2, 7: 1, 4: 1}`. Returns `7`: the tie between `5` and `7` resolves to `7` because it sits closer to the top.
- `pop()`: `max_freq` is `2`. Scanning from the top, `4` (count `1`) is skipped, then `5` (count `2`) matches and is removed. `stack` becomes `[5, 7, 4]`, `freq_count` becomes `{5: 1, 7: 1, 4: 1}`. Returns `5`.
- `pop()`: `max_freq` is `1`. The top element `4` (count `1`) matches immediately and is removed. `stack` becomes `[5, 7]`, `freq_count` becomes `{5: 1, 7: 1}`. Returns `4`.

The four pops return `5, 7, 5, 4`, which matches the expected Output `[null, null, null, null, null, null, null, 5, 7, 5, 4]` for the pop calls.

#### Solution

The code is the walkthrough's two structures and its top-down scan written down.

```python
class FreqStack:
    def __init__(self):
        """
        Brute force approach maintaining complete element history
        """
        self.stack = []  # Complete stack history
        self.freq_count = {}  # Current frequency of each element

    def push(self, val: int) -> None:
        """
        Add to stack and update frequency
        """
        self.stack.append(val)
        self.freq_count[val] = self.freq_count.get(val, 0) + 1

    def pop(self) -> int:
        """
        Find and remove most frequent element (most recent if tie)
        """
        if not self.stack:
            return -1

        # Find maximum frequency
        max_freq = max(self.freq_count.values())

        # Find the most recent element with maximum frequency
        for i in range(len(self.stack) - 1, -1, -1):
            val = self.stack[i]
            if self.freq_count[val] == max_freq:
                # Remove element from stack and update frequency
                self.stack.pop(i)
                self.freq_count[val] -= 1
                if self.freq_count[val] == 0:
                    del self.freq_count[val]
                return val

        return -1  # Should never reach here
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` for push, `O(n)` for pop

Push is constant time, but pop requires scanning the entire stack to find the target element.

##### Space Complexity: `O(n)`

Maintains the complete element history in the stack.

#### Key Insights

- Keeping the literal push order in one list and a live frequency map is the most direct model: you can answer "most frequent, most recent" by reading both directly.
- The recency tie-break falls out of scanning the stack from the top down and stopping at the first element whose frequency equals the maximum.
- `pop(i)` from the middle of a Python list is `O(n)`, and `max(self.freq_count.values())` re-scans every distinct value, so each pop is linear; this is the cost the later designs eliminate.
- Correct for every valid sequence, but too slow at the upper constraint of `2 * 10^4` calls.

### Stack of Stacks

#### Derivation

The Brute Force pop searches for two things it could have maintained: the maximum frequency, and the most recent element carrying it. The repair is to organize elements by the very property the pop keys on. Give each frequency level its own [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)): when a value's count climbs to `k`, that occurrence is appended to bucket `k`. The most frequent element is then always on top of the highest non-empty bucket, and because each bucket is itself a stack, elements with the same frequency come off most-recent-first, which is exactly the required tie-break.

The remaining question is how `max_freq` moves. A push raises it by at most one (a value's count climbs one step at a time). On a pop that empties the top bucket, a single decrement suffices: an element only reaches count `k` after leaving an entry in every bucket from `1` to `k - 1`, so a non-empty `freq_stacks[k]` guarantees a non-empty `freq_stacks[k-1]`. The Invariant below states the property formally and shows that both `push` and `pop` preserve it. The steps:

1. `push(val)`: increment `freq_count[val]` to obtain `freq`, raise `max_freq`
   if `freq` exceeds it, and append `val` to `freq_stacks[freq]` (creating the bucket on first use).
2. `pop()`: pop `val` from `freq_stacks[max_freq]`, decrement
   `freq_count[val]`, and if that bucket is now empty, decrement `max_freq`.
3. Return `val`.

#### Invariant

Write \(F_k\) for `freq_stacks[k]`, the bucket holding one entry for every element whose count has reached \(k\). Two properties hold after every `push` and every `pop`:

$$ \text{(1)}\quad \text{the entries of } \textit{val} \text{ occupy exactly } F_1, F_2, \ldots, F_{\textit{freq\_count}[\textit{val}]} $$

$$ \text{(2)}\quad F_k \ne \varnothing \ \Longrightarrow\ F_{k-1} \ne \varnothing \qquad (2 \le k \le \textit{max\_freq}) $$

```text
(1) the entries of val occupy exactly freq_stacks[1], freq_stacks[2], ...,
    freq_stacks[freq_count[val]]
(2) freq_stacks[k] non-empty implies freq_stacks[k - 1] non-empty,
    for 2 <= k <= max_freq
```

`push` maintains (1) directly: an element climbs its counter one step at a time, and each increment appends it to the bucket named by its *new* count, so arriving in \(F_k\) means it already left an entry in every bucket below. Property (2) follows from (1): anything sitting in \(F_k\) also sits in \(F_{k-1}\), so a non-empty bucket can never have an empty bucket beneath it. Pushing only adds entries, and `max_freq` rises to \(k\) only on the push that fills \(F_k\), so both properties survive.

`pop` preserves them too. It removes one entry of `val` from \(F_{\textit{max\_freq}}\), which by (1) and (2) is the topmost bucket `val` occupies, and decrements `freq_count[val]` to match. No other bucket is touched, so the only way (2) could break is through the change to `max_freq` itself.

That is where the payoff lands. The bare `self.max_freq -= 1` reads like it ought to be a downward scan for the next non-empty bucket, and (2) is precisely what makes the scan unnecessary: when \(F_{\textit{max\_freq}}\) empties, \(F_{\textit{max\_freq}-1}\) is guaranteed non-empty, or else `max_freq` drops to `0` and the structure is empty. A single decrement cannot skip past an empty bucket, so on entry to the next `pop`, `max_freq` still names the true maximum frequency and `freq_stacks[max_freq]` is non-empty.

#### Walkthrough

Let us run Example 1 through the buckets: push `5, 7, 5, 7, 4, 5`, then call `pop()` four times. Each line shows the full internal state after the call:

```text
op          freq_count       freq_stacks                    max_freq
push(5)     {5:1}            {1:[5]}                        1
push(7)     {5:1,7:1}        {1:[5,7]}                      1
push(5)     {5:2,7:1}        {1:[5,7], 2:[5]}               2
push(7)     {5:2,7:2}        {1:[5,7], 2:[5,7]}             2
push(4)     {5:2,7:2,4:1}    {1:[5,7,4], 2:[5,7]}           2
push(5)     {5:3,7:2,4:1}    {1:[5,7,4], 2:[5,7], 3:[5]}    3
pop() -> 5  {5:2,7:2,4:1}    {1:[5,7,4], 2:[5,7], 3:[]}     2
pop() -> 7  {5:2,7:1,4:1}    {1:[5,7,4], 2:[5], 3:[]}       2
pop() -> 5  {5:1,7:1,4:1}    {1:[5,7,4], 2:[], 3:[]}        1
pop() -> 4  {5:1,7:1,4:0}    {1:[5,7], 2:[], 3:[]}          1
```

Each push files the value under its *new* count: the second `5` lands in bucket `2`, the third in bucket `3`, raising `max_freq` step by step. The first pop takes the top of bucket `3`, the lone third copy of `5`; the bucket empties, so `max_freq` drops to `2`. The second pop reads bucket `2`, whose top is `7` because `7`'s second copy was pushed after `5`'s: the LIFO order inside the bucket delivers the recency tie-break with no timestamps. The third pop takes `5` from bucket `2` and empties it (`max_freq` drops to `1`), and the fourth takes the top of bucket `1`, which is `4`.

The four pops return `5, 7, 5, 4`, matching the expected Output `[null, null, null, null, null, null, null, 5, 7, 5, 4]` for the pop calls.

#### Solution

The code is the bucket update from the walkthrough: one count map, one dictionary of per-frequency stacks, and the `max_freq` marker.

```python
class FreqStack:
    def __init__(self):
        """
        Stack of stacks approach - group elements by frequency level
        """
        self.freq_count = {}  # val -> frequency count
        self.freq_stacks = {}  # frequency -> stack of elements with that frequency
        self.max_freq = 0     # track maximum frequency seen

    def push(self, val: int) -> None:
        """
        Push element and update frequency tracking
        """
        # Update frequency count
        self.freq_count[val] = self.freq_count.get(val, 0) + 1
        freq = self.freq_count[val]

        # Update maximum frequency
        self.max_freq = max(self.max_freq, freq)

        # Add to appropriate frequency stack
        if freq not in self.freq_stacks:
            self.freq_stacks[freq] = []
        self.freq_stacks[freq].append(val)

    def pop(self) -> int:
        """
        Pop the most frequent element (most recent if tie)
        """
        # Get element from highest frequency stack
        val = self.freq_stacks[self.max_freq].pop()

        # Decrease frequency count
        self.freq_count[val] -= 1

        # Update max_freq if highest frequency stack becomes empty
        if not self.freq_stacks[self.max_freq]:
            self.max_freq -= 1

        return val
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` for both push and pop operations

All operations involve simple hash map lookups and stack operations, which are constant time.

##### Space Complexity: `O(n)`

Where n is the total number of elements pushed. Each element appears in exactly one frequency stack at any time.

#### Key Insights

- Grouping elements by their current frequency turns "find the most frequent" into "look at the highest non-empty bucket", a constant-time lookup.
- The LIFO order within each frequency bucket encodes recency for free, so ties resolve to the element closest to the top without any timestamps.
- Tracking `max_freq` and decrementing it when its bucket empties is the only bookkeeping needed; the next-lower bucket is always non-empty when this happens.
- This is the optimal from-scratch design: no library handles the priority logic.

### Heap with Timestamps

#### Derivation

Instead of designing a bespoke structure, ask whether a standard one already answers "give me the item of highest priority". A [priority queue](https://en.wikipedia.org/wiki/Priority_queue) does, provided the priority is spelled out: highest frequency first, and among equal frequencies, the most recent push. Encode both in one key by recording, at push time, the frequency the element has *at that moment* alongside a global timestamp. Python's `heapq` is a min-heap, so negating both fields makes the smallest tuple the intended winner. Because each entry snapshots its frequency, the element currently at the highest count always owns the heap's best entry; no stale entry can outrank it. The steps:

1. On `push(val)`, increment the global `timestamp` and `freq_count[val]`, then
   push the tuple `(-self.freq_count[val], -self.timestamp, val)` onto `max_heap`.
2. On `pop()`, `heappop` the top tuple; its `val` is the element with the
   highest current frequency, ties broken toward the later timestamp.
3. Decrement the popped element's `freq_count` so future pushes record accurate
   frequencies.

#### Walkthrough

Let us run Example 1 through the heap: push `5, 7, 5, 7, 4, 5`, then call `pop()` four times. Each push adds one `(-freq, -timestamp, val)` entry. The lines below list the live entries in priority order, best (smallest tuple) first, rather than the heap's internal array layout:

```text
push(5)  ts=1  entry (-1,-1,5)  heap: (-1,-1,5)
push(7)  ts=2  entry (-1,-2,7)  heap: (-1,-2,7) (-1,-1,5)
push(5)  ts=3  entry (-2,-3,5)  heap: (-2,-3,5) (-1,-2,7) (-1,-1,5)
push(7)  ts=4  entry (-2,-4,7)  heap: (-2,-4,7) (-2,-3,5) (-1,-2,7) (-1,-1,5)
push(4)  ts=5  entry (-1,-5,4)  heap: (-2,-4,7) (-2,-3,5) (-1,-5,4) (-1,-2,7) (-1,-1,5)
push(5)  ts=6  entry (-3,-6,5)  heap: (-3,-6,5) (-2,-4,7) (-2,-3,5) (-1,-5,4) (-1,-2,7) (-1,-1,5)
```

Now the pops, each removing the heap's smallest tuple:

```text
pop() -> 5   removes (-3,-6,5)   heap: (-2,-4,7) (-2,-3,5) (-1,-5,4) (-1,-2,7) (-1,-1,5)
pop() -> 7   removes (-2,-4,7)   heap: (-2,-3,5) (-1,-5,4) (-1,-2,7) (-1,-1,5)
pop() -> 5   removes (-2,-3,5)   heap: (-1,-5,4) (-1,-2,7) (-1,-1,5)
pop() -> 4   removes (-1,-5,4)   heap: (-1,-2,7) (-1,-1,5)
```

The first pop takes `(-3,-6,5)`, the only frequency-3 entry. The second is the tie the problem cares about: `(-2,-4,7)` beats `(-2,-3,5)` because `-4 < -3`, so equal frequency `2` resolves to the later timestamp, which is `7`. The third pop takes the remaining frequency-2 entry for `5`, and the fourth compares three frequency-1 entries, where the latest timestamp (`ts=5`) belongs to `4`.

The four pops return `5, 7, 5, 4`, matching the expected Output `[null, null, null, null, null, null, null, 5, 7, 5, 4]` for the pop calls.

#### Solution

The code is the walkthrough's entry bookkeeping handed to `heapq`.

```python
import heapq
from collections import defaultdict

class FreqStack:
    def __init__(self):
        """
        Priority queue approach with timestamp-based tie breaking
        """
        self.freq_count = defaultdict(int)  # val -> frequency
        self.max_heap = []  # (-frequency, -timestamp, val)
        self.timestamp = 0  # global timestamp counter

    def push(self, val: int) -> None:
        """
        Push element with frequency and timestamp tracking
        """
        self.timestamp += 1
        self.freq_count[val] += 1

        # Push to max heap (use negative values for max heap behavior)
        heapq.heappush(self.max_heap,
                      (-self.freq_count[val], -self.timestamp, val))

    def pop(self) -> int:
        """
        Pop element with highest frequency (most recent timestamp if tie)
        """
        neg_freq, neg_timestamp, val = heapq.heappop(self.max_heap)
        self.freq_count[val] -= 1
        return val
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)` for both operations

Each push and pop is a single heap operation over up to `n` entries, so both cost `O(log n)`.

##### Space Complexity: `O(n)`

The heap holds one entry per element currently in the stack: each push adds one entry and each pop removes one, so the size is linear in the number of live elements.

#### Key Insights

- A heap reframes the problem as a generic priority queue, which is easy to reach for but lets the library carry the core logic.
- Encoding the snapshot frequency at push time means the top entry is never stale, so no lazy deletion is required.
- The `(-freq, -timestamp)` key is the trick: it layers the recency tie-break underneath the frequency priority in one comparison.
- It is asymptotically slower than the stack-of-stacks design and depends on `heapq`, so it ranks below the from-scratch solutions.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(1)` push, `O(n)` pop - scanning the stack and re-scanning the frequency map on every pop.
- **Stack of Stacks**: `O(1)` for both operations - hash map lookups and per-frequency stack pushes/pops.
- **Heap with Timestamps**: `O(log n)` for both operations - a single heap push or pop over up to `n` entries.

### Space Complexity

- **Brute Force**: `O(n)` - complete stack history plus a frequency map.
- **Stack of Stacks**: `O(n)` - each element stored once across the per-frequency stacks.
- **Heap with Timestamps**: `O(n)` - one heap entry per element currently in the stack; each pop removes one.

### Trade-offs

- **Brute Force**: Linear pop and a re-scanned frequency map, but the most direct mental model and no library reliance. Suitable as a from-scratch baseline for understanding the problem.
- **Stack of Stacks**: Optimal `O(1)` operations with one stored copy per element, built entirely from hash maps and lists. Slightly more bookkeeping than the brute force, but the cleanest fast design.
- **Heap with Timestamps**: Easy to reach for if you already think in priority queues, but it hands the core priority logic to `heapq` and runs in `O(log n)` where the stack-of-stacks design is `O(1)`.

### When to Use Each

- **Brute Force**: When establishing correctness first, or for very small inputs where the linear pop is irrelevant.
- **Stack of Stacks**: The recommended default - optimal performance with a clean, library-free design.
- **Heap with Timestamps**: When a priority-queue framing is clearer to communicate, accepting the slower bound and the `heapq` dependency.

### Optimization Notes

- The **Stack of Stacks** solution is the recommended approach: it achieves `O(1)` time for both push and pop by grouping elements into a separate stack per frequency level.
- The key implementation detail is tracking `max_freq` and pushing each element onto the stack keyed by its new frequency. Popping from the `max_freq` stack naturally returns the most frequent element, and LIFO ordering within that stack handles the recency tie-breaking automatically.
- A common pitfall is mishandling `max_freq` after a pop: when the highest-frequency stack becomes empty, `max_freq` must be decremented so the next pop targets the correct level.
- The **Heap with Timestamps** design works because each push records the frequency the element had at that instant, so the heap's top entry is always the live winner and no lazy deletion of stale entries is required.
- This problem demonstrates the "group by property" design pattern. Such frequency-based priority systems appear in caching algorithms, load balancing, and resource allocation.
