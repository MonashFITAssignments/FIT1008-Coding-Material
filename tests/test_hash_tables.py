from unittest import TestCase

from data_structures.hash_table_linear_probing import LinearProbeTable
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from data_structures.binary_search_tree import BinarySearchTree
from data_structures.node import BinaryNode


class TestLinearProbeTable(TestCase):
    def setUp(self):
        self.table = LinearProbeTable()

    def test_add(self):
        self.table["Key One"] = 1
        self.assertEqual(len(self.table), 1)
        self.table["Key Two"] = 2
        self.assertEqual(len(self.table), 2)
    
    def test_remove(self):
        self.table["Key Three"] = 3
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.assertEqual(len(self.table), 3)
        
        del self.table["Key One"]
        self.assertEqual(len(self.table), 2)
        self.assertFalse("Key One" in self.table)
        self.assertTrue("Key Two" in self.table)
        self.assertTrue("Key Three" in self.table)
        
        del self.table["Key Three"]
        self.assertEqual(len(self.table), 1)
        self.assertFalse("Key One" in self.table)
        self.assertTrue("Key Two" in self.table)
        self.assertFalse("Key Three" in self.table)
        
        del self.table["Key Two"]
        self.assertEqual(len(self.table), 0)
        self.assertFalse("Key One" in self.table)
        self.assertFalse("Key Two" in self.table)
        self.assertFalse("Key Three" in self.table)
    
    def test_keys(self):
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.table["Key Three"] = 3
        self.assertEqual(len(self.table), 3)

        keys = self.table.keys()
        self.assertTrue("Key One" in keys)
        self.assertTrue("Key Two" in keys)
        self.assertTrue("Key Three" in keys)
        self.assertEqual(len(keys), 3)
    
    def test_values(self):
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.table["Key Three"] = 3
        self.assertEqual(len(self.table), 3)

        values = self.table.values()
        self.assertTrue(1 in values)
        self.assertTrue(2 in values)
        self.assertTrue(3 in values)
        self.assertEqual(len(values), 3)
      
    def test_get(self):
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.table["Key Three"] = 3
        self.assertEqual(len(self.table), 3)

        self.assertEqual(self.table["Key One"], 1)
        self.assertEqual(self.table["Key Two"], 2)
        self.assertEqual(self.table["Key Three"], 3)


class TestHashTableSeparateChaining(TestCase):
    def setUp(self):
        self.table = HashTableSeparateChaining()

    def test_add(self):
        self.table["Key One"] = 1
        self.assertEqual(len(self.table), 1)
        self.table["Key Two"] = 2
        self.assertEqual(len(self.table), 2)
    
    def test_remove(self):
        self.table["Key Three"] = 3
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.assertEqual(len(self.table), 3)
        
        del self.table["Key One"]
        self.assertEqual(len(self.table), 2)
        self.assertFalse("Key One" in self.table)
        self.assertTrue("Key Two" in self.table)
        self.assertTrue("Key Three" in self.table)
        
        del self.table["Key Three"]
        self.assertEqual(len(self.table), 1)
        self.assertTrue("Key Two" in self.table)
        self.assertFalse("Key Three" in self.table)
        
        del self.table["Key Two"]
        self.assertEqual(len(self.table), 0)
        self.assertTrue(self.table.is_empty())
        self.assertFalse("Key Two" in self.table)
    
    def test_keys(self):
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.table["Key Three"] = 3
        self.assertEqual(len(self.table), 3)

        keys = self.table.keys()
        self.assertTrue("Key One" in keys)
        self.assertTrue("Key Two" in keys)
        self.assertTrue("Key Three" in keys)
        self.assertEqual(len(keys), 3)
    
    def test_values(self):
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.table["Key Three"] = 3
        self.assertEqual(len(self.table), 3)

        values = self.table.values()
        self.assertTrue(1 in values)
        self.assertTrue(2 in values)
        self.assertTrue(3 in values)
        self.assertEqual(len(values), 3)
      
    def test_get(self):
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.table["Key Three"] = 3
        self.assertEqual(len(self.table), 3)

        self.assertEqual(self.table["Key One"], 1)
        self.assertEqual(self.table["Key Two"], 2)
        self.assertEqual(self.table["Key Three"], 3)

class TestBinarySearchTree(TestCase):
    def setUp(self):
        self.table = BinarySearchTree()

    def balance_tree(self):
        self.table = BinarySearchTree()
        self.table[4] = 4
        self.table[2] = 2
        self.table[1] = 1
        self.table[3] = 3
        self.table[6] = 6
        self.table[5] = 5
        self.table[7] = 7

    def test_add(self):
        self.table["Key One"] = 1
        self.assertEqual(len(self.table), 1)
        self.table["Key Two"] = 2
        self.assertEqual(len(self.table), 2)
    
    def test_remove(self):
        self.table["Key Three"] = 3
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.assertEqual(len(self.table), 3)
        
        del self.table["Key One"]
        self.assertEqual(len(self.table), 2)
        self.assertFalse("Key One" in self.table)
        self.assertTrue("Key Two" in self.table)
        self.assertTrue("Key Three" in self.table)
        
        del self.table["Key Three"]
        self.assertEqual(len(self.table), 1)
        self.assertTrue("Key Two" in self.table)
        self.assertFalse("Key Three" in self.table)
        
        del self.table["Key Two"]
        self.assertEqual(len(self.table), 0)
        self.assertTrue(self.table.is_empty())
        self.assertFalse("Key Two" in self.table)
    
    def test_keys(self):
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.table["Key Three"] = 3
        self.assertEqual(len(self.table), 3)

        keys = self.table.keys()
        self.assertTrue("Key One" in keys)
        self.assertTrue("Key Two" in keys)
        self.assertTrue("Key Three" in keys)
        self.assertEqual(len(keys), 3)
    
    def test_values(self):
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.table["Key Three"] = 3
        self.assertEqual(len(self.table), 3)

        values = self.table.values()
        self.assertTrue(1 in values)
        self.assertTrue(2 in values)
        self.assertTrue(3 in values)
        self.assertEqual(len(values), 3)
      
    def test_get(self):
        self.table["Key One"] = 1
        self.table["Key Two"] = 2
        self.table["Key Three"] = 3
        self.assertEqual(len(self.table), 3)

        self.assertEqual(self.table["Key One"], 1)
        self.assertEqual(self.table["Key Two"], 2)
        self.assertEqual(self.table["Key Three"], 3)

    def test_iters(self):
        self.balance_tree()

        infix = [n[0] for n in self.table]
        self.assertEqual(infix, [1,2,3,4,5,6,7])
        
        prefix = [n[0] for n in self.table.pre_iter()]
        self.assertEqual(prefix, [4,2,1,3,6,5,7])

        postfix = [n[0] for n in self.table.post_iter()]
        self.assertEqual(postfix, [1,3,2,5,7,6,4])
    
    def test_static(self):
        tree = BinarySearchTree.from_node(None)
        self.assertIs(type(tree), BinarySearchTree)
        self.assertEqual(len(tree), 0)

        node = BinaryNode(1)
        node._left = BinaryNode(2)
        node._right = BinaryNode(3)
        
        
        tree = BinarySearchTree.from_node(node)
        self.assertEqual(len(tree), 3)

