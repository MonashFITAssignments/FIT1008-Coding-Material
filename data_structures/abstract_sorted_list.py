from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from data_structures.sunder_protected import ProtectAttributes

T = TypeVar('T')
K = TypeVar('K')


class SortedList(ABC, Generic[T], ProtectAttributes):
    """ Sorted List ADT.
    Defines a generic abstract sorted list with the standard methods.
    Items to store should be of time ListItem.
    """
    @abstractmethod
    def add(self, item: T) -> None:
        """ Add new element to the list. """
        pass

    @abstractmethod
    def delete_at_index(self, index: int) -> T:
        """ Delete item at a given position. """
        pass

    def remove(self, item: T) -> None:
        """ Remove an item from the list. """
        index = self.index(item)
        self.delete_at_index(index)

    @abstractmethod
    def index(self, item: T) -> int:
        """ Find the position of a given item in the list. """
        pass

    def is_empty(self) -> bool:
        """ Check if the list of empty. """
        return len(self) == 0

    @abstractmethod
    def clear(self) -> None:
        """ Clear the list. """
        pass

    @abstractmethod
    def __getitem__(self, index: int) -> T:
        """ Return the element at a given position. """
        pass

    def __contains__(self, item):
        """ Checks if the item is in the list. """
        try:
            _ = self.index(item)
            return True
        except ValueError:
            return False

    def __len__(self) -> int:
        """ Return the length of the list. """
        return self.__length

    def __str__(self) -> str:
        """ Returns a string representation of the list. """
        strings = (str(item) for item in self)

        return '[' + ', '.join(strings) + ']'

    def __repr__(self) -> str:
        return str(self)
