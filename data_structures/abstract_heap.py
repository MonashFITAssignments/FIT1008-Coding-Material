from __future__ import annotations
from typing import Generic, TypeVar, Literal, Iterable
from abc import abstractmethod, ABC
from data_structures.referential_array import ArrayR

T = TypeVar('T')

class AbstractHeap(Generic[T], ABC):
    """
    Abstract class for min and max heaps
    """

    @abstractmethod
    def __init__(self) -> None:
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

    def is_empty(self) -> bool:
        return len(self) == 0

    @classmethod
    @abstractmethod
    def heapify(cls, items: Iterable[T]) -> AbstractHeap[T]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return str(self)

    @abstractmethod
    def values(self) -> ArrayR[T]:
        pass