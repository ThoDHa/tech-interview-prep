# [Get Min Distance (AMZ CN)](https://www.fastprep.io/problems/amazon-find-minimum-dist)

**Easy** | **NN minutes** | **Sorting, Greedy**

note - See the Problem Source at the vely bottom of the page for the original problem description~



In a realm where data centers and servers flourished along a mystical one-dimensional line, a wise ruler sought to optimize their connections. Each data center needed to establish a bond with a server, minimizing the lag defined as the absolute distance between their coordinates. Tasked with this quest, the ruler gathered the bravest minds to decipher the best pairings from the enchanted positions of the data centers and servers. Together, they embarked on a journey to forge connections that would ensure the smallest lag possible, bringing harmony to the kingdom's network and enhancing its magical efficiency.

## Examples

### Example 1

**Input:** `center = [1, 2, 2]`, `destination = [5, 2, 4]`

**Output:** `6`

**Explanation:** In a land where three connections needed to be forged, the positions of the data centers were as follows: center = [1, 2, 2], while the server destinations were located at: destination = [5, 2, 4].

To achieve the most efficient deliveries, the following connections were made:

a. The data center at location 1 established its first bond with the server at location 2.

b. The data center at location 2 then connected to the server at location 4.

c. Lastly, the other data center at location 2 formed a connection with the server at location 5.

The minimum total lag for these connections was calculated as follows: abs(1 - 2) + abs(2 - 4) + abs(2 - 5) = 1 + 2 + 3 = 6. Thus, the quest for optimization was successful, with a total lag of 6 uniting the realm of data centers and servers.

### Example 2

**Input:** `center = [3, 1, 6, 8, 9]`, `destination = [2, 3, 1, 7, 9]`

**Output:** `5`

**Explanation:** $23

## Constraints

- `1 <= n <= 105`
- `1 <= center[i], destination[i] <= 109`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
