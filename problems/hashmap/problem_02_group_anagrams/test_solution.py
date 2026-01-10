"""Tests for Group Anagrams"""

import pytest
from solution_template import group_anagrams


def normalize_groups(groups):
    """Sort groups for comparison."""
    return sorted([sorted(g) for g in groups])


class TestGroupAnagrams:
    """Test cases for group_anagrams function."""
    
    def test_basic_case(self):
        """Multiple anagram groups."""
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        expected = [["ate", "eat", "tea"], ["nat", "tan"], ["bat"]]
        assert normalize_groups(result) == normalize_groups(expected)
    
    def test_empty_string(self):
        """Single empty string."""
        result = group_anagrams([""])
        assert result == [[""]]
    
    def test_single_char(self):
        """Single character string."""
        result = group_anagrams(["a"])
        assert result == [["a"]]
    
    def test_no_anagrams(self):
        """No strings are anagrams of each other."""
        result = group_anagrams(["abc", "def", "ghi"])
        assert len(result) == 3
        assert all(len(g) == 1 for g in result)
    
    def test_all_anagrams(self):
        """All strings are anagrams."""
        result = group_anagrams(["abc", "bca", "cab", "acb"])
        assert len(result) == 1
        assert len(result[0]) == 4
    
    def test_duplicate_strings(self):
        """Same string appears multiple times."""
        result = group_anagrams(["a", "a", "a"])
        assert normalize_groups(result) == [["a", "a", "a"]]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

