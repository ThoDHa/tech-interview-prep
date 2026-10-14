# [Find Max Num](https://www.fastprep.io/problems/amazon-find-maximum-num)

**Easy** | **NN minutes** | **Array, Greedy, Sorting**


Your team at AmzAn is building a quiz-style application to help students prepare for certification exams. Each quiz module tests one or more subjects and limits the number of review attempts each student has been asked to examine. To do this, please review each of the certification exams provide. You have within quiz modules answered[i] questions in each allows students to "pass" certain subjects with a total of q more questions overall. For each answer the following: Imagine a student has already answered needed[i] in order to pass. For each of the n subjects, and still has answered has to be at least pass if the q additional answered of the subject, the number of questions the student can pass determine the maximum number among the subjects. The questions are optimally distributed.



For example, consider that there are n = 2 subjects and needed = [4, 5] answered questions, respectively, to pass. Imagine another q = 1 questions across all subjects combined. In that case, the best outcome is to answer an additional question in the second subject, in order to pass it, as 2 more answers are required to pass the first subject. The maximum number of subjects that can be passed is 1.

## Examples

### Example 1

**Input:** `answered = [24, 27, 0]`, `needed = [51, 52, 100]`, `q = 100`

**Output:** `2`

**Explanation:** Here answered=[24,27,0] and needed=[51,52,100]. The additional answers needed to pass are [27,25,100]. The best distribution is at least 27+25=52 questions among the first two subjects. It would take all q=100 questions to pass the third subject.

### Example 2

**Input:** `answered = [24, 27, 0]`, `needed = [51, 52, 100]`, `q = 200`

**Output:** `3`

**Explanation:** Explanation not found. If you happen to know about it, feel free to lmk! Manyyy thx in advance 🫰

### Example 3

**Input:** `answered = [2, 4]`, `needed = [4, 5]`, `q = 1`

**Output:** `1`

**Explanation:** There are n = 2 subjects and needed = [4, 5] answered questions, respectively, to pass. The student has answered answered = [2, 4] questions in the two subjects so far, and can answer another q = 1 questions in all subjects combined. The best outcome is to answer an additional question in the second subject to pass it, and it is not possible to pass the first subject. The maximum num of subjects that can be passed is 1 :)

## Constraints

- `1 ≤ n ≤ 10^5`
- `0 ≤ answered[i], needed[i], q ≤ 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
