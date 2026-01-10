# Group Anagrams

## Difficulty: Medium
## Pattern: Hashmap (Grouping)

## Problem Statement

Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

An anagram is a word formed by rearranging the letters of another word using all the original letters exactly once.

## Examples

```
Input: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

Input: strs = [""]
Output: [[""]]

Input: strs = ["a"]
Output: [["a"]]
```

## Constraints

- 1 <= strs.length <= 10^4
- 0 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters

## Time/Space Targets

- Time: O(n * k log k) where k is max string length
- Space: O(n * k)

