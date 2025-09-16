from data_structures.abstract_hash_table import HashTable
from data_structures.referential_array import ArrayR
from data_structures.linked_list import LinkedList
from typing import TypeVar, Tuple

V = TypeVar('V')

class SeparateChainingTable(HashTable[str, V]):
    """
    Separate Chaining Hash Table Implementation using a Linked List.
    It currently rehashes the primary cluster to handle deletion.

    constants:
        DEFAULT_TABLE_SIZE: default table size used in the __init__
        DEFAULT_HASH_TABLE: default hash base used for the hash function

    attributes:
        length: number of elements in the hash table
        array: used to represent our internal array
    """

    DEFAULT_TABLE_SIZE = 17
    DEFAULT_HASH_BASE = 31

    def __init__(self, table_size: int = DEFAULT_TABLE_SIZE) -> None:
        """
        :complexity: O(N) where N is the table size.
        """
        if table_size <= 0:
            raise ValueError("Table size should be larger than 0.")
        
        self._table: ArrayR[LinkedList | None] = ArrayR(table_size)
        self._length = 0

    def hash(self, key: str) -> int:
        """
        Universal Hash function
        :returns: a valid position (0 <= value < table_size) in the hash table
        :complexity: O(K) where K is the length of the key
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % len(self._table)
            a = (a * SeparateChainingTable.DEFAULT_HASH_BASE % (len(self._table) - 1)) + 1
        return value

    @property
    def table_size(self) -> int:
        return len(self._table)

    def items(self) -> ArrayR[Tuple[str, V]]:
        """
        Returns all keys in the hash table
        :complexity: O(N + S) where N is the number of items in our hash table
        and S is the table size. Depending on how the table is created, if the table size
        is not variable (e.g. it's always using the default size), then S can be ignored as
        a constant, simplifying the complexity to O(N).
        """
        res = ArrayR(self._length)
        i = 0
        for list in self._table:
            if list is not None:
                for item in list:
                    res[i] = item
                    i += 1
        return res
    
    def is_empty(self) -> bool:
        """
        Returns whether the hash table is empty
        :complexity: O(1)
        """
        return self._length == 0

    def is_full(self) -> bool:
        """
        Returns whether the hash table is full
        :complexity: O(1)
        """
        return len(self) == len(self.__array)

    def __delitem__(self, key: str) -> None:
        """
        Deletes an item from our hash table
        :raises KeyError: when the key doesn't exist
        :complexity:
            Best: O(K) where K is the length of the key (for hashing). Happens when the chain (linked list) does
                not have many elements.
            Worst: O(N + K) where N is the number of items in the hash table and K is the length of the key.
                Happens when the position has many elements and we have to traverse the linked list.
        """
        position = self.hash(key)
        if self._table[position] is None:
            raise KeyError(key)

        for index, item in enumerate(self._table[position]):
            if item[0] == key:
                if len(self._table[position]) <= 1:
                    self._table[position] = None
                else:
                    self._table[position].delete_at_index(index)

                self._length -= 1
                return

        raise KeyError(key)

    def __getitem__(self, key: str) -> V:
        """
        Get the data associated with a key
        :raises KeyError: when the key doesn't exist
        :complexity:
            Best: O(K) where K is the length of the key (for hashing). Happens when the chain at the position
                doesn't have many items.
            Worst: O(N + K) where N is the number of items in the hash table and K is the length of the key.
                Happens when we have to traverse a long chain to find the key.
        """
        position = self.hash(key)
        if self._table[position] is None:
            raise KeyError(key)
        for item in self._table[position]:
            if item[0] == key:
                return item[1]

        raise KeyError(key)

    def __setitem__(self, key: str, data: V) -> None:
        """
        Set a (key, data) pair in our hash table
        :complexity:
            Best: O(K) where K is the length of the key (for hashing). Happens when the position is empty.
            Worst: O(N + K) where N is the number of items in the hash table and K is the length of the key.
                Happens when the position is not empty and we have to traverse the linked list.
        """
        position = self.hash(key)
        if self._table[position] is None:
            self._table[position] = LinkedList()

        # Attempt to find the key in our linked list
        if len(self._table[position]) > 0:
            for index, item in enumerate(self._table[position]):
                if item[0] == key:
                    # If found update the data
                    self._table[position][index] = (key, data)
                    return

        # Insert at the beginning for better time complexity
        self._table[position].insert(0, (key, data))
        self._length += 1

    def __iter__(self):
        """
        Returns an iterator for the hash table
        :complexity: O(N) where N n is the number of items in our hash table
        """
        for list in self._table:
            if list is not None:
                for item in list:
                    yield item[1]

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self._length

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular order)
        :complexity: O(N) where N is the number of items in our hash table
        """
        items = self.items()
        items = '\n'.join(map(lambda x: f"({x[0]}, {x[1]})", items))
        return f"<SeparateChainingTable\n{items}\n>"
