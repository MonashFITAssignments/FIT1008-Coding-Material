from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.hash_table_linear_probing import LinearProbeTable


class DoubleHashingTable(LinearProbeTable):
    """
    Double Hashing Probe Table.
    Defines a Hash Table using Double Hashing for collision resolution.
    If you want to use this with a different key type, you should override the hash function.
    """

    def hash2(self, key: str) -> int:
        return 1 + (hash(key) % (self.table_size - 1))

    def __handle_probing(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using double hashing probing.
        :complexity:
            Best: O(K) happens when we hash the key and the position is empty.
            Worst: O(N + K) happens when we hash the key but the position is taken and we have to
                search the entire table.
            N is the number of items in the table.
            K is the length of the key.
        :raises KeyError: When the key is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        # Initial position
        position = self.hash(key)
        step = self.hash2(key)

        for _ in range(self.table_size):
            if self.__array[position] is None:
                # Empty spot. Am I upserting or retrieving?
                if is_insert:
                    return position
                else:
                    raise KeyError(key)
            elif self.__array[position][0] == key:
                return position
            else:
                # Taken by something else. Time to linear probe.
                position = (position + step) % self.table_size


        if is_insert:
            raise RuntimeError("Table is full!")
        else:
            raise KeyError(key)
