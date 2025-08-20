from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.abstract_set import Set, T
from algorithms.mergesort import mergesort

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev and Sean Silva'
__docformat__ = 'reStructuredText'


class ArraySortedSet(Set[T]):
    """ Array-based sorted list implementation of the Abstract Set. """

    def __init__(self, initial_capacity: int = 1) -> None:
        if initial_capacity <= 0:
            raise ValueError("Capacity should be larger than 0.")

        self.__array = ArrayR(initial_capacity)
        self.__length = 0

    def add(self, item: T) -> None:
        """ Add new element to the set. """
        index = self.__index_of_item(item)
        if self.__array[index] == item:
            return
        
        if self.is_full():
            self.__resize()
        
        self.__shuffle_right(index)
        self.__array[index] = item
        self.__length += 1

    def remove(self, item: T) -> None:
        """
        Removes an item from the set
        :complexity best: O(logn * comp) Item is at end of array
        :complexity worst: O(logn * comp + n) Item is at front of array
            comp - cost of comparision
            n - size of the set
        """
        index = self.__index_of_item(item)
        if not self.__array[index] == item:
            raise KeyError(item)
        #shuffle left to remove the item. Swapping with the last item would break sorted order.
        self.__shuffle_left(index)
        self.__length += -1

    def values(self) -> ArrayR[T]:
        """
        Returns elements of the set as an array.
        """
        res = ArrayR(len(self))
        for i in range(len(self)):
            res[i] = self.__array[i]
        return res

    def clear(self):
        """ Clear the set.
        All we need to do is reset the size of the set to 0.
        This will start writing elements from the beginning of the array.
        """
        self.__length = 0

    def is_full(self) -> bool:
        """ True if the set is full. """
        return len(self) == len(self.__array)

    def is_empty(self) -> bool:
        """ True if the set is empty. """
        return len(self) == 0

    def __shuffle_right(self, index: int) -> None:
        """
        Shuffle items to the right up to a given position.
        """
        for i in range(len(self), index, -1):
            self.__array[i] = self.__array[i - 1]

    def __shuffle_left(self, index: int) -> None:
        """
        Shuffle items starting at the given position to the left.
        """
        for i in range(index, len(self)):
            self.__array[i] = self.__array[i + 1]

    def __resize(self) -> None:
        """ Resize the set.
        It only sizes up, so should only be called when adding new items.
        """
        if self.is_full():
            new_cap = int(2 * len(self.__array)) + 1
            new_array = ArrayR(new_cap)
            for i in range(len(self)):
                new_array[i] = self.__array[i]
            self.__array = new_array
        assert len(self) < len(
            self.__array
        ), "Capacity not greater than length after __resize."

    def __index_of_item(self, item: T) -> int:
        """
        Find the position where the new item should be placed.
        :complexity best: O(comp)   item is the middle element
        :complexity worst: O(logn * comp)  first or last element
            comp - cost of comparision
            n - size of the set
        """

        low = 0
        high = len(self) - 1

        # until we have checked all elements in the search space
        while low <= high:
            mid = (low + high) // 2
            # Found the item
            if self.__array[mid] == item:
                return mid
            # check right of the remaining list
            elif self.__array[mid] < item:
                low = mid + 1
            # check left of the remaining list
            else:
                high = mid - 1

        return low
    
    def union(self, other: Set[T]) -> ArraySortedSet[T]:
        """
        Return the union of two sets, returns a set with every item in either self or other set.
        :complexity: O((n + mlogm) * comp)
            n - size of self
            m - size of other
            comp - cost of comparison
        """
        res = ArraySortedSet(len(self) + len(other))
        other_values = other.values()
        sorted_values = mergesort(other_values)

        # merge the two arrays discarding duplicates
        i = 0
        j = 0
        while i < len(self) and j < len(sorted_values):
            i_value = self.__array[i]
            j_value = sorted_values[j]
            if i_value < j_value:
                res.__array[res.__length] = i_value
                res.__length += 1
                i += 1
            elif j_value < i_value:
                res.__array[res.__length] = sorted_values[j]
                res.__length += 1
                j += 1
            elif i_value == j_value:
                res.__array[res.__length] = i_value
                res.__length += 1
                i += 1
                j += 1
            else:
                raise ValueError(f"Comparison operator poorly implemented {i_value} and {j_value} cannot be compared.")

        if i < len(self):
            for k in range(i, len(self)):
                res.__array[res.__length] = self.__array[k]
                res.__length += 1
        if j < len(sorted_values):
            for k in range(j, len(sorted_values)):
                res.__array[res.__length] = sorted_values[k]
                res.__length += 1

        return res

    def intersection(self, other:Set[T]) -> ArraySortedSet[T]:
        """
        Return the intersection of two sets, returns a set with every item in both self and other set.
        :complexity: O(n * contains)
            n - size of self
            contains - complexity of in of other set
        """
        res = ArraySortedSet(min(len(self), len(other)))
        for i in range(len(self)):
            item = self.__array[i]
            if item in other:
                res.__array[res.__length] = item
                res.__length += 1
        
        return res

    def difference(self, other: Set[T]) -> ArraySortedSet[T]:
        """
        Return the difference of two sets, returns a set with every item not in the other set.
        :complexity: O(n * contains)
            n - size of self
            contains - complexity of in of other set
        """
        res = ArraySortedSet(len(self))
        for i in range(len(self)):
            item = self.__array[i]
            if item not in other:
                res.__array[res.__length] = item
                res.__length += 1

        return res

    def __contains__(self, item):
        """ Checks if the item is in the list.
        :returns: True if the item is in the list, False otherwise.
        """
        index = self.__index_of_item(item)
        return item == self.__array[index]

    def __len__(self):
        return self.__length

    def __str__(self):
        """ Returns a string representation of the set. """
        return f'<ArraySortedSet {Set.__str__(self)}>'
