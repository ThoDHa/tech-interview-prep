# [Max Consecutive ON Servers](https://www.fastprep.io/problems/amazon-get-max-consecutive-on)

**Hard** | **NN minutes** | **String, Sliding Window**

Special thanks: Barry contributed this problem.


Amazon operates a network of n machines. Some are currently inactive, while others are active. The engineers managing the infrastructure have access to a specific procedure that allows toggling the states of machines. In one use of this operation, they can select a continuous segment of machines and invert their statuses—turning active to inactive, and inactive to active. Due to certain restrictions, this procedure can be used at most k times.



You are given a binary string machine_status, of length n, where '1' indicates an active machine and '0' represents an inactive one, along with an integer max_flips that denotes the maximum number of operations allowed. Determine the highest possible number of adjacent active machines that can be achieved after at most max_flips operations.

## Examples

### Example 1

**Input:** `machine_status = "00010"`, `max_flips = 1`

**Output:** `4`

**Explanation:** The optimal approach is to perform one flip on the range of indices [0..2].

After flipping: "11110"

This results in a sequence of 4 consecutive active machines.

### Example 2

**Input:** `machine_status = "1001"`, `max_flips = 2`

**Output:** `4`

**Explanation:** You can flip indices [1..2] to obtain "1111".



Only one operation is needed to achieve a maximum of 4 continuous active machines.

There’s no advantage in using the second operation.

### Example 3

**Input:** `machine_status = "11101010110011"`, `max_flips = 2`

**Output:** `8`

**Explanation:** Flip indices [7..9]: "11101011000011"

Then flip [8..11]: "11101011111111"

This strategy yields a block of 8 active machines in a row.

## Constraints

- `1 ≤ n ≤ 2 * 10^5`
- `1 ≤ max_flips ≤ 2 * 10^5`
- `machine_status contains only 0s and 1s`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
