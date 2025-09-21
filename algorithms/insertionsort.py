from __future__ import annotations

from data_structures.referential_array import ArrayR, T
from data_structures.abstract_list import List
from typing import Callable, Any

def insertion_sort(items: ArrayR[T] | List[T], key: Callable[[T], Any] = lambda x: x) -> ArrayR[T] | List[T]:
    """
    Sort an array or list using insertion sort.
    It sorts arrays inplace (mutation), and returns a copy for lists.
    The returned list is of the same type as the argument.

    :complexity:
        Best case O(N) when the list is mostly sorted
        Worst case O(N^2)
        Where N is the length of the list.
    """
    arr = items if type(items) is ArrayR else ArrayR.from_list(items)

    for i in range(1,len(arr)):
        i_item = arr[i]
        i_key = key(i_item)
        j = i - 1
        while j >= 0 and i_key < key(arr[j]):
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j+1] = i_item
    
    if type(items) is ArrayR:
        return arr

    # Construct a new list of same type as items
    res = type(items)()
    for item in arr:
        res.append(item)
    return res
