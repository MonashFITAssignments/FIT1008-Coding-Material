from unittest import TestCase
from data_structures.binary_search_tree import BinarySearchTree, BinaryNode


def check_bst_invariant(node: BinaryNode | None, l=None, r=None) -> bool:
    if node is None:
        return True
    if not l is None:
        if node._key < l: return False
    if not r is None:
        if node._key > r: return False
    return (check_bst_invariant(node._left, l, node._key) and
            check_bst_invariant(node._right, node._key, r))


def double(iterator):
    for x in iterator:
        yield (x, x)


class TestBinarySearchTree(TestCase):
    NUM_ITEMS = 15

    def setUp(self):
        self._empty = BinarySearchTree()
        self._one = BinarySearchTree()
        self._left_tree = BinarySearchTree()
        self._right_tree = BinarySearchTree()
        self._balanced = BinarySearchTree()
        self._one[0] = 0
        balanced_items = [7, 3, 1, 0, 2, 5, 4, 6, 11, 9, 8, 10, 13, 12, 14]
        for i in range(self.NUM_ITEMS):
            self._right_tree[i] = i
            self._left_tree[self.NUM_ITEMS - i - 1] = self.NUM_ITEMS - i - 1
            self._balanced[balanced_items[i]] = balanced_items[i]

        self._trees = [self._empty, self._one, self._left_tree, self._right_tree, self._balanced]
        
        self._table = BinarySearchTree()

    def test_len(self):
        self.assertEqual(len(self._empty), 0)
        self.assertEqual(len(self._one), 1)
        self.assertEqual(len(self._left_tree), 15)
        self.assertEqual(len(self._right_tree), 15)
        self.assertEqual(len(self._balanced), 15)

    def test_setup_invariant(self):
        for tree in self._trees:
            self.assertTrue(check_bst_invariant(tree._root))

        incorrect = BinaryNode(1, 1)
        incorrect._right = BinaryNode(0, 0)
        self.assertFalse(check_bst_invariant(incorrect))
        incorrect = BinaryNode(1, 1)
        incorrect._left = BinaryNode(2, 2)
        self.assertFalse(check_bst_invariant(incorrect))
        incorrect = BinaryNode(1, 1)
        incorrect._left = BinaryNode(0, 0)
        incorrect._left._right = BinaryNode(2, 2)
        self.assertFalse(check_bst_invariant(incorrect))

    def test_is_empty(self):
        for tree in self._trees[1:]:
            self.assertFalse(tree.is_empty())
        self.assertTrue(self._empty.is_empty())

    def test_contains(self):
        for x in [-1, 5.5, True, "hi", None]:
            self.assertNotIn(x, self._empty)

        self.assertIn(0, self._one)
        self.assertNotIn(1, self._one)

        for i in range(self.NUM_ITEMS):
            for tree in self._trees[2:]:
                self.assertIn(i, tree)

        self.assertRaises(TypeError, lambda: "hi" in self._one)
        self.assertRaises(TypeError, lambda: None in self._left_tree)

    def test_inorder_iter(self):
        lists = [[x for x in tree] for tree in self._trees]
        for tree_iter_list, tree in zip(lists, self._trees):
            self.assertEqual(tree_iter_list, list(double(range(len(tree)))))

    def test_preorder_iter(self):
        lists = [[x for x in tree.pre_iter()] for tree in self._trees]
        self.assertEqual(lists[0], [])

        self.assertEqual(lists[1], [(0, 0)])

        self.assertEqual(lists[2], list(double(range(self.NUM_ITEMS - 1, -1, -1))))  # left tree

        self.assertEqual(lists[3], list(double(range(self.NUM_ITEMS))))  # right tree

        self.assertEqual(lists[4], list(double([7, 3, 1, 0, 2, 5, 4, 6, 11, 9, 8, 10, 13, 12, 14])))  # balanced

    def test_postorder_iter(self):
        lists = [[x for x in tree.post_iter()] for tree in self._trees]
        self.assertEqual(lists[0], [])

        self.assertEqual(lists[1], [(0, 0)])

        self.assertEqual(lists[2], list(double(range(self.NUM_ITEMS))))

        self.assertEqual(lists[3], list(double(range(self.NUM_ITEMS - 1, -1, -1))))

        self.assertEqual(lists[4], list(double([0, 2, 1, 4, 6, 5, 3, 8, 10, 9, 12, 14, 13, 11, 7])))

    def test_remove(self):
        self._table["Key Three"] = 3
        self._table["Key One"] = 1
        self._table["Key Two"] = 2
        self.assertEqual(len(self._table), 3)
        
        del self._table["Key One"]
        self.assertEqual(len(self._table), 2)
        self.assertFalse("Key One" in self._table)
        self.assertTrue("Key Two" in self._table)
        self.assertTrue("Key Three" in self._table)
        
        del self._table["Key Three"]
        self.assertEqual(len(self._table), 1)
        self.assertTrue("Key Two" in self._table)
        self.assertFalse("Key Three" in self._table)
        
        del self._table["Key Two"]
        self.assertEqual(len(self._table), 0)
        self.assertTrue(self._table.is_empty())
        self.assertFalse("Key Two" in self._table)
    
    def test_keys(self):
        self._table["Key One"] = 1
        self._table["Key Two"] = 2
        self._table["Key Three"] = 3
        self.assertEqual(len(self._table), 3)

        keys = self._table.keys()
        self.assertTrue("Key One" in keys)
        self.assertTrue("Key Two" in keys)
        self.assertTrue("Key Three" in keys)
        self.assertEqual(len(keys), 3)
    
    def test_values(self):
        self._table["Key One"] = 1
        self._table["Key Two"] = 2
        self._table["Key Three"] = 3
        self.assertEqual(len(self._table), 3)

        values = self._table.values()
        self.assertTrue(1 in values)
        self.assertTrue(2 in values)
        self.assertTrue(3 in values)
        self.assertEqual(len(values), 3)
      
    def test_get(self):
        self._table["Key One"] = 1
        self._table["Key Two"] = 2
        self._table["Key Three"] = 3
        self.assertEqual(len(self._table), 3)

        self.assertEqual(self._table["Key One"], 1)
        self.assertEqual(self._table["Key Two"], 2)
        self.assertEqual(self._table["Key Three"], 3)
    
    def test_static(self):
        tree = BinarySearchTree.from_node(None)
        self.assertIs(type(tree), BinarySearchTree)
        self.assertEqual(len(tree), 0)

        node = BinaryNode(1)
        node._left = BinaryNode(2)
        node._right = BinaryNode(3)
        
        tree = BinarySearchTree.from_node(node)
        self.assertEqual(len(tree), 3)

        #Passed bst doesn't satisfy BST invariant so cannot find 2
        self.assertNotIn(2, tree)
        self.assertIn(3, tree)

        self.assertRaises(ValueError, lambda: BinarySearchTree.from_node(node, check_invariant=True))

        self.assertRaises(TypeError, lambda: BinarySearchTree.from_node("hello"))


    def test_str(self):
        empty_str = str(self._empty)
        self.assertEqual(empty_str, "<BinarySearchTree(None)>")

        one_str = str(self._one)
        self.assertEqual(one_str, "<BinarySearchTree(0, 0, None, None)>")

        left_str = str(self._left_tree)
        self.assertEqual(left_str,
                         "<BinarySearchTree(14, 14, (13, 13, (12, 12, (11, 11, (10, 10, (9, 9, (8, 8, (7, 7, (6, 6, (5, 5, (4, 4, (3, 3, (2, 2, (1, 1, (0, 0, None, None), None), None), None), None), None), None), None), None), None), None), None), None), None), None)>")

        right_str = str(self._right_tree)
        self.assertEqual(right_str,
                         "<BinarySearchTree(0, 0, None, (1, 1, None, (2, 2, None, (3, 3, None, (4, 4, None, (5, 5, None, (6, 6, None, (7, 7, None, (8, 8, None, (9, 9, None, (10, 10, None, (11, 11, None, (12, 12, None, (13, 13, None, (14, 14, None, None)))))))))))))))>")

        balanced_str = str(self._balanced)
        self.assertEqual(balanced_str,
                         "<BinarySearchTree(7, 7, (3, 3, (1, 1, (0, 0, None, None), (2, 2, None, None)), (5, 5, (4, 4, None, None), (6, 6, None, None))), (11, 11, (9, 9, (8, 8, None, None), (10, 10, None, None)), (13, 13, (12, 12, None, None), (14, 14, None, None))))>")

    def test_str_indent(self):
        empty_str = self._empty.str(indent=2)
        self.assertEqual(empty_str, "<BinarySearchTree(None)>")

        one_str = self._one.str(indent=2)
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

        self.assertEqual(self._left_tree.str(indent=2),
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

        self.assertEqual(self._right_tree.str(indent=2),
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

        self.assertEqual(self._balanced.str(indent=2),
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
