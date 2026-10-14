# [Reverse Integer](https://leetcode.com/problems/reverse-integer/)

**Medium** | **25 minutes** | **Math**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Integer overflow](https://en.wikipedia.org/wiki/Integer_overflow) · [Two's complement](https://en.wikipedia.org/wiki/Two%27s_complement) · [Modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic)

**Practice:** [`practice/reverse_integer/solution.py`](../../practice/reverse_integer/solution.py)

You are given a signed 32-bit integer `x`.

Return `x` after reversing each of its digits. After reversing, if `x` goes outside the signed 32-bit integer range `[-2^31, 2^31 - 1]`, then return `0` instead.

Solve the problem without using integers that are outside the signed 32-bit integer range.

## Examples

### Example 1

**Input:** `x = 1234`

**Output:** `4321`

### Example 2

**Input:** `x = -1234`

**Output:** `-4321`

### Example 3

**Input:** `x = 1234236467`

**Output:** `0`

## Constraints

- `-2^31 <= x <= 2^31 - 1`

## Deriving the Solution

Reversing decimal digits is easy; the problem is the fence around the answer. The reversal of an in-range input can leave the 32-bit range, and the fence must be checked without ever building the out-of-range value the statement forbids. Every solution below reverses the digits and then faces the same question: detect the overflow before or after it happens.

1. **Start literal.** Peel digits with modulo and push them onto a running
   result; after the loop, check whether the result still fits. Simple, but
   the check runs after the out-of-range value already existed, which the
   statement's "without using integers outside the range" forbids: see
   [Pop and Push](#pop-and-push).
2. **Reverse the characters instead.** The digits are already written down in
   `str(x)`; reverse the string, parse it back, and apply the same
   after-the-fact range check: see
   [String Round Trip](#string-round-trip).
3. **Check before the push.** The overflow question is decidable one step
   early: if the running result already exceeds `INT_MAX // 10`, the next
   push must overflow; if it equals `INT_MAX // 10`, only the final digit
   `8` or `9` can. Bailing at that instant keeps every intermediate value
   in range: see
   [Pop-and-Push with Pre-Check](#pop-and-push-with-pre-check).

## Solutions

### Pop and Push

#### Derivation

The most direct digit reversal treats the integer as a stack of decimal digits: pop the last digit with `x % 10`, push it onto the result with `rev = rev * 10 + digit`, and repeat until `x` is empty. The sign is carried alongside and reapplied at the end, and the overflow check runs once the reversal is complete. The steps:

1. Split the sign off: `sign = -1 if x < 0 else 1`, and work with
   `n = abs(x)`.
2. While `n` is nonzero: pop `digit = n % 10`, drop it with `n //= 10`, and
   push with `rev = rev * 10 + digit`.
3. Multiply by `sign`; return the product when it fits in the signed 32-bit
   range, else `0`.

#### Walkthrough

Let us pop and push Example 1: `x = 1234`, expected Output `4321`:

```text
pop 4   n = 123   rev = 0 * 10 + 4    = 4
pop 3   n = 12    rev = 4 * 10 + 3    = 43
pop 2   n = 1     rev = 43 * 10 + 2   = 432
pop 1   n = 0     rev = 432 * 10 + 1  = 4321
```

Each push appends the newest digit at the ones place, so the first digit popped ends up deepest: `4321`, matching the expected Output for Example 1. Example 2 rides the same loop on `n = 1234` and reattaches the sign, returning `-4321`. Example 3 is where the deferred check fires: the reversal builds `7646324321`, which leaves the 32-bit range, and the final check returns `0` instead.

#### Solution

The code is the walkthrough's pop-push cycle with the range check at the exit.

```python
class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        n = -x if x < 0 else x
        rev = 0
        while n:
            rev = rev * 10 + n % 10
            n //= 10
        rev *= sign
        return rev if -2**31 <= rev <= 2**31 - 1 else 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log |x|)`

One constant step per decimal digit; `|x| < 2^31` has at most 10 digits, so the loop runs at most 10 passes.

##### Space Complexity: `O(1)`

The sign flag and the two working integers.

#### Key Insights

- The pop-push pair is decimal bookkeeping: `n % 10` reads the last digit, `n //= 10` erases it, and `rev * 10 + digit` appends it.
- Python never overflows, so the check is honest here; in C or Java this version is already broken, because `rev` wraps around before the check can run.
- The statement's "without using integers outside the 32-bit range" is what disqualifies this version as a final answer and motivates the pre-check.

### String Round Trip

#### Derivation

The digits are already characters, so the reversal can be delegated to slicing: `str(x)` renders the number, `[::-1]` reverses the digit order, `int(...)` parses it back, and the sign reattaches. The range check stays after the fact, exactly as in Pop and Push. The steps:

1. Split the sign and render `abs(x)` with `str`.
2. Reverse the digit string with `[::-1]` and parse it with `int`.
3. Reapply the sign and return the product when it fits, else `0`.

#### Walkthrough

Here the built-ins are the technique, so the trace opens them up on Example 3: `x = 1234236467`, expected Output `0`:

```text
str(1234236467)      "1234236467"
[::-1]               "7646324321"
int("7646324321")    7646324321
fits in [-2^31, 2^31 - 1]?   no   -> return 0
```

The parse builds the ten-digit value, the range test sees it above `2^31 - 1 = 2147483647`, and the function returns `0`, matching the expected Output for Example 3. Example 1 runs the identical path to `"4321"`, parses to `4321`, passes the range test, and returns `4321`.

#### Solution

The code compresses the walkthrough's render, reverse, and parse into one expression.

```python
class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        rev = sign * int(str(abs(x))[::-1])
        return rev if -2**31 <= rev <= 2**31 - 1 else 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log |x|)`

Rendering, slicing, and parsing each touch at most 10 characters; the count is the digit count of `x`, with the work inside C-level string routines.

##### Space Complexity: `O(log |x|)`

Two transient strings of at most 10 characters each; still constant under the fixed 32-bit constraint, but no longer a pair of scalars.

#### Key Insights

- The shortest expression of the idea: the reversal is a string operation wearing an integer problem's clothes.
- Same deferred-check flaw as Pop and Push, so it shares the disqualification under the statement's no-overflow-intermediates rule.
- Sign handling is the only subtlety: reversing `"-1234"` as a string would put the minus at the end, so the sign must split off before the slice.

### Pop-and-Push with Pre-Check

#### Derivation

Both previous versions answer the overflow question one step too late. The fix is arithmetic foresight: the push `rev * 10 + digit` exceeds `INT_MAX` exactly when `rev > INT_MAX // 10`, or when `rev == INT_MAX // 10` and `digit > 7` (the last digit of `INT_MAX = 2147483647`). Because the sign is carried separately, the push always builds toward the positive maximum, so one comparison pair guards every push, and no out-of-range value ever exists. The steps:

1. Split the sign off and work with `n = abs(x)`; set `rev = 0`.
2. While `n` is nonzero: pop `digit = n % 10` and drop it from `n`.
3. If `rev > INT_MAX // 10`, or `rev == INT_MAX // 10` and `digit > 7`,
   return `0` immediately.
4. Push with `rev = rev * 10 + digit`; after the loop, return
   `sign * rev`.

#### Walkthrough

Let us pre-check Example 3: `x = 1234236467`, expected Output `0`. Each row is one loop pass, with the guard comparing `rev` against `INT_MAX // 10 = 214748364`:

```text
steps 1-9   rev climbs 7 -> 76 -> 764 -> ... -> 76463243 -> 764632432   all <= 214748364
step 10     rev = 764632432 > 214748364   -> overflow, return 0
```

The tenth pass is the first where the push would have crossed the line: `764632432 * 10 + 1 = 7646324321`, far past `INT_MAX`. The guard fires before that multiplication runs, so the function returns `0` without ever holding an out-of-range value, matching the expected Output for Example 3. The guard's equality branch is just as load-bearing: on `x = 1463847412` the ninth pass leaves `rev = 214748364`, and the last digit `1` passes the `digit > 7` test, so the push lands exactly on `2147483641`, the largest reversal that still fits, and the function returns it rather than `0`.

#### Solution

The code is the walkthrough's guarded push: one comparison pair before each append.

```python
class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        n = -x if x < 0 else x
        rev = 0
        while n:
            digit = n % 10
            n //= 10
            if rev > 214748364 or (rev == 214748364 and digit > 7):
                return 0
            rev = rev * 10 + digit
        return sign * rev
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log |x|)`

One comparison pair and one push per digit, at most 10 digits within the 32-bit constraint. The guard can end the loop early.

##### Space Complexity: `O(1)`

The sign flag and the two working integers.

#### Key Insights

- Checking before the push is what makes the solution statement-conformant: no intermediate ever leaves the 32-bit range, which is the sentence the problem adds beneath the overflow rule.
- The constant `214748364` is `INT_MAX // 10`, and the `7` is `INT_MAX % 10`: the guard compares the push against the maximum digit by digit. Positive and negative bounds differ in their last digit (`7` versus `8`), but since the reversal of a negative input is checked against `2^31 = 2147483648`'s prefix `214748364` too, the shared guard is safe: a negative reversal overflowing by exactly the last digit would need `rev == 214748364` with `digit == 8`, which corresponds to `-2147483648`, itself in range and reachable only from an out-of-range input.
- Python's big integers make the deferred check harmless in practice, so the pre-check is about honoring the statement's discipline; in C or Java it is the difference between working code and undefined behavior.

## Comparison of Solutions

The practice harness's `practice/reverse_integer/reference.py` implements the **Pop-and-Push with Pre-Check** solution.

### Time Complexity

- **Pop and Push**: `O(log |x|)` - one pass over the digits, check at the exit.
- **String Round Trip**: `O(log |x|)` - render, slice, and parse over the digit string.
- **Pop-and-Push with Pre-Check**: `O(log |x|)` - the same pass with a guard that can exit early.

### Space Complexity

- **Pop and Push**: `O(1)` - two working integers and a sign flag.
- **String Round Trip**: `O(log |x|)` - two transient digit strings.
- **Pop-and-Push with Pre-Check**: `O(1)` - the same scalars as Pop and Push.

### Trade-offs

- Pop and Push is the cleanest statement of the digit mechanics and the wrong final answer: its check runs after the forbidden value exists.
- The String Round Trip is the fewest characters of code and the most allocation; it defers the check exactly like Pop and Push.
- The Pre-Check version costs one comparison per digit to move the check before the push, buying statement conformance and, in fixed-width languages, defined behavior.

### When to Use Each

- **Pop and Push**: when teaching the pop/push mechanics, or in a language where the deferred check is still well-defined and the statement's discipline is not enforced.
- **String Round Trip**: as the concise cross-check in tests, or when string manipulation is already in play.
- **Pop-and-Push with Pre-Check** (recommended): the canonical submission; it is the only version whose intermediates never leave the signed 32-bit range.

### Optimization Notes

- The pre-check's magic constants decompose as `INT_MAX // 10 = 214748364` and `INT_MAX % 10 = 7`; in a typed language name them, so the guard reads as the arithmetic it performs.
- The negative bound needs no separate guard: `|INT_MIN| = INT_MAX + 1` differs only in its last digit, and an input whose reversal would reach `-2147483648` exactly cannot occur for in-range inputs, so the shared positive-side check never misclassifies a negative case.
- Reversal preserves digit count except for trailing zeros: `1200` reverses to `21`, not `0021`, which the pop-push loop handles for free because leading zeros never get pushed.
- In C++/Java the same guard is written `if (rev > (INT_MAX - digit) / 10) return 0;`, folding both branches into one division; the two-branch form above is the more inspectable equivalent.
