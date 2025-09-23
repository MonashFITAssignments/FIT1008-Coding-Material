from unittest import TestCase
from data_structures.binary_search_tree import BinarySearchTree, BinaryNode


def check_bst_invariant(node: BinaryNode | None, l=None, r=None) -> bool:
    if node is None:
        return True
    if not l is None:
        if node.key < l: return False
    if not r is None:
        if node.key > r: return False
    return (check_bst_invariant(node.left, l, node.key) and
            check_bst_invariant(node.right, node.key, r))


def double(iterator):
    for x in iterator:
        yield (x, x)


class TestBinarySearchTree(TestCase):
    NUM_ITEMS = 15

    def setUp(self):
        self.empty = BinarySearchTree()
        self.one = BinarySearchTree()
        self.left_tree = BinarySearchTree()
        self.right_tree = BinarySearchTree()
        self.balanced = BinarySearchTree()
        self.one[0] = 0
        balanced_items = [7, 3, 1, 0, 2, 5, 4, 6, 11, 9, 8, 10, 13, 12, 14]
        for i in range(self.NUM_ITEMS):
            self.right_tree[i] = i
            self.left_tree[self.NUM_ITEMS - i - 1] = self.NUM_ITEMS - i - 1
            self.balanced[balanced_items[i]] = balanced_items[i]

        self.trees = [self.empty, self.one, self.left_tree, self.right_tree, self.balanced]
        
        self.table = BinarySearchTree()

    def test_len(self):
        self.assertEqual(len(self.empty), 0)
        self.assertEqual(len(self.one), 1)
        self.assertEqual(len(self.left_tree), 15)
        self.assertEqual(len(self.right_tree), 15)
        self.assertEqual(len(self.balanced), 15)

    def test_setup_invariant(self):
        for tree in self.trees:
            self.assertTrue(check_bst_invariant(tree._ProtectedAbstractBinarySearchTree__BinarySearchTree__root))

        incorrect = BinaryNode(1, 1)
        incorrect.right = BinaryNode(0, 0)
        self.assertFalse(check_bst_invariant(incorrect))
        incorrect = BinaryNode(1, 1)
        incorrect.left = BinaryNode(2, 2)
        self.assertFalse(check_bst_invariant(incorrect))
        incorrect = BinaryNode(1, 1)
        incorrect.left = BinaryNode(0, 0)
        incorrect.left.right = BinaryNode(2, 2)
        self.assertFalse(check_bst_invariant(incorrect))

    def test_is_empty(self):
        for tree in self.trees[1:]:
            self.assertFalse(tree.is_empty())
        self.assertTrue(self.empty.is_empty())

    def test_contains(self):
        for x in [-1, 5.5, True, "hi", None]:
            self.assertNotIn(x, self.empty)

        self.assertIn(0, self.one)
        self.assertNotIn(1, self.one)

        for i in range(self.NUM_ITEMS):
            for tree in self.trees[2:]:
                self.assertIn(i, tree)

        self.assertRaises(TypeError, lambda: "hi" in self.one)
        self.assertRaises(TypeError, lambda: None in self.left_tree)

    def test_inorder_iter(self):
        lists = [[x for x in tree] for tree in self.trees]
        for tree_iter_list, tree in zip(lists, self.trees):
            self.assertEqual(tree_iter_list, list(double(range(len(tree)))))

    def test_preorder_iter(self):
        lists = [[x for x in tree.pre_iter()] for tree in self.trees]
        self.assertEqual(lists[0], [])

        self.assertEqual(lists[1], [(0, 0)])

        self.assertEqual(lists[2], list(double(range(self.NUM_ITEMS - 1, -1, -1))))  # left tree

        self.assertEqual(lists[3], list(double(range(self.NUM_ITEMS))))  # right tree

        self.assertEqual(lists[4], list(double([7, 3, 1, 0, 2, 5, 4, 6, 11, 9, 8, 10, 13, 12, 14])))  # balanced

    def test_postorder_iter(self):
        lists = [[x for x in tree.post_iter()] for tree in self.trees]
        self.assertEqual(lists[0], [])

        self.assertEqual(lists[1], [(0, 0)])

        self.assertEqual(lists[2], list(double(range(self.NUM_ITEMS))))

        self.assertEqual(lists[3], list(double(range(self.NUM_ITEMS - 1, -1, -1))))

        self.assertEqual(lists[4], list(double([0, 2, 1, 4, 6, 5, 3, 8, 10, 9, 12, 14, 13, 11, 7])))

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
    
    def test_static(self):
        tree = BinarySearchTree.from_node(None)
        self.assertIs(type(tree), BinarySearchTree)
        self.assertEqual(len(tree), 0)

        node = BinaryNode(1)
        node.left = BinaryNode(2)
        node.right = BinaryNode(3)
        
        tree = BinarySearchTree.from_node(node)
        self.assertEqual(len(tree), 3)

        #Passed bst doesn't satisfy BST invariant so cannot find 2
        self.assertNotIn(2, tree)
        self.assertIn(3, tree)

        self.assertRaises(ValueError, lambda: BinarySearchTree.from_node(node, check_invariant=True))

        self.assertRaises(TypeError, lambda: BinarySearchTree.from_node("hello"))


    def test_str(self):
        empty_str = str(self.empty)
        self.assertEqual(empty_str, "<BinarySearchTree(None)>")

        one_str = str(self.one)
        self.assertEqual(one_str, "<BinarySearchTree(0, 0, None, None)>")

        left_str = str(self.left_tree)
        self.assertEqual(left_str,
                         "<BinarySearchTree(14, 14, (13, 13, (12, 12, (11, 11, (10, 10, (9, 9, (8, 8, (7, 7, (6, 6, (5, 5, (4, 4, (3, 3, (2, 2, (1, 1, (0, 0, None, None), None), None), None), None), None), None), None), None), None), None), None), None), None), None)>")

        right_str = str(self.right_tree)
        self.assertEqual(right_str,
                         "<BinarySearchTree(0, 0, None, (1, 1, None, (2, 2, None, (3, 3, None, (4, 4, None, (5, 5, None, (6, 6, None, (7, 7, None, (8, 8, None, (9, 9, None, (10, 10, None, (11, 11, None, (12, 12, None, (13, 13, None, (14, 14, None, None)))))))))))))))>")

        balanced_str = str(self.balanced)
        self.assertEqual(balanced_str,
                         "<BinarySearchTree(7, 7, (3, 3, (1, 1, (0, 0, None, None), (2, 2, None, None)), (5, 5, (4, 4, None, None), (6, 6, None, None))), (11, 11, (9, 9, (8, 8, None, None), (10, 10, None, None)), (13, 13, (12, 12, None, None), (14, 14, None, None))))>")

    def test_str_indent(self):
        empty_str = self.empty.str(indent=2)
        self.assertEqual(empty_str, "<BinarySearchTree(None)>")

        one_str = self.one.str(indent=2)
        self.assertEqual(one_str,
"""<BinarySearchTree
(
  0, 
  0, 
  None, 
  None
)>""")
        two_tree = BinarySearchTree()
        two_tree[2] = "two"
        two_tree[1] = 1

        two_str = two_tree.str(indent=2)
        self.assertEqual(two_str,
"""<BinarySearchTree
(
  2, 
  two, 
  (
    1, 
    1, 
    None, 
    None
  ), 
  None
)>""")
        self.assertEqual(two_tree.str(indent=4),
"""<BinarySearchTree
(
    2, 
    two, 
    (
        1, 
        1, 
        None, 
        None
    ), 
    None
)>""")

        self.assertEqual(self.left_tree.str(indent=2),
"""<BinarySearchTree
(
  14, 
  14, 
  (
    13, 
    13, 
    (
      12, 
      12, 
      (
        11, 
        11, 
        (
          10, 
          10, 
          (
            9, 
            9, 
            (
              8, 
              8, 
              (
                7, 
                7, 
                (
                  6, 
                  6, 
                  (
                    5, 
                    5, 
                    (
                      4, 
                      4, 
                      (
                        3, 
                        3, 
                        (
                          2, 
                          2, 
                          (
                            1, 
                            1, 
                            (
                              0, 
                              0, 
                              None, 
                              None
                            ), 
                            None
                          ), 
                          None
                        ), 
                        None
                      ), 
                      None
                    ), 
                    None
                  ), 
                  None
                ), 
                None
              ), 
              None
            ), 
            None
          ), 
          None
        ), 
        None
      ), 
      None
    ), 
    None
  ), 
  None
)>""")

        self.assertEqual(self.right_tree.str(indent=2),
"""<BinarySearchTree
(
  0, 
  0, 
  None, 
  (
    1, 
    1, 
    None, 
    (
      2, 
      2, 
      None, 
      (
        3, 
        3, 
        None, 
        (
          4, 
          4, 
          None, 
          (
            5, 
            5, 
            None, 
            (
              6, 
              6, 
              None, 
              (
                7, 
                7, 
                None, 
                (
                  8, 
                  8, 
                  None, 
                  (
                    9, 
                    9, 
                    None, 
                    (
                      10, 
                      10, 
                      None, 
                      (
                        11, 
                        11, 
                        None, 
                        (
                          12, 
                          12, 
                          None, 
                          (
                            13, 
                            13, 
                            None, 
                            (
                              14, 
                              14, 
                              None, 
                              None
                            )
                          )
                        )
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
  )
)>""")

        self.assertEqual(self.balanced.str(indent=2),
"""<BinarySearchTree
(
  7, 
  7, 
  (
    3, 
    3, 
    (
      1, 
      1, 
      (
        0, 
        0, 
        None, 
        None
      ), 
      (
        2, 
        2, 
        None, 
        None
      )
    ), 
    (
      5, 
      5, 
      (
        4, 
        4, 
        None, 
        None
      ), 
      (
        6, 
        6, 
        None, 
        None
      )
    )
  ), 
  (
    11, 
    11, 
    (
      9, 
      9, 
      (
        8, 
        8, 
        None, 
        None
      ), 
      (
        10, 
        10, 
        None, 
        None
      )
    ), 
    (
      13, 
      13, 
      (
        12, 
        12, 
        None, 
        None
      ), 
      (
        14, 
        14, 
        None, 
        None
      )
    )
  )
)>""")
