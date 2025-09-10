from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Tuple
from data_structures.dunder_protected import DunderProtected
from data_structures.referential_array import ArrayR


K = TypeVar('K')
V = TypeVar('V')


class HashTable(ABC, Generic[K, V], DunderProtected):
    """
    Hash Table (Map/Dictionary) ADT. 
    """

    def insert(self, key: str, data: V) -> None:
        """
        Utility method to call our setitem method
        """
        self[key] = data

    @abstractmethod
    def hash(self, key: K) -> int:
        pass

    @property
    @abstractmethod
    def table_size(self) -> int:
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

    def is_empty(self) -> bool:
        return len(self) == 0

    @abstractmethod
    def is_full(self) -> bool:
        pass

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

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
