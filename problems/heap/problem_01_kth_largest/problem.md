# Kth Largest Element in Array

## Difficulty: Medium
## Pattern: Heap / Top-K

## Problem Statement

Given an integer array `nums` and an integer `k`, return the kth largest element in the array.

Note that it is the kth largest element in sorted order, not the kth distinct element.

## Examples

```
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5

Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
```

## Constraints

- 1 <= k <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

## Time/Space Targets

- Time: O(n log k) with heap, O(n) average with quickselect
- Space: O(k) with heap

