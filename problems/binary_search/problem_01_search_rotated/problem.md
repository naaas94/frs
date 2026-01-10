# Search in Rotated Sorted Array

## Difficulty: Medium
## Pattern: Binary Search

## Problem Statement

Given a rotated sorted array `nums` (rotated at some pivot) and a target value, return the index of target if it exists, or -1 if it doesn't.

The array was originally sorted in ascending order and then rotated.

## Examples

```
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Input: nums = [1], target = 0
Output: -1
```

## Constraints

- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values in nums are unique
- nums is rotated at some pivot

## Time/Space Targets

- Time: O(log n)
- Space: O(1)

