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
