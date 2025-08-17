from unittest import TestCase
from algorithms.mergesort import mergesort
from data_structures.referential_array import ArrayR
import random
import time

class TestMergeSort(TestCase):
    def test_sort(self):
        seed = time.time_ns()
        random.seed(seed)
        
        # Generate a random list of integers
        random_list = [random.randint(0, 100) for _ in range(random.randint(0, 100))]
        
        unsorted_array = ArrayR.from_list(random_list)
        sorted_array = ArrayR.from_list(sorted(random_list))

        result_array = mergesort(unsorted_array)
        
        for i in range(len(sorted_array)):
            self.assertEqual(result_array[i], sorted_array[i], f"Failed at index {i} with seed {seed}")
        self.assertEqual(len(result_array), len(sorted_array), f"Result length {len(result_array)} does not match expected length {len(sorted_array)}")

    def test_sort_empty(self):
        empty_array = ArrayR.from_list([])
        result_array = mergesort(empty_array)
        self.assertEqual(len(result_array), 0, "Resulting array should be empty for an empty input array")
