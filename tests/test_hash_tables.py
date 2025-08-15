from unittest import TestCase

from data_structures.hash_table_linear_probing import LinearProbeTable
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from data_structures.binary_search_tree import BinarySearchTree


class TestLinearProbeTable(TestCase):
    def setUp(self):
        self.table = LinearProbeTable()

class TestHashTableSeparateChaining(TestCase):
    def setUp(self):
        self.table = HashTableSeparateChaining()

class TestDictionaries(TestCase):
    def setUp(self):
        self.dictionaries = [
            LinearProbeTable(),
            HashTableSeparateChaining(),
            BinarySearchTree()
        ]
        self.dictionary = None
    
    def test_add(self):
        for dictionary in self.dictionaries:
            dictionary["Key One"] = 1
            self.assertEqual(len(dictionary), 1)
            dictionary["Key Two"] = 2
            self.assertEqual(len(dictionary), 2)
            dictionary["Key Two"] = 3
            self.assertEqual(len(dictionary), 2)
            self.assertEqual(dictionary["Key Two"], 3, dictionary)
    
    def test_remove(self):
        for dictionary in self.dictionaries:
            dictionary["Key Three"] = 3
            dictionary["Key One"] = 1
            dictionary["Key Two"] = 2
            self.assertEqual(len(dictionary), 3)
            
            del dictionary["Key One"]
            self.assertEqual(len(dictionary), 2)
            self.assertNotIn("Key One", dictionary)
            self.assertIn("Key Two", dictionary)
            self.assertIn("Key Three", dictionary)
            
            del dictionary["Key Three"]
            self.assertEqual(len(dictionary), 1)
            self.assertIn("Key Two", dictionary)
            self.assertNotIn("Key Three", dictionary)
            
            del dictionary["Key Two"]
            self.assertEqual(len(dictionary), 0)
            self.assertTrue(dictionary.is_empty())
            self.assertNotIn("Key Two", dictionary)


            self.assertRaises(KeyError, lambda: dictionary.__delitem__("no key"))
    
    def test_keys(self):
        for dictionary in self.dictionaries:
            dictionary["Key One"] = 1
            dictionary["Key Two"] = 2
            dictionary["Key Three"] = 3
            self.assertEqual(len(dictionary), 3)

            keys = dictionary.keys()
            self.assertTrue("Key One" in keys)
            self.assertTrue("Key Two" in keys)
            self.assertTrue("Key Three" in keys)
            self.assertEqual(len(keys), 3)
    
    def test_values(self):
        for dictionary in self.dictionaries:
            dictionary["Key One"] = 1
            dictionary["Key Two"] = 2
            dictionary["Key Three"] = 3
            self.assertEqual(len(dictionary), 3)

            values = dictionary.values()
            self.assertTrue(1 in values)
            self.assertTrue(2 in values)
            self.assertTrue(3 in values)
            self.assertEqual(len(values), 3)