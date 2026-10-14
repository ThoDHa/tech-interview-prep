# [Password Strength](https://www.fastprep.io/problems/amazon-password-strength)

**Medium** | **NN minutes** | **String, Greedy**

Sup! I might be a sister question of Password Strength 🐣



Your group at Amazon has recently set up a fresh verification rule for internal employee login credentials.



A credential consists solely of lowercase English alphabets and is deemed acceptable only if it includes at least one vowel and at least one consonant. The vowel set includes 'a', 'e', 'i', 'o', 'u'. All other letters are treated as consonants.



Given a text string representing the credential, determine and return its strength value. If the entire credential fails to meet the criteria, return 0.



Note: A piece refers to a sequence of neighboring characters taken from the original string, maintaining the same order.

## Examples

### Example 1

**Input:** `credential = "hackerrank"`

**Output:** `3`

**Explanation:** This credential can be broken down into three consecutive sections: "hack", "er", and "rank". Every section includes at least one vowel and one consonant.

It can be verified that the string cannot be split into more than three valid sections. Therefore, the strength value of the credential is 3.

## Constraints

- `1 ≤ |credential| ≤ 10 (the length of credential)`
- `Credential consists of lowercase English letters only.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
