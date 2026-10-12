# [Next Palindromic Time](https://www.fastprep.io/problems/amazon-next-palindromic-time)

**Medium** | **NN minutes** | **String, Simulation**

Given a valid 24-hour time time in HH:MM format, return the first strictly later time whose four digits form a palindrome.

Advance in one-minute steps and wrap from 23:59 to 00:00. The input itself is never returned unless a full day has elapsed.

## Examples

### Example 1

**Input:** `time = "12:21"`

**Output:** `"13:31"`

**Explanation:** 13:31 is the first later valid time whose digits read the same in both directions.

### Example 2

**Input:** `time = "23:32"`

**Output:** `"00:00"`

**Explanation:** No later palindromic time remains that day, so the search wraps to midnight.

### Example 3

**Input:** `time = "05:50"`

**Output:** `"10:01"`

**Explanation:** The next palindromic four-digit clock value after 0550 is 1001.

## Constraints

- `time.length == 5.`
- `time[2] == ':'.`
- `time is a valid zero-padded 24-hour time from 00:00 through 23:59.`

## Solutions

### One-Minute Simulation

#### Derivation

The most literal reading of the problem is the algorithm: the problem says "advance in one-minute steps", so advance in one-minute steps, and after each step test whether the four digits read the same in both directions. The only machinery needed is a clock rollover (minutes `60` become hour `+1`, hour `24` becomes `00`) and a string comparison. Termination is guaranteed without any cleverness: `00:00` is itself palindromic, so a strictly later palindrome always exists within one day:

1. Parse `hours` and `minutes` from `time`.
2. Increment `minutes`; roll over into the next hour, and `23:xx` into the
   next day's `00:xx`, when `minutes` reaches `60`.
3. Format the clock as `candidate`; when `candidate == candidate[::-1]`,
   return it.
4. Otherwise keep incrementing.

#### Walkthrough

Example 1 starts from `time = "12:21"`. Each increment produces one candidate, and the palindrome test rejects it until the clock reaches `13:31`:

```text
hours = 12, minutes = 21
increment -> 12:22   "1222" reversed "2221" != "1222", keep going
increment -> 12:23   "1223" reversed "3221" != "1223", reject
   ...               (12:24 through 12:59 all rejected)
rollover   -> 13:00   "1300" reversed "0031", reject
   ...               (13:01 through 13:30 all rejected)
increment -> 13:31   "1331" reversed "1331", palindrome -> return "13:31"
```

The rejected stretch is `12:22` through `13:30`, which is `70` increments, and the `71`st candidate `13:31` passes. The returned string matches the expected Output for Example 1.

#### Solution

The code is the walkthrough's increment, rollover, and test, with no other state:

```python
class Solution:
    def solve(self, time: str) -> str:
        hours, minutes = int(time[:2]), int(time[3:])
        while True:
            minutes += 1
            if minutes == 60:
                minutes = 0
                hours = (hours + 1) % 24
            candidate = f"{hours:02d}:{minutes:02d}"
            if candidate == candidate[::-1]:
                return candidate
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

The loop walks at most the 1,440 minutes of one day (the longest stretch without a palindrome runs from 15:51 to 20:02, 251 steps) before `00:00` forces a hit: a constant bound.

##### Space Complexity: `O(1)`

Two integers and one five-character candidate string.

#### Key Insights

- The simulation is correct by construction: it literally implements the problem statement, so rollover and the "strictly later" rule cannot drift out of sync with the specification.
- Testing `candidate == candidate[::-1]` delegates the palindrome definition to the string, avoiding manual index comparisons.
- The price is wasted work: of the up-to-251 candidates tested in the worst gap, only 16 clock strings per day could ever pass, which motivates the table approach.

### Sorted Palindrome Table

#### Derivation

The simulation re-tests up to 251 clock strings when only 16 could ever pass, and that is the waste to remove. The palindrome condition on `HH:MM` forces a relation between the halves: `MM` must be the reverse of `HH`. So the entire palindrome set is derivable from the hour alone: try all 24 hour strings, keep those whose reversed hour is a valid minute (`<= 59`), and 16 entries survive. With the table sorted, the answer is the first entry strictly greater than the current minute-of-day, wrapping to the first entry when none is:

1. Build `palindromic_minutes`: for each `hour` in `0..23`, reverse its
   two-digit text; if the reversed value is at most `59`, record
   `hour * 60 + reversed_minute`.
2. Sort the table.
3. Convert `time` to `current_minute`; scan the sorted table for the first
   entry `> current_minute` and format it back to `HH:MM`.
4. When the scan falls through (the input is `23:32` or later), return the
   first entry, which is midnight `00:00`.

#### Walkthrough

Example 2 exercises the wrap, on `time = "23:32"`. The table build keeps 16 of the 24 hour candidates (`06` through `09` reverse to `60` through `90`, and `16` through `19` reverse past `59`, all rejected). In minute-of-day form the sorted table reads:

```text
[    0,   70,  140,  210,  280,  350,  601,  671,
  741,  811,  881,  951, 1202, 1272, 1342, 1412 ]
  00:00 01:10 02:20 03:30 04:40 05:50 10:01 11:11
  12:21 13:31 14:41 15:51 20:02 21:12 22:22 23:32
```

The input converts to `current_minute = 23 * 60 + 32 = 1412`. The scan needs an entry strictly greater than `1412`, and the last entry `1412` itself does not qualify (`23:32` must not be returned), so the scan falls through and returns the first entry:

```text
current_minute = 1412
scan: 0 > 1412? no ... 1412 > 1412? no -> fall through
return table[0] = 0 minutes = "00:00"
```

The result matches the expected Output for Example 2. Example 1 on the same table is a two-entry scan: `current_minute = 741`, the first entry greater than `741` is `811`, which formats to `"13:31"`.

#### Solution

The code is the table build, the sort, and the successor scan with wraparound:

```python
from typing import List


class Solution:
    def solve(self, time: str) -> str:
        palindromic_minutes: List[int] = []
        for hour in range(24):
            reversed_minute = int(f"{hour:02d}"[::-1])
            if reversed_minute <= 59:
                palindromic_minutes.append(hour * 60 + reversed_minute)
        palindromic_minutes.sort()

        current_minute = int(time[:2]) * 60 + int(time[3:])
        for palindromic_minute in palindromic_minutes:
            if palindromic_minute > current_minute:
                hour, minute = divmod(palindromic_minute, 60)
                return f"{hour:02d}:{minute:02d}"

        hour, minute = divmod(palindromic_minutes[0], 60)
        return f"{hour:02d}:{minute:02d}"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

Building the table touches 24 hours, the sort handles 16 fixed entries, and the successor scan walks at most 16 entries.

##### Space Complexity: `O(1)`

The table holds at most 24 integers regardless of input.

#### Key Insights

- The single observation `MM = reverse(HH)` collapses a search over 1,440 minutes into a list of 16 entries derived from the hour alone.
- Storing minute-of-day integers makes "strictly later" a plain integer comparison and makes the day wrap a single `%`-free fallthrough to `table[0]`.
- The table is built per call here; in a real system serving many queries it would be built once at startup and shared.

### Palindrome Table with Bisect

#### Derivation

The previous solution already sorts the table, and then ignores the sort by scanning linearly. Handing the successor query to the standard library is the same algorithm with only its bookkeeping moved: [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) via `bisect_right` returns the index of the first table entry strictly greater than `current_minute` in one call. The only new idea is the wrap: when the query exceeds every entry, `bisect_right` returns `len(table)`, and one modulo maps that back to index `0`, midnight:

1. Build and sort `palindromic_minutes` exactly as before.
2. `insert_point = bisect_right(palindromic_minutes, current_minute)`.
3. Format `palindromic_minutes[insert_point % len(palindromic_minutes)]` and
   return it.

#### Walkthrough

Example 2 again, `time = "23:32"`, `current_minute = 1412`: the 16-entry table is the one shown in the previous walkthrough, and the query sits exactly on its last entry:

```text
table      = [0, 70, ..., 1342, 1412]   (16 entries)
bisect_right(table, 1412) = 16          (past the last entry)
16 % 16 = 0                             -> table[0] = 0 minutes
return "00:00"
```

Example 3, `time = "05:50"`, `current_minute = 350`, shows the ordinary in-range case:

```text
table      = [0, 70, 140, 210, 280, 350, 601, ...]
bisect_right(table, 350) = 6            (first entry strictly > 350)
table[6] = 601                          -> 601 minutes = "10:01"
```

Both results match the expected Outputs for Examples 2 and 3.

#### Solution

The code is the shared table build with the scan replaced by one `bisect_right` call and a modulo wrap:

```python
from bisect import bisect_right
from typing import List


class Solution:
    def solve(self, time: str) -> str:
        palindromic_minutes: List[int] = []
        for hour in range(24):
            reversed_minute = int(f"{hour:02d}"[::-1])
            if reversed_minute <= 59:
                palindromic_minutes.append(hour * 60 + reversed_minute)
        palindromic_minutes.sort()

        current_minute = int(time[:2]) * 60 + int(time[3:])
        insert_point = bisect_right(palindromic_minutes, current_minute)
        hour, minute = divmod(
            palindromic_minutes[insert_point % len(palindromic_minutes)], 60)
        return f"{hour:02d}:{minute:02d}"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

The table build and sort are fixed-size, and `bisect_right` performs at most `log2(16) = 4` comparisons.

##### Space Complexity: `O(1)`

The same fixed 16-entry table.

#### Key Insights

- `bisect_right` (not `bisect_left`) is the correct probe for "strictly later": it lands after any entry equal to `current_minute`, so an input like `12:21` can never return itself.
- The modulo wrap folds the midnight case into the same expression as the ordinary case, deleting the fallthrough branch the linear version needed.
- With 16 entries the scan and the binary search are both instant; the bisect form earns its keep only when the table idea generalizes to larger calendars (seconds, or other palindromic formats).

### Direct Hour Mirror

#### Derivation

The table still enumerates all 24 hours even though the answer almost always sits in the current or next few hours. The same `MM = reverse(HH)` relation can construct the answer directly instead of searching for it. Standing at `HH:MM`, exactly one of two cases holds: the mirrored minute of the current hour, `reverse(HH)`, is a valid minute strictly greater than `MM`, in which case that is the answer and nothing else needs checking; or the answer lives in some later hour, in which case advance the hour one step at a time, skipping hours whose mirror exceeds `59`, and return the first valid mirror. Hour `00` always mirrors to the valid minute `00`, so the advance loop always terminates, and advancing from `23` lands on `00`, which makes the day wrap a natural consequence rather than a branch:

1. Parse `hour` and `minute` from `time`.
2. Compute `same_hour_minute = reverse of the two-digit hour`; if it is at
   most `59` and strictly greater than `minute`, return it formatted.
3. Otherwise loop: advance `hour = (hour + 1) % 24`, compute its mirror, and
   return as soon as the mirror is at most `59`.

#### Walkthrough

Example 3, `time = "05:50"`, hits the skip streak: the current hour's mirror fails, and four hours in a row mirror past `59`:

```text
hour = 5, minute = 50
same_hour_minute = reverse("05") = 50
  50 <= 59 but 50 > 50 is false          -> answer is in a later hour

advance to hour 6:  mirror("06") = 60    -> invalid, skip
advance to hour 7:  mirror("07") = 70    -> invalid, skip
advance to hour 8:  mirror("08") = 80    -> invalid, skip
advance to hour 9:  mirror("09") = 90    -> invalid, skip
advance to hour 10: mirror("10") = 01    -> valid

return "10:01"
```

The result matches the expected Output for Example 3. Example 2, `time = "23:32"`, shows the wrap: the mirror of `23` is `32`, which is valid but not strictly greater than `32`, so the loop advances to hour `(23 + 1) % 24 = 0`, whose mirror `00` is valid, returning `"00:00"`.

#### Solution

The code is the two cases: one mirrored-minute check, then the hour-advance loop:

```python
class Solution:
    def solve(self, time: str) -> str:
        hour = int(time[:2])
        minute = int(time[3:])

        same_hour_minute = int(f"{hour:02d}"[::-1])
        if minute < same_hour_minute <= 59:
            return f"{hour:02d}:{same_hour_minute:02d}"

        while True:
            hour = (hour + 1) % 24
            candidate_minute = int(f"{hour:02d}"[::-1])
            if candidate_minute <= 59:
                return f"{hour:02d}:{candidate_minute:02d}"
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

One mirror check plus at most 24 hour advances (the longest skip, hours `16` through `19` and `06` through `09`, is four consecutive invalid hours before a valid mirror appears).

##### Space Complexity: `O(1)`

A handful of integers and short strings.

#### Key Insights

- Constructing beats searching: the answer's hour is either the current one (mirror strictly later within the hour) or the next valid one, so no palindrome list is ever materialized.
- The strict `>` in the same-hour check is what upholds "never return the input": an input like `12:21` rejects its own mirror `21` and moves on.
- The `% 24` wrap is doing double duty: it is both the day rollover of the specification and the termination proof of the loop, since hour `00` always mirrors to a valid minute.

## Comparison of Solutions

### Time Complexity

- **One-Minute Simulation**: `O(1)` - at most 1,440 minute steps, with the worst real gap 251 minutes (15:51 to 20:02).
- **Sorted Palindrome Table**: `O(1)` - a 24-hour table build, a 16-entry sort, and a linear successor scan.
- **Palindrome Table with Bisect**: `O(1)` - the same table with a `log2(16)` binary search.
- **Direct Hour Mirror**: `O(1)` - one mirror check plus at most a few hour advances.

### Space Complexity

- **One-Minute Simulation**: `O(1)` - two integers and one candidate string.
- **Sorted Palindrome Table**: `O(1)` - a fixed table of at most 24 integers.
- **Palindrome Table with Bisect**: `O(1)` - the same fixed table.
- **Direct Hour Mirror**: `O(1)` - a handful of integers and short strings.

### Trade-offs

- **One-Minute Simulation**: nothing to derive and nothing to get wrong, but it burns up to 251 iterations re-testing strings that never had a chance.
- **Sorted Palindrome Table**: turns the palindrome definition into data, making the successor query and the midnight wrap explicit and inspectable, at the cost of building the table on every call as written.
- **Palindrome Table with Bisect**: same algorithm, tighter successor query and a branch-free wrap, but it only pays off if the table is shared across queries or grows.
- **Direct Hour Mirror**: no table and the smallest constant, but its correctness rests on two cases that must be argued (same-hour strictness, loop termination at hour `00`) rather than seen.

### When to Use Each

- **One-Minute Simulation (Recommended for a first pass)**: when the problem is read cold and the clock arithmetic is the risk: say the simulation out loud, pass the tests, refine if asked.
- **Sorted Palindrome Table**: when asked to reason about the structure ("which times can even qualify?") or when many queries share one precomputed table.
- **Palindrome Table with Bisect**: when the table is already in hand and the successor query should be one standard-library call with the wrap folded in.
- **Direct Hour Mirror**: the polished final answer: state the `MM = reverse(HH)` relation, present the two cases, and note the 251-to-a-few constant-factor drop.

### Optimization Notes

- The two strictness points that decide correctness are easy to lose: the same-hour mirror must be strictly greater than the current minute (Example 2's `23:32` must not return itself), and the successor scan must use strictly greater (`bisect_right`, not `bisect_left`).
- The `06` through `09` and `16` through `19` hour streaks are the whole reason the advance loop and the table filter exist: mirrors past `59` are the only invalid candidates.
- If many queries arrive, build the 16-entry table once at module load and reuse it across calls; the per-call build in the table solutions is a teaching choice, not a requirement.
