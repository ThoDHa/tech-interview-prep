# [Pow(x, n)](https://leetcode.com/problems/powx-n/)

**Medium** | **25 minutes** | **Math, Recursion**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Algorithm:** [Exponentiation by squaring](https://en.wikipedia.org/wiki/Exponentiation_by_squaring) · [Divide-and-conquer](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm) · [Binary exponentiation](https://en.wikipedia.org/wiki/Modular_exponentiation#Binary_method)

**Practice:** [`practice/powx_n/solution.py`](../../practice/powx_n/solution.py)

`Pow(x, n)` is a mathematical function to calculate the value of `x` raised to the power of `n` (i.e., `x^n`).

Given a floating-point value `x` and an integer value `n`, implement the `myPow(x, n)` function, which calculates `x` raised to the power `n`.

You may **not** use any built-in library functions.

## Examples

### Example 1

**Input:** `x = 2.00000, n = 5`

**Output:** `32.00000`

### Example 2

**Input:** `x = 1.10000, n = 10`

**Output:** `2.59374`

### Example 3

**Input:** `x = 2.00000, n = -3`

**Output:** `0.12500`

## Constraints

- `-100.0 < x < 100.0`
- `-2^31 <= n <= 2^31 - 1`
- `n` is an integer.
- Either `x` is not zero or `n > 0`.
- `-10^4 <= x^n <= 10^4`

## Deriving the Solution

Computing `x^n` naively multiplies `x` into an accumulator `n` times, but the exponent's binary structure makes most of that work redundant: `x^8` is `x^4` squared, which is `x^2` squared, which is `x` squared. Halving the exponent instead of decrementing it collapses a linear chain into a logarithmic one, and a negative exponent just inverts the positive power.

1. **Start literal.** Multiply `x` into a running product `n` times; handle
   `n < 0` by computing the positive power and returning its reciprocal.
   Correct, but `O(|n|)` multiplications with `|n|` up to `2^31`: see
   [Iterative Multiplication](#iterative-multiplication).
2. **Spot the redundancy.** The accumulator recomputes what squaring already
   knows: `x^n` is either `(x^(n/2))^2` or that times one extra `x`, so each
   question about `n` reduces to one about `n // 2`: see
   [Recursive Divide-and-Conquer](#recursive-divide-and-conquer).
3. **Flip the recursion.** The halving chain fills from the bottom anyway, so
   an iterative loop can consume the exponent's binary digits from the low
   end with a squaring per bit: see
   [Iterative Binary Exponentiation](#iterative-binary-exponentiation).

## Solutions

### Iterative Multiplication

#### Derivation

The definition on the tin: `x^n` is `x` multiplied by itself `n` times. The loop writes itself, and the negative case falls out of the identity `x^(-n) = 1 / x^n`:

1. Reduce `n = 0` immediately to `1.0` (the empty product).
2. For negative `n`, remember to invert: compute `x^|n|` and return
   `1 / result`.
3. Multiply a `result` accumulator by `x`, `|n|` times.

The constraint `|n| <= 2^31` is what disqualifies this: two billion iterations of float multiplication is minutes of runtime for a problem that hides the same answer behind 31 squarings.

#### Walkthrough

Multiply out Example 1: `x = 2.0`, `n = 5`. The accumulator takes one `x` per pass:

```text
start     result = 1.0
pass 1    result = 1.0 * 2.0 = 2.0
pass 2    result = 2.0 * 2.0 = 4.0
pass 3    result = 4.0 * 2.0 = 8.0
pass 4    result = 8.0 * 2.0 = 16.0
pass 5    result = 16.0 * 2.0 = 32.0
```

Five passes for exponent five, `result = 32.0`, matching the expected Output for Example 1. The same shape at `n = -3` would run three passes to `8.0` and return `1 / 8.0 = 0.125`, which is exactly Example 3's answer.

#### Solution

The code is the accumulator loop with the reciprocal wrapped around the negative case.

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0
        magnitude = abs(n)
        result = 1.0
        for _ in range(magnitude):
            result *= x
        return 1.0 / result if n < 0 else result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|n|)`

One floating-point multiplication per unit of exponent magnitude, up to `2^31` of them at the constraint cap.

##### Space Complexity: `O(1)`

One accumulator, no recursion, no tables.

#### Key Insights

- `x^0 = 1` is the empty product, which anchors every other approach's base case.
- `abs(n)` risks nothing here (no `-2^31` negation overflow in Python), but in fixed-width languages the negative bound needs the long-long dodge, a classic interview trap.
- Linear time in the exponent value is exponential time in the input's bit length: this is the waste the next solution attacks.

### Recursive Divide-and-Conquer

#### Derivation

Watch what the linear loop redoes: by the time it has computed `x^4`, it held `x^2` two passes ago and threw the information away. Squaring is the shortcut: `x^n = (x^(n/2))^2` when `n` is even, and `(x^(n/2))^2 * x` when `n` is odd, with `x^0 = 1` ending the halving. That is a recurrence with `n // 2` inside, so a recursion over it touches `O(log n)` exponents:

1. Base: `n == 0` returns `1.0`.
2. Recurse once on `half = myPow(x, n // 2)`; the integer division makes
   odd exponents round down, so `x^5` asks about `x^2`.
3. Even `n`: return `half * half`; odd `n`: return `half * half * x`.
4. Negative `n`: compute `myPow(x, -n)` and return its reciprocal.

#### Recurrence

Let `p(n)` be the power of `x` at exponent `n`, with `x` fixed:

$$ p(n) = \begin{cases} 1, & n = 0 \\[4pt] p(\lfloor n/2 \rfloor)^2, & n > 0,\ n \text{ even} \\[4pt] p(\lfloor n/2 \rfloor)^2 \cdot x, & n > 0,\ n \text{ odd} \end{cases} $$

```text
p(0) = 1
p(n) = p(n // 2) ** 2          for even n > 0
p(n) = p(n // 2) ** 2 * x      for odd n > 0
myPow(x, n) = p(|n|)           when n >= 0
myPow(x, n) = 1 / p(-n)        when n < 0
```

The base case is the empty product `1`; each level squares the half-exponent's result and multiplies one extra `x` exactly when the bit dropped by the floor division was a `1`. The answer is read from the top-level call, with the reciprocal carrying negative exponents.

#### Walkthrough

Unroll the recursion on Example 1: `x = 2.0`, `n = 5`. Each call first asks its half-exponent, then squares on the way back up:

```text
p(5)  wants p(2)^2 * x        odd, 5 // 2 = 2
  p(2)  wants p(1)^2          even, 2 // 2 = 1
    p(1)  wants p(0)^2 * x    odd, 1 // 2 = 0
      p(0) = 1.0              base case
    p(1) = 1.0^2 * 2.0 = 2.0
  p(2) = 2.0^2 = 4.0
p(5) = 4.0^2 * 2.0 = 32.0
```

Three calls plus the base case for exponent five, each contributing at most one extra multiplication of `x`: `p(5) = 32.0`, matching the expected Output for Example 1. The odd-step extra `x` factors are exactly the bits of `5 = 101b`.

#### Solution

The code is the recurrence transcribed: halve, square, conditionally multiply, invert for negative `n`.

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0
        if n < 0:
            return 1.0 / self.myPow(x, -n)

        half = self.myPow(x, n // 2)
        if n % 2 == 0:
            return half * half
        return half * half * x
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Each call halves the exponent, so the recursion depth is the bit length of `n` (at most `31` at the constraint cap) and each level does constant work.

##### Space Complexity: `O(log n)`

The call stack holds one frame per halving level; no memoization is needed because each exponent is asked exactly once down the chain.

#### Key Insights

- The single recursion into `n // 2` (not two into `n - 1`) is the whole win: it makes the call tree a chain of depth `log n` rather than a tree of size `n`.
- The odd-case extra `x` rebuilds the exponent from its binary digits, with the deepest call contributing the most significant bit.
- Python's big integers make `-n` safe at `n = -2^31`, where fixed-width languages must negate inside a wider type.

### Iterative Binary Exponentiation

#### Derivation

The recursion's chain is a straight line: `p(0)` builds `p(1)`, which builds `p(2)`, which builds `p(5)`. The same chain can be walked with a loop by consuming `n`'s binary digits from the low end, keeping the current squared base in a variable: `result` accumulates a factor of `base` exactly at the bit positions where `n` has a `1`, and `base` squares once per bit regardless:

1. Handle `n == 0` and negative `n` (reciprocal of the positive power) up
   front, as before.
2. Initialize `result = 1.0` and `base = x`.
3. While `n > 0`: if the low bit `n & 1` is `1`, multiply `result *= base`;
   then square `base *= base` and shift `n >>= 1`.
4. When `n` exhausts, `result` holds `x^n`: the squarings delivered
   `x^(2^k)` for every bit position `k`, and only the set bits contributed.

#### Walkthrough

Run the bit loop on Example 1: `x = 2.0`, `n = 5 = 101b`, so bit `0` and bit `2` are set:

```text
start       n = 101b = 5   result = 1.0    base = 2.0
bit 0 = 1   result = 2.0   base = 4.0      n >>= 1 -> 10b
bit 1 = 0   (skip)         base = 16.0     n >>= 1 -> 1b
bit 2 = 1   result = 32.0  base = 256.0    n >>= 1 -> 0b
n == 0      return result = 32.0
```

The skipped bit `1` left `result` untouched while `base` squared on through `4.0` to `16.0`, and the set bits `0` and `2` contributed `2.0` and `16.0`: their product `32.0` matches the expected Output for Example 1.

#### Solution

The code is the bit loop: test the low bit, accumulate, square, shift.

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0
        if n < 0:
            return 1.0 / self.myPow(x, -n)

        result = 1.0
        base = x
        while n > 0:
            if n & 1:
                result *= base
            base *= base
            n >>= 1
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

One loop iteration per bit of `n`, constant work per bit: at most `31` iterations at the constraint cap.

##### Space Complexity: `O(1)`

Two variables and no call stack, the recursion's log-depth frames flattened away.

#### Key Insights

- The loop reads `n` as its own binary representation: `result` ends up as the product of `x^(2^k)` over the set bits `k`, which is positional notation applied to multiplication.
- Squaring `base` unconditionally (even after the last bit) costs at most one wasted multiplication and keeps the loop branch-light.
- This is the production form: no stack, cache-friendly, and the same skeleton serves modular exponentiation by reducing `result` at each step.

## Comparison of Solutions

The practice harness's `practice/powx_n/reference.py` implements the **Iterative Binary Exponentiation** solution.

### Time Complexity

- **Iterative Multiplication**: `O(|n|)` - one multiplication per unit of exponent.
- **Recursive Divide-and-Conquer**: `O(log n)` - one call per halving level.
- **Iterative Binary Exponentiation**: `O(log n)` - one loop iteration per bit.

### Space Complexity

- **Iterative Multiplication**: `O(1)` - one accumulator.
- **Recursive Divide-and-Conquer**: `O(log n)` - one stack frame per halving level.
- **Iterative Binary Exponentiation**: `O(1)` - two variables, no stack.

### Trade-offs

- **Iterative Multiplication**: Trivial to trust but hopeless at the constraint cap of `|n| = 2^31`, where it needs two billion multiplications.
- **Recursive Divide-and-Conquer**: The recurrence reads directly off the halving insight, at the price of log-depth stack frames.
- **Iterative Binary Exponentiation**: Constant space and no recursion, with the bit loop's mechanics slightly less self-evident than the recurrence.

### When to Use Each

- **Iterative Multiplication**: Only as the baseline that motivates everything else, or when `n` is provably tiny.
- **Recursive Divide-and-Conquer**: When clarity of the halving argument matters most, or as the derivation from which the iterative form is reached.
- **Iterative Binary Exponentiation** (recommended): The default; logarithmic time, constant space, and the form that generalizes to modular arithmetic.

### Optimization Notes

- Exponentiation by squaring is optimal up to constants for a single power: the bit length of `n` bounds the number of multiplications any method that only squares and multiplies can achieve.
- The negative branch's reciprocal is where precision lives: `x^(-n)` computed as `1 / x^n` doubles the rounding relative to a directly negative-aware loop, which is invisible at this problem's tolerance but matters in numerically sensitive code.
- The identity powering this file, `x^(2k) = (x^k)^2`, is the same halving that drives fast Fibonacci (matrix power) and modular exponentiation; learning it once covers the family.

