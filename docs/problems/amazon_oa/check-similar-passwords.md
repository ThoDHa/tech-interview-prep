# [Check Similar Passwords](https://www.fastprep.io/problems/check-similar-passwords)

**Medium** | **NN minutes** | **String, Two Pointers**

Amazon would like to enforce a password policy for password changes. For each pair of strings newPasswords[i] and oldPasswords[i], determine whether the two passwords are similar.

To test similarity, you may choose any set of indices in newPasswords[i], including the empty set. Each chosen character is changed exactly once to its next cyclic lowercase character: 'a' becomes 'b', 'b' becomes 'c', and 'z' becomes 'a'. Characters at indices not chosen remain unchanged.

The passwords are similar if, after applying the operation to the new password, oldPasswords[i] is a subsequence of the transformed new password.

A subsequence is a sequence that can be derived from another sequence by deleting zero or more characters without changing the order of the remaining characters.

Return an array of strings where the i-th result is "YES" if oldPasswords[i] can be made a subsequence of newPasswords[i] using the operation above, and "NO" otherwise.

## Examples

### Example 1

**Input:** `newPasswords = ["baacbab", "accdb", "baacba"]`, `oldPasswords = ["abdbc", "ach", "abb"]`

**Output:** `["YES", "NO", "YES"]`

**Explanation:** For the first pair, choose indices 3, 4, and 7 in "baacbab" using 1-based indexing. The selected characters "a", "c", and "b" become "b", "d", and "c", so "abdbc" is a subsequence of the transformed password.

For the second pair, no choice of indices can make "ach" a subsequence of "accdb", because no transformed character can become 'h'.

For the third pair, "abb" can be matched as a subsequence after choosing an appropriate subset of indices.

### Example 2

**Input:** `newPasswords = ["aaccbbee", "aab"]`, `oldPasswords = ["bdbf", "aee"]`

**Output:** `["YES", "NO"]`

**Explanation:** For newPasswords[0] = "aaccbbee" and oldPasswords[0] = "bdbf", choose characters so the transformed new password contains "bdbf" as a subsequence.

For newPasswords[1] = "aab" and oldPasswords[1] = "aee", there is no way to obtain two 'e' characters as a subsequence, so the answer is "NO".

## Constraints

- `1 <= n <= 10`
- `newPasswords.length == oldPasswords.length == n`
- `1 <= oldPasswords[i].length <= newPasswords[i].length`
- `The total length of all strings in newPasswords and oldPasswords does not exceed 2 * 10^5.`
- `All passwords consist of lowercase English letters.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
