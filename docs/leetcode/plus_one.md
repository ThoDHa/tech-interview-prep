# [Plus One](https://leetcode.com/problems/plus-one/)

**Easy** | **15 minutes** | **Array, Math**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Carry (arithmetic)](https://en.wikipedia.org/wiki/Carry_(arithmetic)) · [Positional notation](https://en.wikipedia.org/wiki/Positional_notation)

**Practice:** [`practice/plus_one/solution.py`](../../practice/plus_one/solution.py)

You are given an integer array `digits`, where each `digits[i]` is the `ith` digit of a large integer. It is ordered from most significant to least significant digit, and it will not contain any leading zero.

Return the digits of the given integer after incrementing it by one.

## Examples

### Example 1

**Input:** `digits = [1,2,3,4]`

**Output:** `[1,2,3,5]`

### Example 2

**Input:** `digits = [9,9,9]`

**Output:** `[1,0,0,0]`

## Constraints

- `1 <= digits.length <= 100`
- `0 <= digits[i] <= 9`

## Deriving the Solution

Adding one touches only the trailing run of nines: digits after it are untouched, digits inside it roll `9 -> 0`, and the first non-nine either absorbs the carry by incrementing or, if every digit is a nine, a new `1` is prepended. So the problem is one ripple of carry logic, and the approaches differ in how far they let the ripple run and what they allocate for it.

1. **Start literal.** Convert the digits to an integer, add one, convert back:
   two passes and one big temporary, exactly what the problem's framing
   about "large" integers warns about: see
   [Integer Round-Trip](#integer-round-trip).
2. **Do the schoolbook step.** Walk from the least significant digit, add the
   carry in place, stop at the first digit that does not roll over: see
   [Right-to-Left Carry Ripple](#right-to-left-carry-ripple).
3. **Exploit the +1 shape.** The carry is always `1` and the walk cannot stop
   except at a non-nine or the front, so the loop collapses to "flip the
   trailing nines, increment the next digit, else prepend": see
   [Trailing-Nines Scan](#trailing-nines-scan).

## Solutions

### Integer Round-Trip

#### Derivation

The most literal reading outsources the arithmetic: the digit array is a positional number, Python's `int` is unlimited-precision, so convert, add, and convert back:

1. Fold the digits into an integer: `value = value * 10 + digit` left to
   right.
2. Add one.
3. Unfold with `divmod(value, 10)` right to left, reversing at the end.

The statement's note that the array models a "large integer" is a hint against this shape: the conversion is the work the problem wants done by hand, and the temporary integer is as long as the number itself.

#### Walkthrough

Round-trip Example 2: `digits = [9, 9, 9]`.

```text
fold      9 -> 99 -> 999           value = 999
add one   999 + 1 = 1000
unfold    1000 % 10 = 0, 100 -> 0, 10 -> 0, 1 -> 1, 0
reverse   [0, 0, 0, 1] -> [1, 0, 0, 0]
```

The unfold peels `1000` into digits `0, 0, 0, 1` least-significant first, and the final reverse restores most-significant-first order: `[1, 0, 0, 0]`, matching the expected Output for Example 2.

#### Solution

The code is the fold, the increment, and the unfold of the walkthrough.

```python
from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        value = 0
        for digit in digits:
            value = value * 10 + digit
        value += 1
        out = []
        while value > 0:
            value, digit = divmod(value, 10)
            out.append(digit)
        out.reverse()
        return out
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Constant work per digit in the fold and the unfold; the hidden cost is that each big-integer operation itself touches all `n` digits.

##### Space Complexity: `O(n)`

The temporary integer holds `n` digits, and the output list holds `n + 1` in the all-nines case.

#### Key Insights

- The round-trip is correct and short, but it solves a different problem, "add one to an integer", rather than the one posed, "increment a digit array".
- The all-nines case is the round-trip's free lunch: `999 + 1 = 1000` just works, which is where hand-rolled versions must decide to prepend.
- Languages without arbitrary-precision integers bar this approach outright, which is the honest framing of its portability trade.

### Right-to-Left Carry Ripple

#### Derivation

The schoolbook view adds two numbers column by column, and adding one means the second addend is a single `1` at the units position with carry zero everywhere else. So walk from the least significant digit, add the carry, and write back; the carry starts at `1` and survives only while digits keep rolling over:

1. Index `i` from the last digit down to `0`.
2. If `digits[i] < 9`, increment it in place and return the array: the carry
   is absorbed, no digit to the left changes.
3. Otherwise set `digits[i] = 0` and carry the `1` leftward.
4. If the loop exhausts the array, every digit rolled over: prepend a `1`
   (the result list grows by one, `100...0`).

#### Walkthrough

Ripple through Example 1: `digits = [1, 2, 3, 4]`, then through Example 2's all-nines:

```text
[1,2,3,4]   i = 3: 4 < 9 -> digits[3] = 5, return [1,2,3,5]
[9,9,9]     i = 2: 9 -> set 0, carry   [9,9,0]
            i = 1: 9 -> set 0, carry   [9,0,0]
            i = 0: 9 -> set 0, carry   [0,0,0]
            loop done -> prepend 1     [1,0,0,0]
```

The mixed case stops at the first non-nine, leaving every digit to its left untouched, `[1,2,3,5]` matching the expected Output for Example 1. The all-nines case rolls the whole array to zeros and prepends the final carry, `[1,0,0,0]` matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's ripple with the prepend as the fall-through.

```python
from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                # Carry absorbed here: nothing to the left changes
                digits[i] += 1
                return digits
            digits[i] = 0
        return [1] + digits
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The ripple stops at the first non-nine, so typical inputs cost a single write; the all-nines worst case rewrites every digit once.

##### Space Complexity: `O(1)`

The input array is mutated in place; the all-nines return allocates one new list with `n + 1` entries, which is the required output rather than scratch.

#### Key Insights

- The early return inside the loop is the carry logic: a digit below `9` absorbs the carry, and everything to its left is provably unchanged.
- `9 -> 0` is the only rollover possible when adding one, which is why the loop body has just two cases.
- The prepend `[1] + digits` runs only when every digit was nine, the single case where the result outgrows the input.

### Trailing-Nines Scan

#### Derivation

The ripple's carry variable is constant (`1`) and its loop exits in exactly two ways, so the control flow can be read backwards from the outcome: the result equals the input with every trailing `9` flipped to `0`, plus either an increment of the next digit or a prepended `1` when no next digit exists. Count the trailing nines first, then emit:

1. Scan `nine_run` from the end while digits equal `9`.
2. If the run covers the whole array, the answer is `1` followed by all
   zeros: return `[1] + [0] * n`.
3. Otherwise copy the input, flip the run's digits to `0`, increment the
   digit just left of the run, and return.

The copy keeps the method pure (the input list survives), a deliberate contrast with the ripple's in-place mutation.

#### Walkthrough

Scan Example 1: `digits = [1, 2, 3, 4]`, and a nine-rich case `[2, 9, 9, 9]` to show the run boundary doing the work:

```text
[1,2,3,4]   nine_run = 0 (last digit 4)
            copy [1,2,3,4], increment index 3 -> [1,2,3,5]
[2,9,9,9]   nine_run = 3 (indices 3, 2, 1 are 9)
            copy, flip indices 1..3 to 0, increment index 0
            -> [3,0,0,0]
```

The mixed case's run stops at index `1`, so index `0` absorbs the increment and the tail zeros: `[1,2,3,5]` matches the expected Output for Example 1. The nine-rich case shows the whole run flipping at once around the increment at the front.

#### Solution

The code is the scan, the early all-nines return, and the flip-plus-increment.

```python
from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        n = len(digits)
        nine_run = 0
        while nine_run < n and digits[n - 1 - nine_run] == 9:
            nine_run += 1
        if nine_run == n:
            # Every digit rolled: 99...9 + 1 = 100...0
            return [1] + [0] * n
        out = digits[:]
        for i in range(n - nine_run, n):
            out[i] = 0
        out[n - nine_run - 1] += 1
        return out
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The scan touches the trailing run plus one digit, the copy and flips are linear; the all-nines return builds one list of `n + 1` zeros.

##### Space Complexity: `O(n)`

The copied output list; the input is left unmodified, which is the trade this version makes against the ripple's in-place write.

#### Key Insights

- Adding one is fully characterized by the trailing run of nines: everything left of the run either absorbs the carry or the run was the whole array.
- The pure (non-mutating) variant costs an `O(n)` copy that the ripple avoids, a real trade when callers expect their list untouched versus expect in-place efficiency.
- `[0] * n` builds the all-nines answer in one expression because that case's shape is fully known before any digit is emitted.

## Comparison of Solutions

The practice harness's `practice/plus_one/reference.py` implements the **Right-to-Left Carry Ripple** solution.

### Time Complexity

- **Integer Round-Trip**: `O(n)` - one fold pass, one increment, one unfold pass.
- **Right-to-Left Carry Ripple**: `O(n)` - stops at the first non-nine, worst case one pass.
- **Trailing-Nines Scan**: `O(n)` - one run scan plus a copy and flips.

### Space Complexity

- **Integer Round-Trip**: `O(n)` - the big temporary integer plus the output.
- **Right-to-Left Carry Ripple**: `O(1)` - mutates the input; the all-nines return is the output itself.
- **Trailing-Nines Scan**: `O(n)` - the copied output list keeps the input intact.

### Trade-offs

- **Integer Round-Trip**: The shortest correct code, but it dodges the exercise's digit-level intent and leans on arbitrary-precision integers.
- **Right-to-Left Carry Ripple**: Minimal memory and an early exit for typical inputs, at the price of mutating the caller's list.
- **Trailing-Nines Scan**: Pure output with the input preserved, paying an explicit copy for the guarantee.

### When to Use Each

- **Integer Round-Trip**: Prototyping or cross-checking in a language with big integers; never the interview answer.
- **Right-to-Left Carry Ripple** (recommended): The default; the schoolbook step done exactly once, in place, with an immediate exit on the common path.
- **Trailing-Nines Scan**: When the API contract requires a fresh list and the input must survive the call.

### Optimization Notes

- The ripple's average case is `O(1)`: a uniformly random digit is a nine with probability one tenth, so the expected run length is about `1/0.9`, barely more than one write.
- The all-nines prepend is the only allocation beyond the input; every other path returns the mutated input, which callers relying on identity can detect, so document the mutation or pick the scan.
- The same ripple answers "add any single digit `d`" with the rollover test generalized to `digit + carry >= 10`; adding arbitrary addends reintroduces a per-column carry loop.

