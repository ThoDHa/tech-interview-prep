# [Closest Version Date](https://www.fastprep.io/problems/amazon-closest-version-date)

**Easy** | **NN minutes** | **Array, String, Binary Search**

2026-07-02 •ᴗ• Practice note: This version should match the core of the reported interview question by about 85%-90%. It was reported for SDE II. It may not be word-for-word identical, but the main idea and expected approach are close.

You are given a target date and a list of release dates for different software versions. Return the release date that is closest to the target date. The distance between two dates is the absolute number of calendar days between them.

If two release dates are equally close to the target date, return the later date. All dates are provided in YYYY-MM-DD format.

Function Signature

function findClosestVersionDate(targetDate: string, versions: string[]): string

## Examples

### Example 1

**Input:** `targetDate = "2026-04-01"`, `versions = ["2023-04-01", "2025-04-01", "2026-05-03"]`

**Output:** `"2026-05-03"`

**Explanation:** 2023-04-01 is 1096 days away, 2025-04-01 is 365 days away, and 2026-05-03 is 32 days away. The closest release date is 2026-05-03.

### Example 2

**Input:** `targetDate = "2024-06-10"`, `versions = ["2024-06-01", "2024-06-20", "2024-07-01"]`

**Output:** `"2024-06-01"`

**Explanation:** 2024-06-01 is 9 days away, which is closer than 2024-06-20 and 2024-07-01.

### Example 3

**Input:** `targetDate = "2025-01-15"`, `versions = ["2025-01-10", "2025-01-20"]`

**Output:** `"2025-01-20"`

**Explanation:** Both dates are 5 days away. Since there is a tie, return the later date.

### Example 4

**Input:** `targetDate = "2026-04-01"`, `versions = ["2026-04-01", "2026-05-03", "2025-12-31"]`

**Output:** `"2026-04-01"`

**Explanation:** An exact match has distance 0, so it is the closest version date.

## Constraints

- `1 <= versions.length <= 100000`
- `targetDate and every date in versions are valid dates in YYYY-MM-DD format.`
- `versions may not be sorted.`
- `Follow-up`
- `If versions is already sorted, can you solve each query faster than checking every date? What if there are many target dates queried against the same version list?`

## Solutions

### Linear Scan with Date Objects

#### Derivation

The distances are calendar-day gaps, so the first question is how to measure one: Python's [datetime](https://docs.python.org/3/library/datetime.html) module parses `YYYY-MM-DD` with `date.fromisoformat`, and subtracting two `date` objects yields a `timedelta` whose `.days` is exactly the day count, leap years and month lengths included. With a trustworthy distance in hand, the problem collapses to the plainest scan there is: walk the list, remember the best candidate, replace it whenever something beats it.

The tie rule folds into the replacement condition. A release date wins only when it is strictly closer, or when it ties on distance and is the later of the two, which for `YYYY-MM-DD` strings is just `>`:

1. Parse `targetDate` once into the `date` object `target`.
2. Initialize `best_date` to the first version and `best_gap` to its distance.
3. For each remaining version, compute `gap`; replace the incumbent when
   `gap < best_gap`, or when `gap == best_gap` and `version > best_date`.
4. Return `best_date`.

#### Walkthrough

Example 1, with target 2026-04-01. The statement supplies the day gaps (1096, 365, 32); the trace shows only the best-tracking logic:

```text
init        best_date = 2023-04-01   best_gap = 1096
2025-04-01  gap = 365 < 1096         best_date = 2025-04-01  best_gap = 365
2026-05-03  gap = 32  < 365          best_date = 2026-05-03  best_gap = 32
```

Every version after the first either beats the incumbent or is discarded, so after the scan `best_date = 2026-05-03`, the expected Output.

#### Solution

The code is the scan from the walkthrough, with the calendar work delegated to `date.fromisoformat`.

```python
from datetime import date
from typing import List


class Solution:
    def findClosestVersionDate(self, targetDate: str, versions: List[str]) -> str:
        target = date.fromisoformat(targetDate)
        best_date = versions[0]
        best_gap = abs((date.fromisoformat(best_date) - target).days)

        for version in versions[1:]:
            gap = abs((date.fromisoformat(version) - target).days)
            if gap < best_gap or (gap == best_gap and version > best_date):
                best_date = version
                best_gap = gap

        return best_date
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` versions is parsed and compared once; parsing a fixed-format `YYYY-MM-DD` string is constant work.

##### Space Complexity: `O(1)`

Only the target, the incumbent, and its gap are held between iterations.

#### Key Insights

- The whole problem is the distance function: once `YYYY-MM-DD` maps to a real day count, the rest is a best-element scan.
- The tie rule becomes one comparison clause: on equal gaps, `version > best_date` keeps the later date, and ISO strings compare chronologically.
- Comparing the date strings directly (`version > best_date`) for the tie-break is legal even though gaps themselves cannot be read off strings.

### Linear Scan with Hand-Rolled Day Numbers

#### Derivation

The library scan hides the one interesting question: what does "absolute number of calendar days" actually require? A day count needs a reference point and the Gregorian calendar's rules, and both are small enough to write by hand. The observation is that differences are all that matter, so any monotone day numbering works; the standard choice counts days from a fixed epoch year using the leap rule that year numbers divisible by 4 are leap years, except centuries not divisible by 400:

1. Parse each date into `year`, `month`, `day`.
2. Count `days_before_year`, the days in every year before `year`:
   `365 * (year - 1)` ordinary days plus one extra for each leap year before it,
   which is `(year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400`.
3. Add `DAYS_BEFORE_MONTH[month - 1]`, the cumulative days of the months
   before `month` in a non-leap year, plus `day`, plus one when `month > 2`
   and `year` is a leap year.
4. Run the same scan and tie-break as [Linear Scan with Date Objects](#linear-scan-with-date-objects), now over integer day numbers.

#### Walkthrough

Example 1, target 2026-04-01. The conversions, using `DAYS_BEFORE_MONTH[3] = 90` for the months before April:

```text
2023-04-01: 365*2022 + (505 - 20 + 5) + 90 + 1 = 739011    gap = |739011 - 740107| = 1096
2025-04-01: 365*2024 + (506 - 20 + 5) + 90 + 1 = 739742    gap = |739742 - 740107| =  365
2026-04-01: 365*2025 + (506 - 20 + 5) + 90 + 1 = 740107    target
2026-05-03: 740107 + 31 + 3                     = 740141    gap = |740141 - 740107| =   32
```

The scan initializes on 2023-04-01 with `best_gap = 1096`, drops the incumbent for 2025-04-01 (`365 < 1096`), then for 2026-05-03 (`32 < 365`), and returns `2026-05-03`.

#### Solution

The code is the day-number arithmetic from the walkthrough feeding the unchanged scan.

```python
from typing import List

DAYS_BEFORE_MONTH = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)


def to_day_number(date_text: str) -> int:
    year, month, day = (int(part) for part in date_text.split("-"))
    days_before_year = (365 * (year - 1)
                        + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400)
    is_leap_year = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    february_correction = 1 if is_leap_year and month > 2 else 0
    return days_before_year + DAYS_BEFORE_MONTH[month - 1] + day + february_correction


class Solution:
    def findClosestVersionDate(self, targetDate: str, versions: List[str]) -> str:
        target_day = to_day_number(targetDate)
        best_date = versions[0]
        best_gap = abs(to_day_number(best_date) - target_day)

        for version in versions[1:]:
            gap = abs(to_day_number(version) - target_day)
            if gap < best_gap or (gap == best_gap and version > best_date):
                best_date = version
                best_gap = gap

        return best_date
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each version is split, converted, and compared once, all constant work per date.

##### Space Complexity: `O(1)`

The month table is fixed size and the scan holds three values.

#### Key Insights

- Distances only need a monotone day numbering, so the epoch is arbitrary and the arithmetic stays in integers.
- The Gregorian leap rule is three clauses: divisible by 4, except centuries, except centuries divisible by 400; `days_before_year` counts leap days before the year, the correction adds February 29 inside it.
- This version and the `datetime` version agree everywhere; the hand-rolled one is what you would write in a language without a date library, and it makes the cost of the abstraction visible.

### Binary Search over Sorted Day Numbers

#### Derivation

Both scans pay `O(n)` per query. The Follow-up asks what a sorted list buys: in a sorted list of day numbers, the closest entry to the target is one of the two dates that surround it, the last one before and the first one at or after. So one pass of [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) for the insertion point of the target reduces each query to `O(log n)` comparisons after an `O(n log n)` sort. For a single query the sort dominates and the linear scan wins; for many target dates queried against the same version list, the sort is paid once and every later query costs `O(log n)`, which is the Follow-up's second question:

1. Convert every version to a day number and sort the `(day_number, date_text)`
   pairs into `pairs`; keep `ordered_days`, the day numbers alone, for searching.
2. Binary-search `ordered_days` for `target_day`: find `position`, the first
   index whose day number is not less than the target.
3. The only candidates are `position - 1` (last earlier date) and `position`
   (first later-or-equal date); both are in bounds unless the target falls
   outside the list, in which case only one exists.
4. Compare their gaps; scanning the candidates in increasing order and
   replacing on `gap <= best_gap` resolves the tie rule in favor of the later date.

#### Walkthrough

Example 2, target 2024-06-10, versions `["2024-06-01", "2024-06-20", "2024-07-01"]`. Sorted pairs; the absolute day numbers only need relative order, so the trace labels them `d1 < d2 < d3`:

```text
pairs        = [(d1, 2024-06-01), (d2, 2024-06-20), (d3, 2024-07-01)]
target_day   = d1 + 9

search: low = 0, high = 3
  middle = 1: ordered_days[1] = d2 >= target -> high = 1
  middle = 0: ordered_days[0] = d1 <  target -> low  = 1
  low == high = 1 -> position = 1

candidates:  position - 1 = 0 -> 2024-06-01, gap = 9
             position     = 1 -> 2024-06-20, gap = 10
```

The candidate loop starts at position 0 (`best_gap` becomes 9), then reaches position 1 (gap 10, not `<= 9`), so `best_date` stays `2024-06-01`, the expected Output. On Example 3 (target 2025-01-15, gaps 5 and 5) the same loop reaches the later date last and its `gap <= best_gap` replacement keeps `2025-01-20`.

#### Solution

The code is the search and the two-candidate check from the walkthrough.

```python
from typing import List

DAYS_BEFORE_MONTH = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)


def to_day_number(date_text: str) -> int:
    year, month, day = (int(part) for part in date_text.split("-"))
    days_before_year = (365 * (year - 1)
                        + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400)
    is_leap_year = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    february_correction = 1 if is_leap_year and month > 2 else 0
    return (days_before_year + DAYS_BEFORE_MONTH[month - 1]
            + day + february_correction)


class Solution:
    def findClosestVersionDate(self, targetDate: str, versions: List[str]) -> str:
        target_day = to_day_number(targetDate)
        pairs = sorted((to_day_number(version), version) for version in versions)
        ordered_days = [day_number for day_number, _ in pairs]

        low, high = 0, len(ordered_days)
        while low < high:
            middle = (low + high) // 2
            if ordered_days[middle] < target_day:
                low = middle + 1
            else:
                high = middle
        position = low

        best_date = ""
        best_gap = None
        for candidate_position in (position - 1, position):
            if 0 <= candidate_position < len(ordered_days):
                gap = abs(ordered_days[candidate_position] - target_day)
                if best_gap is None or gap <= best_gap:
                    best_date = pairs[candidate_position][1]
                    best_gap = gap

        return best_date
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The sort costs `O(n log n)`; the search and the two candidate checks cost `O(log n)`. For one query this is worse than the linear scan; with `q` queries against one preprocessed list, the total is `O((n + q) log n)`.

##### Space Complexity: `O(n)`

The sorted pair list and its parallel day-number list.

#### Key Insights

- Sorted order localizes the answer: the closest date is always a neighbor of the target's insertion point, so a query never touches more than two candidates.
- The sort is preprocessing, not per-query work; the amortized view is what answers the Follow-up's many-queries variant.
- Carrying `(day_number, date_text)` pairs sidesteps converting a day number back into a date string.

### Binary Search with bisect

#### Derivation

The hand-written search is eight lines of loop bookkeeping around one idea: find where the target inserts. The standard library owns exactly that idea as [bisect](https://docs.python.org/3/library/bisect.html): `bisect_left(ordered_days, target_day)` returns the same `position` the loop computed, leaving the two-candidate comparison untouched. This is the same algorithm with the loop handed over, so it earns its own short section rather than a replacement:

1. Build `pairs` and `ordered_days` as before.
2. Call `bisect_left` to get `position`.
3. Run the unchanged candidate loop over `position - 1` and `position`.

#### Walkthrough

The same Example 2 input jumps straight to the state the manual search converged to:

```text
ordered_days = [d1, d2, d3],  target_day = d1 + 9
bisect_left  -> position = 1   (first index with day >= target)
candidate 0  -> 2024-06-01, gap 9    best
candidate 1  -> 2024-06-20, gap 10   not <= 9, discarded
```

The result is again `2024-06-01`; only the loop's eight lines collapsed into one call.

#### Solution

```python
from bisect import bisect_left
from typing import List

DAYS_BEFORE_MONTH = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)


def to_day_number(date_text: str) -> int:
    year, month, day = (int(part) for part in date_text.split("-"))
    days_before_year = (365 * (year - 1)
                        + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400)
    is_leap_year = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    february_correction = 1 if is_leap_year and month > 2 else 0
    return (days_before_year + DAYS_BEFORE_MONTH[month - 1]
            + day + february_correction)


class Solution:
    def findClosestVersionDate(self, targetDate: str, versions: List[str]) -> str:
        target_day = to_day_number(targetDate)
        pairs = sorted((to_day_number(version), version) for version in versions)
        ordered_days = [day_number for day_number, _ in pairs]

        position = bisect_left(ordered_days, target_day)

        best_date = ""
        best_gap = None
        for candidate_position in (position - 1, position):
            if 0 <= candidate_position < len(ordered_days):
                gap = abs(ordered_days[candidate_position] - target_day)
                if best_gap is None or gap <= best_gap:
                    best_date = pairs[candidate_position][1]
                    best_gap = gap

        return best_date
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting dominates, exactly as in the hand-written search; the `bisect_left` call is the same `O(log n)`.

##### Space Complexity: `O(n)`

The sorted pair list and its parallel day-number list.

#### Key Insights

- `bisect_left` is the contract version of the loop: leftmost insertion point among equal keys, which is what the neighbor argument needs.
- Reaching for the library here is a readability move, not an asymptotic one; knowing the loop it replaces is what makes the neighbor analysis trustworthy.

## Comparison of Solutions

### Time Complexity

- **Linear Scan with Date Objects**: `O(n)` - one parse and one comparison per version.
- **Linear Scan with Hand-Rolled Day Numbers**: `O(n)` - the same scan with constant-time integer conversions.
- **Binary Search over Sorted Day Numbers**: `O(n log n)` - the sort dominates a single query; each later query costs `O(log n)`.
- **Binary Search with bisect**: `O(n log n)` - identical bounds with the search loop replaced by a library call.

### Space Complexity

- **Linear Scan with Date Objects**: `O(1)` - incumbent, gap, and parsed target only.
- **Linear Scan with Hand-Rolled Day Numbers**: `O(1)` - a fixed month table and three scalars.
- **Binary Search over Sorted Day Numbers**: `O(n)` - sorted day numbers with parallel date strings.
- **Binary Search with bisect**: `O(n)` - the same preprocessed lists.

### Trade-offs

- **Linear Scan with Date Objects**: the shortest correct expression of the problem; it delegates the calendar, which is fine in Python and impossible where no date library exists.
- **Linear Scan with Hand-Rolled Day Numbers**: makes the calendar arithmetic explicit and dependency-free, at the cost of writing the leap rule by hand.
- **Binary Search over Sorted Day Numbers**: pays a sort up front to make every query after the first logarithmic; overkill for a single query.
- **Binary Search with bisect**: the same performance profile as the hand-written search with less code to get wrong.

### When to Use Each

- **Linear Scan with Date Objects (Recommended)**: the single-query interview answer: `O(n)`, minimal code, and the tie rule in one clause.
- **Linear Scan with Hand-Rolled Day Numbers**: when the interviewer asks how you would measure date distances without a date library.
- **Binary Search over Sorted Day Numbers**: when the Follow-up's many-queries scenario is in play and the version list is preprocessed once.
- **Binary Search with bisect**: the production form of the binary-search approach.

### Optimization Notes

- The tie rule is the main correctness trap: a scan that replaces only on strict improvement returns the earlier date on Example 3. The `gap <= best_gap` order matters because candidates are visited earlier-date first.
- `versions[0]` seeding assumes the constraint `versions.length >= 1`; with an empty list, define the contract before coding.
- For the many-queries variant, hoist the sort into a one-time constructor and keep only `ordered_days` and `pairs` as instance state; each query then touches `O(log n)` entries.
- String comparison is only a proxy for the tie-break; it happens to work because `YYYY-MM-DD` is zero-padded and ordered. The gaps themselves must come from real day numbers, since month lengths make substring distance wrong.
