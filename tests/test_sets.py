from unittest import TestCase

from data_structures.abstract_set import Set
from data_structures.array_set import ArraySet
from data_structures.bit_vector_set import BitVectorSet
from data_structures.array_sorted_set import ArraySortedSet

class TestArraySet(TestCase):
    def setUp(self):
        self._set = ArraySet(10)

    def test_contains(self):
        self.assertFalse(1 in self._set)
        self._set.add(1)
        self.assertTrue(1 in self._set)
        self._set.remove(1)
        self.assertFalse(1 in self._set)
    
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
        self._set.add('hi')
        self._set.add('hello')
        self._set.add('goodbye')
        
        value_array = self._set.values()
        self.assertIn('hi', value_array)
        self.assertIn('hello', value_array)
        self.assertIn('goodbye', value_array)

    def test_string(self):
        self.assertEqual(str(self._set), '<ArraySet {}>')

        self._set.add(1)
        self._set.add(1)
        self._set.add(3)
        self.assertEqual(str(self._set), '<ArraySet {1, 3}>')

class TestSortedArraySet(TestCase):
    def setUp(self):
        self._set = ArraySortedSet(10)
    
    def test_contains(self):
        self.assertFalse(1 in self._set)
        self._set.add(1)
        self.assertTrue(1 in self._set)
        self._set.remove(1)
        self.assertFalse(1 in self._set)
    
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
        self._set.add('hi')
        self._set.add('hello')
        self._set.add('goodbye')
        
        value_array = self._set.values()
        self.assertIn('hi', value_array)
        self.assertIn('hello', value_array)
        self.assertIn('goodbye', value_array)

    def test_string(self):
        self.assertEqual(str(self._set), '<ArraySortedSet {}>')

        self._set.add(3)
        self._set.add(1)
        self.assertEqual(str(self._set), '<ArraySortedSet {1, 3}>')

class TestBitVectorSet(TestCase):
    def setUp(self):
        self._set = BitVectorSet()
    
    def test_contains(self):
        self.assertFalse(1 in self._set)
        self._set.add(1)
        self.assertTrue(1 in self._set)
        self._set.remove(1)
        self.assertFalse(1 in self._set)
    
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
        self.assertRaises(TypeError, self._set.add, 0)
        self.assertRaises(TypeError, self._set.add, -1)
        self.assertRaises(TypeError, self._set.add, 0.5)
    
    def test_string(self):
        self.assertEqual(str(self._set), '<BitVectorSet {}>')

        self._set.add(1)
        self._set.add(1)
        self._set.add(3)
        self.assertEqual(str(self._set), '<BitVectorSet {1, 3}>')


class TestSets(TestCase):
    CAPACITY = 10
    def setUp(self):
        self._sets:list[Set] = [ArraySet(self.CAPACITY), ArraySortedSet(self.CAPACITY), BitVectorSet()]

    def test_add(self):
        for set_ in self._sets:
            set_.add(1)
            self.assertEqual(len(set_), 1)
            set_.add(2)
            self.assertEqual(len(set_), 2)
            
            self.assertTrue(1 in set_)
            self.assertTrue(2 in set_)
            self.assertFalse(3 in set_)
    
    def test_add_duplicates(self):
        for set_ in self._sets:
            set_.add(1)
            self.assertEqual(len(set_), 1)
            set_.add(1)
            self.assertEqual(len(set_), 1)
            for _ in range(self.CAPACITY):
                set_.add(1)
    
    def test_remove(self):
        for set_ in self._sets:
            set_.add(3)
            set_.add(1)
            set_.add(2)
            self.assertEqual(len(set_), 3)
            
            set_.remove(1)
            self.assertEqual(len(set_), 2)
            self.assertFalse(1 in set_)
            self.assertTrue(2 in set_)
            self.assertTrue(3 in set_)
            
            set_.remove(3)
            self.assertEqual(len(set_), 1)
            self.assertFalse(1 in set_)
            self.assertTrue(2 in set_)
            self.assertFalse(3 in set_)
            
            set_.remove(2)
            self.assertEqual(len(set_), 0)
            self.assertFalse(1 in set_)
            self.assertFalse(2 in set_)
            self.assertFalse(3 in set_)

            self.assertRaises(KeyError, lambda: set_.remove(5))

    def test_clear(self):
        for set_ in self._sets:
            for i in range(1, 11):
                set_.add(i)
            self.assertEqual(len(set_), 10)

            set_.clear()
            self.assertEqual(len(set_), 0)
            self.assertTrue(set_.is_empty())

            for i in range(11,21):
                set_.add(i)

    def test_values(self):
        for set_ in self._sets:
            set_.add(4)
            set_.add(15)
            set_.add(23)
            
            value_array = set_.values()
            self.assertIn(4, value_array)
            self.assertIn(15, value_array)
            self.assertIn(23, value_array)
            self.assertEqual(3, len(value_array))
