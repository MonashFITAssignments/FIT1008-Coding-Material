from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.in_review.array_unordered_heap import ArrayUnorderedHeap, T
from typing import Literal, Iterable

HeapOrders = Literal['min', 'max']

class ArrayHeap(ArrayUnorderedHeap[T]):
    MAX_ORDERING = 0
    MIN_ORDERING = 1

    def __init__(self, max_items:int, ordering: HeapOrders):
        ArrayUnorderedHeap.__init__(self, max_items)

        if ordering == 'min':
            self._heap_order = ArrayHeap.MIN_ORDERING
        elif ordering == 'max':
            self._heap_order = ArrayHeap.MAX_ORDERING
        else:
            raise ValueError("Array heap received invalid heap ordering: " + ordering)
    
    def _should_rise(self, below:T, above:T) -> bool:
        if self._heap_order == ArrayHeap.MIN_ORDERING:
            return below < above
        else:
            return below > above 
        
    def _should_sink(self, above:T, below:T ) -> bool:
        if self._heap_order == ArrayHeap.MIN_ORDERING:
            return above > below
        else:
            return above < below
        
    @classmethod
    def heapify(cls, items: Iterable[T], ordering:HeapOrders, min_capacity:int = 1) -> ArrayHeap[T]:
        """ Construct a heap from an iterable of items. 
        returns: A heap containing all of the items in the iterable.
        complexity: O(n) where n is the number of items in the iterable.
        """
        return ArrayHeap(0, ordering)._heapify(items, min_capacity)
    
    def __str__(self):
        return "<ArrayHeap(" + ("min, " if self._heap_order == ArrayHeap.MIN_ORDERING else "max, ") + ArrayUnorderedHeap.__str__(self) + ')>'
