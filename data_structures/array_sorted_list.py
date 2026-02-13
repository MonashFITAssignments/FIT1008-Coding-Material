from data_structures.referential_array import ArrayR
from data_structures.abstract_sorted_list import SortedList, T

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev'
__docformat__ = 'reStructuredText'

class ArraySortedList(SortedList[T]):
    """ Array-based implementation of the Abstract Sorted List. """

    def __init__(self, initial_capacity: int = 1) -> None:
        if initial_capacity < 0:
            raise ValueError("Capacity cannot be negative.")

        SortedList.__init__(self)
        self._array = ArrayR(initial_capacity)
        self._length = 0

    def add(self, item: T) -> None:
        """
        Add new element to the list.
        :complexity:
            Best case: O(log N) when the item is added at the end of the list.
            Worst case: O(N) when the item is added at the beginning of the list.
            N is the number of items in the list.
        """
        if self.is_full():
            self.__resize()
        index = self.__index_to_add(item)
        self.__shuffle_right(index)
        self._array[index] = item
        self._length += 1

    def delete_at_index(self, index: int) -> T:
        """
        Delete item at the given position.
        :complexity:
            Best case: O(1) when the item is at the end of the list.
            Worst case: O(N) when the item is at the beginning of the list. N is the
              number of items in the list.
        """
        item = self[index]
        index = self._absolute_index(index)
        self.__shuffle_left(index)
        self._length -= 1
        return item

    def index(self, item: T) -> int:
        """
        Find the position of a given item in the list,
        by means of calling the __index_to_add() method.
        :raises ValueError: if the item is not found.
        :complexity: See __index_to_add()
        """
        # Try finding the index
        index = self.__index_to_add(item)

        if index < len(self) and self._array[index] == item:
            return index

        raise ValueError(f"{item} not found")

    def is_full(self) -> bool:
        """ Check if the list of full. """
        return len(self) == len(self._array)

    def clear(self) -> None:
        """ Clear the list. """
        self._length = 0

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
        for i in range(index, len(self) - 1):
            self._array[i] = self._array[i + 1]

    def __resize(self) -> None:
        """ Resize the list.
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

    def __index_to_add(self, item: T) -> int:
        """
        Find the position where the new item should be placed.
        :complexity: 
            Best: O(Comp) happens when item is the middle element
            Worst: O(Log N * comp) happens when item is the first or the last element
            
            Comp - cost of comparision - can be assumed O(1) for simple types like numbers
            N - length of the list
        """

        low = 0
        high = len(self) - 1

        # until we have checked all elements in the search space
        while low <= high:
            mid = (low + high) // 2
            # Found the item
            if self[mid] == item:
                return mid
            # check right of the remaining list
            elif self[mid] < item:
                low = mid + 1
            # check left of the remaining list
            else:
                high = mid - 1

        return low

    def __len__(self) -> int:
        """ Return the length of the list. """
        return self._length

    def __getitem__(self, index: int) -> T:
        """ Return the element at the given position.
        :raises IndexError: if the index is out of bounds.
        :complexity: O(1)
        """
        index = self._absolute_index(index)
        if index < 0 or index >= len(self):
            raise IndexError('Out of bounds access in list.')
        return self._array[index]

    def __str__(self) -> str:
        """ Returns a string representation of the list. """
        return f'<ArraySortedList {SortedList.__str__(self)}>'
