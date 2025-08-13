""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import Tuple

from data_structures.abstract_binary_search_tree import AbstractBinarySearchTree, K, V
from data_structures.abstract_hash_table import HashTable
from data_structures.linked_stack import LinkedStack
from data_structures.node import BinaryNode, Generic
from data_structures.referential_array import ArrayR


class BSTPreOrderIterator(Generic[K,V]):
    """ Pre-order iterator for the binary search tree.
        Performs stack-based BST traversal.
    """

    def __init__(self, root: BinaryNode[K, V] | None) -> None:
        """ Iterator initialiser. """
        self.__stack = LinkedStack[BinaryNode[K,V]]()
        if root is not None:
            self.__stack.push(root)

    def __iter__(self) -> BSTPreOrderIterator:
        """ Standard __iter__() method for initialisers. Returns itself. """
        return self

    def __next__(self) -> Tuple[K, V]:
        """ The main body of the iterator.
            Returns keys of the BST one by one respecting the pre-order.
        """
        if self.__stack.is_empty():
            raise StopIteration
        current = self.__stack.pop()
        if current.right:
            self.__stack.push(current.right)
        if current.left:
            self.__stack.push(current.left)

        return current.key, current.item

class BSTInOrderIterator(Generic[K,V]):
    """ In-order iterator for the binary search tree.
        Performs stack-based BST traversal.
    """

    def __init__(self, root: BinaryNode[K, V] | None) -> None:
        """ Iterator initialiser. """

        self.__stack = LinkedStack[BinaryNode[K,V]]()
        self.__current = root

    def __iter__(self) -> BSTInOrderIterator:
        """ Standard __iter__() method for initialisers. Returns itself. """
        return self

    def __next__(self) -> Tuple[K, V]:
        """ The main body of the iterator.
            Returns keys of the BST one by one respecting the in-order.
        """
        while self.__current:
            self.__stack.push(self.__current)
            self.__current = self.__current.left

        if self.__stack.is_empty():
            raise StopIteration

        result = self.__stack.pop()
        self.__current = result.right

        return result.key, result.item


class BSTPostOrderIterator(Generic[K,V]):
    """ Post-order iterator for the binary search tree.
        Performs stack-based BST traversal.
    """

    def __init__(self, root: BinaryNode[K, V] | None) -> None:
        """ Iterator initialiser. """
        self.__stack = LinkedStack[Tuple[BinaryNode[K, V], bool]]()
        if root is not None:
            self.__stack.push((root, False))

    def __iter__(self) -> BSTPostOrderIterator:
        """ Standard __iter__() method for initialisers. Returns itself. """
        return self

    def __next__(self) -> Tuple[K, V]:
        """ The main body of the iterator.
            Returns keys of the BST one by one respecting the post-order.
        """
        while True:
            if self.__stack.is_empty():
                raise StopIteration
            current, expanded = self.__stack.pop()
            if expanded:
                return current.key, current.item
            else:
                self.__stack.push((current, True))
                if current.right:
                    self.__stack.push((current.right, False))
                if current.left:
                    self.__stack.push((current.left, False))


class BinarySearchTree(AbstractBinarySearchTree[K,V]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        self.__root: BinaryNode[K, V] | None = None
        self.__length = 0

    @staticmethod
    def from_node(node: BinaryNode[K, V] | None, length: int = 0) -> BinarySearchTree[K, V]:
        """
            Creates a binary search tree object from binary node.
            Useful if a bottom up construction of the tree can be done efficiently.
            Length argument is not checked if passed in.
            Search invariant is not checked.
            :complexity:
                :best: O(1) when length is passed
                :worst: O(N) where N is the number of nodes in the tree
        """

        def len_aux(current: BinaryNode | None) -> int:
            if current is None:
                return 0
            return 1 + len_aux(current.left) + len_aux(current.right)

        if not isinstance(node, (BinaryNode, type(None))):
            raise TypeError(f"Cannot instantiate binary tree with node type: {type(node)}")
        tree = BinarySearchTree()
        tree._BinarySearchTree__root = node
        tree._BinarySearchTree__length = length if length else len_aux(node)

        return tree

    def __get_successor(self, current: BinaryNode[K, V]) -> BinaryNode[K, V] | None:
        """
            Get successor of the current node.
            It should be a node in the subtree rooted at current having the smallest key among all the
            larger keys.
            If no such node exists, then none should be returned.
        """
        if current is None:
            return None
        return self.__get_min_node(current.right)
    
    def __get_predecessor(self, current: BinaryNode[K, V]) -> BinaryNode[K, V] | None:
        """
            Get predecessor of the current node.
            It should be a node in the subtree rooted at current having the largest key among all the
            smaller keys.
            If no such node exists, then none should be returned.
        """
        if current is None:
            return None
        return self.__get_max_node(current.left)

    def __get_min_node(self, current: BinaryNode[K, V]) -> BinaryNode[K, V] | None:
        """
            Get a node having the smallest key in the current sub-tree.
        """
        if current is None:
            return None
        while current.left:
            current = current.left
        return current

    def __get_max_node(self, current: BinaryNode[K, V]) -> BinaryNode[K, V] | None:
        """
            Get a node having the largest key in the current sub-tree.
        """
        if current is None:
            return None
        while current.right:
            current = current.right
        return current

    def is_leaf(self, current: BinaryNode[K, V]) -> bool:
        """ Simple check whether or not the node is a leaf. """
        return current.left is None and current.right is None

    def items(self) -> ArrayR[Tuple[K, V]]:
        array = ArrayR(len(self))
        for i, node in enumerate(self):
            tup = (node[0], node[1])
            array[i] = tup
        return array

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.__root is None

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST
            :complexity: see __getitem__(self, key: K) -> (K, I)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __iter__(self) -> BSTInOrderIterator:
        """ Create an in-order iterator. """
        return BSTInOrderIterator(self.__root)

    def post_iter(self) -> BSTPostOrderIterator:
        return BSTPostOrderIterator(self.__root)

    def pre_iter(self) -> BSTPreOrderIterator:
        return BSTPreOrderIterator(self.__root)

    def __delitem__(self, key: K) -> None:
        def delete_aux(bst: BinarySearchTree[K, V], current: BinaryNode[K, V], key: K) -> BinaryNode[K, V]:
            """
                Attempts to delete an item from the tree, it uses the Key to
                determine the node to delete.
            """

            if current is None:  # key not found
                raise ValueError('Deleting non-existent item')
            elif key < current.key:
                current.left = delete_aux(bst, current.left, key)
            elif key > current.key:
                current.right = delete_aux(bst, current.right, key)
            else:  # we found our key => do actual deletion
                if self.is_leaf(current):
                    self.__length -= 1
                    return None
                elif current.left is None:
                    self.__length -= 1
                    return current.right
                elif current.right is None:
                    self.__length -= 1
                    return current.left

                # general case => find a successor
                successor = bst.__get_successor(current)
                current.key = successor.key
                current.item = successor.item
                current.right = delete_aux(current.right, successor.key)

            return current

        self.__root = delete_aux(self, self.__root, key)

    def __getitem__(self, key: K) -> V:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """

        def get_tree_node_by_key(current: BinaryNode[K, V], key: K) -> BinaryNode[K, V]:
            if current is None:  # base case: empty
                raise KeyError(f'Key not found: {key}')
            elif key == current.key:  # base case: found
                return current
            elif key < current.key:
                return get_tree_node_by_key(current.left, key)
            else:  # key > current.key
                return get_tree_node_by_key(current.right, key)

        return get_tree_node_by_key(self.__root, key).item

    def __setitem__(self, key: K, item: V) -> None:
        def insert_aux(current: BinaryNode[K, V], key: K, item: V, current_depth: int) -> BinaryNode[K, V] | None:
            """
                Attempts to insert an item into the tree, it uses the Key to insert it
                :complexity:
                    :best: O(CompK) inserts the item at the root.
                    :worst: O(CompK * D) inserting at the bottom of the tree
                where D is the depth of the tree
                CompK is the complexity of comparing the keys
            """
            if current is None:  # base case: at the leaf
                current = BinaryNode(item, key)
                self.__length += 1
            elif key < current.key:
                current.left = insert_aux(current.left, key, item, current_depth + 1)
            elif key > current.key:
                current.right = insert_aux(current.right, key, item, current_depth + 1)
            else:  # key == current.key
                current.item = item
            return current

        self.__root = insert_aux(self.__root, key, item, 1)

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """
        return self.__length

    def str(self, indent: int) -> str:
        def str_aux(current: BinaryNode[K, V] | None, indent, depth) -> str:
            prefix = "\n" + " " * indent * depth if indent > 0 else ""
            if current is None:
                return prefix[:-indent] + str(None)
            return f"{prefix[:-indent]}({prefix}{current.key}, {prefix}{current.item}, {str_aux(current.left, indent, depth + 1)}, {str_aux(current.right, indent, depth + 1)}{prefix[:-indent]})"

        if self.__root is None:
            return f"<BinarySearchTree({self.__root})>"
        tree_str = str_aux(self.__root, indent = indent, depth = 1)
        return f"<BinarySearchTree{tree_str}>"

    def __str__(self) -> str:
        return self.str(0)
