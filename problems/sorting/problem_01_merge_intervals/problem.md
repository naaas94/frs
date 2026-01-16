# Merge Intervals

## Difficulty: Medium
## Pattern: Sorting + Key Functions

## Problem Statement

Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return an array of the non-overlapping intervals that cover all the intervals in the input.

## Examples

```
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: [1,3] and [2,6] overlap, merge into [1,6]

Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: [1,4] and [4,5] are considered overlapping (touching)
```

## Constraints

- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start_i <= end_i <= 10^4

## Time/Space Targets

- Time: O(n log n) for sorting
- Space: O(n) for output


