from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Tuple
from data_structures.node import BinaryNode
from data_structures.referential_array import ArrayR

K = TypeVar('K')
V = TypeVar('V')

class AbstractBinarySearchTree(ABC, Generic[K, V]):
    """
    Hash Table (Map/Dictionary) ADT.
    """
    @abstractmethod
    def is_leaf(self):
        pass

    @abstractmethod
    def items(self) -> ArrayR[Tuple[K, V]]:
        pass

    def keys(self) -> ArrayR[K]:
        array = self.items()
        for i in range(len(array)):
            array[i] = array[i][0]
        return array

    def values(self) -> ArrayR[V]:
        array = self.items()
        for i in range(len(array)):
            array[i] = array[i][1]
        return array

    @abstractmethod
    def is_empty(self) -> bool:
        return len(self) == 0

    @abstractmethod
    def __contains__(self, key: K) -> bool:
        pass

    @abstractmethod
    def __delitem__(self, key: K) -> None:
        pass

    @abstractmethod
    def __getitem__(self, key: K) -> V:
        pass

    @abstractmethod
    def __setitem__(self, key: K, data: V) -> None:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return str(self)
