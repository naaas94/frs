"""
BFS / DFS WITH VISITED PATTERN
===============================

When to use:
- Graph traversal (connected components, shortest path)
- Tree traversal
- Grid problems (islands, flood fill)
- Topological sort (DAG)
- Cycle detection

Time: O(V + E) for graphs, O(m*n) for grids
Space: O(V) for visited set, O(V) for queue/stack
"""

from typing import List, Set, Dict, Optional, Tuple
from collections import deque, defaultdict


# =============================================================================
# TEMPLATE 1: BFS - Level Order / Shortest Path (Unweighted)
# =============================================================================
def bfs_template(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    BFS traversal from start node.
    
    Use BFS when you need:
    - Shortest path (unweighted)
    - Level-by-level processing
    
    INVARIANT: All nodes at distance d are processed before distance d+1.
    """
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result


def bfs_shortest_path(graph: Dict[int, List[int]], start: int, end: int) -> int:
    """
    Find shortest path length from start to end.
    
    INVARIANT: When we reach a node, we've found the shortest path to it.
    """
    if start == end:
        return 0
    
    visited = {start}
    queue = deque([(start, 0)])  # (node, distance)
    
    while queue:
        node, dist = queue.popleft()
        
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return dist + 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1  # No path found


# =============================================================================
# TEMPLATE 2: DFS - Recursive
# =============================================================================
def dfs_recursive_template(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    DFS traversal using recursion.
    
    Use DFS when you need:
    - Path finding (any path, not necessarily shortest)
    - Cycle detection
    - Topological sort
    - Connected components
    """
    visited = set()
    result = []
    
    def dfs(node: int):
        visited.add(node)
        result.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
    
    dfs(start)
    return result


# =============================================================================
# TEMPLATE 3: DFS - Iterative (with Stack)
# =============================================================================
def dfs_iterative_template(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    DFS traversal using explicit stack.
    
    Use when recursion depth might exceed limit.
    """
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        result.append(node)
        
        # Add neighbors in reverse order for same traversal order as recursive
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)
    
    return result


# =============================================================================
# TEMPLATE 4: Number of Islands (Grid BFS/DFS)
# =============================================================================
def num_islands_template(grid: List[List[str]]) -> int:
    """
    Count connected components in a grid.
    
    INVARIANT: After processing a cell, all connected cells are marked visited.
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    visited = set()
    islands = 0
    
    def bfs(r: int, c: int):
        queue = deque([(r, c)])
        visited.add((r, c))
        
        while queue:
            row, col = queue.popleft()
            
            # 4 directions: up, down, left, right
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                
                if (0 <= nr < rows and 0 <= nc < cols and 
                    (nr, nc) not in visited and 
                    grid[nr][nc] == '1'):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                bfs(r, c)
                islands += 1
    
    return islands


# =============================================================================
# TEMPLATE 5: Clone Graph (DFS with Mapping)
# =============================================================================
class Node:
    def __init__(self, val: int = 0, neighbors: List['Node'] = None):
        self.val = val
        self.neighbors = neighbors if neighbors else []


def clone_graph_template(node: Optional[Node]) -> Optional[Node]:
    """
    Deep copy a graph.
    
    INVARIANT: old_to_new maps each original node to its clone.
    """
    if not node:
        return None
    
    old_to_new = {}
    
    def dfs(original: Node) -> Node:
        if original in old_to_new:
            return old_to_new[original]
        
        # Create clone
        clone = Node(original.val)
        old_to_new[original] = clone
        
        # Clone neighbors
        for neighbor in original.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)


# =============================================================================
# TEMPLATE 6: Topological Sort (Kahn's Algorithm - BFS)
# =============================================================================
def topological_sort_template(num_nodes: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    Topological sort of a DAG.
    edges: [(from, to), ...] means from -> to dependency
    
    INVARIANT: Process nodes with 0 incoming edges first.
    """
    # Build adjacency list and in-degree count
    graph = defaultdict(list)
    in_degree = [0] * num_nodes
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    # Start with nodes that have no dependencies
    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycle
    if len(result) != num_nodes:
        return []  # Cycle detected
    
    return result


# =============================================================================
# TEMPLATE 7: Cycle Detection (Directed Graph - DFS with Colors)
# =============================================================================
def has_cycle_template(num_nodes: int, edges: List[Tuple[int, int]]) -> bool:
    """
    Detect cycle in directed graph using 3-color DFS.
    
    Colors:
    - WHITE (0): Not visited
    - GRAY (1): Currently in recursion stack
    - BLACK (2): Fully processed
    
    INVARIANT: If we visit a GRAY node, we've found a back edge (cycle).
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    
    color = [WHITE] * num_nodes
    
    def dfs(node: int) -> bool:
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # Back edge = cycle
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        
        color[node] = BLACK
        return False
    
    # Check all nodes (graph might be disconnected)
    for node in range(num_nodes):
        if color[node] == WHITE and dfs(node):
            return True
    
    return False


# =============================================================================
# EDGE CASES TO CHECK
# =============================================================================
"""
□ Empty graph
□ Single node
□ Disconnected components
□ Cycle in graph
□ Self-loop
□ Grid: empty, single cell, single row/column
□ Start == end
□ No path exists
"""


# =============================================================================
# COMMON BUGS
# =============================================================================
"""
1. Not marking visited BEFORE adding to queue (causes duplicates)
2. Wrong grid bounds check order (short-circuit evaluation)
3. Forgetting to handle disconnected components
4. Using list instead of set for visited (O(n) vs O(1) lookup)
5. Stack overflow in deep recursion -> use iterative
6. Modifying grid as visited marker vs using separate set
"""

