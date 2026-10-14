# [Find Min Time Required](https://www.fastprep.io/problems/amazon-find-minimum-time-required)

**Medium** | **NN minutes** | **String, Greedy, Hash Table**

Some developers at Amazon are building a prototype for a simple rate-limiting algorithm. There are n requests to be processed by the server represented by a string requests where the ith character represents the region of the ith client. Each request takes 1 unit of time to process. There must be a minimum time gap of minGap units between any two requests from the same region.



The requests can be sent in any order and there can be gaps in transmission for testing purposes. Find the minimum amount of time required to process all the requests such that no request is denied.

## Examples

### Example 1

**Input:** `requests = "abacadaeafag"`, `minGap = 2`

**Output:** `16`

**Explanation:** One optimal strategy is "ab_ad_afgae_ac_a".

### Example 2

**Input:** `requests = "aaabbb"`, `minGap = 0`

**Output:** `6`

**Explanation:** Since the minGap is 0, the requests can be processed in any order without any gaps.

### Example 3

**Input:** `requests = "aaabbb"`, `minGap = 2`

**Output:** `8`

**Explanation:** The requests can be sent in order "ab_ab_ab" wher _ represents that no request was sent. Here, the min time gap between two requests from the same region is minGap = 2. The total time taken is 8 units :)

## Constraints

- `🍓`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
