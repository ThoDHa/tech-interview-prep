# [Feasible Indices After Prefix/Suffix Reduction](https://www.fastprep.io/problems/amazon-feasible-indices-after-prefix-suffix-reduction)

**Medium** | **NN minutes** | **Array, Greedy**

Note: This problem is a duplicate of Feasible Indices After Reduction. The sighting dates have been merged into that version.

You are given an integer array arr of size n, where all elements are distinct.

You can perform the following operations any number of times:

Choose a non-empty prefix of the array and delete all elements except the minimum element of that prefix.Choose a non-empty suffix of the array and delete all elements except the maximum element of that suffix.After each operation, the remaining elements are concatenated to form a new array.

An index i is called feasible if it is possible to reduce the array to a single element [arr[i]] using the above operations.

Return a binary string of length n where:

1 means the index is feasible.0 means the index is not feasible.

## Examples

### Example 1

**Input:** `arr = [1, 3, 2, 5, 4]`

**Output:** `"10011"`

## Constraints

- `1 <= n <= 2 * 10^5`
- `1 <= arr[i] <= 10^6`
- `All elements are distinct.`

## Solutions

Each operation erases one stretch of the array and keeps exactly one
representative from it, so a surviving element's value depends only on which
stretches it can come to represent, never on bookkeeping between operations.
Every approach below searches the space of reachable sequences; the last one
proves that space collapses to two per-index checks.

### Recursive Deletion Enumeration

#### Derivation

The most literal reading: starting from `arr`, repeatedly try every prefix
operation and every suffix operation, and record which singleton sequences
ever appear. Each operation is one choice of boundary, so a depth-first walk
that branches on every cut covers all reachable sequences:

1. Hold sequences as tuples so they can be members of `seen_sequences`, seeded
   with the full array, and `survivor_values`, the set of singleton values
   reached.
2. `expand(state)` returns immediately when `len(state) == 1`, adding
   `state[0]` to `survivor_values`.
3. Otherwise every cut `1..len(state)` defines a prefix operation: the new head
   is `min(state[:cut])` and the tail `state[cut:]` survives unchanged. Each
   result not seen before is recorded and expanded recursively.
4. Every cut `0..len(state) - 1` defines a suffix operation: the tail collapses
   to `max(state[cut:])`. New results are recorded and expanded the same way.
5. An index is feasible when `arr[position]` sits in `survivor_values`; build
   the answer string from that membership test.

#### Walkthrough

Example 1 has five elements, so the first expansion already branches ten ways;
to keep the trace readable we use the smaller tailored input
`arr = [5, 1, 7]`. The root expands into every one-operation result, and cuts
of length 1 reproduce the same sequence, which `seen_sequences` filters:

```text
(5, 1, 7)  root
  prefix cut 2: min(5, 1) = 1    -> (1, 7)
  prefix cut 3: min(5, 1, 7) = 1 -> (1,)
  suffix cut 0: max(5, 1, 7) = 7 -> (5, 7)
  suffix cut 1: max(1, 7) = 7    -> (5, 7)   duplicate, skipped

(1, 7)
  prefix cut 2: min(1, 7) = 1    -> (1,)
  suffix cut 0: max(1, 7) = 7    -> (7,)
(1,)  survivor value 1

(5, 7)
  prefix cut 2: min(5, 7) = 5    -> (5,)
  suffix cut 0: max(5, 7) = 7    -> (7,)     duplicate, skipped
(5,)  survivor value 5              (7,)  survivor value 7
```

All three values surface as singletons, so the answer is `"111"`: 1 rides a
prefix minimum all the way down, 7 a suffix maximum, and 5 survives by first
absorbing 1 into a prefix (leaving `(5, 7)`) and then absorbing 7 the same way.
(For Example 1, the same search reaches `(1,)`, `(5,)`, and `(4,)` but never
`(2,)` or `(3,)`, producing `"10011"`.)

#### Solution

```python
from typing import List, Tuple


class Solution:
    def solve(self, arr: List[int]) -> str:
        """Return the feasibility bit string over the original indices.

        Time:  O(S × n^2), where S is the number of distinct reachable
            sequences: each is expanded once, trying O(n) cuts that each
            cost O(n) to build and hash.
        Space: O(S × n) for the visited sequences and the recursion stack.
        """
        start_sequence = tuple(arr)
        seen_sequences = {start_sequence}
        survivor_values = set()

        def expand(state: Tuple[int, ...]) -> None:
            if len(state) == 1:
                survivor_values.add(state[0])
                return
            for cut in range(1, len(state) + 1):
                reduced = (min(state[:cut]),) + state[cut:]
                if reduced not in seen_sequences:
                    seen_sequences.add(reduced)
                    expand(reduced)
            for cut in range(len(state)):
                reduced = state[:cut] + (max(state[cut:]),)
                if reduced not in seen_sequences:
                    seen_sequences.add(reduced)
                    expand(reduced)

        expand(start_sequence)
        return "".join(
            "1" if arr[position] in survivor_values else "0"
            for position in range(len(arr))
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(S × n^2)`

Where `S` is the number of distinct reachable sequences: each is expanded
once, each expansion tries `O(n)` cuts, and building and hashing one reduced
sequence costs `O(n)`.

##### Space Complexity: `O(S × n)`

The visited set stores up to `S` sequences of length up to `n`, and the
recursion stack adds one frame per level, at most `n`.

#### Key Insights

- Tuples are the state format because lists cannot enter a set; hashing the
  whole sequence is what makes revisits cheap to reject.
- The cut of length 1 is a legal operation whose result equals its input, so
  the visited set is load-bearing for termination even before duplicates
  collide.
- Exponential in the worst case, this search is unusable at the constraint
  limit of `2 * 10^5` elements, but it defines exactly what feasible means,
  which the faster approaches must respect.

### Reachable States Search

#### Derivation

The recursion above carries one risk the search itself does not need: a chain
of reductions one operation long adds one call frame, so the stack can grow to
`n` frames. Converting the traversal to an explicit queue changes only the
exploration order, and the level structure that order produces is worth
having: every state first reached at depth `d` needs exactly `d` operations,
which makes the trace of reachable sequences readable layer by layer:

1. Seed `queue` with the full sequence and `seen_states` with it as well.
2. Dequeue `state`; a singleton joins `survivor_values` and nothing else
   happens.
3. Otherwise enqueue every unseen prefix reduction `(min(state[:cut]),) +
   state[cut:]` and every unseen suffix reduction
   `state[:cut] + (max(state[cut:]),)`, marking each on enqueue.
4. When the queue empties, translate `survivor_values` into the bit string by
   membership of each `arr[position]`.

#### Walkthrough

Example 1, `arr = [1, 3, 2, 5, 4]`, expands to 11 distinct states over three
levels; each line shows the state dequeued and the new states it enqueues:

```text
level 0
  (1,3,2,5,4) -> (1,2,5,4), (1,5,4), (1,4), (1,), (5,), (1,5), (1,3,5), (1,3,2,5)
level 1
  (1,2,5,4)   -> (1,2,5)
  (1,5,4)     -> nothing new
  (1,4)       -> (4,)
  (1,)        survivor value 1
  (5,)        survivor value 5
  (1,5)       -> nothing new
  (1,3,5)     -> nothing new
  (1,3,2,5)   -> nothing new
level 2
  (1,2,5)     -> nothing new
  (4,)        survivor value 4
  queue empty
```

The singletons reached are values 1, 5, and 4; sequences containing 2 or 3
always also contain something smaller (as a prefix neighbor) or larger (as a
suffix neighbor), so neither can ever be the representative of a collapse.
Mapping values back to positions gives `1` at index 0, `0` at indices 1 and 2,
`1` at indices 3 and 4: the expected Output `"10011"`.

#### Solution

The code is the level sweep from the walkthrough, with the visited set
guarding every enqueue.

```python
from collections import deque
from typing import List, Tuple


class Solution:
    def solve(self, arr: List[int]) -> str:
        """Return the feasibility bit string over the original indices.

        Time:  O(S × n^2), where S is the number of distinct reachable
            sequences: each is dequeued once, trying O(n) cuts that each
            cost O(n) to build and hash.
        Space: O(S × n) for the visited set and the queue.
        """
        start_state = tuple(arr)
        seen_states = {start_state}
        queue = deque([start_state])
        survivor_values = set()
        while queue:
            state = queue.popleft()
            if len(state) == 1:
                survivor_values.add(state[0])
                continue
            for cut in range(1, len(state) + 1):
                reduced = (min(state[:cut]),) + state[cut:]
                if reduced not in seen_states:
                    seen_states.add(reduced)
                    queue.append(reduced)
            for cut in range(len(state)):
                reduced = state[:cut] + (max(state[cut:]),)
                if reduced not in seen_states:
                    seen_states.add(reduced)
                    queue.append(reduced)
        return "".join(
            "1" if arr[position] in survivor_values else "0"
            for position in range(len(arr))
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(S × n^2)`

Same expansion accounting as the recursion: `S` reachable sequences, `O(n)`
cuts each, `O(n)` per reduced sequence built and hashed.

##### Space Complexity: `O(S × n)`

The visited set dominates; the queue holds at most one level of it.

#### Key Insights

- The queue only relocates the to-do list out of the call stack; the state
  space, the visited discipline, and the answer are identical to the recursive
  version.
- Levels are the bonus of breadth-first order: a singleton first seen at level
  `d` certifies exactly `d` operations suffice for its index.
- The search is still exponential in `S`, so it inherits the same ceiling as
  the recursion; its value is the readable state space the optimal approach
  must then be checked against.

### Prefix Minima and Suffix Maxima Scan

#### Derivation

The searches never explain why the state space stays small: something about
the two operations makes most sequences unreachable. The key is what one
operation does to a survivor's value. A prefix operation keeps, from the
deleted stretch, the minimum of a stretch that starts at index 0; a suffix
operation keeps the maximum of a stretch that ends at index `n - 1`. Working
backward, the final survivor `arr[position]` must therefore be, at the moment
of its last operation, either the minimum of a stretch starting at index 0 or
the maximum of a stretch ending at index `n - 1`, and by induction every
operation in its history preserves that shape. So `arr[position]` is feasible
exactly when it equals the minimum of some prefix of `arr` or the maximum of
some suffix, and the tightest tests are the full ones: `prefix_minima[position]
== arr[position]` (it is the smallest value seen from the left up to it) or
`suffix_maxima[position] == arr[position]` (the largest seen from it to the
right). Conversely, when both tests fail, some earlier index holds a smaller
value and some later index a larger one, and every deletion sequence leaves
one of them standing beside or after it, so no last operation can ever expose
`arr[position]` alone. (All elements are distinct, so "equals the running
extreme" is unambiguous.)

Both arrays build in one sweep each, and the bit string follows:

1. Sweep left to right over `arr`, filling `prefix_minima` with the running
   minimum.
2. Sweep right to left, filling `suffix_maxima` with the running maximum.
3. Emit `"1"` at each position passing either test, `"0"` otherwise, and
   return the joined string.

#### Walkthrough

Example 1, `arr = [1, 3, 2, 5, 4]`. The two sweeps produce:

```text
position        0    1    2    3    4
arr             1    3    2    5    4
prefix_minima   1    1    1    1    1
suffix_maxima   5    5    5    5    4

position 0:  prefix_minima 1 == arr 1   -> feasible
position 1:  prefix 1 != 3, suffix 5 != 3 -> not feasible
position 2:  prefix 1 != 2, suffix 5 != 2 -> not feasible
position 3:  prefix 1 != 5, suffix 5 == 5 -> feasible
position 4:  prefix 1 != 4, suffix 4 == 4 -> feasible
```

Reading the two failed rows shows the obstruction directly: value 3 has a
smaller element (1) before it and a larger element (5) after it, so no prefix
can bequeath it a minimum and no suffix a maximum; the same pair of witnesses
blocks value 2. Joining the five verdicts yields `"10011"`, the expected
Output.

#### Solution

The code is the two sweeps and the per-position verdict from the walkthrough.

```python
from typing import List


class Solution:
    def solve(self, arr: List[int]) -> str:
        """Return the feasibility bit string over the original indices.

        Time:  O(n): two sweeps build the prefix minima and suffix maxima,
            and a final pass scores every index.
        Space: O(n) for the two auxiliary arrays and the output string.
        """
        size = len(arr)
        prefix_minima = [0] * size
        running_min = arr[0]
        for position in range(size):
            if arr[position] < running_min:
                running_min = arr[position]
            prefix_minima[position] = running_min

        suffix_maxima = [0] * size
        running_max = arr[size - 1]
        for position in range(size - 1, -1, -1):
            if arr[position] > running_max:
                running_max = arr[position]
            suffix_maxima[position] = running_max

        return "".join(
            "1"
            if prefix_minima[position] == arr[position]
            or suffix_maxima[position] == arr[position]
            else "0"
            for position in range(size)
        )
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two constant-work sweeps over the array plus one pass to emit the answer.

##### Space Complexity: `O(n)`

The two auxiliary arrays dominate; folding each sweep into the final pass
would reduce the auxiliary space to `O(1)` beyond the output.

#### Key Insights

- Working backward from the last operation converts "which sequences are
  reachable" into a property of single positions: prefix minimum from the
  left, suffix maximum to the right.
- The distinctness constraint is what makes the equality tests clean; with
  duplicates, ties would need tie-breaking rules spelled out per operation.
- An element with both a smaller predecessor and a larger successor is
  infeasible no matter how many operations are spent, which is why the answer
  tends to be sparse on random inputs.

## Comparison of Solutions

### Time Complexity

- **Recursive Deletion Enumeration**: `O(S × n^2)` - every reachable sequence
  expanded once with linear-time cut construction.
- **Reachable States Search**: `O(S × n^2)` - same expansion count, breadth-first
  order instead of depth-first.
- **Prefix Minima and Suffix Maxima Scan**: `O(n)` - two sweeps and a verdict
  pass.

### Space Complexity

- **Recursive Deletion Enumeration**: `O(S × n)` - visited sequences plus the
  recursion stack.
- **Reachable States Search**: `O(S × n)` - visited sequences, with the queue
  holding at most one level.
- **Prefix Minima and Suffix Maxima Scan**: `O(n)` - two auxiliary arrays plus
  the output.

### Trade-offs

- **Recursive Deletion Enumeration**: the shortest faithful transcription of
  the rules and a natural correctness oracle, but the recursion depth and the
  exponential state space cap it at small inputs.
- **Reachable States Search**: identical cost with no recursion-depth risk,
  and the level structure doubles as a proof aid, at the price of queue
  bookkeeping.
- **Prefix Minima and Suffix Maxima Scan**: linear time and the only approach
  that scales to `n = 2 * 10^5`, but its correctness rests on a backward
  argument that takes longer to state than the search it replaces.

### When to Use Each

- **Recursive Deletion Enumeration**: while prototyping or generating expected
  outputs for tiny arrays in tests.
- **Reachable States Search**: when an explicit, inspectable state space is
  wanted, or as a non-recursive refactor of the enumeration.
- **Prefix Minima and Suffix Maxima Scan**: always, in production and in the
  assessment itself; it is the intended solution.

### Optimization Notes

- The scan's two arrays can be folded into one pass each side of the verdict
  loop, cutting auxiliary space to `O(1)` beyond the output, with no change
  in asymptotics.
- The equivalence between "reachable singleton" and "prefix minimum or suffix
  maximum" is worth testing empirically: compare the scan against either
  search on small random arrays before trusting it.
- Distinctness is not incidental: with duplicates, `prefix_minima[position]
  == arr[position]` would need care over which equal element the operations
  actually keep.

