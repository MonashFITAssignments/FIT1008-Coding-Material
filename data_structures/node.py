from typing import TypeVar, Generic
T = TypeVar('T')
K = TypeVar('K')

class Node(Generic[T]):
    """ Simple linked node.
    It contains an item and has a reference to next node. It can be used in
    linked structures.
    """

    def __init__(self, item: T = None):
        self.item = item
        self.link: Node[T] | None = None

    def __str__(self) -> str:
        return f"Node({self.item}, {'...' if self.link else 'None'})"

class BinaryNode(Generic[K, T]):
    """ Simple binary node.
    Has two links two more nodes.
    Has general attribute size which may store depth, number of nodes in subtree or any other metadata.
    """
    def __init__(self, item: T = None, key: K = None, size: int = 0):
        self.__item = item
        self.__key = key if key is not None else item
        self.__size = size
        self.__left: BinaryNode[K, T] | None = None
        self.__right: BinaryNode[K, T] | None = None

    @property
    def item(self) -> T:
        return self.__item

    @property
    def key(self) -> K:
        return self.__key

    @property
    def size(self) -> int:
        return self.__size

    @size.setter
    def size(self, size: int) -> None:
        self.__size = size

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, value: 'BinaryNode[K, T]') -> None:
        self.__left = value

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, value: 'BinaryNode[K, T]') -> None:
        self.__right = value

    def __str__(self):
        return f"BinaryNode({self.item}, {self.key}, {self.size}, {'...' if self.left else 'None'}, {'...' if self.right else 'None'})"
