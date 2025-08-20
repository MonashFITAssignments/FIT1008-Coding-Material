from data_structures.node import Node
from data_structures.abstract_stack import Stack, T


class LinkedStack(Stack[T]):
    """ Implementation of a stack with linked nodes. """

    def __init__(self, _=None) -> None:
        self.__top = None
        self.__length = 0

    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack.
        :complexity: O(1)
        """
        new_node = Node(item)
        new_node.link = self.__top
        self.__top = new_node
        self.__length += 1

    def pop(self) -> T:
        """ Pops the element at the top of the stack.
        :complexity: O(1)
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception('Stack is empty')

        item = self.__top.item
        self.__top = self.__top.link
        self.__length -= 1
        return item

    def peek(self) -> T:
        """ Returns the element at the top, without popping it from stack.
        :complexity: O(1)
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception('Stack is empty')
        return self.__top.item

    def clear(self) -> None:
        """" Resets the stack to an empty state. """
        self.__top = None
        self.__length = 0

    def __len__(self) -> int:
        """ Returns the number of elements in the stack.
        :complexity: O(1)
        """
        return self.__length

    def __str__(self) -> str:
        """ Returns a string representation of the stack."""
        i = self.__top
        stack_str = ""
        while i is not None:
            if stack_str == "":
                stack_str = str(i.item)
            else:
                stack_str = str(i.item) + ", " + stack_str
            i = i.link
        return f"<LinkedStack [{stack_str}]>"
