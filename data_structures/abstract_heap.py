from __future__ import annotations
from typing import Generic, TypeVar, Literal, Iterable
from abc import abstractmethod, ABC

T = TypeVar('T')

class AbstractHeap(Generic[T], ABC):
    """
    Abstract class for min and max heaps
    """

    @abstractmethod
    def __init__(self, ordering: Literal['min', 'max']) -> None:
        pass
    
    
    def is_empty(self) -> bool:
        return len(self) == 0

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def add(self, item:T) -> None:
        pass

    @abstractmethod
    def extract_root(self) -> T:
        pass

    @abstractmethod
    def peek(self) -> T:
        pass

    @classmethod
    @abstractmethod
    def heapify(cls, items:Iterable[T]) -> AbstractHeap[T]:
        pass
