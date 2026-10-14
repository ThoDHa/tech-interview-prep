# [Get Min Subsegments](https://www.fastprep.io/problems/amazon-get-min-subsegments)

**Hard** | **NN minutes** | **Dynamic Programming, Greedy, String**

Amazon Prime Video is developing a new feature called "Segmentify." This feature applies to a video with n (even) visual frames, where each frame is represented by a binary character in the array frames. In this format, a "0" represents a black pixel, and a "1" represents a white pixel.

Due to factors like lighting and camera angles, some frames may need horizontal or vertical flips (changing "0"s to "1"s and vice versa) to create consistent visuals. The objective is to divide the video into subsegments so that all frames in a subsegment are visually identical (i.e., the frames in a subsegment are either all "0"s or all "1"s). Additionally, each subsegment should have an even length.

The goal is to accomplish this segmentation with two criteria in mind:

Minimize the number of flips required to form valid segments, let this be denoted by B.Among all configurations requiring B flips, minimize the total number of subsegments.Given the binary string frames, determine the minimum number of even-length subsegments that can be created while utilising the least number of flips.

Note: A subsegment is a segment that can be derived from another segment by deleting some elements without changing the order of the remaining elements.

## Examples

### Example 1

**Input:** `frames = "1110011000"`

**Output:** `2`

**Explanation:** So, the length of all subsegments - (11111111 and 00)is even.

So again, the minimum number of subsegments that frames can be divided into to make it "Segmentify-compliant" is 2 with minimum flips of 3.

Hence answer is 2.

### Example 2

**Input:** `frames = "110011"`

**Output:** `3`

**Explanation:** Another example, frames = "110011", In this example, the string already consists of groups of "0"s and "1"s that have even lengths. Therefore, no flipping is necessary, and the string can be divided into 3 even-length subsegments without modification. Hence, the answer is 3. Recall that we need to minimize flips first and give that priority before minimizing segments.

### Example 3

**Input:** `frames = "100110"`

**Output:** `1`

**Explanation:** Flip the first 0 to 1. So, frames = "110110".

~~ Again flip the first 0 to 1. So, frames = "111110".

~~ At last, again flip the first 0 to 1. So, frames = "111111".

Hence, the length of the only segment formed is even. So, the minimum number of subsegments that s can be divided to make it fine is 1 with minimum flips of 3. Hence, the answer is 1.

## Constraints

- `2 ≤ n ≤ 10^5, where n is the length of frames and is even.`
- `It is guaranteed that the string frames only consists of 0s and 1s.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
