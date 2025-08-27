from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Tuple, List
from data_structures.referential_array import ArrayR
from data_structures.dunder_protected import DunderProtected

K = TypeVar('K')
V = TypeVar('V')


class HashTable(ABC, Generic[K, V], DunderProtected):
    """
    Hash Table (Map/Dictionary) ADT. 
    """

    __TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    def __init__(self, sizes: None | List[int] = None, hash_base: int | None = 31) -> None:
        """
        :param sizes: Optional list of sizes to use for the hash table.
                      If not provided, a default list of sizes will be used.
        :complexity: O(1) - Assuming the default sizes are used, we can assume the array is created in O(1) time.
            If you use this function in any way that passes some variable input for the sizes, then the complexity
            needs to change accordingly.
        """
        if sizes is not None:
            self.__TABLE_SIZES = sizes

        self.__size_index = 0
        self.__array: ArrayR[tuple[str, V]] = ArrayR(self.__TABLE_SIZES[self.__size_index])
        self.__length = 0
        self.__hash_base = hash_base

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
