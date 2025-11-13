from typing import TypeVar, Generic
T = TypeVar('T')
K = TypeVar('K')

class BinaryNode(Generic[K, T]):
    """ Simple binary node.
    Has two links two more nodes.
    Has general attribute size which may store depth, number of nodes in subtree or any other metadata.
    """
    def __init__(self, item: T = None, key: K = None, size: int = 0):
        self.item = item
        self.key = key if key is not None else item
        self.size = size
        self.left: BinaryNode[K, T] | None = None
        self.right: BinaryNode[K, T] | None = None

    def __str__(self):
        return f"BinaryNode({self.item}, {self.key}, {self.size}, {'...' if self.left else 'None'}, {'...' if self.right else 'None'})"

    def __repr__(self):
        return str(self)