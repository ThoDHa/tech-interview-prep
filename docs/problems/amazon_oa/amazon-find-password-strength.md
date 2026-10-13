# [Find Password Strength](https://www.fastprep.io/problems/amazon-find-password-strength)

**Medium** | **NN minutes** | **String, Hash Table**

Hello! Did you navigate here from my sister question Password Strength 🐣?



Another check pwd strength question you might be interested in:



Find the password strength for a given password. For example, if the password is "good", 
then iterate over all substrings and find the distinct character counts:



g = 1,
o = 1,
o = 1,
d = 1,
go = 2,
oo = 1,
od = 2,
goo = 2,
ood = 2,
good = 3

At the end, add all the distinct character counts to determine the password strength. In this case, the password strength is 16.

## Examples

### Example 1

**Input:** `password = "good"`

**Output:** `16`

**Explanation:** Iterate over all substrings and find the distinct character counts:




g = 1,
o = 1,
o = 1,
d = 1,
go = 2,
oo = 1,
od = 2,
goo = 2,
ood = 2,
good = 3


The total strength is the sum of all distinct character counts: 1 + 1 + 1 + 1 + 2 + 1 + 2 + 2 + 2 + 3 = 16.

### Example 2

**Input:** `password = "aa"`

**Output:** `2`

**Explanation:** Iterate over all substrings and find the distinct character counts:

"a"
"a"
"aa"

We return 2 because both "a" and "a" have dictinct character counts of 1.

1 + 1 = 2

This case was added on 03-22-2025 :) Here is the source img -

## Constraints

- `🐈`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
