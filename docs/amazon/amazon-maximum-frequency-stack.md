# [Maximum Frequency Stack](https://www.fastprep.io/problems/amazon-maximum-frequency-stack)

**Hard** | **NN minutes** | **Hash Table, Stack, Design**

Design a stack-like data structure that supports push and pop.

push(x) adds x to the structure.pop() removes and returns the value with the highest current frequency. If several values have the same highest frequency, return the one pushed most recently among them.Process the operations in order and return the values produced by the pop operations.

## Examples

### Example 1

**Input:** `operations = ["push","push","push","push","push","push","pop","pop","pop","pop"]`, `values = [5,7,5,7,4,5,0,0,0,0]`

**Output:** `[5,7,5,4]`

**Explanation:** The first pop returns 5 because it has frequency 3. The next two pops break frequency ties by recency, and the final pop returns 4.

### Example 2

**Input:** `operations = ["push","push","pop","pop"]`, `values = [1,2,0,0]`

**Output:** `[2,1]`

**Explanation:** Both values have frequency 1, so the more recently pushed value 2 is removed first.

## Constraints

- `1 <= operations.length <= 2 * 10^4`
- `values.length == operations.length`
- `Each operation is either push or pop.`
- `0 <= values[i] <= 10^9 for a push operation.`
- `Every pop operation is issued when the structure is nonempty.`
- `The value paired with a pop operation is ignored.`

## Solutions

Each solution below wraps a frequency-stack design in the same batch driver: build the structure, replay `operations` (the value paired with a `pop` is ignored), and collect what the pops return.

### Brute Force

#### Derivation

The most literal model keeps exactly what the statement describes: the push history as one list `stack`, plus a live `freq_count` map from value to current frequency. `push` appends and increments. `pop` then answers its two requirements by searching: the highest frequency is a `max` over the map, and the most recent element carrying it is the first match in a scan of `stack` from the top down. The steps:

1. `push(val)`: append `val` to `stack` and increment `freq_count[val]`.
2. `pop()`: compute `max_freq = max(freq_count.values())`.
3. Scan `stack` from the last position toward `0`; the first value whose
   `freq_count` equals `max_freq` is the winner. Remove it, decrement its
   count (deleting the entry at zero), and return it.

Scanning from the top is what enforces the tie-break: among all values at the maximum frequency, the first one met is the most recently pushed.

#### Walkthrough

Example 1 pushes `5, 7, 5, 7, 4, 5`, then pops four times. Each `push` appends to `stack` and bumps that value's count in `freq_count`:

| Operation | `stack` after | `freq_count` after |
| --- | --- | --- |
| `push(5)` | `[5]` | `{5: 1}` |
| `push(7)` | `[5, 7]` | `{5: 1, 7: 1}` |
| `push(5)` | `[5, 7, 5]` | `{5: 2, 7: 1}` |
| `push(7)` | `[5, 7, 5, 7]` | `{5: 2, 7: 2}` |
| `push(4)` | `[5, 7, 5, 7, 4]` | `{5: 2, 7: 2, 4: 1}` |
| `push(5)` | `[5, 7, 5, 7, 4, 5]` | `{5: 3, 7: 2, 4: 1}` |

Now the pops. Each computes `max_freq`, then scans from the top down and removes the first value whose count equals `max_freq`:

- `pop()`: `max_freq = 3`. The topmost `5` matches, is removed, its count drops
  to 2. Returns `5`.
- `pop()`: `max_freq = 2`. The scan skips `4` (count 1) and removes `7`
  (count 2). Returns `7`: the tie between `5` and `7` resolves to `7` because
  it sits closer to the top.
- `pop()`: `max_freq = 2`. The scan skips `4`, removes the remaining `5`
  (count 2). Returns `5`.
- `pop()`: `max_freq = 1`. The top element `4` matches immediately. Returns
  `4`.

The pops return `5, 7, 5, 4`, matching the expected Output.

#### Solution

The code is the walkthrough's two structures and its top-down scan written down.

```python
from typing import Dict, List


class FreqStack:
    def __init__(self) -> None:
        self.stack: List[int] = []
        self.freq_count: Dict[int, int] = {}

    def push(self, val: int) -> None:
        self.stack.append(val)
        self.freq_count[val] = self.freq_count.get(val, 0) + 1

    def pop(self) -> int:
        max_freq = max(self.freq_count.values())
        for position in range(len(self.stack) - 1, -1, -1):
            if self.freq_count[self.stack[position]] == max_freq:
                val = self.stack.pop(position)
                self.freq_count[val] -= 1
                if self.freq_count[val] == 0:
                    del self.freq_count[val]
                return val
        raise ValueError("pop called on an empty frequency stack")


class Solution:
    def processFrequencyStack(self, operations: List[str],
                              values: List[int]) -> List[int]:
        freq_stack = FreqStack()
        popped_values: List[int] = []
        for operation, value in zip(operations, values):
            if operation == "push":
                freq_stack.push(value)
            else:
                popped_values.append(freq_stack.pop())
        return popped_values
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` push, `O(n)` pop

Each pop re-scans the frequency map for the maximum and then walks up to the whole list, for `n` the number of live elements; a batch of `n` operations therefore costs `O(n^2)` in the worst case.

##### Space Complexity: `O(n)`

The push history plus one counter per distinct value.

#### Key Insights

- Keeping the literal push order plus a frequency map is the most direct model of the statement, and the recency tie-break falls out of a top-down scan.
- `list.pop(position)` from the middle is `O(n)`, and `max` over the map re-reads every distinct value, so each pop pays twice.
- Correct for every valid sequence but quadratic over the batch, which is the cost the later designs remove.

### Stack of Stacks

#### Derivation

The brute-force pop searches for two things it could have maintained: the maximum frequency, and the most recent element carrying it. The repair is to organize elements by the very property the pop keys on. Give each frequency level its own [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) bucket: when a value's count climbs to `k`, that occurrence is appended to bucket `k`. The winner is then always the top of bucket `max_freq`, and because each bucket is itself a stack, equal-frequency values come off most-recent-first, which is exactly the required tie-break. `max_freq` moves in single steps: a push raises it by at most one, and on a pop that empties the top bucket, one decrement suffices, because a value only reaches count `k` after leaving an entry in every bucket below `k`, so a non-empty bucket `k` always has non-empty buckets `1` through `k - 1` underneath. The steps:

1. `push(val)`: increment `freq_count[val]` to obtain `freq`, raise `max_freq`
   when `freq` exceeds it, and append `val` to the bucket named `freq`.
2. `pop()`: pop `val` from the `max_freq` bucket, decrement `freq_count[val]`,
   and when that bucket is now empty, decrement `max_freq`.
3. Return `val`.

#### Walkthrough

Example 1 through the buckets, one line per operation. Each push files the value under its new count:

```text
op          freq_count       freq_buckets                   max_freq
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

The first pop takes the top of bucket `3`, the lone third copy of `5`, and the emptied bucket drops `max_freq` to `2`. The second pop reads bucket `2`, whose top is `7` because `7`'s second copy was pushed after `5`'s: the LIFO order inside the bucket delivers the recency tie-break with no timestamps. The third pop empties bucket `2` (`max_freq` drops to `1`), and the fourth takes the top of bucket `1`, which is `4`. The pops return `5, 7, 5, 4`, matching the expected Output. Example 2 exercises the same tie rule in miniature: after `push(1)` and `push(2)`, bucket `1` is `[1, 2]`, so its top `2` pops first, then `1`.

#### Solution

The code is the bucket update from the walkthrough: one count map, one dictionary of per-frequency stacks, and the `max_freq` marker.

```python
from typing import Dict, List


class FreqStack:
    def __init__(self) -> None:
        self.freq_count: Dict[int, int] = {}
        self.freq_buckets: Dict[int, List[int]] = {}
        self.max_freq = 0

    def push(self, val: int) -> None:
        self.freq_count[val] = self.freq_count.get(val, 0) + 1
        freq = self.freq_count[val]
        if freq > self.max_freq:
            self.max_freq = freq
        self.freq_buckets.setdefault(freq, []).append(val)

    def pop(self) -> int:
        val = self.freq_buckets[self.max_freq].pop()
        self.freq_count[val] -= 1
        if not self.freq_buckets[self.max_freq]:
            self.max_freq -= 1
        return val


class Solution:
    def processFrequencyStack(self, operations: List[str],
                              values: List[int]) -> List[int]:
        freq_stack = FreqStack()
        popped_values: List[int] = []
        for operation, value in zip(operations, values):
            if operation == "push":
                freq_stack.push(value)
            else:
                popped_values.append(freq_stack.pop())
        return popped_values
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` per operation

Every push and pop touches one hash entry and one list end, so a batch of `n` operations runs in `O(n)`.

##### Space Complexity: `O(n)`

Each live element sits in exactly one bucket, plus one counter per distinct value.

#### Key Insights

- Grouping elements by their current frequency turns "find the most frequent" into "look at the top of bucket `max_freq`", a constant-time lookup.
- The LIFO order within each frequency bucket encodes recency for free, so ties resolve without timestamps.
- The single decrement of `max_freq` on an emptied bucket is safe because a value reaching count `k` has an entry in every lower bucket; the next-lower bucket can never be empty.
- This is the optimal from-scratch design: no library carries the priority logic.

### Heap with Timestamps

#### Derivation

Instead of designing a bespoke structure, ask whether a standard one already answers "give me the item of highest priority". A [priority queue](https://en.wikipedia.org/wiki/Priority_queue) does, provided the priority is spelled out: highest frequency first, and among equal frequencies the most recent push. Encode both in one key by recording, at push time, the frequency the element has at that moment alongside a global timestamp. Python's `heapq` is a min-heap, so negating both fields makes the smallest tuple the intended winner. Because each entry snapshots its frequency, the element currently at the highest count always owns the heap's best entry, so no stale entry can outrank it and no lazy deletion is needed. The steps:

1. On `push(val)`, increment the global `timestamp` and `freq_count[val]`, then
   push the tuple `(-freq_count[val], -timestamp, val)` onto `entry_heap`.
2. On `pop()`, `heappop` the top tuple and return its value.
3. Decrement `freq_count[val]` so future pushes record accurate frequencies.

#### Walkthrough

Example 1 through the heap. Each push adds one `(-freq, -timestamp, val)` entry; the lines below list the live entries in priority order, best first, rather than the heap's internal array layout:

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

The first pop takes the only frequency-3 entry. The second is the tie the problem cares about: `(-2,-4,7)` beats `(-2,-3,5)` because `-4 < -3`, so equal frequency `2` resolves to the later timestamp, which is `7`. The third takes the remaining frequency-2 entry for `5`, and the fourth compares three frequency-1 entries, where the latest timestamp (`ts=5`) belongs to `4`. The pops return `5, 7, 5, 4`, matching the expected Output.

#### Solution

The code is the walkthrough's entry bookkeeping handed to `heapq`.

```python
import heapq
from typing import Dict, List, Tuple


class FreqStack:
    def __init__(self) -> None:
        self.freq_count: Dict[int, int] = {}
        self.entry_heap: List[Tuple[int, int, int]] = []
        self.timestamp = 0

    def push(self, val: int) -> None:
        self.timestamp += 1
        self.freq_count[val] = self.freq_count.get(val, 0) + 1
        heapq.heappush(
            self.entry_heap,
            (-self.freq_count[val], -self.timestamp, val))

    def pop(self) -> int:
        val = heapq.heappop(self.entry_heap)[2]
        self.freq_count[val] -= 1
        return val


class Solution:
    def processFrequencyStack(self, operations: List[str],
                              values: List[int]) -> List[int]:
        freq_stack = FreqStack()
        popped_values: List[int] = []
        for operation, value in zip(operations, values):
            if operation == "push":
                freq_stack.push(value)
            else:
                popped_values.append(freq_stack.pop())
        return popped_values
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)` per operation

Each push and pop is a single heap operation over up to `n` live entries, so a batch of `n` operations runs in `O(n log n)`.

##### Space Complexity: `O(n)`

The heap holds exactly one entry per live element: each push adds one and each pop removes one.

#### Key Insights

- A heap reframes the problem as a generic priority queue, easy to reach for, but the library now carries the core priority logic.
- The `(-freq, -timestamp)` key layers the recency tie-break underneath the frequency priority in one comparison.
- Snapshotting the frequency at push time keeps the top entry live: a pop always removes the entry it consumed, so no lazy deletion is required.
- Asymptotically slower than the stack-of-stacks design, which achieves the same behavior in constant time.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(1)` push, `O(n)` pop - the pop re-scans the frequency map and walks the list, `O(n^2)` over a batch.
- **Stack of Stacks**: `O(1)` per operation - hash lookups plus list-end appends and pops, `O(n)` over a batch.
- **Heap with Timestamps**: `O(log n)` per operation - one heap push or pop over up to `n` entries, `O(n log n)` over a batch.

### Space Complexity

- **Brute Force**: `O(n)` - the full push history plus one counter per distinct value.
- **Stack of Stacks**: `O(n)` - each live element stored exactly once across the buckets.
- **Heap with Timestamps**: `O(n)` - one heap entry per live element.

### Trade-offs

- **Brute Force**: the most direct model and the easiest to argue correct, but quadratic over the batch.
- **Stack of Stacks**: optimal constant-time operations built from plain dicts and lists; slightly more bookkeeping (the `max_freq` marker and its decrement rule) than the brute force.
- **Heap with Timestamps**: reuses a standard structure and needs no bespoke invariant, but hands the priority logic to `heapq` and pays a logarithmic factor.

### When to Use Each

- **Brute Force**: to establish correctness first, or for tiny operation counts where the linear pop is irrelevant.
- **Stack of Stacks (Recommended)**: the interview answer: optimal, library-free, and the cleanest fast design.
- **Heap with Timestamps**: when a priority-queue framing is clearer to communicate and the logarithmic factor is acceptable.

### Optimization Notes

- The **Stack of Stacks** design is the recommended approach: file each element under its new frequency, pop from the `max_freq` bucket, and decrement `max_freq` only when that bucket empties.
- A common pitfall is mishandling `max_freq` after a pop: when the highest-frequency bucket empties, the single decrement is correct because lower buckets are guaranteed non-empty.
- The heap variant works because each entry snapshots the frequency at push time; if the key used the live count instead, stale entries would corrupt the ordering.
- The same group-by-frequency pattern reappears in caches (LFU eviction), schedulers, and rate limiters.
