from unittest import TestCase

from data_structures.array_sorted_list import ArraySortedList


class TestArraySortedList(TestCase):
    def setUp(self):
        self.list = ArraySortedList()
    
    def test_add(self):
        self.list.add(1)
        self.assertEqual(len(self.list), 1)
        self.list.add(2)
        self.assertEqual(len(self.list), 2)
        
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 2)

        self.list.add(0)
        self.assertEqual(len(self.list), 3)
        # It should be inserted at the beginning to keep the order
        self.assertEqual(self.list[0], 0)
    
    def test_remove(self):
        self.list.add(3)
        self.list.add(1)
        self.list.add(2)
        self.assertEqual(len(self.list), 3)
        
        self.list.remove(1)
        self.assertEqual(len(self.list), 2)
        self.assertEqual(self.list[0], 2)
        self.assertEqual(self.list[1], 3)
        
        self.list.remove(3)
        self.assertEqual(len(self.list), 1)
        self.assertEqual(self.list[0], 2)

        self.list.remove(2)
        self.assertEqual(len(self.list), 0)
        self.assertTrue(self.list.is_empty())
    
    def test_clear(self):
        for i in range(10):
            self.list.add(i)
        self.assertEqual(len(self.list), 10)

        self.list.clear()
        self.assertEqual(len(self.list), 0)
        self.assertTrue(self.list.is_empty())
    
    def test_index(self):
        for i in range(10):
            # Insert in the reverse order
            self.list.add(10 - i)
        
        for i in range(10):
            # Insert in ascending order
            self.list.add(i + 11)
        
        for i in range(20):
            self.assertEqual(self.list.index(i + 1), i)
    
    def test_contains(self):
        for i in range(10):
            self.list.add(i)
        
        for i in range(10):
            self.assertTrue(i in self.list)
        
        # But these items shouldn't be present
        self.assertFalse(10 in self.list)
        # Running operations with a different type should raise TypeError
        self.assertRaises(TypeError, lambda: "string" in self.list)
        self.assertFalse(0.5 in self.list)
