from typing import TypeVar, Generic
T = TypeVar('T')

class Node(Generic[T]):
    """ Simple linked node.
    It contains an item and has a reference to next node. It can be used in
    linked structures.
    """

    def __init__(self, item: T = None):
        self._item = item
        self._link: Node[T] | None = None

    def __str__(self) -> str:
        return f"Node({self._item}, {'...' if self._link else 'None'})"

class BinaryNode(Generic[K, T]):
    """ Simple binary node.
    Has two links two more nodes.
    Has general attribute size which may store depth, number of nodes in subtree or any other metadata.
    """
    def __init__(self, item: T = None, key: K = None, size: int = 0):
        self._item = item
        self._key = key if key is not None else item
        self._size = size
        self._left: BinaryNode[K, T] | None = None
        self._right: BinaryNode[K, T] | None = None

    def __str__(self):
        return f"BinaryNode({self._item}, {self._key}, {self._size}, {'...' if self._left else 'None'}, {'...' if self._right else 'None'})"
        return f"Node({self.item}, {'...' if self.link else 'None'})"
