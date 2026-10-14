# [Rice Bags](https://www.fastprep.io/problems/max-set-size)

**Medium** | **NN minutes** | **Hash Table, Dynamic Programming**

You are shopping on Amazon.com for some bags of rice. Each listing displays the number of grains of rice that the bag contains. You want to buy a perfect set of rice bags chosen from the entire search results list, riceBags.

A perfect set of rice bags, perfect, is defined as:

The set contains at least two bags of rice.When the selected bags are sorted in increasing order by grain count, every adjacent pair satisfies perfect[i] * perfect[i] = perfect[i + 1]. In other words, each grain count must be the exact square of the previous grain count.Each bag from riceBags can be used at most once, and values that are not present in riceBags cannot be inserted into the set. All values in riceBags are distinct, and riceBags[i] >= 2, so a value of 1 will never appear.

Find the largest possible perfect set and return the size of that set. If no perfect set is possible, return -1.

## Examples

### Example 1

**Input:** `riceBags = [625, 4, 2, 5, 25]`

**Output:** `3`

**Explanation:** After sorting each selected set, the possible perfect sets include [5, 25], [2, 4], and [5, 25, 625]. The largest perfect set has size 3.

### Example 2

**Input:** `riceBags = [3, 9, 4, 2, 16]`

**Output:** `3`

**Explanation:** The possible perfect sets include [3, 9], [2, 4], [4, 16], and [2, 4, 16]. The largest perfect set has size 3.

## Constraints

- `1 <= n <= 2 * 10^5`
- `2 <= riceBags[i] <= 10^6`
- `All elements of riceBags are distinct.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
