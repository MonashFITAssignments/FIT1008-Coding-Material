from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.hash_table_linear_probing import LinearProbeTable


class QuadraticProbeTable(LinearProbeTable, private="array,length,size_index,hash_base"):
    """
    Quadratic Probe Table.
    Defines a Hash Table using Quadratic Probing for collision resolution.
    If you want to use this with a different key type, you should override the hash function.
    """

    def __handle_probing(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using quadratic probing.
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
        orig_position = position
        step = 1

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
                position = (orig_position + step*step) % self.table_size
                step += 1


        if is_insert:
            raise RuntimeError("Table is full!")
        else:
            raise KeyError(key)

    def __delitem__(self, key: str) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :complexity:
            Best: O(N + K) when we reinsert without probing.
            Worst: O(N * (N + K)) every element has to be reinserted.
            N is the number of items in the table.
            K is the length of the key.

        :raises KeyError: when the key doesn't exist.
        """
        position = self.__handle_probing(key, False)
        self.__array[position] = None
        self.__length -= 1

        old_array = self.__array
        self.__array = ArrayR(self.table_size)
        self.__length = 0
        for item in old_array:
            if item is not None:
                key, value = item
                self[key] = value
    
    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        """
        items = self.items()
        items = '\n'.join(map(lambda x: f"({x[0]}, {x[1]})", items))
        return f"<QuadraticProbeTable\n{items}\n>"
