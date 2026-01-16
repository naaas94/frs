# Container With Most Water

## Difficulty: Medium
## Pattern: Two Pointers (Opposite Ends)

## Problem Statement

Given an array `height` of n non-negative integers where each represents a point at coordinate (i, height[i]), find two lines that together with the x-axis form a container that holds the most water.

Return the maximum amount of water a container can store.

## Examples

```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: Lines at index 1 (height 8) and index 8 (height 7)
             Width = 8 - 1 = 7, Height = min(8, 7) = 7
             Area = 7 * 7 = 49

Input: height = [1,1]
Output: 1
```

## Constraints

- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4

## Time/Space Targets

- Time: O(n)
- Space: O(1)


