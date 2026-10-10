# [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)

**Hard** | **40 minutes** | **Array, String, Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort**

> This problem is locked behind [LeetCode Premium](https://leetcode.com/problems/alien-dictionary/); read it free on [NeetCode](https://neetcode.io/problems/foreign-dictionary).

**Pattern:** [Topological Sort](../patterns/topological_sort/intuition.md)

**Algorithm:** [Topological sorting](https://en.wikipedia.org/wiki/Topological_sorting) · [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn%27s_algorithm) · [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)

**Practice:** [`practice/alien_dictionary/solution.py`](../../practice/alien_dictionary/solution.py)

There is a new alien language that uses the English alphabet, but the order of the letters is unknown.

You are given a list of strings `words` from the alien language's dictionary. It is claimed that the strings in `words` are sorted lexicographically by the rules of this new language.

If this claim is incorrect, and the given arrangement of strings in `words` cannot correspond to any order of letters, return `""`.

Otherwise, return a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules. If there are multiple solutions, return **any** of them.

A string `a` is lexicographically smaller than a string `b` if either of the following is true:
* The first letter where they differ is smaller in `a` than in `b`.
* `a` is a prefix of `b` *and* `a.length < b.length`.

## Examples

### Example 1

**Input:** `words = ["z","o"]`

**Output:** `"zo"`

**Explanation:** From `"z"` and `"o"`, we know `'z' < 'o'`, so return `"zo"`.

### Example 2

**Input:** `words = ["hrn","hrf","er","enn","rfnn"]`

**Output:** `"hernf"`

**Explanation:** * from `"hrn"` and `"hrf"`, we know `'n' < 'f'`
* from `"hrf"` and `"er"`, we know `'h' < 'e'`
* from `"er"` and `"enn"`, we know `'r' < 'n'`
* from `"enn"` and `"rfnn"` we know `'e' < 'r'`
* so one possible solution is `"hernf"`

### Example 3

**Input:** `words = ["abc","ab"]`

**Output:** `""`

**Explanation:** The second word is a prefix of the first word, but the first word appears before the second. This is impossible in a valid lexicographical ordering, so return `""`.

## Constraints

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 100`
- `words[i]` consists of only lowercase English letters.

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See _TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
