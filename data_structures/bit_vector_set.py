from __future__ import annotations
from data_structures.abstract_set import Set
from data_structures.referential_array import ArrayR

class BitVectorSet(Set[int]):
    """
    A bit-vector implementation of the set ADT. The set is represented
    as an integer. The element is present in the set if and only if the
    corresponding bit of the integer is 1.
    """

    def __init__(self):
        Set.__init__(self)
        self._elems = 0

    def add(self, item: int) -> None:
        """
        Adds an element to the set.
        :raises TypeError: if the item is not a positive integer.
        """
        if not isinstance(item, int) or item <= 0:
            raise TypeError('Set elements should be positive integers.')
        self._elems |= 1 << (item - 1)

    def remove(self, item: int) -> None:
        """
        Removes an element from the set.
        :raises TypeError: if the item is not a positive integer.
        :raises KeyError: if the item is not in the set.
        """
        if not isinstance(item, int) or item <= 0:
            raise TypeError('Set elements should be positive integers.')
        if item in self:
            self._elems ^= 1 << (item - 1)
        else:
            raise KeyError(item)

    def values(self) -> ArrayR[int]:
        """
        Returns the elements of the set as an array.
        """
        res = ArrayR(len(self))
        count = 0
        for item in range(1, int.bit_length(self._elems) + 1):
            if item in self:
                res[count] = item
                count += 1
        return res

    def clear(self) -> None:
        """ Makes the set empty. """
        self._elems = 0

    def is_empty(self) -> bool:
        """ True if the set is empty. """
        return self._elems == 0

    def union(self, other: BitVectorSet[int]) -> BitVectorSet[int]:
        """
        Creates the union of the set with another one.
        The result set should contain all elements in self and other.
        """
        res = BitVectorSet()
        res._elems = self._elems | other._elems
        return res

    def intersection(self, other: BitVectorSet[int]) -> BitVectorSet[int]:
        """
        Creates the intersection of the set with another one.
        The result set should contain the elements that are both in
        self and other.
        """
        res = BitVectorSet()
        res._elems = self._elems & other._elems
        return res

    def difference(self, other: BitVectorSet[int]) -> BitVectorSet[int]:
        """
        Creates the difference of the set with another one.
        The result set should contain the elements that are in self
        but not in other. I.e. self - other.
        """
        res = BitVectorSet()
        res._elems = self._elems & ~other._elems
        return res

    def __contains__(self, item: int) -> bool:
        """
        True if the set contains the item. False otherwise.
        :raises TypeError: if the item is not a positive integer.
        """
        if not isinstance(item, int) or item <= 0:
            raise TypeError('Set elements should be positive integers.')
        return (self._elems >> (item - 1)) & 1 == 1

    def __len__(self) -> int:
        """
        Size computation. The most expensive operation.
        Use int.bit_length(your_integer) to calculate the bit length.
        """
        res = 0
        for item in range(1, int.bit_length(self._elems) + 1):
            if item in self:
                res += 1
        return res

    def __str__(self):
        """ Returns a string representation of the set. """
        return f'<BitVectorSet {Set.__str__(self)}>'
