# [Max Transfer Rate](https://www.fastprep.io/problems/amazon-max-transfer-rate)

**Easy** | **NN minutes** | **Greedy, Sorting, Math**

You are in the Amazon's Cloud Infrastructure Team, and you are working on a project to optimize how data flows through its network of storage servers.



You are given with n storage servers, and the throughput capacity of each server is given in an integer array named throughput.



There are pipelineCount data pipelines that need to be connected to two storage servers, one as the primary connection and the other as the backup. Each data pipeline must choose a unique pair of servers for its connections.



The transferRate for each data pipeline is defined as the sum of the throughput of its primary and backup servers.



Given an integer array throughput and an integer pipelineCount, find the maximum total transferRate that can be obtained by optimally choosing unique pairs of connections for each data pipeline.



Note:



A pair of servers (x, y) is said to be unique if no other pipeline has selected the same pair. However, the pairs (y, x) and (x, y) are treated as different connections.
It is also possible to select the same server for primary and backup connections, which means that (x, x) is a valid pair for the connection.

## Examples

### Example 1

**Input:** `throughput = [4, 2, 5]`, `pipelineCount = 4`

**Output:** `36`

**Explanation:** The data pipelines can select their connection among the following 9 possible server pairs:

[1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]
(Assuming 1-based indexing of throughput array).

However, each data pipeline must select a unique pair of servers.

To achieve the maximum total transferRate, the data pipelines can optimally choose the pairs [3, 3], [1, 3], [3, 1], [1, 1] to obtain the maximum sum of transferRate = (5 + 5) + (5 + 4) + (4 + 5) + (4 + 4) = 36.

## Constraints

- `:)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
