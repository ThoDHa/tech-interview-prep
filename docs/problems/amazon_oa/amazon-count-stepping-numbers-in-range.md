# [Count Stepping Numbers In Range](https://www.fastprep.io/problems/amazon-count-stepping-numbers-in-range)

**Hard** | **NN minutes** | **Math, Breadth First Search, Dynamic Programming**

A stepping number is an integer whose adjacent digits differ by exactly 1. Every one-digit integer, including 0, is a stepping number.

Given two integers low and high, return the number of stepping numbers in the inclusive range [low, high].

## Examples

### Example 1

**Input:** `low = 0`, `high = 21`

**Output:** `13`

**Explanation:** The stepping numbers in [0, 21] are 0 through 9, plus 10, 12, and 21.

### Example 2

**Input:** `low = 10`, `high = 15`

**Output:** `2`

**Explanation:** Only 10 and 12 are stepping numbers in [10, 15].

## Constraints

- `0 <= low <= high <= 10^15.`

## Solutions

### Brute Force Enumeration

#### Derivation

The most literal reading executes the problem's own sentence: an integer is a stepping number exactly when every adjacent digit pair differs by 1, so visit every integer in `[low, high]`, test its digits, and count the survivors. The range is explicit in the input and the test is a property of the decimal string, which makes this the natural first pass:

1. `is_stepping(value)` converts `value` to its decimal string `digits` and
   checks `abs(int(digits[position]) - int(digits[position - 1])) == 1` for every
   `position` from `1` to the last digit; a one-digit string has no adjacent pair,
   so it passes vacuously, which encodes the "every one-digit integer is a
   stepping number" rule for free.
2. Iterate `value` over `low` through `high` inclusive and count the values where
   `is_stepping` holds.

#### Walkthrough

Example 1, `low = 0`, `high = 21`, walks twenty-two candidates. The single digits and `0` all pass with no adjacent pair to check, and the two-digit candidates split by their one gap:

```text
0..9          one digit -> stepping                counted = 10
10            gap 1 -> 0: diff 1 -> stepping       counted = 11
11            gap 1 -> 1: diff 0 -> rejected
12            gap 1 -> 2: diff 1 -> stepping       counted = 12
13..20        each has a gap with diff != 1 -> rejected
21            gap 2 -> 1: diff 1 -> stepping       counted = 13
```

The scan ends with `counted = 13`, the expected Output for Example 1. The telling rows are `11`, which fails because equal adjacent digits differ by 0, and `20`, whose gap `2 -> 0` differs by 2.

#### Solution

The code is the walkthrough's per-candidate digit test folded over the range:

```python
class Solution:
    def solve(self, low: int, high: int) -> int:
        """Count stepping numbers in the inclusive range [low, high].

        Time:  O((high - low + 1) * d) where d is the digit count of high:
            every integer in the range is tested once, and each test reads
            its d digits.
        Space: O(d) for the digit string of the candidate under test.
        """

        def is_stepping(value: int) -> bool:
            digits = str(value)
            return all(
                abs(int(digits[position]) - int(digits[position - 1])) == 1
                for position in range(1, len(digits))
            )

        return sum(1 for value in range(low, high + 1) if is_stepping(value))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O((high - low + 1) × d)`

Every integer in the range is visited once, and each visit reads all `d` digits of the candidate, where `d` is the digit count of `high`.

##### Space Complexity: `O(d)`

Only the decimal string of the current candidate is held at any moment.

#### Key Insights

- The one-digit rule needs no special case: a one-digit string has no adjacent pair, so the `all` over an empty sequence passes, and `0` through `9` are stepping numbers by construction.
- The approach is correct for any range but pays for scanning the whole interval, and the interval can hold astronomically more non-stepping numbers than stepping ones.
- This brute force is the baseline every later approach is measured against; on the stated constraint `high <= 10^15` the range itself can exceed any time budget, which is what motivates generating instead of scanning.

### BFS from Single Digits

#### Derivation

The brute force wastes its budget on the overwhelming majority of integers that are not stepping numbers at all: over `[0, 10^15]` only about `1.6 × 10^5` stepping numbers exist, yet the scan touches all `10^15` candidates. The repair flips generation into construction: a stepping number stays a stepping number when a valid successor digit (one more or one less than the current last digit) is appended, so every stepping number can be grown from a single digit by repeatedly appending `last_digit - 1` or `last_digit + 1`. Growing one digit at a time and counting the values that land inside `[low, high]` touches only genuine stepping numbers, and processing the numbers in nondecreasing digit count makes the generation a breadth-first search over a tree whose nodes are stepping numbers:

1. Count `0` when `low == 0`; `0` is a stepping number but has no children, so it
   lives outside the growth tree.
2. Seed a `queue` with the single digits `1` through `9`, counting each seed that
   is already `>= low` (every seed at most `high` is enqueued, because its
   descendants can still fall inside the range).
3. Pop `value`, read `last_digit = value % 10`, and for each `next_digit` in
   `(last_digit - 1, last_digit + 1)` that lies in `0..9`, form
   `next_value = value * 10 + next_digit`.
4. Skip `next_value` when it exceeds `high`: appending digits only grows the
   number, so the whole subtree under it is out of range and the prune is final.
5. Otherwise count `next_value` when `next_value >= low`, and enqueue it for
   growth; stop when the queue drains and return the count.

#### Walkthrough

Example 1, `low = 0`, `high = 21`. Seeding counts `0` plus the nine single digits, so the count opens at `10`. Each line below is one queue event; the two candidate extensions of a pop are written as `digit-1` then `digit+1`:

```text
seed 1..9     all <= 21 and >= 0 -> each counted      count = 10
pop 1  (1)    ext 0 -> 10 in range, count + enqueue   count = 11
              ext 2 -> 12 in range, count + enqueue   count = 12
pop 2  (2)    ext 1 -> 21 in range, count + enqueue   count = 13
              ext 3 -> 23 > 21 -> prune
pop 3..9      both extensions are 3x..9x > 21 -> pruned
pop 10 (0)    ext -1 rejected; ext 1 -> 101 > 21 -> pruned
pop 12 (2)    121 > 21, 123 > 21 -> pruned
pop 21 (1)    210 > 21, 212 > 21 -> pruned
pop 11 (1)    110 > 21, 112 > 21 -> pruned            queue empty
```

Exactly three two-digit numbers were born: `10`, `12`, `21`, matching the Explanation of Example 1, and the final count is `13`. Note `11` was never generated at all: no legal append turns a single digit into `11`.

#### Solution

The code is the seed-and-grow loop from the walkthrough, with the two prune conditions (`next_digit` outside `0..9`, `next_value` beyond `high`) guarding the enqueue:

```python
from collections import deque


class Solution:
    def solve(self, low: int, high: int) -> int:
        """Count stepping numbers in the inclusive range [low, high].

        Time:  O(s) where s is the number of stepping numbers <= high:
            every stepping number at most high is enqueued and popped once.
        Space: O(s) for the queue, which at worst holds one full
            digit-length layer of the growth tree.
        """
        stepping_count = 1 if low == 0 else 0
        queue = deque()
        for seed in range(1, 10):
            if seed > high:
                break
            if seed >= low:
                stepping_count += 1
            queue.append(seed)

        while queue:
            value = queue.popleft()
            last_digit = value % 10
            for next_digit in (last_digit - 1, last_digit + 1):
                if not 0 <= next_digit <= 9:
                    continue
                next_value = value * 10 + next_digit
                if next_value > high:
                    continue
                if next_value >= low:
                    stepping_count += 1
                queue.append(next_value)

        return stepping_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(s)`

Where `s` is the count of stepping numbers not exceeding `high`: each in-range-or-ancestor stepping number is enqueued and popped exactly once with a constant amount of work per pop. On the stated constraint `high = 10^15` this is about `1.6 × 10^5` events.

##### Space Complexity: `O(s)`

The queue can hold one entire digit-length layer of the growth tree, and the total across layers is bounded by the number of stepping numbers grown.

#### Key Insights

- Generating only valid stepping numbers replaces a scan of up to `10^15` candidates with roughly `10^5` construction steps: the interval length leaves the runtime entirely.
- Appending digits never shrinks a number, so `next_value > high` prunes the whole subtree in one test; there is no need to explore below a rejected node.
- Single digits smaller than `low` must still be enqueued: they sit below the range, but their longer descendants can climb back into it.
- `low` acts only as a counting filter, never as a prune at the bottom end: a parent smaller than `low` can still have in-range children.

### Digit DP with Tight Bounds

#### Derivation

The BFS still materializes every stepping number at most `high` before counting it, and the count itself is the runtime: fine at `10^15`, but the enumeration grows tenfold per extra digit while the digit string of `high` grows by one. The counting question can be answered without naming a single stepping number by reading the bound's digits left to right, the way [digit DP](https://en.wikipedia.org/wiki/Structural_induction) organizes counting problems: `count_up_to(limit)` returns how many stepping numbers lie in `[0, limit]`, and inclusion-exclusion (`count_up_to(high) - count_up_to(low - 1)`) turns the range count into two bound counts.

Each recursion position carries four facts: `position` in the digit string, the `previous_digit` the next digit must sit beside, a `started` flag telling whether a leading digit has been placed yet (while `False`, the number so far is `0`, which is itself a stepping number and may end at any position), and a `tight` flag telling whether every digit so far equals the bound's prefix (while `True`, the next digit is capped at the bound's own digit). The memo table collapses the states, and states, not paths, are what the runtime pays for:

1. Guard `limit < 0` by returning `0`, so `low = 0` asks for `count_up_to(-1)`.
2. Split the digits of `limit` into the list `digits`; recursion ends at
   `position == length` and contributes exactly `1` finished number.
3. While not `started`, two moves exist: leave the number at `0` (stay
   `started = False`, consume one position) or place a first digit `first_digit`
   from `1` up to the cap (`9`, or `digits[position]` under `tight`), which
   starts the number and becomes the first `previous_digit`.
4. Once `started`, only `previous_digit - 1` and `previous_digit + 1` within
   `0..9` and at most the cap may be appended; each move updates `tight` to
   `tight and candidate_digit == digits[position]`.
5. Return `count_up_to(high) - count_up_to(low - 1)`.

#### Walkthrough

Example 1, `low = 0`, `high = 21`, so the answer is `count_up_to(21) - count_up_to(-1)` and the second term is the `limit < 0` guard returning `0`. In `count_up_to(21)` the digits are `[2, 1]`, and the top-level call at `position = 0`, `started = False`, `tight = True` branches over the three legal moves at a first position:

```text
leading 0     stay not started -> recursively counts 0..9 in one
              unconstrained branch                          10 numbers
first 1 (< 2, now free)  any stepping continuation of length 2
              from previous 1: 10, 12                        2 numbers
first 2 (= 2, still tight) next digit capped at 1;
              previous 2 allows 1 or 3, cap admits 1 -> 21   1 number
                                                            ----
count_up_to(21) = 10 + 2 + 1 = 13
```

Every branch reaches `position = 2` and contributes its `1` at the base case, so the total is `13 - 0 = 13`, the expected Output. Example 2, `low = 10`, `high = 15`, exercises the subtraction: `count_up_to(15) = 12` (the ten one-digit numbers plus `10` and `12`), `count_up_to(9) = 10`, and `12 - 10 = 2`.

#### Solution

The code is the four-flag recursion from the derivation, wrapped in the `count_up_to` helper and closed by the subtraction:

```python
from typing import Dict, Tuple


class Solution:
    def solve(self, low: int, high: int) -> int:
        """Count stepping numbers in the inclusive range [low, high].

        Time:  O(d) where d is the digit count of high: the memo holds at
            most 40 * (d + 1) states (10 previous digits x 2 flags x 2
            flags per position) and each state costs constant work.
        Space: O(d) for the memo table and the recursion stack.
        """

        def count_up_to(limit: int) -> int:
            if limit < 0:
                return 0
            digits = [int(digit_char) for digit_char in str(limit)]
            length = len(digits)
            memo: Dict[Tuple[int, int, bool, bool], int] = {}

            def count_from(
                position: int, previous_digit: int, started: bool, tight: bool
            ) -> int:
                if position == length:
                    return 1
                state = (position, previous_digit, started, tight)
                if state in memo:
                    return memo[state]
                cap = digits[position] if tight else 9
                total = 0
                if started:
                    for candidate_digit in (previous_digit - 1, previous_digit + 1):
                        if 0 <= candidate_digit <= cap:
                            total += count_from(
                                position + 1,
                                candidate_digit,
                                True,
                                tight and candidate_digit == digits[position],
                            )
                else:
                    total += count_from(position + 1, 0, False, tight and cap == 0)
                    for first_digit in range(1, cap + 1):
                        total += count_from(
                            position + 1,
                            first_digit,
                            True,
                            tight and first_digit == digits[position],
                        )
                memo[state] = total
                return total

            return count_from(0, 0, False, True)

        return count_up_to(high) - count_up_to(low - 1)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(d)`

Where `d` is the digit count of `high`: each recursion state is a `(position, previous_digit, started, tight)` tuple, at most `40 × (d + 1)` of them, and each computes its total from at most ten constant-time branches once.

##### Space Complexity: `O(d)`

The memo holds one entry per visited state, linear in the digit count, and the recursion stacks one frame per position.

#### Key Insights

- Inclusion-exclusion over `count_up_to` is the standard bridge from "count in `[low, high]`" to "count from `0`", and the `limit < 0` guard absorbs the `low = 0` edge so `low - 1 = -1` never needs a digit string.
- The `started` flag is what lets `0` be counted exactly once: the never-started branch contributes one finished number per position, encoding that `0`, `0` followed by nothing, is a stepping number, while no positive number acquires a spurious leading zero.
- The `tight` flag is the only thing tying the count to the specific bound: once a placed digit falls below the cap, all later positions draw from the same unconstrained subproblem, which is exactly what the memo deduplicates.
- Enumeration grows tenfold per digit but this count grows by a constant factor: the DP scales to bounds of thousands of digits where both scanning and BFS are hopeless.

## Comparison of Solutions

### Time Complexity

- **Brute Force Enumeration**: `O((high - low + 1) × d)` - every integer in the range is visited and its `d` digits read.
- **BFS from Single Digits**: `O(s)` - only the `s` stepping numbers at most `high` are constructed, each enqueued once.
- **Digit DP with Tight Bounds**: `O(d)` - at most `40 × (d + 1)` memo states over the `d` digits of the bound.

### Space Complexity

- **Brute Force Enumeration**: `O(d)` - one candidate's digit string at a time.
- **BFS from Single Digits**: `O(s)` - the queue can hold a full digit-length layer of the growth tree.
- **Digit DP with Tight Bounds**: `O(d)` - the memo table plus the recursion stack.

### Trade-offs

- **Brute Force Enumeration**: impossible to get wrong and needs no insight into the structure, but its runtime is the interval length, which reaches `10^15` under the stated constraints.
- **BFS from Single Digits**: runtime proportional to the answer rather than the interval, and the same generation loop extends naturally to "list all stepping numbers" variants, but it still pays for each stepping number individually and its growth is exponential in the digit count.
- **Digit DP with Tight Bounds**: the only approach whose input is the digit count of the bound rather than the value, so it scales to enormous limits, at the cost of the most machinery: four flags, a memo, and inclusion-exclusion.

### When to Use Each

- **Brute Force Enumeration (Recommended for small ranges)**: when `high` is small enough to scan directly, this is the fastest correct thing to write and an easy baseline to test against.
- **BFS from Single Digits (Recommended for the stated constraints)**: the right interview answer for `high <= 10^15`: polynomial in the answer size, and the generation idea transfers to many "count numbers with a digit property" problems.
- **Digit DP with Tight Bounds**: when the bound grows past what enumerating the answer can afford, or when the problem asks only for the count and never the numbers themselves.

### Optimization Notes

- The BFS prune only needs `next_value > high`: there is no lower-bound prune, because `low` filters counting but never blocks growth.
- In the BFS, checking `0 <= next_digit <= 9` before forming `next_value` keeps a negative `last_digit - 1` from ever becoming a bogus child.
- The digit DP's memo key must include `tight`: ignoring it would merge constrained and unconstrained states and overcount, the classic digit DP bug.
- `count_up_to(low - 1)` with `low = 0` is why the `limit < 0` guard exists; raising on negative input instead would break the most common edge case.
