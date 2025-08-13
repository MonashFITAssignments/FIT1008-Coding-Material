from unittest import TestCase

from data_structures.array_set import ArraySet
from data_structures.bit_vector_set import BitVectorSet
from data_structures.array_sorted_set import ArraySortedSet


class TestArraySet(TestCase):
    def setUp(self):
        self.set = ArraySet(10)
    
    def test_add(self):
        self.set.add(1)
        self.assertEqual(len(self.set), 1)
        self.set.add(2)
        self.assertEqual(len(self.set), 2)
        
        self.assertTrue(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertFalse(3 in self.set)
    
    def test_remove(self):
        self.set.add(3)
        self.set.add(1)
        self.set.add(2)
        self.assertEqual(len(self.set), 3)
        
        self.set.remove(1)
        self.assertEqual(len(self.set), 2)
        self.assertFalse(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertTrue(3 in self.set)
        
        self.set.remove(3)
        self.assertEqual(len(self.set), 1)
        self.assertFalse(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertFalse(3 in self.set)
        
        self.set.remove(2)
        self.assertEqual(len(self.set), 0)
        self.assertFalse(1 in self.set)
        self.assertFalse(2 in self.set)
        self.assertFalse(3 in self.set)

    def test_values(self):
        for i in range(1, 11):
            self.set.add(i)
        
        values = self.set.values()
        self.assertEqual(len(values), 10)
        
        for i in range(1, 11):
            self.assertTrue(i in values)
    
    def test_clear(self):
        for i in range(10):
            self.set.add(i)
        self.assertEqual(len(self.set), 10)

        self.set.clear()
        self.assertEqual(len(self.set), 0)
        self.assertTrue(self.set.is_empty())
    
    def test_contains(self):
        self.assertFalse(1 in self.set)
        self.set.add(1)
        self.assertTrue(1 in self.set)
        self.set.remove(1)
        self.assertFalse(1 in self.set)
    
    def test_union(self):
        set1 = ArraySet(10)
        set2 = ArraySet(10)
        
        for i in range(10):
            set1.add(i)
            set2.add(i + 5)
        
        union = set1.union(set2)
        self.assertEqual(len(union), 15)
        
        for i in range(15):
            self.assertTrue(i in union)
    
    def test_intersection(self):
        set1 = ArraySet(10)
        set2 = ArraySet(10)
        
        for i in range(10):
            set1.add(i)
            set2.add(i + 5)
        
        intersection = set1.intersection(set2)
        self.assertEqual(len(intersection), 5)
        
        for i in range(5, 10):
            self.assertTrue(i in intersection)
        
        for i in range(5):
            self.assertFalse(i in intersection)
        
        for i in range(10, 15):
            self.assertFalse(i in intersection)

    def test_difference(self):
        set1 = ArraySet(10)
        set2 = ArraySet(10)

        for i in range(10):
            set1.add(i)
            set2.add(i + 5)
        
        difference = set1.difference(set2)
        self.assertEqual(len(difference), 5)

        for i in range(5):
            self.assertTrue(i in difference)
        
        for i in range(5, 15):
            self.assertFalse(i in difference)
    
    def test_values(self):
        self.set.add('hi')
        self.set.add('hello')
        self.set.add('goodbye')
        
        value_array = self.set.values()
        self.assertIn('hi', value_array)
        self.assertIn('hello', value_array)
        self.assertIn('goodbye', value_array)

    def test_string(self):
        self.assertEqual(str(self.set), '<ArraySet {}>')

        self.set.add(1)
        self.set.add(1)
        self.set.add(3)
        self.assertEqual(str(self.set), '<ArraySet {1, 3}>')

class TestSortedArraySet(TestCase):
    def setUp(self):
        self.set = ArraySortedSet(10)
    
    def test_add(self):
        self.set.add(1)
        self.assertEqual(len(self.set), 1)
        self.set.add(2)
        self.assertEqual(len(self.set), 2)
        
        self.assertTrue(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertFalse(3 in self.set)
    
    def test_remove(self):
        self.set.add(3)
        self.set.add(1)
        self.set.add(2)
        self.assertEqual(len(self.set), 3)
        
        self.set.remove(1)
        self.assertEqual(len(self.set), 2)
        self.assertFalse(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertTrue(3 in self.set)
        
        self.set.remove(3)
        self.assertEqual(len(self.set), 1)
        self.assertFalse(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertFalse(3 in self.set)
        
        self.set.remove(2)
        self.assertEqual(len(self.set), 0)
        self.assertFalse(1 in self.set)
        self.assertFalse(2 in self.set)
        self.assertFalse(3 in self.set)

    def test_values(self):
        for i in range(1, 11):
            self.set.add(i)
        
        values = self.set.values()
        self.assertEqual(len(values), 10)
        
        for i in range(1, 11):
            self.assertTrue(i in values)
    
    def test_clear(self):
        for i in range(10):
            self.set.add(i)
        self.assertEqual(len(self.set), 10)

        self.set.clear()
        self.assertEqual(len(self.set), 0)
        self.assertTrue(self.set.is_empty())
    
    def test_contains(self):
        self.assertFalse(1 in self.set)
        self.set.add(1)
        self.assertTrue(1 in self.set)
        self.set.remove(1)
        self.assertFalse(1 in self.set)
    
    def test_union(self):
        set1 = ArraySortedSet(10)
        set2 = ArraySortedSet(10)
        
        for i in range(10):
            set1.add(i)
            set2.add(i + 5)
        
        union = set1.union(set2)
        self.assertEqual(len(union), 15)
        
        for i in range(15):
            self.assertTrue(i in union)

    def test_magic_union(self):
        set1 = ArraySortedSet(10)
        set2 = ArraySortedSet(10)
        
        for i in range(10):
            set1.add(i)
            set2.add(i + 5)
        
        union = set1 | set2
        self.assertEqual(len(union), 15)
        
        for i in range(15):
            self.assertTrue(i in union)
    
    def test_intersection(self):
        set1 = ArraySortedSet(10)
        set2 = ArraySortedSet(10)
        
        for i in range(10):
            set1.add(i)
            set2.add(i + 5)
        
        intersection = set1.intersection(set2)
        self.assertEqual(len(intersection), 5)
        
        for i in range(5, 10):
            self.assertTrue(i in intersection)
        
        for i in range(5):
            self.assertFalse(i in intersection)
        
        for i in range(10, 15):
            self.assertFalse(i in intersection)

    def test_magic_intersection(self):
        set1 = ArraySortedSet(10)
        set2 = ArraySortedSet(10)
        
        for i in range(10):
            set1.add(i)
            set2.add(i + 5)
        
        intersection = set1 & set2
        self.assertEqual(len(intersection), 5)
        
        for i in range(5, 10):
            self.assertTrue(i in intersection)
        
        for i in range(5):
            self.assertFalse(i in intersection)
        
        for i in range(10, 15):
            self.assertFalse(i in intersection)

    def test_difference(self):
        set1 = ArraySortedSet(10)
        set2 = ArraySortedSet(10)

        for i in range(10):
            set1.add(i)
            set2.add(i + 5)
        
        difference = set1.difference(set2)
        self.assertEqual(len(difference), 5)

        for i in range(5):
            self.assertTrue(i in difference)
        
        for i in range(5, 15):
            self.assertFalse(i in difference)

    def test_magic_difference(self):
        set1 = ArraySortedSet(10)
        set2 = ArraySortedSet(10)

        for i in range(10):
            set1.add(i)
            set2.add(i + 5)
        
        difference = set1 - set2
        self.assertEqual(len(difference), 5)

        for i in range(5):
            self.assertTrue(i in difference)
        
        for i in range(5, 15):
            self.assertFalse(i in difference)

    def test_values(self):
        self.set.add('hi')
        self.set.add('hello')
        self.set.add('goodbye')
        
        value_array = self.set.values()
        self.assertIn('hi', value_array)
        self.assertIn('hello', value_array)
        self.assertIn('goodbye', value_array)

    def test_string(self):
        self.assertEqual(str(self.set), '<ArraySortedSet {}>')

        self.set.add(3)
        self.set.add(1)
        self.assertEqual(str(self.set), '<ArraySortedSet {1, 3}>')

class TestBitVectorSet(TestCase):
    def setUp(self):
        self.set = BitVectorSet()
    
    def test_add(self):
        self.set.add(1)
        self.assertEqual(len(self.set), 1)
        self.set.add(2)
        self.assertEqual(len(self.set), 2)
        
        self.assertTrue(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertFalse(3 in self.set)
    
    def test_remove(self):
        self.set.add(3)
        self.set.add(1)
        self.set.add(2)
        self.assertEqual(len(self.set), 3)
        
        self.set.remove(1)
        self.assertEqual(len(self.set), 2)
        self.assertFalse(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertTrue(3 in self.set)
        
        self.set.remove(3)
        self.assertEqual(len(self.set), 1)
        self.assertFalse(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertFalse(3 in self.set)
        
        self.set.remove(2)
        self.assertEqual(len(self.set), 0)
        self.assertFalse(1 in self.set)
        self.assertFalse(2 in self.set)
        self.assertFalse(3 in self.set)
    
    def test_clear(self):
        for i in range(1, 11):
            self.set.add(i)
        self.assertEqual(len(self.set), 10)

        self.set.clear()
        self.assertEqual(len(self.set), 0)
        self.assertTrue(self.set.is_empty())
    
    def test_contains(self):
        self.assertFalse(1 in self.set)
        self.set.add(1)
        self.assertTrue(1 in self.set)
        self.set.remove(1)
        self.assertFalse(1 in self.set)
    
    def test_union(self):
        set1 = BitVectorSet()
        set2 = BitVectorSet()
        
        for i in range(1, 11):
            set1.add(i)
            set2.add(i + 5)
        
        union = set1.union(set2)
        self.assertEqual(len(union), 15)
        
        for i in range(1, 16):
            self.assertTrue(i in union)
    
    def test_intersection(self):
        set1 = BitVectorSet()
        set2 = BitVectorSet()
        
        for i in range(1, 11):
            set1.add(i)
            set2.add(i + 5)
        
        intersection = set1.intersection(set2)
        self.assertEqual(len(intersection), 5)

        for i in range(6, 11):
            self.assertTrue(i in intersection)
        
        for i in range(1, 6):
            self.assertFalse(i in intersection)
        
        for i in range(11, 16):
            self.assertFalse(i in intersection)
    
    def test_difference(self):
        set1 = BitVectorSet()
        set2 = BitVectorSet()

        for i in range(1, 11):
            set1.add(i)
            set2.add(i + 5)
        
        difference = set1.difference(set2)
        self.assertEqual(len(difference), 5)

        for i in range(1, 6):
            self.assertTrue(i in difference)
        
        for i in range(6, 16):
            self.assertFalse(i in difference)

    def test_invalid_entry_types(self):
        self.assertRaises(TypeError, self.set.add, 0)
        self.assertRaises(TypeError, self.set.add, -1)
        self.assertRaises(TypeError, self.set.add, 0.5)
    
    def test_values(self):
        self.set.add(4)
        self.set.add(15)
        self.set.add(23)
        
        value_array = self.set.values()
        self.assertIn(4, value_array)
        self.assertIn(15, value_array)
        self.assertIn(23, value_array)
    
    def test_string(self):
        self.assertEqual(str(self.set), '<BitVectorSet {}>')

        self.set.add(1)
        self.set.add(1)
        self.set.add(3)
        self.assertEqual(str(self.set), '<BitVectorSet {1, 3}>')
