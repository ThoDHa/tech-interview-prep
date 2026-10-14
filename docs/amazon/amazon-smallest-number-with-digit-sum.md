# [Smallest Number With a Given Digit Sum](https://www.fastprep.io/problems/amazon-smallest-number-with-digit-sum)

**Medium** | **NN minutes** | **Greedy, Math, String**

Given integers digitSum and numberOfDigits, construct the smallest non-negative decimal number that:

has exactly numberOfDigits digits, andhas digits whose sum is exactly digitSum.Return the number as a string. The first digit cannot be zero unless numberOfDigits is 1. The input is guaranteed to admit at least one valid number.

## Examples

### Example 1

**Input:** `digitSum = 20`, `numberOfDigits = 3`

**Output:** `"299"`

**Explanation:** The smallest three-digit number with digit sum 20 is 299. Any smaller hundreds digit would leave more than 18 for the final two digits.

### Example 2

**Input:** `digitSum = 1`, `numberOfDigits = 4`

**Output:** `"1000"`

**Explanation:** The leading digit must be nonzero, so 1000 is the smallest four-digit number with digit sum 1.

## Constraints

- `1 <= numberOfDigits.`
- `0 <= digitSum <= 9 * numberOfDigits.`
- `If numberOfDigits is greater than 1, then digitSum is positive.`
- `The returned string has exactly numberOfDigits characters and no leading zero.`

## Solutions

### Candidate Enumeration

#### Derivation

The most literal reading of the problem: try every non-negative integer in increasing order and return the first one that satisfies both conditions, having exactly `numberOfDigits` digits and a digit sum of `digitSum`. Numbers never grow a digit count in mid-range, and the first match in increasing order is automatically the smallest, so the only check worth designing is "does this integer qualify":

1. Define `digit_sum(value)` as the sum of the integer's decimal digits.
2. Iterate `candidate` from `0` up to `10^numberOfDigits` (a valid number with
   `numberOfDigits` digits always lies below that bound).
3. A `candidate` qualifies when `len(str(candidate)) == numberOfDigits` and
   `digit_sum(candidate) == digitSum`; the string length test doubles as the
   no-leading-zero rule, because `str` never produces one.
4. Return the first qualifying candidate as a string.

#### Walkthrough

Example 1, `digitSum = 20`, `numberOfDigits = 3`. The scan tests every integer from `0` upward; representative failures and the hit:

```text
candidate 0     str "0"     length 1 != 3            skip
candidate 99    str "99"    length 2 != 3            skip
candidate 100   digit sum 1 + 0 + 0 = 1  != 20      skip
candidate 199   digit sum 1 + 9 + 9 = 19 != 20      skip
candidate 289   digit sum 2 + 8 + 9 = 19 != 20      skip
candidate 299   digit sum 2 + 9 + 9 = 20 == 20      return "299"
```

Every candidate from `100` to `298` carries a digit sum of at most `19`: a hundreds digit of `1` leaves `9 + 9 = 18` for the rest, and a hundreds digit of `2` caps the value below `300`, so the tens and units cannot both reach `9` until the value hits `299` itself. The first qualifying candidate is therefore `299`, matching the expected Output.

#### Solution

The code is the increasing scan from the walkthrough, with the two qualification tests in one `if`.

```python
class Solution:
    def solve(self, digitSum: int, numberOfDigits: int) -> str:
        def digit_sum(value: int) -> int:
            return sum(int(digit) for digit in str(value))

        limit = 10 ** numberOfDigits
        for candidate in range(limit):
            if len(str(candidate)) == numberOfDigits and digit_sum(candidate) == digitSum:
                return str(candidate)
        raise ValueError("no valid number exists below 10 ** numberOfDigits")
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(10^numberOfDigits × numberOfDigits)`

The qualifying number can sit anywhere below `10^numberOfDigits`, and each of the up to `10^numberOfDigits` candidates costs `O(numberOfDigits)` to stringify and sum.

##### Space Complexity: `O(numberOfDigits)`

The string form of the current candidate, plus the returned result of the same size.

#### Key Insights

- `str(candidate)` is the whole validation trick: it never carries a leading zero, so the length test enforces the digit count and the leading-digit rule in one comparison.
- The first match in an increasing scan is the smallest by construction; no tie-breaking logic exists to get wrong.
- Correct but hopeless at scale: for `numberOfDigits = 18` the scan walks past `10^17` candidates, which motivates constructing the answer digit by digit instead of searching for it.

### Top-Down Digit Choice

#### Derivation

Enumeration wastes its effort discovering what each digit must be, one rejected candidate at a time. Build the answer instead, left to right, deciding one digit at a time: because the length is fixed, numeric order is digit-string lexicographic order, so the smallest number places the smallest feasible digit at every position. Feasibility is a one-line window: after placing digits with `sum_left` still to distribute over `positions_left` remaining positions, a completion exists exactly when the remainder fits between `0` and `9 × positions_left`. The leading digit of a multi-digit number is additionally floored at `1`:

1. `build(position, sum_left)` returns the digit string for positions
   `position .. numberOfDigits - 1` carrying `sum_left` to distribute.
2. At `position == numberOfDigits`, return the empty string; all digits are
   placed and the remainder is `0`.
3. Otherwise try `digit_value` from `digit_floor` up to `9` in increasing
   order, where `digit_floor` is `1` for the leading digit of a multi-digit
   number and `0` otherwise.
4. The first `digit_value` with `feasible(sum_left - digit_value,
   numberOfDigits - position - 1)` is placed, and the recursion never
   backtracks: a smaller leading digit beats anything built past a larger one,
   so no later choice can resurrect a skipped digit.

#### Walkthrough

Example 1, `digitSum = 20`, `numberOfDigits = 3`. Each position tries digits smallest first and keeps the first one whose remainder stays inside the feasibility window:

```text
position 0  floor 1
  try 1   remainder 19 over 2 positions, capacity 9 x 2 = 18   19 > 18 infeasible
  try 2   remainder 18 <= 18 feasible                          place 2, sum_left 18
position 1  floor 0
  try 0   remainder 18 over 1 position, capacity 9             infeasible
  try 1..8 each leave 17..10 over 1 position                 infeasible
  try 9   remainder 9 <= 9 feasible                            place 9, sum_left 9
position 2
  try 0..8 each leave 9..1 over 0 positions                    infeasible
  try 9   remainder 0 <= 0 feasible                            place 9, sum_left 0
```

The recursion consumed the whole sum exactly at the last position and returns `"2" + "9" + "9" = "299"`, matching the expected Output. Example 2 (`digitSum = 1`, `numberOfDigits = 4`) exercises the leading floor instead: digit `1` is the first whose remainder `0` fits the remaining three positions, and zeros follow, yielding `"1000"`.

#### Solution

The code is the per-position trial from the walkthrough, wrapped in a `feasible` helper the trials share.

```python
class Solution:
    def solve(self, digitSum: int, numberOfDigits: int) -> str:
        def feasible(sum_left: int, positions_left: int) -> bool:
            return 0 <= sum_left <= 9 * positions_left

        def build(position: int, sum_left: int) -> str:
            if position == numberOfDigits:
                return ""
            digit_floor = 1 if position == 0 and numberOfDigits > 1 else 0
            for digit_value in range(digit_floor, 10):
                if feasible(sum_left - digit_value, numberOfDigits - position - 1):
                    return str(digit_value) + build(position + 1, sum_left - digit_value)
            raise ValueError(f"position {position} admits no feasible digit")

        return build(0, digitSum)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(numberOfDigits)`

Each of the `numberOfDigits` positions trials at most ten digits against an `O(1)` feasibility window; the constant ten never grows with the input.

##### Space Complexity: `O(numberOfDigits)`

The recursion descends one frame per position and assembles the output string of the same length.

#### Key Insights

- The feasibility window `0 <= sum_left <= 9 × positions_left` is the entire problem: every decision reduces to keeping the remainder inside it.
- Fixed length makes numeric order identical to lexicographic order, which is why committing to the smallest feasible digit at each position is globally optimal and the recursion never backtracks.
- The leading-digit floor (`1` instead of `0` when `numberOfDigits > 1`) is the one asymmetric position; forgetting it builds numbers like `090`, which are not valid answers.
- The construction still asks every position a small question; the next solution answers those questions in closed form.

### Greedy Fill from the Right

#### Derivation

The top-down construction asks each position "what is the smallest digit that keeps the remainder feasible?", but the answers have closed forms. At the leading digit the floor is exact: the tail of `numberOfDigits - 1` positions can absorb at most `9 × (numberOfDigits - 1)`, so the leading digit must be at least `digitSum - 9 × (numberOfDigits - 1)`, and at least `1` for a multi-digit number; the smaller of those two lower bounds is the answer. Every later position is the mirror image: pushing as much of the remaining sum as the law of digits allows (`min(9, remaining_sum)`) into the rightmost slot makes every position to its left as small as possible, which is exactly the objective:

1. Return `str(digitSum)` immediately when `numberOfDigits == 1` (the digit is
   the sum, including the single-digit answer `0`).
2. Set `leading_digit = max(1, digitSum - 9 * (numberOfDigits - 1))`.
3. Allocate `digits` with the leading digit and zeros; fill from the rightmost
   position toward position `1` with `min(9, remaining_sum)` per slot.
4. The fill cannot reach the leading slot: `leading_digit >= digitSum -
   9 × (numberOfDigits - 1)` caps the remainder at the tail's capacity.
5. Join `digits` into the returned string.

#### Walkthrough

Example 1, `digitSum = 20`, `numberOfDigits = 3`, filled in three moves:

```text
leading_digit  = max(1, 20 - 9 x 2) = max(1, 2) = 2    remaining_sum = 18
tail position 2 = min(9, 18) = 9                       remaining_sum = 9
tail position 1 = min(9, 9)  = 9                       remaining_sum = 0
digits = [2, 9, 9]  ->  "299"
```

The leading digit lands on its exact lower bound (`20 - 18 = 2`), the tail soaks up the rest as two nines, and the result is `"299"`, matching the expected Output. Example 2 shows the floor doing the leading: `max(1, 1 - 27) = 1` with `remaining_sum = 0`, so the tail keeps its zeros and the result is `"1000"`.

#### Solution

The code is the two closed forms from the walkthrough: one `max` for the leading digit, one `min`-driven sweep for the tail.

```python
class Solution:
    def solve(self, digitSum: int, numberOfDigits: int) -> str:
        if numberOfDigits == 1:
            return str(digitSum)

        leading_digit = max(1, digitSum - 9 * (numberOfDigits - 1))
        remaining_sum = digitSum - leading_digit
        digits = [leading_digit] + [0] * (numberOfDigits - 1)
        position = numberOfDigits - 1
        while remaining_sum > 0:
            placed = min(9, remaining_sum)
            digits[position] = placed
            remaining_sum -= placed
            position -= 1
        return ''.join(map(str, digits))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(numberOfDigits)`

One pass fills the tail and the join assembles the output; every arithmetic step is constant time.

##### Space Complexity: `O(numberOfDigits)`

The `digits` buffer, which becomes the returned string.

#### Key Insights

- The leading digit is forced, not chosen: `max(1, digitSum - 9 × (numberOfDigits - 1))` is simultaneously the no-leading-zero floor and the smallest value that leaves the tail enough capacity.
- Mass belongs as far right as possible: every unit pushed into a rightward slot is a unit not inflating a more significant position.
- The naive version of this greedy (fill the tail first, let the front take the leftover) breaks on inputs like `digitSum = 9`, `numberOfDigits = 3`: the tail absorbs everything and the front strands a zero, producing the invalid `090`. Reserving the leading digit before the tail sweep is the fix.
- The single-digit case needs its own branch: `max(1, ...)` would wrongly promote a `digitSum` of `0` to `1`.

## Comparison of Solutions

### Time Complexity

- **Candidate Enumeration**: `O(10^numberOfDigits × numberOfDigits)` - scans up to `10^numberOfDigits` integers, each costing a length check and a digit sum.
- **Top-Down Digit Choice**: `O(numberOfDigits)` - at most ten constant-time feasibility trials per position.
- **Greedy Fill from the Right**: `O(numberOfDigits)` - one closed-form leading digit plus one tail sweep.

### Space Complexity

- **Candidate Enumeration**: `O(numberOfDigits)` - the string form of the current candidate.
- **Top-Down Digit Choice**: `O(numberOfDigits)` - recursion depth plus the assembled output.
- **Greedy Fill from the Right**: `O(numberOfDigits)` - the `digits` buffer that becomes the result.

### Trade-offs

- **Candidate Enumeration**: impossible to get wrong and doubles as a testing oracle, but exponential in the digit count; unusable past a handful of digits.
- **Top-Down Digit Choice**: optimal and self-documenting, since the feasibility window states the whole constraint, but it re-derives each digit by trial instead of computing it.
- **Greedy Fill from the Right**: the shortest and fastest expression, with both per-position decisions in closed form, at the cost of a correctness argument (the leading-digit reserve) that is easy to miss under interview pressure.

### When to Use Each

- **Greedy Fill from the Right (Recommended)**: the interview answer: linear, direct, and the leading-digit formula doubles as the infeasibility explanation.
- **Top-Down Digit Choice**: when you want the feasibility window spoken out loud, or as the derivation step that makes the closed forms believable.
- **Candidate Enumeration**: for tiny digit counts, as a cross-check oracle in tests, or to probe the leading-zero rule before committing to a construction.

### Optimization Notes

- The single-digit branch must return `str(digitSum)` before any `max(1, ...)` runs, otherwise the valid answer `0` is corrupted into `1`.
- `''.join(map(str, digits))` converts each digit once; building the string by repeated concatenation inside the loop would be quadratic.
- The tail fill writes only tail slots: `leading_digit >= digitSum - 9 × (numberOfDigits - 1)` caps `remaining_sum` at the tail's capacity, which is the invariant that keeps the leading slot untouched.
- The `raise ValueError` branches in the first two solutions are unreachable for inputs satisfying the statement's guarantee; they exist so the functions are total and honest about inputs outside the contract.
