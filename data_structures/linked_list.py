from data_structures.abstract_list import List, T
from data_structures.node import Node

class LinkedListIterator:
    """ Iterator for LinkedList. """
    def __init__(self, head_node: Node):
        self._current = head_node

    def __iter__(self):
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        else:
            item = self._current._item
            self._current = self._current._link
            return item

class LinkedList(List[T]):
    """ Linked-node based implementation of List ADT. """

    def __init__(self):
        List.__init__(self)
        self._head = None
        self._rear = None
        self._length = 0

    def insert(self, index: int, item: T) -> None:
        """
        Inserts a new item before position index.
        :complexity:
            Best: O(1) if adding to the beginning or end of the list.
            Worst: O(N) where N is the number of items in the list. Occurs when inserting towards the end of the list (but not at the end).
        """
        if index == len(self):
            self.append(item)
        else:
            new_node = Node(item)
            if index == 0:
                new_node._link = self._head
                self._head = new_node
            else:
                previous_node = self.__get_node_at_index(index-1)
                new_node._link = previous_node._link
                previous_node._link = new_node

            self._length += 1

    def append(self, item: T) -> None:
        """ Append the item to the end of the list.
        :complexity: Given we have a reference to the rear of the list, this is O(1).
        """
        new_node = Node(item)
        if self._head is None:
            self._head = new_node
        else:
            self._rear._link = new_node
        self._rear = new_node
        self._length += 1

    def clear(self):
        """ Clear the list. """
        List.clear(self)
        self._head = None
        self._rear = None
        self._length = 0

    def delete_at_index(self, index: int) -> T:
        """
        Deletes an item at position index.
        :complexity:
            Best: O(1) Deleting the first item in the list.
            Worst: O(N) Deleting the last item in the list, where N is the number of items in the list.
        """
        if not self.is_empty():
            if index > 0:
                previous_node = self.__get_node_at_index(index-1)
                item = previous_node._link._item
                previous_node._link = previous_node._link._link
            elif index == 0:
                item = self._head._item
                self._head = self._head._link
                previous_node = self._head
            else:
                raise ValueError("Index out of bounds")

            if index == len(self) - 1:
                self._rear = previous_node

            self._length -= 1
            return item
        else:
            raise ValueError("Index out of bounds: list is empty")

    def index(self, item: T) -> int:
        """
        Find the position of a given item in the list.
        :complexity:
            Best: O(1) if the item is at the head of the list.
            Worst: O(N) where N is the number of items in the list. Happens when the item is at
                the end of the list or it doesn't exist in the list.
        """
        current = self._head
        index = 0
        while current is not None and current._item != item:
            current = current._link
            index += 1
        if current is None:
            raise ValueError('Item is not in list')
        else:
            return index

    def __get_node_at_index(self, index: int) -> Node[T]:
        """
        Gets the nodes at a given index
        :complexity:
            Best: O(1) if the index is 0 or len(list) - 1
            Worst: O(N) where N is the number of items in the list. Happens when the item is close
                to the end of the list or it doesn't exist in the list.
        """
        if -1 * len(self) <= index and index < len(self):
            if index < 0:
                index = len(self) + index
            elif index == len(self) - 1:
                return self._rear
            current = self._head
            for _ in range(index):
                current = current._link
            return current
        else:
            raise IndexError('Out of bounds access in list.')

    def __getitem__(self, index: int) -> T:
        """ Return the element at a given position.
        :complexity: See self.__get_node_at_index().
        """
        node_at_index = self.__get_node_at_index(index)
        return node_at_index._item

    def __setitem__(self, index: int, item: T) -> None:
        """ Insert the item at a given position.
        :complexity: See self.__get_node_at_index().
        """
        node_at_index = self.__get_node_at_index(index)
        node_at_index._item = item

    def __iter__(self):
        """ Iterate through the list. """
        return LinkedListIterator(self._head)

    def __len__(self) -> int:
        """ Return the length of the list. """
        return self._length

    def __str__(self) -> str:
        if not len(self):
            return "<LinkedList []>"

        return "<LinkedList [" + ", ".join(str(item) for item in self) + "]>"
