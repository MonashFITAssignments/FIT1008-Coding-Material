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
    def from_node(node: BinaryNode[K, V] | None, length: int = 0, check_invariant: bool = False) -> BinarySearchTree[K, V]:
        """
            Creates a binary search tree object from binary node.
            Useful if a bottom up construction of the tree can be done efficiently.
            Length argument is not checked if passed in.
            :complexity:
                :best: O(1) when length and search invariant are not checked.
                :worst: O(N) where N is the number of nodes in the tree
        """

        def len_aux(current: BinaryNode | None) -> int:
            if current is None:
                return 0
            return 1 + len_aux(current.left) + len_aux(current.right)

        def check_bst_invariant(node: BinaryNode | None, l=None, r=None) -> bool:
            if node is None:
                return True
            if not l is None:
                if node.key < l: return False
            if not r is None:
                if node.key > r: return False
            return (check_bst_invariant(node.left, l, node.key) and
                    check_bst_invariant(node.right, node.key, r))

        if not isinstance(node, (BinaryNode, type(None))):
            raise TypeError(f"Cannot instantiate binary tree with node type: {type(node)}")
        
        if check_invariant:
            if not check_bst_invariant(node):
                raise ValueError("Constructed BinarySearchTree does not satisfy search invariant.")
        
        tree = BinarySearchTree()
        tree.__root = node
        tree.__length = length if length else len_aux(node)

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

    def __str__(self):
        buffer = self.__str_aux(self.__root, [], prefix='', postfix='')
        return '\n'.join(buffer)
    
    def __str_aux(self, current:BinaryNode, buffer:list, prefix='', postfix=''):
        if current is not None:
            real_prefix = prefix[:-2] + postfix
            buffer.append(f'{real_prefix}{current.key}')
            if current._left or current._right:
                self.__str_aux(current._left, buffer, prefix=prefix + '\u2551 ', postfix='\u255f\u2550')
                self.__str_aux(current._right, buffer, prefix=prefix + '  ', postfix='\u2559\u2550')
        else:
            real_prefix = prefix[:-2] + postfix
            buffer.append(f'{real_prefix}')
        return buffer

    def __str__(self) -> str:
        return self.str(0)
