# Day 7: Mixed Problems - Plumbing Heavy

## Today's Goal
Balance algorithm work with data plumbing. Real interviews often have both.

---

## Session 1: Clone Graph (45 min)

### Problem
`problems/graph/problem_02_clone_graph/`

Deep copy an undirected graph.

**Pattern**: BFS/DFS + hashmap for old→new node mapping

**Invariant**: After visiting node N, `cloned[N]` exists with all its neighbors cloned.

```python
# Key insight
cloned = {node: Node(node.val)}  # Create clone
for neighbor in node.neighbors:
    if neighbor not in cloned:
        cloned[neighbor] = Node(neighbor.val)
        queue.append(neighbor)
    cloned[node].neighbors.append(cloned[neighbor])
```

---

## Session 2: Full Pipeline Exercise (45 min)

### Exercise: Build a Complete Data Pipeline

Given this scenario:
> Process a log file with mixed valid/invalid entries, aggregate by category,
> find top-5 by count, handle errors gracefully.

Build the full pipeline from scratch:
1. Parse (handle malformed)
2. Validate (check required fields)
3. Normalize (clean data)
4. Aggregate (group and compute metrics)
5. Select (top-k)
6. Report (errors + results)

**Time yourself**. Target: 30 minutes for clean implementation.

---

## End of Day Postmortem
- Which felt more natural today: algo or plumbing?
- What's your plumbing pipeline time?

---

## Tomorrow Preview
Day 8: Full Mock #1

