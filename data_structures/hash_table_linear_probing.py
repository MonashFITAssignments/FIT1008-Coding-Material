from __future__ import annotations
from typing import TypeVar, Tuple, List
from data_structures.abstract_hash_table import HashTable
from data_structures.referential_array import ArrayR
from data_structures.dunder_protected import protected_names
V = TypeVar('V')


class LinearProbeTable(HashTable[str, V], protected_names("_size_index", "_array", "_length", "_hash_base", "_handleProbing")):
    """
    Linear Probe Table.
    Defines a Hash Table using Linear Probing for collision resolution.
    If you want to use this with a different key type, you should override the hash function.
    
    Type Arguments:
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    _TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    def __init__(self, sizes: None | List[int] = None, hash_base: int | None = 31) -> None:
        """
        :param sizes: Optional list of sizes to use for the hash table.
                      If not provided, a default list of sizes will be used.
        :complexity: O(1) - Assuming the default sizes are used, we can assume the array is created in O(1) time.
            If you use this function in any way that passes some variable input for the sizes, then the complexity
            needs to change accordingly.
        """
        if sizes is not None:
            self._TABLE_SIZES = sizes
        else:
            self._TABLE_SIZES = LinearProbeTable._TABLE_SIZES

        self._size_index = 0
        self._array: ArrayR[tuple[str, V]] = ArrayR(max(self._TABLE_SIZES[self._size_index], 2))
        self._length = 0
        self._hash_base = hash_base

    def hash(self, key: str) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.
        :complexity: O(K) where K is the length of the key.
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = (a * self._hash_base % (self.table_size - 1)) + 1
        return value

    @property
    def table_size(self) -> int:
        return len(self._array)

    def _handle_probing(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using linear probing.
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

        for _ in range(self.table_size):
            if self._array[position] is None:
                # Empty spot. Am I upserting or retrieving?
                if is_insert:
                    return position
                else:
                    raise KeyError(key)
            elif self._array[position][0] == key:
                return position
            else:
                # Taken by something else. Time to linear probe.
                position = (position + 1) % self.table_size

        if is_insert:
            raise RuntimeError("Table is full!")
        else:
            raise KeyError(key)

    def items(self) -> ArrayR[Tuple[str, V]]:
        """
        Returns all keys in the hash table.
        :complexity: O(N) where N is the table size.
        """
        res = ArrayR(self._length)
        i = 0
        for x in range(self.table_size):
            if self._array[x] is not None:
                res[i] = self._array[x]
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
        return len(self) == len(self._array)

    def __delitem__(self, key: str) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :complexity: 
            Best: O(K) when the key is at the beginning of the table and no cluster is present to rehash.
            Worst: O(N * (N + K)) when the key is at the beginning of a large cluster and we have to effectively
                rehash all elements. And each element has to linear probe over all (or a factor of) other elements currently
                in the table. This is assuming K here is representing an average key length.
            N is the number of items in the table.
            K is the length of the key.

        :raises KeyError: when the key doesn't exist.
        """
        position = self._handle_probing(key, False)
        # Remove the element
        self._array[position] = None
        self._length -= 1
        # Start moving over the cluster
        position = (position + 1) % self.table_size
        while self._array[position] is not None:
            key2, value = self._array[position]
            self._array[position] = None
            # Reinsert.
            newpos = self._handle_probing(key2, True)
            self._array[newpos] = (key2, value)
            position = (position + 1) % self.table_size

    def __getitem__(self, key: str) -> V:
        """
        Get the value at a certain key

        :complexity: See linear probe.
        :raises KeyError: when the key doesn't exist.
        """
        position = self._handle_probing(key, False)
        return self._array[position][1]

    def __setitem__(self, key: str, data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity:
            Best: Same as linear probe, when no rehashing is needed.
            Worst: Same as __rehash.
        :raises FullError: when the table cannot be resized further.
        """

        position = self._handle_probing(key, True)

        if self._array[position] is None:
            self._length += 1

        self._array[position] = (key, data)

        if len(self) > self.table_size / 2:
            self.__rehash()

    def __rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity:
            Best: O(N * K) happens when all items can be inserted immediately after being hashed
                with no probing needed.
            Worst: O(N * (N + K)) happens when all items need maximum probing to be inserted in the new table.
                This is assuming K here is representing an average key length.

            N is the number of items in the table.
            K is the length of the key.
            This analysis is assuming the default table sizes are used, and thus the
                cost of creating a new table is constant. This assumption can be extended to any table size
                as long as the sizes are growing by a constant factor (e.g. each table size is almost double the previous one).
        """
        old_array = self._array
        if self._size_index + 1 == len(self._TABLE_SIZES):
            if self.is_full():
                raise RuntimeError("Table is full!")

            # Cannot be resized further.
            return
        self._size_index += 1
        self._array = ArrayR(self._TABLE_SIZES[self._size_index])
        self._length = 0
        for item in old_array:
            if item is not None:
                key, value = item
                self[key] = value

    def __len__(self) -> int:
        """
        Returns the number of elements in the hash table
        """
        return self._length

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        """
        items = self.items()
        items = '\n'.join(map(lambda x: f"({x[0]}, {x[1]})", items))
        return f"<LinearProbeTable\n{items}\n>"