from __future__ import annotations
from data_structures.in_review.array_unordered_heap import ArrayUnorderedHeap, T
from typing import Iterable

class ArrayMaxHeap(ArrayUnorderedHeap[T]):
    def _should_rise(self, below:T, above:T) -> bool:
        """ :complexity: O(1) """
        return below > above

    def _should_sink(self, above:T, below:T ) -> bool:
        """ :complexity: O(1) """
        return above < below
    
    def extract_max(self) -> T:
        """ Alias for extract_root, specific for max heaps. """
        return self.extract_root()
    
    @classmethod
    def heapify(cls, items: Iterable[T]) -> ArrayMaxHeap[T]:
        """ Construct a heap from an iterable of items. 
        returns: A heap containing all items in the iterable.
        complexity: O(n) where n is the number of items in the iterable.
        """
        return ArrayMaxHeap(0)._heapify(items)

    def __str__(self):
        return '<ArrayMaxHeap(' + ArrayUnorderedHeap.__str__(self) + ')>'
