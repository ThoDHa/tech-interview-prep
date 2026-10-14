# [Get Min Cost Data](https://www.fastprep.io/problems/get-min-cost-data)

**Medium** | **NN minutes** | **String, Greedy, Hash Table**

You are given a string data containing lowercase English letters and question marks. Replace every ? with a lowercase English letter.

The cost of a position is the number of earlier positions containing the same letter. Equivalently, if a letter appears f times in the completed string, it contributes f * (f - 1) / 2 to the total cost.

Return a completed string with the minimum possible total cost. If several completed strings have that minimum cost, return the lexicographically smallest one.

## Examples

### Example 1

**Input:** `data = "aaaa?aaaa"`

**Output:** `"aaaabaaaa"`

**Explanation:** Replacing ? with b creates no additional equal-letter pair and is the lexicographically smallest minimum-cost choice.

### Example 2

**Input:** `data = "??????"`

**Output:** `"abcdef"`

**Explanation:** Using six distinct letters gives total cost 0. Sorting the chosen letters produces the smallest such string, abcdef.

### Example 3

**Input:** `data = "abcd?"`

**Output:** `"abcde"`

**Explanation:** Choosing a through d would repeat an existing letter and add cost. The smallest unused letter is e, so abcde has minimum cost 0.

## Constraints

- `1 <= data.length <= 10^5`
- `data contains lowercase English letters and ? only.`
- `data contains at least one ?.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
