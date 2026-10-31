# [Word Dictionary with Wildcard Find](https://www.fastprep.io/problems/amazon-wildcard-word-dictionary)

**Medium** | **NN minutes** | **Trie, String, Depth First Search, Design**

Build a word dictionary that supports inserting words and finding words with wildcards. Process the rows of operations from left to right. The dictionary starts empty, and each row has one of these forms:

["insert", word] adds word to the dictionary. Inserting a word that is already present changes nothing.
["find", pattern] asks whether the dictionary currently holds at least one word that matches pattern.

A pattern matches a word when both have the same length and, at every position, the pattern character is either the same letter or a period .. A period is a wildcard that matches exactly one lowercase letter. It never matches zero letters or more than one letter.

## Examples

### Example 1

**Input:** `operations = [["insert","cat"],["insert","car"],["insert","cart"],["find","ca."],["find","c..t"],["find","ca"],["find","d.."]]`

**Output:** `[true,true,false,false]`

**Explanation:** The pattern ca. matches both cat and car, so the first answer is true. The pattern c..t has length 4 and matches cart. No stored word has length 2, so ca is false. Every stored word starts with c, so d.. is false.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-wildcard-word-dictionary; fill them in. -->

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
