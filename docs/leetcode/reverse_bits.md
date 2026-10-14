# [Reverse Bits](https://leetcode.com/problems/reverse-bits/)

**Easy** | **15 minutes** | **Divide and Conquer, Bit Manipulation**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Bitwise operation](https://en.wikipedia.org/wiki/Bitwise_operation) · [Divide-and-conquer bit swap](https://en.wikipedia.org/wiki/Hamming_weight)

**Practice:** [`practice/reverse_bits/solution.py`](../../practice/reverse_bits/solution.py)

Given a 32-bit unsigned integer `n`, reverse the bits of the binary representation of `n` and return the result.

## Examples

### Example 1

**Input:** `n = 00000000000000000000000000010101`

**Output:** `2818572288 (10101000000000000000000000000000)`

**Explanation:** Reversing `00000000000000000000000000010101`, which represents the unsigned integer `21`, gives us `10101000000000000000000000000000` which represents the unsigned integer `2818572288`.

## Constraints

<!-- Constraints not parseable from NeetCode for reverse_bits; fill them in. -->

## Constraints

- `0 <= n < 2^31`

## Deriving the Solution

Reversing 32 fixed positions is a simulation, and the only design question is how the bits travel from position `i` to position `31 - i`: one at a time in a loop, by index arithmetic, or in whole interleaved halves at once.

1. **Start literal.** Read `n`'s bits one by one from the right and append
   each to a result growing leftward; 32 passes move every bit to its mirror
   position. Correct and simple: see [Build-by-Shift Loop](#build-by-shift-loop).
2. **Address it directly.** The destination of bit `i` is `31 - i`, so the
   same result can be assembled positionally, `sum` over 32 masked reads:
   see [Positional Reconstruction](#positional-reconstruction).
3. **Swap halves instead of single bits.** Divide and conquer: swap the two
   16-bit halves, then the bytes inside each half, then nibbles, pairs, and
   single bits. Five fixed mask-and-shift rounds reverse everything with
   `O(log w)` operations instead of `O(w)`: see
   [Divide-and-Conquer Swap Folds](#divide-and-conquer-swap-folds).
4. **Or reverse the string.** Format `n` as a 32-character bit string,
   reverse it, and parse it back: see
   [String Round Trip](#string-round-trip).

## Solutions

### Build-by-Shift Loop

#### Derivation

The most direct simulation of "reverse the bits": consume `n` from its low end and grow the answer from its high end. Each pass peels `n`'s lowest bit and appends it to `result`'s right edge after pushing `result` one position left. Because 32 bits are consumed and 32 appends happen, bit `i` is appended on pass `i + 1`, after which it has been shifted left `31 - i` times: it lands exactly at its mirror position. The loop count is the width, 32, and no padding logic is needed because leading zeros are consumed like any other bit. The steps:

1. Initialize `result = 0`.
2. Repeat 32 times: shift `result` left one position, OR in `n & 1`,
   then shift `n` right one position.
3. Return `result`.

#### Walkthrough

Trace the loop on Example 1: `n = 21`, which in 32-bit form is `...00010101`, expected Output `2818572288`. The first five passes move all the set bits; the table shows `result` growing in its low positions while `n` erodes from the right:

```text
pass 1   bit = 1   result = 1           n >>= 1 -> ...01010
pass 2   bit = 0   result = 10          n >>= 1 -> ...00101
pass 3   bit = 1   result = 101         n >>= 1 -> ...00010
pass 4   bit = 0   result = 1010        n >>= 1 -> ...00001
pass 5   bit = 1   result = 10101       n >>= 1 -> ...00000
```

`n` is now zero, but 27 low-order zeros of the original still owe their mirrored high-order positions, so the loop keeps going: each of the remaining 27 passes appends a `0`, pushing `result`'s five set bits further left. After pass 32, `result` is `10101` followed by 27 zeros, which is `10101000000000000000000000000000` = `2818572288`, matching the expected Output for Example 1. The mirror arithmetic checks out on the first pass's bit: position `0` was appended first and has been shifted left 31 times, landing at position `31`.

#### Solution

The code is the walkthrough's append loop with the pass count pinned to the width.

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`, 32 iterations

Exactly one shift, one mask, one OR, and one shift per pass, 32 passes: constant work with a small constant. The loop cannot exit early, since trailing zeros must still be mirrored into leading ones of the answer.

##### Space Complexity: `O(1)`

The two working integers `result` and the eroding `n`.

#### Key Insights

- The simulation needs no positional arithmetic at all: consume low, append right, and the mirror placement is a byproduct of 32 fixed passes.
- The loop must run all 32 passes even after `n` hits zero, because the remaining zeros are bits too; this is the exact inverse of the single_number fold, where zeros could be skipped.
- `n & 1` then `n >>= 1` is the consume-one-bit idiom; its inverse, `result << 1 | bit`, is the append-one-bit idiom. The whole solution is those two idioms in a loop.

### Positional Reconstruction

#### Derivation

The Build-by-Shift Loop moves bits by traffic, appending and shifting. The alternative is addressing: bit `i`'s destination is fixed at position `31 - i`, so the answer is the sum of every source bit placed directly at its destination, `(n >> i) & 1` shifted left by `31 - i`. No result register evolves; the answer is one comprehension over the 32 positions. The steps:

1. For each source position `i` from `0` through `31`, read its bit with
   `(n >> i) & 1`.
2. Shift that bit left by `31 - i`, its destination.
3. Sum the 32 placed bits and return the total.

#### Walkthrough

Let us place the bits of Example 1 by address: `n = 21` = `10101` in the low five positions, expected Output `2818572288`. Only the set positions contribute nonzero terms:

```text
i=0   (21 >> 0) & 1 = 1   placed at 31 -> 1 << 31 = 2147483648
i=2   (21 >> 2) & 1 = 1   placed at 29 -> 1 << 29 =  536870912
i=4   (21 >> 4) & 1 = 1   placed at 27 -> 1 << 27 =  134217728
i=1,3 (bits 0)            contribute 0
remaining 27 positions           contribute 0
sum = 2147483648 + 536870912 + 134217728 = 2818572288
```

The bits of `21` at even positions `0, 2, 4` land at odd positions `31, 29, 27`, preserving their order but flipping their parity. The sum is `2818572288`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's addressed placement written as one sum.

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        return sum(((n >> i) & 1) << (31 - i) for i in range(32))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`, 32 iterations

Thirty-two constant-work terms: two shifts, two masks, and one addition each. The generator allocation makes the constant slightly larger than the loop version's.

##### Space Complexity: `O(1)`

The generator holds one term at a time; the sum accumulates in a single integer.

#### Key Insights

- Reads like the definition reversed: position `i` in, position `31 - i` out, no intermediate state.
- The mirror map `i -> 31 - i` is the only thing to get right; getting it backwards yields the identity, not the reversal, a bug the zero answer would never expose.
- Python's arbitrary-precision ints make the sum safe; in fixed-width languages the shifts are well-defined because every destination is below the width.

### Divide-and-Conquer Swap Folds

#### Derivation

The first two solutions pay one operation per bit. The divide-and-conquer formulation pays one round per halving level: swap the two 16-bit halves of the word, then swap the two bytes inside each 16-bit half, then the nibbles inside each byte, the bit pairs inside each nibble, and finally the bits inside each pair. After `log2(32) = 5` rounds every bit has crossed exactly the partners it needs to reach its mirror. Each round is two masks isolating the halves to move and two shifts moving them, which modern hardware does in a handful of instructions. The steps:

1. Swap 16-bit halves: `(n >> 16) | (n << 16)`, masked to 32 bits.
2. Swap bytes: `((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)`.
3. Swap nibbles: `((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)`.
4. Swap bit pairs: `((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)`.
5. Swap adjacent bits: `((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)`.
6. Return the accumulated value.

#### Walkthrough

Let us fold Example 1 down: `n = 21` = `0x00000015`, expected Output `2818572288`. Each round swaps halves at one scale, shown in hex with the bits that move underlined by their masks:

```text
n = 00000015
round 1 (16s)   0000 | 0015   ->  00150000
round 2 (8s)    00 | 15 | 00 | 00  ->  15000000
round 3 (4s)    1 | 5 | 0 | 0 | 0 | 0 | 0 | 0  ->  51000000
round 4 (2s)    0101 | 0001  pairs ->  0101 | 0100   =  54000000
round 5 (1s)    01 01 01 00  bits ->  10 10 10 00    =  A8000000
```

The set bits travel right to left across the word, one merge per scale: `15` crosses to the top as a byte, its nibbles reorder to `51`, round 4 leaves the self-mirrored `01` nibble alone while flipping `0001` to `0100` (`51` becomes `54`), and the final bit-level swap turns `01010100` into `10101000` (`54` becomes `A8`), which is `A8000000` = `2818572288`, matching the expected Output for Example 1. Five rounds, not thirty-two passes.

#### Solution

The code is the walkthrough's five fold rounds, each one mask-swap line.

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        n = (n >> 16) | (n << 16)
        n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
        n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
        n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
        n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)
        return n & 0xFFFFFFFF
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`, 5 rounds

Five rounds for 32 bits, `log2(32)` in general: each round is four or five bitwise operations regardless of the word's contents. The operation count grows logarithmically with the width, where the two loop solutions grow linearly.

##### Space Complexity: `O(1)`

The working integer is overwritten in place; the masks are compile-time constants.

#### Key Insights

- Reversal is the fixed point of halving swaps: swapping equal-sized chunks is reversible and, applied bottom-up, every pair of mirror positions ends up exchanged exactly once.
- The masks are the documentation: `0xAAAAAAAA` selects odd positions, `0x55555555` even ones, and their nested cousins (`0xCCCC...`/`0x3333...`, `0xF0F0...`/`0x0F0F...`, `0xFF00...`/`0x00FF...`) select the higher/lower member at each scale.
- The final `& 0xFFFFFFFF` exists for Python: its shifts never truncate, so the intermediate `n << 16` must be cut back to width. In fixed-width languages the overflow is free.

### String Round Trip

#### Derivation

The reversal can be delegated entirely to string operations: render `n` as a 32-character binary string with `format(n, "032b")`, reverse it with a slice, and parse it back with `int(..., 2)`. The width is enforced by the format spec, so leading zeros survive the trip, which is exactly what distinguishes this from `bin(n)`. The steps:

1. Format `n` zero-padded to 32 binary digits with `format(n, "032b")`.
2. Reverse the string with `[::-1]`.
3. Parse it back with `int(reversed_string, 2)`.

#### Walkthrough

Here the built-ins are the technique, so the trace opens them up on Example 1: `n = 21`, expected Output `2818572288`:

```text
format(21, "032b")    "00000000000000000000000000010101"   zero-padded to width 32
[::-1]                "10101000000000000000000000000000"   character reversal
int(..., 2)           2818572288                           positional parse
```

The padded format is what makes the round trip faithful: `bin(21)[2:]` alone would render `"10101"`, and reversing that loses the 27 leading zeros that must become trailing ones-scale zeros of the answer. The parsed value is `2818572288`, matching the expected Output for Example 1.

#### Solution

The code compresses the walkthrough's three steps into one expression.

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        return int(format(n, "032b")[::-1], 2)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`, bounded by 32 characters

Formatting, slicing, and parsing each touch a fixed 32-character string, with the work inside C-level string routines. The constant is the largest of the four solutions.

##### Space Complexity: `O(1)`, a 32-character string

Two transient 32-character strings: the padded rendering and its reversed copy.

#### Key Insights

- The width `032b` is load-bearing: without zero padding the reversal silently drops high-order zeros, the exact edge this problem tests.
- Clearest to audit bit by bit, which makes it the natural cross-check against the arithmetic versions in tests.
- `int(x, 2)` accepts at most one sign and the digit characters; the reversed string of a binary rendering is always parseable, so the round trip has no failure mode within the constraint.

## Comparison of Solutions

The practice harness's `practice/reverse_bits/reference.py` implements the **Build-by-Shift Loop** solution.

### Time Complexity

- **Build-by-Shift Loop**: `O(1)` - 32 fixed passes of constant bit work.
- **Positional Reconstruction**: `O(1)` - 32 addressed terms, generator overhead on top.
- **Divide-and-Conquer Swap Folds**: `O(1)` - 5 mask-swap rounds, `log` in the width.
- **String Round Trip**: `O(1)` - three C-level passes over a 32-character string.

### Space Complexity

- **Build-by-Shift Loop**: `O(1)` - two working integers.
- **Positional Reconstruction**: `O(1)` - one accumulator.
- **Divide-and-Conquer Swap Folds**: `O(1)` - the word overwritten in place.
- **String Round Trip**: `O(1)` - two transient 32-character strings.

### Trade-offs

- The Build-by-Shift Loop is the reference simulation: two bit idioms in a loop, the easiest to rederive under pressure, but linear in the width.
- The Positional Reconstruction trades the evolving state for one mirror formula, which reads cleanly but carries generator overhead.
- The Divide-and-Conquer Swap Folds reaches for the hardware answer: logarithmic rounds, constant-space in-place folding, at the price of five mask constants that need verifying once and trusting after.
- The String Round Trip is the audit tool: slowest and most allocation-heavy, but its intermediate state is human-readable.

### When to Use Each

- **Build-by-Shift Loop** (recommended): the default interview answer; it needs nothing memorized beyond the consume and append idioms, and the width is a parameter.
- **Positional Reconstruction**: when writing it as a one-line comprehension or cross-checking the loop in tests.
- **Divide-and-Conquer Swap Folds**: in performance-sensitive fixed-width code, where the round count beats any per-bit loop and the idiom is standard library fare in C and Java.
- **String Round Trip**: for tests, teaching, and debugging, where seeing the bit string is worth more than the cycles it costs.

### Optimization Notes

- Many architectures reverse bits in one instruction (`RBIT` on ARM); compiler intrinsics expose the divide-and-conquer pattern directly, and the swap-fold solution is the portable transcription of it.
- The swap-fold masks nest by halving (`FF00FF00 -> F0F0F0F0 -> CCCCCCCC -> AAAAAAAA`), which is the pattern to reconstruct if the constants are ever in doubt: at each scale, the high-half mask is the even/odd interleave of the scale above.
- Reversal is an involution: applying any of these solutions twice returns the original word, a property worth asserting in tests because it catches every mask typo at once.
- For word sizes other than 32, the loop and fold solutions adapt by one constant each (the pass count, the round count), while the string version's format width and the reconstruction's `31 - i` are the two spots that must move together.
