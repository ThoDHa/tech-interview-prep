# [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/)

**Medium** | **25 minutes** | **Linked List, Math, Recursion**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Linked list](https://en.wikipedia.org/wiki/Linked_list) · [Recursion (computer science)](https://en.wikipedia.org/wiki/Recursion_(computer_science)) · [Positional notation](https://en.wikipedia.org/wiki/Positional_notation)

**Practice:** [`practice/add_two_numbers/solution.py`](../../practice/add_two_numbers/solution.py)

You are given two **non-empty** linked lists, `l1` and `l2`, where each represents a non-negative integer.

The digits are stored in **reverse order**, e.g. the number 321 is represented as `1 -> 2 -> 3 ->` in the linked list.

Each of the nodes contains a single digit. You may assume the two numbers do not contain any leading zero, except the number `0` itself.

Return the sum of the two numbers as a linked list.

## Examples

### Example 1

**Input:** `l1 = [1,2,3], l2 = [4,5,6]`

**Output:** `[5,7,9]`

**Explanation:** 321 + 654 = 975.

### Example 2

**Input:** `l1 = [9], l2 = [9]`

**Output:** `[8,1]`

## Constraints

- `1 <= l1.length, l2.length <= 100`.
- `0 <= Node.val <= 9`

## Deriving the Solution

Digits stored in reverse order put the least significant digits first, which is exactly the order schoolbook addition consumes them: add the two current digits plus a carry, emit the unit digit, promote the carry. Every solution is that algorithm; they differ in whether the traversal is iterative or recursive and in how the unequal lengths and the final carry are handled.

1. **Start literal.** Decode each list into its integer, add them, and encode
   the sum back into a list. One pass per conversion, `O(n + m)`, but it
   builds two full numbers the problem never needs: see
   [Integer Round Trip](#integer-round-trip).
2. **Spot the waste.** The decode step is only a way to align digit places,
   which the list order already does: position `i` of each list holds the
   same power of ten. Add digit-wise with a carry instead, walking both lists
   at once, and a dummy head spares the special case for the result's first
   node: see [Digit-wise Addition](#digit-wise-addition).
3. **The same sum, recursively.** A linked list is a natural recursion: the
   sum of two lists is one node (the digit total mod 10) followed by the sum
   of the tails (and an extra node carrying `1` when both tails end on a
   carry): see [Recursive Addition](#recursive-addition).

## Solutions

### Integer Round Trip

#### Derivation

The most direct reading turns the linked lists into the numbers they denote and lets arithmetic do the rest:

1. Walk each list tracking the current place value `place`, starting at `1`
   and multiplied by `10` per step: the reversed storage makes the head the
   units digit, so accumulate `value += node.val * place`.
2. Compute `total = value1 + value2`.
3. Emit `total`'s digits least-significant-first by repeatedly taking
   `total % 10` and dividing by `10`, allocating one node per digit. `total`
   of `0` emits a single `0` node.

#### Walkthrough

Trace the round trip on Example 1: `l1 = [1,2,3]`, `l2 = [4,5,6]`:

```text
decode l1:  1·1 + 2·10 + 3·100  = 321
decode l2:  4·1 + 5·10 + 6·100  = 654
total = 321 + 654 = 975
encode:     975 % 10 = 5, 975 // 10 = 97
            97  % 10 = 7, 97  // 10 = 9
            9   % 10 = 9, 9   // 10 = 0
            digits emitted: [5, 7, 9]
```

The decoded values match the problem's reading (the problem states `321 + 654 = 975`), and the encoding emits least-significant digit first, which is the list's storage order. The result list is `[5,7,9]`, matching the expected Output for Example 1.

#### Solution

The code is the decode, add, encode pipeline. Python integers are unbounded, so no overflow case exists.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def to_number(node: Optional[ListNode]) -> int:
            value = 0
            place = 1
            while node is not None:
                value += node.val * place
                place *= 10
                node = node.next
            return value

        total = to_number(l1) + to_number(l2)

        dummy = ListNode()
        current = dummy
        while True:
            current.next = ListNode(total % 10)
            current = current.next
            total //= 10
            if total == 0:
                break
        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + m)`

Two decode walks plus one encode walk, linear in the list lengths. (For fixed-width machine integers the arithmetic itself would also matter; Python's big integers make digit additions cost more than `O(1)` at extreme sizes.)

##### Space Complexity: `O(n + m)`

The output list holds `max(n, m) + 1` nodes in the worst case, and the two decoded integers hold up to `n` and `m` digits.

#### Key Insights

- The place-value multiplier is what makes the naive decode correct: the
  head is the units digit, so each step's contribution is
  `node.val * place`, not a new most-significant digit.
- Clean and obviously correct, but it materializes numbers the problem never
  asks for; languages without big integers fail the length-100 constraint.
- The dummy head absorbs the "first node" special case in the encode loop.

### Digit-wise Addition

#### Derivation

Both lists store the same decimal place at the same position, so addition can stream: the `i`-th nodes and the carry decide the `i`-th output digit, exactly as schoolbook addition decides column `i` from column `i` alone. Unequal lengths become "a missing digit is `0`", and a leftover carry after both lists end becomes one extra node. A dummy head lets the first output node be attached with the same code as every later one:

1. Start at `n1 = l1`, `n2 = l2`, `carry = 0`, with `dummy` as the anchor and
   `current` the growth point.
2. While a list has nodes or `carry` is set: read `digit1` and `digit2`
   (`0` past a list's end), compute `total = digit1 + digit2 + carry`.
3. Append `ListNode(total % 10)` and set `carry = total // 10`.
4. Advance each list that still has nodes; return `dummy.next`.

#### Invariant

After each iteration the digits emitted so far are the low `i` digits of the true sum, and `carry` is the amount owed to position `i + 1`:

```text
before iteration i:   result holds digits 0..i-1 of (l1 + l2), carry = owed carry
the step:             total = digit1(i) + digit2(i) + carry
                      emit total % 10, carry becomes total // 10
loop ends when:       both lists exhausted and carry == 0
                      -> every position has been emitted, nothing is owed
```

The loop condition `n1 is not None or n2 is not None or carry != 0` is the invariant's termination clause: ending only when no position remains and no carry is owed is what makes the final `[9] + [9] -> [8,1]` case fall out without post-loop code.

#### Walkthrough

Trace the streaming add on Example 2: `l1 = [9]`, `l2 = [9]`:

```text
round 1:  digit1=9  digit2=9  carry=0   total=18   emit 8   carry=1
round 2:  digit1=0  digit2=0  carry=1   total=1    emit 1   carry=0
          both lists exhausted, carry 0 -> stop
```

Round 1 emits the unit digit `8` and owes `1`. Round 2 runs only because the carry is still set, and emits it as the final node. The result is `[8,1]`, matching the expected Output for Example 2. On Example 1 (`[1,2,3] + [4,5,6]`) the three rounds compute `1+4 = 5`, `2+5 = 7`, and `3+6 = 9`, all below ten, so `carry` stays `0` and the result `[5,7,9]` matches the expected Output for Example 1.

#### Solution

The code is the invariant's loop written down; the sentinel reads keep the unequal-length case branch-free.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        current = dummy
        carry = 0
        n1, n2 = l1, l2
        while n1 is not None or n2 is not None or carry != 0:
            digit1 = n1.val if n1 is not None else 0
            digit2 = n2.val if n2 is not None else 0
            total = digit1 + digit2 + carry
            current.next = ListNode(total % 10)
            current = current.next
            carry = total // 10
            if n1 is not None:
                n1 = n1.next
            if n2 is not None:
                n2 = n2.next
        return dummy.next
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

One iteration per output digit; each does constant work and advances at least one list.

##### Space Complexity: `O(max(n, m))`

The output list: one node per emitted digit, plus the carry node when set.

#### Key Insights

- Streaming with a carry is the schoolbook algorithm the reversed order was
  designed for; no number is ever materialized.
- `digit = node.val if node is not None else 0` is the idiomatic way to add
  lists of different lengths without padding.
- The triple loop condition (either list, or carry) is the whole edge-case
  story: `[9] + [9]` and `[5] + [5]` need no special code.

### Recursive Addition

#### Derivation

The streaming add is already a recurrence: the output at a pair of positions is a node whose tail is the output of the next pair. Write it as one: `add(n1, n2, carry)` returns the list summing the lists from `n1` and `n2` on, given the carry owed in. The base case is "nothing left and nothing owed is the empty list", and the recursion steps one position per call. Each call consumes the current nodes, so depth is the output length:

1. If `n1` and `n2` are both `None` and `carry == 0`, return `None`.
2. Read `digit1` and `digit2` (`0` for a `None` list) and compute
   `total = digit1 + digit2 + carry`.
3. Allocate the node holding `total % 10`; its `next` is the recursion on the
   successors with `carry = total // 10`.
4. Return the node; the top-level call uses `carry = 0`.

#### Walkthrough

Trace the recursion on Example 2: `l1 = [9]`, `l2 = [9]`:

```text
add(9, 9, carry=0):   total=18, node(8), recurse add(None, None, 1)
  add(None, None, 1): total=1,  node(1), recurse add(None, None, 0)
    add(None, None, 0): base case -> None
result: 8 -> 1
```

The carry rides down the call chain as an argument, and the final carry spawns the extra node one level above the base case. The result is `[8,1]`, matching the expected Output for Example 2. On Example 1 the three calls emit `5`, `7`, `9` (total `5`, `7`, `9`, never exceeding nine), and the fourth call hits the base case, producing `[5,7,9]`, matching the expected Output for Example 1.

#### Solution

The code is the recurrence; default arguments express the `0` digit and the initial carry.

```python
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def add(n1: Optional[ListNode], n2: Optional[ListNode], carry: int) -> Optional[ListNode]:
            if n1 is None and n2 is None and carry == 0:
                return None
            digit1 = n1.val if n1 is not None else 0
            digit2 = n2.val if n2 is not None else 0
            total = digit1 + digit2 + carry
            node = ListNode(total % 10)
            node.next = add(
                n1.next if n1 is not None else None,
                n2.next if n2 is not None else None,
                total // 10,
            )
            return node

        return add(l1, l2, 0)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

One call per output digit, constant work per call.

##### Space Complexity: `O(max(n, m))`

The output list plus a call stack frame per digit; the recursion depth equals the result length.

#### Key Insights

- The carry is naturally a recursion parameter: each level owes the next
  level one digit of debt.
- The base case folds three conditions (both lists done, no carry), which
  is why the iterative loop's triple condition and this base case are the
  same statement.
- Python's default recursion limit (about 1000) is just above the
  constraint's maximum length of 100 digits; in shallower-stack languages
  the iterative version is the safe one.

## Comparison of Solutions

### Time Complexity

- **Integer Round Trip**: `O(n + m)` - decode both lists, add, encode.
- **Digit-wise Addition**: `O(max(n, m))` - one iteration per output digit.
- **Recursive Addition**: `O(max(n, m))` - one call per output digit.

### Space Complexity

- **Integer Round Trip**: `O(n + m)` - two decoded integers plus the output.
- **Digit-wise Addition**: `O(max(n, m))` - the output list only.
- **Recursive Addition**: `O(max(n, m))` - the output list plus the call stack.

### Trade-offs

- All three are linear; the round trip hides a bigger constant and a
  big-integer dependency behind its brevity.
- The digit-wise loop is the portable answer: constant work per digit, no
  stack growth, no overflow concerns.
- The recursion is the same algorithm as the loop with the stack implicit;
  it reads cleanly but spends a frame per digit.

### When to Use Each

- **Integer Round Trip**: When lists are known to be short and the language
  has arbitrary-precision integers; fastest to write from scratch.
- **Digit-wise Addition**: The default and the interview answer; streaming,
  stack-free, and edge cases absorbed by one loop condition (recommended here).
- **Recursive Addition**: When the interviewer asks for the recursive
  formulation, or as a stepping stone to sum-lists-with-carry variants.

### Optimization Notes

- The dummy head in the iterative version exists to make the first append
  identical to every other append; without it the first node is a special
  case.
- The round trip's encode loop uses `while True` with a trailing break so a
  `total` of `0` still emits its single `0` digit.
- Neither streaming version mutates the input lists; only fresh nodes are
  allocated.
