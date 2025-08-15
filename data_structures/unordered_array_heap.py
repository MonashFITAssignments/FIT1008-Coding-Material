from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.abstract_heap import AbstractHeap, T
from typing import Literal, Iterable
from abc import abstractmethod

HeapOrders = Literal['min', 'max']

class UnorderedArrayHeap(AbstractHeap[T]):
    def __init__(self, max_items:int = 1):
        if not max_items >= 0:
            raise ValueError("Heap must store 0 or more items.")
        self.__array = ArrayR[T](max_items + 1)
        self.__length:int = 0

    def add(self, item: T) -> None:
        """ Add an item to the heap.
        :raises ValueError: if the heap's array is full
        :complexity best: O(1) the item is adding to the end of the array (no rising required)
        :complexity worst: O(logN) Need to rise the item to the top of the heap (N is the size of the heap)
        """
        if len(self) == len(self.__array) - 1:
            raise ValueError("Cannot add to full heap.")

        self.__length += 1
        self.__array[len(self)] = item
        self._rise(len(self))

    def extract_root(self) -> T:
        """ Get and remove the root of the heap.
        :raises: ValueError if the heap is empty
        :returns: The root of the heap
        :complexity: O(logN) where N is the size of the heap.
        Note: Technically there is a best case of O(1) if the items are all the same.
        """
        if self.__length == 0:
            raise ValueError("Cannot extract_root from empty heap.")
        res = self.__array[1]
        self.__array[1] = self.__array[len(self)]
        self.__length -= 1
        self._sink(1)
        return res

    def peek(self) -> T:
        """ Returns the root of the heap without updating the heap. 
        :raises: ValueError if the heap is empty.
        :returns: The root of the heap
        :complexity: O(1)
        """
        if self.__length == 0:
            raise ValueError("Cannot peek from empty heap.")
        return self.__array[1]
    
    @abstractmethod
    def _should_rise(self, below:T, above:T) -> bool:
        """ Returns if the below element should rise up. 
        Depends on the ordering of the heap.
        """
        pass
        
    @abstractmethod
    def _should_sink(self, above:T, below:T ) -> bool:
        """ Returns if the above element should sink down. 
        Depends on the ordering of the heap.
        """
        pass
        
    def __get_child_index(self, k:int) -> int | None:
        """ Returns the index of child of k that would be the parent of the other.
        :returns: None if no child exists, else index of child
        :complexity: O(1)
        """
        k2 = k * 2
        if k2 > len(self):
            return None
        elif k2 == len(self):
            return k2
        else:
            left = self.__array[k2]
            right = self.__array[k2 + 1]

            if self._should_sink(left, right):
                #if left is put on top it is unstable, so right should be put on top
                return k2 + 1
            return k2

    def __get_parent_index(self, k:int) -> int | None:
        """ Returns the index of the parent of k
        :returns: None if k is the root, else index of k's parent
        :complexity: O(1)
        """
        if k == 1:
            return None
        return k // 2

    def _rise(self, k:int) -> None:
        """ Rise the element at index k
        N represents the size of the heap
        :complexity best: O(1) when no rising is required
        :complexity worst: O(logN) where you need to rize to the top of the heap.
        """
        rising_item = self.__array[k]
        
        # := is the walrus operator, it assigns the right expression to the left variable, and returns the expression.
        # This gets the parent_i and checks if parent_i is not None in the condition
        while (parent_i := self.__get_parent_index(k)) is not None and self._should_rise(rising_item, self.__array[parent_i]):
            self.__array[k] = self.__array[parent_i]
            k = parent_i
            
        self.__array[k] = rising_item

    def _sink(self, k:int) -> None:
        """ Sink the element at index k
        :complexity best: O(1) when no sinking is required
        :complexity worst: O(logN) where you need to sink to the bottom of the heap.
        """
        sinking_item = self.__array[k]
        while (child_i := self.__get_child_index(k)) is not None and self._should_sink(sinking_item, self.__array[child_i]):
            self.__array[k] = self.__array[child_i]
            k = child_i

        self.__array[k] = sinking_item

    def _heapify(heap: UnorderedArrayHeap[T], items: Iterable[T]) -> UnorderedArrayHeap[T]:
        """ Construct a heap from an iterable of items. 
        :returns: A heap containing items in the iterable.
        :complexity: O(n) where n is the number of items in the iterable.
        """
        try: #call len(iterable) to avoid having to resize a temporary array
            length = len(items)
            array = ArrayR(length + 1)
            for i, item in enumerate(items):
                array[i + 1] = item
            

        except TypeError: #iterable doesn't have len(), iterate until exhaustion and resize as necessary.
            def resize(array):
                new_array = ArrayR(len(array) * 2)
                for i in range(len(array)):
                    new_array[i] = array[i]
                return new_array
            
            array = ArrayR(2)
            i = -1
            for i, item in enumerate(items):
                if i + 1 >= len(array):
                    array = resize(array)
                array[i + 1] = item
            
            length = i + 1
        
        heap.__array = array
        heap.__length = length

        for i in range(len(heap) // 2, 0, -1):
            heap._sink(i)
        
        return heap

    def __len__(self) -> int:
        return self.__length

    def __str__(self) -> str:
        """
        :complexity: O(n) where n is the number of items in the heap.
        """
        res = ArrayR(self.__length)
        for i in range(self.__length):
            res[i] = str(self.__array[i + 1])
        
        return '[' + ', '.join(res) + ']'
