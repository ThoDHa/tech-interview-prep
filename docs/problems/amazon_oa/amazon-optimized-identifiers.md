# [Optimize Identifiers](https://www.fastprep.io/problems/amazon-optimized-identifiers)

**Medium** | **NN minutes** | **String, Two Pointers**

In an Amazon inventory management, an operations analyst is dealing with a set of initial product identifiers represented by strings. The type of a string product identifier is determined by the first and last letters in the identifier string, for example, the type of the identifier string "abddaac" is "ac".



The analyst wants to optimize the product identifiers by performing a series of operations on the string to maximize the number of operation between the final and initial types. Given a product identifier string s, the analyst can perform one operation at a time, involving the removal of either the first or last letter from the string.



Find the maximum number of operations they can perform on the string while ensuring that its type aligns with the initial string's type.



Note: The type of an empty string" is", and the type of a string with a single character, like "a", is "aa".

## Examples

### Example 1

**Input:** `s = "hchc"`

**Output:** `2`

**Explanation:** The type of the initial string is "h", so the operations analyst can remove the first 2 or last 2 letters and get the string "h" with a type "h", hence the answer is 2.

### Example 2

**Input:** `s = "abbc"`

**Output:** `0`

**Explanation:** The operations analyst can't remove any letters from the string since the type will change, hence the answer is 0.

### Example 3

**Input:** `s = "babdcaac"`

**Output:** `0`

**Explanation:** The type of the initial string s is "bc":
Final String, Number of Operations, Type
babdcaac, 0, bc
bdcaac, 6, bc
d, 7, dd
bdc, 5, bc
babdc, 3, bc


From the above final strings, the only valid final strings (strings with a type equal to the type of the initial string "bc") are "babdcaac", "bdc", and "babdc" with a total of operations performed of 0, 5, and 3 respectively, hence the answer is 5.

## Constraints

- `2 ≤ |s| ≤ 2 * 10^5`
- `String s consists of lowercase English letters only.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
