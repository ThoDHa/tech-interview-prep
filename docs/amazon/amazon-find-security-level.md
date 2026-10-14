# [Find Security Level](https://www.fastprep.io/problems/amazon-find-security-level)

**Hard** | **NN minutes** | **Array, Prefix Sum, Hash Table**

Source said that the other problem 👇 in the same batch was for Newe Grad, so I assume this problem is for New Grad as well.  


Segmentify: Minimum Subsegments 🦔
Amazon is launching a revolutionary security feature that incorporates an advanced antivirus program, adept at identifying and halting potential threats. This framework manages n active programs, each with a unique Program Identifier (PID).



The antivirus program evaluates the overall security risk of the system using a specialized algorithm.



• The algorithm analyzes contiguous subarrays of Program Identifiers (PIDs) represented by the array pid. 
• For each subarray, it calculates the sum of the PIDs and divides this sum by a given integer k. 
• The remainder obtained from this division is compared to the number of programs in the subarray. 
• A subarray is flagged if the remainder equals the number of programs within it and is considered as malicious. 
• The overall security risk is determined by the total count of such flagged subarrays.



Formally, given an array pid of size n, representing the PIDs of the programs running on the computer, and an integer k, with which remainder has to be checked. The task is to calculate the system's security risk level.



Note: 
• Remainder is defined as the remaining part after performing the division. For example, the remainder of 13 with 5 is 3. 
• A subarray is a continuous portion of an array. For example, in the array [5, 7, 9, 11], possible subarrays include [5, 7], [7, 9, 11], [11] etc. Note that a subarray maintains the original order of elements and consists of consecutive elements.

## Examples

### Example 1

**Input:** `pid = [1, 3, 2, 4]`, `k = 4`

**Output:** `2`

**Explanation:** $24

## Constraints

- `1 ≤ n ≤ 2×10^5`
- `1 ≤ pid[i] ≤ 10^9`
- `1 ≤ k ≤ 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
