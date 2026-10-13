# [Reverse Binary String](https://www.fastprep.io/problems/amazon-reverse-binary-string)

**Medium** | **NN minutes** | **String, Two Pointers, Greedy**

You are given a binary string. Find the minimum number of operations required to reverse it. An operation is defined as:
Remove a character from any index and append it to the end of the string.


Function Description 
Complete the function reverseBinaryString in the editor.



reverseBinaryString has the following parameter:



String s: a binary string
Returns 
int: the minimum number of operations required to reverse the binary string

## Examples

### Example 1

**Input:** `s = "00110101"`

**Output:** `3`

**Explanation:** Here is one way to reverse the string in 3 operations:



00110101 - 00101011 (index 3 was appended at the end)00101011 - 01010110 (index 0 was appended at the end)01010110 - 10101100 (index 0 was appended at the end)

So the answer here is 3 operations.

## Constraints

- `1 ≤ S.length ≤ 1e5`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
