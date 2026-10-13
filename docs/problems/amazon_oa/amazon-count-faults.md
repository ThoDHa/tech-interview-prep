# [Count Faults (Faulty Binding 101 😁)](https://www.fastprep.io/problems/amazon-count-faults)

**Easy** | **NN minutes** | **Simulation, Hash Table, String**

There are n servers with IDs s1, s2, ..., sn. You are given an array logs in chronological order. Each entry has the form "<server_id> <status>", where status is either success or error.

Track consecutive errors separately for each server. An entry for another server does not interrupt a server's streak. A success resets that server's streak to zero. Whenever a server reaches three consecutive errors, it is considered faulty and is immediately replaced by a new server with the same ID; after replacement, that ID's error streak also resets to zero.

Return the total number of server replacements recorded while processing all logs.

## Examples

### Example 1

**Input:** `n = 2`, `logs = ["s1 error", "s1 error", "s2 error", "s1 error", "s1 error", "s2 success"]`

**Output:** `1`

**Explanation:** Server s1 logs errors on its first, second, and third requests. The intervening request for s2 does not break s1's streak, so s1 is replaced after its third error. Its following error starts a new streak. Server s2 never reaches three consecutive errors because its later success resets its streak. Therefore, exactly one replacement occurs.

## Constraints

- `1 <= n <= 200`
- `1 <= logs.length <= 2 * 10^4`
- `Every log contains one of the server IDs s1 through sn followed by either success or error.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
