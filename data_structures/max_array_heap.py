from __future__ import annotations
from data_structures.unordered_array_heap import UnorderedArrayHeap, T
from typing import Iterable

class MaxArrayHeap(UnorderedArrayHeap[T]):
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
    def heapify(cls, items: Iterable[T]) -> MaxArrayHeap[T]:
        """ Construct a heap from an iterable of items. 
        returns: A heap containing all items in the iterable.
        complexity: O(n) where n is the number of items in the iterable.
        """
        return MaxArrayHeap(0)._heapify(items)

    def __str__(self):
        return '<MaxArrayHeap(' + UnorderedArrayHeap.__str__(self) + ')>'
