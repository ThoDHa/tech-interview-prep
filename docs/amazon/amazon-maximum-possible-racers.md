# [Maximum Possible Racers](https://www.fastprep.io/problems/amazon-maximum-possible-racers)

**Medium** | **NN minutes** | **Sliding Window, Hash Table**

HackerLand Sports Club wants to send a team for a relay race. There are n racers in the group indexed from 0 to n. The ith racer has a speed of speed[i] units.



The coach decided to send some contiguous subsegments of racers for the race i.e. racers with index i, i+1, i+2..., such that each racer has the same speed in the group to ensure smooth baton transfer. To achieve the goal, the coach decided to remove some racers from the group such that the number of racers with the same speed in some contiguous segment is maximum.



Given the array, racers, and an integer k, find the maximum possible number of racers in some contiguous segment of racers with the same speed after at most k racers are removed.

## Examples

### Example 1

**Input:** `speed = [1, 4, 4, 2, 2, 4]`, `k = 2`

**Output:** `4`

**Explanation:** It is optimal to remove the two racers with speed 2 to get the racers [1, 4, 4, 4, 4]. Each racer with speed 4 can now be sent as they are in a contiguous segment. A maximum of 4 racers can be sent for the relay race.

## Constraints

- `🍉🍉`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
