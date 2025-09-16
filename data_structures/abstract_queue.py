from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from data_structures.sunder_protected import ProtectAttributes

T = TypeVar('T')


class Queue(ABC, Generic[T], ProtectAttributes):
    """ Queue ADT
    Defines a generic abstract queue with the usual methods.
    """

    @abstractmethod
    def append(self, item: T) -> None:
        """ Adds an element to the rear of the queue."""
        pass

    @abstractmethod
    def serve(self) -> T:
        """ Deletes and returns the element at the queue's front."""
        pass

    @abstractmethod
    def peek(self) -> T:
        """ Returns the element at the queue's front. """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """ Returns the number of elements in the queue."""
        pass

    def is_empty(self) -> bool:
        """ True if the queue is empty. """
        return len(self) == 0

    @abstractmethod
    def clear(self) -> None:
        """ Clears all elements from the queue. """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """ Returns the string representation of the queue """
        pass

    def __repr__(self) -> str:
        return str(self)
