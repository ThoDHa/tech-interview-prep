# [Get Max Pairs](https://www.fastprep.io/problems/amazon-get-max-pairs)

**Easy** | **NN minutes** | **Array, Sorting, Greedy, Two Pointers**

An AWS client wants to deploy multiple applications and needs two servers, one for their frontend and another for their backend. They have a list of integers representing the quality of servers in terms of availability. The client's preference is that the availability of an application's frontend server must be greater than that of its backend.



Two arrays of same size n, frontend[n] and backend[n] where elements represent the quality of the servers, create pairs of elements (frontend[i], backend[i]) such that frontend[i] > backend[i] in each pair. Each element from an array can be picked only once to form a pair, Find the maximum number pairs that can be formed.

## Examples

### Example 1

**Input:** `frontend = [1, 2, 3]`, `backend = [1, 2, 1]`

**Output:** `2`

**Explanation:** The possible valid pairs which can be made are:



(frontend[1], backend[0])=(2, 1) and (frontend[2], backend[2])=(3, 1) are valid pairs.(frontend[1], backend[0])=(2, 1) and (frontend[2], backend[1])=(3, 2) are valid pairs.

It can be seen that a maximum of 2 valid pairs can be made at a time. So the maximum number of pairs that can be formed is 2. Return 2.

## Constraints

- `N/A`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
