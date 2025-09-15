from unittest import TestCase

from data_structures.hash_table_linear_probing import LinearProbeTable
from data_structures.hash_table_quadratic_probing import QuadraticProbeTable
from data_structures.hash_table_double_hashing import DoubleHashingTable
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from data_structures.binary_search_tree import BinarySearchTree


class TestLinearProbeTable(TestCase):
    def setUp(self):
        self.table = LinearProbeTable()

class TestQuadraticProbeTable(TestCase):
    def setUp(self):
        self.table = QuadraticProbeTable()

class TestDoubleHashingProbeTable(TestCase):
    def setUp(self):
        self.table = DoubleHashingTable()

class TestHashTableSeparateChaining(TestCase):
    def setUp(self):
        self.table = HashTableSeparateChaining()

class TetsHashTables(TestCase):
    def setUp(self):
        self.dictionaries = [
            LinearProbeTable(),
            DoubleHashingTable(),
            QuadraticProbeTable(),
            HashTableSeparateChaining(),
        ]
    
    def test_resize(self):
        restricted_tables = [
            LinearProbeTable([2,10]),
            DoubleHashingTable([2,10]),
            QuadraticProbeTable([2,10]),
            # HashTableSeparateChaining([2,10])
        ]
        for table in restricted_tables:
            for i in range(5):
                table[str(i)] = i
            table["5"] = 5 #This will call resize, but fail as reached max size
            table["6"] = 5 #This again will call resize as it is still above load factor, this should work as well
            for _ in range(30):
                table["6"] = 6
    
    def test_str(self):
        for dictionary in self.dictionaries:
            dictionary["Key One"] = 1
            self.assertEqual(len(dictionary), 1)
            dictionary["Key Two"] = 2
            self.assertEqual(len(dictionary), 2)
            dictionary["Key Two"] = 3
            self.assertEqual(len(dictionary), 2)
            self.assertEqual(dictionary["Key Two"], 3, dictionary)
            dict_type_name = type(dictionary).__name__
            self.assertEqual(str(dictionary), f"<{dict_type_name}\n(Key One, 1)\n(Key Two, 3)\n>")

class TestDictionaries(TestCase):
    def setUp(self):
        self.dictionaries = [
            LinearProbeTable(),
            DoubleHashingTable(),
            QuadraticProbeTable(),
            DoubleHashingTable(),
            HashTableSeparateChaining(),
            BinarySearchTree()
        ]
    
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
            dictionary["Key Four"] = 4
            dictionary["Key Two"] = 2
            dictionary["Key Five"] = 5
            self.assertEqual(len(dictionary), 5)
            
            del dictionary["Key One"]
            self.assertEqual(len(dictionary), 4)
            self.assertNotIn("Key One", dictionary)
            self.assertIn("Key Two", dictionary)
            self.assertIn("Key Three", dictionary)
            self.assertIn("Key Four", dictionary)
            self.assertIn("Key Five", dictionary)

            del dictionary["Key Three"]
            self.assertEqual(len(dictionary), 3)
            self.assertIn("Key Two", dictionary)
            self.assertNotIn("Key Three", dictionary)
            self.assertIn("Key Four", dictionary)
            self.assertIn("Key Five", dictionary)

            del dictionary["Key Two"]
            self.assertEqual(len(dictionary), 2)
            self.assertNotIn("Key Two", dictionary)
            self.assertIn("Key Four", dictionary)
            self.assertIn("Key Five", dictionary)

            del dictionary["Key Four"]
            self.assertEqual(len(dictionary), 1)
            self.assertNotIn("Key Four", dictionary)
            self.assertIn("Key Five", dictionary)

            del dictionary["Key Five"]
            self.assertEqual(len(dictionary), 0)
            self.assertNotIn("Key Five", dictionary)
            self.assertTrue(dictionary.is_empty())

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
    