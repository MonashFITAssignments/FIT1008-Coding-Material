from __future__ import annotations
from data_structures.abstract_list import List, T
from data_structures.node import Node


class LinkedListIterator:
    """ Iterator for LinkedList. """
    def __init__(self, parent_list:LinkedList[T]):
        self.__curr:Node[T] | None = None
        self.__prev:Node[T] | None = None
        self.__parent = parent_list

    def __iter__(self):
        return self

    def __next__(self) -> T:
        if self.__curr is None:
            self.__curr = self.__parent._LinkedList__head
            if self.__curr is None:
                raise StopIteration
            return self.__curr.item

        else:
            if self.__curr.link is None:
                raise StopIteration
            self.__prev = self.__curr
            self.__curr = self.__curr.link
            return self.__curr.item
        
    def insert_before(self, item:T):
        new_node = self.__parent._insert_after_node(item, self.__prev)
        if self.__curr is None:
            pass
        else:
            self.__prev = new_node

    def insert_after(self, item:T):
        self.__parent._insert_after_node(item, self.__curr)
        

    def delete_current(self):
        self.__parent._delete_after_node(self.__prev)
        self.__curr = self.__prev
        

    def delete_next(self):
        self.__parent._delete_after_node(self.__curr)
        

    def set_current(self, item):
        self.__curr.item = item

    def has_next(self) -> bool:
        return self.__get_next_node() is not None

    def peek(self) -> T:
        return self.__get_next_node().item
    
    def __get_next_node(self) -> Node[T] | None:
        if self.__curr is None:
            return self.__parent._LinkedList__head
        return self.__curr.link

class LinkedList(List[T]):
    """ Linked-node based implementation of List ADT. """

    def __init__(self):
        List.__init__(self)
        self.__head = None
        self.__rear = None
        self.__length = 0

    def clear(self):
        """ Clear the list. """
        List.clear(self)
        self.__head = None
        self.__rear = None
        self.__length = 0

    def __setitem__(self, index: int, item: T) -> None:
        """ Insert the item at a given position. """
        node_at_index = self.__get_node_at_index(index)
        node_at_index.item = item

    def __getitem__(self, index: int) -> T:
        """ Return the element at a given position. """
        node_at_index = self.__get_node_at_index(index)
        return node_at_index.item

    def __len__(self) -> int:
        """ Return the number of elements in the list. """
        return self.__length

    def __iter__(self):
        """ Iterate through the list. """
        return LinkedListIterator(self)

    def __contains__(self, item: T) -> bool:
        """ Check if the item is in the list. """
        current = self.__head
        while current is not None and current.item != item:
            current = current.link
        return current is not None

    def append(self, item: T) -> None:
        """ Append the item to the end of the list. 
        :complexity: Given we have a reference to the rear of the list, this is O(1).
        """
        new_node = Node(item)
        if self.__head is None:
            self.__head = new_node
        else:
            self.__rear.link = new_node
        self.__rear = new_node
        self.__length += 1

    def __get_node_at_index(self, index: int) -> Node[T]:
        if -1 * len(self) <= index and index < len(self):
            if index < 0:
                index = len(self) + index
            current = self.__head
            for _ in range(index):
                current = current.link
            return current
        else:
            raise IndexError('Out of bounds access in list.')
    
    def _insert_after_node(self, item:T, node:Node[T]):
        if node is None:
            self.insert(0, item)
            return self.__head
        else:
            new_node = Node(item)
            new_node.link = node.link
            node.link = new_node
            self.__length += 1
            if node is self.__rear:
                self.__rear = new_node
            return new_node

    def _delete_after_node(self, node:Node[T]):
        if node is None:
            self.delete_at_index(0)
        else:
            node.link = node.link.link
            self.__length -= 1
            if node.link is None:
                self.__rear = node

    def index(self, item: T) -> int:
        """
        Find the position of a given item in the list.
        :complexity:
            Best: O(1) if the item is at the head of the list.
            Worst: O(N) where N is the number of items in the list. Happens when the item is at
                the end of the list or it doesn't exist in the list.
        """
        current = self.__head
        index = 0
        while current is not None and current.item != item:
            current = current.link
            index += 1
        if current is None:
            raise ValueError('Item is not in list')
        else:
            return index

    def delete_at_index(self, index: int) -> T:
        if not self.is_empty():
            if index > 0:
                previous_node = self.__get_node_at_index(index-1)
                item = previous_node.link.item
                previous_node.link = previous_node.link.link
            elif index == 0:
                item = self.__head.item
                self.__head = self.__head.link
                previous_node = self.__head
            else:
                raise ValueError("Index out of bounds")

            if index == len(self) - 1:
                self.__rear = previous_node

            self.__length -= 1
            return item
        else:
            raise ValueError("Index out of bounds: list is empty")

    def insert(self, index: int, item: T) -> None:
        new_node = Node(item)
        if index == 0:
            new_node.link = self.__head
            self.__head = new_node
        else:
            previous_node = self.__get_node_at_index(index-1)
            new_node.link = previous_node.link
            previous_node.link = new_node

        if index == len(self):
            if len(self) > 0:
                self.__rear.link = new_node
            self.__rear = new_node

        self.__length += 1

    def is_empty(self) -> bool:
        """ Check if the list is empty. """
        return len(self) == 0

    def __str__(self) -> str:
        if not len(self):
            return "Linked List []"

        return "Linked List [" + ", ".join(str(item) for item in self) + "]"

    def __repr__(self) -> str:
        return str(self)
