# [Find Minimum Inefficiency](https://www.fastprep.io/problems/find-minimum-inefficiency)

**Medium** | **NN minutes** | **Dynamic Programming, String**


Amazon Web Service has n servers, each of them either has high fault tolerance or high reliability. 
A system works better if all the servers have the same attributes. The inefficiency of a group of 
server is defined as the number of adjacent pairs of server that have different attributes.



Consider, for example, a set of servers described as 1001001 where '0' means the server has 
high fault tolerance, '1' means the server has high reliabiity. The inefficiency of this group is 4 as 
described in the image below:




Given a string serverType of length n
consisting of '0', '1', and '?', where '0' means the server has high fault 
tolerance, '1' means the server has high reliability, and '?' means you can install any
type of server there, find the minimum inefficiency you can get after install a server at each '?'.


Complete the function findMinimumInefficiency in the editor.

findMinimumInefficiency has the following parameter:

string serverType: the server typesint: the minimum possible inefficiency

## Examples

### Example 1

**Input:** `serverType = "??011??0"`

**Output:** `2`

**Explanation:** In the above example, the number of servers n = 8. One optimal way to install servers is to

Install a server having fault tolerance (0) at the first and the second positions.Install a server having high reliability (1) at the sixth and the seventh positions.After making these changes, the server types are '00011110'. The number of adjacent pairs having different server types is 2. It can be shown that the answer cannot be reduced from 2. Return 2.

Note that another possible way to achieve a minimum number of different adjancet pairs as 2 would 00011100 and 00011000.

### Example 2

**Input:** `serverType = "00?10??1?"`

**Output:** `3`

**Explanation:** One optimal way to install servers is to install high-reliability servers at every '?'. The new server types are "001101111" with 3 adjacent dissimilar pairs. Return 3.

## Constraints

- `1 <= n <= 10^5`
- `serverType consists of '0', '1' and '?' only`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
