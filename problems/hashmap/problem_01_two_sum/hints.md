# Hints for Two Sum

## Hint 1 (Pattern Recognition)
Think about what information you need to store as you traverse the array.
For each number, what are you looking for?

## Hint 2 (Data Structure)
A hashmap allows O(1) lookup. What would you use as the key?

## Hint 3 (Algorithm)
For each number `num`, you need `target - num` to exist somewhere.
Store numbers you've seen so you can check if the complement exists.

## Hint 4 (Implementation Detail)
Check if the complement exists BEFORE adding the current number to the map.
This prevents using the same element twice.

## Solution Approach
```
seen = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        return (seen[complement], i)
    seen[num] = i
```

