from unittest import TestCase

from data_structures.linked_list import LinkedList
from data_structures.array_list import ArrayList
from data_structures.array_sorted_list import ArraySortedList
from data_structures.referential_array import ArrayR
from data_structures.abstract_list import List

class TestArrayList(TestCase):
    def setUp(self):
        self._list = ArrayList()
    
    def test_capacity(self):
        # These should work
        ArrayList(10)
        ArrayList(0)
        
        # This should raise ValueError
        with self.assertRaises(ValueError):
            ArrayList(-1)

    def test_append(self):
        self._list.append(1)
        self.assertEqual(len(self._list), 1)
        self._list.append(2)
        self.assertEqual(len(self._list), 2)
        
        self.assertEqual(self._list[0], 1)
        self.assertEqual(self._list[1], 2)

    def test_insert(self):
        self._list.insert(0, 1)
        self.assertEqual(len(self._list), 1)
        self._list.insert(1, 2)
        self.assertEqual(len(self._list), 2)
        self._list.insert(1, 3)
        self.assertEqual(len(self._list), 3)
        
        self.assertEqual(self._list[0], 1)
        self.assertEqual(self._list[1], 3)
        self.assertEqual(self._list[2], 2)
    
    def test_remove(self):
        self._list.append(1)
        self._list.append(2)
        self._list.append(3)
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
            self._list.append(i)
        self.assertEqual(len(self._list), 10)

        self._list.clear()
        self.assertEqual(len(self._list), 0)
        self.assertTrue(self._list.is_empty())
    
    def test_index(self):
        for i in range(10):
            self._list.append(i + 1)
        
        self.assertEqual(self._list.index(1), 0)
        self.assertEqual(self._list.index(5), 4)
        self.assertEqual(self._list.index(10), 9)

        # Add a second 1
        self._list.append(1)
        # Should still return the first 1
        self.assertEqual(self._list.index(1), 0)
    
    def test_len(self):
        for i in range(10):
            self._list.append(i)
            self.assertEqual(len(self._list), i + 1)
        
        for i in range(10):
            self._list.remove(i)
            self.assertEqual(len(self._list), 9 - i)

    def test_getitem(self):
        self.assertRaises(IndexError, lambda: self._list[-1])
        self.assertRaises(IndexError, lambda: self._list[0])
        self.assertRaises(IndexError, lambda: self._list[1])

        self._list.append(0)
        self._list.append(1)
        self.assertEqual(self._list[0], 0)
        self.assertEqual(self._list[1], 1)
        self.assertEqual(self._list[-1], 1)
        self.assertEqual(self._list[-2], 0)

        self.assertRaises(IndexError, lambda: self._list[2])
        self.assertRaises(IndexError, lambda: self._list[-3])

    def test_contains(self):
        self._list.append(1)
        self._list.append(2)
        self._list.append(3)
        self.assertTrue(1 in self._list)
        self.assertTrue(2 in self._list)
        self.assertTrue(3 in self._list)
        self.assertFalse(4 in self._list)

    def test_str(self):
        self.assertEqual(str(self._list), '<ArrayList []>')

        self._list.append(1)
        self.assertEqual(str(self._list), '<ArrayList [1]>')

        self._list.append(2)
        self.assertEqual(str(self._list), '<ArrayList [1, 2]>')

class TestSortedList(TestCase):
    def setUp(self):
        self._list = ArraySortedList()

    def test_add(self):
        self._list.add(2)
        self.assertEqual(len(self._list), 1)
        self._list.add(3)
        self.assertEqual(len(self._list), 2)
        self._list.add(1)
        self.assertEqual(len(self._list), 3)

        self.assertEqual(self._list[0], 1)
        self.assertEqual(self._list[1], 2)
        self.assertEqual(self._list[2], 3)

    def test_delete_at_index(self):
        self._list.add(1)
        self._list.add(2)
        self._list.add(3)

        self.assertEqual(len(self._list), 3)

        self._list.delete_at_index(2)
        self.assertEqual(len(self._list), 2)
        self.assertEqual(self._list[0], 1)
        self.assertEqual(self._list[1], 2)
        self.assertRaises(IndexError, lambda: self._list.delete_at_index(2))

        self._list.delete_at_index(0)
        self.assertEqual(len(self._list), 1)
        self.assertEqual(self._list[0], 2)
        self.assertRaises(IndexError, lambda: self._list.delete_at_index(1))

        self._list.delete_at_index(0)
        self.assertEqual(len(self._list), 0)
        self.assertTrue(self._list.is_empty())

    def test_remove(self):
        self._list.add(1)
        self._list.add(2)
        self._list.add(3)
        self.assertEqual(len(self._list), 3)

        self._list.remove(1)
        self.assertEqual(len(self._list), 2)
        self.assertEqual(self._list[0], 2)
        self.assertEqual(self._list[1], 3)
        self.assertRaises(ValueError, lambda: self._list.remove(1))

        self._list.remove(3)
        self.assertEqual(len(self._list), 1)
        self.assertEqual(self._list[0], 2)

        self._list.remove(2)
        self.assertEqual(len(self._list), 0)
        self.assertTrue(self._list.is_empty())

    def test_index(self):
        for i in range(10):
            self._list.add(i + 1)

        self.assertEqual(self._list.index(1), 0)
        self.assertEqual(self._list.index(5), 4)
        self.assertEqual(self._list.index(10), 9)

        # Add a second 1
        self._list.add(1)
        # Should still return the first 1
        self.assertEqual(self._list.index(1), 0)

    def test_clear(self):
        for i in range(10):
            self._list.add(i)
        self.assertEqual(len(self._list), 10)

        self._list.clear()
        self.assertEqual(len(self._list), 0)
        self.assertTrue(self._list.is_empty())

    def test_contains(self):
        self._list.add(1)
        self._list.add(2)
        self._list.add(3)
        self.assertTrue(1 in self._list)
        self.assertTrue(2 in self._list)
        self.assertTrue(3 in self._list)
        self.assertFalse(4 in self._list)

    def test_str(self):
        self.assertEqual(str(self._list), '<ArraySortedList []>')

        self._list.add(1)
        self.assertEqual(str(self._list), '<ArraySortedList [1]>')

        self._list.add(2)
        self.assertEqual(str(self._list), '<ArraySortedList [1, 2]>')

class TestLinkedList(TestCase):
    def setUp(self):
        self._list = LinkedList()
    
    def test_append(self):
        self._list.append(1)
        self.assertEqual(len(self._list), 1)
        self._list.append(2)
        self.assertEqual(len(self._list), 2)
        
        self.assertEqual(self._list[0], 1)
        self.assertEqual(self._list[1], 2)

    def test_insert(self):
        self._list.insert(0, 1)
        self.assertEqual(len(self._list), 1)
        self._list.insert(1, 2)
        self.assertEqual(len(self._list), 2)
        self._list.insert(1, 3)
        self.assertEqual(len(self._list), 3)
        
        self.assertEqual(self._list[0], 1)
        self.assertEqual(self._list[1], 3)
        self.assertEqual(self._list[2], 2)
    
    def test_remove(self):
        self._list.append(1)
        self._list.append(2)
        self._list.append(3)
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
            self._list.append(i)
        self.assertEqual(len(self._list), 10)

        self._list.clear()
        self.assertEqual(len(self._list), 0)
        self.assertTrue(self._list.is_empty())
    
    def test_index(self):
        for i in range(10):
            self._list.append(i + 1)
        
        self.assertEqual(self._list.index(1), 0)
        self.assertEqual(self._list.index(5), 4)
        self.assertEqual(self._list.index(10), 9)

        # Add a second 1
        self._list.append(1)
        # Should still return the first 1
        self.assertEqual(self._list.index(1), 0)
    
    def test_len(self):
        for i in range(10):
            self._list.append(i)
            self.assertEqual(len(self._list), i + 1)
        
        for i in range(10):
            self._list.remove(i)
            self.assertEqual(len(self._list), 9 - i)

    def test_getitem(self):
        self.assertRaises(IndexError, lambda: self._list[0])
        self.assertRaises(IndexError, lambda: self._list[-1])

        self._list.append(0)
        self._list.append(1)
        self.assertEqual(self._list[0], 0)
        self.assertEqual(self._list[1], 1)
        self.assertEqual(self._list[-1], 1)
        self.assertEqual(self._list[-2], 0)

        self.assertRaises(IndexError, lambda: self._list[2])
        self.assertRaises(IndexError, lambda: self._list[-3])

    def test_iteration(self):
        self._list.append(1)
        self._list.append(2)
        self._list.append(3)

        items = [item for item in self._list]
        self.assertEqual(items, [1, 2, 3])

        iter2 = iter(self._list)
        for _ in range(len(self._list)):
            next(iter2)
        self.assertRaises(StopIteration, next, iter2)

    def test_str(self):
        self.assertEqual(str(self._list), '<LinkedList []>')

        self._list.append(1)
        self.assertEqual(str(self._list), '<LinkedList [1]>')

        self._list.append(2)
        self.assertEqual(str(self._list), '<LinkedList [1, 2]>')

class TestLists(TestCase):
    def setUp(self):
        self._lists:list[List] = [ArrayList(), LinkedList()]
        self._empty_lists = [ArrayList(), LinkedList()]
        [list.append(i) for i in range(5) for list in self._lists]

    def test_convert_to_arrayR(self):
        arrays = [ArrayR.from_list(list) for list in self._lists]
        empty_arrays = [ArrayR.from_list(list) for list in self._empty_lists]
        self.assertEqual(list(map(len, arrays)), [5,5])
        self.assertEqual(list(map(len, empty_arrays)), [0,0])
        for i in range(5):
            for array in arrays:
                self.assertIn(i, array)