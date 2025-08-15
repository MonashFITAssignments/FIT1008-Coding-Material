from __future__ import annotations
from data_structures.unordered_array_heap import UnorderedArrayHeap, T
from typing import Iterable

class MinArrayHeap(UnorderedArrayHeap[T]):
    def _should_rise(self, below:T, above:T) -> bool:
        """ :complexity: O(1) """
        return below < above

    def _should_sink(self, above:T, below:T ) -> bool:
        """ :complexity: O(1) """
        return above > below
    
    def extract_min(self) -> T:
        """ Alias for extract_root, specific for min heaps. """
        return self.extract_root()
    
    @classmethod
    def heapify(cls, items: Iterable[T]) -> MinArrayHeap[T]:
        """ Construct a heap from an iterable of items. 
        returns: A heap containing all items in the iterable.
        complexity: O(n) where n is the number of items in the iterable.
        """
        return MinArrayHeap(0)._heapify(items)
    
    def __str__(self):
        return '<MinArrayHeap(' + UnorderedArrayHeap.__str__(self) + ')>'
