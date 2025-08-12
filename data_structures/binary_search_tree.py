""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

import math
from typing import TypeVar, Tuple

from data_structures.linked_list import LinkedList
from data_structures.linked_stack import LinkedStack
from data_structures.node import BinaryNode, Generic
from data_structures.abstract_hash_table import HashTable
from data_structures.referential_array import ArrayR

# generic types
K = TypeVar('K')
V = TypeVar('V')
T = TypeVar('T')


class BSTPreOrderIterator(Generic[K,V]):
    """ Pre-order iterator for the binary search tree.
        Performs stack-based BST traversal.
    """

    def __init__(self, root: BinaryNode[K, V] | None) -> None:
        """ Iterator initialiser. """

        self.stack = LinkedStack[BinaryNode[K,V]]()
        if root is not None:
            self.stack.push(root)

    def __iter__(self) -> BSTPreOrderIterator:
        """ Standard __iter__() method for initialisers. Returns itself. """

        return self

    def __next__(self) -> Tuple[K, V]:
        """ The main body of the iterator.
            Returns keys of the BST one by one respecting the pre-order.
        """

        if self.stack.is_empty():
            raise StopIteration
        current = self.stack.pop()
        if current._right:
            self.stack.push(current._right)
        if current._left:
            self.stack.push(current._left)
        return (current.key, current.item)


class BSTInOrderIterator(Generic[K,V]):
    """ In-order iterator for the binary search tree.
        Performs stack-based BST traversal.
    """

    def __init__(self, root: BinaryNode[K, V] | None) -> None:
        """ Iterator initialiser. """

        self.stack = LinkedStack[BinaryNode[K,V]]()
        self.current = root

    def __iter__(self) -> BSTInOrderIterator:
        """ Standard __iter__() method for initialisers. Returns itself. """

        return self

    def __next__(self) -> Tuple[K, V]:
        """ The main body of the iterator.
            Returns keys of the BST one by one respecting the in-order.
        """

        while self.current:
            self.stack.push(self.current)
            self.current = self.current._left

        if self.stack.is_empty():
            raise StopIteration

        result = self.stack.pop()
        self.current = result._right

        return (result.key, result.item)


class BSTPostOrderIterator(Generic[K,V]):
    """ Post-order iterator for the binary search tree.
        Performs stack-based BST traversal.
    """

    def __init__(self, root: BinaryNode[K, V] | None) -> None:
        """ Iterator initialiser. """

        self.stack = LinkedStack[Tuple[BinaryNode, bool]]()
        if root is not None:
            self.stack.push((root, False))

    def __iter__(self) -> BSTPostOrderIterator:
        """ Standard __iter__() method for initialisers. Returns itself. """
        return self

    def __next__(self) -> Tuple[K, V]:
        """ The main body of the iterator.
            Returns keys of the BST one by one respecting the post-order.
        """

        while True:
            if self.stack.is_empty():
                raise StopIteration
            current, expanded = self.stack.pop()
            if expanded:
                return (current.key, current.item)
            else:
                self.stack.push((current, True))
                if current._right:
                    self.stack.push((current._right, False))
                if current._left:
                    self.stack.push((current._left, False))


class BinarySearchTree(HashTable[K,V]):
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
            return 1 + len_aux(current._left) + len_aux(current._right)
        
        if not isinstance(node, (BinaryNode, type(None))):
            raise TypeError(f"Cannot instantiate binary tree with node type: {type(node)}")
        tree = BinarySearchTree()
        tree.__root = node
        tree.__length = length if length else len_aux(node)

        return tree

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.__root is None

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.__length

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

    def __getitem__(self, key: K) -> V:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        return self.__get_tree_node_by_key_aux(self.__root, key).item

    def __get_tree_node_by_key_aux(self, current: BinaryNode | None, key: K) -> BinaryNode:
        if current is None:  # base case: empty
            raise KeyError(f'Key not found: {key}')
        elif key == current.key:  # base case: found
            return current
        elif key < current.key:
            return self.__get_tree_node_by_key_aux(current._left, key)
        else:  # key > current.key
            return self.__get_tree_node_by_key_aux(current._right, key)

    def __setitem__(self, key: K, item: V) -> None:
        self.__root = self.__insert_aux(self.__root, key, item, 1)

    def __insert_aux(self, current: BinaryNode|None, key: K, item: V, current_depth: int) -> BinaryNode:
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
            current._left = self.__insert_aux(current._left, key, item, current_depth + 1)
        elif key > current.key:
            current._right = self.__insert_aux(current._right, key, item, current_depth + 1)
        else:  # key == current.key
            current.item = item
        return current

    def __delitem__(self, key: K) -> None:
        self.__root = self.__delete_aux(self.__root, key)

    def __delete_aux(self, current: BinaryNode|None, key: K) -> BinaryNode | None:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current._left = self.__delete_aux(current._left, key)
        elif key > current.key:
            current._right = self.__delete_aux(current._right, key)
        else:  # we found our key => do actual deletion
            if self._is_leaf(current):
                self.__length -= 1
                return None
            elif current._left is None:
                self.__length -= 1
                return current._right
            elif current._right is None:
                self.__length -= 1
                return current._left

            # general case => find a successor
            successor = self.__get_minimal(current._right)
            current.key = successor.key
            current.item = successor.item
            current._right = self.__delete_aux(current._right, successor.key)

        return current

    def __get_minimal(self, current: BinaryNode) -> BinaryNode:
        """
            Get a node having the smallest key in the current sub-tree.
        """
        if current is None:
            return None
        while current._left:
            current = current._left
        return current

    def __get_maximal(self, current: BinaryNode | None) -> BinaryNode | None:
        """
            Get a node having the largest key in the current sub-tree.
        """
        if current is None:
            return None
        while current._right:
            current = current._right
        return current

    def _is_leaf(self, current: BinaryNode) -> bool:
        """ Simple check whether or not the node is a leaf. """

        return current._left is None and current._right is None

    def items(self) -> ArrayR[Tuple[K, V]]:
        array = ArrayR(len(self))
        for i, tup in enumerate(self):
            array[i] = tup
        return array

    def __str__(self):
        return self.str(indent=0)
    
    def str(self, indent = 0):
        """Create string representing the binary tree
        Can pass indent to make the tree depths easier to parse.
        """
        if self.__root is None:
            return f"BinarySearchTree({self.__root})"
        tree_str = self.__str_aux(self.__root, indent=indent, depth = 1)
        return "BinarySearchTree" + tree_str + ""



    def __str_aux(self, current: BinaryNode|None, indent, depth) -> str:
        prefix = "\n" + " "*indent * depth if indent > 0 else ""
        if current is None:
            return  prefix[:-indent] + str(None)
        return f"{prefix[:-indent]}({prefix}{current.key}, {prefix}{current.item}, {self.__str_aux(current._left, indent, depth+1)}, {self.__str_aux(current._right, indent, depth + 1)}{prefix[:-indent]})"

    # def str_2d(self):
    #     if self.__root is None:
    #         return str(None)
    #     buffer = self.__str_2d_aux(self.__root, LinkedList(), prefix='', postfix='')
    #     return '\n'.join(buffer)
    
    # def __str_2d_aux(self, current:BinaryNode|None, buffer:LinkedList, prefix='', postfix=''):
    #     if current is not None:
    #         real_prefix = prefix[:-2] + postfix
    #         buffer.append(f'{real_prefix}({current.key}, {current.item})')
    #         if current._left or current._right:
    #             self.__str_2d_aux(current._left, buffer, prefix=prefix + '\u2551 ', postfix='\u255f\u2550')
    #             self.__str_2d_aux(current._right, buffer, prefix=prefix + '  ', postfix='\u2559\u2550')
    #     else:
    #         real_prefix = prefix[:-2] + postfix
    #         buffer.append(f'{real_prefix}')
    #     return buffer

