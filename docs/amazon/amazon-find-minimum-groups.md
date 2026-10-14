# [Find Minimum Groups](https://www.fastprep.io/problems/amazon-find-minimum-groups)

**Medium** | **NN minutes** | **Array, Hash Table, Greedy**

A financial services company has requested AWS for a private deployment of its cloud network. Considering the sensitive nature of the company's business, AWS has also advised them to add a specific type of security system.

Overall, there are n servers in the network where the security needs of the i-th server are represented by security[i], where each element represents the grade of security needed for a server.

To ensure the highest possible protection, the AWS security team has recommended the following rule to be followed while designing the security system: all servers in a security group must have the same grade of security needs, and the number of servers in any two security groups should not differ by more than 1.

Given an integer array security, find the minimum number of security levels needed to ensure the protection of the network.

## Examples

### Example 1

**Input:** `security = [2, 3, 3, 3, 2, 1]`

**Output:** `4`

**Explanation:** Consider n = 6 and security = [2, 3, 3, 3, 2, 1].

Then, the elements can be grouped as follows:

Group 1: 2 devices of vulnerability 2.Group 2: 2 devices of vulnerability 3.Group 3: 1 device of vulnerability 3.Group 4: 1 device of vulnerability 1.It requires 4 groups.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-find-minimum-groups; fill them in. -->

## Solutions

### Candidate Group Count Sweep

#### Derivation

A tempting first reading treats the size rule as local to each grade: split every grade into same-size chunks and sum the group counts. On Example 1 that reading produces six groups (two for grade 2, three for grade 3, one for grade 1), but the expected Output is 4, and the statement's own grouping (sizes 2, 2, 1, 1) mixes two groups inside a single grade. The correct reading is global: the group sizes of any two security groups, whatever their grades, differ by at most one.

That reading collapses the search space. If the network uses `group_count` groups in total over `n` servers, every group must hold either `base_size = floor(n / group_count)` or `base_size + 1` servers. All servers in a group share one security grade, so grades never mix inside a group, and each grade is planned independently against that two-value size menu. A grade appearing `frequency` times can then use any number `used_groups` of groups from 1 up to `group_count`, provided the menu can sum exactly to `frequency`:

1. Tally `frequency_counts`, a [hash map](https://en.wikipedia.org/wiki/Hash_table)
   from security grade to occurrence count, and let `distinct_grades` be its
   length. At least one group per grade is mandatory, so candidates start at
   `distinct_grades`; at most `n` groups (one per server) can ever be needed.
2. For each candidate `group_count`, set `base_size = total_servers // group_count`.
3. A frequency passes the candidate when some `used_groups` in `1..group_count`
   satisfies `used_groups * base_size <= frequency <= used_groups * (base_size + 1)`:
   `used_groups * base_size` is the smallest total that many groups can hold and
   `used_groups * (base_size + 1)` the largest.
4. The first `group_count` where every frequency passes is the answer.

#### Walkthrough

Example 1 has `security = [2, 3, 3, 3, 2, 1]`, so `total_servers = 6`, `distinct_grades = 3`, and the tally is `{2: 2, 3: 3, 1: 1}`. The sweep starts at three groups:

```text
group_count = 3, base_size = 2, admissible sizes {2, 3}
  frequency 2: used_groups 1 -> total range [2, 2], 2 fits            pass
  frequency 3: used_groups 1 -> range [2, 3], 3 fits                  pass
  frequency 1: used_groups 1 -> range [2, 2], 1 misses; used 2, 3 -> worse
               no group of size 2 or 3 can hold exactly 1 server      fail

group_count = 4, base_size = 1, admissible sizes {1, 2}
  frequency 2: used_groups 2 -> range [2, 4], 2 fits (two of size 1)  pass
  frequency 3: used_groups 2 -> range [2, 4], 3 fits (2 + 1)          pass
  frequency 1: used_groups 1 -> range [1, 2], 1 fits (one of size 1)  pass

all frequencies pass -> return 4
```

The failing check at `group_count = 3` is the whole difficulty of the problem in miniature: grade 1 needs a group of size 1, and no partition of size-2-or-3 groups supplies one. At `group_count = 4` every grade finds a plan, and the group sizes 2, 2, 1, 1 reproduce the statement's own grouping, matching the expected Output of `4`.

#### Solution

The code is the candidate sweep from the walkthrough, with `can_split` carrying the menu check per frequency.

```python
from collections import Counter
from typing import List


class Solution:
    def findMinimumGroups(self, security: List[int]) -> int:
        frequency_counts = Counter(security)
        distinct_grades = len(frequency_counts)
        total_servers = len(security)

        for group_count in range(distinct_grades, total_servers + 1):
            base_size = total_servers // group_count
            if all(self.can_split(frequency, group_count, base_size)
                   for frequency in frequency_counts.values()):
                return group_count
        return total_servers

    @staticmethod
    def can_split(frequency: int, group_count: int, base_size: int) -> bool:
        for used_groups in range(1, group_count + 1):
            if used_groups * base_size <= frequency <= used_groups * (base_size + 1):
                return True
        return False
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(d × A²)`

Where `d` is the number of distinct grades and `A` the returned group count: the sweep tries `A - distinct_grades + 1` candidates, and each candidate checks `d` frequencies, each check scanning up to `group_count` values of `used_groups`. The bound is `O(d × n²)` in the worst case, but the sweep stops at the first feasible count.

##### Space Complexity: `O(d)`

The counter holds one entry per distinct grade; the sweep itself uses constant extra space.

#### Key Insights

- The statement's worked grouping is the specification: sizes 2, 2, 1, 1 for `n = 6` pin the rule globally, not per grade.
- Fixing the total group count `group_count` reduces every grade's constraint to a two-value size menu, `{floor(n / group_count), floor(n / group_count) + 1}`.
- A grade may occupy fewer groups than `group_count`; only the sizes of the groups it does occupy are constrained.
- The per-grade reading returns 6 on Example 1 instead of 4, which is exactly the kind of mismatch that should send you back to the statement's example before coding.

### Interval Membership Check

#### Derivation

The sweep's inner loop asks a question with a closed-form answer: for which values of `used_groups` can a menu of `used_groups` groups holding `base_size` or `base_size + 1` servers each sum to `frequency`? The reachable totals form the interval `[used_groups * base_size, used_groups * (base_size + 1)]`, so a valid `used_groups` exists exactly when the two inequalities admit an integer. Solving them for `used_groups` turns each frequency check into a constant-time range comparison, and the sweep over candidates keeps only the O(1) check:

1. Tally the frequencies as before and sweep `group_count` candidates upward.
2. For each frequency, compute the smallest usable group count
   `smallest_fit = ceil(frequency / (base_size + 1))` (fewer groups cannot
   reach the frequency even at maximum size) and the largest
   `largest_fit = floor(frequency / base_size)` (more groups overshoot it
   even at minimum size).
3. The frequency passes when `smallest_fit <= largest_fit` and
   `smallest_fit <= group_count`, so at least one admissible group count
   exists within the budget.
4. The first `group_count` where every frequency passes is the answer.

#### Walkthrough

The same two candidates from the previous walkthrough, now with the closed-form check. At `group_count = 3`, `base_size = 2`, the menu is `{2, 3}` and the range check kills grade 1 immediately:

```text
frequency 2: smallest_fit = ceil(2/3) = 1, largest_fit = 2//2 = 1 -> 1 in [1, 3] pass
frequency 3: smallest_fit = ceil(3/3) = 1, largest_fit = 3//2 = 1 -> 1 in [1, 3] pass
frequency 1: smallest_fit = ceil(1/3) = 1, largest_fit = 1//2 = 0 -> 1 > 0     fail
```

At `group_count = 4`, `base_size = 1`, the menu is `{1, 2}`:

```text
frequency 2: smallest_fit = ceil(2/2) = 1, largest_fit = 2//1 = 2 -> 1 in [1, 4] pass
frequency 3: smallest_fit = ceil(3/2) = 2, largest_fit = 3//1 = 3 -> 2 in [1, 4] pass
frequency 1: smallest_fit = ceil(1/2) = 1, largest_fit = 1//1 = 1 -> 1 in [1, 4] pass

all frequencies pass -> return 4
```

The decisive line is `frequency 1` at `group_count = 3`: even one group overshoots a single server when the smallest admissible group holds 2, and `largest_fit = 0` states that in one arithmetic step. The sweep then accepts 4, matching the expected Output.

#### Solution

The code replaces the `used_groups` scan with the two bounds; the candidate sweep is unchanged.

```python
from collections import Counter
from typing import List


class Solution:
    def findMinimumGroups(self, security: List[int]) -> int:
        frequency_counts = Counter(security)
        distinct_grades = len(frequency_counts)
        total_servers = len(security)

        for group_count in range(distinct_grades, total_servers + 1):
            base_size = total_servers // group_count
            if all(self.can_split(frequency, group_count, base_size)
                   for frequency in frequency_counts.values()):
                return group_count
        return total_servers

    @staticmethod
    def can_split(frequency: int, group_count: int, base_size: int) -> bool:
        smallest_fit = (frequency + base_size) // (base_size + 1)
        largest_fit = frequency // base_size
        return smallest_fit <= largest_fit and smallest_fit <= group_count
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × d)`

Where `d` is the number of distinct grades: up to `n` candidate group counts, each validated with one constant-time check per frequency.

##### Space Complexity: `O(d)`

The counter holds one entry per distinct grade; the sweep uses constant extra space.

#### Key Insights

- Both inequalities on `used_groups` are monotone, so the interval of valid group counts is contiguous and testing its endpoints decides membership in constant time.
- `smallest_fit` is the ceiling division `(frequency + base_size) // (base_size + 1)`, written without floating point to stay exact on large frequencies.
- The check degrades gracefully: a frequency below `base_size` yields `largest_fit = 0`, and a frequency the budget cannot reach yields `smallest_fit > group_count`, both rejected without special cases.
- The overall shape is unchanged from the sweep version; only the per-frequency cost collapsed from `O(group_count)` to `O(1)`.

## Comparison of Solutions

### Time Complexity

- **Candidate Group Count Sweep**: `O(d × A²)` - each candidate checks every grade with a scan over `used_groups`, and the sweep stops at the answer `A`.
- **Interval Membership Check**: `O(n × d)` - up to `n` candidates, each validating `d` frequencies in constant time.

### Space Complexity

- **Candidate Group Count Sweep**: `O(d)` - one counter entry per distinct grade.
- **Interval Membership Check**: `O(d)` - one counter entry per distinct grade.

### Trade-offs

- **Candidate Group Count Sweep**: states the reachability test as the two raw bounds of the menu, which is easy to trust during an interview, but pays a linear scan per frequency per candidate.
- **Interval Membership Check**: needs one monotonicity argument to trust, then runs the same sweep with constant-time checks and no scanning at all.

### When to Use Each

- **Candidate Group Count Sweep**: when the candidate count is obviously small, or as the derivation step that motivates the interval check.
- **Interval Membership Check (Recommended)**: as the submission: same logic, worst-case bounds that no input can inflate beyond `O(n × d)`.

### Optimization Notes

- The sweep starts at `distinct_grades` because grade-pure groups force at least one group per grade, and its range stops at `total_servers` so `base_size` never reaches 0; letting `group_count` exceed `n` would drive `base_size` to 0 and the interval check to divide by zero.
- The candidate sweep always terminates by `group_count = n`, where every server forms its own size-1 group, so the fallback `return total_servers` is unreachable and exists to satisfy the type checker.
- Integer ceiling division `(frequency + base_size) // (base_size + 1)` avoids `math.ceil` on floats, which loses precision once frequencies exceed 2^53.
