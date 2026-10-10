# [Maximize Center A Package Benefit](https://www.fastprep.io/problems/amazon-center-a-package-benefit)

**Medium** | **NN minutes** | **Array, Greedy, Sorting**

Two distribution centers, A and B, must allocate n packages. Package i is worth benefitA[i] to Center A and benefitB[i] to Center B.

The array linkedPairs contains disjoint pairs [x, y]. For each linked pair, exactly one package goes to A and the other goes to B; A receives whichever of the two packages has the larger A-benefit. Packages that do not appear in any linked pair are independent.

Order the independent packages by decreasing benefitA[i] + benefitB[i], breaking a tie by smaller package index. Center A receives the first independent package in that order and then every other package; Center B receives the remaining independent packages.

## Examples

### Example 1

**Input:** `benefitA = [8,3,7,4]`, `benefitB = [1,9,2,6]`, `linkedPairs = [[0,1]]`

**Output:** `12`

**Explanation:** From linked pair [0,1], A takes package 0 for benefit 8. Independent packages 2 and 3 have combined benefits 9 and 10, so their order is 3,2. A receives package 3 for another 4, giving 12.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-center-a-package-benefit; fill them in. -->

## Solutions

### Linear Pair Scans

#### Derivation

The allocation rules are deterministic, so the literal reading simulates them rule by rule: settle every linked pair first, then sort the unlinked packages and hand them out alternately. The only bookkeeping question is which packages are unlinked, and the most direct answer is to search `linkedPairs` for each package in turn:

1. For each pair `[x, y]` in `linkedPairs`, add `max(benefitA[x], benefitA[y])` to `total_a`, since A receives whichever member has the larger A-benefit.
2. For each `package_index`, scan `linkedPairs`; a package no pair mentions is independent, so record the entry `(-combined, package_index)` where `combined = benefitA[package_index] + benefitB[package_index]`.
3. Sort the entries, which orders by decreasing combined benefit and breaks ties toward the smaller package index.
4. A receives the first independent package and then every other one, so add `benefitA` of the entries at even positions `0, 2, 4, ...` to `total_a` and return it.

#### Walkthrough

Let us run the rules by hand on Example 1: `benefitA = [8,3,7,4]`, `benefitB = [1,9,2,6]`, `linkedPairs = [[0,1]]`:

```text
pair [0,1]        benefitA 8 vs 3   A takes package 0            total_a = 8
package 0, 1      appear in [0,1]   linked, not independent
package 2         unlinked          combined 7+2 = 9             entry (-9, 2)
package 3         unlinked          combined 4+6 = 10            entry (-10, 3)
sorted entries    [(-10, 3), (-9, 2)]   independent order [3, 2]
position 0        A takes package 3, benefitA[3] = 4             total_a = 8 + 4 = 12
```

The alternation ends after one pick because only two independent packages exist: A gets the first, B gets the second. The function returns `12`, matching the expected Output for Example 1.

#### Solution

The code is the rule-by-rule transcription from the walkthrough: pair credits first, then the membership scan, the sort, and the stride-by-two handout.

```python
from typing import List


class Solution:
    def solve(self, benefitA: List[int], benefitB: List[int], linkedPairs: List[List[int]]) -> int:
        total_a = 0

        for first_package, second_package in linkedPairs:
            total_a += max(benefitA[first_package], benefitA[second_package])

        independent_entries = []
        for package_index in range(len(benefitA)):
            linked = False
            for pair_first, pair_second in linkedPairs:
                if package_index in (pair_first, pair_second):
                    linked = True
                    break
            if not linked:
                combined = benefitA[package_index] + benefitB[package_index]
                independent_entries.append((-combined, package_index))

        independent_entries.sort()
        for position in range(0, len(independent_entries), 2):
            package_index = independent_entries[position][1]
            total_a += benefitA[package_index]

        return total_a
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × p + m log m)`

With `n` packages, `p` linked pairs, and `m` independent packages, each package's membership scan walks all `p` pairs, and sorting the `m` entries adds `m log m`.

##### Space Complexity: `O(m)`

Only the list of `m` independent entries is stored beyond scalars.

#### Key Insights

- The rules leave nothing to search over: the pair winners, the ordering, and the alternation are all fixed, so a faithful simulation is automatically correct.
- Packing `(-combined, package_index)` into one tuple lets the sort apply both the decreasing-benefit order and the smaller-index tie-break without a custom comparator.
- The per-package membership scan is the only avoidable cost, and it re-reads the same pair list once per package.

### Partner Map

#### Derivation

The membership scan in the brute force walks all `p` pairs once per package, `O(n × p)` work that asks the same question, "which pair does this package belong to?", over and over. A [hash map](https://en.wikipedia.org/wiki/Hash_table) built in one pass over `linkedPairs` answers it in constant time: store each package's partner, and membership reduces to a key lookup. The rest of the simulation is unchanged:

1. In one pass over `linkedPairs`, set `partner_of[first_package] = second_package` and `partner_of[second_package] = first_package` for each pair, and add `max(benefitA[first_package], benefitA[second_package])` to `total_a`.
2. Classify each `package_index` with a single lookup: a package absent from `partner_of` is independent and becomes the entry `(-combined, package_index)`.
3. Sort the entries exactly as before and add `benefitA` of the entries at even positions to `total_a`.

#### Walkthrough

Let us rebuild the same allocation for Example 1: `benefitA = [8,3,7,4]`, `benefitB = [1,9,2,6]`, `linkedPairs = [[0,1]]`:

```text
pair [0,1]      partner_of = {0: 1, 1: 0}   A takes max(8, 3) = 8   total_a = 8
package 0       0 in partner_of             linked, not independent
package 1       1 in partner_of             linked, not independent
package 2       absent                      combined 9              entry (-9, 2)
package 3       absent                      combined 10             entry (-10, 3)
sorted entries  [(-10, 3), (-9, 2)]
position 0      A takes package 3, benefitA[3] = 4                 total_a = 12
```

The lookup replaces the pair scans, and every later step matches the brute force line for line. The function returns `12`, matching the expected Output for Example 1.

#### Solution

The code is the same simulation with every membership scan swapped for a `partner_of` lookup.

```python
from typing import List


class Solution:
    def solve(self, benefitA: List[int], benefitB: List[int], linkedPairs: List[List[int]]) -> int:
        partner_of = {}
        total_a = 0

        for first_package, second_package in linkedPairs:
            partner_of[first_package] = second_package
            partner_of[second_package] = first_package
            total_a += max(benefitA[first_package], benefitA[second_package])

        independent_entries = []
        for package_index in range(len(benefitA)):
            if package_index not in partner_of:
                combined = benefitA[package_index] + benefitB[package_index]
                independent_entries.append((-combined, package_index))

        independent_entries.sort()
        for position in range(0, len(independent_entries), 2):
            package_index = independent_entries[position][1]
            total_a += benefitA[package_index]

        return total_a
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + p + m log m)`

One pass builds the map over `p` pairs, one pass classifies `n` packages with constant-time lookups, and sorting the `m` independent entries costs `m log m`.

##### Space Complexity: `O(n)`

The `partner_of` map stores one entry per linked package, and the independent list adds up to `m <= n` entries.

#### Key Insights

- Building `partner_of` once converts the repeated pair scans into constant-time membership tests, the same trade the hash map makes in classic lookup problems.
- Because the pairs are disjoint, one dictionary entry per package endpoint is exact; no package ever appears in two pairs.
- The sort key and the stride-by-two handout are identical to the brute force, which keeps the optimized version easy to check against it.

## Comparison of Solutions

### Time Complexity

- **Linear Pair Scans**: `O(n × p + m log m)` - every package rescans the whole pair list to test membership.
- **Partner Map**: `O(n + p + m log m)` - one pass builds the map and lookups then cost constant time; the shared sort remains.

### Space Complexity

- **Linear Pair Scans**: `O(m)` - stores the independent entries only.
- **Partner Map**: `O(n)` - adds the `partner_of` map with one entry per linked package.

### Trade-offs

- Linear Pair Scans keeps all state in scalars and the entry list, and its membership test is hard to get wrong, but the double loop over packages and pairs dominates as both grow.
- Partner Map spends one dictionary to remove the double loop, paying linear extra memory for linear-time classification.

### When to Use Each

- **Linear Pair Scans**: Reasonable when packages number in the dozens or the pair list is tiny; also a compact reference implementation for testing.
- **Partner Map**: The default choice, since the map costs nothing conceptually and classification no longer depends on the pair count.

### Optimization Notes

- The tuple key `(-combined, package_index)` removes any need for a two-level comparator; negating the combined benefit turns "decreasing" into a plain ascending sort.
- `benefitB` values influence the result only through `combined`; B's own total is never needed, so no second accumulator exists to maintain.
- Only the `m` independent entries are sorted, never all `n` packages, so the sort cost stays proportional to the independent set the rules actually alternate over.
