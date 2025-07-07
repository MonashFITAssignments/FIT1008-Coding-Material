from unittest import TestCase

from data_structures.linked_list import LinkedList
from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR


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

class TestArrayRConversions(TestCase):
    def test_from_ArrayList(self):
        al = ArrayList(5)
        for i in range(4):
            al.append(i)
        
        ar = ArrayR.from_list(al)

        for i in range(len(ar)):
            self.assertEqual(ar[i], al[i])
        
        self.assertEqual(len(ar), 4)

    def test_from_LinkedList(self):
        ll = LinkedList()
        for i in range(4):
            ll.append(i)
        
        ar = ArrayR.from_list(ll)

        for i in range(len(ar)):
            self.assertEqual(ar[i], ll[i])
        
        self.assertEqual(len(ar), 4)

    def test_to_array_list(self):
        array = ArrayR(5)
        for i in range(4):
            array[i] = i
        
        array_list = ArrayList.from_arrayR(array)
        self.assertEqual([n for n in array_list], [0,1,2,3, None])
        self.assertEqual(len(array_list), 5)

    def test_to_linked_list(self):
        array = ArrayR(5)
        for i in range(4):
            array[i] = i
        
        linked_list = LinkedList.from_arrayR(array)
        self.assertEqual([n for n in linked_list], [0,1,2,3, None])
        self.assertEqual(len(linked_list), 5)