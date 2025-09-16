from data_structures.abstract_stack import Stack
from data_structures.referential_array import ArrayR, T


class ArrayStack(Stack[T]):
    """ Implementation of a stack with arrays.

    Attributes:
         length (int): number of elements in the stack (inherited)
         array (ArrayR[T]): array storing the elements of the queue
    """

    def __init__(self, max_capacity: int = 1) -> None:
        """
        Constructor for the ArrayStack class.
        :param max_capacity: maximum capacity of the stack
        :complexity: O(max_capacity) due to the creation of the array
        """
        if max_capacity <= 0:
            raise ValueError("Capacity should be larger than 0.")

        self._array = ArrayR(max_capacity)
        self._length = 0

    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack.
        :raises Exception: if the stack is full
        :complexity: O(1)
        """
        if self.is_full():
            raise Exception("Stack is full")
        self._array[len(self)] = item
        self._length += 1

    def pop(self) -> T:
        """ Pops the element at the top of the stack.
        :raises Exception: if the stack is empty
        :complexity: O(1)
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        self._length -= 1
        return self._array[self._length]

    def peek(self) -> T:
        """ Returns the element at the top, without popping it from stack.
        :raises Exception: if the stack is empty
        :complexity: O(1)
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        return self._array[self._length-1]

    def is_full(self) -> bool:
        """ True if the stack is full and no element can be pushed. """
        return len(self) == len(self._array)

    def clear(self):
        self._length = 0

    def __len__(self) -> int:
        """ Returns the number of items in the stack"""
        return self._length

    def __str__(self) -> str:
        """ Returns the string representation of the stack """
        return '<ArrayStack [' + ', '.join(
            str(self._array[i]) for i in range(len(self))
        ) + ']>'
