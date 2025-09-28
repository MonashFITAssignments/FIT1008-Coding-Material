from unittest import TestCase
from algorithms.mergesort import mergesort
from algorithms.insertionsort import insertion_sort
from data_structures.referential_array import ArrayR
from data_structures.linked_list import LinkedList
from data_structures.array_list import ArrayList
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

    def test_key(self):
        reverse_sorted = list(range(10))
        sorted_list = mergesort(ArrayR.from_list(reverse_sorted), lambda x: -x)
        self.assertEqual([x for x in sorted_list], list(reversed(range(10))))

    def test_linked(self):
        seed = time.time_ns()
        random.seed(seed)
        
        # Generate a random list of integers
        random_list = [random.randint(0, 100) for _ in range(random.randint(0, 100))]

        ll = LinkedList()
        for i in random_list:
            ll.append(i)
        
        res = mergesort(ll)
        self.assertIs(type(res), LinkedList)
        actual = sorted(random_list)
        for i, item in enumerate(res):
            self.assertEqual(item, actual[i])



class TestInsertionSort(TestCase):
    def test_sort(self):
        seed = time.time_ns()
        random.seed(seed)
        
        # Generate a random list of integers
        random_list = [random.randint(0, 100) for _ in range(random.randint(0, 100))]
        
        unsorted_array = ArrayR.from_list(random_list)
        sorted_array = ArrayR.from_list(sorted(random_list))

        result_array = insertion_sort(unsorted_array)
        
        for i in range(len(sorted_array)):
            self.assertEqual(result_array[i], sorted_array[i], f"Failed at index {i} with seed {seed}")
        self.assertEqual(len(result_array), len(sorted_array), f"Result length {len(result_array)} does not match expected length {len(sorted_array)}")
        self.assertEqual([x for x in unsorted_array], [x for x in result_array])

    
    def test_out_of_place(self):
        random_list = [random.randint(0, 100) for _ in range(random.randint(2, 100))]
        
        unsorted_list = random_list + [-1]
        ll = LinkedList()
        al = ArrayList(len(unsorted_list))
        for i in unsorted_list:
            ll.append(i)
            al.append(i)
        
        ll_sorted = insertion_sort(ll)
        al_sorted = insertion_sort(al)
        self.assertIs(type(ll_sorted), LinkedList)
        self.assertIs(type(al_sorted), ArrayList)
        self.assertNotEqual([x for x in ll], sorted(unsorted_list))
        self.assertNotEqual([x for x in al], sorted(unsorted_list))


    def test_sort_empty(self):
        empty_array = ArrayR.from_list([])
        result_array = insertion_sort(empty_array)
        self.assertEqual(len(result_array), 0, "Resulting array should be empty for an empty input array")
    
    def test_key(self):
        reverse_sorted = list(range(10))
        sorted_list = insertion_sort(ArrayR.from_list(reverse_sorted), lambda x: -x)
        self.assertEqual([x for x in sorted_list], list(reversed(range(10))))

