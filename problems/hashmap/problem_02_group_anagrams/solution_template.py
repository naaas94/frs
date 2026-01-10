"""Group Anagrams - Solution Template"""

from typing import List
from collections import defaultdict


def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Group strings that are anagrams of each other.
    
    Args:
        strs: List of strings to group
        
    Returns:
        List of groups, where each group contains anagrams
    
    INVARIANT: After processing string i, all anagrams seen so far
    are in the same group (keyed by their canonical form).
    """
    # TODO: Implement your solution here
    pass


if __name__ == "__main__":
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    print(f"Result: {result}")

