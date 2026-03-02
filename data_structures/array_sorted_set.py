from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.abstract_set import Set, T

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev and Sean Silva'
__docformat__ = 'reStructuredText'

class ArraySortedSet(Set[T]):
    """ Array-based sorted list implementation of the Abstract Set. """

    def __init__(self, initial_capacity: int = 1) -> None:
        if initial_capacity <= 0:
            raise ValueError("Capacity should be larger than 0.")

        Set.__init__(self)
        self._array = ArrayR(initial_capacity)
        self._length = 0

    def add(self, item: T) -> None:
        """ Add new element to the set. """
        index = self.__index_of_item(item)
        if self._array[index] == item:
            return
        
        if self.is_full():
            self.__resize()
        
        self.__shuffle_right(index)
        self._array[index] = item
        self._length += 1

    def remove(self, item: T) -> None:
        """
        Removes an item from the set
        :complexity best: O(logn) Item is at end of array
        :complexity worst: O(logn + n) Item is at front of array
            n - size of the set
        """
        index = self.__index_of_item(item)
        if not self._array[index] == item:
            raise KeyError(item)
        #shuffle left to remove the item. Swapping with the last item would break sorted order.
        self.__shuffle_left(index)
        self._length += -1

    def values(self) -> ArrayR[T]:
        """
        Returns elements of the set as an array.
        """
        res = ArrayR(len(self))
        for i in range(len(self)):
            res[i] = self._array[i]
        return res

    def clear(self):
        """ Clear the set.
        All we need to do is reset the size of the set to 0.
        This will start writing elements from the beginning of the array.
        """
        self._length = 0

    def is_full(self) -> bool:
        """ True if the set is full. """
        return len(self) == len(self._array)

    def is_empty(self) -> bool:
        """ True if the set is empty. """
        return len(self) == 0

    def __shuffle_right(self, index: int) -> None:
        """
        Shuffle items to the right up to a given position.
        """
        for i in range(len(self), index, -1):
            self._array[i] = self._array[i - 1]

    def __shuffle_left(self, index: int) -> None:
        """
        Shuffle items starting at the given position to the left.
        """
        for i in range(index, len(self)):
            self._array[i] = self._array[i + 1]

    def __resize(self) -> None:
        """ Resize the set.
        It only sizes up, so should only be called when adding new items.
        """
        if self.is_full():
            new_cap = int(2 * len(self._array)) + 1
            new_array = ArrayR(new_cap)
            for i in range(len(self)):
                new_array[i] = self._array[i]
            self._array = new_array
        assert len(self) < len(
            self._array
        ), "Capacity not greater than length after __resize."

    def __index_of_item(self, item: T) -> int:
        """
        Find the position where the new item should be placed.
        :complexity best: O(1)   item is the middle element
        :complexity worst: O(logn)  first or last element
            n - size of the set
        """

        low = 0
        high = len(self) - 1

        # until we have checked all elements in the search space
        while low <= high:
            mid = (low + high) // 2
            # Found the item
            if self._array[mid] == item:
                return mid
            # check right of the remaining list
            elif self._array[mid] < item:
                low = mid + 1
            # check left of the remaining list
            else:
                high = mid - 1

        return low
    
    def union(self, other: ArraySortedSet[T]) -> ArraySortedSet[T]:
        """
        Return the union of two sets, returns a set with every item in either self or other set.
        :complexity: O(n + m)
            n - size of self
            m - size of other
        """
        #Check that the other set is sorted
        if not isinstance(other, ArraySortedSet):
            # Alternatively get other.values() and sort them
            raise ValueError(f"Union not supported between {type(self).__name__} and {type(other).__name__}")
        else:
            other_values = other._array
            other_length = len(other)

        res = ArraySortedSet(len(self) + other_length)
        # merge the two arrays discarding duplicates
        i = 0
        j = 0
        while i < len(self) and j < other_length:
            i_value = self._array[i]
            j_value = other_values[j]
            if i_value < j_value:
                res._array[res._length] = i_value
                res._length += 1
                i += 1
            elif j_value < i_value:
                res._array[res._length] = j_value
                res._length += 1
                j += 1
            elif i_value == j_value:
                res._array[res._length] = i_value
                res._length += 1
                i += 1
                j += 1
            else:
                raise ValueError(f"Comparison operator poorly implemented {i_value} and {j_value} cannot be compared.")

        while i < len(self):
            res._array[res._length] = self._array[i]
            res._length += 1
            i += 1
        while j < other_length:
            res._array[res._length] = other_values[j]
            res._length += 1
            j += 1

        return res

    def intersection(self, other:Set[T]) -> ArraySortedSet[T]:
        """
        Return the intersection of two sets, returns a set with every item in both self and other set.
        :complexity best : O(k) When the largest element in the smaller set is smaller than kth element in the larger set 
        :complexity worst: O(n + m)
            k - min(n, m), the size of the smaller set.
            n - size of self
            m - size of other
        """
        #Check that the other set is sorted
        if not isinstance(other, ArraySortedSet):
            # Alternatively get other.values() and sort them
            raise ValueError(f"Intersection not supported between {type(self).__name__} and {type(other).__name__}")
        else:
            other_values = other._array
            other_length = len(other)

        res = ArraySortedSet(min(len(self), other_length))

        i = 0
        j = 0
        while i < len(self) and j < other_length:
            i_value = self._array[i]
            j_value = other_values[j]
            if i_value < j_value:
                i += 1
            elif j_value < i_value:
                j += 1
            elif i_value == j_value:
                res._array[res._length] = i_value
                res._length += 1
                i += 1
                j += 1
            else:
                raise ValueError(f"Comparison operator poorly implemented {i_value} and {j_value} cannot be compared.")
        
        return res

    def difference(self, other: Set[T]) -> ArraySortedSet[T]:
        """
        Return the difference of two sets, returns a set with every item not in the other set.
        :complexity best : O(n) When all items in self are smaller than the smallest item in other.
        :complexity worst: O(n + m)
            n - size of self
            m - size of other
        """
        #Check that the other set is sorted
        if not isinstance(other, ArraySortedSet):
            # Alternatively get other.values() and sort them
            raise ValueError(f"Difference not supported between {type(self).__name__} and {type(other).__name__}")
        else:
            other_values = other._array
            other_length = len(other)
        res = ArraySortedSet(len(self))
        
        i = 0
        j = 0
        while i < len(self) and j < other_length:
            i_value = self._array[i]
            j_value = other_values[j]
            if i_value < j_value:
                res._array[res._length] = i_value
                res._length += 1
                i += 1
            elif j_value < i_value:
                j += 1
            elif i_value == j_value:
                i += 1
                j += 1
            else:
                raise ValueError(f"Comparison operator poorly implemented {i_value} and {j_value} cannot be compared.")

        while i < len(self):
            res._array[res._length] = self._array[i]
            res._length += 1
            i += 1

        return res

    def __contains__(self, item):
        """ Checks if the item is in the list.
        :returns: True if the item is in the list, False otherwise.
        """
        index = self.__index_of_item(item)
        return item == self._array[index]

    def __len__(self):
        return self._length

    def __str__(self):
        """ Returns a string representation of the set. """
        return f'<ArraySortedSet {Set.__str__(self)}>'
