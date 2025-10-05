
from typing import TypeVar

from data_structures.node import Node
from data_structures.abstract_queue import Queue

T = TypeVar("T")


class LinkedQueue(Queue[T]):
    """ Linked Queue
    The Queue ADT implemented using a linked structure.
    """

    def __init__(self) -> None:
        """
        Constructor for the LinkedQueue class.
        :complexity: O(1)
        """
        self.clear()

    def append(self, item: T) -> None:
        """ Adds an element to the rear of the queue.
        :raises Exception: if the queueu is full.
        :complexity: O(1)
        """
        # Case 1: Empty queue
        if self._front is None:
            self._front = Node(item)
            self._rear = self._front
            self._length += 1
            return

        # Case 2: Non Empty queue
        # Add to the rear
        new_node = Node(item)
        self._rear.link = new_node
        self._rear = new_node
        self._length += 1

    def serve(self) -> T:
        """ Deletes and returns the element at the queue's front.
        :raises Exception: if the queue is empty
        :complexity: O(1)
        """
        if self.is_empty():
            raise Exception("Queue is empty")

        # Case 1: Single element in the queue
        if self._front == self._rear:
            item = self._front.item
            self._front = None
            self._rear = None
            self._length -= 1
            return item

        # Case 2: Multiple elements in the queue
        item = self._front.item
        self._front = self._front.link
        self._length -= 1
        return item

    def peek(self) -> T:
        """ Returns the element at the queue's front without deleting it.
        :raises Exception: if the queue is empty
        """
        if self.is_empty():
            raise Exception("Queue is empty")
        return self._front.item

    def peek_node(self) -> Node:
        """ Returns the node at the queue's front without deleting it.
        :pre: queue is not empty
        :raises Exception: if the queue is empty
        """
        if self.is_empty():
            raise Exception("Queue is empty")
        return self._front

    def clear(self) -> None:
        """ Clears all elements from the queue. """
        self._front = None
        self._rear = None
        self._length = 0

    def __len__(self) -> int:
        """ Returns the number of elements in the queue. """
        return self._length

    def __str__(self) -> str:
        """ Returns a string representation of the queue."""
        i = self._front
        result = "<LinkedQueue ["
        while i is not None:
            result += str(i.item)
            if i.link is not None:
                result += ", "
            i = i.link
        return f"{result}]>"
