# [Rearrange Binary String](https://www.fastprep.io/problems/amazon-rearrange-binary-string)

**Medium** | **NN minutes** | **String, Greedy, Hash Table**

You are given a binary string, binary, consisting only of characters '0' and '1'. You are allowed to perform the following operation zero or more times:


Choose any subsequence of binary.Sort this subsequence.Replace the chosen subsequence in binary with its sorted version.
Additionally, you are given an array arr of length n, where each element of arr is a string of the same length as binary. Each string in arr consists of characters '0', '1', and the wildcard character '?'. The '?' character can be replaced with either '0' or '1' arbitrarily.



For each string in arr, after replacing every '?' character with either '0' or '1', you need to determine whether it is possible to rearrange the binary string into the modified string using the sorting operation described above. If it is possible, store "YES" as the corresponding answer; otherwise, store "NO".



Notes:



A subsequence of a string is obtained by deleting some (possibly zero) characters from the string without changing the order of the remaining characters.
Each computation for the elements of arr is independent of the others. The binary string is reset to its original state before checking each string in arr.

## Examples

### Example 1

**Input:** `binary = "101100"`, `arr = ["?110?1", "111???"]`

**Output:** `["YES", "NO"]`

**Explanation:** Consider the binary string binary = "101100" and the array arr = ["?110?1", "111???"].




For arr[0] = "?110?1", you can replace the '?' characters to form the string "011001". It is possible to rearrange the binary string into "011001" using the sorting operations:

Choose the subsequence {0, 2}, and sorting it transforms binary to "011100".
Choose the subsequence {3, 4, 5}, and sorting it transforms binary to "011001".

The answer for this element is "YES".


For arr[1] = "111???", no valid replacement of '?' characters allows the binary string to be rearranged to match the resulting string. Therefore, the answer is "NO".


Thus, the output for this case would be ["YES", "NO"].

## Constraints

- `🐵🐵`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
