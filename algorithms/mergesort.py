from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.abstract_list import List
from typing import TypeVar

T = TypeVar("T")

def merge(items1: List[T] | ArrayR[T], items2: List[T] | ArrayR[T], key = lambda x:x) -> List[T] | ArrayR[T]:
    """
    Merges two sorted lists into one larger sorted list,
    containing all elements from the smaller lists.

    :param items1:
    :param items2: Two lists or arrays, they must be of the same type.
    :param key: A function used to create a custom sorting order for the inputs, see usage.
        Named functions can also be used:    
    ```python
    def key_func(obj):
        if obj.type == "X":
            return obj.x
        else:
            return obj.y
    merge(arr1, arr2, key_func)
    ```

    :returns:
    The sorted list in the same type as the input lists.

    :raises ValueError:
    When two collections of items are different types.

    ### Complexity:
    Best/Worst Case: O(n), n = len(items1) + len(items2).
    
    ### Usage
    >>> l1 = LinkedList()
    >>> l2 = LinkedList()
    >>> l1.append("B") 
    >>> l1.append("f")
    >>> l2.append("a")
    >>> l2.append("Z")
    >>> merge(l1, l2)
    <LinkedList ["B", "a", "Z", "f"]>
    >>> merge(l1, l2, lambda s: s.upper())
    <LinkedList ["a", "B", "f", "Z"]>
    """
    if type(items1) is not type(items2):
        raise ValueError(f"cannot merge collections '{type(items1).__name__}' and '{type(items2).__name__}' of differing type")
    if type(items1) is ArrayR:
        return _merge_array(items1, items2, key)
    arr1 = ArrayR.from_list(items1)
    arr2 = ArrayR.from_list(items2)
    arr3 = _merge_array(arr1, arr2, key)
    #Create new list of same type as input
    res = type(items1)()
    for item in arr3:
        res.append(item)
    return res

def _merge_array(arr1: ArrayR[T], arr2: ArrayR[T], key) -> ArrayR[T]:
    
    n = len(arr1) + len(arr2)
    res = ArrayR(n)
    ia = 0
    ib = 0
    
    for _ in range(n):
        if ia >= len(arr1):
            res[ia + ib] = arr2[ib]
            ib += 1
        elif ib >= len(arr2):
            res[ia + ib] = arr1[ia]
            ia += 1
        elif not key(arr2[ib]) < key(arr1[ia]):
            res[ia + ib] = arr1[ia]
            ia += 1
        else:
            res[ia + ib] = arr2[ib]
            ib += 1
    return res

def _mergesort_array(array: ArrayR, key) -> ArrayR:
    if len(array) <= 1:
        return array
    
    # Split the list into two halves
    break_index = (len(array)+1) // 2
    
    # Create two new lists to hold the two halves.
    
    left_half = ArrayR(break_index)
    right_half = ArrayR(len(array) - break_index)

    # Now fill the two halves with the elements from the original list
    # Left half
    for i in range(break_index):
        left_half[i] = array[i]
    
    # Right half
    for i in range(break_index, len(array)):
        right_half[i - break_index] = array[i]
    
    # Recursively sort the two halves and merge them
    arr1 = _mergesort_array(left_half, key)
    arr2 = _mergesort_array(right_half, key)
    return _merge_array(arr1, arr2, key)

def mergesort(items: List[T] | ArrayR[T], key = lambda x: x) -> List[T] | ArrayR[T]:
    """
    Sort a list or array using the mergesort algorithm.

    :param items: An ArrayList, LinkedList or ArrayR of items to sort.
    :param key: A function used to create a custom sorting order for the inputs, see usage and merge.

    :returns: A sorted list/array of the same type as the input.

    ### Complexity:
    Best/Worst Case: O(NlogN) where N is the length of the list/array.

    ### Usage:
    >>> arr = Array.from_list(["Z", "a", "B", "e"])
    >>> mergesort(arr)
    ["B", "Z", "a", "e"]
    >>> mergesort(arr, lambda s: s.upper())
    ["a", "B", "e", "Z"]
    """
    if type(items) is ArrayR:
        return _mergesort_array(items, key)
    else:
        array = ArrayR.from_list(items)
        array = _mergesort_array(array, key)
        #Create new list of same type as input
        res = type(items)() 
        for item in array:
            res.append(item)
        return res
