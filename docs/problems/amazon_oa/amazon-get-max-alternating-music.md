# [Get Max Alternating Music](https://www.fastprep.io/problems/amazon-get-max-alternating-music)

**Medium** | **NN minutes** | **String, Sliding Window**

Amazon Music is working on harmonizing their music playlist.



In their playlist system, each song is represented by a binary string music, where '0' and '1' denote two different types of music, say TypeA and TypeB. An "alternating music string" is one where no two adjacent songs are of the same type. For example, "1", "0", "10", "01", "101" are alternating music strings.



Given a binary string music representing the playlist and an integer k, you can perform up to k operations where each operation involves flipping a character, i.e., turning '0' into '1' and '1' into '0'.



As a developer at Amazon, the task is to determine the longest alternating substring that can be created from the music string by performing at most k operations.



Note:



A binary string is a sequence of '0' and '1' characters.
A string A is a substring of a string B if A can be obtained from B by deleting several (possibly, zero or all) characters from the beginning and several (possibly, zero or all) characters from the end.

## Examples

### Example 1

**Input:** `music = "1001"`, `k = 1`

**Output:** `3`

**Explanation:** By flipping the third character, the string becomes music = "1011". The longest alternating music string in this modified string is "101", which spans from the 0th index to the 2nd index and has a length of 3. With only one operation, it is not possible to obtain a longer alternating binary substring. Thus, the answer is 3.

## Constraints

- `🐼`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
