# [Min Stack](https://leetcode.com/problems/min-stack/)

**Medium** | **20 minutes** | **Stack, Design**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md)

**Algorithm:** [Stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))

**Practice:** [`practice/min_stack/solution.py`](../../practice/min_stack/solution.py)

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:

- `MinStack()` initializes the stack object.
- `void push(int val)` pushes the element val onto the stack.
- `void pop()` removes the element on the top of the stack.
- `int top()` gets the top element of the stack.
- `int getMin()` retrieves the minimum element in the stack.

You must implement a solution with `O(1)` time complexity for each function.

## Examples

### Example 1

**Input:**

```text
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]
```

**Output:** `[null,null,null,null,-3,null,0,-2]`

**Explanation:**

```text
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // return -3
minStack.pop();
minStack.top();    // return 0
minStack.getMin(); // return -2
```

## Constraints

- `-2^31 <= val <= 2^31 - 1`
- Methods `pop`, `top` and `getMin` operations will always be called on **non-empty** stacks.
- At most `3 * 10^4` calls will be made to `push`, `pop`, `top`, and `getMin`.

## Deriving the Solution

On a plain stack, `push`, `pop`, and `top` are already constant time; the whole problem is `getMin`, which must stay `O(1)` even after arbitrary pops. Every fast solution below answers the same way: record, at push time, what the minimum is at each height of the stack, so that popping automatically re-exposes an older minimum.

1. **Start literal.** Keep one stack of values and compute the minimum on
   demand by scanning every element. Correct, but `getMin` costs `O(n)`, which the problem statement forbids: see [Brute Force](#brute-force).
2. **Spot the redo.** The scan recomputes a value that was already known: the
   minimum changes only when a smaller value is pushed or when the entry that set it is popped. Between those events, every `getMin` re-derives the same number from scratch.
3. **Cache it at push.** Store alongside each entry the minimum of the stack up
   to and including that entry. `getMin` becomes a top-of-stack read, and `pop` restores the older minimum for free, because it already sits one entry down. The same idea wears two costumes: value and cached minimum bundled as a tuple, in [Single Stack of Pairs](#single-stack-of-pairs), or kept in a parallel minimum stack, in [Two Stacks](#two-stacks).
4. **Shrink the cache.** One extra integer per element is mostly redundant,
   since the cached minimum rarely changes. Encode only the changes into the stored numbers themselves with reversible arithmetic, leaving one integer per element plus a single variable: see [Single Stack with Encoded Minimum](#single-stack-with-encoded-minimum).

## Solutions

### Brute Force

#### Derivation

The most direct idea ignores the `O(1)` requirement at first and asks: what is the simplest structure that answers all four calls correctly? A single plain [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) of values suffices. `push`, `pop`, and `top` are trivial list operations. For `getMin`, with no extra bookkeeping, the only option is to walk every element and track the smallest one seen.

1. Store pushed values in a single list used as a stack.
2. `push` appends, `pop` removes the last element, and `top` reads the last
   element.
3. `getMin` linearly scans the entire stack, comparing each value against a
   running smallest, and returns the smallest found.

This is correct and simple to reason about, but `getMin` does `O(n)` work, which violates the problem's `O(1)` requirement.

#### Walkthrough

Let us watch the Brute Force code run on Example 1, calling each method in order on a fresh `MinStack`. After `__init__`, `self.stack` is the empty list `[]`. The table shows `self.stack` after each call, plus what the call returns (`push` and `pop` return nothing, shown as `None`).

| Call | What runs | `self.stack` after | Returns |
|------|-----------|--------------------|---------|
| `push(-2)` | `append(-2)` | `[-2]` | `None` |
| `push(0)` | `append(0)` | `[-2, 0]` | `None` |
| `push(-3)` | `append(-3)` | `[-2, 0, -3]` | `None` |
| `getMin()` | scan `[-2, 0, -3]` | `[-2, 0, -3]` | `-3` |
| `pop()` | `pop()` removes last | `[-2, 0]` | `None` |
| `top()` | read `stack[-1]` | `[-2, 0]` | `0` |
| `getMin()` | scan `[-2, 0]` | `[-2, 0]` | `-2` |

The two `getMin` calls are where the scan happens. Trace the first one: it sets `smallest = stack[0] = -2`, then walks the list. `-2 < -2` is false, `0 < -2` is false, `-3 < -2` is true so `smallest` becomes `-3`, and `-3` is returned. The second `getMin` runs on the shorter list `[-2, 0]`: `smallest` starts at `-2`, `0 < -2` is false, so it stays `-2` and returns `-2`.

Collecting every return value in order gives `[null, null, null, null, -3, null, 0, -2]`, which matches the example's expected Output.

#### Solution

The code is the table above written down: three one-line list operations plus the scanning loop inside `getMin`.

```python
class MinStack:

    def __init__(self):
        self.stack: list[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        # Scan the whole stack every time to find the smallest value.
        smallest = self.stack[0]
        for value in self.stack:
            if value < smallest:
                smallest = value
        return smallest


# Your MinStack object will be instantiated and used as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` for push/pop/top, `O(n)` for getMin

`push`, `pop`, and `top` touch only the last element, but `getMin` scans all `n` elements on every call, so it fails the constant-time requirement.

##### Space Complexity: `O(n)`

A single list stores the `n` pushed values with no auxiliary structure.

#### Key Insights

- The naive baseline: store values plainly and recompute the minimum on demand.
- It exposes the real challenge, which is making `getMin` constant time rather
  than a full scan.
- Every later solution removes the `getMin` scan by caching the minimum as
  elements are pushed.

### Single Stack of Pairs

#### Derivation

The Brute Force scan exists because, after a pop, nothing remembers what the minimum used to be, so it must be rediscovered from scratch. The repair is to make every entry remember it: store the minimum alongside each value, so each entry records what the minimum was when it sat on top. Popping then restores the older minimum automatically, because the entry underneath carries it.

1. Store each pushed element as a pair `(val, current_min)`, where
   `current_min` is the smaller of `val` and the minimum currently on top of the stack.
2. On `push`, look at the previous top's stored minimum (or use `val` itself
   when the stack is empty) and record the new pair.
3. On `pop`, simply discard the top pair; the entry now on top already carries
   the correct minimum for the remaining elements.
4. `top` returns the value field of the top pair, and `getMin` returns its
   minimum field.

Because each entry caches the minimum of the entire stack beneath it, removing the top never requires recomputation.

#### Walkthrough

Let us run the Example 1 sequence on a fresh `MinStack`, watching `self.stack`, now a list of `(val, current_min)` pairs:

```text
push(-2)   stack = [(-2, -2)]                      empty stack: current_min = -2
push(0)    stack = [(-2, -2), (0, -2)]             min(0, -2) = -2
push(-3)   stack = [(-2, -2), (0, -2), (-3, -3)]   min(-3, -2) = -3
getMin()   -> -3                                   read stack[-1][1]
pop()      stack = [(-2, -2), (0, -2)]             discard the top pair
top()      -> 0                                    read stack[-1][0]
getMin()   -> -2                                   read stack[-1][1]
```

The `pop` is where the caching pays off: discarding `(-3, -3)` exposes `(0, -2)`, whose second field already holds the minimum of the remaining elements, so the final `getMin` answers `-2` with a single lookup and no scan. The returns collected in order are `[null, null, null, null, -3, null, 0, -2]`, matching the expected Output.

#### Solution

The code is the pair bookkeeping from the trace: `push` computes `current_min`, and the three reads index the top pair.

```python
class MinStack:

    def __init__(self):
        # Each entry stores (value, minimum of the stack at and below this entry)
        self.stack: list[tuple[int, int]] = []

    def push(self, val: int) -> None:
        current_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


# Your MinStack object will be instantiated and used as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` per operation

`push`, `pop`, `top`, and `getMin` each perform a constant number of list operations and comparisons, so all four run in constant time as required.

##### Space Complexity: `O(n)`

Each of the `n` pushed elements stores an extra integer for the cached minimum, which doubles the storage but remains linear in the number of elements.

#### Key Insights

- Pairing every value with the minimum-so-far converts the `getMin` query into
  a constant-time lookup of the top entry.
- The cached minimum is monotonic going down the stack, so popping the top
  automatically exposes the correct minimum underneath.
- Bundling both fields in a single list keeps the data structure compact: there
  is only one container to push to and pop from.

### Two Stacks

#### Derivation

The pairs solution bundles two concerns into one tuple: the value the caller pushed and the bookkeeping minimum. This variant asks whether the two concerns read more clearly kept apart, and splits them into two separate stacks that move in lockstep: one holds the raw values, and the other tracks the running minimum so its top always equals the minimum of everything currently in the value stack.

1. On `push`, append the value to the value stack. Then push the smaller of the
   new value and the current top of the minimum stack (or the value itself when the minimum stack is empty).
2. On `pop`, pop both stacks together so they stay aligned.
3. `top` returns the top of the value stack, and `getMin` returns the top of the
   minimum stack.

Because the minimum stack mirrors the value stack one-for-one, every pop exposes the correct minimum for the remaining elements without recomputation.

#### Walkthrough

Let us run the Example 1 sequence again, now watching both stacks. `self.mins` holds, at each height, the minimum of everything at or below that height in `self.stack`:

```text
push(-2)   stack = [-2]          mins = [-2]           first value is its own minimum
push(0)    stack = [-2, 0]       mins = [-2, -2]       min(0, -2) = -2
push(-3)   stack = [-2, 0, -3]   mins = [-2, -2, -3]   min(-3, -2) = -3
getMin()   -> -3                                       read mins[-1]
pop()      stack = [-2, 0]       mins = [-2, -2]       both stacks pop together
top()      -> 0                                        read stack[-1]
getMin()   -> -2                                       read mins[-1]
```

The two stacks always have the same height, and `mins` is exactly the second field of the pairs solution split into its own container: after the `pop` removes `-3` from both stacks, the top of `mins` is again `-2`, the minimum of what remains. The returns in order are `[null, null, null, null, -3, null, 0, -2]`, matching the expected Output.

#### Solution

The code is the lockstep bookkeeping from the trace: every `push` and `pop` touches both lists.

```python
class MinStack:

    def __init__(self):
        self.stack: list[int] = []
        # Parallel stack whose top is always the minimum of the value stack.
        self.mins: list[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Carry forward the smaller of the new value and the current minimum.
        current_min = val if not self.mins else min(val, self.mins[-1])
        self.mins.append(current_min)

    def pop(self) -> None:
        self.stack.pop()
        self.mins.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.mins[-1]


# Your MinStack object will be instantiated and used as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` per operation

Each method performs a fixed number of list appends, pops, and comparisons, so all four operations run in constant time as required.

##### Space Complexity: `O(n)`

The minimum stack grows one entry per push, matching the value stack, so the total storage is linear in the number of elements.

#### Key Insights

- Separating values from minimums keeps each stack holding plain integers, which
  some readers find clearer than reasoning about tuples.
- The minimum stack is non-increasing from bottom to top, so its top is always
  the global minimum of the current contents.
- Pushing and popping both stacks together is what guarantees alignment; the two
  stacks always have identical heights.

### Single Stack with Encoded Minimum

#### Derivation

Both cached approaches above store an extra integer for every pushed element, even though the cached minimum rarely changes from one entry to the next. This variant keeps a single stack of plain integers plus one minimum variable, and encodes the history of the minimum directly into the stored numbers, so the only overhead beyond the values themselves is that one variable.

1. Keep one stack and a `min` variable holding the current minimum.
2. On `push`, if the value is at least the current minimum, store it as is. If
   it is a new minimum, store the encoded value `2 * val - min` instead and set `min = val`. Because `val < min`, the encoded number equals `val + (val - min)`, which is strictly less than `val`: every encoded entry sits strictly below the minimum that was current when it was pushed.
3. On `pop`, compare the removed entry against `min`. A value below `min` can
   only be an encoded "the minimum changed here" marker, so undo that change by decoding the previous minimum: `2 * min - popped` expands to `2 * val - (2 * val - old_min) = old_min`. A value at or above `min` is a plain entry and leaves the minimum untouched.
4. `top` applies the same test: a top entry below `min` is encoded, and the
   real value it represents is the current minimum itself; otherwise the entry is the value. `getMin` just returns the variable.

The invariant that makes this work is that no plain entry is ever below the current minimum while every encoded entry is strictly below it, so "stored entry is less than `min`" is an unambiguous signal that the entry encodes a minimum change. The Invariant below states that formally, along with why the encode and decode are inverses. Note that equal values are stored plainly (the test is a strict `<`), so repeated minima pop off without disturbing `min` until the entry that actually changed it is removed.

One honest caveat: in Python this is fully correct because integers have arbitrary precision, so `2 * val - min` can never overflow. In fixed-width languages the doubling can exceed the integer range (with `val` near the 32-bit limits, `2 * val - min` needs a 64-bit type), so the trick demands a wider type or careful bounds analysis. That fragility is why the pairs and two-stack approaches are usually preferred in interviews unless the space follow-up is asked explicitly.

#### Invariant

Write \(\textit{min}\) for `self.min`. Call a stored entry *plain* when it is the pushed value itself and *encoded* when it is `2 * val - min`. Everything rests on one property, checked against the minimum current while the entry sits on top:

$$ \text{plain entry } e:\ e \ge \textit{min} \qquad\qquad \text{encoded entry } e:\ e < \textit{min} $$

```text
plain entry e:    e >= self.min
encoded entry e:  e <  self.min
                  (self.min taken while e sits on top of the stack)
```

Both halves hold. A plain entry is stored only when `val >= self.min`, and `self.min` always equals the minimum over the values still in the stack, so it can never exceed a buried entry: that entry is still at least the minimum when it resurfaces. Note the minimum does *rise* as encoded entries are popped, so it is this stack-wide reading, not a claim that the minimum never increases, that carries the argument. An encoded entry is stored only when `val < self.min`, and

$$ 2\,\textit{val} - \textit{min} \;=\; \textit{val} - (\textit{min} - \textit{val}) \;<\; \textit{val} \;=\; \textit{min}_{\text{new}} $$

```text
when val < self.min:
    2 * val - self.min = val - (self.min - val) < val = new self.min
```

so the stored number lands strictly below the minimum it announces. The strict `<` in the push test is what keeps the two ranges disjoint: on `val == self.min` the same arithmetic gives `2 * val - min == val == min`, which would sit in both ranges at once and make the classification test ambiguous. Relaxing it to `<=` happens to change no observable behavior, since that branch would then store `val` and leave the minimum untouched, which is what the plain branch already does. The invariant is what needs the strictness, not the output. Equal values are stored plainly instead, which is exactly right, since discarding one of several equal minima leaves the minimum where it is.

Because the ranges are disjoint, the single test `popped < self.min` in `pop` (and `value < self.min` in `top`) classifies an entry with no flag, tuple, or second container. For an encoded entry the decode then inverts the encode: with `popped = 2 * val - old_min` and `self.min == val`,

$$ 2\,\textit{min} - \textit{popped} \;=\; 2\,\textit{val} - (2\,\textit{val} - \textit{old\_min}) \;=\; \textit{old\_min} $$

```text
when popped = 2 * val - old_min and self.min == val:
    2 * self.min - popped = 2 * val - (2 * val - old_min) = old_min
```

so `pop` restores the previous minimum exactly, and `top` reports `self.min`, which is the `val` the encoded entry stood for.

#### Walkthrough

Example 1 exercises the encoding directly, because its third push is a new minimum. Watch `self.stack` and `self.min` through the sequence:

```text
push(-2)   stack = [-2]          min = -2   empty stack: store plainly, set min
push(0)    stack = [-2, 0]       min = -2   0 >= min: store plainly
push(-3)   stack = [-2, 0, -4]   min = -3   -3 < min: store 2*(-3) - (-2) = -4, min = -3
getMin()   -> -3                            return min
pop()      stack = [-2, 0]       min = -2   popped -4 < min: min = 2*(-3) - (-4) = -2
top()      -> 0                             0 >= min: plain entry, return it
getMin()   -> -2                            return min
```

The value `-3` is never stored at all: the stack holds the marker `-4` in its place, strictly below the new minimum, exactly as the Invariant requires. When `pop` removes that marker, the test `-4 < -3` recognizes it as encoded and the decode `2 * (-3) - (-4)` restores the previous minimum `-2`. The returns in order are `[null, null, null, null, -3, null, 0, -2]`, matching the expected Output.

#### Solution

The code is the trace's three-way `push` branch plus the decode in `pop` and the classification test in `top`.

```python
class MinStack:

    def __init__(self):
        self.stack: list[int] = []
        self.min: int = 0

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append(val)
            self.min = val
        elif val < self.min:
            # New minimum: store an encoded marker instead of the value.
            # Since val < min, 2*val - min = val + (val - min) < val, so the
            # stored entry is strictly below the new minimum (val). That is
            # what lets pop and top recognize it as encoded later.
            self.stack.append(2 * val - self.min)
            self.min = val
        else:
            self.stack.append(val)

    def pop(self) -> None:
        popped = self.stack.pop()
        if popped < self.min:
            # Encoded entry: the minimum changed at this element, so restore
            # the previous minimum. With popped = 2*val - old_min and
            # min = val, 2*min - popped = 2*val - 2*val + old_min = old_min.
            self.min = 2 * self.min - popped

    def top(self) -> int:
        value = self.stack[-1]
        # An encoded entry always represents the current minimum itself.
        return self.min if value < self.min else value

    def getMin(self) -> int:
        return self.min


# Your MinStack object will be instantiated and used as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` per operation

- `push`: one comparison and at most one multiply-subtract before a single
  append.
- `pop`: one list pop plus a constant-time decode when the entry was encoded.
- `top`: one index lookup and one comparison.
- `getMin`: returns the stored variable directly.

##### Space Complexity: `O(n)`

The single stack holds exactly one integer per pushed element, and the only auxiliary state is the one `min` variable: `O(1)` extra beyond the values. The pairs and two-stack versions store up to `2n` integers for the same contents.

#### Key Insights

- The encoding is sentinel-free: no flag, tuple, or second container marks
  where the minimum changed. The ordering invariant itself (encoded entries are strictly below the current minimum) carries that information.
- It halves the constant factor on space: `n` stored numbers plus one variable,
  versus up to `2n` for the pairs and two-stack versions, while keeping every operation `O(1)`.
- The trick is not fully portable: `2 * val - min` relies on arithmetic that
  cannot overflow. Python grants that for free; C, C++, and Java require a wider intermediate type, which is why this is a follow-up answer rather than a default interview answer.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(1)` for push/pop/top, `O(n)` for getMin - the scan walks
  every element to find the minimum.
- **Single Stack of Pairs**: `O(1)` per operation - one tuple append, pop, or
  index lookup.
- **Two Stacks**: `O(1)` per operation - one append or pop on each of two stacks.
- **Single Stack with Encoded Minimum**: `O(1)` per operation - one append or
  pop plus a constant amount of encode/decode arithmetic.

### Space Complexity

- **Brute Force**: `O(n)` - a single list of values with no auxiliary structure.
- **Single Stack of Pairs**: `O(n)` - each element stores its value and the
  cached minimum together.
- **Two Stacks**: `O(n)` - the parallel minimum stack adds one integer per push.
- **Single Stack with Encoded Minimum**: `O(n)` - one integer per element plus
  a single minimum variable, so only `O(1)` extra beyond the values themselves.

### Trade-offs

- Brute Force is the simplest to write and uses the least memory, but its `O(n)`
  `getMin` fails the problem's constant-time requirement.
- The two cached approaches store the same amount of extra information (one
  cached minimum per element) and meet the `O(1)` requirement for every operation.
- The single stack keeps everything in one container, so push and pop touch only
  one list.
- The two-stack version keeps each container holding plain integers, which some
  find easier to read, at the cost of maintaining two lists in lockstep.
- The encoded variant is the leanest on memory (no second number per element),
  but the stored entries are no longer the raw values, so inspecting the stack requires decoding, and in fixed-width languages the arithmetic risks overflow.

### When to Use Each

- **Brute Force**: Never for this problem's stated `O(1)` constraint; useful only
  as a teaching baseline that motivates caching the minimum.
- **Single Stack of Pairs**: When you prefer a single data structure and are
  comfortable unpacking tuples.
- **Two Stacks**: When you prefer to keep values and minimums conceptually
  separate, or when an interviewer asks for the classic two-stack formulation.
- **Single Stack with Encoded Minimum**: When memory is at a premium, or as the
  answer to the follow-up "can you do it with `O(1)` extra space beyond the values?"; otherwise prefer the pairs or two-stack versions, which have no overflow caveat.

### Optimization Notes

- The brute force recomputes the minimum on every `getMin`; both cached solutions
  eliminate that scan by carrying the running minimum forward, which is the core trick that turns an `O(n)` query into an `O(1)` lookup.
- A further memory optimization stores only minimums that actually change (a
  monotonic minimum stack), shrinking the auxiliary stack when many pushes share the same minimum, at the cost of slightly more bookkeeping on pop.
- The encoded variant takes that idea to its limit: it records minimum changes
  in-place with arithmetic instead of extra storage, leaving exactly one number per element plus one variable. The cost is that the arithmetic must not overflow, which Python guarantees and fixed-width languages do not.
