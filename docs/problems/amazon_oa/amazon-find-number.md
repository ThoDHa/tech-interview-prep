# [Find Number](https://www.fastprep.io/problems/amazon-find-number)

**Medium** | **NN minutes** | **Math, Combinatorics, Dynamic Programming**

In order to ensure maximum security, the developers at Amazon employ multiple encryption methods to keep user data protected.



In one method, numbers are encrypted using a scheme called 'Pascal Triangle'. When an array of digits is fed to this system, it sums the adjacent digits. It then takes the rightmost digit (least significant digit) of each addition for the next step. Thus, the number of digits in each step is reduced by 1. This procedure is repeated until there are only 2 digits left, and this sequence of 2 digits forms the encrypted number.



Given the initial sequence of the digits of numbers, find the encrypted number. You should report a string of digits representing the encrypted number.

## Examples

### Example 1

**Input:** `numbers = [4, 5, 6, 7]`

**Output:** `"04"`

**Explanation:** Encryption occurs as follows:



Hence, the encrypted number formed is 04.

## Constraints

- `2 ≤ numbers.length ≤ 5 · 10^3`
- `0 ≤ numbers[i] ≤ 9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
