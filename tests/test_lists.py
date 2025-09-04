from unittest import TestCase

from data_structures.linked_list import LinkedList
from data_structures.array_list import ArrayList
from data_structures.array_sorted_list import ArraySortedList
from data_structures.referential_array import ArrayR
from data_structures.abstract_list import List
from data_structures.node import Node


class TestArrayList(TestCase):
    def setUp(self):
        self.list = ArrayList()
    
    def test_capacity(self):
        # These should work
        ArrayList(10)
        ArrayList(0)
        
        # This should raise ValueError
        with self.assertRaises(ValueError):
            ArrayList(-1)

    def test_append(self):
        self.list.append(1)
        self.assertEqual(len(self.list), 1)
        self.list.append(2)
        self.assertEqual(len(self.list), 2)
        
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 2)

    def test_insert(self):
        self.list.insert(0, 1)
        self.assertEqual(len(self.list), 1)
        self.list.insert(1, 2)
        self.assertEqual(len(self.list), 2)
        self.list.insert(1, 3)
        self.assertEqual(len(self.list), 3)
        
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 3)
        self.assertEqual(self.list[2], 2)
    
    def test_remove(self):
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
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
            self.list.append(i)
        self.assertEqual(len(self.list), 10)

        self.list.clear()
        self.assertEqual(len(self.list), 0)
        self.assertTrue(self.list.is_empty())
    
    def test_index(self):
        for i in range(10):
            self.list.append(i + 1)
        
        self.assertEqual(self.list.index(1), 0)
        self.assertEqual(self.list.index(5), 4)
        self.assertEqual(self.list.index(10), 9)

        # Add a second 1
        self.list.append(1)
        # Should still return the first 1
        self.assertEqual(self.list.index(1), 0)
    
    def test_len(self):
        for i in range(10):
            self.list.append(i)
            self.assertEqual(len(self.list), i + 1)
        
        for i in range(10):
            self.list.remove(i)
            self.assertEqual(len(self.list), 9 - i)

    def test_getitem(self):
        self.assertRaises(IndexError, lambda: self.list[-1])
        self.assertRaises(IndexError, lambda: self.list[0])
        self.assertRaises(IndexError, lambda: self.list[1])

        self.list.append(0)
        self.list.append(1)
        self.assertEqual(self.list[0], 0)
        self.assertEqual(self.list[1], 1)
        self.assertEqual(self.list[-1], 1)
        self.assertEqual(self.list[-2], 0)

        self.assertRaises(IndexError, lambda: self.list[2])
        self.assertRaises(IndexError, lambda: self.list[-3])

    def test_contains(self):
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        self.assertTrue(1 in self.list)
        self.assertTrue(2 in self.list)
        self.assertTrue(3 in self.list)
        self.assertFalse(4 in self.list)

    def test_str(self):
        self.assertEqual(str(self.list), '<ArrayList []>')

        self.list.append(1)
        self.assertEqual(str(self.list), '<ArrayList [1]>')

        self.list.append(2)
        self.assertEqual(str(self.list), '<ArrayList [1, 2]>')

class TestSortedList(TestCase):
    def setUp(self):
        self.list = ArraySortedList()

    def test_add(self):
        self.list.add(2)
        self.assertEqual(len(self.list), 1)
        self.list.add(3)
        self.assertEqual(len(self.list), 2)
        self.list.add(1)
        self.assertEqual(len(self.list), 3)

        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 2)
        self.assertEqual(self.list[2], 3)

    def test_delete_at_index(self):
        self.list.add(1)
        self.list.add(2)
        self.list.add(3)

        self.assertEqual(len(self.list), 3)

        self.list.delete_at_index(2)
        self.assertEqual(len(self.list), 2)
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 2)
        self.assertRaises(IndexError, lambda: self.list.delete_at_index(2))

        self.list.delete_at_index(0)
        self.assertEqual(len(self.list), 1)
        self.assertEqual(self.list[0], 2)
        self.assertRaises(IndexError, lambda: self.list.delete_at_index(1))

        self.list.delete_at_index(0)
        self.assertEqual(len(self.list), 0)
        self.assertTrue(self.list.is_empty())

    def test_remove(self):
        self.list.add(1)
        self.list.add(2)
        self.list.add(3)
        self.assertEqual(len(self.list), 3)

        self.list.remove(1)
        self.assertEqual(len(self.list), 2)
        self.assertEqual(self.list[0], 2)
        self.assertEqual(self.list[1], 3)
        self.assertRaises(ValueError, lambda: self.list.remove(1))

        self.list.remove(3)
        self.assertEqual(len(self.list), 1)
        self.assertEqual(self.list[0], 2)

        self.list.remove(2)
        self.assertEqual(len(self.list), 0)
        self.assertTrue(self.list.is_empty())

    def test_index(self):
        for i in range(10):
            self.list.add(i + 1)

        self.assertEqual(self.list.index(1), 0)
        self.assertEqual(self.list.index(5), 4)
        self.assertEqual(self.list.index(10), 9)

        # Add a second 1
        self.list.add(1)
        # Should still return the first 1
        self.assertEqual(self.list.index(1), 0)

    def test_clear(self):
        for i in range(10):
            self.list.add(i)
        self.assertEqual(len(self.list), 10)

        self.list.clear()
        self.assertEqual(len(self.list), 0)
        self.assertTrue(self.list.is_empty())

    def test_contains(self):
        self.list.add(1)
        self.list.add(2)
        self.list.add(3)
        self.assertTrue(1 in self.list)
        self.assertTrue(2 in self.list)
        self.assertTrue(3 in self.list)
        self.assertFalse(4 in self.list)

    def test_str(self):
        self.assertEqual(str(self.list), '<ArraySortedList []>')

        self.list.add(1)
        self.assertEqual(str(self.list), '<ArraySortedList [1]>')

        self.list.add(2)
        self.assertEqual(str(self.list), '<ArraySortedList [1, 2]>')

class TestLinkedList(TestCase):
    def setUp(self):
        self.list = LinkedList()
    
    def test_append(self):
        self.list.append(1)
        self.assertEqual(len(self.list), 1)
        self.list.append(2)
        self.assertEqual(len(self.list), 2)
        
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 2)

    def test_insert(self):
        self.list.insert(0, 1)
        self.assertEqual(len(self.list), 1)
        self.list.insert(1, 2)
        self.assertEqual(len(self.list), 2)
        self.list.insert(1, 3)
        self.assertEqual(len(self.list), 3)
        
        self.assertEqual(self.list[0], 1)
        self.assertEqual(self.list[1], 3)
        self.assertEqual(self.list[2], 2)
    
    def test_remove(self):
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
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
            self.list.append(i)
        self.assertEqual(len(self.list), 10)

        self.list.clear()
        self.assertEqual(len(self.list), 0)
        self.assertTrue(self.list.is_empty())
    
    def test_index(self):
        for i in range(10):
            self.list.append(i + 1)
        
        self.assertEqual(self.list.index(1), 0)
        self.assertEqual(self.list.index(5), 4)
        self.assertEqual(self.list.index(10), 9)

        # Add a second 1
        self.list.append(1)
        # Should still return the first 1
        self.assertEqual(self.list.index(1), 0)
    
    def test_len(self):
        for i in range(10):
            self.list.append(i)
            self.assertEqual(len(self.list), i + 1)
        
        for i in range(10):
            self.list.remove(i)
            self.assertEqual(len(self.list), 9 - i)

    def test_getitem(self):
        self.assertRaises(IndexError, lambda: self.list[0])
        self.assertRaises(IndexError, lambda: self.list[-1])

        self.list.append(0)
        self.list.append(1)
        self.assertEqual(self.list[0], 0)
        self.assertEqual(self.list[1], 1)
        self.assertEqual(self.list[-1], 1)
        self.assertEqual(self.list[-2], 0)

        self.assertRaises(IndexError, lambda: self.list[2])
        self.assertRaises(IndexError, lambda: self.list[-3])

    def test_iteration(self):
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)

        items = [item for item in self.list]
        self.assertEqual(items, [1, 2, 3])

        iter2 = iter(self.list)
        for _ in range(len(self.list)):
            next(iter2)
        self.assertRaises(StopIteration, next, iter2)

    def test_str(self):
        self.assertEqual(str(self.list), '<LinkedList []>')

        self.list.append(1)
        self.assertEqual(str(self.list), '<LinkedList [1]>')

        self.list.append(2)
        self.assertEqual(str(self.list), '<LinkedList [1, 2]>')

    def test_from_node(self):
        empty = None
        ll = LinkedList.from_node(empty)
        self.assertTrue(ll.is_empty())

        chain_3 = Node(1, Node(2, Node(3, None)))
        ll = LinkedList.from_node(chain_3)
        self.assertEqual(len(ll), 3)
        self.assertEqual([x for x in ll], [1,2,3])
        ll.append(4) #check that rear is set properly
        self.assertEqual([x for x in ll], [1,2,3,4])

        chain_3.item = "This shouldn't affect ll"
        chain_3.link.link = None
        self.assertEqual([x for x in ll], [1,2,3,4])


        for i in range(10):
            chain = None
            for j in range(i):
                chain = Node(j, chain)
            ll = LinkedList.from_node(chain)
            self.assertEqual(len(ll), i)
            self.assertEqual(list(ll), list(range(i))[::-1])

    def test_from_node_cycles(self):
        cycle1 = Node(1)
        cycle1.link = cycle1
        self.assertRaises(ValueError, LinkedList.from_node, cycle1)
        
        cycle2a = cycle2b = Node(2)
        cycle2a.link, cycle2b.link = cycle2b, cycle2a
        self.assertRaises(ValueError, LinkedList.from_node, cycle2a)
        self.assertRaises(ValueError, LinkedList.from_node, cycle2b)
        
        cycle3 = Node(3, cycle2a)
        for _ in range(50):
            cycle3 = Node(3, cycle3)
        self.assertRaises(ValueError, LinkedList.from_node, cycle3)

        for length in range(15):
            cycle_top = Node(1)
            cycle_bottom = cycle_top
            for _ in range(length):
                cycle_top = Node(1, cycle_top)
            cycle_bottom.link = cycle_top
            self.assertRaises(ValueError, LinkedList.from_node, cycle_top)


class TestLists(TestCase):
    def setUp(self):
        self.lists:list[List] = [ArrayList(), LinkedList()]
        self.empty_lists = [ArrayList(), LinkedList()]
        [list.append(i) for i in range(5) for list in self.lists]

    def test_convert_to_arrayR(self):
        arrays = [ArrayR.from_list(list) for list in self.lists]
        empty_arrays = [ArrayR.from_list(list) for list in self.empty_lists]
        self.assertEqual(list(map(len, arrays)), [5,5])
        self.assertEqual(list(map(len, empty_arrays)), [0,0])
        for i in range(5):
            for array in arrays:
                self.assertIn(i, array)