# Problem Bank

Curated problems organized by pattern. Each problem includes:
- `problem.md` - Problem statement and constraints
- `solution_template.py` - Starter code with invariant hints
- `test_solution.py` - Pytest test cases
- `hints.md` (optional) - Progressive hints

## Problems by Pattern

### Hashmap (3 problems)
| Problem | Difficulty | Key Technique |
|---------|------------|---------------|
| [Two Sum](hashmap/problem_01_two_sum/) | Easy | Complement lookup |
| [Group Anagrams](hashmap/problem_02_group_anagrams/) | Medium | Key = sorted tuple |
| [Top K Frequent](hashmap/problem_03_top_k_frequent/) | Medium | Counter + heap |

### Two Pointers (3 problems)
| Problem | Difficulty | Key Technique |
|---------|------------|---------------|
| [Container Water](two_pointers/problem_01_container_water/) | Medium | Opposite ends, move shorter |
| [Longest Substring](two_pointers/problem_02_longest_substring/) | Medium | Sliding window + set |
| [Three Sum](two_pointers/problem_03_three_sum/) | Medium | Sort + two pointers |

### Sorting (3 problems)
| Problem | Difficulty | Key Technique |
|---------|------------|---------------|
| [Merge Intervals](sorting/problem_01_merge_intervals/) | Medium | Sort by start, merge adjacent |
| [Meeting Rooms II](sorting/problem_02_meeting_rooms/) | Medium | Events sweep line |
| [Largest Number](sorting/problem_03_largest_number/) | Medium | Custom comparator |

### Heap (3 problems)
| Problem | Difficulty | Key Technique |
|---------|------------|---------------|
| [Kth Largest](heap/problem_01_kth_largest/) | Medium | Min-heap of size k |
| [Task Scheduler](heap/problem_02_task_scheduler/) | Medium | Greedy + max heap |
| [Merge K Lists](heap/problem_03_merge_k_lists/) | Hard | Heap of list heads |

### Binary Search (3 problems)
| Problem | Difficulty | Key Technique |
|---------|------------|---------------|
| [Search Rotated](binary_search/problem_01_search_rotated/) | Medium | Find sorted half |
| [Find Peak](binary_search/problem_02_find_peak/) | Medium | Move toward higher |
| [Median Sorted](binary_search/problem_03_median_sorted/) | Hard | Binary search on partitions |

### Graph/BFS/DFS (3 problems)
| Problem | Difficulty | Key Technique |
|---------|------------|---------------|
| [Number of Islands](graph/problem_01_num_islands/) | Medium | BFS/DFS flood fill |
| [Clone Graph](graph/problem_02_clone_graph/) | Medium | BFS + hashmap |
| [Course Schedule](graph/problem_03_course_schedule/) | Medium | Topological sort |

### Data Plumbing (3 problems)
| Problem | Difficulty | Key Technique |
|---------|------------|---------------|
| [JSONL Aggregation](plumbing/problem_01_jsonl_aggregation/) | Medium | Parse → validate → aggregate |
| [CSV Validation](plumbing/problem_02_csv_validation/) | Medium | Row validation + error collection |
| [API Merger](plumbing/problem_03_api_merger/) | Medium | Deduplicate by ID |

## Running Tests

```bash
# Run tests for a specific problem
cd problems/hashmap/problem_01_two_sum
python -m pytest test_solution.py -v

# Run all tests in a pattern
python -m pytest problems/hashmap/ -v
```

## Difficulty Progression

**Week 1** (Pattern Practice):
- Day 1-5: One medium problem per day, focus on template mastery

**Week 2** (Mixed Practice):
- Day 6+: Mix patterns, simulate interview conditions

