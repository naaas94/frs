# Day 4: BFS/DFS Visited Template

## Today's Goal
Automate the BFS/DFS template with proper visited handling. Know when to use which.

---

## Warm-Up (5 min)

**Micro-drill from yesterday**: [Insert from postmortem]

```python
from collections import deque

# BFS Template (shortest path, level-order)
def bfs(graph, start):
    visited = {start}  # Mark BEFORE adding to queue
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)  # Mark when enqueueing!
                queue.append(neighbor)

# DFS Template (path existence, cycle detection)
def dfs(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            stack.append(neighbor)
```

**Key difference**: BFS = shortest path (unweighted), DFS = easier to implement recursively

---

## Timed Problem (45 min)

### Problem: Number of Islands
`problems/graph/problem_01_num_islands/`

**Invariant**: After BFS from (r, c), all connected land is marked. Each BFS = one island.

**Edge cases**:
- Empty grid
- Single cell
- Diagonal cells NOT connected
- All land vs all water

---

## Plumbing Rep (45 min)

### Exercise: API Response Merger
`problems/plumbing/problem_03_api_merger/`

Merge paginated API responses, deduplicate by ID.

---

## End of Day Postmortem
1. **Pattern used**: _______________
2. **Bug class**: _______________
3. **Fix rule**: _______________
4. **Micro-drill for tomorrow**: _______________
5. **Test case**: _______________

---

## Tomorrow Preview
Day 5: Mixed Problem (combining patterns)

