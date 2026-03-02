from __future__ import annotations
from data_structures.abstract_heap import AbstractHeap, T
from data_structures.referential_array import ArrayR
from typing import Iterable, Union
from data_structures.node_binary import BinaryNode
from typing import Iterable, Union, Tuple

MaybeNode = Union[BinaryNode[int, T], None]

class MinLinkedHeap(AbstractHeap[T]):
    """ Implementation of Leftist Tree based heap
    Each node has the shorter path to a leaf in their right child.
    When adding or removing items, the path to the highest leaf is always followed.
    This guarantess log(n) complexity as the deepest the highest leaf can be is log2(n),
        when the binary tree is complete.
    """
    def __init__(self):
        self._root: MaybeNode = None

    def add(self, item:T) -> None:
        """ Add item to the heap
        :comp best : O(1) when item is valid root
        :comp worst: O(log(n)) where n is len(self)
        """
        new_node = BinaryNode(item, 1, 1)
        self._root = self.__merge(self._root, new_node)

    def extract_root(self):
        if self._root:
            res = self._root._item
            self._root = self.__merge(self._root._left, self._root._right)
            return res
        raise ValueError("Cannot extract root from empty heap")

    def peek(self) -> T:
        if self._root:
            return self._root._item
        raise ValueError("Cannot peek from empty heap")

    def __merge(self, node1:MaybeNode, node2:MaybeNode) -> BinaryNode[int, T]:
        """ Merge two binary trees of a heap into a single tree.
        The shortest path to a leaf from any node is always stored in the right branch.
        The nodes track the path length (key) to the nearest leaf to facilitate the above property.

        :comp best : O(1) when both nodes are linked lists
        :comp worst: O(log(max(n,m))) 
            where n, m are the node1.size, node2.size
        
        At each call, we traverse down the right child of either node1 or node2, and we stop when the child is None.
        Thus merge is called at most (node1.key + node2.key - 1) times and at least min(node1.key, node2.key) times.
        If node.key == k, then that means that node must be a complete binary tree to depth k-1, thus has at least 2^(node.key - 1) nodes
        Therefore node.key is no larger than log2(node.size) + 1
        """        
        if node1 is None:
            return node2
        if node2 is None:
            return node1
        
        def key(n:MaybeNode):
            if n is None:
                return 0
            return n._key
        
        size = node1._size + node2._size

        if node1._item > node2._item: #This part determines the heap ordering, makes node1 a valid parent
            node1, node2 = node2, node1

        node1._right = self.__merge(node1._right, node2)

        if key(node1._right) > key(node1._left):
            node1._left, node1._right = node1._right, node1._left

        node2 = BinaryNode(node1._item, key(node1._right) + 1, size)
        node2._left = node1._left
        node2._right = node1._right

        return node2

    @classmethod
    def heapify(cls, items: Iterable[T]) -> MinLinkedHeap:
        """ Construct a heap from an iterable of items
        returns: A heap containing all items in the iterable.
        complexity: O(n) where n is the number of items in the iterable.

        With the stack, only similar sized merges occur. 
        This means 3/4 n merges of depth 1, n/8 merges of depth 2, n/16 merges of depth 3 etc.
        This is the same series for array based heapify.
        """
        res = cls()

        linked_stack = (None, None) #To reduce dependencies

        def size(node : MaybeNode) -> int:
            if node is None:
                return 0
            return node._size
        
        def merge(new_node: BinaryNode[int, T]):
            tail = linked_stack
            while tail and new_node._size >= size(tail[0]):
                head, tail = tail
                
                new_node = res.__merge(new_node, head)
                
            return (new_node, tail)
            

        for item in items:
            new_node = BinaryNode(item, 1, 1)
            linked_stack = merge(new_node)
        
        tree, linked_stack = linked_stack
        while linked_stack:
            head, linked_stack = linked_stack 
            tree = res.__merge(tree, head)
        
        res._root = tree
        return res
    
    def values(self):
        """
        Returns all the items in the heap in no particular order.
        :complexity: O(n) where n is the number of items in the heap.
        """
        res = ArrayR(len(self))
        def add(i:int, node:BinaryNode):
            if node is None:
                return i
            
            res[i] = node._item
            i = add(i + 1, node._left)
            return add(i + 1, node._right)
        add(0, self.__root)
        return res


    def __len__(self) -> int:
        if self._root:
            return self._root._size
        return 0

    def __str__(self) -> str:
        def get_elements(node: BinaryNode[int, T], elements: ArrayR[T], index: int) -> None:
            if node is not None:
                elements[index] = str(node._item)
                get_elements(node._left, elements, index * 2 + 1)
                get_elements(node._right, elements, index * 2 + 2)

        elements = ArrayR(len(self))
        get_elements(self._root, elements, 0)
        return "<MinLinkedHeap([" + ", ".join(elements) + "])>"
