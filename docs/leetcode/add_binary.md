# [Add Binary](https://leetcode.com/problems/add-binary/)

**Easy** | **15 minutes** | **Math, String, Bit Manipulation**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Bitwise operation](https://en.wikipedia.org/wiki/Bitwise_operation)

**Practice:** [`practice/add_binary/solution.py`](../../practice/add_binary/solution.py)

Given two binary strings `a` and `b`, return their sum as a binary string.

## Examples

### Example 1

**Input:** `a = "11", b = "1"`

**Output:** `"100"`

### Example 2

**Input:** `a = "1010", b = "1011"`

**Output:** `"10101"`

## Constraints

- `1 <= a.length, b.length <= 10^4`
- `a` and `b` consist only of `'0'` or `'1'` characters.
- Each string does not contain leading zeros except for the zero itself.

## Deriving the Solution

Binary addition is column addition in base two: at each position the two bits plus the incoming carry form a `total`, whose parity (`total % 2`) is the output bit and whose half (`total // 2`) is the carry passed leftward. Every solution below is that one rule in different clothing.

1. **Start literal.** Walk both strings from their last characters with indices
   `i` and `j`, apply the column rule, collect bits in a list, and reverse once at the end. This is already linear, `O(max(n, m))`, the best any approach here achieves: see [Brute Force](#brute-force).
2. **Same loop, costlier bookkeeping.** Two common variants keep the identical
   column rule but build the result by prepending to a string, which copies the whole result on every iteration and silently turns the loop quadratic: padding the inputs to equal length first in [Bit-by-bit Computation](#bit-by-bit-computation), or tracking indices without padding in [Single-Loop Iterative Approach](#single-loop-iterative-approach).
3. **Push the carry into bitwise operators.** Treating each whole number at once,
   XOR is the carry-free sum and the shifted AND is exactly the carries; folding the carry back in until it vanishes adds without ever using `+`: see [Bit Manipulation](#bit-manipulation).
4. **Delegate everything.** Python can parse, add, and format on its own:
   `int(a, 2) + int(b, 2)` followed by `bin` hands the entire technique to the library: see [Using Built-in Functions](#using-built-in-functions).

## Solutions

### Brute Force

#### Derivation

The most intuitive idea is to mimic the column addition we learned for decimal numbers, only in base two. Starting from the rightmost bit of each string, we add the two digits plus any carry from the column to the right, write down the parity bit, and pass the carry leftward.

1. Set two indices `i` and `j` at the last character of `a` and `b`, and a `carry` of `0`.
2. Loop while either index is still in range or a carry remains. Each pass compares characters to `"1"` directly to add `0` or `1`, never converting the whole string to a number.
3. The current bit is `total % 2` and the next carry is `total // 2`, since `total` is at most `3`.
4. Bits are appended least-significant first, so reverse the collected list and join it into the result string.

#### Walkthrough

Let us watch the brute force run on Example 1: `a = "11"`, `b = "1"`, expected Output `"100"`.

We start with `i = 1` (last index of `a`), `j = 0` (last index of `b`), `carry = 0`, and an empty `result = []`. Each pass adds the in-range bits plus the carry into `total`, appends `total % 2` as the new bit, and keeps `total // 2` as the next `carry`.

| Step | bit `a[i]` | bit `b[j]` | `carry` in | `total` | appended bit | `carry` out | `result` after |
|------|------------|------------|------------|---------|--------------|-------------|----------------|
| 1 | `a[1]` = `1` | `b[0]` = `1` | `0` | `2` | `0` | `1` | `["0"]` |
| 2 | `a[0]` = `1` | none (`j` < 0) | `1` | `2` | `0` | `1` | `["0", "0"]` |
| 3 | none (`i` < 0) | none (`j` < 0) | `1` | `1` | `1` | `0` | `["0", "0", "1"]` |

After step 1, `i` drops to `0` and `j` drops to `-1`. After step 2, `i` drops to `-1`. By step 3 both indices are out of range, but `carry` is still `1`, so the loop runs once more to flush it: `total = 1`, which writes the final `1` bit and clears the carry to `0`. Now `i < 0`, `j < 0`, and `carry == 0`, so the loop stops.

The bits were collected least-significant first, so `result` holds `["0", "0", "1"]`. Reversing and joining gives `"100"`, which matches the expected Output `"100"`.

#### Solution

The code is the column loop from the walkthrough: one pass from the least significant bits, with the loop condition flushing any final carry.

```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        result = []

        # Walk both strings from the least significant bit, exactly like
        # adding by hand on paper. Treat a missing digit as 0.
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += 1 if a[i] == "1" else 0
                i -= 1
            if j >= 0:
                total += 1 if b[j] == "1" else 0
                j -= 1
            # total is 0, 1, 2, or 3: the bit is its parity, the carry its half
            result.append("1" if total % 2 == 1 else "0")
            carry = total // 2

        # Bits were collected least-significant first, so reverse them
        return "".join(reversed(result))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

Each loop iteration consumes one bit position from the longer string (plus at most one extra pass for a trailing carry), so the work is linear in the longer input.

##### Space Complexity: `O(max(n, m))`

The result list holds at most `max(n, m) + 1` bits before it is joined into the output string.

#### Key Insights

- Mirrors pencil-and-paper addition: add a column, write the parity, carry the rest.
- Compares characters directly against `"1"`, so it never leans on `int(s, 2)` or `bin()` to do the arithmetic.
- Appending to a list and reversing once at the end avoids the quadratic cost of repeated string prepending.

### Bit-by-bit Computation

#### Derivation

The brute force handles unequal lengths by testing each index inside the loop. This variant asks: what if the strings had equal lengths to begin with? Padding the shorter one with leading zeros makes every column hold two real bits, so the loop body needs no in-range tests and can walk a single index. The column rule is unchanged; what changes is the bookkeeping, and for the worse: each bit is prepended to the `result` string, which copies everything built so far on every iteration.

1. Pad `a` and `b` with leading zeros (`zfill`) to the longer length.
2. Walk `i` from the last index down to `0`; each column's `bit_sum` is
   `int(a[i]) + int(b[i]) + carry`.
3. Prepend `str(bit_sum % 2)` to `result` and keep `carry = bit_sum // 2`.
4. After the loop, prepend a final `'1'` if a carry remains.

#### Walkthrough

Let us run this variant on Example 1: `a = "11"`, `b = "1"`, expected Output `"100"`. The padding step brings both strings to length `2`, so `b` becomes `"01"`, and a single index `i` walks the columns right to left:

```text
padding   a = "11"   b = "01"                     b gains one leading zero
i = 1     bit_sum = 1 + 1 + 0 = 2                 result = "0"    carry = 1
i = 0     bit_sum = 1 + 0 + 1 = 2                 result = "00"   carry = 1
after     carry = 1 still set                     result = "100"
```

The loop ends with `carry = 1`, so the final `if carry` prepends the leading `'1'`. Note that each of those `result` updates copied the whole string built so far, which is the hidden quadratic cost. The returned string is `"100"`, matching the expected Output.

#### Solution

The code is the padded column loop from the walkthrough, prepending each bit to `result`.

```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        result = ""
        carry = 0

        # Make sure a and b have the same length by padding with zeros
        a = a.zfill(max(len(a), len(b)))
        b = b.zfill(max(len(a), len(b)))

        # Iterate from right to left
        for i in range(len(a) - 1, -1, -1):
            bit_sum = int(a[i]) + int(b[i]) + carry
            result = str(bit_sum % 2) + result
            carry = bit_sum // 2

        # Add the final carry if needed
        if carry:
            result = '1' + result

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m)^2)`

The loop visits each bit position once, but `result = str(bit_sum % 2) + result` copies the entire result string on every iteration. Prepending to a string of growing length `1, 2, ..., max(n, m)` sums to quadratic work overall. Collecting bits in a list and reversing once at the end (as the brute force does) would bring this down to `O(max(n, m))`.

##### Space Complexity: `O(max(n, m))`

We create a new string to store the result, which has at most max(n, m) + 1 bits.

#### Key Insights

- Simulates the binary addition process bit-by-bit
- Uses modulo operation to determine the current bit value
- Uses integer division to determine the carry bit

### Single-Loop Iterative Approach

#### Derivation

The padding variant spends a preliminary pass equalizing the strings and still needs a special case for the final carry. This version asks whether one loop can absorb both: keep separate indices `i` and `j`, read a bit as `0` once its index runs off the string, and let the loop condition `i >= 0 or j >= 0 or carry` run one extra pass to flush a trailing carry. The column rule is again unchanged, and so is the flaw it inherits: the result is still built by string prepending, so the loop remains quadratic.

1. Start `i` and `j` at the last characters of `a` and `b`, with `carry = 0`.
2. Loop while either index is in range or a carry remains; read `bit_a` and
   `bit_b` as `0` when their index is out of range.
3. Compute `current_sum = bit_a + bit_b + carry`, prepend `str(current_sum % 2)`
   to `result`, and set `carry = current_sum // 2`.
4. Decrement both indices; when both are exhausted, the carry term of the loop
   condition performs the final flush with no special case.

#### Walkthrough

Let us run this version on Example 2: `a = "1010"`, `b = "1011"`, expected Output `"10101"`. Both indices start at `3` and step left together:

```text
i=3  j=3    bit_a=0  bit_b=1  carry=0   current_sum=1   result = "1"      carry = 0
i=2  j=2    bit_a=1  bit_b=1  carry=0   current_sum=2   result = "01"     carry = 1
i=1  j=1    bit_a=0  bit_b=0  carry=1   current_sum=1   result = "101"    carry = 0
i=0  j=0    bit_a=1  bit_b=1  carry=0   current_sum=2   result = "0101"   carry = 1
i=-1 j=-1   bit_a=0  bit_b=0  carry=1   current_sum=1   result = "10101"  carry = 0
```

After the fourth pass both indices are exhausted, but `carry = 1` keeps the loop alive for one more pass, which reads both bits as `0` and writes the leading `1`. With `i < 0`, `j < 0`, and `carry == 0` the loop stops, returning `"10101"`, which matches the expected Output for Example 2.

#### Solution

The code is the trace written down: out-of-range bits read as `0`, and the carry keeps the loop alive for the final flush.

```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        result = ""
        carry = 0
        i, j = len(a) - 1, len(b) - 1

        # Process both strings until we reach the end of both
        while i >= 0 or j >= 0 or carry:
            # Get current bits (0 if we've reached the end of the string)
            bit_a = int(a[i]) if i >= 0 else 0
            bit_b = int(b[j]) if j >= 0 else 0

            # Compute sum and carry
            current_sum = bit_a + bit_b + carry
            result = str(current_sum % 2) + result
            carry = current_sum // 2

            # Move to the next bits
            i -= 1
            j -= 1

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m)^2)`

The single pass visits each bit position once, but `result = str(current_sum % 2) + result` rebuilds the result string on every iteration, so the total work is quadratic in the longer input. Appending to a list and reversing once at the end would restore the linear bound.

##### Space Complexity: `O(max(n, m))`

The space needed for the result string, which is at most max(n, m) + 1 bits.

#### Key Insights

- Handles both strings in a single loop
- Works efficiently for strings of different lengths
- Avoids unnecessary string padding or multiple loops

### Bit Manipulation

#### Derivation

Every version so far processes one column per iteration. This approach asks whether the columns can all be processed at once, using the classic carry-propagation loop built entirely from [bitwise operators](https://en.wikipedia.org/wiki/Bitwise_operation). The XOR of two values gives their sum at each bit position while ignoring any carries, and the AND of the two values (shifted left by one) gives exactly the carry bits. Folding the carry back in repeatedly, the carry eventually becomes zero and `x` holds the final sum.

Being honest about the boundaries: `int(a, 2)` and `bin(...)` are still used for input parsing and output formatting, so the I/O is not bitwise. The arithmetic itself, however, never uses `+`: every bit of the sum is produced purely with XOR, AND, and shift.

1. Parse `a` and `b` into integers `x` and `y` (I/O only; the addition never
   touches `+`).
2. While `y` is nonzero, compute `sum_without_carry = x ^ y` and
   `carry = (x & y) << 1`.
3. Replace `x` with `sum_without_carry` and `y` with `carry`; the pair's total is
   preserved while the carries move one position left.
4. When `y` reaches `0`, `x` holds the sum; format it with `bin(x)[2:]`.

#### Formula

Addition splits into a carry-free part and a carry part, each of which is a single bitwise operation:

$$ x \oplus y \quad=\quad \text{sum at each bit, carries ignored} $$

$$ (x \wedge y) \ll 1 \quad=\quad \text{the carries, shifted into their next position} $$

```text
sum_without_carry = x ^ y            the sum at each bit, carries ignored
carry             = (x & y) << 1     the carries, shifted into their next position
```

Together they preserve the total, which is what makes iterating valid:

$$ x + y \;=\; (x \oplus y) \;+\; \bigl((x \wedge y) \ll 1\bigr) $$

```text
x + y == (x ^ y) + ((x & y) << 1)
```

Each pass replaces \((x, y)\) with that right-hand pair, leaving the sum unchanged while pushing carries leftward. The process terminates because the carry term gains at least one trailing zero every round, so after at most \(\max(n, m) + 1\) passes it reaches \(y = 0\) and \(x\) holds the answer.

This is a [ripple-carry adder](https://en.wikipedia.org/wiki/Adder_(electronics)#Ripple-carry_adder) written in software: \(\oplus\) is the half-adder's sum bit and \(\wedge\) its carry bit.

#### Walkthrough

Let us fold the carries on Example 2: `a = "1010"`, `b = "1011"`, expected Output `"10101"`. Parsing gives `x = 10` and `y = 11`; the trace below shows each value in five binary digits, since the answer needs five bits:

```text
start     x = 01010 (10)    y = 01011 (11)
pass 1    sum_without_carry = 01010 ^ 01011 = 00001    bits where exactly one is set
          carry = (01010 & 01011) << 1
                = 01010 << 1 = 10100                   both-set bits, moved one left
          x = 00001 (1)     y = 10100 (20)
pass 2    sum_without_carry = 00001 ^ 10100 = 10101    no positions overlap
          carry = (00001 & 10100) << 1 = 00000         no bit set in both
          x = 10101 (21)    y = 00000 (0)
```

The invariant is visible at every line: `10 + 11 = 21` and `1 + 20 = 21`, so each pass preserves the total while the carry marches left. After the second pass `y = 0`, the loop exits, and `bin(21)[2:]` formats `x` as `"10101"`, matching the expected Output for Example 2.

#### Solution

The code is the fold from the walkthrough: XOR and shifted AND replace the pair until the carry dies out.

```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        # Parse the inputs into integers for the bitwise work
        x = int(a, 2)
        y = int(b, 2)

        # Add using only bitwise operations: XOR is the sum ignoring carries,
        # and (x & y) << 1 is the carry that must be propagated. Repeat until
        # there is no carry left to fold back in.
        while y:
            sum_without_carry = x ^ y
            carry = (x & y) << 1
            x = sum_without_carry
            y = carry

        # Strip the '0b' prefix to return the binary string
        return bin(x)[2:]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m)^2)` worst case

The loop can run up to max(n, m) + 1 times (a carry can ripple one position per pass, as in `0b111...1 + 1`), and each XOR, AND, and shift on Python's arbitrary-precision integers costs `O(max(n, m))` bit operations when the values span up to 10^4 bits. The worst case is therefore quadratic in the input length, even though typical inputs resolve in far fewer passes.

##### Space Complexity: `O(max(n, m))`

Only a constant number of integer variables are used, but each holds an arbitrary-precision integer of up to max(n, m) + 1 bits, and the output string is proportional to the input sizes as well.

#### Key Insights

- XOR computes the sum of two bits without their carry
- `(x & y) << 1` isolates and positions the carry for the next round
- The loop terminates because every pass pushes carries further left until they
  fall off entirely
- Demonstrates how addition can be expressed without the `+` operator

### Using Built-in Functions

#### Derivation

The last step is to delegate the whole task. Python already knows how to parse a binary string, add integers of any size, and format the result back, so the entire problem collapses into one expression. Nothing of the column rule remains visible; the library performs it internally.

1. `int(a, 2)` and `int(b, 2)` parse the strings positionally: each character
   contributes its bit times the matching power of two.
2. Native `+` adds the two integers into `sum_int`.
3. `bin(sum_int)` formats the sum with a `0b` prefix, which `[2:]` strips off.

#### Walkthrough

Here the built-ins are themselves the technique, so the trace opens them up on Example 1: `a = "11"`, `b = "1"`, expected Output `"100"`.

```text
int("11", 2)    1 * 2^1 + 1 * 2^0 = 3        positional parse of a
int("1", 2)     1 * 2^0 = 1                  positional parse of b
sum_int         3 + 1 = 4                    native integer addition
bin(4)          "0b100"                      binary formatting, prefixed
bin(4)[2:]      "100"                        prefix stripped
```

The returned string is `"100"`, matching the expected Output for Example 1.

#### Solution

```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        # Convert binary strings to integers, add them, then convert back to binary
        sum_int = int(a, 2) + int(b, 2)
        # Remove '0b' prefix from binary representation
        return bin(sum_int)[2:]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + m)`

Converting the strings to integers and back to binary takes linear time.

##### Space Complexity: `O(max(n, m))`

The parsed integers hold one bit per input character, and the output string is proportional to the input sizes, so the built-in conversion stores linear space like every other approach here.

#### Key Insights

- Takes advantage of Python's built-in conversion functions
- Very concise solution
- May not work for extremely large binary numbers due to potential integer overflow in some languages (but works in Python due to arbitrary precision integers)

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(max(n, m))` - One pass over the longer string, plus at most one carry pass; list append keeps each step `O(1)`
- **Bit-by-bit**: `O(max(n, m)^2)` - Single loop over padded strings, but string prepending copies the result on every iteration
- **Single-Loop**: `O(max(n, m)^2)` - One pass with index tracking, but the same string prepending makes each step linear in the result built so far
- **Bit Manipulation**: `O(max(n, m)^2)` worst case - Up to max(n, m) carry-propagation passes, each doing `O(max(n, m))`-bit integer operations
- **Built-in Functions**: `O(n + m)` - Linear time for conversion operations

### Space Complexity

- **Brute Force**: `O(max(n, m))` - Result list size
- **Bit-by-bit**: `O(max(n, m))` - Padded strings and result
- **Single-Loop**: `O(max(n, m))` - Result string only
- **Bit Manipulation**: `O(max(n, m))` - The arbitrary-precision integers hold one bit per input bit, plus the output string
- **Built-in Functions**: `O(max(n, m))` - The parsed arbitrary-precision integers hold one bit per input bit, plus the output string

### Trade-offs

- The brute force mirrors pencil-and-paper addition and stays library-free, comparing characters directly instead of parsing numbers; its list-append-then-reverse pattern is what keeps it linear
- The bit-by-bit computation is more uniform with padding but pays for the padding step and, more importantly, the quadratic cost of repeated string prepending
- The single-loop iterative approach drops the padding and the final reverse, but its string prepending makes it quadratic; converting it to list append would combine the best of both
- The bit manipulation approach expresses addition without the `+` operator, which is instructive, but it still relies on `int()`/`bin()` for parsing and formatting and is worst-case quadratic on huge inputs
- Using built-in functions is extremely concise but defers the entire core task to `int(a, 2)` and `bin()`, and may not work in languages without arbitrary precision integers

### When to Use Each

- **Brute Force**: When learning the problem, or when a library-free, from-scratch baseline is required; it is also the only from-scratch version here with a linear bound
- **Bit-by-bit Computation**: When a uniform approach with consistent string lengths is desired and inputs are small enough that the quadratic prepending does not matter
- **Single-Loop Iterative**: When readability matters more than the asymptotic bound; switch the result to a list to make it linear for large inputs
- **Bit Manipulation**: When demonstrating how addition reduces to XOR and carry shifts, or in settings that favor bitwise reasoning
- **Built-in Functions**: When code brevity is paramount and the language supports large integers

### Optimization Notes

- Only the brute force and built-in approaches are truly linear here; the two string-prepending versions and the bit-manipulation loop are quadratic in the worst case
- Replacing `result = bit + result` with `result.append(bit)` plus one final reverse-join is the single change that makes the bit-by-bit and single-loop versions linear
- The single-loop iterative approach demonstrates how to handle asymmetric inputs without padding
- The built-in approach leverages Python's arbitrary-precision integers but offloads the core arithmetic the problem is meant to teach
