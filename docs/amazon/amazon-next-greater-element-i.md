# [Next Greater Element I](https://www.fastprep.io/problems/amazon-next-greater-element-i)

**Easy** | **NN minutes** | **Stack, Hash Table**

You are given two arrays of distinct integers, query and reference, where every query value appears in reference.

For each query value, return the first greater value to its right in reference, or -1 when none exists.

## Examples

### Example 1

**Input:** `query = [4,1,2]`, `reference = [1,3,4,2]`

**Output:** `[-1,3,-1]`

**Explanation:** Four and two have no greater value to their right; one is followed by three.

### Example 2

**Input:** `query = [2,4]`, `reference = [1,2,3,4]`

**Output:** `[3,-1]`

**Explanation:** Three is the next greater value after two, while four has none.

## Constraints

- `1 <= query.length <= reference.length <= 10^5.`
- `All values in each array are distinct.`
- `Every value in query appears in reference.`

## Deriving the Solution

The answer to a query depends only on where the queried value sits in `reference`: everything to the left of that position is irrelevant, and the answer is the first strictly greater value to the right. So the work reduces to a per-position question over `reference`, and every approach below is a way of answering that question n times, for the n query values:

1. **Start literal.** For each query, find its position and scan right until a greater value appears. It is correct but rescans the same stretches of `reference` once per query: see [Brute Force Scan per Query](#brute-force-scan-per-query).
2. **Compute once, answer by lookup.** Every position's first greater value to the right can be computed once for the whole of `reference`, turning each query into a table read. A rightward scan per position is the naive way to fill that table: see [One-Time Greater Table](#one-time-greater-table).
3. **Fill the table in one pass.** A sweep with a stack of values still waiting for a greater neighbor resolves every position's answer in a single left-to-right pass: see [Monotonic Stack](#monotonic-stack).

## Solutions

### Brute Force Scan per Query

#### Derivation

The statement's literal reading: for each query value, look at `reference` and take the first strictly greater value to its right, or -1 when none exists. Locating the value is a linear scan (or one index lookup from a position map), and the answer search is a linear scan to the right:

1. Find `anchor = reference.index(value)` for the query `value`.
2. Scan `candidate` over `reference[anchor + 1:]`.
3. Return the first `candidate` with `candidate > value`.
4. Return -1 when the scan exhausts the tail.

Each query is independent, which is exactly why the approach repeats itself: neighboring queries pay for overlapping stretches of the same array.

#### Walkthrough

Example 2, `query = [2, 4]`, `reference = [1, 2, 3, 4]`:

```text
query 2   anchor = 1        tail = [3, 4]
          3 > 2             -> 3
query 4   anchor = 3        tail = []
          scan exhausted    -> -1
```

The answers assemble into `[3, -1]` in query order, matching the expected Output. The single query whose answer exists costs one scan of the whole remaining tail; the missing-answer query pays the full scan only to conclude there is nothing.

#### Solution

```python
from typing import List


class Solution:
    def nextGreaterElement(
        self, query: List[int], reference: List[int]
    ) -> List[int]:
        answers: List[int] = []
        for value in query:
            anchor = reference.index(value)
            found = -1
            for candidate in reference[anchor + 1:]:
                if candidate > value:
                    found = candidate
                    break
            answers.append(found)
        return answers
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * m)`

Each of the `n` queries pays `O(m)` to locate its value and up to another `O(m)` to scan the tail, with `m = reference.length`.

##### Space Complexity: `O(m)`

Each query slices `reference[anchor + 1:]`, a transient copy of the unscanned tail, so the auxiliary space beyond the output list is one tail copy at a time; only the loop's index and candidate live across iterations.

#### Key Insights

- The relation "first greater to the right" is a property of the value's position in `reference`; the query array only picks positions, it never changes the relation.
- A missing answer is the expensive case here: proving no greater value exists requires scanning the entire tail.
- The per-query independence is the waste. Nothing learned while answering one query survives to the next.

### One-Time Greater Table

#### Derivation

The Brute Force rescans `reference` for every query, but the scan it performs for a value depends only on that value's position, and the positions repeat across queries. Computing each position's first greater value once, into a map from value to answer, collapses every query to a lookup. The naive fill runs the same rightward scan as before, once per position of `reference`; the pass over queries then touches the map only:

1. Build `greater_map`, initially empty; values never chosen as some other
   value's answer stay absent, which the query pass reads as -1.
2. For each `anchor` position of `reference`, scan the tail for the first
   strictly greater value and record `greater_map[reference[anchor]]`.
3. Answer each query value with `greater_map.get(value, -1)`, in query order.

The table idea is the lasting step; its `O(m^2)` fill is what the next approach removes.

#### Walkthrough

Example 1, `reference = [1, 3, 4, 2]`, filling `greater_map` position by position:

```text
anchor 0 (1)   tail [3, 4, 2]    first greater: 3    greater_map[1] = 3
anchor 1 (3)   tail [4, 2]       first greater: 4    greater_map[3] = 4
anchor 2 (4)   tail [2]          none greater        (4 absent from map)
anchor 3 (2)   tail []           none greater        (2 absent from map)

query 4   greater_map.get(4, -1) -> -1
query 1   greater_map.get(1, -1) -> 3
query 2   greater_map.get(2, -1) -> -1
```

The lookups assemble into `[-1, 3, -1]` in query order, matching the expected Output. Note how the anchors for 4 and 2 paid a scan and recorded nothing: the map only stores answers that exist.

#### Solution

```python
from typing import Dict, List


class Solution:
    def nextGreaterElement(
        self, query: List[int], reference: List[int]
    ) -> List[int]:
        greater_map: Dict[int, int] = {}
        for anchor in range(len(reference)):
            value = reference[anchor]
            for candidate in reference[anchor + 1:]:
                if candidate > value:
                    greater_map[value] = candidate
                    break
        return [greater_map.get(value, -1) for value in query]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m^2 + n)`

The table fill scans a tail of up to `m` entries for each of `m` positions; each of the `n` queries is then one dictionary read. When several queries repeat values this beats the per-query scan, but the fill itself is quadratic.

##### Space Complexity: `O(m)`

`greater_map` holds at most one entry per reference value (only the ones with an answer), plus the output list.

#### Key Insights

- Splitting the work into a one-time computation and per-query lookups is the shape every efficient batch-query design takes; only the table's construction cost remains to attack.
- Leaving answered-absent values out of the map lets `get(value, -1)` express the -1 branch without a sentinel entry.
- The fill still re-scans entries a greater neighbor already resolved: position `anchor + 1`'s answer cannot help position `anchor`, although they overlap. That is the local structure a stack can exploit.

### Monotonic Stack

#### Derivation

The table fill is quadratic because each position re-reads a tail its neighbor just read. Watching what a fill actually learns: when a new value arrives and is greater than the value just before it, it answers that neighbor immediately, and any earlier waiting values smaller than it too, because the new value is the *first* greater value to reach them from the right. Keeping the unresolved values on a stack, newest first, makes each arrival pop and answer exactly the waiting values it is greater than, then join the stack itself. The stack stays strictly decreasing from bottom to top, which is why this is a [monotonic stack](https://en.wikipedia.org/wiki/Monotonic_stack). Each of the `m` values is pushed once and popped at most once, so the whole table fills in one linear pass:

1. Keep `waiting`, a list used as a stack, and `greater_map`, both empty.
2. For each `value` in `reference`, left to right: while `waiting` is non-empty
   and `waiting[-1] < value`, pop it and record
   `greater_map[popped] = value`.
3. Push `value` onto `waiting`.
4. After the sweep, answer each query with `greater_map.get(value, -1)`, in
   query order.

#### Walkthrough

Example 1, `reference = [1, 3, 4, 2]`, showing `waiting` after each step:

```text
value 1   nothing to pop        push 1            waiting = [1]
value 3   pop 1 (1 < 3)         map[1] = 3        waiting = [3]
value 4   pop 3 (3 < 4)         map[3] = 4        waiting = [4]
value 2   4 < 2 is false        push 2            waiting = [4, 2]

greater_map = {1: 3, 3: 4}

query 4   get(4, -1) -> -1
query 1   get(1, -1) -> 3
query 2   get(2, -1) -> -1
```

The values still on `waiting` at the end (4 and 2) are exactly the ones with no greater value to their right. The lookups assemble into `[-1, 3, -1]`, matching the expected Output.

#### Solution

The code is the walkthrough's sweep plus the query pass.

```python
from typing import Dict, List


class Solution:
    def nextGreaterElement(
        self, query: List[int], reference: List[int]
    ) -> List[int]:
        greater_map: Dict[int, int] = {}
        waiting: List[int] = []
        for value in reference:
            while waiting and waiting[-1] < value:
                greater_map[waiting.pop()] = value
            waiting.append(value)
        return [greater_map.get(value, -1) for value in query]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

The sweep pushes each of the `m` values once and pops each at most once, so the whole table fills in `O(m)`; the `n` queries are one dictionary read each.

##### Space Complexity: `O(m)`

`waiting` and `greater_map` each hold at most one entry per reference value, plus the output list.

#### Key Insights

- Each element's answer is decided by the first later arrival greater than it; a decreasing stack of unresolved elements turns that arrival into a batch of pops.
- Every value enters and leaves the stack at most once, which is what makes the two nested loops linear rather than quadratic.
- Values remaining on the stack after the sweep are precisely the -1 answers, so the map needs no entries for them.
- Distinctness within `reference` is what lets the stack and map hold values directly; with duplicates, hold positions instead and compare through the array.

## Comparison of Solutions

### Time Complexity

- **Brute Force Scan per Query**: `O(n * m)` - each query locates its value and rescans the tail.
- **One-Time Greater Table**: `O(m^2 + n)` - the quadratic fill is paid once; queries become lookups.
- **Monotonic Stack**: `O(m + n)` - one push-and-maybe-pop per reference value, one lookup per query.

### Space Complexity

- **Brute Force Scan per Query**: `O(m)` - the transient per-query tail slice, beyond the output.
- **One-Time Greater Table**: `O(m)` - the answer map.
- **Monotonic Stack**: `O(m)` - the stack and the answer map.

### Trade-offs

- **Brute Force Scan per Query**: no preprocessing and the least code, but overlapping tails are rescans; the cost grows with the query count.
- **One-Time Greater Table**: separates computation from lookup cleanly, yet fills the table by repeating the very scans the brute force ran.
- **Monotonic Stack**: linear in the input size with a small constant, at the price of the stack invariant, which must be recognized and stated.

### When to Use Each

- **Brute Force Scan per Query**: as the definition baseline, or for a single query against a tiny `reference`.
- **One-Time Greater Table**: when many queries repeat the same values and the input is small enough that the quadratic fill is harmless.
- **Monotonic Stack (Recommended)**: the answer to give in an interview: linear time, and the same sweep pattern transfers directly to next-greater variants (circular arrays, next smaller, daily temperatures).

### Optimization Notes

- **Monotonic Stack** is the recommended choice: it computes the same table as the One-Time Greater Table but in a single pass, by reusing each arrival's work for every waiting element it resolves.
- The stack holds values here only because `reference` is guaranteed distinct; holding indices generalizes the pattern to arrays with duplicates.
- The sweep never revisits a value, so streaming the values through works without random access: the pattern survives on inputs that can only be read once, left to right.
