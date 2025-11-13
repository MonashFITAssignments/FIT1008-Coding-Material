from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.abstract_heap import AbstractHeap, T
from typing import Iterable

class ArrayMaxHeap(AbstractHeap[T]):
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
        if self.is_full():
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
        But in a heap of distinct elements extract_root always takes O(logN) time, 
            otherwise heapsort would be a comparison based O(N) sorting algorithm, which is impossible.
        """
        if self.__length == 0:
            raise ValueError("Cannot extract_root from empty heap.")
        res = self.__array[1]
        self.__array[1] = self.__array[len(self)]
        self.__length -= 1
        self._sink(1)
        return res
  
    def extract_max(self) -> T:
        """ Alias for extract_root, specific for max heaps. """
        return self.extract_root()

    def peek(self) -> T:
        """ Returns the root of the heap without updating the heap. 
        :raises: ValueError if the heap is empty.
        :returns: The root of the heap
        :complexity: O(1)
        """
        if self.__length == 0:
            raise ValueError("Cannot peek from empty heap.")
        return self.__array[1]

    def is_full(self) -> bool:
        return len(self) == len(self.__array) - 1
        
    def __get_child_index(self, k:int) -> int | None:
        """ Returns the index of child of k that would be the parent of the other (the larger child).
        :complexity: O(1)
        """
        k2 = k * 2
        if k2 == len(self) or self.__array[k2] > self.__array[k2 + 1]:
            return k2
        else:
            return k2 + 1

    def _rise(self, k:int) -> None:
        """ Rise the element at index k
        :complexity best: O(1) when no rising is required
        :complexity worst: O(logN) when you need to rise to the top of the heap.
            Where N is the size of the heap.
        """
        rising_item = self.__array[k]
        
        while k > 1 and rising_item > self.__array[k // 2]:
            self.__array[k] = self.__array[k // 2]
            k = k //2
            
        self.__array[k] = rising_item

    def _sink(self, k:int) -> None:
        """ Sink the element at index k
        :complexity best: O(1) when no sinking is required
        :complexity worst: O(logN) when you need to sink to the bottom of the heap.
            Where N is the size of the heap.
        """
        sinking_item = self.__array[k]
        while 2 * k <= len(self):
            child_i = self.__get_child_index(k)
            if sinking_item >= self.__array[child_i]:
                break
            self.__array[k] = self.__array[child_i]
            k = child_i

        self.__array[k] = sinking_item

    @classmethod
    def heapify(cls, items: Iterable[T], min_capacity: int = 1) -> ArrayMaxHeap[T]:
        """ Construct a heap from an iterable of items. 
        :param min_capacity: Specifies the minimum capacity of the returned heap.
            If the iterable has more items than `min_capacity` the heap's capacity will grow to fit the items in the iterable.
        :returns: A heap containing items in the iterable.
        :complexity: O(n) where n is the number of items in the iterable.
        """
        try: #call len(iterable) to avoid having to resize a temporary array
            length = len(items)
            array = ArrayR(max(min_capacity, length) + 1)
            for i, item in enumerate(items):
                array[i + 1] = item
            

        except TypeError: #iterable doesn't have len(), iterate until exhaustion and resize as necessary.
            def resize(array):
                new_array = ArrayR(len(array) * 2)
                for i in range(len(array)):
                    new_array[i] = array[i]
                return new_array

            array = ArrayR(max(min_capacity + 1, 1))
            i = -1
            for i, item in enumerate(items):
                if i + 1 >= len(array):
                    array = resize(array)
                array[i + 1] = item
            
            length = i + 1
        
        heap = ArrayMaxHeap(length)
        heap.__array = array
        heap.__length = length

        for i in range(len(heap) // 2, 0, -1):
            heap._sink(i)
        
        return heap
    
    def values(self):
        """
        Returns all the items in the heap in no particular order.
        :complexity: O(n) where n is the number of items in the heap.
        """
        res = ArrayR(len(self))
        for i in range(len(self)):
            res[i] = self.__array[i + 1]
        return res

    def __len__(self) -> int:
        return self.__length

    def __str__(self) -> str:
        """
        :complexity: O(n) where n is the number of items in the heap.
        """
        res = ArrayR(self.__length)
        for i in range(self.__length):
            res[i] = str(self.__array[i + 1])
        
        return '<ArrayMaxHeap([' + ', '.join(res) + '])>'
