# [Min Retailers](https://www.fastprep.io/problems/amazon-minimum-retailers)

**Hard** | **NN minutes** | **Intervals, Sorting, Greedy**

An online marketplace has onboarded n retailers, each operating within a designated geographical range. Retailer i operates over the interval from regionStart[i] to regionEnd[i] (inclusive on both ends).

A set of k retailers is said to be inclusive if there exists at least one retailer in the set whose operating interval intersects (overlaps with, or touches at an endpoint) the interval of each of the other k - 1 retailers individually. In other words, some chosen retailer must pairwise intersect every other retailer in the set; the other retailers do not need to intersect one another.

The marketplace wants to relocate some retailers to a different location. A relocated retailer is removed from the remaining set (it no longer participates in forming the inclusive set). Determine the minimum number of retailers that must be relocated so that the remaining retailers form an inclusive set.

Equivalently, if you select one retailer i to act as the hub, every retained retailer's interval must intersect retailer i's interval, and all retailers whose intervals do not intersect retailer i's interval must be relocated. The answer is the minimum number of relocations over all possible choices of hub, i.e. n minus the maximum, over all i, of the number of intervals (including i itself) that intersect interval i.

Complete the function minimumRetailers in the editor below.

minimumRetailers has the following parameters:

int regionStart[n]: the left ends of the operating regionsint regionEnd[n]: the right ends of the operating regionsint: the minimum number of retailers to relocate

## Examples

### Example 1

**Input:** `zoneStart = [1, 3, 4, 6, 9]`, `zoneEnd = [2, 8, 5, 7, 10]`

**Output:** `2`

**Explanation:** Intervals: retailer 1 = [1, 2], retailer 2 = [3, 8], retailer 3 = [4, 5], retailer 4 = [6, 7], retailer 5 = [9, 10]. Choosing retailer 2 ([3, 8]) as the hub: it intersects retailer 3 ([4, 5]) and retailer 4 ([6, 7]), but not retailer 1 ([1, 2]) or retailer 5 ([9, 10]). So retailers 2, 3, 4 already form an inclusive set of size 3. Relocating retailers 1 and 5 leaves an inclusive set, requiring 2 relocations, which is the minimum.

### Example 2

**Input:** `zoneStart = [1, 2, 3, 4]`, `zoneEnd = [2, 3, 5, 5]`

**Output:** `1`

**Explanation:** Region 1 (1, 2) intersects only region 2. (move regions 3 and 4)

Region 2 (2, 3) intersects regions 1 and 3. (move region 4)

Region 3 (3, 5) intersects regions 2 and 4. (move region 1)

Region 4 (4, 5) intersects region 3. (move regions 1 and 2)

The minimum number of moves is 1, moving region 1 or 4

### Example 3

**Input:** `zoneStart = [1, 2, 4]`, `zoneEnd = [7, 5, 6]`

**Output:** `0`

**Explanation:** Intervals: retailer 1 = [1, 7], retailer 2 = [2, 5], retailer 3 = [4, 6]. Choosing retailer 1 ([1, 7]) as the hub: it intersects retailer 2 ([2, 5]) and retailer 3 ([4, 6]). All three retailers are retained with retailer 1 as the hub, so the set is already inclusive and no relocations are needed. The answer is 0.

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ regionStart[i] ≤ regionEnd[i] ≤ 10^9 (for each i, 0 ≤ i < n)`
- `Multiple regions may share the same start and end points.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
