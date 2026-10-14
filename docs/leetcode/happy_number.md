# [Happy Number](https://leetcode.com/problems/happy-number/)

**Easy** | **15 minutes** | **Hash Table, Math, Two Pointers**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md), [Two Pointers](../patterns/two_pointers/intuition.md)

**Algorithm:** [Cycle detection](https://en.wikipedia.org/wiki/Cycle_detection) · [Floyd's cycle detection](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare) · [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/happy_number/solution.py`](../../practice/happy_number/solution.py)

A **non-cyclical number** is an integer defined by the following algorithm:

* Given a positive integer, replace it with the sum of the squares of its digits.
* Repeat the above step until the number equals `1`, or it **loops infinitely in a cycle** which does not include `1`.
* If it stops at `1`, then the number is a **non-cyclical number**.

Given a positive integer `n`, return `true` if it is a **non-cyclical number**, otherwise return `false`.

## Examples

### Example 1

**Input:** `n = 100`

**Output:** `true`

**Explanation:** `1² + 0² + 0² = 1`

### Example 2

**Input:** `n = 101`

**Output:** `false`

**Explanation:** `1² + 0² + 1² = 2`
`2² = 4`
`4² = 16`
`1² + 6² = 37`
`3² + 7² = 58`
`5² + 8² = 89`
`8² + 9² = 145`
`1² + 4² + 5² = 42`
`4² + 2² = 20`
`2² + 0² = 4` (This number has already been seen)

## Constraints

- `1 <= n <= 1000`

## Deriving the Solution

The digit-square-sum rule turns every starting number into a chain: `n` leads to a next value, which leads to another, forever. Since values are bounded, the chain must eventually revisit a value, and the whole question is what it revisits: `1` (then stuck at `1` forever, happy) or a cycle that excludes `1`. So the problem is cycle detection on an implicitly defined sequence, and the approaches differ in how they notice the revisit.

1. **Start literal.** Follow the chain, collecting every value in a seen set;
   stop at `1` (happy) or at the first repeat (stuck). Correct, but the set
   grows with the chain length: see [Hash Set](#hash-set).
2. **Spot the waste.** Only two facts ever matter: whether the chain loops,
   and where. Memory of every past value is overkill when two runners at
   different speeds must meet iff a cycle exists: see
   [Floyd's Cycle Detection](#floyds-cycle-detection).

## Solutions

### Hash Set

#### Derivation

The literal reading simulates the algorithm from the statement and remembers everything it has produced: replace `n` with the sum of the squares of its digits, repeat, and stop when the number equals `1` or when a value repeats. The repeat is the statement's "loops infinitely in a cycle", caught the moment it happens:

1. Define `next_number(value)`: split `value` into its digits with divmod by
   `10`, sum the squares, return the total.
2. Keep `seen` as a set of visited values, seeded with `n`.
3. Loop: if the current value is `1`, return `True`; otherwise compute its
   successor; if the successor is already in `seen`, return `False`; add it.

One subtlety makes the bound tight: the chain from any `n <= 1000` drops below `243` (three digits of `9` sum to at most `243`) within a step or two and then wanders a bounded set, so the loop always terminates.

#### Walkthrough

Follow the chain from Example 2: `n = 101`, recording every value the loop produces and the test each one fails:

```text
seen = {}                     current = 101
101 not 1, 101 new            seen = {101},        next = 1 + 0 + 1 = 2
2   not 1, 2   new            seen = {101, 2},     next = 4
4   not 1, 4   new            seen = {101, 2, 4},  next = 16
16  not 1, 16  new            seen = {101, 2, 4, 16},   next = 37
37  not 1, 37  new            seen = {..., 37},    next = 58
58  not 1, 58  new            seen = {..., 58},    next = 89
89  not 1, 89  new            seen = {..., 89},    next = 145
145 not 1, 145 new            seen = {..., 145},   next = 42
42  not 1, 42  new            seen = {..., 42},    next = 20
20  not 1, 20  new            seen = {..., 20},    next = 4
4   already in seen          -> return False
```

The successor `4` collides with a stored value: the chain has entered the cycle `4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4`, which never reaches `1`, so the method returns `False`, matching the expected Output for Example 2. The set caught the loop at its first repetition.

#### Solution

The code is the walkthrough's loop: test for `1`, test the successor against `seen`, advance.

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def next_number(value: int) -> int:
            total = 0
            while value > 0:
                value, digit = divmod(value, 10)
                total += digit * digit
            return total

        seen = {n}
        while n != 1:
            n = next_number(n)
            if n in seen:
                return False
            seen.add(n)
        return True
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)` per step

Computing one successor costs a pass over the digits, `O(log n)`. The chain reaches the bounded regime below `243` after at most a couple of steps and then cycles within it, so the total is a bounded number of `O(log n)` digit passes for the fixed constraint range.

##### Space Complexity: `O(log n)` chain values in the bounded regime

The set holds every visited value: a couple of transient large ones, then at most the `243` values below the three-digit ceiling.

#### Key Insights

- The seen set converts the statement's vague "loops infinitely" into a precise, checkable event: the first repeat of a value.
- Every chain collapses into the sub-`243` regime almost immediately, which is why termination is guaranteed and the analysis stays honest despite unbounded-looking values.
- The set remembers far more than needed: membership tests only ever ask about the future's collisions, which is the observation Floyd's version exploits.

### Floyd's Cycle Detection

#### Derivation

The Hash Set answers one question, "does this chain loop?", but pays for a full memory of the past. [Floyd's tortoise and hare](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare) answers the same question with two pointers: `slow` takes one successor step per round and `fast` takes two. Inside a cycle, the gap between them shrinks by one each round, so they must meet; on a cycle-free tail into `1`, `fast` reaches `1` and parks there (`1`'s successor is `1`), where `slow` eventually joins it. Either way the loop ends, with no set:

1. Keep `next_number` verbatim from the Hash Set.
2. Start `slow = n` and `fast = next_number(n)`; loop while `fast != 1` and
   `slow != fast`.
3. Each round: `slow = next_number(slow)` and
   `fast = next_number(next_number(fast))`.
4. When the loop exits, `fast == 1` means happy and `slow == fast` means a
   cycle that excludes `1`.

#### Walkthrough

Run the two runners from Example 1: `n = 100`. The chain is `100 -> 1 -> 1 -> ...`, so the race ends almost immediately, with `fast` one step ahead from the start:

```text
start   slow = 100    fast = next(100) = 1     fast == 1 -> exit loop
return  fast == 1    -> True
```

The cycle-free case exits on the loop guard. For the cycle case, trace Example 2's chain `101 -> 2 -> 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4 -> ...`. The start is `slow = 101` and `fast = next(101) = 2`; each round advances `slow` one successor and `fast` two, so `fast` gains one position per round and must catch `slow` inside the cycle:

```text
round   slow   fast
start   101    2       seeded before the loop
1       2      16      fast gains one position per round
2       4      58
3       16     145
4       37     20
5       58     16
6       89     58
7       145    145     slow lands on fast's position -> slow == fast
exit    slow == fast and fast != 1    -> False
```

The runners meet inside the cycle at value `145` after seven rounds, and `fast` is not `1`, so the chain cycles without reaching `1` and the method returns `False`, matching the expected Output for Example 2.

#### Solution

The code is the race: advance the two runners until one lands on `1` or they collide.

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def next_number(value: int) -> int:
            total = 0
            while value > 0:
                value, digit = divmod(value, 10)
                total += digit * digit
            return total

        slow = n
        fast = next_number(n)
        while fast != 1 and slow != fast:
            slow = next_number(slow)
            fast = next_number(next_number(fast))
        return fast == 1
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)` per step, bounded rounds

Each round costs three successor computations, each `O(log n)`. Once both runners are inside the cycle of length at most `243`, they meet within that many rounds, so the total is a bounded number of digit passes for the constraint range.

##### Space Complexity: `O(1)`

Two integer variables; the chain's past is never stored.

#### Key Insights

- Floyd's algorithm needs no memory of the past because a cycle forces a meeting: on a cycle of length `L` the gap shrinks by exactly one per round, so collision is inevitable within `L` rounds.
- The exit condition reads `fast`, not `slow`: `fast` visits every value `slow` does and more, so it is guaranteed to be the first to touch `1` on a happy chain.
- This is the same two-pointer pattern that detects cycles in linked lists, applied to an implicit list whose "next" pointer is the digit-square-sum function.

## Comparison of Solutions

The practice harness's `practice/happy_number/reference.py` implements the **Floyd's Cycle Detection** solution.

### Time Complexity

- **Hash Set**: bounded number of `O(log n)` successor computations - the chain enters the sub-`243` regime within a couple of steps and each successor is a digit pass.
- **Floyd's Cycle Detection**: bounded rounds of three `O(log n)` successor computations - meeting is guaranteed within one cycle length once both runners are inside.

### Space Complexity

- **Hash Set**: `O(log n)` chain values in the bounded regime - every visited value is stored until the first repeat.
- **Floyd's Cycle Detection**: `O(1)` - two runner variables, no history.

### Trade-offs

- **Hash Set**: The simulation that reads exactly like the statement, trivially correct and easy to debug, at the price of storing the whole visited chain.
- **Floyd's Cycle Detection**: Constant space with a two-line core, at the price of trusting a meeting argument instead of observing a repeated value.

### When to Use Each

- **Hash Set**: First implementation and the oracle; also the right call whenever the successor function is expensive, since it never recomputes a step.
- **Floyd's Cycle Detection** (recommended): The default; the successor is cheap here, so paying memory to remember it buys nothing.

### Optimization Notes

- Hardcoding is a legitimate constant-factor win on this problem: the only cycles are the `1` loop and the eight-value `4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4` cycle, so testing membership in the unhappy cycle's set decides every chain in one step once it drops below `243`.
- The successor's digit loop via `divmod` avoids string conversion, which would allocate a fresh string per step; the arithmetic form is both faster and allocation-free.
- The bounded-regime argument (three digits sum to at most `243`) is what makes "the loop terminates" provable rather than hopeful; any analysis skipping it is incomplete.

