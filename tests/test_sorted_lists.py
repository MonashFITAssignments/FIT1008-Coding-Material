from unittest import TestCase

from data_structures.array_sorted_list import ArraySortedList
from data_structures.referential_array import ArrayR

class TestArraySortedList(TestCase):
    def setUp(self):
        self._list = ArraySortedList()
    
    def test_add(self):
        self._list.add(1)
        self.assertEqual(len(self._list), 1)
        self._list.add(2)
        self.assertEqual(len(self._list), 2)
        
        self.assertEqual(self._list[0], 1)
        self.assertEqual(self._list[1], 2)

        self._list.add(0)
        self.assertEqual(len(self._list), 3)
        # It should be inserted at the beginning to keep the order
        self.assertEqual(self._list[0], 0)
    
    def test_remove(self):
        self._list.add(3)
        self._list.add(1)
        self._list.add(2)
        self.assertEqual(len(self._list), 3)
        
        self._list.remove(1)
        self.assertEqual(len(self._list), 2)
        self.assertEqual(self._list[0], 2)
        self.assertEqual(self._list[1], 3)
        
        self._list.remove(3)
        self.assertEqual(len(self._list), 1)
        self.assertEqual(self._list[0], 2)

        self._list.remove(2)
        self.assertEqual(len(self._list), 0)
        self.assertTrue(self._list.is_empty())
    
    def test_clear(self):
        for i in range(10):
            self._list.add(i)
        self.assertEqual(len(self._list), 10)

        self._list.clear()
        self.assertEqual(len(self._list), 0)
        self.assertTrue(self._list.is_empty())
    
    def test_index(self):
        for i in range(10):
            # Insert in the reverse order
            self._list.add(10 - i)
        
        for i in range(10):
            # Insert in ascending order
            self._list.add(i + 11)
        
        for i in range(20):
            self.assertEqual(self._list.index(i + 1), i)
    
    def test_contains(self):
        for i in range(10):
            self._list.add(i)
        
        for i in range(10):
            self.assertTrue(i in self._list)
        
        # But these items shouldn't be present
        self.assertFalse(10 in self._list)
        # Running operations with a different type should raise TypeError
        self.assertRaises(TypeError, lambda: "string" in self._list)
        self.assertFalse(0.5 in self._list)

    def test_convert_to_arrayR(self):
        for i in range(10):
            self._list.add(i)
        
        array = ArrayR.from_list(self._list)
        self.assertEqual(len(array), 10)
        for i in range(10):
            self.assertIn(i, array)
