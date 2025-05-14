from unittest import TestCase

from data_structures.linked_list import LinkedList
from data_structures.array_list import ArrayList


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

    def test_node_iterator(self):
        list_iter = iter(self.list)
        self.assertFalse(list_iter.has_next())
        list_iter.insert_after(1)
        self.assertTrue(list_iter.has_next())
        self.assertEqual(len(self.list), 1)
        self.assertIsNotNone(self.list._LinkedList__head)
        self.assertIsNotNone(self.list._LinkedList__rear)
        self.assertEqual(list_iter.peek(), 1)
        
        next(list_iter)
        self.assertFalse(list_iter.has_next())
        self.assertRaises(StopIteration, next, list_iter)
        self.assertRaises(AttributeError, list_iter.delete_next)
        self.assertRaises(AttributeError, list_iter.peek)

        list_iter2 = iter(self.list)
        list_iter2.insert_after(2)
        self.assertIsNot(self.list._LinkedList__head, self.list._LinkedList__rear)
        self.assertEqual([i for i in self.list], [2,1])
        self.assertEqual(len(self.list), 2)

        list_iter2.delete_next()
        self.assertTrue(list_iter2.has_next())
        self.assertIs(self.list._LinkedList__head, self.list._LinkedList__rear)
        self.assertEqual([i for i in self.list], [1])
        self.assertEqual(len(self.list), 1)

        list_iter2.delete_next()
        self.assertFalse(list_iter2.has_next())
        self.assertIsNone(self.list._LinkedList__head)
        self.assertIsNone(self.list._LinkedList__rear)
        self.assertEqual(len(self.list), 0)

        list_iter = iter(self.list)
        list_iter.insert_after(1)
        next(list_iter)
        list_iter.insert_after(2)
        self.assertIsNot(self.list._LinkedList__head, self.list._LinkedList__rear)

    def test_delete_negatives(self):
        for value in [-5, 2, 6, -4, -6, 4, 1, -3]:
            self.list.append(value)
        
        list_iter = iter(self.list)
        while list_iter.has_next():
            if list_iter.peek() < 0:
                list_iter.delete_next()
            else:
                next(list_iter)
        
        self.assertEqual([i for i in self.list], [2,6,4,1])
        self.assertEqual(len(self.list), 4)

        self.list = LinkedList()
        for value in [-5, 2, 6, -4, -6, 4, 1, -3]:
            self.list.append(value)
        
        list_iter = iter(self.list)
        for value in list_iter:
            if value < 0:
                list_iter.delete_current()
        
        self.assertEqual([i for i in self.list], [2,6,4,1])
        self.assertEqual(len(self.list), 4)


        self.list = LinkedList()
        for value in [-5, -4, -6, -3]:
            self.list.append(value)
        
        list_iter = iter(self.list)
        while list_iter.has_next():
            if list_iter.peek() < 0:
                list_iter.delete_next()
            else:
                next(list_iter)
        
        self.assertEqual([i for i in self.list], [])
        self.assertEqual(len(self.list), 0)
        self.assertIsNone(self.list._LinkedList__head)
        self.assertIsNone(self.list._LinkedList__rear)

        self.list = LinkedList()
        for value in [-5, -4, -6, -3]:
            self.list.append(value)
        
        list_iter = iter(self.list)
        for value in list_iter:
            if value < 0:
                list_iter.delete_current()

        self.assertEqual([i for i in self.list], [])
        self.assertEqual(len(self.list), 0)
        self.assertIsNone(self.list._LinkedList__head)
        self.assertIsNone(self.list._LinkedList__rear)

    
    def test_insert_iterator(self):
        list_iter = iter(self.list)
        list_iter.insert_before(1)
        self.assertEqual(len(self.list), 1)
        self.assertIs(self.list._LinkedList__head, self.list._LinkedList__rear)
        self.assertIsNotNone(self.list._LinkedList__head)
        
        list_iter.insert_before(1)
        self.assertEqual(len(self.list), 2)
        self.assertIsNot(self.list._LinkedList__head, self.list._LinkedList__rear)

        self.list = LinkedList()

        self.list.append(0)
        list_iter = iter(self.list)
        for v in list_iter:
            list_iter.insert_after(v+1)
            if v == 99:
                break
        
        self.assertEqual(len(self.list), 101)
        values = [i for i in self.list]

        self.assertTrue(values == sorted(values[:]))
        self.assertTrue(list_iter.has_next())

        self.list = LinkedList()

        list_iter = iter(self.list)
        for i in range(10):
            list_iter.insert_before(i)

        values = [i for i in self.list]
        
        self.assertTrue(values == list(range(10)))
        self.assertFalse(list_iter.has_next())


        

            