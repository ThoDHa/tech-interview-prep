# [Remove Characters in Frequency Order](https://www.fastprep.io/problems/amazon-remove-characters-in-frequency-order)

**Hard** | **NN minutes** | **String, Dynamic Programming**

(Look into LC 664. Strange Printer may help :)



Given a string, determine the minimum number of operations (deletions) required to make the string empty.



You can perform the deletion operation as many times as you prefer::



Pick any group of consecutive chars in the string, with a group size s ranging from 1 up to the curr len of the string. Delete them only when all the chars in this group are the same.
Function Description 
Complete the function minimumOperationsToRemove in the editor.



minimumOperationsToRemove has the following parameter:



String s: the string to be processed
Returns 
int: the minimum number of operations required

## Examples

### Example 1

**Input:** `s = "abaca"`

**Output:** `3`

**Explanation:** Pick s = 1: remove "b" -> "aaca"
Pick s = 1: remove "c" -> "aaa"
Pick s = 3: since all the a's are together remove all a's at once. Now it is empty.

We can make the input string empty in just 3 operations. So, we return 3 as the answer.

## Constraints

- `TO-DO`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
