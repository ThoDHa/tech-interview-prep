# [Word Ladder](https://www.fastprep.io/problems/amazon-word-ladder)

**Hard** | **NN minutes** | **Breadth First Search, Graph, String**

You are given beginWord, endWord, and a dictionary wordList. A transformation changes exactly one character, and every transformed word—including endWord—must appear in the dictionary.

Return the number of words in the shortest valid sequence from beginWord through endWord, counting both endpoints. Return 0 when no sequence exists. If the two endpoints are equal, the answer is 1 only when that word appears in the dictionary.

## Examples

### Example 1

**Input:** `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`

**Output:** `5`

**Explanation:** One shortest sequence is hit -> hot -> dot -> dog -> cog, which contains five words.

### Example 2

**Input:** `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log"]`

**Output:** `0`

**Explanation:** The endpoint is absent from the dictionary, so no valid ladder exists.

### Example 3

**Input:** `beginWord = "same"`, `endWord = "same"`, `wordList = ["same","came"]`

**Output:** `1`

**Explanation:** The endpoints already match and the endpoint appears in the dictionary.

## Constraints

- `1 <= beginWord.length == endWord.length <= 10.`
- `1 <= wordList.length <= 5000.`
- `Every dictionary word has the same length as beginWord.`
- `Words contain only lowercase English letters.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
