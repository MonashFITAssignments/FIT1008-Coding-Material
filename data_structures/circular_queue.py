from data_structures.abstract_queue import Queue, T
from data_structures.referential_array import ArrayR


class CircularQueue(Queue[T]):
    """ Circular implementation of a queue with arrays.

    Attributes:
         __length (int): number of elements in the stack (inherited)
         __front (int): index of the element at the front of the queue
         __rear (int): index of the first empty space at the back of the queue
         __array (ArrayR[T]): array storing the elements of the queue
    """

    def __init__(self, max_capacity: int) -> None:
        """
        Constructor for the CircularQueue class.
        :param max_capacity: maximum capacity of the queue
        :complexity: O(max_capacity) due to the creation of the array
        """
        if max_capacity <= 0:
            raise ValueError("Capacity should be larger than 0.")

        self._front = 0
        self._rear = 0
        self._array = ArrayR(max_capacity)
        self._length = 0

    def append(self, item: T) -> None:
        """ Adds an element to the rear of the queue.
        :raises Exception: if the queue is full
        :complexity: O(1)
        """
        if self.is_full():
            raise Exception("Queue is full")

        self._array[self._rear] = item
        self._length += 1
        self._rear = (self._rear + 1) % len(self._array)

    def serve(self) -> T:
        """ Deletes and returns the element at the queue's front.
        :raises Exception: if the queue is empty
        :complexity: O(1)
        """
        if self.is_empty():
            raise Exception("Queue is empty")

        self._length -= 1
        item = self._array[self._front]
        self._front = (self._front + 1) % len(self._array)
        return item

    def peek(self) -> T:
        """ Returns the element at the queue's front.
        :raises Exception: if the queue is empty
        :complexity: O(1)
        """
        if self.is_empty():
            raise Exception("Queue is empty")

        return self._array[self._front]

    def is_full(self) -> bool:
        """ True if the queue is full and no element can be appended. """
        return len(self) == len(self._array)

    def clear(self) -> None:
        """ Clears all elements from the queue. """
        Queue.__init__(self)
        self._front = 0
        self._rear = 0
        self._length = 0

    def __len__(self) -> int:
        """ Returns the number of elements in the queue. """
        return self._length

    def __str__(self) -> str:
        """ Returns the string representation of the queue """
        return '<CircularQueue [' + ', '.join(
            str(self._array[(i + self._front) % len(self._array)]) for i in range(len(self))
        ) + ']>'
