# [Minimum Merge Conflicts](https://www.fastprep.io/problems/amazon-minimum-merge-conflicts)

**Hard** | **NN minutes** | **Dynamic Programming, String**

Special thanks: A special thank you to a lovely, amazing fren who shared that this question appeared again on September 17, 2026! 💜

Developers want to merge two source-control branches into one unified branch while preserving the relative order of commits from each branch.

Each branch is represented by a lowercase string. Each character represents a commit priority, where a lower alphabetical character has higher priority.

A conflict occurs when, in the merged branch, a lower-priority commit appears before a higher-priority commit. In other words, for positions i < j in the merged string, there is a conflict when merged[i] > merged[j].

Return the minimum possible number of conflicts over all valid merges of primary and secondary.

A valid merge must contain every character from both branches and preserve the original order within each input branch.

## Examples

### Example 1

**Input:** `primary = "zc"`, `secondary = "d"`

**Output:** `2`

**Explanation:** Valid merges include:

zcd with 2 merge conflicts (z being lower priority is placed before higher priority commits c and d).Similarly, zdc with 3 merge conflicts.Similarly, dzc with 2 merge conflicts.The minimum number of merge conflicts possible is 2.

### Example 2

**Input:** `primary = "dae"`, `secondary = "add"`

**Output:** `1`

**Explanation:** adadde has 1 merge conflict.

### Example 3

**Input:** `primary = "aaa"`, `secondary = "abb"`

**Output:** `0`

**Explanation:** aaaabb has no merge conflicts.

Added from a newer source found on June 24, 2026 🦒

## Constraints

- `1 <= |primary|, |secondary| <= 1000`
- `primary and secondary consist of lowercase English letters only.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
