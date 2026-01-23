from unittest import TestCase

from data_structures.referential_array import ArrayR
from algorithms.binary_search import binary_search

class TestArrayList(TestCase):
    def setUp(self):
        self._array = ArrayR.from_list([i for i in range(107)])
    
    def test_binary_search_all(self):
        # Test searching for all elements
        for i in range(107):
            index = binary_search(self._array, i)
            self.assertEqual(index, i, f"Failed to find {i} at index {index}")
    
    def test_binary_search_not_found(self):
        # Test searching for an element not in the array
        for i in [107, -1]:
            with self.assertRaises(ValueError):
                binary_search(self._array, i)
    
    def test_binary_search_empty(self):
        # Test searching in an empty array
        empty_array = ArrayR.from_list([])
        with self.assertRaises(ValueError):
            binary_search(empty_array, 1)
    
    def test_binary_search_single_element(self):
        # Test searching in a single-element array
        single_element_array = ArrayR.from_list([42])
        index = binary_search(single_element_array, 42)
        self.assertEqual(index, 0, "Failed to find the single element in the array")
        
        with self.assertRaises(ValueError):
            binary_search(single_element_array, 0)
